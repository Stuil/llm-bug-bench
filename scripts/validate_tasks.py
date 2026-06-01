#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
import tempfile

TASKS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tasks")


def get_task_dirs():
    task_dirs = []
    for root, dirs, files in os.walk(TASKS_DIR):
        if "task.json" in files and "buggy.py" in files and "fixed.py" in files and "test.py" in files:
            task_dirs.append(root)
    return sorted(task_dirs)


def load_task_metadata(task_dir):
    meta_path = os.path.join(task_dir, "task.json")
    with open(meta_path) as f:
        return json.load(f)


def validate_task(task_dir):
    task_id = os.path.basename(task_dir)
    required_files = ["buggy.py", "fixed.py", "test.py", "task.json"]
    errors = []

    for f in required_files:
        if not os.path.exists(os.path.join(task_dir, f)):
            errors.append(f"Missing {f}")

    if errors:
        return errors

    buggy_path = os.path.join(task_dir, "buggy.py")
    fixed_path = os.path.join(task_dir, "fixed.py")
    test_path = os.path.join(task_dir, "test.py")

    with open(buggy_path) as f:
        buggy_code = f.read()
    with open(fixed_path) as f:
        fixed_code = f.read()

    if buggy_code == fixed_code:
        errors.append("buggy.py and fixed.py are identical")
        return errors

    with tempfile.TemporaryDirectory() as tmpdir:
        test_tmp = os.path.join(tmpdir, "test.py")
        with open(test_tmp, "w") as f:
            f.write(open(test_path).read())

        buggy_tmp = os.path.join(tmpdir, "buggy.py")
        with open(buggy_tmp, "w") as f:
            f.write(buggy_code)
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_tmp, "-v", "--tb=short"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                errors.append("buggy.py passed all tests (should fail at least 1)")
        except subprocess.TimeoutExpired:
            pass

        fixed_tmp = os.path.join(tmpdir, "buggy.py")
        with open(fixed_tmp, "w") as f:
            f.write(fixed_code)
        shutil.rmtree(os.path.join(tmpdir, "__pycache__"), ignore_errors=True)
        shutil.rmtree(os.path.join(tmpdir, ".pytest_cache"), ignore_errors=True)
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_tmp, "-v", "--tb=short"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                stderr = result.stderr.strip()
                stdout = result.stdout.strip()
                detail = f"(exit code {result.returncode})"
                if stderr:
                    detail += f" stderr={stderr[:200]}"
                if stdout:
                    detail += f" stdout={stdout[:200]}"
                errors.append(f"fixed.py failed tests {detail}")
        except subprocess.TimeoutExpired:
            errors.append("fixed.py timed out (tests hung)")

    return errors


def update_global_index():
    tasks = []
    for task_dir in get_task_dirs():
        meta = load_task_metadata(task_dir)
        tasks.append(meta)

    index_path = os.path.join(TASKS_DIR, "tasks.json")
    with open(index_path) as f:
        index = json.load(f)
    index["meta"]["total_tasks"] = len(tasks)
    index["meta"]["generated_at"] = __import__("datetime").datetime.now().isoformat()
    index["tasks"] = sorted(tasks, key=lambda t: t["id"])
    with open(index_path, "w") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    print(f"Updated index: {len(tasks)} tasks")


def main():
    result = subprocess.run([sys.executable, "-m", "pytest", "--version"],
                            capture_output=True, timeout=10)
    if result.returncode != 0:
        print("Error: pytest is not installed")
        sys.exit(1)

    task_dirs = get_task_dirs()
    if not task_dirs:
        print("No task directories found")
        sys.exit(1)

    print(f"Found {len(task_dirs)} tasks\n")

    all_failed = False
    for task_dir in task_dirs:
        task_id = os.path.basename(task_dir)
        errors = validate_task(task_dir)
        if errors:
            all_failed = True
            print(f"  FAIL: {task_id}")
            for e in errors:
                print(f"    - {e}")
        else:
            print(f"  PASS: {task_id}")

    if all_failed:
        print("\nSome tasks failed validation!")
        sys.exit(1)

    print("\nAll tasks passed validation!")
    update_global_index()


if __name__ == "__main__":
    main()
