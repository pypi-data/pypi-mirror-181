from enum import Enum
from typing import List


class InstantiationForbiddenError(Exception):
    pass


class ConfigAttributeErrorType(str, Enum):
    NOT_SET = "Not set"
    INVALID_VALUE = "Invalid value"


class ConfigAttributeError(Exception):
    __slots__ = ["error_type", "attribute_name", "required_type"]

    def __init__(
        self,
        error_type: ConfigAttributeErrorType,
        attribute_name: str,
        required_type: type,
    ):
        self.error_type = error_type
        self.attribute_name = attribute_name
        self.required_type = required_type

    def __repr__(self):
        return f"{self.attribute_name}: {self.error_type}"

    def __str__(self) -> str:
        return f"{self.attribute_name}: {self.error_type}. Required type: {self.required_type}"


class ValidationError(Exception):
    __slots__ = ["errors"]

    def __init__(self, errors: List[ConfigAttributeError]):
        self.errors = errors
