from dataclasses import dataclass
import inspect
from typing import (
    Any,
    Iterable,
    Mapping,
    MutableMapping,
    Optional,
    Protocol,
    Sequence,
    TypeVar,
)

from .typing import DependencyProvider

__all__: Sequence[str] = (
    "Dependent",
    "DependencyParameter",
    "SolvedDependent",
    "Container",
)


T = TypeVar("T")


class Dependent(Protocol[T]):
    type: Any

    def get_dependencies(self) -> Sequence["Dependent"]:
        ...

    @staticmethod
    def on(type_: Any, /) -> "Dependent[T]":
        return IdentityDependent(type_)

    @staticmethod
    def of(type_: Any, value: T, /) -> "Dependent[T]":
        return SupplierDependent(type=type_, value=value)


class BuildableDependent(Dependent[T], Protocol[T]):
    def build(self, dependencies: Mapping["Dependent", Any], /) -> T:
        ...


@dataclass(unsafe_hash=True)
class UnsatisfiableDependent(Dependent[T]):
    type: Any = Any

    @staticmethod
    def get_dependencies() -> Sequence[Dependent]:
        return []


@dataclass(unsafe_hash=True)
class IdentityDependent(BuildableDependent[T]):
    type: Any
    
    @property
    def sub_dependent(self) -> Dependent[T]:
        return UnsatisfiableDependent(self.type)

    def get_dependencies(self) -> Sequence[Dependent]:
        return [self.sub_dependent]

    def build(self, dependencies: Mapping["Dependent", Any], /) -> T:
        assert len(dependencies) == 1

        return dependencies[self.sub_dependent]


@dataclass(unsafe_hash=True)
class SupplierDependent(BuildableDependent[T]):
    type: Any
    value: T

    @staticmethod
    def get_dependencies() -> Sequence[Dependent]:
        return []

    def build(self, dependencies: Mapping[Dependent, Any], /) -> T:
        assert not dependencies

        return self.value


@dataclass
class DependencyParameter:
    dependency: Dependent
    parameter: inspect.Parameter


class SolvedDependent(Protocol[T]):
    dependency: Dependent[T]
    dag: Mapping[Dependent[Any], Iterable[Dependent]]

    def execute(
        self, *, values: Optional[Mapping[DependencyProvider[Any], Any]] = None
    ) -> T:
        ...


@dataclass
class StaticSolvedDependent(SolvedDependent[T]):
    dependency: Dependent[T]
    dag: Mapping[Dependent[Any], Iterable[Dependent]]

    def execute(
        self, *, values: Optional[Mapping[DependencyProvider[Any], Any]] = None
    ) -> T:
        if values is None:
            values = {}

        resolved: MutableMapping[Any, Any] = {}

        # For now, assume that all of the values have no sub-dependencies,
        # so can be immediately resolved
        resolved.update(values)

        dependency: Dependent[Any]
        dependency_parameters: Iterable[Dependent]
        for dependency, dependency_parameters in self.dag.items():
            if dependency is self.dependency:
                continue

            arguments: MutableMapping[Dependent[Any], Any] = {}

            dependency_parameter: Dependent
            for dependency_parameter in dependency_parameters:
                value: Any

                if dependency_parameter.type in resolved:
                    value = resolved[dependency_parameter.type]
                else:
                    value = dependency_parameter.build({})

                resolved[dependency_parameter.type] = value

                arguments[dependency_parameter] = value

            resolved[dependency.type] = dependency.build(arguments)

        args: MutableMapping[Dependent[Any], Any] = {}

        dependency_parameter: Dependent[Any]
        for dependency_parameter in self.dag[self.dependency]:
            args[dependency_parameter] = resolved[dependency_parameter.type]

        return self.dependency.build(args)


class Container(Protocol):
    def solve(self, dependent: Dependent[T], /) -> SolvedDependent[T]:
        ...

    @staticmethod
    def of(*dependents: Dependent) -> "Container":
        return StaticContainer(dependencies=dependents)


class MutableContainer(Container):
    def register(self, dependent: Dependent[T], /) -> None:
        ...


@dataclass
class StaticContainer(Container):
    dependencies: Sequence[Dependent]

    def solve(self, dependent: Dependent[T], /) -> SolvedDependent[T]:
        dag: MutableMapping[Dependent[Any], Iterable[Dependent]] = {}

        registered_dependency: Dependent[Any]
        for registered_dependency in self.dependencies:
            dag[registered_dependency] = registered_dependency.get_dependencies()

        dag[dependent] = dependent.get_dependencies()

        return StaticSolvedDependent(
            dependency=dependent,
            dag=dag,
        )
