# LLM Bug Benchmark — Agent Guide

## Commands

```bash
pip install pytest          # only dependency
python3 scripts/validate_tasks.py   # validate ALL tasks (run after any change)
```

## Repo structure

```
tasks/
├── basic/          # 8 tasks (001-008)
├── intermediate/   # 8 tasks (009-016)
└── advanced/       # 4 tasks (017-020)
```

Each task dir has exactly 4 files: `buggy.py` (broken), `fixed.py` (correct), `test.py` (pytest tests), `task.json` (Chinese metadata).

## Validation rules (enforced by `scripts/validate_tasks.py`)

- `buggy.py` + `test.py` → must **fail** ≥1 test
- `fixed.py` + `test.py` → must **pass** all tests
- `buggy.py` and `fixed.py` must differ
- Tests always `from buggy import ...` (never from `fixed`)
- Fixed code may use different imports/approaches than buggy (e.g., `collections.OrderedDict` vs manual list, `csv` vs split, `Decimal` vs float)

## Dev notes

- Use `python3` (not `python`)
- `tasks/tasks.json` index is **auto-generated** by validation script
- Task metadata is in Chinese, `source` field is always `"synthetic"`
- `__pycache__/` and `*.pyc` are gitignored
- `docs/superpowers/` contains design spec and implementation plan — read before planning new tasks
- To add a task: create dir under appropriate category, add 4 files, run validation
- Validation copies files to temp dir and runs `python3 -m pytest -v --tb=short`
- Existing `task.json` format: `id`, `category`, `title`, `description`, `difficulty` (`easy`/`medium`/`hard`), `bug_type`, `knowledge_points`, `source`
