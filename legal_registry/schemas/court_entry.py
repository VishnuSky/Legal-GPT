"""Pydantic schemas for Court Registry entries."""

from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class CourtEntry(BaseModel):
    court_id: str = Field(..., description="Unique ID e.g. WA-SKAGIT-SUPERIOR, FED-SCOTUS, FED-9TH-CIR")
    name: str
    jurisdiction: str = Field(..., description="US, US-WA, US-IL, US-OH, etc.")
    state: Optional[str] = None
    county: Optional[str] = None
    level: Literal["supreme", "appellate", "trial", "specialized_juvenile", "specialized_family", "tribal", "bankruptcy", "federal_district"]
    court_type: Literal["state_supreme", "state_appellate", "state_superior", "state_circuit", "county_court", "juvenile_dependency", "family_court", "federal_supreme", "federal_circuit", "federal_district", "tribal_court"]
    official_url: str
    opinions_url: Optional[str] = None
    local_rules_url: Optional[str] = None
    forms_url: Optional[str] = None
    courtlistener_id: Optional[str] = None
    citation_abbreviation: Optional[str] = None
    cps_jurisdiction: bool = False
    active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
