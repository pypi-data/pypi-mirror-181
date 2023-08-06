"""This module contains the hookspec for plugins.
    Implement one or more of the defined hooks in your plugins.
"""
from typing import Tuple, Type
import pluggy

from mosaic_orchestrator.execution_tracker import ExecutionTracker
from mosaic_orchestrator.pdk import RootPDK
from mosaic_orchestrator.tool import Tool

hookspec = pluggy.HookspecMarker("mosaic_orchestrator")


@hookspec
def get_pdk() -> RootPDK:
    """Returns:
        A `PDK` object.
    """


@hookspec
def get_tool() -> Tuple[Type[Tool], Tool]:
    """Returns:
        A tuple of Tool base class and `Tool` object.
        E.g. Virtuoso, MyVirtuoso()
    """

@hookspec
def get_execution_tracker() -> ExecutionTracker:
    """Returns:
        A `ExecutionTracker` object.
    """
