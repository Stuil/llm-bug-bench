# LLM Bug Benchmark v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first version of the LLM Bug Benchmark — 20 Python bug-fixing tasks with validation scripts

**Architecture:** Each task lives in its own directory under `tasks/{category}/XXX_name/` with 4 files (task.json, buggy.py, fixed.py, test.py). A validation script ensures every task meets invariants (buggy fails tests, fixed passes). A global index (`tasks/tasks.json`) provides a unified view.

**Tech Stack:** Python 3.10+, pytest, no external dependencies

---

### Task 1: Project scaffold and README

**Files:**
- Create: `README.md`
- Create: `tasks/tasks.json`
- Create: `tasks/basic/001_list_sort/task.json`
- Create: `tasks/basic/001_list_sort/buggy.py`
- Create: `tasks/basic/001_list_sort/fixed.py`
- Create: `tasks/basic/001_list_sort/test.py`

- [ ] **Step 1: Create README.md**

```markdown
# LLM Bug Benchmark

A Python bug-fixing benchmark for evaluating large language models' ability to repair code.

## Quick Start

```bash
pip install pytest
python scripts/validate_tasks.py
```

## Structure

```
tasks/
├── basic/           # 20-60 lines, simple logic bugs
├── intermediate/    # 60-150 lines, edge cases and subtle bugs
└── advanced/        # 150+ lines, complex scenarios
```

Each task contains:
- `buggy.py` — code with a bug
- `fixed.py` — correct reference implementation
- `test.py` — pytest tests (fail on buggy, pass on fixed)
- `task.json` — metadata

## Adding a Task

1. Create a new directory under the appropriate category
2. Add the 4 task files (buggy.py, fixed.py, test.py, task.json)
3. Run `python scripts/validate_tasks.py` to verify
```

- [ ] **Step 2: Create `tasks/tasks.json`**

```json
{
  "meta": {
    "name": "LLM Bug Benchmark",
    "version": "1.0.0",
    "language": "Python",
    "total_tasks": 0,
    "generated_at": ""
  },
  "tasks": []
}
```

- [ ] **Step 3: Create task 001 — list sort**

Create `tasks/basic/001_list_sort/task.json`:

```json
{
  "id": "001",
  "category": "basic",
  "title": "列表排序函数错误",
  "description": "sort_list 函数在输入包含重复元素时返回错误结果：当相邻元素相等时，函数会错误地交换它们，导致排序不稳定且结果不正确。",
  "difficulty": "easy",
  "bug_type": "逻辑错误",
  "knowledge_points": ["冒泡排序", "比较运算符"],
  "source": "synthetic"
}
```

Create `tasks/basic/001_list_sort/buggy.py`:

```python
def sort_list(items):
    n = len(items)
    for i in range(n):
        for j in range(0, n - i - 1):
            if items[j] >= items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
    return items
```

Create `tasks/basic/001_list_sort/fixed.py`:

```python
def sort_list(items):
    n = len(items)
    for i in range(n):
        for j in range(0, n - i - 1):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
    return items
```

Create `tasks/basic/001_list_sort/test.py`:

```python
from buggy import sort_list

def test_sort_ascending():
    assert sort_list([3, 1, 2]) == [1, 2, 3]

def test_sort_descending():
    assert sort_list([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

def test_sort_with_duplicates():
    assert sort_list([3, 1, 2, 1]) == [1, 1, 2, 3]

def test_sort_empty():
    assert sort_list([]) == []

def test_sort_single():
    assert sort_list([42]) == [42]

def test_sort_all_same():
    assert sort_list([7, 7, 7, 7]) == [7, 7, 7, 7]
```

- [ ] **Step 4: Commit**

```bash
git -C /home/zwh16/proj/llm-bug-bench init
git -C /home/zwh16/proj/llm-bug-bench add README.md tasks/tasks.json tasks/basic/001_list_sort/
git -C /home/zwh16/proj/llm-bug-bench commit -m "feat: project scaffold and task 001"
```

