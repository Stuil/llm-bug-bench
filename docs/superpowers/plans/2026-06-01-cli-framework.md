# CLI Evaluation Framework (v2) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) for tracking.

**Goal:** Build the `bench` CLI tool that evaluates LLMs on the bug-fixing benchmark.

**Architecture:** A pure-Python CLI with no runtime dependencies beyond stdlib + pytest. Subcommands: `run` (evaluate tasks against an LLM) and `list` (show available tasks). The core flow is: read task → assemble prompt → call OpenAI-compatible API → extract code → run pytest → report results.

**Tech Stack:** Python 3.8+ stdlib (argparse, json, subprocess, tempfile, urllib), pytest

---

### Task 1: `cli/__init__.py` and `cli/__main__.py`

**Files:**
- Create: `cli/__init__.py`
- Create: `cli/__main__.py`

- [ ] **Step 1: Create `cli/__init__.py`** — empty file

- [ ] **Step 2: Create `cli/__main__.py`** — delegates to `main.py`

```python
from cli.main import main

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Commit**

```bash
git add cli/__init__.py cli/__main__.py
git commit -m "chore: scaffold cli package"
```

---

### Task 2: Entry point with argument parsing

**Files:**
- Create: `cli/main.py`

- [ ] **Step 1: Create `cli/main.py`**

```python
import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bench",
        description="LLM Bug Benchmark CLI — Evaluate LLMs on bug-fixing tasks",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="Run evaluation on selected tasks")
    run_parser.add_argument("--model", default="gpt-4o", help="Model name (default: gpt-4o)")
    run_parser.add_argument("--tasks", help="Comma-separated task IDs (e.g. 001,002)")
    run_parser.add_argument("--all", action="store_true", help="Run all tasks")
    run_parser.add_argument("--base-url", help="API base URL (overrides LLM_BASE_URL env)")
    run_parser.add_argument("--api-key", help="API key (overrides LLM_API_KEY env)")

    list_parser = sub.add_parser("list", help="List available tasks")
    list_parser.add_argument("--category", choices=["basic", "intermediate", "advanced"],
                             help="Filter by category")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        from cli.runner import run_evaluation
        run_evaluation(args)
    elif args.command == "list":
        from cli.lister import list_tasks
        list_tasks(args)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Commit**

```bash
git add cli/main.py
git commit -m "feat: add CLI argument parser with run/list subcommands"
```

---

### Task 3: Task loader utility

**Files:**
- Create: `cli/tasks.py`

- [ ] **Step 1: Create `cli/tasks.py`**

```python
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASKS_DIR = os.path.join(BASE_DIR, "tasks")
INDEX_PATH = os.path.join(TASKS_DIR, "tasks.json")


def load_index() -> dict:
    with open(INDEX_PATH) as f:
        return json.load(f)


def get_task_path(task_id: str) -> str:
    index = load_index()
    for t in index["tasks"]:
        if t["id"] == task_id:
            return os.path.join(TASKS_DIR, t["category"], f"{task_id}_{t['title'].split('（')[0].split(' ')[0]}")
    raise ValueError(f"Task {task_id} not found")


def get_task_dir(task_id: str) -> str:
    """Find task directory by walking tasks directory."""
    for root, dirs, files in os.walk(TASKS_DIR):
        if os.path.basename(root).startswith(task_id):
            return root
    raise ValueError(f"Task directory for {task_id} not found")


def load_task(task_id: str) -> dict:
    task_dir = get_task_dir(task_id)
    with open(os.path.join(task_dir, "buggy.py")) as f:
        buggy_code = f.read()
    with open(os.path.join(task_dir, "test.py")) as f:
        test_code = f.read()
    with open(os.path.join(task_dir, "task.json")) as f:
        metadata = json.load(f)
    return {
        "id": task_id,
        "buggy_code": buggy_code,
        "test_code": test_code,
        "metadata": metadata,
        "dir": task_dir,
    }


def get_all_task_ids() -> list[str]:
    index = load_index()
    return [t["id"] for t in index["tasks"]]


def filter_tasks(task_ids: list[str] | None = None, category: str | None = None) -> list[dict]:
    """Load tasks, optionally filtered by IDs or category."""
    index = load_index()
    tasks = index["tasks"]
    if category:
        tasks = [t for t in tasks if t["category"] == category]
    if task_ids:
        tasks = [t for t in tasks if t["id"] in task_ids]
    return tasks
```

