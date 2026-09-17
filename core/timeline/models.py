"""Data models for the Legal-GPT Timeline Construction Engine."""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class EventCategory(str, Enum):
    INVESTIGATION = "INVESTIGATION"
    REMOVAL = "REMOVAL"
    PETITION = "PETITION"
    HEARING = "HEARING"
    ORDER = "ORDER"
    SERVICE = "SERVICE"
    VISITATION = "VISITATION"
    MOTION = "MOTION"
    CONFERENCE = "CONFERENCE"
    DISPOSITION = "DISPOSITION"
    TERMINATION = "TERMINATION"
    OTHER = "OTHER"


class SequenceFlag(str, Enum):
    NORMAL = "NORMAL"
    OUT_OF_SEQUENCE = "OUT_OF_SEQUENCE"
    MISSING_REQUIRED_EVENT = "MISSING_REQUIRED_EVENT"
    DEADLINE_EXCEEDED = "DEADLINE_EXCEEDED"
    JURISDICTION_SHIFT = "JURISDICTION_SHIFT"
    GAP_DETECTED = "GAP_DETECTED"


class TimelineEvent(BaseModel):
    """An individual event on a legal timeline."""
    id: str = Field(..., description="Unique event identifier or UUID")
    date: str = Field(..., description="Event date (ISO 8601 YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
    title: str = Field(..., description="Short summary of event")
    description: str = Field("", description="Detailed factual description (metadata only, no PII)")
    category: str = Field(EventCategory.OTHER.value, description="Event classification")
    jurisdiction: Optional[str] = Field(None, description="Controlling jurisdiction code (e.g. 'WA', 'TX')")
    source_document: Optional[str] = Field(None, description="Metadata reference to document type")
    participants: List[str] = Field(default_factory=list, description="Roles involved (e.g. 'Caseworker', 'Judge')")
    flags: List[str] = Field(default_factory=list, description="Detected procedural warnings or defects")
    notes: Optional[str] = Field(None, description="Explanatory procedural notes")


class TimelineRequest(BaseModel):
    """Request payload for constructing and analyzing a legal timeline."""
    events: List[TimelineEvent] = Field(..., description="List of raw or unordered events")
    default_jurisdiction: Optional[str] = Field("US", description="Default state or federal jurisdiction")
    case_type: Optional[str] = Field("cps_dependency", description="'cps_dependency', 'criminal', 'civil', or 'general'")


class ProceduralIssue(BaseModel):
    """A procedural defect, missing milestone, or timing anomaly detected on the timeline."""
    issue_type: str = Field(..., description="e.g. 'MISSING_SHELTER_HEARING', 'OUT_OF_SEQUENCE_ADJUDICATION'")
    severity: str = Field("WARNING", description="'CRITICAL', 'WARNING', or 'INFORMATIONAL'")
    description: str = Field(..., description="Specific statutory explanation of the procedural defect")
    affected_events: List[str] = Field(default_factory=list, description="IDs of related events")
    governing_authority: Optional[str] = Field(None, description="Controlling statutory citation or court rule")


class TimelineReport(BaseModel):
    """Complete chronological timeline analysis report."""
    total_events: int
    chronological_events: List[TimelineEvent] = Field(default_factory=list)
    detected_issues: List[ProceduralIssue] = Field(default_factory=list)
    jurisdictions_involved: List[str] = Field(default_factory=list)
    has_jurisdiction_shift: bool = False
    procedural_compliance_score: float = 1.0
    summary: str = ""
