from buggy import parse_query_string

def test_simple():
    assert parse_query_string("a=1&b=2") == {"a": "1", "b": "2"}

def test_value_has_equals():
    result = parse_query_string("data=a=b=c")
    assert result == {"data": "a=b=c"}

def test_no_value():
    assert parse_query_string("flag") == {"flag": ""}

def test_empty():
    assert parse_query_string("") == {}

def test_empty_pair():
    assert parse_query_string("a=1&&b=2") == {"a": "1", "b": "2"}
