"""This module contains helper functions for the mosaic framework"""

from contextlib import contextmanager
from datetime import datetime
import functools
import os
import pathlib
import types
import typing
from logging import Logger
import uuid

from mosaic_orchestrator import tree
from mosaic_orchestrator.cachable_task import CachableTask, CacheResult
from mosaic_orchestrator.cache import Cache
from mosaic_orchestrator.result import ValidationError, Result, ErrorType, ErrorDefinition
from mosaic_orchestrator.task import TaskNode, Task, TaskParameter, TaskParameterException, Calculated, \
    wrap_in_task_parameter, TaskState, is_calculated, \
    is_calculated_or_mutable_or_const, is_mutable, CalculatedAccessException, is_const, Const, _is_task_parameter, \
    get_task_parameters, _get_cache_dir
from mosaic_orchestrator.tool import Tool
from mosaic_orchestrator.tree import Path, concat
from mosaic_orchestrator.utils import get_type_annotations, get_all_parameters, get_type_of_class_field, \
    is_function, ListHandler

_INJECTED_DEFAULTS = "INJECTED_DEFAULTS"


class MosaicException(Exception):
    """Generic mosaic exception holder"""
    def __init__(self, error: ErrorDefinition):
        self.error = error


class TaskTreeException(Exception):
    """raised if the task tree can not be constructed"""


def find_node(task_tree: TaskNode, path: Path, check_parameter: bool = True) -> Result[TaskNode]:
    """Find a node identified by its path in a trask tree

    Args:
        check_parameter: when True the path is expected to point to a TaskParameter which is then
            checked to be valid.

    Returns:
        A result containing the TaskNode if it was found or an error if it was not found.
    """
    current_node = task_tree

    if path.length == 1 and check_parameter:
        result = _check_parameter(path.target, task_tree.value)
        if result.failure:
            return result

    for step in path.steps[:-1]:
        children = current_node.children
        step_list = list(filter(lambda child: child.value.path.target == step, children)) \
            # pylint: disable=cell-var-from-loop
        if not step_list:
            return Result.Fail(f"'{step}' is no child of {type(current_node.value)}")

        current_node = step_list[0]

    return Result.Ok(current_node)


def find_task(task: Task, path: Path):
    """Get a subtask of the given task identified by the relative path

    Args:
        task: the task that is used as a root
        path: the path to the target subtask. it must be relative to the given task and include it
            as a root.

    Returns:
        the instance of the subtask.
        """
    current = task

    for step in path.steps[:-1]:
        if not hasattr(current, step):
            raise TaskTreeException(
                f"'{step}' is no child of {type(current)}")

        current = getattr(current, step)

    return current


def _validate_parameter(task: Task, parameter: TaskParameter):
    """calls TaskParameters validation lamda or validate function"""
    if parameter.validate_func:
        validation = parameter.validate_func(task, parameter.value)
    else:
        validation = parameter.validate()
    return validation


def _prepare_inject_calculated_and_default(task: Task, path: Path) -> Result:
    """add check error for injection of Calculated parameter. Also remember which Default parameters
    are being injected."""
    param = getattr(task, path.target)
    if is_calculated(param):
        return Result.Fail(f"parameter {path} cannot be altered since it is set to Calculated")
    if is_const(param):
        return Result.Fail(f"parameter {path} cannot be altered since it is set to Const")
    if is_mutable(param):
        if not hasattr(task, _INJECTED_DEFAULTS):
            setattr(task, _INJECTED_DEFAULTS, [])
        defaults = getattr(task, _INJECTED_DEFAULTS)
        defaults.append(path.target)

    return Result.Ok()


def _set_param_or_wrap(instance: object, name: str, param) -> Result:
    """set a parameter to an instance, if the given parameter is not a TaskParameter it gets wrapped into it"""
    param_type = get_type_of_class_field(instance=instance, name=name)

    origin = typing.get_origin(param_type)
    if origin is not None:
        param_type = origin

    if param_type == type(param):
        if hasattr(instance, name) and isinstance(getattr(instance, name), TaskParameter):
            present_param = getattr(instance, name)
            param.description = present_param.description
            param.transient = present_param.transient
            param.validate_func = present_param.validate_func

        result = param
    else:
        try:
            if isinstance(param, TaskParameter):
                value = param.value
            else:
                value = param

            new_param = param_type(value)

            if hasattr(instance, name):
                present_param = getattr(instance, name)
                if isinstance(present_param, TaskParameter):
                    new_param.description = present_param.description
                    new_param.transient = present_param.transient
                    new_param.validate_func = present_param.validate_func

            result = new_param
        except TypeError as error:
            return Result.Fail(
                f"parameter {param_type} not instantiable with {param} of type {type(instance)} - {error}")

    setattr(instance, name, result)

    return Result.Ok(value=result)


