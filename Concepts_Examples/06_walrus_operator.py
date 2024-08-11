"""
Looping and Conditional Statements
The walrus operator is useful in loops to both assign and use a variable:
"""

# Traditional approach
values = []
while True:
    value = input("Enter a value (or 'done' to finish): ")
    if value == 'done':
        break
    values.append(value)

# Using walrus operator
values = []
while (value := input("Enter a value (or 'done' to finish): ")) != 'done':
    values.append(value)


# In this example, the walrus operator allows you to both capture and check the user input in a single line.
