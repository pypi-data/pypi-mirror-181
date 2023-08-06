"""this module contains mosaic unrelated helper methods"""
from __future__ import annotations

import logging
import typing
from typing import Type, runtime_checkable, Protocol


def get_all_parameters(instance):
    """returns a list of all parameters of an object"""
    return {name: getattr(instance, name) for name in _get_fields_of_type(type(instance))
            if hasattr(instance, name)}


def _get_fields_of_type(wanted_type: Type):
    """return all fields of a class (type)"""
    fields = []
    for base in wanted_type.__bases__:
        fields.extend(_get_fields_of_type(base))

    for name in get_type_annotations(wanted_type).keys():
        fields.append(name)

    for name in wanted_type.__dict__.keys():
        if name[-2:] != '__':
            fields.append(name)

    return fields


def get_type_annotations(cls):
    """return all type hints of a class"""
    return typing.get_type_hints(cls)


def get_type_of_class_field(instance, name: str) -> Type:
    """return the type of class field with given name. If the field is not available an error will be raised."""
    annotations = get_type_annotations(type(instance))
    if name in annotations:
        return annotations[name]

    parameters = _get_fields_of_type(type(instance))
    for param in parameters:
        if name == param:
            return type(getattr(type(instance), name))

    if hasattr(instance, name):
        return type(getattr(instance, name))

    raise ValueError(f"{name} not found in parameters of {instance}")


def is_function(value) -> bool:
    """check it is a function"""
    return callable(value) and not isinstance(value, type)


class ListHandler(logging.Handler):
    """List logging handler"""
    def __init__(self):
        logging.Handler.__init__(self)
        self.log_list = []

    def emit(self, record):
        """append a record to the log list"""
        self.log_list.append(record)


@runtime_checkable
class LifeCycleListener(Protocol):
    """The methods of this protocol are called before startup and after teardown of a run."""
    # pylint: disable=too-few-public-methods

    def _on_start(self):
        """called before the run of the root task."""

    def _on_end(self, exception: Exception = None):
        """called after the run of the root task.

        This method is called even if an exception is thrown during the run, similar to
        try-catch-finally in python.

        Args:
            exception: if the run aborted with an exception it is passed as an argument.
        """