---

### Task 2: Tasks 002-008 (basic level)

**Files:**
- Create: `tasks/basic/002_json_parse/task.json`
- Create: `tasks/basic/002_json_parse/buggy.py`
- Create: `tasks/basic/002_json_parse/fixed.py`
- Create: `tasks/basic/002_json_parse/test.py`
- Create: ... (003 through 008)

- [ ] **Step 1: Task 002 — json_parse**

Bug: `parse_json` 函数在传入空字符串时没有处理，直接抛异常。应返回 None。

buggy.py:
```python
import json

def parse_json(text):
    return json.loads(text)
```

fixed.py:
```python
import json

def parse_json(text):
    if not text or not text.strip():
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None
```

test.py:
```python
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
```

- [ ] **Step 2: Task 003 — fibonacci**

Bug: `fibonacci` 函数对 n=0 返回错误结果（没有处理 n=0 的情况）。

buggy.py:
```python
def fibonacci(n):
    if n == 1:
        return 0
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

fixed.py:
```python
def fibonacci(n):
    if n == 0:
        return 0
    if n == 1:
        return 0
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

test.py:
```python
from buggy import fibonacci

def test_fib_0():
    assert fibonacci(0) == 0

def test_fib_1():
    assert fibonacci(1) == 0

def test_fib_2():
    assert fibonacci(2) == 1

def test_fib_10():
    assert fibonacci(10) == 55

def test_fib_20():
    assert fibonacci(20) == 6765
```

- [ ] **Step 3: Task 004 — max_value**

Bug: `find_max` 在处理全负数列表时返回了错误的初始值 0。

buggy.py:
```python
def find_max(numbers):
    if not numbers:
        return None
    max_val = 0
    for n in numbers:
        if n > max_val:
            max_val = n
    return max_val
```

fixed.py:
```python
def find_max(numbers):
    if not numbers:
        return None
    max_val = numbers[0]
    for n in numbers:
        if n > max_val:
            max_val = n
    return max_val
```

test.py:
```python
from buggy import find_max

def test_max_positive():
    assert find_max([1, 5, 3, 9, 2]) == 9

def test_max_negative():
    assert find_max([-5, -2, -8, -1]) == -1

def test_max_single():
    assert find_max([42]) == 42

def test_max_empty():
    assert find_max([]) is None

def test_max_mixed():
    assert find_max([-10, 0, 10]) == 10
```

- [ ] **Step 4: Task 005 — dict_merge**

Bug: `merge_dicts` 使用了可变默认参数，多次调用会导致状态累积。

buggy.py:
```python
def merge_dicts(base, updates={}):
    for k, v in updates.items():
        base[k] = v
    return base
```

fixed.py:
```python
def merge_dicts(base, updates=None):
    if updates is None:
        updates = {}
    result = base.copy()
    for k, v in updates.items():
        result[k] = v
    return result
```

test.py:
```python
from buggy import merge_dicts

def test_merge_normal():
    assert merge_dicts({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}

def test_merge_overwrite():
    assert merge_dicts({"a": 1}, {"a": 99}) == {"a": 99}

def test_merge_empty():
    assert merge_dicts({"a": 1}, {}) == {"a": 1}

def test_merge_no_side_effect():
    base = {"x": 10}
    merge_dicts(base, {"y": 20})
    # Second call should not retain state from first
    result2 = merge_dicts({"a": 1}, {"b": 2})
    assert result2 == {"a": 1, "b": 2}

def test_merge_none_updates():
    assert merge_dicts({"a": 1}) == {"a": 1}
```

- [ ] **Step 5: Task 006 — file_reader**

Bug: `read_lines` 打开文件后没有关闭，且未处理文件不存在的异常。

buggy.py:
```python
def read_lines(filename):
    f = open(filename, "r")
    return [line.strip() for line in f.readlines()]
```

fixed.py:
```python
def read_lines(filename):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []
```

