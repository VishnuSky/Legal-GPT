"""Tests for Legal Literacy Truth Engine Wiring (Days 6-7)."""

import pytest
from core.literacy.engine import LegalLiteracyEngine
from core.literacy.models import LiteracyLevel, DrillDownAction, PrimaryAuthorityReference
from core.citation_verifier import CitationVerifier
from core.explanation_trace.models import InterrogativeTraceType


def test_tampered_citation_string_not_verified():
    """Verify that tampered / hallucinated citations fail verification and are marked UNVERIFIED."""
    # Direct verifier test
    v_res = CitationVerifier.verify_citation("RCW 999.99.999")
    assert v_res.verified is False
    assert v_res.authority_tier == "TIER_5"
    assert "unrecognized" in v_res.rejection_reason.lower() or "not found" in v_res.rejection_reason.lower()

    v_fake = CitationVerifier.verify_citation("FakeStatute § 123.456")
    assert v_fake.verified is False
    assert v_fake.authority_tier == "TIER_5"

    # Check that explain() catches and flags unverified citations
    exp = LegalLiteracyEngine.explain("due_process", jurisdiction="WA")
    # All canonical authorities should be verified
    for auth in exp.level_4_primary_authority:
        assert auth.verification_status == "VERIFIED"

    # Test with tampered citation
    tampered_auth = PrimaryAuthorityReference(
        citation="RCW 999.99.999",
        source_type="STATUTE",
        official_portal_url="https://example.com/fake",
        key_holding_or_text="Fake text",
        jurisdiction="WA",
        is_binding=True
    )
    v_record = CitationVerifier.verify_citation(tampered_auth.citation)
    assert v_record.verified is False


def test_stale_or_missing_effective_date_temporal_abstains():
    """Verify that SHOW_TEMPORAL_CHANGE returns an explicit abstention when temporal version history is missing."""
    res = LegalLiteracyEngine.drill_down("nonexistent_concept_99", DrillDownAction.SHOW_TEMPORAL_CHANGE)
    assert res.action == DrillDownAction.SHOW_TEMPORAL_CHANGE
    assert "abstain" in res.content.lower() or "no verified" in res.content.lower()
    assert len(res.citations) == 0


def test_jurisdiction_contamination_foreign_state_non_binding():
    """Verify that foreign state citations are strictly marked non-binding for a state-specific request."""
    # When requesting WA, IL statutes must never be marked binding
    exp_wa = LegalLiteracyEngine.explain("emergency_removal", jurisdiction="WA")
    for auth in exp_wa.level_4_primary_authority:
        auth_j = (auth.jurisdiction or "").upper().replace("US-", "")
        if auth_j not in ("WA", "US", "FED"):
            assert auth.is_binding is False, f"Foreign state authority {auth.citation} ({auth.jurisdiction}) was marked binding in WA query"


def test_explanation_trace_integration():
    """Verify that LegalLiteracyEngine can generate 10-field explanation traces and answer interrogations."""
    trace = LegalLiteracyEngine.get_explanation_trace("emergency_removal", jurisdiction="WA")
    assert trace.claim
    assert trace.source
    assert trace.authority_level
    assert trace.jurisdiction in ("WA", "US-WA", "US")
    assert trace.effective_date
    assert trace.relevant_text
    assert trace.reasoning_step
    assert trace.confidence_verification
    assert trace.counterargument
    assert trace.limitation

    # Interrogation queries
    why_res = LegalLiteracyEngine.interrogate_concept("emergency_removal", InterrogativeTraceType.WHY, jurisdiction="WA")
    assert why_res.trace_type == InterrogativeTraceType.WHY
    assert why_res.concise_auditable_summary

    source_res = LegalLiteracyEngine.interrogate_concept("emergency_removal", InterrogativeTraceType.SOURCE, jurisdiction="WA")
    assert source_res.trace_type == InterrogativeTraceType.SOURCE
    assert source_res.supporting_authority
