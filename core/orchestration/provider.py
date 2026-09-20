"""Unified Provider Orchestration Layer: Grok, Local AI, and Deterministic Fallback."""

import os
import json
import time
import logging
import urllib.request
import urllib.error
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Literal
from pydantic import BaseModel, Field, field_validator
from core.orchestration.handoff import SafeHandoffContract, HandoffVerificationResult
from audit.ledger import audit_ledger

logger = logging.getLogger("legal_gpt.orchestration")


class ProviderConfig(BaseModel):
    """Configuration validator for model providers."""
    provider_type: Literal["grok", "local", "deterministic"]
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model_name: str
    timeout_seconds: int = 30
    max_retries: int = 2
    retry_delay_seconds: float = 0.5
    temperature: float = 0.1
    max_tokens: int = 2048
    local_only: bool = False

    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        if v < 0.0 or v > 1.0:
            raise ValueError("Temperature must be between 0.0 and 1.0 for legal reasoning stability.")
        return v

    @field_validator("max_tokens")
    @classmethod
    def validate_max_tokens(cls, v: int) -> int:
        if v <= 0 or v > 32768:
            raise ValueError("max_tokens must be between 1 and 32768.")
        return v


class ProviderExecutionResult(BaseModel):
    """Execution telemetry and output from a provider call."""
    provider_id: str
    model_name: str
    success: bool
    raw_text: Optional[str] = None
    verified_result: Optional[HandoffVerificationResult] = None
    error_message: Optional[str] = None
    latency_ms: float = 0.0
    attempts: int = 1