test.py:
```python
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
```

- [ ] **Step 6: Task 007 — palindrome**

Bug: `is_palindrome` 对空字符串和单字符返回错误结果。同时大小写处理有误。

buggy.py:
```python
def is_palindrome(s):
    chars = []
    for c in s:
        if c.isalpha():
            chars.append(c.lower())
    n = len(chars)
    for i in range(n // 2):
        if chars[i] != chars[n - i]:
            return False
    return True if n > 0 else False
```

fixed.py:
```python
def is_palindrome(s):
    chars = []
    for c in s:
        if c.isalpha():
            chars.append(c.lower())
    n = len(chars)
    if n == 0:
        return True
    for i in range(n // 2):
        if chars[i] != chars[n - 1 - i]:
            return False
    return True
```

test.py:
```python
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
```

- [ ] **Step 7: Task 008 — url_parser**

Bug: `parse_query_string` 使用 split 解析参数时，没有处理值中包含 `=` 的情况。

buggy.py:
```python
def parse_query_string(query):
    params = {}
    for pair in query.split("&"):
        if not pair:
            continue
        key, value = pair.split("=")
        params[key] = value
    return params
```

fixed.py:
```python
from urllib.parse import unquote_plus

def parse_query_string(query):
    params = {}
    for pair in query.split("&"):
        if not pair:
            continue
        if "=" in pair:
            key, value = pair.split("=", 1)
            params[key] = unquote_plus(value)
        else:
            params[pair] = ""
    return params
```

test.py:
```python
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
```

- [ ] **Step 8: Commit**

```bash
git -C /home/zwh16/proj/llm-bug-bench add tasks/basic/002_json_parse/ tasks/basic/003_fibonacci/ tasks/basic/004_max_value/ tasks/basic/005_dict_merge/ tasks/basic/006_file_reader/ tasks/basic/007_palindrome/ tasks/basic/008_url_parser/
git -C /home/zwh16/proj/llm-bug-bench commit -m "feat: add tasks 002-008 (basic level)"
```

---

### Task 3: Tasks 009-016 (intermediate level)

**Files:**
- Create: `tasks/intermediate/009_csv_parser/task.json`
- Create: `tasks/intermediate/009_csv_parser/buggy.py`
- Create: `tasks/intermediate/009_csv_parser/fixed.py`
- Create: `tasks/intermediate/009_csv_parser/test.py`
- Create: ... (010 through 016)

- [ ] **Step 1: Task 009 — csv_parser**

Bug: `parse_csv` 没有处理引号中包含逗号的情况。

buggy.py:
```python
def parse_csv(line):
    return line.split(",")
```

fixed.py:
```python
import csv
import io

def parse_csv(line):
    reader = csv.reader(io.StringIO(line))
    return next(reader)
```

test.py:
```python
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
```

- [ ] **Step 2: Task 010 — thread_safe_counter**

Bug: `Counter.increment` 在没有锁的情况下多线程调用会丢失计数。

buggy.py:
```python
import threading

class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def get(self):
        return self.count
```

fixed.py:
```python
import threading

class Counter:
    def __init__(self):
        self.count = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self.count += 1

    def get(self):
        with self._lock:
            return self.count
```

test.py:
```python
import threading
from buggy import Counter

def test_single_thread():
    c = Counter()
    c.increment()
    c.increment()
    assert c.get() == 2

def test_multi_thread():
    c = Counter()
    n = 1000
    threads = []
    for _ in range(10):
        t = threading.Thread(target=lambda: [c.increment() for _ in range(n)])
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    assert c.get() == n * 10, f"Expected {n * 10}, got {c.get()}"
```

- [ ] **Step 3: Task 011 — regex_email**

Bug: `validate_email` 的正则太宽松，允许无效格式。

buggy.py:
```python
import re

def validate_email(email):
    return bool(re.match(r"^(.+)@(.+)$", email))
```

fixed.py:
```python
import re

def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))
```