def _evaluate_callable_parameters(node: TaskNode):
    """evaluates callable parameters"""
    _evaluate_constructor_lambdas(node)
    _evaluate_default_lambdas(node)
    _evaluate_const_lambdas(node)
    _evaluate_task_states(node)


def _evaluate_task_states(node):
    """evaluates callable (lambda) value of a TaskState"""
    for name, var in vars(node.task).items():
        if isinstance(var, TaskState) and is_function(var.value):
            try:
                var.value = var.value(node.task)
            except CalculatedAccessException:
                if not hasattr(node.task, "_runtime_evaluation_functions"):
                    node.task._runtime_evaluation_functions = {}  # pylint: disable=protected-access
                node.task._runtime_evaluation_functions[name] \
                    = functools.partial(var.value, node.task)  # pylint: disable=protected-access

                setattr(node.task, name, Calculated)


def _evaluate_default_lambdas(node):
    """evaluates callable (lambda) value of TaskParameters"""
    for name, parameter in get_task_parameters(node.task).items():
        if parameter and is_function(parameter.value):
            try:
                parameter.value = parameter.value(node.task)
            except CalculatedAccessException:
                if not hasattr(node.task, "_runtime_evaluation_functions"):
                    node.task._runtime_evaluation_functions = {}  # pylint: disable=protected-access
                node.task._runtime_evaluation_functions[name] \
                    = functools.partial(parameter.value, node.task)  # pylint: disable=protected-access
                setattr(node.task, name, Calculated)


def _evaluate_const_lambdas(node):
    """evaluates callable (lambda) value of a Const TaskParameters"""
    for name, parameter in get_all_parameters(node.task).items():
        if parameter and isinstance(parameter, Const) and is_function(parameter.value):
            try:
                parameter.value = parameter.value(node.task)
            except CalculatedAccessException:
                if not hasattr(node.task, "_runtime_evaluation_functions"):
                    node.task._runtime_evaluation_functions = {}  # pylint: disable=protected-access
                node.task._runtime_evaluation_functions[name] \
                    = functools.partial(parameter.value, node.task)  # pylint: disable=protected-access
                setattr(node.task, name, Calculated)


def _evaluate_constructor_lambdas(node):
    """evaluates callable (lambda) value of a constructor"""
    for path, task in node.injected_params:
        param = getattr(node.task, path.target)
        if is_function(param.value):
            try:
                param.value = param.value(task)
            except CalculatedAccessException:
                if not hasattr(node.task, "_runtime_evaluation_functions"):
                    node.task._runtime_evaluation_functions = {}  # pylint: disable=protected-access
                node.task._runtime_evaluation_functions[path.target] \
                    = functools.partial(param.value, task)  # pylint: disable=protected-access

                setattr(node.task, path.target, Calculated)


def _check_parameter(name, task: Task) -> Result:
    """Check if a given name is a valid parameter of a Task"""
    annotations = get_type_annotations(type(task))
    if name not in annotations.keys() and not hasattr(task, name):
        return Result.Fail(f"'{name}' is no parameter of {type(task)}")
    if hasattr(task, name) and isinstance(getattr(task, name), TaskState):
        return Result.Fail(f"'{name}' of {type(task)} is a TaskState and not settable")
    if (hasattr(task, name) and not isinstance(getattr(task, name), TaskParameter)) or (
            name in annotations.keys() and not _is_task_parameter(annotations[name])):
        return Result.Fail(f"'{name}' of {type(task)} is not a TaskParameter or subclassing it")

    return Result.Ok()


