"""this module contains the abstract tool implementation"""

from abc import ABC, abstractmethod

from mosaic_orchestrator.result import Validation
from mosaic_orchestrator.utils import LifeCycleListener


class Tool(ABC, LifeCycleListener):
    """Abstract base class for tools that provided to tasks via dependency injection."""

    def _get_all_parameters(self):
        return {name: getattr(self, name) for name in dir(self)}

    @abstractmethod
    def validate(self) -> Validation:
        """check if tool is accessible and return ValidationSuccess if it is, otherwise ValidationError"""
        raise NotImplementedError("check_tool not implemented")

    def task_hash(self):
        """by default tools are ignored for caching."""
        return None

    def _on_start(self):
        """By default, tools are not initialized at startup. It Can be optional done by overriding this method. Is
        called before the root run method. """
        return None

    def _on_end(self, exception: Exception = None):
        """Override this method to optional stop the tool and cleans up resources.

        This method is called after each run of the task hierarchy, even if an exception is thrown
        during the run, similar to try-catch-finally in python.

        Args:
            exception: if the run aborted with an exception it is passed as an argument.
        """
        return None
