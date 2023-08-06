"""this module contains the abstract PDK implementation"""
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from semantic_version import Version, NpmSpec

from mosaic_orchestrator.result import Result
from mosaic_orchestrator.utils import LifeCycleListener


@dataclass
class PdkItem:
    """Single entry in the PDK, subclass to implement more functionality"""
    version: str
    name: str

    def __init__(self, name:str, version:str) -> None:
        self.name = name
        self.version = version

    def _try_init(self) -> bool:
        """is called during initialization, can be used for custom validation"""
        return True

class NonCachablePdkItem(PdkItem):
    """PdkItems should only change when the version is changed.
    Therefore, if a PDKItem is using lambdas or other non-cachable constructs,
    then use this PdkItem instead.
    """

    def __getstate__(self):
        return {"name": self.name, "version": self.version}

    def __setstate__(self, state):
        import pdb
        pdb.set_trace()
        self.__dict__.update(self.__class__(**state).__dict__)

@dataclass
class FileBasePdkItem(PdkItem):
    """File PdkItem implementation. Contains a path, validation fails if file not exists."""
    path: str = None

    def _try_init(self) -> bool:
        return self.exists()

    def exists(self) -> bool:
        """checks if th file exists"""
        return os.path.exists(self.path)


@dataclass
class Library:
    """A Library can be used to combine related Items"""
    name: str
    items: List[PdkItem]


def _get_highest_version(version_matches):
    """returns the highest version matches the pattern"""
    return sorted(version_matches,
                  key=lambda v: Version(v.version))[-1]


class PDK(ABC):
    """abstract base PDK implementation, use RootPDK for lifecycle dependent PDKs"""

    def get_item(self, name, versions: str = None) -> Result[PdkItem]:
        """get a item from the pdk identified by its name and a versions string.

        The versions string follows the NPM range specification scheme
        (https://docs.npmjs.com/about-semantic-versioning). When multiple versions match the newest
        one is returned.

        Returns:
            A `Result` object containing either the item or an error.
        """
        name_matches = list(filter(lambda v: v.name == name, self.supported_items()))

        version_matches = list(
            filter(lambda v: Version(v.version) in NpmSpec(versions), name_matches))

        if version_matches:
            return Result.Ok(_get_highest_version(version_matches))

        return Result.Fail(f"PDKItem {name} in version {versions} not found")

    @abstractmethod
    def supported_items(self) -> List[PdkItem]:
        """implement this method to provide a list of all items supported by your implementation."""
        raise NotImplementedError("supported_items not implemented")

    @abstractmethod
    def get_library(self, name) -> Library:
        """implement this method to provide a library for the given name"""
        raise NotImplementedError("get_library not implemented")

    @abstractmethod
    def supported_libraries(self) -> List[Library]:
        """implement this method to provide a list of all libraries supported by your implementation."""
        raise NotImplementedError("supported_libraries not implemented")


class RootPDK(PDK, ABC, LifeCycleListener):
    """Abstract base class for a PDK.

    Implementation of the `task_hash` method is mandatory in order to include the PDK in the state
    representation of a `CachableTask`.
    """

    @abstractmethod
    def task_hash(self):
        """represents the state of this PDK. The same function will be used for all PDK items in
        the task hierarchy.
        """
        raise NotImplementedError("task_hash not implemented")

    def _on_start(self):
        """Is called before run() is executed. Can be used for example to initialize the PDK or connect to
        a database """

    def _on_end(self, exception: Exception = None):
        """Is called after run() is executed. Can be used to de-initialize the PDK, e.g. disconnect from DB or close
        file... """