test.py:
```python
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
```

- [ ] **Step 4: Task 012 — binary_search**

Bug: `binary_search` 存在 off-by-one 错误，可能在包含目标元素时返回 -1。

buggy.py:
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

fixed.py:
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

test.py:
```python
from buggy import binary_search

def test_found_first():
    assert binary_search([1, 3, 5, 7, 9], 1) == 0

def test_found_last():
    assert binary_search([1, 3, 5, 7, 9], 9) == 4

def test_found_middle():
    assert binary_search([1, 3, 5, 7, 9], 5) == 2

def test_not_found():
    assert binary_search([1, 3, 5, 7, 9], 4) == -1

def test_single_element_found():
    assert binary_search([42], 42) == 0

def test_single_element_not_found():
    assert binary_search([42], 1) == -1

def test_empty():
    assert binary_search([], 1) == -1
```

- [ ] **Step 5: Task 013 — lru_cache**

Bug: `LRUCache.get` 在多 key 场景下错误移除了最近使用的元素。

buggy.py:
```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.order = []

    def get(self, key):
        if key not in self.cache:
            return -1
        self.order.remove(key)
        self.order.append(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        self.cache[key] = value
        self.order.append(key)
```

fixed.py:
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value
```

test.py:
```python
from buggy import LRUCache

def test_basic():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1

def test_eviction():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)
    assert cache.get(1) == -1

def test_update_renews():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.get(1)
    cache.put(3, 3)
    assert cache.get(1) == 1
    assert cache.get(2) == -1

def test_overwrite():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(1, 99)
    assert cache.get(1) == 99

def test_capacity_one():
    cache = LRUCache(1)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == -1
    assert cache.get(2) == 2
```

- [ ] **Step 6: Task 014 — rate_limiter**

Bug: `RateLimiter.allow_request` 存在竞态条件，高并发下允许超过限制的请求。

buggy.py:
```python
import time

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.timestamps = []

    def allow_request(self):
        now = time.time()
        self.timestamps = [t for t in self.timestamps if now - t < self.window_seconds]
        if len(self.timestamps) < self.max_requests:
            self.timestamps.append(now)
            return True
        return False
```

fixed.py:
```python
import time
import threading

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.timestamps = []
        self._lock = threading.Lock()

    def allow_request(self):
        with self._lock:
            now = time.time()
            self.timestamps = [t for t in self.timestamps if now - t < self.window_seconds]
            if len(self.timestamps) < self.max_requests:
                self.timestamps.append(now)
                return True
            return False
```

test.py:
```python
import threading
from buggy import RateLimiter

def test_within_limit():
    limiter = RateLimiter(3, 10)
    assert limiter.allow_request() is True
    assert limiter.allow_request() is True
    assert limiter.allow_request() is True

def test_exceed_limit():
    limiter = RateLimiter(2, 10)
    limiter.allow_request()
    limiter.allow_request()
    assert limiter.allow_request() is False

