from buggy import calculate_discount

def test_no_discount():
    assert calculate_discount([(10.00, 2)], 0) == 20.00

def test_simple_discount():
    assert calculate_discount([(100.00, 1)], 0.1) == 90.00

def test_multiple_items():
    result = calculate_discount([(10.00, 3), (5.00, 2)], 0.2)
    expected = round((30.00 + 10.00) * 0.8, 2)
    assert result == expected

def test_rounding():
    result = calculate_discount([(9.99, 3)], 0.1)
    assert result == round(29.97 * 0.9, 2)

def test_precision():
    result = calculate_discount([(2.675, 1)], 0)
    assert result == 2.68
