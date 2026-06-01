# LLM Bug Benchmark

一个用于评测大语言模型修复 bug 能力的 Python 基准测试集。

## 目录结构

```
llm-bug-bench/
├── cli/                    # （v2）评测 CLI 工具
│   ├── __init__.py
│   ├── __main__.py         # python -m cli 入口
│   ├── main.py             # 参数解析
│   ├── tasks.py            # 题目加载
│   ├── prompt.py           # Prompt 组装
│   ├── extractor.py        # LLM 响应代码提取
│   ├── llm.py              # OpenAI 兼容 API 客户端
│   ├── evaluator.py        # pytest 评测
│   ├── reporter.py         # 结果报告
│   ├── runner.py           # 评测协调器
│   └── lister.py           # 题目列表
├── tasks/                   # 所有题目
│   ├── basic/               # 基础题（8 道）
│   ├── intermediate/        # 进阶题（8 道）
│   ├── advanced/            # 挑战题（4 道）
│   └── tasks.json           # 全局索引（自动生成）
├── scripts/
│   ├── validate_tasks.py    # 题目验证脚本
│   └── bench                # CLI 入口脚本
├── docs/
│   └── superpowers/         # 设计和实现文档
└── README.md
```

## 快速开始

```bash
pip install pytest
python scripts/validate_tasks.py
```

## 题目格式

每道题包含 4 个文件：

- `buggy.py` — 有 bug 的代码
- `fixed.py` — 修复后的参考实现
- `test.py` — pytest 测试用例（对 buggy 至少 fail 1 个，对 fixed 全部通过）
- `task.json` — 题目元信息

## 添加题目

1. 在对应类别目录下创建新目录
2. 添加 4 个文件：buggy.py、fixed.py、test.py、task.json
3. 运行 `python scripts/validate_tasks.py` 验证

## CLI 评测（v2）

评测工具通过 OpenAI 兼容接口调用 LLM，自动提取修复代码并运行 pytest 验证。

### 基本用法

```bash
# 列出所有题目
./scripts/bench list

# 按类别过滤
./scripts/bench list --category basic

# 评测指定题目
export LLM_API_KEY="sk-xxx"
./scripts/bench run --model gpt-4o --tasks 001,002,003

# 评测全部题目
./scripts/bench run --model deepseek-chat --all

# JSON 格式输出
./scripts/bench run --model gpt-4o --tasks 001 --json
```

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `LLM_API_KEY` 或 `OPENAI_API_KEY` | API 密钥 | — |
| `LLM_BASE_URL` 或 `OPENAI_BASE_URL` | API 地址 | `https://api.openai.com/v1` |

### 评测流程

1. 读取 `buggy.py` + 题目描述 → 组装 prompt
2. 调用 LLM API（temperature=0）
3. 从响应中提取 Python 代码
4. 写入临时目录，运行 pytest
5. 输出评分报告
