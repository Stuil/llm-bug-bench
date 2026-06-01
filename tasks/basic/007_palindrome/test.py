from buggy import is_palindrome

def test_empty_string():
    assert is_palindrome("") is True

def test_single_char():
    assert is_palindrome("a") is True

def test_simple():
    assert is_palindrome("racecar") is True

def test_non_palindrome():
    assert is_palindrome("hello") is False

def test_case_insensitive():
    assert is_palindrome("RaceCar") is True

def test_with_spaces():
    assert is_palindrome("A man a plan a canal Panama") is True

def test_with_punctuation():
    assert is_palindrome("Able was I, ere I saw Elba!") is True
