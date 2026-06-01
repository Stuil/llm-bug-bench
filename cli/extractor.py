import re


def extract_code(text: str) -> str | None:
    pattern = re.compile(r"```(?:python)?\s*\n(.*?)```", re.DOTALL)
    matches = pattern.findall(text)
    if matches:
        return matches[0].strip()
    stripped = text.strip()
    return stripped if stripped else None


def validate_code(code: str) -> bool:
    try:
        compile(code, "<extracted>", "exec")
        return True
    except SyntaxError:
        return False