def _wrap_root(root: Task):
    """wrap the run method of a task"""
    root._old_root_run = root.run  # pylint: disable=protected-access
    root.run = types.MethodType(_root_run_wrapper, root)
    root.measure_execution_time = types.MethodType(_measure_exec_time_run_wrapper, root)
    root.track_parameter = types.MethodType(_track_parameter_wrapper, root)

@contextmanager
def _measure_exec_time_run_wrapper(self, name:str, is_root_task:bool=False) -> None:
    """
        Wrapper to measure the exection time of a nested code block.
        This measured time is forwarded to all registered trackers.
        If an exception is throw during the nested block execution, the type of
        this exception is added into the value colection and the exception is rethrown.
        The execution time until the exception is cated is logged.

        Args:
            name:   The name part of key
    """

    try:
        start_time = datetime.now()
        yield start_time


    except Exception as exc:
        for tracker in self._mosaic.execution_trackers:
            tracker.add_exception(name, value=exc)
        raise

    finally:
        end_time = datetime.now()

        for tracker in self._mosaic.execution_trackers:
            tracker.add_start_and_end_time(name, start_time=start_time, end_time=end_time, is_root_task=is_root_task)

def _track_parameter_wrapper(self, pname:str, value:any) -> None:
    """
    Wrapper to add the pname,value pair into all registered trackers.

    Args:
        pname: The name part of key
        value: The value to add
    """
    for tracker in self._mosaic.execution_trackers:
        tracker.add_parameter(pname, value)

def _root_run_wrapper(self, *args, **kwargs):
    """wrapped run method, creates current working directories, calls the run method and cleanup after run"""
    self._mosaic._startup()  # pylint: disable=protected-access

    cwd = pathlib.Path.cwd()

    try:
        os.makedirs(self._mosaic.run_directory, exist_ok=True)  # pylint: disable=protected-access
        os.chdir(self._mosaic.run_directory)  # pylint: disable=protected-access

        root_event_id = str(uuid.uuid4())
        for tracker in self._mosaic.execution_trackers:
            tracker.set_root_task_event(root_event_id)

        # forward that the current task is the root task
        # this value is required for later logging of the task execution time
        # set eventID
        new_args = dict(**kwargs, is_root_task=True)
        result = self._old_root_run(*args, **new_args)  # pylint: disable=protected-access

        os.chdir(cwd)
        self._mosaic._cleanup()  # pylint: disable=protected-access
        return result
    except Exception as error:
        os.chdir(cwd)
        self._mosaic._cleanup(error)  # pylint: disable=protected-access
        raise error from error


def _evaluate_runtime_lambdas(task):
    """evaluate the runtime lambdas of a task"""
    if hasattr(task, "_runtime_evaluation_functions"):
        for name, function in task._runtime_evaluation_functions.items():  # pylint: disable=protected-access
            _set_param_or_wrap(task, name, function())
            _try_validate_parameter(name, task)


def _try_validate_parameter(name, task: Task):
    """try to validate a parameter of a Task, rises an exception if validation fails"""
    param = getattr(task, name)
    task_type = type(task)
    if hasattr(task_type, name):
        class_param = getattr(type(task), name)
        if hasattr(class_param, "validate"):
            if class_param.validate_func:
                validation = class_param.validate_func(task, param.value)
            else:
                validation = param.validate()

            if isinstance(validation, ValidationError):
                path = concat(task.path, name)
                raise MosaicException(ErrorDefinition(
                    error_type=ErrorType.PARAMETER_ERROR,
                    message=f"Validation failed for '{path}' with value "
                            f"'{param.value}' reason: {validation.message}",
                    source=str(path)
                ))


def _collect_results(task: CachableTask) -> CacheResult:
    """collects the results of a cachable tasks cache"""
    result = CacheResult(result=task.task_result, sub_results={})

    stack = []

    stack.extend(task.get_fields_of_type(CachableTask))

    while stack:
        current_task = stack.pop()

        stack.extend(current_task.get_fields_of_type(CachableTask))

        if not current_task.task_hash:
            continue

        result.sub_results[current_task.path.remove(task.path)] = current_task.task_hash

    return result


def _inject_log_to_task_tool(task):
    """inject the task logger to a tool, during execution of a task the used tool should use the logger of the task"""
    for _, var in vars(task).items():
        if isinstance(var, Tool):
            _inject_log_to_tools(tool=var, log=task._mosaic_logger)  # pylint: disable=protected-access


