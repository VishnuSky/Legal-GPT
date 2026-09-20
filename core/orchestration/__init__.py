"""Legal-GPT Unified Orchestration Package."""

from core.orchestration.handoff import (
    VerifiedSourceReference,
    SafeHandoffContract,
    HandoffVerificationResult,
)
from core.orchestration.provider import (
    ProviderConfig,
    ProviderExecutionResult,
    BaseProvider,
    GrokProvider,
    LocalLLMProvider,
    FallbackDeterministicProvider,
    OrchestrationRouter,
)

__all__ = [
    "VerifiedSourceReference",
    "SafeHandoffContract",
    "HandoffVerificationResult",
    "ProviderConfig",
    "ProviderExecutionResult",
    "BaseProvider",
    "GrokProvider",
    "LocalLLMProvider",
    "FallbackDeterministicProvider",
    "OrchestrationRouter",
]
