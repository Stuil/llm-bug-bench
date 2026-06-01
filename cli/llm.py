import json
import os
import urllib.error
import urllib.request


def get_api_config(args) -> tuple[str, str, str]:
    api_key = args.api_key or os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
    base_url = args.base_url or os.environ.get("LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = args.model
    return api_key, base_url.rstrip("/"), model


def call_llm(messages: list[dict], api_key: str, base_url: str, model: str) -> str:
    url = f"{base_url}/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.0,
    }).encode()

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode())
        return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        detail = e.read().decode()
        raise RuntimeError(f"API 错误 {e.code}: {detail}") from e
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        raise RuntimeError(f"API 响应格式异常: {e}") from e
