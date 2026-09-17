"""Pydantic data models for the Legal-GPT Deadline Engine."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Deadline(BaseModel):
    """A specific calculated legal deadline anchored in authoritative law."""
    name: str = Field(..., description="Name of the procedural milestone or required action")
    due_date: str = Field(..., description="ISO date (YYYY-MM-DD) or 'UNKNOWN'")
    authority: str = Field(..., description="Governing statutory title or procedural rule")
    citation: str = Field(..., description="Pinpoint statutory or court rule citation")
    calendar_or_court_days: str = Field(..., description="'calendar_days', 'court_days', 'hours', or 'UNKNOWN'")
    notes: str = Field("", description="Explanatory computation notes or holiday rules")
    verification_status: str = Field("VERIFIED", description="'VERIFIED', 'PROVISIONAL', or 'UNKNOWN_AUTHORITY_GAP'")


class DeadlineRequest(BaseModel):
    """Input payload for deadline calculation."""
    event_type: str = Field(..., description="e.g. 'emergency_removal', 'petition_filed', 'speedy_trial'")
    event_date: str = Field(..., description="ISO 8601 event date string (YYYY-MM-DD)")
    jurisdiction: str = Field(..., description="Controlling jurisdiction code (e.g. 'US-WA', 'IL', 'US')")
    county: Optional[str] = Field(None, description="Optional county or local court district")


class DeadlineReport(BaseModel):
    """Structured report containing calculated deadlines and authority sources."""
    event_type: str
    event_date: str
    jurisdiction: str
    county: Optional[str] = None
    deadlines: List[Deadline] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    is_known_event: bool = True
    error: Optional[str] = None
