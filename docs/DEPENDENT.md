# Dependent
A *dependent* is an entity that may have one or more dependencies, and may itself be dependended upon.

For example, lets define an `Animal` type:
```python
from dataclasses import dataclass

@dataclass
class Animal:
    name: str
```

Then, let's create an instance of this class:
```python
animal: Animal = Animal(name="Buster")
```

We can now create a *dependent*:
```python
from needle.api import Dependent

Dependent.of(animal)
```


#############

A "dependency" can have the following information:
* An optional "name", e.g. `"elasticsearchClient"`
* A type, e.g. `ElasticsearchClient`
* A sequence of dependencies





#############

## Dependency Provider
A *dependency provider* is a callable which accepts any number of arguments, and returns an instance of the dependent.

Then, let's create a *dependency provider*:
```python
def animal() -> Animal:
    return Animal(name="Buster")
```