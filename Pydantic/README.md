# Pydantic
Pydantic is Python's most popular data validation library and uses type-hint to do this validation.

If you are already using Type-Hints in your code, then this should feel pretty natural to add to your projects.

Pydanti'c primary purpose is to ensure that the data coming into our application meets certain expectations. 

If you ever striggled with the data coming into your applications not being the right type or format, or if you've written a lot of manual validation code thats ugly and hard to maintain, then Pydantic is going to make all of this a lot easier for us.

- Fast API uses this for validating API requests and responses. 
- Its used in data processing to ensure clean data.
- Even in AI, we have Pydantic-AI that allows us to buidl AI agents with structured and validated outputs.

# Manual Validation Vs Pydantic Validation
```python
# Manual Validation
def create_user(username, email, age):
    if not isinstance(username, str):
        raise TypeError("Username must be a string")
    if not isinstance(email, str):
        raise TypeError("Invalid email format")
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")

    return {"username": username, "email": email, "age": age}

user1 = create_user("abcdef", "abcedf@somerandom.com", 38)
print(user1)

user2 = create_user("john doe", None, "old")
print(user2)

```
Note: Above it will fail for user2, for email and after fixing it, will fail again for age. So it wont show both the errors.

```python
# Pydantic Validation
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    age: int

user1 = User(username="abcdef", email = "abcedf@somerandom.com", age=30)
print(user1)

user2 = User(username="john doe", email = None, age = "old")
print(user2)
```

# Limitation
- Changing field value after creation doesn't trigger revalidation. Its only during creation.


