"""Legal uncertainty quantification and missing facts identification."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class UncertaintyAssessment(BaseModel):
    confidence_score: float  # 0.0 to 1.0
    missing_material_facts: List[str] = Field(default_factory=list)
    unresolved_legal_questions: List[str] = Field(default_factory=list)
    abstention_warranted: bool = False
    abstention_reason: Optional[str] = None


class UncertaintyEngine:
    """Quantifies uncertainty and determines if procedural abstention is required."""

    @classmethod
    def evaluate_uncertainty(
        cls,
        jurisdiction: Optional[str],
        material_facts_present: List[str],
        verified_authorities: List[str]
    ) -> UncertaintyAssessment:
        missing_facts = []
        unresolved_q = []
        abstention = False
        reason = None

        if not jurisdiction or jurisdiction.upper() in ("UNKNOWN", "UNSPECIFIED", ""):
            abstention = True
            reason = "Jurisdiction not specified. State-specific statutory requirements cannot be conclusively advised."
            unresolved_q.append("What state or tribal jurisdiction governs this proceeding?")

        if not verified_authorities:
            abstention = True
            reason = "No authoritative primary sources verified for this legal proposition."
            unresolved_q.append("Primary controlling statute, court rule, or precedent required.")

        # Check facts
        if len(material_facts_present) == 0:
            missing_facts.append("Specific date of state intervention or court hearing")
            missing_facts.append("Exact procedural posture (e.g. initial detention vs adjudication vs disposition)")

        score = 0.95
        if missing_facts:
            score -= 0.20
        if abstention:
            score = 0.30

        return UncertaintyAssessment(
            confidence_score=max(0.1, score),
            missing_material_facts=missing_facts,
            unresolved_legal_questions=unresolved_q,
            abstention_warranted=abstention,
            abstention_reason=reason
        )
