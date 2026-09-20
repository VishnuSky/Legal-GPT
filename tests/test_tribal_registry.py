"""Tests for Tribal Rights, Indigenous Law & Historical Accountability Module (feat/tribal-indigenous-v1)."""

import pytest
import yaml
from pathlib import Path
from core.literacy.engine import LegalLiteracyEngine
from core.literacy.models import DrillDownAction

REGISTRY_DIR = Path(__file__).resolve().parent.parent / "legal_registry"
TRIBAL_DIR = REGISTRY_DIR / "tribal"
INTL_DIR = REGISTRY_DIR / "international" / "indigenous"

PACK_C_CONCEPTS = [
    "tribal_sovereignty",
    "treaty_rights",
    "indian_country_jurisdiction",
    "icwa_active_efforts",
    "icwa_qualified_expert_witness",
    "tribal_court_jurisdiction_icwa",
    "blood_quantum_vs_citizenship",
    "doctrine_of_discovery_repudiation",
    "land_rights_and_trust_responsibility",
    "native_voting_rights",
]


def test_sovereignty_doctrine_loads_with_verified_citations():
    """Verify tribal sovereignty doctrine loads with verified citations."""
    doctrine_path = TRIBAL_DIR / "sovereignty" / "doctrine.yaml"
    assert doctrine_path.exists(), "doctrine.yaml missing"
    with open(doctrine_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data.get("verification_status") == "VERIFIED"
    auths = data.get("primary_authorities", [])
    assert len(auths) >= 3
    citations = [a["citation"] for a in auths]
    assert any("Worcester v. Georgia" in c for c in citations)
    assert any("Cherokee Nation v. Georgia" in c for c in citations)
    assert any("Johnson v. M'Intosh" in c for c in citations)
    assert any("McGirt v. Oklahoma" in c for c in citations)

    for a in auths:
        assert a.get("official_url", "").startswith("https://")


def test_pacific_northwest_treaty_has_boldt_decision():
    """Verify Pacific Northwest treaty entry includes Boldt Decision citation."""
    pnw_path = TRIBAL_DIR / "treaties" / "pacific_northwest.yaml"
    assert pnw_path.exists(), "pacific_northwest.yaml missing"
    with open(pnw_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    treaties = data.get("treaties", [])
    pt_elliott = next((t for t in treaties if "Point Elliott" in t.get("name", "")), None)
    assert pt_elliott is not None, "Treaty of Point Elliott missing"
    assert pt_elliott.get("statutory_citation") == "12 Stat. 927"

    caselaw = pt_elliott.get("controlling_caselaw", [])
    assert any("Boldt Decision" in c.get("citation", "") or "384 F. Supp. 312" in c.get("citation", "") for c in caselaw), (
        "Boldt decision citation missing from Pacific Northwest treaties"
    )


def test_icwa_history_cites_congressional_finding():
    """Verify ICWA history entry cites 25 U.S.C. § 1901 congressional finding."""
    history_path = TRIBAL_DIR / "icwa" / "history.yaml"
    assert history_path.exists(), "icwa/history.yaml missing"
    with open(history_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    findings = data.get("historical_context", {}).get("congressional_findings", [])
    assert len(findings) >= 2
    citations = [f["citation"] for f in findings]
    assert any("1901(4)" in c for c in citations)
    assert any("1901(3)" in c for c in citations)

    # Pre-ICWA rate check
    rates = data.get("historical_context", {}).get("pre_icwa_separation_rates", "")
    assert "25%" in rates or "35%" in rates


def test_undrip_labeled_as_non_binding_domestic():
    """Verify UNDRIP is explicitly labeled as non-binding in U.S. domestic law."""
    undrip_path = INTL_DIR / "undrip.yaml"
    assert undrip_path.exists(), "undrip.yaml missing"
    with open(undrip_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    domestic_status = data.get("legal_status_domestic", "").lower()
    assert "not a legally binding treaty" in domestic_status or "non-binding" in domestic_status
    assert "international norm" in domestic_status


def test_historical_timeline_minimum_15_entries_chronological():
    """Verify legal timeline has at least 15 entries and is in chronological order."""
    timeline_path = TRIBAL_DIR / "history" / "legal_timeline.yaml"
    assert timeline_path.exists(), "legal_timeline.yaml missing"
    with open(timeline_path, "r", encoding="utf-8") as f:
        entries = yaml.safe_load(f)

    assert isinstance(entries, list)
    assert len(entries) >= 15, f"Expected at least 15 timeline entries, got {len(entries)}"

    years = []
    for entry in entries:
        d_str = str(entry.get("date", "")).strip()[:4]
        assert d_str.isdigit(), f"Invalid timeline date: {entry.get('date')}"
        years.append(int(d_str))

    # Verify monotonic chronological order
    for i in range(len(years) - 1):
        assert years[i] <= years[i + 1], f"Timeline out of order: {years[i]} came before {years[i+1]}"


def test_boarding_school_entry_cites_doi_2022_report():
    """Verify boarding school entry cites DOI 2022 investigative report."""
    bs_path = TRIBAL_DIR / "history" / "boarding_schools.yaml"
    assert bs_path.exists(), "boarding_schools.yaml missing"
    with open(bs_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    inv = data.get("official_investigation", {})
    assert "Federal Indian Boarding School Initiative" in inv.get("title", "")
    assert "Department of the Interior" in inv.get("agency", "")
    assert "2022" in str(inv.get("published", ""))
    assert "408" in str(inv.get("key_findings", []))
    assert "53" in str(inv.get("key_findings", []))


def test_pack_c_concepts_load_with_5_levels_non_empty():
    """Verify all 10 Pack C concepts load successfully with non-empty Levels 1 through 5."""
    for cid in PACK_C_CONCEPTS:
        exp = LegalLiteracyEngine.explain(cid, jurisdiction="FED")
        assert exp is not None, f"Failed to load concept {cid}"
        assert exp.level_1_plain_english and len(exp.level_1_plain_english.strip()) > 10, f"{cid} Level 1 empty"
        assert exp.level_2_practical and len(exp.level_2_practical.strip()) > 10, f"{cid} Level 2 empty"
        assert exp.level_3_terminology and len(exp.level_3_terminology.strip()) > 10, f"{cid} Level 3 empty"
        assert len(exp.level_4_primary_authority) > 0, f"{cid} Level 4 authorities empty"
        assert exp.level_5_advanced_analysis and len(exp.level_5_advanced_analysis.strip()) > 10, f"{cid} Level 5 empty"


def test_pack_c_level_4_rows_have_https_urls():
    """Verify each Pack C concept has Level 4 authorities with https:// URLs."""
    for cid in PACK_C_CONCEPTS:
        exp = LegalLiteracyEngine.explain(cid, jurisdiction="FED")
        for auth in exp.level_4_primary_authority:
            url = auth.official_portal_url
            assert url and url.startswith("https://"), (
                f"Concept {cid} citation {auth.citation} has invalid URL: {url}"
            )


def test_pack_c_undrip_references_labeled_non_binding():
    """Verify that Level 5 for all Pack C concepts labels UNDRIP as non-binding international norm."""
    for cid in PACK_C_CONCEPTS:
        exp = LegalLiteracyEngine.explain(cid, jurisdiction="FED")
        l5 = exp.level_5_advanced_analysis.lower()
        if "undrip" in l5:
            assert "non-binding" in l5 or "international norm" in l5, (
                f"Concept {cid} Level 5 refers to UNDRIP without non-binding designation"
            )


def test_doctrine_of_discovery_neutral_presentation():
    """Verify Doctrine of Discovery entry presents domestic legal status and international critique without editorializing."""
    exp = LegalLiteracyEngine.explain("doctrine_of_discovery_repudiation", jurisdiction="FED")
    l3 = exp.level_3_terminology.lower()
    l5 = exp.level_5_advanced_analysis.lower()

    # Must state domestic law (Johnson v. M'Intosh, aboriginal title)
    assert "johnson v. m'intosh" in l3 or "johnson v. m'intosh" in l5
    assert "occupancy" in l3 or "occupancy" in l5

    # Must state international critique / repudiation
    assert "repudiat" in l5 or "condemn" in l5
    assert "vatican" in l5 or "united nations" in l5

    # Must present both sides
    assert "competing positions" in l5 or "domestic" in l5