- [ ] **Step 2: Commit**

```bash
git add cli/tasks.py
git commit -m "feat: add task loader utility"
```

---

### Task 4: Prompt assembly module

**Files:**
- Create: `cli/prompt.py`

- [ ] **Step 1: Create `cli/prompt.py`**

```python
SYSTEM_PROMPT = (
    "You are a Python bug-fixing expert. "
    "Given a piece of buggy Python code and a description of the bug, "
    "return the complete fixed code. "
    "Output ONLY the fixed Python code inside a ```python code block. "
    "Do not include any explanations or commentary."
)


def build_user_prompt(buggy_code: str, description: str) -> str:
    return f"""The following Python code contains a bug:

```python
{buggy_code}
```

Bug description: {description}

Please fix the bug and return the complete corrected code."""


def build_messages(buggy_code: str, description: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_prompt(buggy_code, description)},
    ]
```

- [ ] **Step 2: Commit**

```bash
git add cli/prompt.py
git commit -m "feat: add prompt assembly module"
```

---

### Task 5: Code extractor (parse LLM response)

**Files:**
- Create: `cli/extractor.py`

- [ ] **Step 1: Create `cli/extractor.py`**

```python
import re


def extract_code(response_text: str) -> str | None:
    """Extract Python code from LLM response.
    
    Looks for ```python ... ``` blocks first, then falls back to ``` ... ```,
    then tries to extract any Python-looking code.
    """
    pattern = re.compile(
        r"```(?:python)?\s*\n(.*?)```",
        re.DOTALL,
    )
    matches = pattern.findall(response_text)
    if matches:
        return matches[0].strip()
    
    stripped = response_text.strip()
    if stripped:
        return stripped
    
    return None


def validate_code(code: str) -> bool:
    """Quick syntax check on extracted code."""
    try:
        compile(code, "<extracted>", "exec")
        return True
    except SyntaxError:
        return False
```

- [ ] **Step 2: Commit**

```bash
git add cli/extractor.py
git commit -m "feat: add code extractor for LLM responses"
```

---

### Task 6: OpenAI-compatible LLM client

**Files:**
- Create: `cli/llm.py`

- [ ] **Step 1: Create `cli/llm.py`**

```python
import json
import os
import urllib.request
import urllib.error


def get_api_config(args) -> tuple[str, str, str]:
    api_key = args.api_key or os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
    base_url = args.base_url or os.environ.get("LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = args.model
    return api_key, base_url.rstrip("/"), model


def call_llm(messages: list[dict], api_key: str, base_url: str, model: str) -> str:
    url = f"{base_url}/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.0,
    }).encode()

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode())
        return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        detail = e.read().decode()
        raise RuntimeError(f"API error {e.code}: {detail}") from e
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Unexpected API response format: {e}") from e
```

- [ ] **Step 2: Commit**

```bash
git add cli/llm.py
git commit -m "feat: add OpenAI-compatible API client"
```

---

### Task 7: Evaluator — run pytest on extracted code

**Files:**
- Create: `cli/evaluator.py`

- [ ] **Step 1: Create `cli/evaluator.py`**

```python
import os
import subprocess
import sys
import tempfile


EvalResult = dict
# {
#   "task_id": str,
#   "passed": bool,
#   "passed_count": int,
#   "total_count": int,
#   "output": str,
#   "error": str | None,
# }


