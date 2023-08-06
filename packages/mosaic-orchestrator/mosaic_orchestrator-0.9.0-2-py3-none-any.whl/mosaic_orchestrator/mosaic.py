"""This module contains the mosaic-orchestrator framework core functionality"""
from __future__ import annotations

import copy
import importlib
import logging
import os
import pathlib
import time
import types
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging import Logger
from typing import Type, Union, Dict, List, Tuple, Optional, TypeVar, Generic, Protocol, runtime_checkable

import pluggy

from mosaic_orchestrator import tree, hookspecs
from mosaic_orchestrator.asset import Asset
from mosaic_orchestrator.cachable_task import CachableTask
from mosaic_orchestrator.config import Config
from mosaic_orchestrator.mosaic_utils import _set_param_or_wrap, find_node, _filter_calculated_params, \
    _validate_parameter, _prepare_inject_calculated_and_default, _check_parameter, _evaluate_callable_parameters, \
    _add_prefix_to_all_params, _wrap_root, MosaicException, _inject_calculated_params, _evaluate_runtime_lambdas, \
    _get_cached_result_and_logs, _inject_log_to_task_tool, _collect_results, _cache_log, \
    _measure_exec_time_run_wrapper, _track_parameter_wrapper
from mosaic_orchestrator.pdk import PDK, PdkItem
from mosaic_orchestrator.result import ValidationError, ErrorType, ErrorDefinition, Validation
from mosaic_orchestrator.task import TaskNode, Task, TaskParameter, wrap_in_task_parameter, is_calculated, \
    CheckResult, is_calculated_or_const, \
    is_const, Const, get_task_parameters, _is_value_none
from mosaic_orchestrator.tool import Tool
from mosaic_orchestrator.tree import is_path_string, Path, concat, prepend
from mosaic_orchestrator.utils import get_type_annotations, get_all_parameters, LifeCycleListener, ListHandler


@dataclass
class ToolHolder:
    """Simple holder class that marks used tools"""
    base_class: Type
    tool: Tool
    used: bool
    """When True the tool is used by at least on of the tasks."""


class ToolStore:
    """Holds all tools of a task hierarchy.

    Can be used to get a list of used tools"""

    def __init__(self):
        self._store: Dict[Type[Tool], ToolHolder] = {}

    def put(self, base_class: Union[Type[Tool], str], tool: Tool, overwrite: bool=False):
        """add tool to store"""
        if overwrite or base_class not in self._store:
            self._store[base_class] = ToolHolder(base_class, tool, used=False)

    def set_used(self, tool_type: Type[Tool]):
        """set a tool to used"""
        self._store[tool_type].used = True

    def used_tools(self) -> List[Tool]:
        """filter for used tools only"""
        return [holder.tool for holder in self._store.values() if holder.used]


@runtime_checkable
class Validate(Protocol):
    """Protocol that is used to indentify and validate task members.

    When a member variable of a task object conforms to this protocol the `validate()` function
    will be called during initialization of the task hierarchy. In case validation is unsuccessful
    an error is reported.
    """
    # pylint: disable=too-few-public-methods

    def validate(self) -> Validation:
        """validates this object during initialization.

        This function is called before any task is executed.

        Returns:
            `ValidationSuccess` or `ValidationError` in case of an error
        """


T = TypeVar("T")


