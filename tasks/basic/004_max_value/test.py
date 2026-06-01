from buggy import find_max

def test_max_positive():
    assert find_max([1, 5, 3, 9, 2]) == 9

def test_max_negative():
    assert find_max([-5, -2, -8, -1]) == -1

def test_max_single():
    assert find_max([42]) == 42

def test_max_empty():
    assert find_max([]) is None

def test_max_mixed():
    assert find_max([-10, 0, 10]) == 10
