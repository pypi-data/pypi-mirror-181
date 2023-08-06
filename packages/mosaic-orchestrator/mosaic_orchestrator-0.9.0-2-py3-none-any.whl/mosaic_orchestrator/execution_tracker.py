"""this module contains the abstract implementation for the execution tracker"""

from abc import ABC, abstractmethod
import datetime

from mosaic_orchestrator.utils import LifeCycleListener


class ExecutionTracker(ABC, LifeCycleListener):

    def _on_start(self):
        """
        By default, tools are not initialized at startup. It Can be optional done by overriding this method. Is
        called before the root run method.
        """
        return None

    def _on_end(self, exception: Exception = None):
        """
        Override this method to optional stop the tool and cleans up resources.

        This method is called after each run of the task hierarchy, even if an exception is thrown
        during the run, similar to try-catch-finally in python.

        Args:
            exception: if the run aborted with an exception it is passed as an argument.
        """
        return None

    @abstractmethod
    def add_parameter(self, pname:str, value:any) -> None:
        """
        Add the pname, value pair into the value collection.

        Args:
            pname: The name part of key
            value: The value to add
        """

    @abstractmethod
    def add_exception(self, pname:str, value:Exception) -> None:
        """
        Add the pname, exception pair into the value collection.

        Args:
            pname: The name part of key
            value: The exception to add
        """

    @abstractmethod
    def add_start_and_end_time(self, name:str, start_time:datetime, end_time:datetime, is_root_task:bool=False) -> None:
        """
        Add a new timing value with the start and the end value for the passed name into the value collection.

        Args:
            name:           The name part of key
            start_time:     The start time
            end_time:       The end time
            is_root_task:   Is the current task the root task?
        """

    @abstractmethod
    def set_root_task_event(self, event_value:str) -> None:
        """

        """
