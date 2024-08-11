# Traditional Way

numbers: list[int] = list(range(1,11))
text: str = 'Hello, World!'

print(numbers[::-1])
print(text[::-1])

# Slicing Way ;) 

rev: slice = slice(None, None, -1)

print(numbers[rev])
print(text[rev])

f_five: slice = slice(None, 5)
print(numbers[f_five])
print(text[f_five])
