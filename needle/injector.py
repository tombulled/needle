from dataclasses import dataclass, field
from typing import (
    Any,
    Iterable,
    MutableMapping,
    MutableSequence,
    Sequence,
    TypeVar,
)


from .api import Dependent, DependencyParameter, Injector, SolvedDependent
from .solved import SolvedDependentImpl

__all__: Sequence[str] = ("InjectorImpl",)


T = TypeVar("T")


@dataclass
class InjectorImpl(Injector):
    _dependencies: MutableSequence[Dependent[Any]] = field(default_factory=list)

    def register(self, dependency: Dependent[T]) -> None:
        self._dependencies.append(dependency)

    def solve(self, dependency: Dependent[T]) -> SolvedDependent[T]:
        dag: MutableMapping[Dependent[Any], Iterable[DependencyParameter]] = {}

        registered_dependency: Dependent[Any]
        for registered_dependency in self._dependencies:
            dag[registered_dependency] = registered_dependency.get_dependencies()

        dag[dependency] = dependency.get_dependencies()

        return SolvedDependentImpl(
            dependency=dependency,
            dag=dag,
        )
