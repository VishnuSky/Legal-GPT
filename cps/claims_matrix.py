"""Legal Claims & Evidence Matrix: Maps Facts, Allegations, Evidence, and Controlling Authority."""

from datetime import date
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field


class CaseItem(BaseModel):
    item_id: str
    item_type: Literal["FACT", "ALLEGATION", "ASSERTION", "DOCUMENTED_EXHIBIT", "DISPUTED", "COURT_FINDING"]
    description: str
    source_document: Optional[str] = None # e.g. "CPS Report #47", "Police Incident Report", "Parent Text Msg"
    date_occurred: Optional[date] = None
    party: str # e.g. "CPS Investigator", "Mother", "Father", "Caseworker", "GAL"
    corroborated: bool = False
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class LegalClaimRecord(BaseModel):
    claim_id: str
    claim_name: str # e.g. "Failure to provide timely 72-hour notice", "Lack of Reasonable Efforts"
    associated_items: List[CaseItem] = Field(default_factory=list)
    controlling_authority: List[str] = Field(default_factory=list) # e.g. ["RCW 13.34.065", "42 U.S.C. § 671"]
    counterarguments: List[str] = Field(default_factory=list)
    status: Literal["SUPPORTED", "DISPUTED", "REQUIRES_REVIEW", "INSUFFICIENT_EVIDENCE"] = "REQUIRES_REVIEW"
    required_next_steps: List[str] = Field(default_factory=list)


class ClaimsMatrix:
    def __init__(self):
        self.items: List[CaseItem] = []
        self.claims: List[LegalClaimRecord] = []

    def add_item(self, item: CaseItem):
        self.items.append(item)

    def add_claim(self, claim: LegalClaimRecord):
        self.claims.append(claim)

    def get_summary_table(self) -> List[Dict[str, Any]]:
        summary = []
        for claim in self.claims:
            summary.append({
                "claim_id": claim.claim_id,
                "claim_name": claim.claim_name,
                "authorities": ", ".join(claim.controlling_authority),
                "status": claim.status,
                "evidence_count": len(claim.associated_items),
                "next_steps": "; ".join(claim.required_next_steps),
            })
        return summary