def test_concurrent():
    limiter = RateLimiter(5, 10)
    results = []
    lock = threading.Lock()
    def req():
        allowed = limiter.allow_request()
        with lock:
            results.append(allowed)
    threads = [threading.Thread(target=req) for _ in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    allowed_count = sum(1 for r in results if r)
    assert allowed_count <= 5, f"Allowed {allowed_count}, max is 5"
```

- [ ] **Step 7: Task 015 — date_parser**

Bug: `parse_date` 没有处理不同分隔符的日期格式，且未处理无效日期。

buggy.py:
```python
def parse_date(date_str):
    parts = date_str.split("-")
    if len(parts) != 3:
        return None
    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
    return {"year": year, "month": month, "day": day}
```

fixed.py:
```python
from datetime import datetime

def parse_date(date_str):
    for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"]:
        try:
            dt = datetime.strptime(date_str, fmt)
            return {"year": dt.year, "month": dt.month, "day": dt.day}
        except ValueError:
            continue
    return None
```

test.py:
```python
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
```

- [ ] **Step 8: Task 016 — html_escape**

Bug: `escape_html` 的替换顺序导致 `&` 被双重转义。

buggy.py:
```python
def escape_html(text):
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace("&", "&amp;")
    text = text.replace('"', "&quot;")
    return text
```

fixed.py:
```python
import html

def escape_html(text):
    return html.escape(text, quote=True)
```

test.py:
```python
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
```

- [ ] **Step 9: Commit**

```bash
git -C /home/zwh16/proj/llm-bug-bench add tasks/intermediate/009_csv_parser/ tasks/intermediate/010_thread_safe_counter/ tasks/intermediate/011_regex_email/ tasks/intermediate/012_binary_search/ tasks/intermediate/013_lru_cache/ tasks/intermediate/014_rate_limiter/ tasks/intermediate/015_date_parser/ tasks/intermediate/016_html_escape/
git -C /home/zwh16/proj/llm-bug-bench add tasks/intermediate/
git -C /home/zwh16/proj/llm-bug-bench commit -m "feat: add tasks 009-016 (intermediate level)"
```

---

### Task 4: Tasks 017-019 (advanced level)

**Files:**
- Create: `tasks/advanced/017_tcp_server/task.json`, buggy.py, fixed.py, test.py
- Create: `tasks/advanced/018_producer_consumer/task.json`, buggy.py, fixed.py, test.py
- Create: `tasks/advanced/019_tree_traversal/task.json`, buggy.py, fixed.py, test.py
- Create: `tasks/advanced/020_rate_calculator/task.json`, buggy.py, fixed.py, test.py

- [ ] **Step 1: Task 017 — tcp_server**

Bug: TCP echo server 的 `handle_client` 在处理完一个请求后就关闭连接，没有持续监听。

buggy.py:
```python
import socket

def handle_client(conn):
    data = conn.recv(1024)
    if data:
        conn.sendall(data)
    conn.close()

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    while True:
        conn, addr = server.accept()
        handle_client(conn)
```

fixed.py:
```python
import socket

def handle_client(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)
    conn.close()

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    while True:
        conn, addr = server.accept()
        handle_client(conn)
```

test.py:
```python
import socket
import threading
import time
from buggy import start_server

def test_echo():
    HOST, PORT = "127.0.0.1", 19876
    t = threading.Thread(target=start_server, args=(HOST, PORT), daemon=True)
    t.start()
    time.sleep(0.1)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.sendall(b"hello")
    data = client.recv(1024)
    assert data == b"hello"
    client.sendall(b"world")
    # Second echo should work if handle_client loops
    data = client.recv(1024)
    assert data == b"world"
    client.close()
```

- [ ] **Step 2: Task 018 — producer_consumer**

Bug: 生产者-消费者模式中，消费者在没有锁的情况下检查队列状态，可能在队列为空时调用 get() 导致阻塞。

buggy.py:
```python
import threading
import queue

class Pipeline:
    def __init__(self, maxsize=10):
        self.queue = queue.Queue(maxsize=maxsize)
        self._stop = False

    def produce(self, item):
        self.queue.put(item)

    def consume(self):
        if not self.queue.empty():
            return self.queue.get()
        return None

    def stop(self):
        self._stop = True
```

fixed.py:
```python
import threading
import queue

class Pipeline:
    def __init__(self, maxsize=10):
        self.queue = queue.Queue(maxsize=maxsize)

    def produce(self, item):
        self.queue.put(item)

    def consume(self, timeout=0.1):
        try:
            return self.queue.get(timeout=timeout)
        except queue.Empty:
            return None
```

test.py:
```python
import threading
import time
from buggy import Pipeline

def test_single_item():
    p = Pipeline()
    p.produce(42)
    assert p.consume() == 42

def test_multiple_items():
    p = Pipeline()
    for i in range(5):
        p.produce(i)
    for i in range(5):
        assert p.consume() == i

def test_consume_from_empty():
    p = Pipeline()
    result = p.consume()
    assert result is None

def test_concurrent():
    p = Pipeline(maxsize=5)
    results = []
    def producer():
        for i in range(20):
            p.produce(i)
            time.sleep(0.01)
    def consumer():
        for _ in range(20):
            item = p.consume()
            if item is not None:
                results.append(item)
    pt = threading.Thread(target=producer, daemon=True)
    ct = threading.Thread(target=consumer, daemon=True)
    pt.start()
    ct.start()
    pt.join()
    ct.join()
    assert len(results) == 20
    assert sorted(results) == list(range(20))
```

- [ ] **Step 3: Task 019 — tree_traversal**

Bug: 二叉树的中序遍历使用了错误的递归逻辑——将 node 和 val 混淆。

buggy.py:
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_traversal(root):
    result = []
    if root:
        inorder_traversal(root.left)
        result.append(root.val)
        inorder_traversal(root.right)
    return result
```

fixed.py:
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_traversal(root):
    result = []
    def dfs(node):
        if node is None:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)
    dfs(root)
    return result
