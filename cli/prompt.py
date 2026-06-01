SYSTEM_PROMPT = (
    "You are a Python bug-fixing expert. "
    "Given a piece of buggy Python code and a description of the bug, "
    "return the complete fixed code. "
    "Output ONLY the fixed Python code inside a ```python code block. "
    "Do not include any explanations or commentary."
)


def build_messages(buggy_code: str, description: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"The following Python code contains a bug:\n\n"
                f"```python\n{buggy_code}\n```\n\n"
                f"Bug description: {description}\n\n"
                f"Please fix the bug and return the complete corrected code."
            ),
        },
    ]