def evaluate_task(task_id: str, buggy_code: str, test_code: str, fixed_code: str) -> EvalResult:
    with tempfile.TemporaryDirectory() as tmpdir:
        buggy_path = os.path.join(tmpdir, "buggy.py")
        test_path = os.path.join(tmpdir, "test.py")

        with open(buggy_path, "w") as f:
            f.write(fixed_code)
        with open(test_path, "w") as f:
            f.write(test_code)

        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_path, "-v", "--tb=short"],
                capture_output=True, text=True, timeout=60,
            )
        except subprocess.TimeoutExpired:
            return {
                "task_id": task_id,
                "passed": False,
                "passed_count": 0,
                "total_count": 0,
                "output": "",
                "error": "TIMEOUT",
            }

        output = result.stdout + "\n" + result.stderr

        passed_count = output.count(" PASSED")
        failed_count = output.count(" FAILED")
        error_count = output.count(" ERROR")
        total_count = passed_count + failed_count + error_count

        return {
            "task_id": task_id,
            "passed": result.returncode == 0,
            "passed_count": passed_count,
            "total_count": total_count,
            "output": output.strip(),
            "error": None if result.returncode == 0 else "TESTS_FAILED",
        }
```

- [ ] **Step 2: Commit**

```bash
git add cli/evaluator.py
git commit -m "feat: add pytest evaluator for extracted code"
```

---

### Task 8: Reporter — format and display results

**Files:**
- Create: `cli/reporter.py`

- [ ] **Step 1: Create `cli/reporter.py`**

```python
def print_results(results: list[dict], model: str):
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed

    print()
    for r in results:
        if r["passed"]:
            status = f"PASS ({r['passed_count']}/{r['total_count']})"
        elif r["error"] == "TIMEOUT":
            status = "TIMEOUT"
        elif r["error"] == "EXTRACT_FAILED":
            status = "EXTRACT_FAIL"
        elif r["error"] == "API_ERROR":
            status = "API_ERROR"
        else:
            status = f"FAIL ({r['passed_count']}/{r['total_count']})"
        print(f"  {r['task_id']:>4}  {status}")

    print()
    width = 44
    print("╔" + "═" * width + "╗")
    ratio = passed / total * 100 if total > 0 else 0
    label = f" Results: {passed}/{total} passed ({ratio:.1f}%) "
    print(f"║{label:^{width}}║")
    print("╚" + "═" * width + "╝")
    print()


