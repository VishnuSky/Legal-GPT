"""Tests for Expanded Registries (CA, TX, NY, Territories, Tribal) and Ingestion Connectors."""

from legal_registry.loader import default_registry
from cps.lifecycle import CPSLifecycleEngine, CPSStage
from ingestion.govinfo import GovInfoConnector
from ingestion.courtlistener import CourtListenerConnector
from ingestion.state_crawlers.washington import WashingtonLegConnector
from ingestion.state_crawlers.illinois import IllinoisLegConnector
from ingestion.state_crawlers.ohio import OhioLegConnector
from scripts.seed_database import build_seed_documents


def test_expanded_state_registries():
    # California
    assert "CA" in default_registry.state_sources
    assert any(s.source_id == "CA_CODES" for s in default_registry.state_sources["CA"])
    assert "CPS_CA_WIC_300" in default_registry.cps_sources

    # Texas
    assert "TX" in default_registry.state_sources
    assert any(s.source_id == "TX_FAMILY_CODE" for s in default_registry.state_sources["TX"])
    assert "CPS_TX_FAM_CODE_262" in default_registry.cps_sources

    # New York
    assert "NY" in default_registry.state_sources
    assert any(s.source_id == "NY_FCA" for s in default_registry.state_sources["NY"])
    assert "CPS_NY_FCA_10" in default_registry.cps_sources


def test_territories_registry_loaded():
    assert len(default_registry.territories) >= 5
    assert "PR" in default_registry.territories  # Puerto Rico
    assert "GU" in default_registry.territories  # Guam
    assert "VI" in default_registry.territories  # US Virgin Islands


def test_tribal_registry_loaded():
    assert len(default_registry.tribal_sources) >= 3
    assert "TRIBAL_BIA_DESIGNATED_AGENTS" in default_registry.tribal_sources
    assert "TRIBAL_NAVAJO_CHILD_CODE" in default_registry.tribal_sources
    assert "TRIBAL_PUYALLUP_CHILD_CODE" in default_registry.tribal_sources


def test_expanded_cps_lifecycle_rules():
    # California Detention
    ca_det = CPSLifecycleEngine.get_stage_requirements("CA", CPSStage.SHELTER_CARE_HEARING)
    assert ca_det is not None
    assert "48 to 72 hours" in ca_det.required_notice_hours_or_days

    # Texas Adversary Hearing (14 days)
    tx_adv = CPSLifecycleEngine.get_stage_requirements("TX", CPSStage.SHELTER_CARE_HEARING)
    assert tx_adv is not None
    assert "14 days" in tx_adv.required_notice_hours_or_days
    assert "Tex. Fam. Code" in tx_adv.controlling_statute

    # New York Section 1028 hearing (3 court days)
    ny_1028 = CPSLifecycleEngine.get_stage_requirements("NY", CPSStage.SHELTER_CARE_HEARING)
    assert ny_1028 is not None
    assert "3 court days" in ny_1028.required_notice_hours_or_days


def test_ingestion_connectors_initialization():
    govinfo = GovInfoConnector()
    assert govinfo.source_id == "FED_GOVINFO"

    cl = CourtListenerConnector()
    assert cl.source_id == "FED_COURTLISTENER"

    wa_leg = WashingtonLegConnector()
    doc = wa_leg.parse_rcw_html("13.34.050", "Court order to take child into custody", "<p>Test statutory content</p>")
    assert doc.citation == "RCW 13.34.050"
    assert doc.jurisdiction == "US-WA"


def test_seed_documents_integrity():
    docs = build_seed_documents()
    assert len(docs) == 9
    for d in docs:
        assert d.content_hash != ""
        assert len(d.chunks) >= 1
        assert d.temporal.effective_date is not None
