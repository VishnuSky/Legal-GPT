"""Local AI Inference Layer: OpenAI-Compatible Fleet Reasoner Client."""

import os
import json
import logging
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List

logger = logging.getLogger("legal_gpt.local_llm")


class LocalLLMClient:
    """Client for local OpenAI-compatible inference servers (LM Studio, Ollama, vLLM, llama.cpp)."""

    PREFERRED_REASONING_PATTERNS = [
        "qwen2.5-32b",
        "qwen3",
        "nemotron",
        "deepseek-r1",
        "phi-4-reasoning",
        "phi-4",
        "llama-3.3-70b",
        "llama-3.1-8b",
        "mistral-small",
        "qwen",
        "instruct",
        "chat"
    ]

    def __init__(
        self,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        timeout_seconds: int = 120
    ):
        self.base_url = (base_url or os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:1234/v1")).rstrip("/")
        self.explicit_model = model_name or os.getenv("LOCAL_LLM_MODEL")
        self.timeout_seconds = timeout_seconds

    def get_available_models(self) -> List[str]:
        """Queries GET /models to discover running models on the local AI server."""
        try:
            url = f"{self.base_url}/models"
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    models_list = data.get("data", [])
                    return [m.get("id") for m in models_list if "id" in m]
        except Exception as e:
            logger.debug(f"Local model discovery query failed: {e}")
        return []

    def select_best_model(self) -> str:
        """Selects preferred reasoning/instruct model from active server models."""
        if self.explicit_model:
            return self.explicit_model

        available = self.get_available_models()
        if not available:
            return "local-model"

        # Search by priority
        for pref in self.PREFERRED_REASONING_PATTERNS:
            for model_id in available:
                if pref in model_id.lower():
                    return model_id

        return available[0]

    def is_available(self) -> bool:
        """Check if local inference server is online."""
        try:
            url = f"{self.base_url}/models"
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=2) as response:
                return response.status == 200
        except Exception:
            return False

    @classmethod
    def format_legal_reasoning_prompt(
        cls,
        user_question: str,
        retrieved_chunks: List[Dict[str, str]],
        jurisdiction_lock: str
    ) -> List[Dict[str, str]]:
        """Constructs a strict grounding prompt with retrieved chunks, question, and mandatory abstention rules."""
        chunk_lines = []
        for i, chk in enumerate(retrieved_chunks, 1):
            cite = chk.get("citation", "Statutory Provision")
            txt = chk.get("text", "").strip()
            chunk_lines.append(f"[{i}] {cite}:\n{txt}")

        chunks_block = "\n\n".join(chunk_lines) if chunk_lines else "NO_AUTHORITATIVE_CHUNKS_RETRIEVED"

        system_prompt = (
            f"You are a jurisdiction-locked legal reasoning engine operating under {jurisdiction_lock}.\n"
            "MANDATORY CONSTRAINTS:\n"
            "1. Base your answer EXCLUSIVELY on the retrieved primary statutory and administrative authority provided below.\n"
            "2. If the retrieved authority does NOT contain sufficient legal grounds to answer the question, state 'ABSTAIN: Insufficient controlling authority retrieved.'\n"
            "3. Cite exact sections (e.g., RCW, WAC, U.S.C.) for every assertion made.\n"
            "4. NEVER diagnose, label, or score individuals. Output strictly advisory, procedure-focused legal analysis.\n"
            "5. Maintain absolute zero-hallucination discipline."
        )

        user_content = (
            f"JURISDICTION: {jurisdiction_lock}\n\n"
            f"RETRIEVED AUTHORITATIVE SOURCES:\n{chunks_block}\n\n"
            f"LEGAL QUESTION:\n{user_question}\n\n"
            "Provide your reasoning, followed by the controlling citations and exact statutory standards."
        )

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

    def generate_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.1,
        max_tokens: int = 2048
    ) -> Optional[str]:
        """Generate response via local LLM with 120s timeout and soft fallback to deterministic reasoning."""
        model = self.select_best_model()
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
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
                    choices = res_json.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "").strip()
        except Exception as e:
            logger.debug(f"Local LLM completion failed softly: {e}")
            return None
        return None
