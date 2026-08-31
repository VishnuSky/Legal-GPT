"""Local AI Inference Layer: OpenAI-Compatible Client for LM Studio, Ollama, and Local AI Nodes."""

import os
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List


class LocalLLMClient:
    """Client for local OpenAI-compatible inference servers (LM Studio, Ollama, vLLM, llama.cpp)."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        timeout_seconds: int = 15
    ):
        self.base_url = base_url or os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:1234/v1")
        self.model_name = model_name or os.getenv("LOCAL_LLM_MODEL", "legal-model-v1")
        self.timeout_seconds = timeout_seconds

    def is_available(self) -> bool:
        """Check if local inference server is online."""
        try:
            url = f"{self.base_url.rstrip('/')}/models"
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=2) as response:
                return response.status == 200
        except Exception:
            return False

    def generate_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.1,
        max_tokens: int = 1024
    ) -> Optional[str]:
        """Generate response via local LLM or return None if offline (allowing fallback to deterministic reasoning)."""
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=self.timeout_seconds) as response:
                if response.status == 200:
                    res_json = json.loads(response.read().decode("utf-8"))
                    return res_json["choices"][0]["message"]["content"].strip()
        except Exception:
            return None
        return None
