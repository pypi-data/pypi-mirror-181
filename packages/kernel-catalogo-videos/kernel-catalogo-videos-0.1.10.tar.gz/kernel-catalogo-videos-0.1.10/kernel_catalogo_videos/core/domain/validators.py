"""
A domain seedwork for validator Interfaces
"""

# Python
import abc
from typing import Any, Dict, List, Generic, TypeVar
from dataclasses import dataclass

ErrorsField = Dict[str, List[str]]
PropsValidated = TypeVar("PropsValidated")


@dataclass(frozen=True)
class ValidatorFieldInterface(abc.ABC, Generic[PropsValidated]):
    """
    Interface for any Validator instance with a validate method
    """

    errors: ErrorsField = None
    validated_data: PropsValidated = None

    @abc.abstractmethod
    def validate(self, validator: Any):
        """
        Abstract method for validate the data
        """
        raise NotImplementedError()
