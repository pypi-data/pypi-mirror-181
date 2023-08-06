"""This module is responsible for assets"""
import hashlib
from typing import Union, List
from pathlib import Path
import pkg_resources
from _hashlib import HASH as Hash
from mosaic_orchestrator.utils import LifeCycleListener
from mosaic_orchestrator.task import Hashable


class Asset(Hashable, LifeCycleListener):
    """This class represents one asset and handel the hash calculation"""
    # pylint: disable=too-few-public-methods

    def __init__(self, module: str, *paths: List[str]) -> None:
        """Asset

        Args:
            paths (List[str]): Path to some assets
            module (str, optional): If set to __name__, then the paths
                                    are converted to absolute paths automatically (relative to the package).
                                    Defaults to None.
        """

        if module is not None:
            self.paths = [pkg_resources.resource_filename(module, path) for path in paths]
        else:
            self.paths = paths  # list of paths belonging to this asset -> they end up in the manifest

    def _on_start(self):
        """Override this method to optional start/load the asset before run()"""

    def _on_end(self, exception: Exception = None):
        """Override this method to optional stop/unload the asset after run()"""

    def task_hash(self):
        """Calculate the hash for the asset, is used to evaluate the cache state"""
        hash_str = ""
        for path in self.paths:
            hash_str += md5_path(path)
        return hash_str


def md5_update_from_file(filename: Union[str, Path], current_hash: Hash) -> Hash:
    """returns updated md5 hash of given file"""
    assert Path(filename).is_file()
    with open(str(filename), "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            current_hash.update(chunk)
    return current_hash


def md5_file(filename: Union[str, Path]) -> str:
    """returns md5 hash of given file"""
    return str(md5_update_from_file(filename, hashlib.md5()).hexdigest())


def md5_update_from_dir(directory: Union[str, Path], current_hash: Hash) -> Hash:
    """returns md5 hash of given directory"""
    assert Path(directory).is_dir()
    for path in sorted(Path(directory).iterdir(), key=lambda p: str(p).lower()):
        current_hash.update(path.name.encode())
        if path.is_file():
            current_hash = md5_update_from_file(path, current_hash)
        elif path.is_dir():
            current_hash = md5_update_from_dir(path, current_hash)
    return current_hash


def md5_path(path: Union[str, Path]) -> str:
    """returns md5 hash of given path"""
    path = Path(path)
    if path.is_file():
        return md5_update_from_file(path, hashlib.md5()).hexdigest()
    if path.is_dir():
        return str(md5_update_from_dir(path, hashlib.md5()).hexdigest())
    raise Exception(f"Path {path} is not a file nor a directory!")
