"""OpenWebUI Drop-In Custom Pipeline for Jurisdiction-Aware Legal Reasoning."""

from typing import List, Dict, Any, Optional, Generator, Union
from pydantic import BaseModel, Field
from datetime import date
from agents.legal_orchestrator import LegalGPTOrchestrator
from core.local_llm import LocalLLMClient

orchestrator = LegalGPTOrchestrator()


class PipelineValves(BaseModel):
    default_state: str = Field(default="WA", description="Default state code when unspecified")
    default_persona_mode: str = Field(default="standard", description="standard, self_represented, investigator, attorney, court")
    enable_local_llm_hybrid: bool = Field(default=False, description="Whether to blend local LLM inference with deterministic engine")
    local_llm_url: str = Field(default="http://localhost:1234/v1", description="Local OpenAI-compatible base URL")


class Pipeline:
    """OpenWebUI Custom Pipeline connecting chat UI to Legal-GPT reasoning and citator engines."""

    def __init__(self):
        self.name = "Legal-GPT: Jurisdiction & Citation Verified Legal AI"
        self.valves = PipelineValves()
        self.llm_client = LocalLLMClient(base_url=self.valves.local_llm_url)

    async def on_startup(self):
        print(f"[OpenWebUI Pipeline] Legal-GPT Pipeline initialized (Default State: {self.valves.default_state})")

    async def on_shutdown(self):
        print("[OpenWebUI Pipeline] Legal-GPT Pipeline shutdown.")

    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: List[Dict[str, str]],
        body: Dict[str, Any]
    ) -> Union[str, Generator[str, None, None]]:
        """Processes incoming OpenWebUI user messages through the Legal-GPT core pipeline."""
        if not user_message.strip():
            return "Please provide a legal inquiry or case fact pattern."

        # Execute Legal-GPT reasoning
        resp = orchestrator.process_query(
            query=user_message,
            override_state=self.valves.default_state,
            persona_mode=self.valves.default_persona_mode # type: ignore
        )

        return resp.render_markdown()
