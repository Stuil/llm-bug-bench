import os
import subprocess
import sys
import tempfile


def evaluate_task(task_id: str, test_code: str, fixed_code: str) -> dict:
    with tempfile.TemporaryDirectory() as tmpdir:
        buggy_path = os.path.join(tmpdir, "buggy.py")
        test_path = os.path.join(tmpdir, "test.py")

        with open(buggy_path, "w") as f:
            f.write(fixed_code)
        with open(test_path, "w") as f:
            f.write(test_code)

        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_path, "-v", "--tb=short"],
                capture_output=True, text=True, timeout=60,
            )
        except subprocess.TimeoutExpired:
            return {
                "task_id": task_id,
                "passed": False,
                "passed_count": 0,
                "total_count": 0,
                "output": "",
                "error": "TIMEOUT",
            }

        output = result.stdout + "\n" + result.stderr

        passed_count = output.count(" PASSED")
        failed_count = output.count(" FAILED")
        error_count = output.count(" ERROR")
        total_count = passed_count + failed_count + error_count

        return {
            "task_id": task_id,
            "passed": result.returncode == 0,
            "passed_count": passed_count,
            "total_count": total_count,
            "output": output.strip(),
            "error": None if result.returncode == 0 else "TESTS_FAILED",
        }
