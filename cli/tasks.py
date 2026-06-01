import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASKS_DIR = os.path.join(BASE_DIR, "tasks")
INDEX_PATH = os.path.join(TASKS_DIR, "tasks.json")


def load_index() -> dict:
    with open(INDEX_PATH) as f:
        return json.load(f)


def get_task_dir(task_id: str) -> str:
    for root, dirs, files in os.walk(TASKS_DIR):
        if os.path.basename(root).startswith(task_id):
            return root
    raise ValueError(f"未找到题目 {task_id}")


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
    index = load_index()
    tasks = index["tasks"]
    if category:
        tasks = [t for t in tasks if t["category"] == category]
    if task_ids:
        tasks = [t for t in tasks if t["id"] in task_ids]
    return tasks
