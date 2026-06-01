import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bench",
        description="LLM Bug Benchmark CLI — 评测 LLM 修复 bug 的能力",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="运行评测")
    run_parser.add_argument("--model", default="gpt-4o", help="模型名称 (默认: gpt-4o)")
    run_parser.add_argument("--tasks", help="逗号分隔的题目 ID (如 001,002)")
    run_parser.add_argument("--all", action="store_true", help="运行所有题目")
    run_parser.add_argument("--base-url", help="API 地址 (覆盖 LLM_BASE_URL 环境变量)")
    run_parser.add_argument("--api-key", help="API 密钥 (覆盖 LLM_API_KEY 环境变量)")
    run_parser.add_argument("--json", action="store_true", help="以 JSON 格式输出结果")

    list_parser = sub.add_parser("list", help="列出可用题目")
    list_parser.add_argument("--category", choices=["basic", "intermediate", "advanced"],
                             help="按类别过滤")

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
