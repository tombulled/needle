from dataclasses import dataclass
import inspect
from typing import Any, MutableSequence, Sequence, TypeVar

from .api import Dependent, DependencyParameter
from .typing import DependencyProvider

__all__: Sequence[str] = ("CallableDependent",)


T = TypeVar("T")


@dataclass(frozen=True)
class CallableDependent(Dependent[T]):
    call: DependencyProvider[T]

    def get_dependencies(self) -> Sequence[DependencyParameter]:
        signature: inspect.Signature = inspect.signature(self.call)

        dependencies: MutableSequence[DependencyParameter] = []

        parameter: inspect.Parameter
        for parameter in signature.parameters.values():
            annotation: Any = parameter.annotation
 
            if annotation is inspect.Parameter.empty:
                annotation = Any

            if not callable(annotation):
                raise Exception("Parameter annotation is not callable")

            dependency: Dependent = CallableDependent(annotation)
            dependency_parameter: DependencyParameter = DependencyParameter(
                dependency=dependency,
                parameter=parameter,
            )

            dependencies.append(dependency_parameter)

        return dependencies
