"""Data models and enums for the Legal Literacy Engine."""

from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class LiteracyLevel(int, Enum):
    """The 5 progressive legal literacy levels."""
    LEVEL_1_PLAIN_ENGLISH = 1       # Plain English / Intuitive
    LEVEL_2_PRACTICAL = 2           # Practical explanation in situational context
    LEVEL_3_TERMINOLOGY = 3         # Formal legal terminology and doctrine
    LEVEL_4_PRIMARY_AUTHORITY = 4   # Controlling constitutional, statutory, and caselaw authority
    LEVEL_5_ADVANCED_ANALYSIS = 5   # Advanced analysis: competing doctrines, splits, standards of review


class DrillDownAction(str, Enum):
    """The 5 on-demand drill-down actions."""
    SHOW_SOURCE = "SHOW_SOURCE"                 # "Show me the source."
    SHOW_STATUTE = "SHOW_STATUTE"               # "Show me the statute."
    SHOW_CASE = "SHOW_CASE"                     # "Show me the case."
    EXPLAIN_OPPOSING = "EXPLAIN_OPPOSING"       # "Explain the opposing interpretation."
    SHOW_TEMPORAL_CHANGE = "SHOW_TEMPORAL_CHANGE" # "Show me what changed over time."


class PrimaryAuthorityReference(BaseModel):
    """Structured primary legal authority reference."""
    citation: str
    source_type: str = Field(..., description="CONSTITUTION, STATUTE, REGULATION, CASELAW, POLICY")
    official_portal_url: str
    key_holding_or_text: str
    jurisdiction: str
    is_binding: bool = True


class DrillDownResult(BaseModel):
    """Result of a specific drill-down action."""
    action: DrillDownAction
    title: str
    content: str
    citations: List[str] = Field(default_factory=list)
    official_sources: List[str] = Field(default_factory=list)


class LegalConceptExploration(BaseModel):
    """Comprehensive 5-level explanation and drill-down repository for a legal concept."""
    concept_name: str
    jurisdiction: str = "US"
    situational_context: Optional[str] = None
    
    # The 5 progressive levels
    level_1_plain_english: str = Field(..., description="Level 1: Plain English, intuitive, accessible, no false simplicity")
    level_2_practical: str = Field(..., description="Level 2: Practical explanation of how it operates in real life / situation")
    level_3_terminology: str = Field(..., description="Level 3: Precise legal terminology, doctrines, and doctrinal distinctions")
    level_4_primary_authority: List[PrimaryAuthorityReference] = Field(default_factory=list, description="Level 4: Verified primary authorities")
    level_5_advanced_analysis: str = Field(..., description="Level 5: Competing doctrines, historical tensions, standards of review")

    # The 5 pre-computed or dynamically queried drill-downs
    drill_downs: Dict[DrillDownAction, DrillDownResult] = Field(default_factory=dict)
