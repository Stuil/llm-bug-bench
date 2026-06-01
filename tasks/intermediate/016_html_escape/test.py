from buggy import escape_html

def test_angle_brackets():
    assert escape_html("<script>") == "&lt;script&gt;"

def test_ampersand():
    assert escape_html("a & b") == "a &amp; b"

def test_double_quote():
    assert escape_html('say "hello"') == "say &quot;hello&quot;"

def test_ampersand_before_lt():
    assert escape_html("< & >") == "&lt; &amp; &gt;"

def test_plain_text():
    assert escape_html("hello world") == "hello world"
