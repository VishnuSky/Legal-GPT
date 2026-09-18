"""Tests for Legal Literacy Model contract adherence (Days 1-2)."""

import pytest
from core.literacy.engine import LegalLiteracyEngine
from core.literacy.models import (
    LiteracyLevel,
    DrillDownAction,
    PrimaryAuthorityReference,
    LegalConceptExploration,
)


def test_missing_jurisdiction_returns_unknown():
    """Missing jurisdiction must return JURISDICTION_UNKNOWN, not default silently to US-as-WA."""
    exp = LegalLiteracyEngine.explain("Due Process", jurisdiction=None)
    assert exp.jurisdiction == "JURISDICTION_UNKNOWN"

    exp_empty = LegalLiteracyEngine.explain("Due Process", jurisdiction="")
    assert exp_empty.jurisdiction == "JURISDICTION_UNKNOWN"


def test_unverified_concept_status_not_verified():
    """Unverified concept must have verification_status != VERIFIED and empty Level 4."""
    exp = LegalLiteracyEngine.explain("quantum_custody_doctrine", jurisdiction="WA")
    assert exp.verification_status != "VERIFIED"
    assert exp.verification_status in ("ABSTAIN", "UNVERIFIED")
    assert len(exp.level_4_primary_authority) == 0
    assert exp.abstention_reason is not None
    assert "No verified" in exp.abstention_reason or "authority" in exp.abstention_reason


def test_wrong_state_statute_in_wa_request_is_not_binding():
    """Foreign state authorities (e.g. NY or IL in WA request) must be marked is_binding=False."""
    exp = LegalLiteracyEngine.explain("warrant requirement", jurisdiction="WA")
    for auth in exp.level_4_primary_authority:
        clean_j = (auth.jurisdiction or "").upper().replace("US-", "")
        if clean_j not in ("WA", "US", "FED"):
            assert auth.is_binding is False, (
                f"Authority '{auth.citation}' with jurisdiction '{auth.jurisdiction}' was incorrectly marked binding for WA request."
            )


def test_level_4_authority_reference_contract_fields():
    """Verify all Level 4 authorities adhere to schema fields."""
    exp = LegalLiteracyEngine.explain("Due Process", jurisdiction="WA")
    assert len(exp.level_4_primary_authority) > 0

    valid_source_types = {"CONSTITUTION", "STATUTE", "REGULATION", "CASELAW", "COURT_RULE", "POLICY"}

    for auth in exp.level_4_primary_authority:
        assert isinstance(auth.citation, str) and len(auth.citation) > 0
        assert auth.source_type in valid_source_types
        assert auth.official_portal_url.startswith("http://") or auth.official_portal_url.startswith("https://")
        assert len(auth.key_holding_or_text) > 0
        assert isinstance(auth.is_binding, bool)
        assert auth.verification_status in ("VERIFIED", "UNVERIFIED", "ABSTAIN")


def test_concept_exploration_contract_fields():
    """Verify LegalConceptExploration contract includes disclaimer, verification status, and related concepts."""
    exp = LegalLiteracyEngine.explain("Due Process", jurisdiction="WA")
    assert exp.verification_status in ("VERIFIED", "PARTIAL", "UNVERIFIED", "ABSTAIN")
    assert exp.disclaimer == "Legal information only. Not legal advice. Not a lawyer."
    assert isinstance(exp.related_concepts, list)
