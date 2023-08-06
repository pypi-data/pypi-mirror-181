"""This module contains the configuration base class for the mosaic-orchestrator."""
from pathlib import Path
from typing import Dict, List, Union, Type, Optional

from mosaic_orchestrator.tool import Tool
from mosaic_orchestrator.pdk import PDK


class Config:
    """helper class to hold a configuration for a task hierarchy.

    Subclass this class to set up a configuration.
    """

    def get_pdk(self) -> Optional[PDK]:
        """Optional override this methode and return your PDK here."""
        return None

    def get_parameters(self) -> Dict[str, object]:
        """Optional override this methode and return your Parameters here."""
        return {}

    def get_tools(self) -> List[Tool]:
        """Optional override this methode and return your Tools here."""
        return []

    def get_objects_to_register(self) -> Dict[Union[Type, str], object]:
        """Optional override this methode and return your objects to register for injection here."""
        return {}

    def get_cache_directory(self) -> Optional[Path]:
        """Optional override this methode and return your custom cache directory here."""
        return None

    def get_run_directory(self) -> Optional[Path]:
        """Optional override this methode and return your custom run directory here."""
        return None
