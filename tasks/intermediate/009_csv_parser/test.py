from buggy import parse_csv

def test_simple():
    assert parse_csv("a,b,c") == ["a", "b", "c"]

def test_quoted_comma():
    assert parse_csv('a,"b,c",d') == ["a", "b,c", "d"]

def test_quoted_quotes():
    assert parse_csv('a,"b""c",d') == ["a", 'b"c', "d"]

def test_single():
    assert parse_csv("hello") == ["hello"]

def test_empty_fields():
    assert parse_csv("a,,c") == ["a", "", "c"]
