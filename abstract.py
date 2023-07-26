from dataclasses import dataclass

from needle.api import Dependent, Container

"""
Current problem:

@bean
def dogs() -> List[Dog]:
    ...

^ How do I get that to inject successfully for a type of List[Animal]?
"""


@dataclass(unsafe_hash=True)
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
