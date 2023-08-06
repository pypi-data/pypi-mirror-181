"""This module contains a simple cache implementation"""
import os
import pickle
from typing import List, IO


class Cache:
    """simple file cache implementation. Keys are used as filenames and values are saved inside the
    file."""

    def __init__(self, directory=".cache"):
        self.files: List[IO] = []
        self.directory = directory
        os.makedirs(directory, exist_ok=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        for file in self.files:
            file.close()

    def put(self, key: str, value):
        """puts a value for the given key into the cache, if value is none, the entry is deleted"""
        if value is None:
            self.clear(key)
            return

        with open(self._make_path(key), 'wb') as file:
            pickle.dump(value, file)

    def get(self, key: str):
        """return the value for the given key, None if not available"""
        try:
            with open(self._make_path(key), 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return None

    def clear(self, key: str=None):
        """removes an entry for given key, if key is None, the entire cache is cleared"""
        if key is None:
            for file in os.scandir(self.directory):
                os.remove(file.path)
        else:
            path = self._make_path(key)
            if os.path.exists(path):
                os.remove(path)

    def _make_path(self, key: str):
        """return the file path for the given key"""
        path = os.path.join(self.directory, key)
        return path
