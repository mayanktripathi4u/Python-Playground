# Annotating Lists and Dictionaries

from typing import List, Dict

def summarize_scores(scores: List[int]) -> Dict[str, float]:
    total = sum(scores)
    average = total / len(scores) if scores else 0
    return {"total": total, "average": average}

print(summarize_scores([95, 85, 76, 88]))  
# Output: {'total': 344, 'average': 86.0}

'''
In this example, scores is a list of integers, and the function returns a dictionary with string keys and float values.
'''
