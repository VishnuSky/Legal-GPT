"""Tests for Citation Verifier Edge Cases and Strict Boundary Enforcement."""

from core.citation_verifier import CitationVerifier


def test_invalid_title_rcw_rejected():
    # RCW Title 999 does not exist
    res = CitationVerifier.verify_citation("RCW 999.99.999")
    assert res.verified is False
    assert res.authority_tier == "TIER_5"
    assert "unrecognized" in res.rejection_reason


def test_invalid_chapter_ilcs_rejected():
    # ILCS Chapter 9999 does not exist
    res = CitationVerifier.verify_citation("9999 ILCS 5/1")
    assert res.verified is False
    assert "unrecognized" in res.rejection_reason


def test_invalid_orc_chapter_rejected():
    # ORC Chapter 9999 does not exist
    res = CitationVerifier.verify_citation("ORC § 9999.01")
    assert res.verified is False
    assert "unrecognized" in res.rejection_reason


def test_invalid_usc_title_rejected():
    # Title 99 U.S.C. does not exist (USC only goes to Title 54)
    res = CitationVerifier.verify_citation("99 U.S.C. § 100")
    assert res.verified is False
    assert "unrecognized" in res.rejection_reason


def test_citation_case_insensitivity_and_whitespace():
    res1 = CitationVerifier.verify_citation("rcw 13.34.050")
    assert res1.verified is True
    assert res1.normalized_citation == "RCW 13.34.050"

    res2 = CitationVerifier.verify_citation("  42   U.S.C.   §  671  ")
    assert res2.verified is True
    assert res2.normalized_citation == "42 U.S.C. § 671"
