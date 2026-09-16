"""Model capabilities definition for Legal-GPT."""

from enum import Enum
from typing import List, Dict, Any
from pydantic import BaseModel, Field


class ModelCapability(str, Enum):
    LEGAL_REASONING = "legal_reasoning"
    JURISDICTION_ISOLATION = "jurisdiction_isolation"
    TEMPORAL_AWARENESS = "temporal_awareness"
    AUTHORITY_CLASSIFICATION = "authority_classification"
    CITATION_VERIFICATION = "citation_verification"
    CPS_ANALYSIS = "cps_analysis"
    CONSTITUTIONAL_ANALYSIS = "constitutional_analysis"
    HUMAN_RIGHTS_ANALYSIS = "human_rights_analysis"
    HEALTH_LAW_ANALYSIS = "health_law_analysis"
    CONFLICT_DETECTION = "conflict_detection"
    EPISTEMIC_CLASSIFICATION = "epistemic_classification"
    UNCERTAINTY_QUANTIFICATION = "uncertainty_quantification"


class ModelSpecs(BaseModel):
    name: str = "Legal-GPT"
    version: str = "0.3.0-alpha"
    base_model: str = "Qwen/Qwen2.5-14B-Instruct"
    context_window: int = 32768
    capabilities: List[ModelCapability] = Field(default_factory=lambda: list(ModelCapability))
    quantizations_supported: List[str] = Field(
        default_factory=lambda: ["Q4_K_M", "Q5_K_M", "Q8_0", "F16"]
    )
    metadata: Dict[str, Any] = Field(default_factory=dict)