```

test.py:
```python
from buggy import TreeNode, inorder_traversal

def test_empty():
    assert inorder_traversal(None) == []

def test_single():
    root = TreeNode(5)
    assert inorder_traversal(root) == [5]

def test_left_heavy():
    root = TreeNode(3, TreeNode(2, TreeNode(1)))
    assert inorder_traversal(root) == [1, 2, 3]

def test_full_tree():
    root = TreeNode(4,
        TreeNode(2, TreeNode(1), TreeNode(3)),
        TreeNode(6, TreeNode(5), TreeNode(7))
    )
    assert inorder_traversal(root) == [1, 2, 3, 4, 5, 6, 7]
```

- [ ] **Step 4: Task 020 — rate_calculator**

Bug: `calculate_discount` 在处理层级折扣时，总金额的舍入方式导致最终结果与逐项舍入不一致。

buggy.py:
```python
def calculate_discount(items, discount_rate):
    total = 0
    for price, quantity in items:
        total += price * quantity
    return round(total * (1 - discount_rate), 2)
```

fixed.py:
```python
from decimal import Decimal, ROUND_HALF_UP

def calculate_discount(items, discount_rate):
    total = Decimal("0.00")
    for price, quantity in items:
        item_total = Decimal(str(price)) * Decimal(str(quantity))
        item_total = item_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total += item_total
    discount = total * Decimal(str(discount_rate))
    discount = discount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(total - discount)
```

test.py:
```python
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
```

- [ ] **Step 5: Commit**

```bash
git -C /home/zwh16/proj/llm-bug-bench add tasks/advanced/
git -C /home/zwh16/proj/llm-bug-bench commit -m "feat: add tasks 017-020 (advanced level)"
```

---

### Task 5: Validation script

**Files:**
- Create: `scripts/validate_tasks.py`

- [ ] **Step 1: Write `scripts/validate_tasks.py`**

```python
#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
import importlib.util

TASKS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tasks")

def load_task_metadata(task_dir):
    meta_path = os.path.join(task_dir, "task.json")
    with open(meta_path) as f:
        return json.load(f)