class BaseProvider(ABC):
    """Abstract base provider for inference engines."""

    def __init__(self, config: ProviderConfig):
        self.config = config

    @property
    def provider_id(self) -> str:
        return self.config.provider_type

    @property
    def model_name(self) -> str:
        return self.config.model_name

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is online and reachable."""
        pass

    @abstractmethod
    def execute(self, contract: SafeHandoffContract) -> ProviderExecutionResult:
        """Execute reasoning for the handoff contract."""
        pass


class GrokProvider(BaseProvider):
    """xAI Grok Provider with retry backoff and error handling."""

    def __init__(self, config: Optional[ProviderConfig] = None):
        cfg = config or ProviderConfig(
            provider_type="grok",
            api_key=os.getenv("XAI_API_KEY"),
            base_url=os.getenv("XAI_BASE_URL", "https://api.x.ai/v1"),
            model_name=os.getenv("XAI_MODEL", "grok-2-1212"),
            timeout_seconds=int(os.getenv("XAI_TIMEOUT", "30")),
            local_only=os.getenv("LOCAL_ONLY", "false").lower() == "true"
        )
        super().__init__(cfg)

    def is_available(self) -> bool:
        if self.config.local_only or not self.config.api_key:
            return False
        # Lightweight check: If API key is present and remote not disabled
        return True

    def execute(self, contract: SafeHandoffContract) -> ProviderExecutionResult:
        start_time = time.time()
        if self.config.local_only:
            return ProviderExecutionResult(
                provider_id=self.provider_id,
                model_name=self.model_name,
                success=False,
                error_message="Remote providers disabled (LOCAL_ONLY=True).",
                latency_ms=(time.time() - start_time) * 1000
            )

        if not self.config.api_key:
            return ProviderExecutionResult(
                provider_id=self.provider_id,
                model_name=self.model_name,
                success=False,
                error_message="Grok API key missing (XAI_API_KEY).",
                latency_ms=(time.time() - start_time) * 1000
            )

        messages = contract.build_prompt_messages()
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }

        url = f"{self.config.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }

        attempts = 0
        last_error = None

        for attempt in range(1, self.config.max_retries + 1):
            attempts = attempt
            try:
                data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(url, data=data, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=self.config.timeout_seconds) as resp:
                    if resp.status == 200:
                        body = json.loads(resp.read().decode("utf-8"))
                        choices = body.get("choices", [])
                        if choices:
                            raw_content = choices[0].get("message", {}).get("content", "").strip()
                            verified = contract.validate_model_output(raw_content)
                            return ProviderExecutionResult(
                                provider_id=self.provider_id,
                                model_name=self.model_name,
                                success=verified.passed,
                                raw_text=raw_content,
                                verified_result=verified,
                                latency_ms=(time.time() - start_time) * 1000,
                                attempts=attempts
                            )
            except urllib.error.HTTPError as e:
                last_error = f"HTTP {e.code}: {e.reason}"
                if e.code in (401, 403):
                    break  # Do not retry credential failures
            except Exception as e:
                last_error = str(e)

            time.sleep(self.config.retry_delay_seconds * (2 ** (attempt - 1)))

        return ProviderExecutionResult(
            provider_id=self.provider_id,
            model_name=self.model_name,
            success=False,
            error_message=f"Grok invocation failed: {last_error}",
            latency_ms=(time.time() - start_time) * 1000,
            attempts=attempts
        )


class LocalLLMProvider(BaseProvider):
    """Local OpenAI-compatible inference provider (LM Studio, Ollama, vLLM)."""

    def __init__(self, config: Optional[ProviderConfig] = None):
        cfg = config or ProviderConfig(
            provider_type="local",
            base_url=os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:1234/v1"),
            model_name=os.getenv("LOCAL_LLM_MODEL", "local-reasoning-model"),
            timeout_seconds=int(os.getenv("LOCAL_LLM_TIMEOUT", "10")),
            max_retries=1
        )
        super().__init__(cfg)

    def is_available(self) -> bool:
        try:
            url = f"{self.config.base_url.rstrip('/')}/models"
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=1) as resp:
                return resp.status == 200
        except Exception:
            return False

    def execute(self, contract: SafeHandoffContract) -> ProviderExecutionResult:
        start_time = time.time()
        messages = contract.build_prompt_messages()
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }

        url = f"{self.config.base_url.rstrip('/')}/chat/completions"
        headers = {"Content-Type": "application/json"}

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=self.config.timeout_seconds) as resp:
                if resp.status == 200:
                    body = json.loads(resp.read().decode("utf-8"))
                    choices = body.get("choices", [])
                    if choices:
                        raw_content = choices[0].get("message", {}).get("content", "").strip()
                        verified = contract.validate_model_output(raw_content)
                        return ProviderExecutionResult(
                            provider_id=self.provider_id,
                            model_name=self.model_name,
                            success=verified.passed,
                            raw_text=raw_content,
                            verified_result=verified,
                            latency_ms=(time.time() - start_time) * 1000,
                            attempts=1
                        )
        except Exception as e:
            return ProviderExecutionResult(
                provider_id=self.provider_id,
                model_name=self.model_name,
                success=False,
                error_message=f"Local LLM connection failed: {e}",
                latency_ms=(time.time() - start_time) * 1000,
                attempts=1
            )

        return ProviderExecutionResult(
            provider_id=self.provider_id,
            model_name=self.model_name,
            success=False,
            error_message="Local LLM returned empty choices.",
            latency_ms=(time.time() - start_time) * 1000,
            attempts=1
        )


class FallbackDeterministicProvider(BaseProvider):
    """Deterministic, zero-network fallback synthesizing directly from verified sources."""

    def __init__(self):
        cfg = ProviderConfig(
            provider_type="deterministic",
            model_name="Deterministic-Rule-Engine",
            timeout_seconds=1
        )
        super().__init__(cfg)

    def is_available(self) -> bool:
        return True

    def execute(self, contract: SafeHandoffContract) -> ProviderExecutionResult:
        start_time = time.time()
        if not contract.verified_sources:
            abstain_text = (
                f"ABSTAIN: Insufficient controlling primary authority retrieved for jurisdiction {contract.jurisdiction}. "
                "Legal-GPT will not fabricate legal procedures."
            )
            verified = contract.validate_model_output(abstain_text)
            return ProviderExecutionResult(
                provider_id=self.provider_id,
                model_name=self.model_name,
                success=True,
                raw_text=abstain_text,
                verified_result=verified,
                latency_ms=(time.time() - start_time) * 1000,
                attempts=1
            )

        # Build grounded synthesis strictly from verified sources
        lines = [
            f"[DETERMINISTIC ANALYSIS — JURISDICTION: {contract.jurisdiction}]",
            f"TASK: {contract.task_type.replace('_', ' ').title()}",
            "CONTROLLING VERIFIED AUTHORITIES:"
        ]
        for s in contract.verified_sources:
            lines.append(f"- {s.citation} ({s.authority_layer} / {s.authority_tier}): {s.key_holding_or_text or 'Controlling Standard'}")

        if contract.candidate_claims:
            lines.append("\nPROCEDURAL STATUS OF CLAIMS:")
            for claim in contract.candidate_claims:
                lines.append(f"- Claim: '{claim}' must satisfy statutory standard of proof under {contract.jurisdiction}.")

        lines.append("\nDISCLAIMER: Legal information only. Not legal advice. Procedural rights require verification.")
        synth_text = "\n".join(lines)
        verified = contract.validate_model_output(synth_text)

        return ProviderExecutionResult(
            provider_id=self.provider_id,
            model_name=self.model_name,
            success=verified.passed,
            raw_text=synth_text,
            verified_result=verified,
            latency_ms=(time.time() - start_time) * 1000,
            attempts=1
        )


class OrchestrationRouter:
    """Routes reasoning tasks across providers with role-based routing and failover."""

    ROUTING_POLICY: Dict[str, List[str]] = {
        "concept_explanation": ["grok", "local", "deterministic"],
        "statutory_lookup": ["local", "grok", "deterministic"],
        "case_analysis": ["grok", "local", "deterministic"],
        "adversarial_review": ["grok", "local", "deterministic"],
        "procedural_deadlines": ["deterministic", "local"],
        "service_routing": ["deterministic"]
    }

    def __init__(
        self,
        local_only: Optional[bool] = None,
        grok_provider: Optional[BaseProvider] = None,
        local_provider: Optional[BaseProvider] = None,
        fallback_provider: Optional[BaseProvider] = None
    ):
        self.local_only = local_only if local_only is not None else (os.getenv("LOCAL_ONLY", "false").lower() == "true")
        self.providers: Dict[str, BaseProvider] = {
            "grok": grok_provider or GrokProvider(ProviderConfig(
                provider_type="grok",
                api_key=os.getenv("XAI_API_KEY"),
                model_name=os.getenv("XAI_MODEL", "grok-2-1212"),
                local_only=self.local_only
            )),
            "local": local_provider or LocalLLMProvider(),
            "deterministic": fallback_provider or FallbackDeterministicProvider()
        }

    def dispatch(self, contract: SafeHandoffContract) -> ProviderExecutionResult:
        """Dispatches contract according to routing policy with failover cascade and audit logging."""
        route_chain = self.ROUTING_POLICY.get(contract.task_type, ["grok", "local", "deterministic"])

        # If local_only is enforced, filter out remote providers
        if self.local_only:
            route_chain = [p for p in route_chain if p != "grok"]
            if "deterministic" not in route_chain:
                route_chain.append("deterministic")

        tried_errors = []
        for provider_name in route_chain:
            provider = self.providers.get(provider_name)
            if not provider:
                continue

            if not provider.is_available() and provider_name != "deterministic":
                tried_errors.append(f"{provider_name}: unavailable")
                continue

            res = provider.execute(contract)
            if res.success and res.verified_result and res.verified_result.passed:
                # Log successful handoff to audit ledger
                try:
                    audit_ledger.record_session(
                        user_query=f"Task {contract.task_id} ({contract.task_type})",
                        jurisdiction=contract.jurisdiction,
                        authorities_used=[s.citation for s in contract.verified_sources],
                        output_text=res.raw_text or "",
                        retrieval_queries=[contract.task_id],
                        chunks_used=[],
                        counterarguments_count=0
                    )
                except Exception:
                    pass
                return res
            else:
                tried_errors.append(f"{provider_name}: {res.error_message or (res.verified_result.abstention_reason if res.verified_result else 'failed')}")

        # If all providers failed or were unavailable, fall back to deterministic
        fallback = self.providers["deterministic"]
        res = fallback.execute(contract)
        res.error_message = f"Failover cascade triggered: {'; '.join(tried_errors)}"
        return res
