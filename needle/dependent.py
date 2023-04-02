from dataclasses import dataclass
import inspect
from typing import Any, Generic, MutableSequence, Sequence, TypeVar

from .typing import DependencyProvider

__all__: Sequence[str] = (
    "Dependent",
    "DependencyParameter",
    "DependentImpl",
)


T = TypeVar("T")


class Dependent(Generic[T]):
    call: DependencyProvider[T]

    def get_dependencies(self) -> Sequence["DependencyParameter"]:
        ...


@dataclass
class DependencyParameter:
    dependency: Dependent
    parameter: inspect.Parameter


@dataclass(frozen=True)
class DependentImpl(Dependent[T]):
    call: DependencyProvider[T]

    def get_dependencies(self) -> Sequence[DependencyParameter]:
        signature: inspect.Signature = inspect.signature(self.call)

        dependencies: MutableSequence[DependencyParameter] = []

        parameter: inspect.Parameter
        for parameter in signature.parameters.values():
            annotation: Any = parameter.annotation

            if not callable(annotation):
                raise Exception("Parameter annotation is not callable")

            dependency: Dependent = DependentImpl(annotation)
            dependency_parameter: DependencyParameter = DependencyParameter(
                dependency=dependency,
                parameter=parameter,
            )

            dependencies.append(dependency_parameter)

        return dependencies
