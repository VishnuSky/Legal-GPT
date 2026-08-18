"""Tests for Anti-Hallucination Citation Verification Engine."""

from core.citation_verifier import CitationVerifier


def test_verify_canonical_citations():
    # Washington RCW
    res_wa = CitationVerifier.verify_citation("RCW 13.34.050")
    assert res_wa.verified is True
    assert res_wa.authority_tier == "TIER_0"

    # Illinois ILCS
    res_il = CitationVerifier.verify_citation("705 ILCS 405/2-6")
    assert res_il.verified is True
    assert res_il.authority_tier == "TIER_0"

    # Ohio ORC
    res_oh = CitationVerifier.verify_citation("ORC § 2151.35")
    assert res_oh.verified is True
    assert res_oh.authority_tier == "TIER_0"

    # Federal USC
    res_fed = CitationVerifier.verify_citation("25 U.S.C. § 1912")
    assert res_fed.verified is True
    assert res_fed.authority_tier == "TIER_0"


def test_reject_hallucinated_citations():
    # Completely fake citation
    res_fake = CitationVerifier.verify_citation("FakeStatute 99.999.xyz")
    assert res_fake.verified is False
    assert res_fake.authority_tier == "TIER_5"
    assert "Not found in official legal registry" in res_fake.rejection_reason


def test_extract_citations_from_text():
    text = "The court relied on RCW 13.34.065 and 705 ILCS 405/2-10 as well as 42 U.S.C. § 671."
    extracted = CitationVerifier.extract_citations(text)
    assert len(extracted) == 3
    assert "RCW 13.34.065" in extracted
    assert "705 ILCS 405/2-10" in extracted
    assert "42 U.S.C. § 671" in extracted
