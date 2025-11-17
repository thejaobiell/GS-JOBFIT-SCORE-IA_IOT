import os
import json
import re
from typing import Any, Dict, Optional
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

DEFAULT_OPTIONS = {
    "num_ctx": int(os.getenv("OLLAMA_NUM_CTX", "4096")),
    "temperature": float(os.getenv("OLLAMA_TEMPERATURE", "0.2")),
    "num_predict": int(os.getenv("OLLAMA_NUM_PREDICT", "800")),
}


class OllamaError(RuntimeError):
    pass


def _extract_json(text: str) -> str:
    # Remove cercas de markdown
    cleaned = re.sub(r"```(?:json)?\s*|\s*```", "", text).strip()
    # Tenta pegar bloco entre primeiro { e último }
    if cleaned.count("{") and cleaned.count("}"):
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            return cleaned[start : end + 1]
    return cleaned


def generate_json(
    prompt: str, model: Optional[str] = None, options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Chama o Ollama e retorna um dict JSON garantido."""
    model_name = model or OLLAMA_MODEL
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {**DEFAULT_OPTIONS, **(options or {})},
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=180)
        resp.raise_for_status()
        data = resp.json()
        text = data.get("response", "").strip()
        json_str = _extract_json(text)
        return json.loads(json_str)
    except requests.exceptions.RequestException as e:
        raise OllamaError(f"Erro HTTP ao chamar Ollama: {e}") from e
    except json.JSONDecodeError as e:
        raise OllamaError(
            f"Falha ao decodificar JSON retornado pelo modelo: {e}\nResposta bruta: {text}"
        ) from e
