from cli.tasks import filter_tasks


def list_tasks(args):
    tasks = filter_tasks(category=args.category)
    if not tasks:
        print("未找到题目。")
        return
    print(f"\n{'ID':>4}  {'类别':<14} {'难度':<10} 标题")
    print("-" * 60)
    for t in tasks:
        print(f"{t['id']:>4}  {t['category']:<14} {t['difficulty']:<10} {t['title']}")

    cat = f" ({args.category})" if args.category else ""
    print(f"\n共 {len(tasks)} 道题{cat}\n")
