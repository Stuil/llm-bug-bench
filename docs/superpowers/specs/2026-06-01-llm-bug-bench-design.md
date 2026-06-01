# LLM Bug Benchmark — Design Spec

## 概述

LLM Bug Benchmark 是一个纯 Python 的 bug 修复评测数据集，专用于评估各大语言模型修复 bug 的能力。提供数据集（核心）+ 可选 CLI 评测工具，首批 20 题，后续扩展至 40+ 题。

## 目录结构

```
llm-bug-bench/
├── tasks/                          # 所有题目
│   ├── basic/                      # 基础题（语法、逻辑错误）
│   │   ├── 001_list_sort/
│   │   │   ├── buggy.py            #   有 bug 的代码
│   │   │   ├── fixed.py            #   修复后的正确代码（参考答案）
│   │   │   ├── test.py             #   pytest 测试用例
│   │   │   └── task.json           #   题目元信息
│   │   └── ...
│   ├── intermediate/               # 进阶题（并发、算法、边界条件）
│   │   └── ...
│   ├── advanced/                   # 挑战题（多文件、性能）
│   │   └── ...
│   └── tasks.json                  # 全局索引（自动生成）
├── cli/                            # （v2）评测 CLI，待建设
├── scripts/
│   └── validate_tasks.py           # 校验所有题目完整性
└── README.md
```

## 题目规范

每道题由 4 个文件组成：

### task.json

```json
{
  "id": "001",
  "category": "basic",
  "title": "列表排序函数错误",
  "description": "sort_list 函数排序结果不正确，当输入包含重复元素时行为与预期不符。",
  "difficulty": "easy",
  "bug_type": "逻辑错误",
  "knowledge_points": ["列表排序", "边界条件"],
  "source": "synthetic"
}
```

### buggy.py

包含 bug 的 Python 代码，可以是一个或多个函数/类。代码风格和错误应贴近真实开发场景。

### fixed.py

修复后的参考实现，用于验证测试和生成 test.py 的范围。

### test.py

pytest 测试，同时作用于 buggy.py（应至少 fail 1 个测试）和 fixed.py（应全部通过）。

**核心规则**：测试覆盖足以判定修复是否正确，但不泄漏 bug 的位置或修法。

## 难度分级

| 级别 | 代码行数 | Bug 类型举例 |
|------|---------|-------------|
| basic | 20-60 行 | 语法错误、少参数、比较符号、索引越界 |
| intermediate | 60-150 行 | 边界条件、类型误用、资源泄露、误解 API |
| advanced | 150+ 行或 2-3 文件 | 复杂逻辑、竞态、协议实现 |

## Bug 类型覆盖矩阵（首批 20 题）

| Bug 类型 | 数量 |
|---------|------|
| 逻辑错误 | 5 |
| 索引/切片错误 | 3 |
| 类型误用 | 3 |
| API 误用 | 3 |
| 并发/竞态 | 2 |
| 异常处理遗漏 | 2 |
| 正则/字符串 | 2 |

## 验证脚本

`scripts/validate_tasks.py` 确保：
- 每道题的 4 个文件齐全
- `buggy.py + test.py` → 至少 fail 1 个测试
- `fixed.py + test.py` → 全部通过
- `buggy.py` 与 `fixed.py` 有实际差异

## CLI 评测框架（v2）

CLI 工具 `bench` 的后端设计：

```
bench run --model deepseek-chat --tasks 001,002,003
```

流程：
1. 读取 buggy.py + task.json["description"] → 组装 prompt
2. 调用 LLM OpenAI-compatible API
3. 提取修复代码 → 写入临时目录
4. 运行 pytest 验证
5. 输出评分报告

只对接 OpenAI-compatible 接口，通过环境变量配置 API key 和 endpoint。

## 迭代计划

| 阶段 | 内容 |
|------|------|
| v1 | 数据结构 + 20 道题 + validate_tasks.py |
| v1.1 | 扩展到 40+ 题 |
| v2 | CLI 评测框架 |
| v2.1 | 支持并发多模型评测 |