def validate_task(task_dir):
    task_id = os.path.basename(task_dir)
    meta = load_task_metadata(task_dir)
    required_files = ["buggy.py", "fixed.py", "test.py", "task.json"]
    errors = []

    for f in required_files:
        if not os.path.exists(os.path.join(task_dir, f)):
            errors.append(f"Missing {f}")

    if errors:
        return errors

    buggy_path = os.path.join(task_dir, "buggy.py")
    fixed_path = os.path.join(task_dir, "fixed.py")
    test_path = os.path.join(task_dir, "test.py")

    with open(buggy_path) as f:
        buggy_code = f.read()
    with open(fixed_path) as f:
        fixed_code = f.read()

    if buggy_code == fixed_code:
        errors.append("buggy.py and fixed.py are identical")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_test = os.path.join(tmpdir, "test.py")

        # Test buggy code — should fail
        buggy_tmp = os.path.join(tmpdir, "buggy.py")
        with open(buggy_tmp, "w") as f:
            f.write(buggy_code)
        with open(tmp_test, "w") as f:
            f.write(open(test_path).read())
        result = subprocess.run(
            [sys.executable, "-m", "pytest", tmp_test, "-v", "--tb=short"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            errors.append(f"buggy.py passed all tests (should fail at least 1)")

        # Test fixed code — should pass
        fixed_tmp = os.path.join(tmpdir, "buggy.py")
        with open(fixed_tmp, "w") as f:
            f.write(fixed_code)
        result = subprocess.run(
            [sys.executable, "-m", "pytest", tmp_test, "-v", "--tb=short"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            errors.append(f"fixed.py failed tests ({result.returncode})")

    return errors

def update_global_index():
    tasks = []
    for category in ["basic", "intermediate", "advanced"]:
        cat_path = os.path.join(TASKS_DIR, category)
        if not os.path.isdir(cat_path):
            continue
        for entry in sorted(os.listdir(cat_path)):
            entry_path = os.path.join(cat_path, entry)
            if os.path.isdir(entry_path) and os.path.exists(os.path.join(entry_path, "task.json")):
                meta = load_task_metadata(entry_path)
                tasks.append(meta)

    index_path = os.path.join(TASKS_DIR, "tasks.json")
    with open(index_path) as f:
        index = json.load(f)
    index["meta"]["total_tasks"] = len(tasks)
    index["meta"]["generated_at"] = __import__("datetime").datetime.now().isoformat()
    index["tasks"] = sorted(tasks, key=lambda t: t["id"])
    with open(index_path, "w") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    print(f"Updated index: {len(tasks)} tasks")

def main():
    if not os.path.isdir(TASKS_DIR):
        print(f"Tasks directory not found: {TASKS_DIR}")
        sys.exit(1)

    all_errors = {}
    for category in ["basic", "intermediate", "advanced"]:
        cat_path = os.path.join(TASKS_DIR, category)
        if not os.path.isdir(cat_path):
            continue
        for entry in sorted(os.listdir(cat_path)):
            entry_path = os.path.join(cat_path, entry)
            if os.path.isdir(entry_path):
                errors = validate_task(entry_path)
                if errors:
                    all_errors[entry] = errors
                else:
                    print(f"  PASS: {entry}")

    if all_errors:
        print("\nFAILURES:")
        for task_id, errors in all_errors.items():
            print(f"  {task_id}:")
            for e in errors:
                print(f"    - {e}")
        sys.exit(1)
    else:
        print("\nAll tasks passed validation!")

    update_global_index()

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run validation**

```bash
cd /home/zwh16/proj/llm-bug-bench && python scripts/validate_tasks.py
```
Expected: `All tasks passed validation!`

- [ ] **Step 3: Fix any validation failures**

If any task fails (buggy passes tests, or fixed fails), fix the corresponding test.py or code file and re-run.

- [ ] **Step 4: Commit**

```bash
git -C /home/zwh16/proj/llm-bug-bench add scripts/ scripts/validate_tasks.py
git -C /home/zwh16/proj/llm-bug-bench commit -m "feat: add task validation script"
```

---

### Task 6: Finalize and verify

- [ ] **Step 1: Run full validation**

```bash
cd /home/zwh16/proj/llm-bug-bench && python scripts/validate_tasks.py
```

- [ ] **Step 2: Check directory structure**

```bash
cd /home/zwh16/proj/llm-bug-bench && find . -type f -not -path './.git/*' | sort
```

- [ ] **Step 3: Final commit with any fixes**

```bash
git -C /home/zwh16/proj/llm-bug-bench add -A
git -C /home/zwh16/proj/llm-bug-bench commit -m "chore: finalize v1 with 20 tasks"
```
