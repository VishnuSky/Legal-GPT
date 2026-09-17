"""Unresolved legal conflict surfacing and mandatory explicit disclosure."""

from typing import List, Optional
from pydantic import BaseModel


class UnresolvedConflictDisclosure(BaseModel):
    is_unresolved: bool
    unresolved_point: str
    competing_theories: List[str]
    statutory_silence_or_split: str
    abstention_recommendation: str


class UnresolvedConflictEngine:
    """Surfaces questions of first impression, statutory ambiguity, and circuit splits where no consensus exists."""

    @classmethod
    def disclose(cls, topic: str, theory_a: str, theory_b: str) -> UnresolvedConflictDisclosure:
        return UnresolvedConflictDisclosure(
            is_unresolved=True,
            unresolved_point=f"Unresolved legal question on: {topic}",
            competing_theories=[
                f"Theory A: {theory_a}",
                f"Theory B: {theory_b}"
            ],
            statutory_silence_or_split="Open split of judicial authority / Novel issue of statutory interpretation.",
            abstention_recommendation="Model must explicitly disclose split of authority and refrain from inventing a definitive ruling."
        )
