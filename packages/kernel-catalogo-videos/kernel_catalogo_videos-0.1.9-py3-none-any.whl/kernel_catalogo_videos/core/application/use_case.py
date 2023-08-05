# Python
import abc
from typing import Generic, TypeVar

Input = TypeVar("Input")
Output = TypeVar("Output")


class UseCase(Generic[Input, Output], abc.ABC):
    @abc.abstractmethod
    def execute(self, input_params: Input) -> Output:
        raise NotImplementedError()
