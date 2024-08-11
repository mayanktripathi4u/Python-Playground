"""
Simplifying If-Else Expressions
The walrus operator can be used to simplify if-else expressions:
"""

# Traditional approach
def get_user_input():
    user_input = input("Enter something: ")
    if user_input:
        return user_input
    return "Default Value"

# Using walrus operator
def get_user_input():
    if (user_input := input("Enter something: ")):
        return user_input
    return "Default Value"


"""
In this example, the walrus operator assigns the input value to user_input and checks if it is truthy in a single line.
"""