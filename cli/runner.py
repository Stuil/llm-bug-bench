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
        print("错误: 请指定 --tasks 或 --all", file=sys.stderr)
        sys.exit(1)

    api_key, base_url, model = get_api_config(args)

    if not api_key:
        print("错误: 未设置 LLM_API_KEY 或 OPENAI_API_KEY 环境变量", file=sys.stderr)
        sys.exit(1)

    print(f"\n评测 {len(task_ids)} 道题，模型={model}")
    if base_url:
        print(f"API 地址: {base_url}")
    print()

    results = []
    for i, task_id in enumerate(task_ids, 1):
        print(f"  [{i}/{len(task_ids)}] 题目 {task_id}...", end=" ", flush=True)

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

        result = evaluate_task(task_id, task["test_code"], fixed_code)
        if result["passed"]:
            print("PASS")
        else:
            print(f"FAIL ({result['passed_count']}/{result['total_count']})")
        results.append(result)

    if getattr(args, "json", False):
        print_json_results(results, model)
    else:
        print_results(results, model)