class TaskHierarchyBuilder(ABC, Generic[T]):
    """A builder for a task hierarchy with a specific root task type.

    Use the `check` method to discover missing/invalid dependencies or task parameters. When all
    errors are resolved use `build` to retrieve the instance of the root task.
    """

    @abstractmethod
    def register(self, key: Union[Type, str], value:any, overwrite:bool=False) -> TaskHierarchyBuilder[T]:
        """registers a dependency based on its type or its path in the hierarchy.

        This is the intended way to make tool implementations available for tasks. Subsequent calls
        with the same key overwrite the initial value.

        Args:
            key: `value` will be injected into all tasks that have members annotated with this type.
                When key is `str` it is expected to be a path to a task parameter; in this case
                `value` is set to this parameter.
            value: this object will be injected when `key` matches
            overwrite: Overwrite tool/object if it has already been registered

        Returns:
             a self reference to allow method chaining.
        """
        raise NotImplementedError("register not implemented")

    @abstractmethod
    def with_pdk(self, pdk: PDK) -> TaskHierarchyBuilder[T]:
        """sets the pdk for this hierarchy. Subsequent calls overwrite the inital value.

        Args:
            pdk: the instantiated pdk object.

        Returns:
            a self reference to allow method chaining.
        """
        raise NotImplementedError("with_pdk not implemented")

    @abstractmethod
    def with_parameters(self, parameters: Dict[str, object]) -> TaskHierarchyBuilder[T]:
        """sets parameters for this hierarchy.

        Can be called repeatedly; however, when the same paths are provided any prior values are
        overwritten.

        Args:
            parameters: a dict that contains paths as keys and parameter values as values. Values
                that are not `TaskParameter` instances will be wrapped automatically.

        Returns:
            a self reference to allow method chaining.
        """
        raise NotImplementedError("with_parameters not implemented")

    @abstractmethod
    def with_run_directory(self, path: pathlib.Path) -> TaskHierarchyBuilder[T]:
        """sets the run directory for this hierarchy.

        Args:
            path: a path to the target folder. The folder will be created if it does not exist.

        Returns:
            a self reference to allow method chaining.
        """
        raise NotImplementedError("with_run_directory not implemented")

    @abstractmethod
    def with_cache_directory(self, path: pathlib.Path) -> TaskHierarchyBuilder[T]:
        """sets the cache directory for this hierarchy.

        Args:
            path: a path to the target folder. The folder will be created if it does not exist.

        Returns:
            a self reference to allow method chaining.
        """
        raise NotImplementedError("with_cache_directory not implemented")

    @abstractmethod
    def build(self) -> T:
        """builds the task hierarchy and returns the instance of the root task.

        Use the `check` method to test if build is going to be successful.

        Returns:
            the root task instance.

        Raises:
            MosaicException: in case of a missing dependency or an unsuccessful validation.
        """
        raise NotImplementedError("build not implemented")

    @abstractmethod
    def check(self) -> CheckResult:
        """checks dependencies and task parameters and performs validation.

        This method can be called repeatedly to find remaining errors.

        Returns:
            A `CheckResult` object containing a list of all settable parameters as well as a list
            of remaining errors.
        """
        raise NotImplementedError("check not implemented")

    @abstractmethod
    def with_cfg(self, config: Union[Config, pathlib.Path]) -> TaskHierarchyBuilder[T]:
        """loads a `Config` either from an object or from a python script.

        This method can be called repeatedly to merge multiple configurations.

        Args:
            config: a `Config` object that will be applied to this hierarchy. Alternatively, pass a
                path to a python script containing a `MosaicConfig` class; This class will be
                automatically isntantiated and loaded.

        Returns:
            a self reference to allow method chaining.
        """
        raise NotImplementedError("with_cfg not implemented")