def print_json_results(results: list[dict], model: str):
    import json
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    report = {
        "model": model,
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "results": results,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
```

- [ ] **Step 2: Commit**

```bash
git add cli/reporter.py
git commit -m "feat: add result reporter with table and JSON output"
```

---

### Task 9: Runner — orchestrate the full evaluation

**Files:**
- Create: `cli/runner.py`

- [ ] **Step 1: Create `cli/runner.py`**

```python
import sys

from cli.llm import call_llm, get_api_config
from cli.prompt import build_messages
from cli.extractor import extract_code, validate_code
from cli.evaluator import evaluate_task
from cli.reporter import print_results, print_json_results
from cli.tasks import load_task


def run_evaluation(args):
    task_ids = []
    if args.all:
        from cli.tasks import get_all_task_ids
        task_ids = get_all_task_ids()
    elif args.tasks:
        task_ids = [t.strip() for t in args.tasks.split(",")]
    else:
        print("Error: specify --tasks or --all", file=sys.stderr)
        sys.exit(1)

    api_key, base_url, model = get_api_config(args)

    if not api_key:
        print("Error: LLM_API_KEY or OPENAI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    print(f"\nEvaluating {len(task_ids)} tasks with model={model}")
    if base_url:
        print(f"Base URL: {base_url}")
    print()

    results = []
    for i, task_id in enumerate(task_ids, 1):
        print(f"  [{i}/{len(task_ids)}] Task {task_id}...", end=" ", flush=True)

        try:
            task = load_task(task_id)
            messages = build_messages(task["buggy_code"], task["metadata"]["description"])
            response = call_llm(messages, api_key, base_url, model)
        except Exception as e:
            print(f"API_ERROR: {e}")
            results.append({
                "task_id": task_id,
                "passed": False,
                "passed_count": 0,
                "total_count": 0,
                "output": "",
                "error": "API_ERROR",
            })
            continue

        fixed_code = extract_code(response)
        if fixed_code is None:
            print("EXTRACT_FAIL")
            results.append({
                "task_id": task_id,
                "passed": False,
                "passed_count": 0,
                "total_count": 0,
                "output": response[:200],
                "error": "EXTRACT_FAIL",
            })
            continue

        if not validate_code(fixed_code):
            print("SYNTAX_ERROR")
            results.append({
                "task_id": task_id,
                "passed": False,
                "passed_count": 0,
                "total_count": 0,
                "output": fixed_code[:200],
                "error": "SYNTAX_ERROR",
            })
            continue

        result = evaluate_task(task_id, task["buggy_code"], task["test_code"], fixed_code)
        if result["passed"]:
            print("PASS")
        else:
            print(f"FAIL ({result['passed_count']}/{result['total_count']})")
        results.append(result)

    print_results(results, model)
```

- [ ] **Step 2: Commit**

```bash
git add cli/runner.py
git commit -m "feat: add evaluation runner orchestrator"
```

---

### Task 10: Lister — show available tasks

**Files:**
- Create: `cli/lister.py`

- [ ] **Step 1: Create `cli/lister.py`**

```python
from cli.tasks import filter_tasks


def list_tasks(args):
    tasks = filter_tasks(category=args.category)
    if not tasks:
        print("No tasks found.")
        return
    print(f"\n{'ID':>4}  {'Category':<14} {'Difficulty':<10} Title")
    print("-" * 60)
    for t in tasks:
        print(f"{t['id']:>4}  {t['category']:<14} {t['difficulty']:<10} {t['title']}")

    cat = f" ({args.category})" if args.category else ""
    print(f"\nTotal: {len(tasks)} task{cat}\n")
```

- [ ] **Step 2: Commit**

```bash
git add cli/lister.py
git commit -m "feat: add task listing command"
```

---

### Task 11: `bench` entry point script + README update

**Files:**
- Create: `scripts/bench` (shell wrapper)
- Modify: `README.md`

- [ ] **Step 1: Create `scripts/bench` wrapper**

```bash
#!/usr/bin/env bash
# Wrapper script for the bench CLI
exec python3 -m cli "$@"
```

```bash
chmod +x scripts/bench
```

- [ ] **Step 2: Add `--json` flag to `cli/main.py`**

Update the run subparser to accept `--json` for JSON output.

```python
    run_parser.add_argument("--json", action="store_true", help="Output results as JSON")
```

Update `cli/runner.py` to check `args.json` and call `print_json_results` instead.

Change the last line: replace `print_results(results, model)` with:

```python
    if getattr(args, "json", False):
        print_json_results(results, model)
    else:
        print_results(results, model)
```

- [ ] **Step 3: Update `README.md`**

Append v2 CLI usage section:

```
## CLI Evaluation (v2)

```bash
# List available tasks
./scripts/bench list

# List tasks by category
./scripts/bench list --category basic

# Run evaluation on specific tasks
export LLM_API_KEY="your-api-key"
./scripts/bench run --model gpt-4o --tasks 001,002,003

# Run on all tasks
./scripts/bench run --model deepseek-chat --all

# JSON output
./scripts/bench run --model gpt-4o --tasks 001 --json
```

Environment variables:
- `LLM_API_KEY` or `OPENAI_API_KEY` — API key
- `LLM_BASE_URL` or `OPENAI_BASE_URL` — API endpoint (default: `https://api.openai.com/v1`)
```

- [ ] **Step 4: Clean up `__pycache__` if any**

```bash
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
```

- [ ] **Step 5: Run validation to confirm nothing broke**

```bash
python3 scripts/validate_tasks.py
```

Expected: All 20 tasks pass.

- [ ] **Step 6: Test basic CLI works**

```bash
python3 -m cli list
```

Expected: Shows all 20 tasks in a table.

```bash
python3 -m cli list --category basic
```

Expected: Shows only basic tasks.

- [ ] **Step 7: Commit**

```bash
git add cli/ scripts/bench README.md
git commit -m "feat: add bench CLI entry point and update docs"
```
