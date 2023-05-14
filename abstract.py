from dataclasses import dataclass

from needle.api import Dependent, Container


@dataclass
class Animal:
    name: str


class Dog(Animal):
    pass


class Cat(Animal):
    pass


container: Container = Container.of(
    Dependent.of(Dog, Dog("Buster")), # () -> Dog
    Dependent.of(Cat, Cat("Cinder")), # () -> Cat
)

cat = container.solve(Dependent.on(Cat))
