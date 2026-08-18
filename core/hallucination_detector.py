"""Proposition vs Authority Verification Engine (Hallucination Detector)."""

from typing import List
from pydantic import BaseModel
from core.citation_verifier import CitationVerifier, CitationVerificationRecord


class LegalPropositionCheck(BaseModel):
    proposition: str
    asserted_citation: str
    verification_record: CitationVerificationRecord
    passed: bool
    notes: str


class HallucinationDetector:
    @classmethod
    def audit_response(cls, response_text: str) -> List[LegalPropositionCheck]:
        """Audits generated response to ensure every asserted citation is legally valid and verified."""
        all_passed, records = CitationVerifier.verify_all_citations(response_text)
        checks = []

        for record in records:
            passed = record.verified and record.authority_tier in ("TIER_0", "TIER_1", "TIER_2", "TIER_3")
            note = "Verified authority" if passed else (record.rejection_reason or "Unverified authority tier")
            checks.append(LegalPropositionCheck(
                proposition="Asserted legal citation",
                asserted_citation=record.normalized_citation,
                verification_record=record,
                passed=passed,
                notes=note
            ))

        return checks
