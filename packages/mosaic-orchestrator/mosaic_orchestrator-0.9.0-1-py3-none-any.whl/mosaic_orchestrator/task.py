"""this module contains different types of tasks and some helper functions"""
from __future__ import annotations

import copy
import os.path
import pickle
import shutil
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging import Logger
from typing import Dict, List, Tuple, Optional, Callable, Type, TypeVar, Generic, Protocol, \
    runtime_checkable, Any

from mosaic_orchestrator import tree
from mosaic_orchestrator.pdk import PDK, PdkItem
from mosaic_orchestrator.result import Validation, ValidationError, ValidationSuccess, ErrorDefinition, \
    ErrorType, Result
from mosaic_orchestrator.tree import Path
from mosaic_orchestrator.utils import get_all_parameters, get_type_annotations


class TaskParameterException(Exception):
    """TaskParameterException is raised when a task parameter is not handled right,
     e.g. unexpected task_params in run()"""


TaskStateType = TypeVar('TaskStateType')


@dataclass
class TaskState(Generic[TaskStateType]):
    """Generic class that encapsulates the state of a task.

    This class can be used similarly to a TaskParameter. It is used for caching and is intended to
    be used only from within a task. Hence, it can neither be modified from a parent task nor from
    the top level.
    """
    value: Optional[TaskStateType] = None
    """the value that is encapsulated in this instance."""


class CalculatedAccessException(Exception):
    """raised if a calculated parameter """


class _Calculated:
    """used to mark a parameter as calculated by a task higher in the task-hierarchy"""
    # pylint: disable=too-few-public-methods

    @property
    def value(self):
        """raises CalculatedAccessException on value access"""
        raise CalculatedAccessException()


Calculated = _Calculated()
"""Used to mark a parameter of a subtask as calculated by the current task.

This means that the parameter is no longer settable from a higher hierarchy. Calculated parameters
need to be passed to the run method of the subtask.

Example:
    This example shows how to set Calculated parameters for a child task::

        class Addition(Task):
            summand1 = TaskParameter()
            summand2 = TaskParameter()

            def run(self, *args, **kwargs):
                return self.summand1.value + self.summand2.value


        class MyTask(Task):
            t1 = Addition(task_params={"summand1": Calculated, "summand2": Calculated})

            def run(self, *args, **kwargs):
                t1_result = self.t1.run(task_params={"summand1":2, "summand2":3}) # will be 5
                ...
"""


class Const:
    """Used to mark a parameter of a subtask as constant, i.e. not settable from a higher hierarchy.

    Example:
        When a value is passed to the constructor it is used for the target parameter. It is also
        possible to use the `Const` type as a marker to indicate that the default value of the
        target parameter shall be used als a constant::

            class Addition(Task):
                summand1 = TaskParameter()
                summand2 = TaskParameter(default=0)

                def run(self, *args, **kwargs):
                    return self.summand1.value + self.summand2.value


            class MyTask(Task):
                t1 = Addition(task_params={
                    "summand1": Const(2),
                    "summand2": Const # will be fixed at default value 0
                })

                def run(self, *args, **kwargs):
                    t1_result = self.t1.run() # will be 2 = (2 + 0)
                    ...
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, value):
        self.value = value


def is_calculated(obj) -> bool:
    """Helper function do check if parameter is calculated"""
    return isinstance(obj, _Calculated)


def is_mutable(obj) -> bool:
    """Helper function do check if parameter is mutable"""
    return isinstance(obj, _Mutable)


def is_const(obj) -> bool:
    """Helper function do check if parameter is constant"""
    return isinstance(obj, Const) or obj is Const


def is_calculated_or_mutable_or_const(obj) -> bool:
    """Helper function do check if parameter is calculated, mutable or constant"""
    return is_calculated(obj) or is_mutable(obj) or is_const(obj)


def is_calculated_or_const(obj) -> bool:
    """Helper function do check if parameter is calculated or constant"""
    return is_calculated(obj) or is_const(obj)


def _is_value_none(parameter) -> bool:
    if is_calculated_or_mutable_or_const(parameter):
        return False
    return parameter.value is None


class _Mutable:
    # pylint: disable=too-few-public-methods
    @property
    def value(self):
        """raises CalculatedAccessException on value access"""
        raise CalculatedAccessException()


Mutable = _Mutable()
"""Used to mark a parameter of a subtask as calculated by default but still mutable from a higher hierarchy.

