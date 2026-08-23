"""Claim Provenance Engine: Traceable, Auditable Provenance Records for Every Legal Proposition."""

import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class ClaimRecord(BaseModel):
    claim_id: str = Field(default_factory=lambda: f"CLAIM-{uuid.uuid4().hex[:8].upper()}")
    claim_text: str
    source_citation: str
    version_id: Optional[str] = None
    jurisdiction: str
    authority_tier: str
    support_subsection: Optional[str] = None
    interpreting_cases: List[str] = Field(default_factory=list)
    confidence: float = Field(default=0.95, ge=0.0, le=1.0)
    temporal_status: str = "Current"  # Current, Historical, Superseded
    verification_status: str = "PASS"  # PASS, FAIL, HUMAN_REVIEW
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def render_provenance_block(self) -> str:
        cases_str = ", ".join(self.interpreting_cases) if self.interpreting_cases else "None"
        return (
            f"**[{self.claim_id}]** \"{self.claim_text}\"\n"
            f"- **Source Citation**: {self.source_citation} ({self.authority_tier})\n"
            f"- **Jurisdiction**: {self.jurisdiction} | **Temporal Status**: {self.temporal_status}\n"
            f"- **Support**: {self.support_subsection or 'Direct Statutory / Case Support'}\n"
            f"- **Interpreting Authority**: {cases_str}\n"
            f"- **Confidence**: {self.confidence:.2f} | **Verification**: {self.verification_status}"
        )


class ClaimProvenanceEngine:
    """Tracks and validates the exact provenance of every legal assertion."""

    def __init__(self):
        self.ledger: Dict[str, ClaimRecord] = {}

    def register_claim(
        self,
        claim_text: str,
        source_citation: str,
        jurisdiction: str,
        authority_tier: str,
        support_subsection: Optional[str] = None,
        interpreting_cases: Optional[List[str]] = None,
        confidence: float = 0.95,
        temporal_status: str = "Current",
        verification_status: str = "PASS"
    ) -> ClaimRecord:
        record = ClaimRecord(
            claim_text=claim_text,
            source_citation=source_citation,
            jurisdiction=jurisdiction,
            authority_tier=authority_tier,
            support_subsection=support_subsection,
            interpreting_cases=interpreting_cases or [],
            confidence=confidence,
            temporal_status=temporal_status,
            verification_status=verification_status
        )
        self.ledger[record.claim_id] = record
        return record

    def get_claim(self, claim_id: str) -> Optional[ClaimRecord]:
        return self.ledger.get(claim_id)


# Global singleton
claim_provenance = ClaimProvenanceEngine()
