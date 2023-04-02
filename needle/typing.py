from typing import Callable, Sequence, TypeVar

__all__: Sequence[str] = ("DependencyProvider",)


T = TypeVar("T")

DependencyProvider = Callable[..., T]
