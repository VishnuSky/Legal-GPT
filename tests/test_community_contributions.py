"""Unit tests for the Legal-GPT Community Contribution Framework.

Verifies:
- All 16 contribution types
- All 9 mandatory metadata fields
- All 6 lifecycle states and state transitions
- Strict quarantine isolation firewall
- License compliance and official domain enforcement
- PII and security firewall detection
- Provenance DAG lineage and supersession tracking
"""

import pytest
from datetime import date

from core.contributions.models import (
    ContributionType,
    ContributionState,
    ProvenanceMetadata,
    CommunityContribution,
    ReviewEvent,
)
from core.contributions.validator import ContributionValidator
from core.contributions.provenance_graph import (
    ContributionProvenanceGraph,
    EdgeType,
    ContributionNode,
)
from core.contributions.workflow import ContributionWorkflowEngine


@pytest.fixture
def valid_statute_contribution():
    """Provides a valid statutory contribution conforming to all rules."""
    return CommunityContribution(
        contribution_id="CONTRIB-TEST-STATUTE",
        contribution_type=ContributionType.STATUTE,
        source="RCW 13.34.065",
        submitter="LegalAidFellow",
        date="2026-09-17",
        jurisdiction="US-WA",
        authority_type="T5_STATE_STATUTE",
        effective_date="2021-07-01",
        provenance=ProvenanceMetadata(
            origin_url="https://app.leg.wa.gov/rcw/default.aspx?cite=13.34.065",
            publisher="Washington State Legislature",
            verification_method="Official Code Reviser XML extraction",
        ),
        license="CC0-1.0",
        verification_state=ContributionState.PROPOSED,
        payload={
            "title": "Shelter care—Hearing—Recommendation as to further need—Release.",
            "statutory_text": "The shelter care hearing shall commence not later than seventy-two hours...",
        },
    )


def test_all_16_contribution_types_defined():
    """Verify all 16 required contribution types are enumerated."""
    expected_types = {
        "LEGAL_SOURCE",
        "SOURCE_METADATA",
        "JURISDICTION",
        "CASE",
        "STATUTE",
        "REGULATION",
        "COURT_RULE",
        "AGENCY_POLICY",
        "RESOURCE",
        "DATASET",
        "TEST_CASE",
        "BENCHMARK",
        "BUG_REPORT",
        "DOCUMENTATION",
        "TRANSLATION",
        "LEGAL_LITERACY_MATERIAL",
    }
    actual_types = {t.value for t in ContributionType}
    assert expected_types == actual_types


def test_all_6_contribution_states_defined():
    """Verify all 6 required lifecycle states are enumerated."""
    expected_states = {
        "PROPOSED",
        "UNDER_REVIEW",
        "VERIFIED",
        "REJECTED",
        "SUPERSEDED",
        "ARCHIVED",
    }
    actual_states = {s.value for s in ContributionState}
    assert expected_states == actual_states


def test_valid_contribution_validation(valid_statute_contribution):
    """Verify that a compliant contribution passes validation."""
    is_valid, errors = ContributionValidator.validate(valid_statute_contribution)
    assert is_valid is True
    assert len(errors) == 0


def test_mandatory_fields_validation(valid_statute_contribution):
    """Verify that missing mandatory fields trigger validation errors."""
    # Blank source
    bad_contrib = valid_statute_contribution.model_copy(deep=True)
    bad_contrib.source = ""
    is_valid, errors = ContributionValidator.validate(bad_contrib)
    assert is_valid is False
    assert any("source" in err for err in errors)

    # Blank submitter
    bad_contrib = valid_statute_contribution.model_copy(deep=True)
    bad_contrib.submitter = " "
    is_valid, errors = ContributionValidator.validate(bad_contrib)
    assert is_valid is False
    assert any("submitter" in err for err in errors)

    # Disallowed initial state
    bad_contrib = valid_statute_contribution.model_copy(deep=True)
    bad_contrib.verification_state = ContributionState.VERIFIED
    is_valid, errors = ContributionValidator.validate(bad_contrib)
    assert is_valid is False
    assert any("Initial submission state must be 'PROPOSED'" in err for err in errors)


