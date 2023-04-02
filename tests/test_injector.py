from needle.api import Dependent, Injector, SolvedDependent
from needle.dependent import DependentImpl
from needle.injector import InjectorImpl


def test_solve_1d_func() -> None:
    def foo() -> str:
        return "foo"

    dependency: Dependent[str] = DependentImpl(foo)

    injector: Injector = InjectorImpl()

    solved: SolvedDependent[str] = injector.solve(dependency)

    assert solved.dependency is dependency
    assert set(solved.dag.keys()) == {dependency}
    assert tuple(solved.dag[dependency]) == ()
