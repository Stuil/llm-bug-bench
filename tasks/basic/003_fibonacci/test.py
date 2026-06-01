from buggy import fibonacci

def test_fib_0():
    assert fibonacci(0) == 0

def test_fib_1():
    assert fibonacci(1) == 0

def test_fib_2():
    assert fibonacci(2) == 1

def test_fib_10():
    assert fibonacci(10) == 55

def test_fib_20():
    assert fibonacci(20) == 6765