class Mosaic(TaskHierarchyBuilder[T]):
    """This is the main entry point of the framework. Use `create` to start building an executable
        task tree."""
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    """the formatter used for logging. It is used for stdout as well as log files. Can be set globally"""
    log_level = logging.INFO
    """the log level of all loggers. Can be set globally"""
    default_cache_directory = ".mosaic_orchestrator"
    default_work_directory = "mosaic_orchestrator.work"

    @staticmethod
    def create(root: Type[T], caching: bool = True, plugin_enabled: bool = True) -> TaskHierarchyBuilder[T]:
        """creates a builder for a task hierarchy given a root task.

        Args:
            root: the type of the desired root task. Notice that actual instantiation is done by the
                framework.
            caching: when False all caching is disabled for hierarchies build with this builder.
            plugin_enabled: Enables die plugin discovery for PDKs and tools.

        Returns:
            a `TaskHierarchyBuilder` for the given root type.


        Example:
            This is a simple example that shows how to build a simple mosaic_orchestrator task tree::

                    builder = Mosaic.create(root=MyTask)\
                        .with_pdk(MyPdkImpl())\
                        .register(AtoolInterface, MyToolImpl())\
                        .register(AnotherDependency, AnotherDependency())\
                        .with_parameters({
                            "x1": 5,
                            "x2": 3,
                            "t1.p5": "REF",
                        })

                    if builder.check().success:
                        instance = builder.build()
                        instance.run()
        """
        return Mosaic[T](root, caching, plugin_enabled)

    @staticmethod
    def get_installed_pdks() -> List[PDK]:
        """lists all installed PDKs"""
        plugin_manager = pluggy.PluginManager("mosaic_orchestrator")
        plugin_manager.add_hookspecs(hookspecs)
        plugin_manager.load_setuptools_entrypoints("mosaic_orchestrator")
        return plugin_manager.hook.get_pdk()

    @staticmethod
    def get_installed_tools() -> List[Tool]:
        """lists all installed Tools"""
        plugin_manager = pluggy.PluginManager("mosaic_orchestrator")
        plugin_manager.add_hookspecs(hookspecs)
        plugin_manager.load_setuptools_entrypoints("mosaic_orchestrator")
        return plugin_manager.hook.get_tool()

    def __init__(self, root: Type[T], caching, plugin_enabled):
        self._configure_console_logging()
        self.root_type = root
        self.pdk = None
        self.execution_trackers = None
        self.caching = caching
        self.plugin_enabled = plugin_enabled
        self._store = {}
        self.tools = ToolStore()
        self._callable_params: List[Tuple[TaskParameter, Task]] = []
        self._check_result = CheckResult()
        self._task_tree = None
        self.root = None
        self.measure_execution_time = None
        self.track_parameter = None
        self._loggers = {}
        self.run_directory = pathlib.Path.joinpath(
            pathlib.Path.cwd(),
            Mosaic.default_work_directory
        )
        self.cache_directory = pathlib.Path.joinpath(
            pathlib.Path.cwd(),
            Mosaic.default_cache_directory
        )
        self._life_cycle_listener: List[LifeCycleListener] = []
        self._validate_list: List[Validate] = []

        self.plugin_manager = pluggy.PluginManager("mosaic_orchestrator")
        if plugin_enabled:
            self.plugin_manager.add_hookspecs(hookspecs)
            self.plugin_manager.load_setuptools_entrypoints("mosaic_orchestrator")

    def with_cfg(self, config: Union[Config, str]) -> TaskHierarchyBuilder[T]:
        if isinstance(config, str):
            mod_name, file_ext = os.path.splitext(os.path.split(config)[-1])
            if file_ext.lower() == '.py':
                loader = importlib.machinery.SourceFileLoader(mod_name, config)
                mod = types.ModuleType(loader.name)
                loader.exec_module(mod)
            else:
                raise MosaicException(ErrorDefinition(ErrorType.GENERAL_ERROR, f"Configuration file '{config}' cannot "
                                                                               f"be loaded.", config))
            try:
                config = mod.MosaicConfig()
            except AttributeError as error:
                raise MosaicException(ErrorDefinition(ErrorType.GENERAL_ERROR, f"Configuration file '{config}' has "
                                                                               f"not a Config class named "
                                                                               f"'MosaicConfig'.", config)) from error

        if config.get_pdk():
            self.with_pdk(config.get_pdk())

        self.with_parameters(config.get_parameters())

        if config.get_run_directory():
            self.with_run_directory(config.get_run_directory())

        if config.get_cache_directory():
            self.with_cache_directory(config.get_cache_directory())

        for tool in config.get_tools():
            self.register(key=type(tool), value=tool, overwrite=True)

        for key, value in config.get_objects_to_register():
            self.register(key, value, overwrite=True)
        return self

    def with_pdk(self, pdk: PDK) -> TaskHierarchyBuilder[T]:
        self.pdk = pdk
        self._build_protocol_lists(pdk)
        return self

    def with_run_directory(self, path: pathlib.Path) -> TaskHierarchyBuilder[T]:
        self.run_directory = path
        return self

    def with_cache_directory(self, path: pathlib.Path) -> TaskHierarchyBuilder[T]:
        self.cache_directory = path
        return self

    def register(self, key: Union[Type, str], value:any, overwrite:bool = False) -> TaskHierarchyBuilder[T]:

        # Inject PDK in registered "things"
        if not isinstance(value, TaskParameter):
            for name, param_type in get_type_annotations(type(value)).items():
                if param_type and issubclass(param_type, PDK):
                    setattr(value, name, self.pdk)

        if isinstance(value, Tool):
            self.tools.put(key, value, overwrite)
        else:
            if key not in self._store or overwrite:
                self._store[key] = value
            else:
                raise MosaicException(ErrorDefinition(ErrorType.GENERAL_ERROR,
                f"{key} has already been registered! Maybe you have installed multiple variants in your "
                f"python environment (e.g. {type(value)} and {type(self._store[key])}). "
                "Please uninstall one or more to reduce it to a single tool installation.", value))

        return self

    def with_parameters(self, parameters: Dict[str, object]) -> TaskHierarchyBuilder[T]:
        for name, value in parameters.items():
            self._store[name] = wrap_in_task_parameter(value=value)

        return self

    def build(self) -> T:
        result = self.check()

        if result.success is False:
            raise MosaicException(result.errors[0])

        return self.root

    def check(self) -> CheckResult:
        self._check_result = CheckResult()

        if self.plugin_enabled:

            if not self.execution_trackers:
                self.__load_exection_trackers_from_plugins()

            if not self.pdk:
                self._load_pdk_from_plugins()

            self._load_tools_from_plugins()

        self._inject_by_type(self.pdk)
        self.root = self.root_type()
        self._task_tree = self._build_task_tree(task=self.root, path=Path(self.root_type.__name__))

        self._check_parameters()

        tree.traverse(
            tree=self._task_tree,
            on_each=self._inject
        )

        tree.traverse(
            tree=self._task_tree,
            on_each=self._set_defaults
        )

        for tool in self.tools.used_tools():
            self._inject_pdk_items(tool)

        tree.traverse(
            tree=self._task_tree,
            on_each=self._evaluate_and_validate
        )

        for obj in self._validate_list:

            result = obj.validate()

            if isinstance(result, ValidationError):
                self._check_result.append_error(
                    ErrorType.VALIDATION_ERROR,
                    f"'{type(obj).__name__}' could not be validated - {result.message}",
                    type(obj)
                )

        _wrap_root(self.root)

        return self._check_result

    def _load_pdk_from_plugins(self):
        """try to load a pdk from installed plugin, adds error if more than one PDK is found"""

        pdks = self.plugin_manager.hook.get_pdk()

        # track all selected PDK's
        selected_pdk = ""
        for p in pdks:
            selected_pdk += type(p).__name__ + " "

        for tracker in self.execution_trackers:
            tracker.add_parameter("installed_pdks", selected_pdk.strip())

        if len(pdks) == 1:
            self.with_pdk(pdks[0])
        elif len(pdks) > 1:
            self._check_result.append_error(
                ErrorType.PDK_ERROR,
                f"More then one installed PDKs found in virtual environment: {pdks}",
                self
            )

    def __load_exection_trackers_from_plugins(self):
        """try to load the execution tracker from the installed plugins"""

        self.execution_trackers = self.plugin_manager.hook.get_execution_tracker()
        # TODO what happens if no plugin was found?
        # how can i log all selected tracker?
        for tracker in self.execution_trackers:
            self._build_protocol_lists(tracker)

    def _load_tools_from_plugins(self):
        """try to load tools from installed plugins"""
        tools = self.plugin_manager.hook.get_tool()

        # track all selected tools
        selected_tools = ""
        for t in tools:
            selected_tools += type(t).__name__ + " "

        for tracker in self.execution_trackers:
            tracker.add_parameter("installed_tools", selected_tools.strip())

        for tool in tools:
            self.register(tool[0], tool[1], overwrite=False)

    def _build_task_tree(self, task: Task, path: Path, parent: Optional[Task] = None) -> TaskNode:
        """build the task tree of a given task recursively"""
        task._path = path  # pylint: disable=protected-access
        self._set_logger(task)
        self._inject_pdk_items(task)
        self._inject_by_type(task)
        task_parameters = get_task_parameters(task)

        dynamic_parameters = task.dynamic_parameters()
        if dynamic_parameters:
            for param_name in dynamic_parameters:
                setattr(task, param_name, dynamic_parameters[param_name])
            task_parameters.update(dynamic_parameters)

        root = TaskNode(
            parent=parent,
            value=task,
            children=[],
            parameters=task_parameters,
            injected_params=[]
        )

        dynamic_tasks = task.dynamic_tasks()
        if dynamic_tasks:
            for subtask_name, subtask in dynamic_tasks.items():
                setattr(task, subtask_name, subtask)
                sub_tree = self._build_task_tree(task=subtask,
                                                 path=Path([*path.steps, subtask_name]),
                                                 parent=task)
                root.children.append(sub_tree)
                _add_prefix_to_all_params(sub_tree, subtask_name)

        for subtask_attr_name in type(task).__dict__.keys():
            subtask_attr = getattr(task, subtask_attr_name)
            if issubclass(type(subtask_attr), Task):
                sub_tree = self._build_task_tree(task=subtask_attr,
                                                 path=Path([*path.steps, subtask_attr_name]),
                                                 parent=task)
                root.children.append(sub_tree)
                _add_prefix_to_all_params(sub_tree, subtask_attr_name)

        return root

    def _inject(self, node: TaskNode):
        """wrap run method, handle calculated parameters and inject parameters into task"""
        node.task._mosaic = self  # pylint: disable=protected-access
        self._wrap_run(node.task)
        self._handle_calculated_params(node)
        self._inject_parameters(node)

    def _set_logger(self, task: Task):
        """crate a new or set existing logger given task"""
        task._mosaic_logger = self._get_or_create_logger(task)  # pylint: disable=protected-access

    def _inject_pdk_items(self, instance):
        """inject pdk items to a given instance"""
        source = type(instance)
        if hasattr(instance, "path"):
            source = instance.path
        for name, obj in get_all_parameters(instance).items():

            # Allow assets to use pdk items
            if issubclass(type(obj), Asset):
                self._inject_pdk_items(obj)

            if issubclass(type(obj), PdkItem):
                if not self._check_pdk(source):
                    continue
                result = self.pdk.get_item(obj.name, obj.version)
                if result.failure:
                    
                    supported_items = self.pdk.supported_items() or []

                    self._check_result.append_error(
                        ErrorType.MISSING_PDK_ITEM,
                        f"PdkItem not available in provided PDK ('{obj.name}',"
                        f" {obj.version}). Supported items: [{' '.join([item.name for item in supported_items])}]",
                        source
                    )
                    continue
                item = result.value
                # making item conform to Hashable and dependant on pdk
                item.task_hash = self.pdk.task_hash
                # Check if they are not "related"
                if not issubclass(type(item), type(obj)):
                    self._check_result.append_error(
                        ErrorType.PDK_ERROR,
                        f"Expected pdk item of type '{type(obj).__name__}' not compatible"
                        f" with view from PDK '{type(item).__name__}'",
                        type(instance)
                    )
                if not item._try_init():  # pylint: disable=protected-access
                    self._check_result.append_error(
                        ErrorType.PDK_ERROR,
                        f"Could not validate pdk item '{type(item).__name__}'",
                        type(instance)
                    )
                setattr(instance, name, result.value)

    def _check_pdk(self, source) -> bool:
        """check if pdk is available"""
        if self.pdk is None:
            self._check_result.append_error(ErrorType.PDK_ERROR,
                                            "PDK implementation is missing, "
                                            "please provide a valid implementation", source)
            return False
        return True

    def _inject_by_type(self, obj):
        """inject Logger, Tools, PDK, registered objects and parameter to given objects"""
        annotations = get_type_annotations(type(obj))
        for param_name, annotation in annotations.items():

            origin = typing.get_origin(annotation)
            if origin is not None:
                annotation = origin

            if annotation is Logger:
                if issubclass(type(obj), Task) and not hasattr(obj, param_name):
                    setattr(obj, param_name, obj._mosaic_logger)  # pylint: disable=protected-access
            elif issubclass(annotation, Tool):
                tool_found = []
                for tool in self.tools._store.values():  # pylint: disable=protected-access
                    if issubclass(type(tool.tool), annotation):
                        tool_found.append(tool.tool)
                
                if annotation not in self.tools._store:
                    self._check_result.append_error(ErrorType.MISSING_TOOL,
                                                    f"Tool is missing for {annotation}",
                                                    type(obj))
                    continue
                
                tool = self.tools._store[annotation].tool
                setattr(obj, param_name, tool)
                self._inject_by_type(tool)
                self.tools.set_used(annotation)

            elif annotation is PDK:
                if hasattr(obj, param_name) and getattr(obj, param_name) is not self.pdk:
                    self._check_result.append_error(ErrorType.PDK_ERROR,
                                                    f"Instantiated PDK found in {type(obj)}"
                                                    " - this is not the expected usage, please use "
                                                    "builder function instead",
                                                    type(obj)
                                                    )
                    continue

                if self.pdk is None:
                    self._check_result.append_error(ErrorType.PDK_ERROR,
                                                    "PDK implementation is missing, please provide a valid "
                                                    "implementation",
                                                    type(obj))
                    continue
                setattr(obj, param_name, self.pdk)
            elif annotation in self._store:
                param = self._store[annotation]
                setattr(obj, param_name, param)
                self._inject_by_type(param)
            elif not hasattr(obj, param_name) and not issubclass(annotation,
                                                                 Task) and not issubclass(
                annotation, TaskParameter):
                self._check_result.append_error(ErrorType.PARAMETER_ERROR,
                                                f"{annotation} implementation is missing, "
                                                f"please register a valid implementation",
                                                type(obj))

    def _build_parameter_list(self, node: TaskNode):
        """build parameter list of a task and append it to the check result"""
        for path_str in node.parameters.keys():
            path = prepend(node.task.path.root, Path(path_str))
            if not hasattr(node.task, path.target) or _is_value_none(
                    getattr(node.task, path.target)):
                self._check_result.append_error(ErrorType.MISSING_PARAMETER,
                                                f"Parameter missing: {path}", path)
            elif not is_calculated_or_const(getattr(node.task, path.target)):
                self._check_result.append_parameter(str(path), getattr(node.task, path.target), node.task)

    def _get_or_create_logger(self, task: Task) -> Logger:
        """create a new logger or create the existing one"""
        if task.path in self._loggers:
            return self._loggers[task.path]

        logger = logging.getLogger(name=str(task.path))
        logger.setLevel(Mosaic.log_level)

        filehandler = logging.FileHandler(filename=os.path.join(*self.run_directory.parts,
                                                                *[*task.path.steps, "log"]),
                                          delay=True)
        filehandler.setFormatter(Mosaic.log_formatter)
        logger.addHandler(filehandler)
        self._loggers[task.path] = logger
        return logger

    def _check_parameters(self):
        """check if parameters given to mosaic are valid and given path is correct"""
        for name, _ in self._store.items():
            if isinstance(name, str):
                if is_path_string(name):
                    path = Path(name)
                    node_result = find_node(task_tree=self._task_tree, path=path)
                    if node_result.failure:
                        self._check_result.append_if_error(ErrorType.PARAMETER_ERROR, node_result,
                                                           str(path))
                        continue
                    self._check_result.append_if_error(ErrorType.PARAMETER_ERROR,
                                                       _check_parameter(path.target,
                                                                        node_result.value.task),
                                                       str(path))
                else:
                    self._check_result.append_if_error(ErrorType.PARAMETER_ERROR,
                                                       _check_parameter(name, self.root),
                                                       str(self.root.path))

    def _inject_parameters(self, node: TaskNode):
        """inject parameters form store in given task"""
        node.injected_params = []
        for path_string in node.parameters.keys():
            if path_string in self._store:
                self._inject_parameter_from_store(node, path_string)

    def _inject_parameter_from_store(self, node: TaskNode, path_string):
        """inject a named parameters form store"""
        path = Path(path_string)

        if hasattr(node.task, path.target):
            result = _prepare_inject_calculated_and_default(node.task, path)
            if result.failure:
                self._check_result.append_error(ErrorType.PARAMETER_ERROR, result.error, str(path))
                return

        result = _set_param_or_wrap(instance=node.task, name=path.target,
                                    param=self._store[path_string])
        if result.failure:
            self._check_result.append_error(ErrorType.PARAMETER_ERROR, result.error,
                                            str(node.task.path))
            return
        node.injected_params.append((path, None))

        self._add_to_relevant_parameters_of_ascendants(path, result)

    def _add_to_relevant_parameters_of_ascendants(self, path, result):
        """add parameter to task tree at given path"""
        current_path = path.parent()
        while current_path.steps:
            current_task = find_node(self._task_tree, current_path, check_parameter=False) \
                .raise_on_fail().task
            if not hasattr(current_task, "_relevant_params"):
                current_task._relevant_params = [result.value]  # pylint: disable=protected-access
            else:
                current_task._relevant_params.append(result.value)  # pylint: disable=protected-access
            current_path = current_path.parent()

    def _evaluate_and_validate(self, node: TaskNode):
        """evaluate and validate PDK, callable parameters, parameters, build parameter list and build protocol list"""
        self._validate_pdk(node)
        _evaluate_callable_parameters(node)
        self._validate_parameters(node)
        self._build_parameter_list(node)
        self._build_protocol_lists(node.task)

    def _validate_pdk(self, node: TaskNode):
        """calls validate_pdk of given task and handle error"""
        validation = node.task.validate_pdk(self.pdk)

        if isinstance(validation, ValidationError):
            self._check_result.append_error(
                ErrorType.PDK_ERROR,
                f"Task {node.task.path} could not validate PDK - {validation.message}",
                node.task.path
            )

    def _validate_parameters(self, node: TaskNode):
        """calls validate functions of all TaskParameters. Assumes that all parameters have been
        evaluated"""
        for name, parameter in get_task_parameters(node.task).items():
            if parameter:
                validation = _validate_parameter(node.task, parameter)

                if isinstance(validation, ValidationError):
                    path = concat(node.task.path, name)
                    self._check_result.append_error(
                        ErrorType.PARAMETER_ERROR,
                        f"Validation failed for '{path}' with value "
                        f"'{parameter.value}' reason: {validation.message}",
                        str(path)
                    )

    def _build_protocol_lists(self, obj):
        """add obj to validation_list and/or life_cycle_list if necessary"""
        if isinstance(obj, Validate) and not isinstance(obj, TaskParameter):
            self._validate_list.append(obj)

        if isinstance(obj, LifeCycleListener):
            self._life_cycle_listener.append(obj)

        for _, item in get_all_parameters(obj).items():
            if isinstance(item, Validate) and not isinstance(item, TaskParameter):
                self._validate_list.append(item)

            if isinstance(item, LifeCycleListener):
                self._life_cycle_listener.append(item)

    def _startup(self):
        """calls the on_start method of each registered object implements LifeCycleListener"""
        for obj in self._life_cycle_listener:
            obj._on_start()  # pylint: disable=protected-access

    def _cleanup(self, exception=None):
        """calls the on_end method of each registered object implements LifeCycleListener"""
        for obj in self._life_cycle_listener:
            obj._on_end(exception)  # pylint: disable=protected-access

    def _handle_calculated_params(self, node: TaskNode):
        """handle calculated parameters"""
        calculated_params = _filter_calculated_params(node.task._default_params)  # pylint: disable=protected-access
        node.task._calculated_params = calculated_params  # pylint: disable=protected-access

        for param_name, calculated_or_mutable_or_const in calculated_params.items():
            del node.task._default_params[param_name]  # pylint: disable=protected-access
            path = Path(param_name)
            result = find_node(node, path)
            if result.failure:
                self._check_result.append_if_error(ErrorType.PARAMETER_ERROR, result, path)
                continue
            target_node = result.value
            if hasattr(target_node.task, path.target):
                if is_calculated(getattr(target_node.task, path.target)):
                    self._check_result.append_error(ErrorType.PARAMETER_ERROR,
                                                    f"{target_node.task.path}.{path.target} is already set to",
                                                    f" Calculated {target_node.task.path}.{path.target}")
                if is_const(getattr(target_node.task, path.target)):
                    self._check_result.append_error(ErrorType.PARAMETER_ERROR,
                                                    f"{target_node.task.path}.{path.target} is already set to Const",
                                                    f"{target_node.task.path}.{path.target}")
                if not hasattr(target_node.task, "_calculated_default_values"):
                    target_node.task._calculated_default_values = {}  # pylint: disable=protected-access
                target_node.task._calculated_default_values[path.target] \
                    = getattr(target_node.task, path.target)  # pylint: disable=protected-access

            if calculated_or_mutable_or_const is Const:
                param = getattr(target_node.task, path.target)
                if isinstance(param, TaskParameter):
                    setattr(target_node.task, path.target, Const(param.value))
                    continue
                setattr(target_node.task, path.target, Const(None))
                continue
            setattr(target_node.task, path.target, calculated_or_mutable_or_const)

    def _wrap_run(self, task: Task):
        """wrap run method of given task with _run_wrapper"""
        task._old_run = task.run  # pylint: disable=protected-access
        task.run = types.MethodType(_run_wrapper, task)
        task.measure_execution_time = types.MethodType(_measure_exec_time_run_wrapper, task)
        task.track_parameter = types.MethodType(_track_parameter_wrapper, task)

    def _set_defaults(self, node: TaskNode):
        """set the parameters passed to constructor of task (via task_params)
        if they havent been injected"""
        for name, default_param in node.task._default_params.items():  # pylint: disable=protected-access
            path = Path(name)

            result = find_node(task_tree=node, path=path)
            if result.failure:
                self._check_result.append_if_error(ErrorType.PARAMETER_ERROR, result, str(path))
                continue
            current_node = result.value

            injected_path_list = list(
                filter(lambda param_path: param_path[0].target == path.target,  # pylint: disable=cell-var-from-loop
                       current_node.injected_params))

            if not injected_path_list or injected_path_list[0][0].length < path.length:
                result = _set_param_or_wrap(
                    instance=current_node.task,
                    name=path.target,
                    param=default_param
                )
                if result.failure:
                    self._check_result.append_error(ErrorType.PARAMETER_ERROR, result.error,
                                                    str(current_node.task.path))
                    continue
                if injected_path_list:
                    current_node.injected_params.remove(injected_path_list[0])
                current_node.injected_params.append((path, node.parent))

    def _copy(self, new_id: str, task: Task) -> Task:
        """create a copy of a task"""
        new_task = type(task)()
        new_task._path = Path([*task.path.steps[:-1], new_id])  # pylint: disable=protected-access

        new_task._mosaic = self  # pylint: disable=protected-access
        self._set_logger(new_task)
        self._inject_pdk_items(new_task)
        self._inject_by_type(new_task)
        self._wrap_run(new_task)

        for name, param in get_task_parameters(task).items():
            setattr(new_task, name, copy.copy(param))

        new_task._calculated_params = copy.copy(task._calculated_params)  # pylint: disable=protected-access
        if hasattr(task, "_calculated_default_values"):
            new_task._calculated_default_values = copy.copy(task._calculated_default_values)  # pylint: disable=protected-access

        if hasattr(task, "INJECTED_DEFAULTS"):
            new_task.INJECTED_DEFAULTS = task.INJECTED_DEFAULTS

        return new_task

    def _configure_console_logging(self):
        """setup console logging"""
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(Mosaic.log_formatter)
        logging.getLogger('').addHandler(console_handler)


