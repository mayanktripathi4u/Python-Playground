def is_even_or_add(n):
    if n%2 == 0:
        return "Even"
    else:
        return "Odd"
    

def test_even_num():
    result = is_even_or_add(4)
    print(f"Result for Test number 4: {result}")


def test_odd_num():
    result = is_even_or_add(7)
    print(f"Result for Test number 7: {result}")    


def test_large_even_number():
    result = is_even_or_add(1000000000000)
    assert result == "Even", "1000000000000 should be even."

