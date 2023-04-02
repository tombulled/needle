from dataclasses import dataclass
from needle import Dependent, DependentImpl, SolvedDependent, Injector, InjectorImpl


@dataclass
class Dog:
    name: str


@dataclass
class Person:
    dog: Dog


def dog() -> Dog:
    return Dog(name="Luna")


i: Injector = InjectorImpl()

i.register(DependentImpl(dog))

d: Dependent[Person] = DependentImpl(Person)
s: SolvedDependent[Person] = i.solve(d)
p: Person = s.execute()
