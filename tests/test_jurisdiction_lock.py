"""Tests for Jurisdiction Lock & Cross-Jurisdiction Contamination Defense."""

from core.jurisdiction import JurisdictionEngine


def test_cross_contamination_detected():
    # Context is locked to Washington State
    ctx = JurisdictionEngine.lock_jurisdiction("WA")
    
    # Erroneously includes Illinois ILCS citation
    citations = ["RCW 13.34.050", "705 ILCS 405/2-6"]
    violations = JurisdictionEngine.detect_cross_contamination(ctx, citations)

    assert len(violations) == 1
    assert "belongs to IL, but jurisdiction is locked to WA" in violations[0]


def test_valid_jurisdiction_citations_pass():
    ctx = JurisdictionEngine.lock_jurisdiction("WA")
    citations = ["RCW 13.34.050", "25 U.S.C. § 1912"] # WA + Federal is valid
    violations = JurisdictionEngine.detect_cross_contamination(ctx, citations)
    assert len(violations) == 0
