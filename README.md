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
