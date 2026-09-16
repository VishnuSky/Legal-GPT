"""Temporal law conflict analyzer: Ex Post Facto, Repeals, Amendments, Point-in-Time Applicability."""

from datetime import date
from typing import Optional
from pydantic import BaseModel


class TemporalConflictReport(BaseModel):
    conflict_detected: bool
    event_date: str
    effective_date: Optional[str]
    repealed_date: Optional[str]
    is_valid_at_date: bool
    analysis: str


class TemporalConflictAnalyzer:
    """Evaluates whether an amendment, repeal, or future effective date creates an ex post facto or temporal applicability conflict."""

    @classmethod
    def evaluate(cls, event_date_str: str, effective_date_str: Optional[str], repealed_date_str: Optional[str]) -> TemporalConflictReport:
        e_date = date.fromisoformat(event_date_str)
        eff_date = date.fromisoformat(effective_date_str) if effective_date_str else None
        rep_date = date.fromisoformat(repealed_date_str) if repealed_date_str else None

        if eff_date and e_date < eff_date:
            return TemporalConflictReport(
                conflict_detected=True,
                event_date=event_date_str,
                effective_date=effective_date_str,
                repealed_date=repealed_date_str,
                is_valid_at_date=False,
                analysis=f"TEMPORAL CONFLICT: Event occurred on {event_date_str}, before statutory effective date {effective_date_str}. Applying future statute violates retroactivity rules."
            )

        if rep_date and e_date >= rep_date:
            return TemporalConflictReport(
                conflict_detected=True,
                event_date=event_date_str,
                effective_date=effective_date_str,
                repealed_date=repealed_date_str,
                is_valid_at_date=False,
                analysis=f"TEMPORAL CONFLICT: Statute was repealed on {repealed_date_str} prior to event date {event_date_str}."
            )

        return TemporalConflictReport(
            conflict_detected=False,
            event_date=event_date_str,
            effective_date=effective_date_str,
            repealed_date=repealed_date_str,
            is_valid_at_date=True,
            analysis="Statute is temporally valid and in full legal effect on the operative event date."
        )
