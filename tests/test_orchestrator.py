"""End-to-end tests for LegalGPTOrchestrator across multiple state jurisdictions."""

from datetime import date
from agents.legal_orchestrator import LegalGPTOrchestrator


def test_orchestrator_washington_cps_query():
    orch = LegalGPTOrchestrator()
    resp = orch.process_query(
        query="DCYF took my daughter without court order in Skagit County and didn't hold a shelter care hearing within 72 hours",
        override_state="WA",
        override_county="Skagit"
    )
    assert "WA" in resp.jurisdiction
    assert any("RCW 13.34" in auth for auth in resp.controlling_authority)
    assert resp.confidence_level == "High"
    assert len(resp.verified_sources) >= 1
    assert "IMPORTANT LEGAL DISCLAIMER" in resp.disclaimer


def test_orchestrator_illinois_cps_query():
    orch = LegalGPTOrchestrator()
    resp = orch.process_query(
        query="DCFS placed child in protective custody in Chicago Cook County without a 48 hour temporary custody hearing",
        override_state="IL",
        override_county="Cook"
    )
    assert "IL" in resp.jurisdiction
    assert any("705 ILCS" in auth for auth in resp.controlling_authority)
    assert resp.confidence_level == "High"


def test_orchestrator_ohio_cps_query():
    orch = LegalGPTOrchestrator()
    resp = orch.process_query(
        query="Emergency shelter custody complaint filed in Cuyahoga County juvenile court without notice",
        override_state="OH",
        override_county="Cuyahoga"
    )
    assert "OH" in resp.jurisdiction
    assert any("ORC" in auth for auth in resp.controlling_authority)
    assert resp.confidence_level == "High"


def test_orchestrator_temporal_event_date_handling():
    orch = LegalGPTOrchestrator()
    event_d = date(2025, 4, 15)
    resp = orch.process_query(
        query="CPS removed child without notice",
        override_state="WA",
        event_date=event_d
    )
    assert resp.conflicting_or_distinguishing_authority is not None
    assert "2025-04-15" in resp.conflicting_or_distinguishing_authority


def test_orchestrator_unspecified_jurisdiction_handling():
    orch = LegalGPTOrchestrator()
    # Query with no state or location clues
    resp = orch.process_query(query="What happens when children are removed?")
    assert "Unspecified" in resp.jurisdiction
    assert any("Jurisdiction Not Specified" in issue for issue in resp.legal_issues)