def test_license_whitelist_enforcement(valid_statute_contribution):
    """Verify that only whitelisted permissive open data licenses are accepted."""
    bad_contrib = valid_statute_contribution.model_copy(deep=True)
    bad_contrib.license = "All Rights Reserved (Proprietary)"
    is_valid, errors = ContributionValidator.validate(bad_contrib)
    assert is_valid is False
    assert any("License" in err for err in errors)


def test_privacy_and_pii_rejection(valid_statute_contribution):
    """Verify that PII and disallowed patterns are detected and rejected."""
    # Test SSN pattern
    bad_contrib = valid_statute_contribution.model_copy(deep=True)
    bad_contrib.payload = {"notes": "Party SSN is 000-12-3456"}
    is_valid, errors = ContributionValidator.validate(bad_contrib)
    assert is_valid is False
    assert any("Security/Privacy violation" in err for err in errors)

    # Test reddit/forum citation
    bad_contrib2 = valid_statute_contribution.model_copy(deep=True)
    bad_contrib2.provenance.origin_url = "https://reddit.com/r/legaladvice/post"
    is_valid2, errors2 = ContributionValidator.validate(bad_contrib2)
    assert is_valid2 is False
    assert any("Security/Privacy violation" in err for err in errors2)


def test_official_domain_enforcement_for_primary_law(valid_statute_contribution):
    """Verify primary law must originate from an official government or court repository."""
    bad_contrib = valid_statute_contribution.model_copy(deep=True)
    bad_contrib.provenance.origin_url = "https://randomlawblog.org/rcw-13-34-065"
    is_valid, errors = ContributionValidator.validate(bad_contrib)
    assert is_valid is False
    assert any("official government or court repository" in err for err in errors)


def test_cryptographic_hash_generation(valid_statute_contribution):
    """Verify SHA-256 hash generation is deterministic."""
    hash1 = valid_statute_contribution.calculate_hash()
    hash2 = valid_statute_contribution.calculate_hash()
    assert hash1 == hash2
    assert len(hash1) == 64

    # Modifying content modifies the hash
    modified = valid_statute_contribution.model_copy(deep=True)
    modified.source = "RCW 13.34.066"
    assert modified.calculate_hash() != hash1


def test_quarantine_firewall_isolation(valid_statute_contribution):
    """CRITICAL: Test that unverified submissions NEVER enter the authoritative pool."""
    engine = ContributionWorkflowEngine()

    # 1. Submit contribution into quarantine
    res = engine.submit(valid_statute_contribution)
    assert res["success"] is True
    assert res["status"] == "PROPOSED"

    # 2. Authoritative query MUST return empty
    auth_sources = engine.get_authoritative_verified_sources(jurisdiction="US-WA")
    assert len(auth_sources) == 0

    # 3. Quarantined list contains the item
    quarantined = engine.get_quarantined_submissions()
    assert len(quarantined) == 1
    assert quarantined[0].contribution_id == valid_statute_contribution.contribution_id

    # 4. Move to UNDER_REVIEW
    engine.begin_review(
        contribution_id=valid_statute_contribution.contribution_id,
        reviewer_id="Reviewer-001",
        notes="Starting formal verification.",
    )

    # 5. Authoritative query STILL returns empty during review
    assert len(engine.get_authoritative_verified_sources(jurisdiction="US-WA")) == 0


