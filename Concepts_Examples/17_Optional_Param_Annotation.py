'''
# Using Optional for Optional Parameters
If a parameter can be of a specific type or None, use Optional from the typing module.

'''
from typing import Optional

def find_item(item_id: int) -> Optional[str]:
    items = {1: "apple", 2: "banana", 3: "cherry"}
    return items.get(item_id)

print(find_item(2))  # Output: banana
print(find_item(4))  # Output: None

# Here, find_item may return a str or None, indicating that the item was not found.