This means that the default value of this parameter is calculated at runtime (i.e. task execution).
These default values need to be passed to the run method of the subtask. In general the behaviour is
the same as `Calculated` parameters with the only difference that `Mutable` parameters can still be
overridden from a higher hierarchy."""


class Task(ABC):
    """Abstract class that represents a unit of work within the Mosaic framework.

    The task is the main abstraction of the Mosaic framework. It represents a (single-threaded)
    unit of work that can be reused in different places within an analog generator, much like a
    simple function in Python. To define a task this class must be subclassed and the run() method
    must be implemented. All work a task does is expected to take place within this method. Tasks
    are intended to be used hierarchically, i.e. a parent task can consist of multiple child tasks.
    This is done by declaring a (child) task as a class variable. The framework will automatically
    create instance variables of any child task. Therefore, child tasks should be accessed the same
    as other properties using the self reference. Parameters of child tasks can be set using the
    constructor.

    Example:
        This simple example shows how to define and relate a parent task to a child task::

            class Addition(Task):
                summand1 = TaskParameter()
                summand2 = TaskParameter()

                def run(self, *args, **kwargs):
                    return self.summand1.value + self.summand2.value


            class MyTask(Task):
                t1 = Addition(task_params={"summand1": 2, "summand2": 3})
                t2 = Addition(task_params={"summand1": 1, "summand2": 1})

                def run(self, *args, **kwargs):
                    t1_result = self.t1.run() # will be 5
                    t2_result = self.t2.run() # will be 2
                    ...
    """

    def __init__(self, task_params: Dict[str, object] = None):
        """Constructor method

        Args:
            task_params (:obj:`dict`, optional): a dictionary of parameters that are set from a
                parent task.
        """
        self._default_params = {}
        self._path = None  # is calculated during task tree creation
        self._mosaic_logger = None  # injected
        self._mosaic = None  # injected

        if task_params is not None:
            for name, value in task_params.items():
                if value in [Calculated, Mutable] or isinstance(value, Const) or value is Const:
                    self._default_params[name] = value
                else:
                    self._default_params[name] = wrap_in_task_parameter(value=value)

        self._create_members_from_static_tasks_and_params()

    def _create_members_from_static_tasks_and_params(self):
        """creates member variable of static class variables"""
        for name, value in get_all_parameters(self).items():
            if isinstance(value, (PdkItem, Task, TaskParameter, TaskState)):
                setattr(self, name, copy.deepcopy(value))

    @abstractmethod
    def run(self, *args, **kwargs):
        """This method needs to be implemented when a new task is defined.

        The current working directory of this task depends on its position in the task hierarchy,
        i.e. its path. The directory is created automatically as soon as this method is called.
        Custom runtime arguments are allowed.
        """
        raise NotImplementedError("run method not implemented for this task")

    @property
    def path(self) -> Path:
        """:obj: `Path`: the unique path of this specific task instance starting from the root task.
        """
        return self._path

    @property
    def log(self) -> Logger:
        """:obj: `Logger`: a task specific logger instance. Logs are saved in the run directory of
        each task as well as printed to stdout."""
        return self._mosaic_logger

    @property
    def cwd(self) -> str:
        """path to the root of the current working directory (cwd)"""
        return self._mosaic.run_directory

    def _on_end(self, exception: Exception = None):
        """called after run method has finished, custom cleanup can be done here"""

    def copy(self, new_id: str) -> Task:
        """Allows to copy a task dynamically during task execution.

        The created instance is added as a child of this task using the passed id. All parameters
        are copied from their current state.

        Args:
            new_id: the id of the new task. Must be unique within this task.

        Returns:
            The new task instance.
        """
        return self._mosaic._copy(new_id, self)  # pylint: disable=protected-access

    def delete_run_dirs(self):
        """Deletes the run directory of this task."""
        print(self.cwd)
        taskdir = os.path.join(os.getcwd(), *self._mosaic.run_directory.parts, *self.path.steps)
        print(taskdir)
        shutil.rmtree(taskdir, ignore_errors=True)

    def validate_pdk(self, pdk: PDK) -> Validation:
        """Can be overridden to write custom validation logic for the PDK.

        This method is called during the checking-phase, i.e. before the task tree is executed. Its
        intended use is to search the PDK for a specific functionality instead of a specific view.
        The default implementation returns `ValidationSuccess`.

        Args:
            pdk: The PDK object to validate.

        Returns:
            A Validation object indicating the result of the validation. `ValidationSuccess` in the
                default implementation.
        """
        return ValidationSuccess

    def get_fields_of_type(self, field_type: Type) -> List:
        """Return all fields of this task that are of type `field_type` or a subclass thereof. """
        tasks = []
        for _, obj in self.__dict__.items():
            if issubclass(type(obj), field_type):
                tasks.append(obj)

        return tasks

    def dynamic_parameters(self) -> Dict[str, TaskParameter]:
        """Can be overridden to add dynamic TaskParameter e.g. from tools to the Task.
        Pdks and Tools are already available, other static defined TaskParameters not.

        Returns:
            A dict containing parameter names and TaskParameters to be added to the Task before the run() is called
        """

    def dynamic_tasks(self) -> Dict[str, Task]:
        """Can be overridden to add dynamic Task e.g. from tools to the Task.
        Pdks and Tools are already available, other static defined TaskParameters not.

        Returns:
            A dict containing parameter names and Task to be added to the Task before the run() is called
        """


def wrap_in_task_parameter(value: object):
    """helper function to wrap a plain value into a TaskParameter if necessary"""
    if issubclass(type(value), TaskParameter):
        return value

    return TaskParameter(default=value)


@runtime_checkable
class Hashable(Protocol):
    """Protocol that is used during caching for task state representation.

    When a member variable of a task complies with this protocol the `task_hash` method is called
    to represent its state.
    """
    # pylint: disable=too-few-public-methods

    def task_hash(self) -> Any:
        """Returns a hash that represents this objects state.

        Returns:
            Anything that represents this objects state. It must be pickle-able, i.e. compatible
            with the pickle.dumps() function of the standard library.
        """


ATask = TypeVar('ATask', bound=Task)

TaskParamType = TypeVar('TaskParamType')
"""Type definition of TaskParameter"""


class TaskParameter(Generic[TaskParamType]):
    """Represents a parameter of a task. Parameter values can be set from a higher hierarchy.

    This class may be subclassed to implement custom validation logic. All class variables in `Task`
    objects that are instances of this class are automatically converted to member variables by the
    framework. It is also possible to just annotate a variable (without assigning an actual value);
    in that case the parameter needs to be set from a higher hierarchy, i.e. it has no default value.
    Some subclasses for basic type checking are already implemented; see `FileTaskParameter`,
    `StringTaskParameter`, `ListTaskParameter`, ...

    Attributes:
        default: default value of this parameter. Defaults to None which is interpreted as a missing
            value.

        validate: an optional validation function that is applied to the parameter value once all
            task parameters have been set.

        description: an optional description of the parameter.

        transient: when True this parameter is ignored during caching.

    Example:
        A simple example showing different types of parameters::

            class MyTask(CachableTask):
                # must be set from outside, i.e. has no default value
                p1: TaskParameter

                # a parameter with a default value and a description
                p2 = TaskParameter(default="a string", description="this is a string parameter")

                # use a lambda to access other parameters or dependencies of a task. The passed task
                # is a self reference.
                p3 = StringTaskParameter(default=lambda task: str(task.p1.value))

                # parameters can provide custom validate logic via the constructor. The validate
                # function is called after all parameter values have been set.
                p4 = IntTaskParameter(
                    default=0,
                    validate=lambda task, value: Validation.of(value < 10, "value too large")
                )

                # parameters marked as transient will be ignored when the state of a task is
                # determined in the caching process.
                p5 = TaskParameter(default=0, transient=True)

    """

    def __init__(self, default: Optional[TaskParamType] = None,
                 validate: Optional[Callable[[ATask, TaskParamType], Validation]] = None,
                 description: Optional[str] = None,
                 transient: bool = False):
        self._default = default
        self.value: Optional[TaskParamType] = default
        self.validate_func = validate
        self.description = description
        self.transient = transient
        self._is_const = False

    @property
    def default(self) -> Optional[TaskParamType]:
        """default value"""
        return self._default

    def task_hash(self) -> bytes:
        """default implementation of task hash"""
        return pickle.dumps(self.value)

    def __eq__(self, other):
        return isinstance(other, TaskParameter) and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def validate(self) -> Validation:
        """overwrite this method to implement custom validation logic."""
        return ValidationSuccess


class FileTaskParameter(TaskParameter):
    """The value of this parameter is expected to be an existing file. Validation fails otherwise."""
    def validate(self) -> Validation:
        if not os.path.isfile(self.value):
            return ValidationError(f"The parameter {self} is not a file.")
        return ValidationSuccess


class DirTaskParameter(TaskParameter):
    """The value of this parameter is expected to be an existing directory. Validation fails
    otherwise.
    """
    def validate(self) -> Validation:
        if not os.path.isdir(self.value):
            return ValidationError(f"The parameter {self} is not a directory.")
        return ValidationSuccess


class TypeTaskParameter(TaskParameter):
    """The value of this parameter is expected to match the type passed in the constructor.

    This class implements type checking of parameter values."""
    def __init__(self, assumed_type,
                 default: Optional[TaskParamType] = None,
                 validate: Optional[Callable[[ATask, TaskParamType], Validation]] = None,
                 description: Optional[str] = None,
                 transient: bool = False):
        super().__init__(default, validate, description, transient)
        self.assumed_type = assumed_type

    def validate(self) -> Validation:
        if not isinstance(self.value, self.assumed_type):
            return ValidationError(f"The parameter {self} is not of type {self.assumed_type}")
        return ValidationSuccess


class StringTaskParameter(TypeTaskParameter):
    """The value of this parameter is expected to be a `str`; otherwise validation fails."""
    def __init__(self, default: Optional[TaskParamType] = None,
                 validate: Optional[Callable[[ATask, TaskParamType], Validation]] = None,
                 description: Optional[str] = None,
                 transient: bool = False):
        super().__init__(str, default, validate, description, transient)


class IntTaskParameter(TypeTaskParameter):
    """The value of this parameter is expected to be an `int`; otherwise validation fails."""
    def __init__(self, default: Optional[TaskParamType] = None,
                 validate: Optional[Callable[[ATask, TaskParamType], Validation]] = None,
                 description: Optional[str] = None,
                 transient: bool = False):
        super().__init__(int, default, validate, description, transient)


class DictTaskParameter(TypeTaskParameter):
    """The value of this parameter is expected to be a `dict`; otherwise validation fails."""
    def __init__(self, default: Optional[TaskParamType] = None,
                 validate: Optional[Callable[[ATask, TaskParamType], Validation]] = None,
                 description: Optional[str] = None,
                 transient: bool = False):
        super().__init__(dict, default, validate, description, transient)


class FloatTaskParameter(TaskParameter):
    """The value of this parameter is expected to be a `float` or an `int`; otherwise validation
    fails.
    """
    def validate(self) -> Validation:
        if not isinstance(self.value, float) and not isinstance(self.value, int):
            return ValidationError(f"The parameter {self} is not of type float or int.")
        return ValidationSuccess


class BoolTaskParameter(TypeTaskParameter):
    """The value of this parameter is expected to be a `bool`; otherwise validation fails."""
    def __init__(self, default: Optional[TaskParamType] = None,
                 validate: Optional[Callable[[ATask, TaskParamType], Validation]] = None,
                 description: Optional[str] = None,
                 transient: bool = False):
        super().__init__(bool, default, validate, description, transient)


class ListTaskParameter(TypeTaskParameter):
    """The value of this parameter is expected to be a `list`; otherwise validation fails."""
    def __init__(self, default: Optional[TaskParamType] = None,
                 validate: Optional[Callable[[ATask, TaskParamType], Validation]] = None,
                 description: Optional[str] = None,
                 transient: bool = False):
        super().__init__(list, default, validate, description, transient)


@dataclass
class TaskNode(tree.Node):
    """hepler struct to holding a Task and additional parameters for building the task tree"""
    value: Task
    parameters: dict
    # list of paths with tasks of the origin of the default parameters (in the hierarchy). The
    # origin can be None, which means it was injected from toplevel.
    injected_params: List[Tuple[Path, Optional[Task]]]
    parent: Optional[Task] = None

    @property
    def task(self) -> Task:
        """returning task of the node"""
        return self.value


class CheckResult:
    """Encapsulates the results of a check of the dependencies and validations of a task hierarchy.

    Attributes:
        success: when True no errors were found and the task tree is ready to build and run.
        parameters: a list of all settable parameters and their values.
        errors: a list of errors. See `ErrorType` for the different types of errors.
    """

    def __init__(self, success: bool = True):
        self.success = success
        self.parameters: List[ParameterDescription] = []
        self.errors: List[ErrorDefinition] = []

    def append_if_error(self, error_type: ErrorType, result: Result, source):
        """appends the given error only if the given result is failure"""
        if result.failure:
            self.success = False
            self.errors.append(ErrorDefinition(error_type, result.error, source))

    def append_error(self, error_type: ErrorType, message, source):
        """appends the given error"""
        self.success = False
        self.errors.append(ErrorDefinition(error_type, message, source))

    def append_parameter(self, path: str, parameter: TaskParameter, parent_task: Task):
        """appends the given parameter"""
        self.parameters.append(ParameterDescription(path, parameter, parent_task))


@dataclass
class ParameterDescription:
    """holds a TaskParameter and the path of that object in the task tree"""
    path: str
    parameter: TaskParameter
    parent_task: Task


def get_task_parameters(task: Task) -> Dict[str, TaskParameter]:
    """extracts all task parameter of a given Task, returning a dict of name and task parameter"""
    parameters = _filter_task_parameters(get_all_parameters(task))

    annotations = get_type_annotations(type(task))

    parameters.update(_get_not_set_task_params(annotations, task))

    return parameters


def _filter_task_parameters(parameters):
    return dict(filter(lambda entry: isinstance(entry[1], TaskParameter), parameters.items()))


def _get_not_set_task_params(annotations, task):
    return {name: None for name, ann_type in annotations.items()
            if _is_task_parameter(ann_type) and not hasattr(task, name)}


def _is_task_parameter(annotation) -> bool:
    origin = typing.get_origin(annotation)
    if origin is not None:
        annotation = origin

    return issubclass(annotation, TaskParameter)


def _get_cache_dir(task):
    cds: List[str] = []
    for _ in range(0, task.path.length):
        cds.append("..")
    cache_dir = os.path.join(*cds, task._mosaic.cache_directory)  # pylint: disable=protected-access
    return cache_dir
