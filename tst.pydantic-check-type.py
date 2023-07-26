from dataclasses import dataclass
from typing import List
from pydantic import TypeAdapter

@dataclass
class Animal:
    name: str


class Dog(Animal):
    pass


class Cat(Animal):
    pass

typ = List[Animal]
# data = [Dog("Luna"), Cat("Batman")]
typ2 = List[Dog]

validator: TypeAdapter = TypeAdapter(typ, config={"strict": True})

d = validator.validate_python(data)
