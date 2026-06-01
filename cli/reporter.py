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
        elif r["error"] == "EXTRACT_FAIL":
            status = "EXTRACT_FAIL"
        elif r["error"] == "API_ERROR":
            status = "API_ERROR"
        elif r["error"] == "SYNTAX_ERROR":
            status = "SYNTAX_ERROR"
        else:
            status = f"FAIL ({r['passed_count']}/{r['total_count']})"
        print(f"  {r['task_id']:>4}  {status}")

    print()
    width = 44
    ratio = passed / total * 100 if total > 0 else 0
    label = f" Results: {passed}/{total} passed ({ratio:.1f}%) "
    print("╔" + "═" * width + "╗")
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