def _run_wrapper(task, task_params: Dict[str, object] = None, *args, **kwargs):
    """wrapped run method, creates current working directories, inject logging and handles caching"""
    # the task_params argument can be filled with a custom positional run argument
    # such as : run(my_arg: int)
    # when calling such a run method without keyword - run(1) - it would appear here as task_params
    is_task_params_real = task_params is None or isinstance(task_params, dict)

    if is_task_params_real:
        _inject_calculated_params(task, task_params)

    _evaluate_runtime_lambdas(task)

    working_dir = task.path.target

    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    os.chdir(working_dir)

    if task._mosaic.caching and isinstance(task, CachableTask):  # pylint: disable=protected-access
        task.task_hash = task.calc_hash(task_params, *args, **kwargs)
        cached_result, logs = _get_cached_result_and_logs(task)
        if cached_result is not None:
            _reproduce_cached_logs(logs, task)

            os.chdir("..")
            task.task_result = cached_result
            return cached_result

    _inject_log_to_task_tool(task)

    list_handler = ListHandler()
    if isinstance(task, CachableTask):
        task._mosaic_logger.addHandler(list_handler)  # pylint: disable=protected-access

    # Check whether the curtent task is the root task.
    # The execution trackers may add additional or different parameters to the measured runtime for the root task.
    # The flga for the root shouldn't forward to the run method, therefore we remove this key from the dictonary.
    is_root_task_value = "is_root_task" in kwargs and kwargs.get("is_root_task")
    if is_root_task_value:
        del kwargs["is_root_task"]

    # measure the execution time of the run method and pass this time to all registered execution trackers
    with task.measure_execution_time(str(task.path), is_root_task=is_root_task_value):
        # task.
        if is_task_params_real:
            result = task._old_run(*args, **kwargs)  # pylint: disable=protected-access
        else:
            # task_params contains custom positional argument
            result = task._old_run(task_params, *args, **kwargs)  # pylint: disable=protected-access

    if task._mosaic.caching and isinstance(task, CachableTask):  # pylint: disable=protected-access
        task.task_result = result
        results = _collect_results(task)
        task._cache(results)  # pylint: disable=protected-access
        task.is_invalid = False
        _cache_log(list_handler, task)

    os.chdir("..")
    return result


def _reproduce_cached_logs(logs, task: Task):
    """add cached logs to current task log"""
    if logs is not None:
        logger: Logger = task._mosaic_logger  # pylint: disable=protected-access
        for record in logs:
            record.name = logger.name
            time_created = time.time()

            formatted_cached_timestamp = Mosaic.log_formatter.formatTime(record)

            record.created = time_created
            record.msecs = (time_created - int(time_created)) * 1000
            record.msg = f"[CACHED {formatted_cached_timestamp}] {record.msg}"
            logger.callHandlers(record)
