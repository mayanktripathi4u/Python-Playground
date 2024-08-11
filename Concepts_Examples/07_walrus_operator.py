"""
List Comprehensions
The walrus operator can simplify list comprehensions by reducing the need to call a function multiple times:
"""

items = [1,4,9, 'Apple', 'Tom']

def expensive_function(item):
    return item

# Without walrus operator
results = []
for item in items:
    result = expensive_function(item)
    if result is not None:
        results.append(result)

# With walrus operator
results = [result for item in items if (result := expensive_function(item)) is not None]

"""
Here, expensive_function(item) is called only once per item, and its result is used both to check if it is not None and to append it to the list.
"""