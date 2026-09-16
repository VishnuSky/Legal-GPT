"""Final Review Agent: Inspects, validates, and gates generated legal responses.

This agent operates strictly as a validation and safety filter. It does NOT generate new legal authority.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from core.jurisdiction import JurisdictionEngine
from core.citation_verifier import CitationVerifier
from core.proposition_verifier import PropositionVerifier, PropositionStatus


class FinalReviewVerdict(BaseModel):
    is_approved: bool
    verified_citations: List[str]
    rejected_citations: List[str]
    jurisdiction_safe: bool
    hallucination_detected: bool
    epistemic_safety_passed: bool
    actionable_warnings: List[str] = Field(default_factory=list)


class FinalReviewAgent:
    """Final gatekeeper inspecting responses before delivery."""

    @classmethod
    def review_response(
        cls,
        jurisdiction: str,
        citations: List[str],
        response_text: str,
        allow_unverified: bool = False
    ) -> FinalReviewVerdict:
        verified = []
        rejected = []
        warnings = []

        for c in citations:
            if CitationVerifier.verify_citation(c):
                verified.append(c)
            else:
                rejected.append(c)
                warnings.append(f"Rejected unverified citation: {c}")

        # Check jurisdiction contamination
        alien_cites = JurisdictionEngine.filter_out_of_jurisdiction_citations(citations, jurisdiction)
        jurisdiction_safe = len(alien_cites) == 0
        if not jurisdiction_safe:
            warnings.append(f"Jurisdiction contamination detected: {alien_cites} found in {jurisdiction} context.")

        # Epistemic safety
        has_disclaimer = "legal advice" in response_text.lower() or "research" in response_text.lower() or "disclaimer" in response_text.lower()
        if not has_disclaimer:
            warnings.append("Disclaimer missing in generated response.")

        is_approved = (len(rejected) == 0 or allow_unverified) and jurisdiction_safe

        return FinalReviewVerdict(
            is_approved=is_approved,
            verified_citations=verified,
            rejected_citations=rejected,
            jurisdiction_safe=jurisdiction_safe,
            hallucination_detected=len(rejected) > 0,
            epistemic_safety_passed=has_disclaimer,
            actionable_warnings=warnings
        )
