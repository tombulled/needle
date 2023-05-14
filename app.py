from dataclasses import dataclass
from needle import Dependent, CallableDependent, SolvedDependent, Container, InjectorImpl


@dataclass
class Dog:
    name: str


@dataclass
class Person:
    dog: Dog


def dog() -> Dog:
    return Dog(name="Luna")


i: Container = InjectorImpl()

i.register(CallableDependent(dog))

d: Dependent[Person] = CallableDependent(Person)
s: SolvedDependent[Person] = i.solve(d)
p: Person = s.execute()
