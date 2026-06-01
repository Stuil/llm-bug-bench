from buggy import parse_date

def test_dash():
    assert parse_date("2024-01-15") == {"year": 2024, "month": 1, "day": 15}

def test_slash():
    assert parse_date("2024/01/15") == {"year": 2024, "month": 1, "day": 15}

def test_dot():
    assert parse_date("2024.01.15") == {"year": 2024, "month": 1, "day": 15}

def test_invalid():
    assert parse_date("2024-13-01") is None

def test_wrong_format():
    assert parse_date("01-15-2024") is None

def test_gibberish():
    assert parse_date("not-a-date") is None
