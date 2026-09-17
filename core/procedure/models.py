"""Data models and schemas for the Legal-GPT Procedural Pathway Engine."""

from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class LegalTrack(str, Enum):
    """The four major procedural tracks supported by the engine."""
    CPS_DEPENDENCY = "CPS_DEPENDENCY"
    ADMINISTRATIVE = "ADMINISTRATIVE"
    CRIMINAL = "CRIMINAL"
    CIVIL_LITIGATION = "CIVIL_LITIGATION"


class StageDefinition(BaseModel):
    """Definition of a discrete procedural stage within a legal track."""
    stage_id: str
    track: LegalTrack
    stage_name: str
    order: int
    description: str
    governing_authority: List[str] = Field(default_factory=list)
    possible_next_stages: List[str] = Field(default_factory=list)
    statutory_deadlines: List[str] = Field(default_factory=list)
    notice_requirements: List[str] = Field(default_factory=list)
    hearing_opportunities: List[str] = Field(default_factory=list)
    decision_makers: List[str] = Field(default_factory=list)
    review_mechanisms: List[str] = Field(default_factory=list)
    critical_documents_to_locate: List[str] = Field(default_factory=list)
    questions_to_ask: List[str] = Field(default_factory=list)
    required_factual_predicates: List[str] = Field(default_factory=list)
    unknown_facts_to_investigate: List[str] = Field(default_factory=list)


class ProceduralPathwayInput(BaseModel):
    """Input payload for the Procedural Pathway Engine."""
    narrative: str
    jurisdiction: str = "US"
    track: Optional[LegalTrack] = None
    current_stage_hint: Optional[str] = None
    facts: List[str] = Field(default_factory=list)
    event_date: Optional[date] = None


class ProceduralPathwayReport(BaseModel):
    """Comprehensive, non-predictive procedural pathway report."""
    track: LegalTrack
    jurisdiction: str
    current_stage: StageDefinition
    possible_next_stages: List[StageDefinition] = Field(default_factory=list)
    authority: List[str] = Field(default_factory=list)
    required_verification: List[str] = Field(default_factory=list)
    important_dates: List[Dict[str, Any]] = Field(default_factory=list)
    questions_to_ask: List[str] = Field(default_factory=list)
    documents_to_locate: List[str] = Field(default_factory=list)
    available_review_mechanisms: List[str] = Field(default_factory=list)
    unknown_facts: List[str] = Field(default_factory=list)
    epistemic_notice: str = (
        "NON-PREDICTIVE PROCEDURAL NOTICE: This report identifies procedural stages, source-backed statutory deadlines, "
        "hearing rights, and challenge mechanisms recognized under governing law. Legal-GPT does NOT predict case outcomes, "
        "judicial rulings, or probabilities of success. Determining the legal result of any stage requires formal judicial "
        "adjudication upon admissible evidence and advocacy by qualified legal counsel."
    )

    def render_markdown(self) -> str:
        """Renders the report in structured Markdown format."""
        from core.procedure.renderer import ProceduralReportRenderer
        return ProceduralReportRenderer.render_markdown(self)
