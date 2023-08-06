"""this module contains the cachable task implementation"""
import hashlib
import inspect
import pickle
from abc import ABC
from dataclasses import dataclass
from typing import Dict, Optional

from mosaic_orchestrator.cache import Cache
from mosaic_orchestrator.task import Task, TaskParameter, Hashable, is_calculated_or_mutable_or_const, _get_cache_dir
from mosaic_orchestrator.tree import Path
from mosaic_orchestrator.tool import Tool


@dataclass
class CacheResult:
    """builds the result tree of a task tree, used to evaluate the task cache"""
    result: object
    sub_results: Dict[Path, str]

class CachableTask(Task, ABC):
    """Results of `CachableTasks` are cached persistently and reused when all parameters match.

    The return value of the run() method is considered to be the result of a task. The complete
    state of a task, including all member variables, is considered when looking up previous results.
    In case of a cache-hit the run() method is not executed and the cached result is returned
    instead. To implement custom invalidation logic (e.g. when the result of a cache is representing
    a file that is susceptible to change between executions) the invalidate() method can be
    overridden. When fine-grained control of the state representation of a class is needed the
    `Hashable` protocol can be implemented. It is used whenever it is present in a member variable
    of a task. To ignore a parameter for caching set its `transient` flag to `True`.

    """

    def __init__(self, task_params: Dict[str, object] = None):
        """Constructor method

        Args:
            task_params (:obj:`dict`, optional): a dictionary of parameters that are set from a
                parent task.
        """
        super().__init__(task_params)
        self.is_invalid = False
        self.task_result = None
        self.task_hash = None

    def check_is_cache_valid(self, result) -> bool:
        """This method is called when evaluating cached results.

        Overwrite this method to implement custom result invalidation.

        Args:
            result: the cached result object.

        Returns:
            True if the result is still valid, in this case it will be reused and the task will not
            be executed again. When False is returned the cached result is deleted and the task is
            executed again. The default implementation returns True without considering the result.
        """
        return True

    def calc_hash(self, task_params: Optional, *args, **kwargs) -> str:
        """Calculates a hash for this task based on the runtime arguments.

        Overriding this method is discouraged as it can have unexpected results when not done
        properly.
        """

        obj = []

        for name, parameter in vars(self).items():
            if isinstance(parameter, Tool):
                continue # no need to cache the tools

            if isinstance(parameter, TaskParameter) and parameter.transient:
                continue # no need to cache transient parameters

            if name in ["_default_params", "run", "_old_run", "_old_root_run", "_path",
                          "_mosaic_logger", "_mosaic", "_calculated_default_values", "task_result",
                          "task_hash", "_calculated_params", "measure_execution_time", "track_parameter"]:
                continue

            if isinstance(parameter, Task) or is_calculated_or_mutable_or_const(parameter):
                continue

            if isinstance(parameter, Hashable):
                try:
                    param_hash = parameter.task_hash()
                except Exception as error:
                    raise AttributeError(
                        f"Failed to calculated task_hash of '{name}' in task '{self.path}' - {error}"
                    ) from error
                _try_pickle(param_hash, self.path, name)
                obj.append((f"hashable: {name}", param_hash))
                continue

            # default:
            _try_pickle(parameter, self.path, name)
            obj.append((f"field: {name}", parameter))

        if task_params:
            _try_pickle(task_params,
                        message=f"Caching failed: could not pickle task_params of task {self.path}")
            obj.append(task_params)

        if kwargs:
            _try_pickle(kwargs,
                        message=f"Caching failed: could not pickle custom arguments {kwargs} of task {self.path}")
            obj.append(kwargs)

        if args:
            _try_pickle(args,
                        message=f"Caching failed: could not pickle custom arguments {args} of task {self.path}")
            obj.append(args)

        try:
            source = ""
            if type(self).__module__!="__main__":
                source = inspect.getsource(type(self))
            object_string = f"{pickle.dumps(obj)}_{source}"
            calculated_hash = hashlib.md5(object_string.encode())
            result = f"{self.__class__.__name__}_{calculated_hash.hexdigest()}"
            return result
        except Exception as error:
            raise AttributeError(
                f"{error} - Task parameters and results must be serializable using pickle package") from error



    def _is_task_invalid(self, result: CacheResult, cache: Cache):
        if self.is_invalid:
            return True

        task_invalid = False

        subtasks = self.get_fields_of_type(CachableTask)

        for subtask in subtasks:
            if subtask.is_invalid:
                task_invalid = True
                break

            relative_path = subtask.path.remove(self.path)

            if relative_path not in result.sub_results:
                task_invalid = True
                break

            subtask_hash = result.sub_results[relative_path]
            subtask_result = cache.get(subtask_hash)
            if not subtask_result:
                task_invalid = True
                break

            if subtask._is_task_invalid(subtask_result, cache):  # pylint: disable=protected-access
                task_invalid = True

        if task_invalid:
            self.is_invalid = True
            return True

        if not self.check_is_cache_valid(result.result):
            self.is_invalid = True
            return True

        return False

    def _cache(self, value):
        with Cache(_get_cache_dir(self)) as cache:
            try:
                cache.put(self.task_hash, value)
            except Exception as error:
                raise AttributeError(
                    f"{error} - Task parameters and results must be serializable using pickle package"
                ) from error


def _try_pickle(value, path=None, field=None, message=None):
    """try pickle given value, raises a AttributeError if it not pickleable.
     optional path, field and message can be used to specify the error further"""
    try:
        pickle.dumps(value)
    except Exception as exc:
        if message:
            raise AttributeError(
                f"Caching failed: could not pickle field '{field}' of task '{path}'"
            ) from exc
        raise AttributeError(
            f"Caching failed: could not pickle field '{field}' of task '{path}'"
        ) from exc
