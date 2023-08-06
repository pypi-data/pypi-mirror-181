"""This modul contains more advanced PDK items for JSON, YAML and Python files"""
from dataclasses import dataclass
import json
import os
import yaml
import types
from yaml.loader import SafeLoader
import importlib.machinery
import xml.etree.ElementTree as ET

from mosaic_orchestrator.pdk import FileBasePdkItem


class JSONPdkItem(FileBasePdkItem):
    """A PDK item representing a JSON file. Expects to have a "path" field containing a valid filepath.

    Attributes:
        data: the loaded json
    """
    # pylint: disable=too-few-public-methods

    def _try_init(self) -> bool:
        if not super()._try_init():
            return False
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                self.data = json.load(file)
        except EnvironmentError as error:
            print(error)
            return False
        return True


class YAMLPdkItem(FileBasePdkItem):
    """A PDK item representing a YAML file. Expects to have a "path" field containing a valid filepath.

    Attributes:
        data: the loaded yaml
    """
    # pylint: disable=too-few-public-methods

    def _try_init(self) -> bool:
        if not super()._try_init():
            return False
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                self.data = yaml.load(file, Loader=SafeLoader)
        except EnvironmentError as error:
            print(error)
            return False
        return True

class XMLPdkItem(FileBasePdkItem):
    """A PDK item representing a XML file. Expects to have a "path" field containing a valid filepath.

    Attributes:
        root: the loaded xml root
        tree: the loaded xml tree
    """
    # pylint: disable=too-few-public-methods

    def _try_init(self) -> bool:
        if not super()._try_init():
            return False
        try:
            self.tree = ET.parse(self.path)
            self.root = self.tree.getroot()
        except EnvironmentError as error:
            print(error)
            return False
        return True
