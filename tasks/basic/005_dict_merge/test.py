from buggy import merge_dicts

def test_merge_normal():
    assert merge_dicts({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}

def test_merge_overwrite():
    assert merge_dicts({"a": 1}, {"a": 99}) == {"a": 99}

def test_merge_empty_updates():
    assert merge_dicts({"a": 1}, {}) == {"a": 1}

def test_merge_no_side_effect():
    result1 = merge_dicts({"x": 10})
    result2 = merge_dicts({"a": 1})
    assert result1 == {"x": 10}
    assert result2 == {"a": 1}

def test_merge_none_updates():
    assert merge_dicts({"a": 1}) == {"a": 1}
