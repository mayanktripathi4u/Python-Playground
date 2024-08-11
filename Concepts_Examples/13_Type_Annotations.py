"""
# Type annotations 
Type annotations in Python are a feature introduced in Python 3.5 and enhanced in subsequent versions. 
They allow you to explicitly declare the types of variables, function parameters, and return values, which can help with code clarity, editor support, and static type checking.

# Benefits of Type Annotations
1. Improved Code Readability: Annotations make the expected types of variables and function parameters clear, improving code readability.
2. Static Type Checking: Tools like mypy, Pyright, or PyCharm's built-in checker can analyze your code for type errors before runtime.
3. Enhanced IDE Support: IDEs and editors can provide better autocomplete and inline documentation based on type information.

# Basic Syntax of Type Annotations
1. Variable Annotations
"""

age: int = 25
name: str = "Alice"

# Here, age is annotated as an int, and name is annotated as a str.

'''
2. Function Annotations

Type annotations for functions include annotations for parameters and return values.

'''
def greet(name: str) -> str:
    return f"Hello, {name}!"

'''
* name: str indicates that the name parameter should be a str.
* -> str specifies that the function returns a str.
'''

'''
3. Complex Data Structures

For complex data types like lists, dictionaries, and tuples, you use the typing module.

'''

from typing import List, Dict, Tuple

def process_items(items: List[int]) -> Dict[str, int]:
    result = {"sum": sum(items), "count": len(items)}
    return result

def get_coordinates() -> Tuple[float, float]:
    return (40.7128, -74.0060)

'''
* List[int] specifies a list of integers.
* Dict[str, int] specifies a dictionary with string keys and integer values.
* Tuple[float, float] specifies a tuple containing two float values.
'''