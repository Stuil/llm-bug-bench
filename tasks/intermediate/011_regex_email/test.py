from buggy import validate_email

def test_valid():
    assert validate_email("user@example.com") is True

def test_valid_subdomain():
    assert validate_email("user@mail.example.com") is True

def test_no_at():
    assert validate_email("userexample.com") is False

def test_no_domain():
    assert validate_email("user@") is False

def test_no_tld():
    assert validate_email("user@example") is False

def test_double_at():
    assert validate_email("user@test@example.com") is False

def test_special_chars():
    assert validate_email("user+tag@example.com") is True
