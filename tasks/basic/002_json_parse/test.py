from buggy import parse_json

def test_parse_valid():
    assert parse_json('{"a": 1}') == {"a": 1}

def test_parse_empty_string():
    assert parse_json("") is None

def test_parse_whitespace():
    assert parse_json("   ") is None

def test_parse_invalid():
    assert parse_json("{invalid}") is None

def test_parse_list():
    assert parse_json("[1, 2, 3]") == [1, 2, 3]