def _inject_log_to_tools(tool: Tool, log: Logger):
    """inject log to a tool"""
    for name, annotation_type in get_type_annotations(type(tool)).items():

        if annotation_type is Logger:
            setattr(tool, name, log)
        if issubclass(annotation_type, Tool):
            _inject_log_to_tools(getattr(tool, name), log)


def _get_cached_result_and_logs(task: CachableTask):
    """get cached results and logs for a task, returns None if no cache is available"""
    with Cache(_get_cache_dir(task)) as cache:
        result: CacheResult = cache.get(task.task_hash)

        if result is None:
            return None, None

        logs = cache.get(task.task_hash + "_logs")
        if task._is_task_invalid(result, cache):  # pylint: disable=protected-access
            cache.clear(task.task_hash)
            cache.clear(task.task_hash + "_logs")
            task.task_result = None
            return None, None

        return result.result, logs


def _cache_log(
        handler: ListHandler,
        task: Task
):
    """put the logs of a task into the cache"""
    if not handler.log_list:
        return

    with Cache(_get_cache_dir(task)) as cache:
        key = task.task_hash + "_logs"
        try:
            cache.put(key, handler.log_list)
        except Exception as error:
            raise AttributeError(
                f"{error} - Task parameters and results must be serializable using pickle package"
            ) from error


def _inject_calculated_params(task, task_params):
    """Inject parameters passed to run method via task_params. Parameters that were already injected
    from top level are ignored"""
    if hasattr(task, "_calculated_params"):
        calculated = task._calculated_params.items()  # pylint: disable=protected-access
    else:
        calculated = {}

    if task_params:
        for name, _ in task_params.items():
            if name not in [path for path, _ in calculated]:
                raise TaskParameterException(
                    f"Unexpected run task_params ({name} in {task_params}) for task {type(task)}")
    for name, _ in calculated:
        path = Path(name)
        current_task = find_task(task, path)
        # ignore parameters that were injected from top level
        if hasattr(current_task, _INJECTED_DEFAULTS):
            if path.target in getattr(current_task, _INJECTED_DEFAULTS):
                continue
        if task_params and name in task_params:
            result = _set_param_or_wrap(current_task, path.target,
                                        wrap_in_task_parameter(value=task_params[name]))
            if result.failure:
                raise TaskParameterException(result.error)

            _try_validate_parameter(path.target, current_task)
            continue

        if current_task._calculated_params and path.target in current_task._calculated_params:  # pylint: disable=protected-access
            param = current_task._calculated_params[path.target]  # pylint: disable=protected-access

            if isinstance(param, Const) and param.value is not None:
                result = _set_param_or_wrap(
                    current_task, path.target,
                    wrap_in_task_parameter(value=param.value)
                )
                if result.failure:
                    raise TaskParameterException(result.error)
                _try_validate_parameter(path.target, current_task)
                continue

        if current_task._calculated_default_values and path.target in current_task._calculated_default_values:  # pylint: disable=protected-access
            result = _set_param_or_wrap(
                current_task, path.target,
                wrap_in_task_parameter(value=current_task._calculated_default_values[path.target])  # pylint: disable=protected-access
            )
            if result.failure:
                raise TaskParameterException(result.error)
            _try_validate_parameter(path.target, current_task)
            continue
        raise TaskParameterException(
            f"Missing parameter in calculated task_params for {current_task.path}.{path.target}")


def _filter_calculated_params(params):
    """filter only calculated params"""
    return dict(
        filter(lambda param: is_calculated_or_mutable_or_const(param[1]), params.items())
    )


def _add_prefix_to_all_params(root: TaskNode, prefix):
    """adds a prefix to all parameters according the task tree"""
    tree.traverse(root, lambda node: _add_prefix_to_parameters(node, prefix))


def _add_prefix_to_parameters(node: TaskNode, prefix):
    """adds a given prefix to all parameters of a task"""
    for param_name in list(node.parameters.keys()):
        new_name = f"{prefix}.{param_name}"
        node.parameters[new_name] = node.parameters[param_name]
        del node.parameters[param_name]
