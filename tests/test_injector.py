from needle.api import Dependent, Container, SolvedDependent
from needle.dependent import CallableDependent
from needle.injector import InjectorImpl


def test_solve_1d_func() -> None:
    def foo() -> str:
        return "foo"

    dependency: Dependent[str] = CallableDependent(foo)

    injector: Container = InjectorImpl()

    solved: SolvedDependent[str] = injector.solve(dependency)

    assert solved.dependency is dependency
    assert set(solved.dag.keys()) == {dependency}
    assert tuple(solved.dag[dependency]) == ()
