"""Jurisdiction and interstate custody conflict analyzer (UCCJEA / PKPA)."""

from typing import List, Optional
from pydantic import BaseModel


class JurisdictionConflictReport(BaseModel):
    conflict_detected: bool
    state_a: str
    state_b: str
    home_state: Optional[str]
    emergency_state: Optional[str]
    analysis: str


class JurisdictionConflictAnalyzer:
    """Detects interstate custody conflicts under UCCJEA Sections 201 & 204."""

    @classmethod
    def evaluate(cls, child_home_state: str, filing_state: str, is_emergency: bool) -> JurisdictionConflictReport:
        if child_home_state != filing_state:
            if is_emergency:
                return JurisdictionConflictReport(
                    conflict_detected=True,
                    state_a=child_home_state,
                    state_b=filing_state,
                    home_state=child_home_state,
                    emergency_state=filing_state,
                    analysis=(
                        f"UCCJEA INTERSTATE CONFLICT: {child_home_state} is the statutory Home State (§ 201). "
                        f"{filing_state} holds ONLY Temporary Emergency Jurisdiction (§ 204), and must communicate "
                        f"immediately with the court in {child_home_state} to resolve long-term custody."
                    )
                )
            else:
                return JurisdictionConflictReport(
                    conflict_detected=True,
                    state_a=child_home_state,
                    state_b=filing_state,
                    home_state=child_home_state,
                    emergency_state=None,
                    analysis=f"UCCJEA JURISDICTIONAL DEFECT: {filing_state} lacks Home State jurisdiction. Exclusive initial jurisdiction resides in {child_home_state}."
                )

        return JurisdictionConflictReport(
            conflict_detected=False,
            state_a=child_home_state,
            state_b=filing_state,
            home_state=child_home_state,
            emergency_state=None,
            analysis="No interstate conflict detected. Filing state is the established Home State."
        )
