import inspect
from typing import Any
from needle.api import DependencyParameter
from needle.dependent import CallableDependent


def test_get_dependencies_1d_func() -> None:
    def foo():
        pass

    assert tuple(CallableDependent(foo).get_dependencies()) == ()


def test_get_dependencies_1d_class() -> None:
    class Foo:
        pass

    assert tuple(CallableDependent(Foo).get_dependencies()) == ()


def test_get_dependencies_2d_func() -> None:
    def foo(bar: str) -> None:
        return None

    inspect.Parameter

    assert tuple(CallableDependent(foo).get_dependencies()) == (
        DependencyParameter(
            dependency=CallableDependent(str),
            parameter=inspect.Parameter(
                name="bar",
                kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=str,
            ),
        ),
    )


def test_get_dependencies_2d_class() -> None:
    class Foo:
        def __init__(self, bar: str) -> None:
            pass

    assert tuple(CallableDependent(Foo).get_dependencies()) == (
        DependencyParameter(
            dependency=CallableDependent(str),
            parameter=inspect.Parameter(
                name="bar",
                kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=str,
            ),
        ),
    )


def test_get_dependencies_2d_obj() -> None:
    class Foo:
        def __call__(self, bar: str) -> None:
            ...

    foo: Foo = Foo()

    assert tuple(CallableDependent(foo).get_dependencies()) == (
        DependencyParameter(
            dependency=CallableDependent(str),
            parameter=inspect.Parameter(
                name="bar",
                kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=str,
            ),
        ),
    )
