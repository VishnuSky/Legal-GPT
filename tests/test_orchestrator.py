"""End-to-end tests for LegalGPTOrchestrator across multiple state jurisdictions."""

from datetime import date
from agents.legal_orchestrator import LegalGPTOrchestrator


def test_orchestrator_washington_cps_query():
    orch = LegalGPTOrchestrator()
    resp = orch.process_query(
        query="What are the statutory requirements for emergency child removal and the 72-hour shelter care hearing under RCW 13.34.065 in Washington State?",
        override_state="WA"
    )
    assert "WA" in resp.jurisdiction
    assert any("RCW 13.34" in auth for auth in resp.controlling_authority)
    assert resp.confidence_level == "High"
    assert len(resp.verified_sources) >= 1
    assert "IMPORTANT LEGAL DISCLAIMER" in resp.disclaimer


def test_orchestrator_illinois_cps_query():
    orch = LegalGPTOrchestrator()
    resp = orch.process_query(
        query="What statutory standards govern 48-hour temporary custody hearings under 705 ILCS 405/2-10 in Illinois?",
        override_state="IL"
    )
    assert "IL" in resp.jurisdiction
    assert any("705 ILCS" in auth for auth in resp.controlling_authority)
    assert resp.confidence_level == "High"


def test_orchestrator_ohio_cps_query():
    orch = LegalGPTOrchestrator()
    resp = orch.process_query(
        query="What are the notice and hearing requirements for juvenile shelter custody under Ohio Revised Code Chapter 2151?",
        override_state="OH"
    )
    assert "OH" in resp.jurisdiction
    assert any("ORC" in auth for auth in resp.controlling_authority)
    assert resp.confidence_level == "High"


def test_orchestrator_temporal_event_date_handling():
    orch = LegalGPTOrchestrator()
    event_d = date(2025, 4, 15)
    resp = orch.process_query(
        query="What statutory notice requirements apply to emergency shelter custody under RCW 13.34.065?",
        override_state="WA",
        event_date=event_d
    )
    assert resp.conflicting_or_distinguishing_authority is not None
    assert "2025-04-15" in resp.conflicting_or_distinguishing_authority


def test_orchestrator_unspecified_jurisdiction_handling():
    orch = LegalGPTOrchestrator()
    # Query with no state or location clues
    resp = orch.process_query(query="What statutory standards govern emergency child welfare proceedings generally?")
    assert "WA (State)" in resp.jurisdiction or "Unspecified" in resp.jurisdiction
    assert resp.confidence_level in ["High", "Medium"]
