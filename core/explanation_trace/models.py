"""Data models for the Legal Explanation Trace explainability layer."""

from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class InterrogativeTraceType(str, Enum):
    """The 8 interrogative trace query types."""
    WHY = "WHY"                         # Legal justification, rationale, and policy intent
    SOURCE = "SOURCE"                   # Primary authority, official publisher, portal URL
    WHEN = "WHEN"                       # Temporal validity, effective dates, statutory deadlines
    WHERE = "WHERE"                     # Jurisdictional limits, forum rules, court hierarchy
    WHAT_IF = "WHAT_IF"                 # Counterfactual scenario evaluation
    WHAT_CHANGED = "WHAT_CHANGED"       # Statutory/judicial evolution over time
    WHAT_DISAGREES = "WHAT_DISAGREES"   # Contrary precedents, circuit splits, opposing theories
    WHAT_IS_MISSING = "WHAT_IS_MISSING" # Unverified record facts, missing affidavits or findings


class ExplanationTraceRecord(BaseModel):
    """The 10 mandatory fields exposed for every substantive legal conclusion."""
    claim: str = Field(..., description="1. The substantive legal proposition asserted")
    source: str = Field(..., description="2. The formal legal citation")
    authority_level: str = Field(..., description="3. Hierarchical authority tier e.g. T0 Constitutional, T5 State Statute")
    jurisdiction: str = Field(..., description="4. Controlling jurisdiction code e.g. US-WA, US-IL, US")
    effective_date: str = Field(..., description="5. Date of enactment, effective range, or current validity")
    relevant_text: str = Field(..., description="6. Direct quoted or cited excerpt from primary authority")
    reasoning_step: str = Field(..., description="7. Concise, auditable syllogistic step connecting authority to claim (no hidden CoT)")
    confidence_verification: str = Field(..., description="8. Explicit verification state, citator signal, and confidence score")
    counterargument: str = Field(..., description="9. Opposing legal theory, agency counter-claim, or defense interpretation")
    limitation: str = Field(..., description="10. Boundary conditions, exigent exceptions, or circumstances where claim ceases to hold")


class InterrogativeTraceResult(BaseModel):
    """Result of an interrogative trace inquiry on a specific conclusion."""
    trace_type: InterrogativeTraceType
    claim: str
    inquiry: str
    concise_auditable_summary: str
    supporting_authority: List[str] = Field(default_factory=list)
    factual_predicates_required: List[str] = Field(default_factory=list)
    official_portal_url: Optional[str] = None


class ExplanationTraceReport(BaseModel):
    """Container report aggregating conclusion traces and interrogatives."""
    subject_matter: str
    jurisdiction: str
    traces: List[ExplanationTraceRecord] = Field(default_factory=list)
