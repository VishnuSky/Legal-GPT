"""Typed Safe Handoff Contract for Grok, Local Models, and Orchestration."""

from datetime import date
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field
from core.citation_verifier import CitationVerifier, CitationVerificationRecord
from core.jurisdiction import JurisdictionEngine, JurisdictionContext


class VerifiedSourceReference(BaseModel):
    """Immutable authoritative legal source passed to model as grounding context."""
    citation: str
    authority_tier: str = "TIER_0"
    jurisdiction: str = "US"
    authority_layer: str = "FEDERAL"  # FEDERAL, STATE, TRIBAL, TREATY
    source_url: Optional[str] = None
    publisher_name: str = "Official Legal Registry"
    verified: bool = True
    key_holding_or_text: Optional[str] = None


class HandoffVerificationResult(BaseModel):
    """Result of post-generation verification gating. Models cannot self-certify."""
    passed: bool
    verified_citations: List[str] = Field(default_factory=list)
    unverified_citations: List[str] = Field(default_factory=list)
    contamination_warnings: List[str] = Field(default_factory=list)
    abstention_triggered: bool = False
    abstention_reason: Optional[str] = None
    sanitized_text: str


class SafeHandoffContract(BaseModel):
    """Strict typed handoff object containing only the fields required for the reasoning task."""
    task_id: str
    jurisdiction: str
    relevant_date: Optional[date] = None
    task_type: Literal[
        "statutory_lookup",
        "concept_explanation",
        "service_routing",
        "procedural_deadlines",
        "adversarial_review",
        "case_analysis"
    ]
    verified_sources: List[VerifiedSourceReference] = Field(default_factory=list)
    candidate_claims: List[str] = Field(default_factory=list)
    uncertainty_and_missing_facts: List[str] = Field(default_factory=list)
    requested_output_schema: Dict[str, Any] = Field(default_factory=dict)
    allow_unverified_citations: bool = False
    abstention_prompt_required: bool = True

    def build_prompt_messages(self) -> List[Dict[str, str]]:
        """Constructs a strictly grounded prompt with clear negative constraints and abstention rules."""
        sources_block = []
        for i, s in enumerate(self.verified_sources, 1):
            sources_block.append(
                f"[{i}] {s.citation} (Jurisdiction: {s.jurisdiction}, Layer: {s.authority_layer}, Tier: {s.authority_tier})\n"
                f"Text: {s.key_holding_or_text or 'Authoritative primary statutory/precedent text'}"
            )
        sources_text = "\n\n".join(sources_block) if sources_block else "NO_VERIFIED_PRIMARY_SOURCES_RETRIEVED"

        missing_block = "\n".join(f"- {m}" for m in self.uncertainty_and_missing_facts) if self.uncertainty_and_missing_facts else "None recorded."
        claims_block = "\n".join(f"- {c}" for c in self.candidate_claims) if self.candidate_claims else "None recorded."

        system_msg = (
            f"You are a jurisdiction-locked legal analysis agent operating strictly under {self.jurisdiction}.\n"
            "MANDATORY OPERATIONAL CONSTRAINTS:\n"
            "1. Ground all analysis exclusively in the provided VERIFIED PRIMARY SOURCES below.\n"
            "2. DO NOT invent citations, court rules, statutes, or tribal procedures.\n"
            "3. If verified sources are missing or insufficient to answer, state: 'ABSTAIN: Insufficient controlling authority.'\n"
            "4. Never declare that an individual's rights were violated. Present standard of proof and procedural standards.\n"
            "5. Distinguish clearly between Federal law, State law overlays, and sovereign Tribal Nation codes.\n"
            "6. You CANNOT promote your own output to 'VERIFIED' status; verification is exclusively performed by Legal-GPT's registry."
        )

        user_msg = (
            f"TASK IDENTIFIER: {self.task_id}\n"
            f"TASK TYPE: {self.task_type}\n"
            f"JURISDICTION: {self.jurisdiction}\n"
            f"RELEVANT DATE: {self.relevant_date or 'Present'}\n\n"
            f"VERIFIED PRIMARY SOURCES:\n{sources_text}\n\n"
            f"CANDIDATE CLAIMS UNDER REVIEW:\n{claims_block}\n\n"
            f"KNOWN UNCERTAINTIES & MISSING FACTS:\n{missing_block}\n\n"
            "Provide your structured procedural analysis, citing only the verified authorities provided."
        )

        return [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]

    def validate_model_output(self, response_text: str) -> HandoffVerificationResult:
        """Enforces zero-hallucination verification gating.

        No model output can self-certify authority as VERIFIED.
        Every citation is tested against the deterministic registry.
        """
        # 1. Check for prompt injection attempt or fabricated self-promotion
        cleaned_text = response_text
        if "[SYSTEM OVERRIDE]" in response_text or "IGNORE PREVIOUS INSTRUCTIONS" in response_text.upper():
            return HandoffVerificationResult(
                passed=False,
                abstention_triggered=True,
                abstention_reason="Prompt injection detected in model output.",
                sanitized_text="ABSTAIN: Prompt injection attempt detected and rejected."
            )

        # 2. Extract citations
        citations = CitationVerifier.extract_citations(response_text)

        # 3. Cross-jurisdiction contamination check
        is_tribal = "TRIBAL" in self.jurisdiction.upper()
        ctx = JurisdictionEngine.lock_jurisdiction(
            state=self.jurisdiction,
            is_tribal=is_tribal,
            tribe_name=self.jurisdiction.replace("TRIBAL-", "") if is_tribal else None
        )
        contamination_errors = JurisdictionEngine.detect_cross_contamination(ctx, citations)

        # 4. Verify citations against canonical registry
        verified_cites = []
        unverified_cites = []
        for c in citations:
            rec: CitationVerificationRecord = CitationVerifier.verify_citation(c)
            if rec.verified:
                verified_cites.append(rec.normalized_citation)
            else:
                unverified_cites.append(c)

        # 5. Determine whether output passed
        if unverified_cites and not self.allow_unverified_citations:
            return HandoffVerificationResult(
                passed=False,
                verified_citations=verified_cites,
                unverified_citations=unverified_cites,
                contamination_warnings=contamination_errors,
                abstention_triggered=True,
                abstention_reason=f"Model proposed unverified citation(s): {', '.join(unverified_cites)}",
                sanitized_text=f"ABSTAIN: The generated output referenced unverified authority ({', '.join(unverified_cites)})."
            )

        if contamination_errors:
            return HandoffVerificationResult(
                passed=False,
                verified_citations=verified_cites,
                unverified_citations=unverified_cites,
                contamination_warnings=contamination_errors,
                abstention_triggered=True,
                abstention_reason=f"Jurisdiction cross-contamination: {'; '.join(contamination_errors)}",
                sanitized_text=f"ABSTAIN: Cross-jurisdiction conflict detected ({'; '.join(contamination_errors)})."
            )

        return HandoffVerificationResult(
            passed=True,
            verified_citations=verified_cites,
            unverified_citations=[],
            contamination_warnings=[],
            abstention_triggered=False,
            abstention_reason=None,
            sanitized_text=cleaned_text
        )
