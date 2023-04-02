from dataclasses import dataclass
import inspect
from typing import Any, Iterable, Mapping, Optional, Protocol, Sequence, TypeVar

from .typing import DependencyProvider

__all__: Sequence[str] = (
    "Dependent",
    "DependencyParameter",
    "SolvedDependent",
    "Injector",
)


T = TypeVar("T")


class Dependent(Protocol[T]):
    call: DependencyProvider[T]

    def get_dependencies(self) -> Sequence["DependencyParameter"]:
        ...


@dataclass
class DependencyParameter:
    dependency: Dependent
    parameter: inspect.Parameter


class SolvedDependent(Protocol[T]):
    dependency: Dependent[T]
    dag: Mapping[Dependent[Any], Iterable[DependencyParameter]]

    def execute(
        self, *, values: Optional[Mapping[DependencyProvider[Any], Any]] = None
    ) -> T:
        ...


class Injector(Protocol):
    def register(self, dependency: Dependent[T]) -> None:
        ...

    def solve(self, dependency: Dependent[T]) -> SolvedDependent[T]:
        ...
