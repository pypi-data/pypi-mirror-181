"""this module contains the Result and Validation classes"""
from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Generic, TypeVar


class Validation(ABC):
    """represents the result of a validation.

    This class is not intended to be subclassed by client code. Use the `ValidationSuccess` object
    and the `ValidationError` class instead.
    """
    # pylint: disable=too-few-public-methods

    @classmethod
    def of(cls, success: bool, message: str) -> Validation:
        """convenience method to create a `Validation` object based on a flag and an error message.

        Args:
            success: when True this function returns ValidationSuccess, otherwise a `ValidationError`
                containing `message` is returned
            message: the error message
        """
        if success:
            return ValidationSuccess
        return ValidationError(message)


class _Success(Validation):
    # pylint: disable=too-few-public-methods
    pass


ValidationSuccess = _Success()
"""Static validation result for success"""


@dataclass
class ValidationError(Validation):
    """Validation result for error with optional message"""
    message: Optional[str] = None


T = TypeVar("T")


@dataclass
class Result(Generic[T]):
    """a generic result that contains either an error or a value."""
    success: bool
    value: Optional[T]
    error: Optional[str]

    def raise_on_fail(self) -> T:
        """Raise an error if the result is not successful"""
        if not self.success:
            raise ValueError(
                ErrorDefinition(error_type=ErrorType.GENERAL_ERROR, message=self.error, source=None)
            )
        return self.value

    @property
    def failure(self):
        """True if operation failed, False if successful (read-only)."""
        return not self.success

    @classmethod
    def Fail(cls, error: str):
        """Create a Result object for a failed operation."""
        return cls(False, value=None, error=error)

    @classmethod
    def Ok(cls, value=Optional[T]):
        """Create a Result object for a successful operation."""
        return cls(True, value=value, error=None)


class ErrorType(Enum):
    """Defines the types of errors that can happen when building a task hierarchy."""
    MISSING_PARAMETER = 1
    """a parameter without default value is not set. `source` contains the path to the parameter."""
    PARAMETER_ERROR = 2
    """a dependency could not be found or a supplied parameter-path could not be found."""
    MISSING_TOOL = 3
    """a tool could not be found."""
    TOOL_ERROR = 4
    """general error in connection with a tool."""
    PDK_ERROR = 5
    """general error in connection with the pdk or a view."""
    MISSING_PDK_ITEM = 6
    """a view was not found in the pdk."""
    GENERAL_ERROR = 7
    """an unspecified error has occurred"""
    VALIDATION_ERROR = 8
    """a validation failed."""


@dataclass
class ErrorDefinition:
    """Represents an framework error with type, message and source"""
    error_type: ErrorType
    message: str
    source: object
