"""Jurisdiction Lock, Routing, and Contamination Detector."""

from typing import List, Optional, Set
from pydantic import BaseModel, Field


class JurisdictionContext(BaseModel):
    primary_state: Optional[str] = None # e.g. "WA", "IL", "OH"
    county: Optional[str] = None # e.g. "Skagit", "Cook", "Cuyahoga"
    court_level: Optional[str] = None # e.g. "juvenile_dependency", "superior", "appellate"
    federal_district: Optional[str] = None
    is_tribal_matter: bool = False
    tribe_name: Optional[str] = None
    is_interstate: bool = False
    secondary_states: List[str] = Field(default_factory=list)
    locked: bool = False


class JurisdictionEngine:
    STATE_CITATION_PREFIXES = {
        "WA": ["RCW", "WAC", "Wn.2d", "Wn. App.", "Washington"],
        "IL": ["ILCS", "Ill. Adm. Code", "Ill. S. Ct.", "IL App", "Illinois"],
        "OH": ["ORC", "OAC", "Ohio St.3d", "Ohio App.", "Ohio Juv. R.", "Ohio"],
        "CA": ["Cal.", "Cal. App.", "Cal. Civ. Code", "Cal. Welf. & Inst. Code", "California"],
        "NY": ["N.Y.", "N.Y.S.", "NY CLS", "New York"],
        "TX": ["Tex.", "Tex. Fam. Code", "Texas"],
        "US": ["U.S.C.", "C.F.R.", "U.S.", "F.4th", "F.3d", "F. Supp.", "Fed. Reg."],
    }

    @classmethod
    def lock_jurisdiction(cls, state: str, county: Optional[str] = None, is_tribal: bool = False) -> JurisdictionContext:
        state_code = state.strip().upper()
        return JurisdictionContext(
            primary_state=state_code,
            county=county,
            is_tribal_matter=is_tribal,
            locked=True
        )

    @classmethod
    def detect_cross_contamination(cls, context: JurisdictionContext, citations: List[str]) -> List[str]:
        """Detects if citations from other non-applicable state jurisdictions are erroneously included."""
        if not context.locked or not context.primary_state:
            return []

        violations = []
        target_state = context.primary_state

        for cite in citations:
            for other_state, prefixes in cls.STATE_CITATION_PREFIXES.items():
                if other_state in (target_state, "US"):
                    continue # Federal is always potentially applicable
                if other_state in context.secondary_states:
                    continue # Allowed if explicitly multi-state matter
                for prefix in prefixes:
                    if prefix in cite:
                        violations.append(
                            f"Contamination error: Citation '{cite}' belongs to {other_state}, but jurisdiction is locked to {target_state}."
                        )
                        break

        return violations