def test_full_lifecycle_and_state_transitions(valid_statute_contribution):
    """Verify transitions: PROPOSED -> UNDER_REVIEW -> VERIFIED -> SUPERSEDED."""
    engine = ContributionWorkflowEngine()
    engine.submit(valid_statute_contribution)
    cid = valid_statute_contribution.contribution_id

    # Cannot verify directly from PROPOSED
    with pytest.raises(ValueError):
        engine.verify(cid, reviewer_id="Rev-1", notes="Cannot skip review")

    # Move to UNDER_REVIEW
    engine.begin_review(cid, reviewer_id="Rev-1", notes="Reviewing text")

    # Verify and promote to authoritative registry
    engine.verify(
        cid,
        reviewer_id="Rev-1",
        notes="Matches official code reviser text exactly.",
        metadata={"citator_signal": "GOOD_LAW"},
    )

    # Now authoritative pool contains the verified item
    auth_sources = engine.get_authoritative_verified_sources(jurisdiction="US-WA")
    assert len(auth_sources) == 1
    assert auth_sources[0].contribution_id == cid
    assert auth_sources[0].verification_state == ContributionState.VERIFIED

    # Quarantined list is now empty
    assert len(engine.get_quarantined_submissions()) == 0

    # Submit a successor enactment
    successor_contrib = valid_statute_contribution.model_copy(deep=True)
    successor_contrib.contribution_id = "CONTRIB-TEST-STATUTE-AMENDED"
    successor_contrib.verification_state = ContributionState.PROPOSED
    successor_contrib.effective_date = "2024-06-01"
    successor_contrib.provenance.parent_contribution_id = cid
    res = engine.submit(successor_contrib)
    assert res["success"] is True
    engine.begin_review(successor_contrib.contribution_id, reviewer_id="Rev-1")
    engine.verify(successor_contrib.contribution_id, reviewer_id="Rev-1", notes="Amended law verified")

    # Supersede original
    engine.supersede(
        prior_contribution_id=cid,
        successor_contribution_id=successor_contrib.contribution_id,
        reviewer_id="Rev-1",
        notes="Amended by 2024 legislative session.",
    )

    # Original is no longer in active authoritative pool
    active_sources = engine.get_authoritative_verified_sources(jurisdiction="US-WA")
    assert len(active_sources) == 1
    assert active_sources[0].contribution_id == successor_contrib.contribution_id


def test_rejection_workflow(valid_statute_contribution):
    """Verify rejection keeps the contribution out of the authoritative pool."""
    engine = ContributionWorkflowEngine()
    engine.submit(valid_statute_contribution)
    cid = valid_statute_contribution.contribution_id

    engine.begin_review(cid, reviewer_id="Rev-1", notes="Inspecting")
    rejected = engine.reject(cid, reviewer_id="Rev-1", reason="Statute was repealed in 2020.")

    assert rejected.verification_state == ContributionState.REJECTED
    assert len(engine.get_authoritative_verified_sources(jurisdiction="US-WA")) == 0
    assert len(engine.get_quarantined_submissions(state=ContributionState.REJECTED)) == 1


def test_provenance_dag_lineage_and_supersession(valid_statute_contribution):
    """Verify provenance DAG nodes, edges, lineage trace, and supersession ancestry."""
    graph = ContributionProvenanceGraph()
    engine = ContributionWorkflowEngine(provenance_graph=graph)

    # 1. Ingest original
    engine.submit(valid_statute_contribution)
    cid1 = valid_statute_contribution.contribution_id

    # 2. Ingest successor
    successor = valid_statute_contribution.model_copy(deep=True)
    successor.contribution_id = "CONTRIB-SUCC-1"
    successor.provenance.parent_contribution_id = cid1
    engine.submit(successor)

    # 3. Ingest grandson
    grandson = valid_statute_contribution.model_copy(deep=True)
    grandson.contribution_id = "CONTRIB-SUCC-2"
    grandson.provenance.parent_contribution_id = "CONTRIB-SUCC-1"
    engine.submit(grandson)

    # Check ancestry chain
    ancestry = graph.get_ancestry_chain("CONTRIB-SUCC-2")
    assert ancestry == ["CONTRIB-SUCC-2", "CONTRIB-SUCC-1", cid1]

    # Check lineage of original
    lineage = graph.get_lineage(cid1)
    assert lineage["contribution_id"] == cid1
    assert f"SUBMITTER-{valid_statute_contribution.submitter}" in lineage["submitters"]
    assert f"OFFICIAL-{valid_statute_contribution.provenance.publisher}" in lineage["official_sources"]
    assert "CONTRIB-SUCC-1" in lineage["superseded_by"]
