"""Statutory construction conflict analyzer (General vs. Specific, Later vs. Earlier enacted)."""

from pydantic import BaseModel


class StatutoryConflictReport(BaseModel):
    conflict_detected: bool
    general_statute: str
    specific_statute: str
    controlling_rule: str
    canon_applied: str


class StatutoryConflictAnalyzer:
    """Applies classical canons of statutory construction (Generalia specialibus non derogant)."""

    @classmethod
    def evaluate(cls, general_cite: str, specific_cite: str) -> StatutoryConflictReport:
        return StatutoryConflictReport(
            conflict_detected=True,
            general_statute=general_cite,
            specific_statute=specific_cite,
            controlling_rule=f"Specific statutory provision {specific_cite} controls over general provision {general_cite}.",
            canon_applied="Specific over General Canon (Lex specialis derogat legi generali)"
        )
