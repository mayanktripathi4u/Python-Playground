'''
# Annotating Classes
You can also annotate class attributes and methods.
'''

class Person:
    def __init__(self, name: str, age: int):
        self.name: str = name
        self.age: int = age

    def birthday(self) -> None:
        self.age += 1

    def __str__(self) -> str:
        return f"{self.name} is {self.age} years old"

p = Person("Alice", 30)
print(p)  # Output: Alice is 30 years old
p.birthday()
print(p)  # Output: Alice is 31 years old


