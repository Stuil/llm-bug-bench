import os
import tempfile
from buggy import read_lines

def test_read_existing_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("a\nb\nc\n")
        f.flush()
        result = read_lines(f.name)
        assert result == ["a", "b", "c"]
        os.unlink(f.name)

def test_read_missing_file():
    assert read_lines("/tmp/nonexistent_file_xyz.txt") == []

def test_read_empty_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.flush()
        result = read_lines(f.name)
        assert result == []
        os.unlink(f.name)
