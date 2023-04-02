from dataclasses import dataclass
import inspect
from typing import Any, Iterable, Mapping, MutableMapping, Optional, Sequence, TypeVar

from . import utils
from .api import Dependent, DependencyParameter, SolvedDependent
from .typing import DependencyProvider

__all__: Sequence[str] = ("SolvedDependentImpl",)

T = TypeVar("T")


@dataclass
class SolvedDependentImpl(SolvedDependent[T]):
    dependency: Dependent[T]
    dag: Mapping[Dependent[Any], Iterable[DependencyParameter]]

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
        dependency_parameters: Iterable[DependencyParameter]
        for dependency, dependency_parameters in self.dag.items():
            if dependency is self.dependency:
                continue

            arguments: MutableMapping[str, Any] = {}

            dependency_parameter: DependencyParameter
            for dependency_parameter in dependency_parameters:
                value: Any

                if dependency_parameter.parameter.annotation in resolved:
                    value = resolved[dependency_parameter.parameter.annotation]
                else:
                    value = dependency_parameter.dependency.call()

                resolved[dependency_parameter.parameter.annotation] = value

                arguments[dependency_parameter.parameter.name] = value

            args: Sequence[Any]
            kwargs: Mapping[str, Any]
            args, kwargs = utils.prepare_arguments(dependency.call, arguments)

            resolved[
                inspect.signature(dependency.call).return_annotation
            ] = dependency.call(*args, **kwargs)

        arguments: MutableMapping[str, Any] = {}

        dependency_parameter: DependencyParameter
        for dependency_parameter in self.dag[self.dependency]:
            arguments[dependency_parameter.parameter.name] = resolved[
                dependency_parameter.parameter.annotation
            ]

        args: Sequence[Any]
        kwargs: Mapping[str, Any]
        args, kwargs = utils.prepare_arguments(self.dependency.call, arguments)

        return self.dependency.call(*args, **kwargs)
