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

## CLI Evaluation (v2)

```bash
# 列出可用题目
./scripts/bench list

# 按类别过滤
./scripts/bench list --category basic

# 评测指定题目
export LLM_API_KEY="your-api-key"
./scripts/bench run --model gpt-4o --tasks 001,002,003

# 评测全部题目
./scripts/bench run --model deepseek-chat --all

# JSON 格式输出
./scripts/bench run --model gpt-4o --tasks 001 --json
```

环境变量:
- `LLM_API_KEY` 或 `OPENAI_API_KEY` — API 密钥
- `LLM_BASE_URL` 或 `OPENAI_BASE_URL` — API 地址 (默认: `https://api.openai.com/v1`)
