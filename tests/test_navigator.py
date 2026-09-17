"""Comprehensive unit test suite for the Legal-GPT Public Legal Navigator subsystem."""

import pytest
from core.navigator import (
    PublicLegalNavigator,
    LegalNavigationReport,
    FactClassifier,
    FactExtractionResult,
    StatementType,
    JurisdictionClassifier,
    JurisdictionClassificationResult,
    IssueClassifier,
    LegalDomain,
    ProcedureClassifier,
    ProceduralPosture,
    ResourceDiscovery,
    VerifiedResourceCategory,
    ReportRenderer
)


def test_fact_classifier_separates_categories():
    """Verify FactClassifier accurately separates facts, allegations, and interpretations."""
    narrative = (
        "Caseworker visited my home on Tuesday afternoon. "
        "The caseworker lied to the judge and falsely claimed I have drugs in the house. "
        "I believe this is completely illegal and they have no right to do this to my family."
    )

    result: FactExtractionResult = FactClassifier.classify_narrative(narrative)

    assert len(result.facts) >= 1
    assert len(result.allegations) >= 1
    assert len(result.interpretations) >= 1

    # Check that objective visit statement is a FACT
    fact_texts = [f.text for f in result.facts]
    assert any("visited" in t.lower() for t in fact_texts)

    # Check that caseworker lied/claimed is an ALLEGATION
    allegation_texts = [a.text for a in result.allegations]
    assert any("lied" in t.lower() or "claimed" in t.lower() for t in allegation_texts)

    # Check that lay legal conclusion is an INTERPRETATION
    interp_texts = [i.text for i in result.interpretations]
    assert any("illegal" in t.lower() or "no right" in t.lower() or "believe" in t.lower() for t in interp_texts)


def test_fact_classifier_extracts_dates():
    """Verify FactClassifier extracts ISO and formatted dates and contextualizes them."""
    narrative = (
        "On 2024-03-12, caseworker removed my children from school. "
        "The court scheduled our shelter care hearing on March 15, 2024 at 9:00 AM."
    )

    result = FactClassifier.classify_narrative(narrative)
    assert len(result.extracted_dates) >= 2

    iso_dates = [d.iso_date for d in result.extracted_dates if d.iso_date]
    assert "2024-03-12" in iso_dates
    assert "2024-03-15" in iso_dates

    # Verify hearing category tag
    hearing_dates = [d for d in result.extracted_dates if d.category.value == "HEARING_DATE"]
    assert len(hearing_dates) >= 1


def test_jurisdiction_classifier_resolves_known_state_and_county():
    """Verify JurisdictionClassifier resolves state, county, and court when explicitly supplied."""
    narrative = "I am dealing with a CPS dependency case in Skagit County, Washington in Superior Court."
    res: JurisdictionClassificationResult = JurisdictionClassifier.classify_jurisdiction(narrative)

    assert res.is_known is True
    assert res.state == "WA"
    assert res.state_name == "Washington"
    assert res.county == "Skagit"
    assert res.court is not None
    assert "Superior Court" in res.court
    assert res.normalized_code == "US-WA"


def test_jurisdiction_classifier_unknown_asks_never_guesses():
    """Verify JurisdictionClassifier never silently guesses when state is missing."""
    narrative = "A caseworker showed up yesterday and took my baby. When can I see my child?"
    res: JurisdictionClassificationResult = JurisdictionClassifier.classify_jurisdiction(narrative)

    assert res.is_known is False
    assert res.state is None
    assert res.normalized_code == "UNKNOWN"
    assert len(res.clarification_questions) > 0
    assert any("What state" in q for q in res.clarification_questions)


def test_jurisdiction_classifier_tribal_recognition():
    """Verify JurisdictionClassifier identifies tribal jurisdiction under ICWA."""
    narrative = "Our family is enrolled with the Puyallup Tribe in Pierce County, Washington."
    res = JurisdictionClassifier.classify_jurisdiction(narrative)

    assert res.is_known is True
    assert res.state == "WA"
    assert res.tribal_jurisdiction is not None
    assert "Puyallup" in res.tribal_jurisdiction


def test_issue_classifier_spots_cps_and_constitutional():
    """Verify IssueClassifier correctly classifies CPS and Fourth Amendment search/seizure domains."""
    narrative = (
        "Police and a caseworker entered my house without a warrant and removed my child. "
        "They refused to look at my clean drug test or place my child with her grandmother."
    )

    res = IssueClassifier.classify_issues(narrative)
    assert res.primary_domain in (LegalDomain.CPS_CHILD_WELFARE, LegalDomain.CONSTITUTIONAL)
    all_domains = [res.primary_domain] + res.secondary_domains
    assert LegalDomain.CPS_CHILD_WELFARE in all_domains
    assert LegalDomain.CONSTITUTIONAL in all_domains

    # Check spotted issues
    assert len(res.spotted_issues) > 0
    issue_text = " ".join(res.spotted_issues).lower()
    assert "warrantless" in issue_text or "emergency" in issue_text or "removal" in issue_text


def test_procedure_classifier_identifies_emergency_removal_posture():
    """Verify ProcedureClassifier identifies agency action / emergency removal and statutory deadlines."""
    narrative = "CPS removed my son on Tuesday without warning. What do I need to do?"
    res = ProcedureClassifier.classify_posture(narrative, state="WA")

    assert res.posture in (ProceduralPosture.AGENCY_ACTION, ProceduralPosture.PRELIMINARY_HEARING)
    assert len(res.urgent_deadlines) > 0
    # Should cite 72-hour shelter care hearing in WA
    assert any("72 hours" in d or "RCW 13.34.065" in d for d in res.urgent_deadlines)
    assert len(res.immediate_procedural_steps) > 0


def test_resource_discovery_returns_verified_resources():
    """Verify ResourceDiscovery retrieves genuine, verified legal aid and court resources."""
    res = ResourceDiscovery.discover_resources(state="WA", county="Skagit", domain_name="CPS_CHILD_WELFARE")

    assert res.total_found > 0
    # Check that all resources have verified official URLs
    for la in res.legal_aid_services:
        assert la.website.startswith("http")
        assert la.is_official is True
        assert "Northwest Justice Project" in la.name or "Legal" in la.name


def test_navigator_end_to_end_report_16_sections():
    """Verify the complete 10-step PublicLegalNavigator generates all 16 required report sections."""
    narrative = (
        "On March 12, 2024, a DCYF caseworker and police officer came to my home in Skagit County, Washington. "
        "They entered without a warrant and took my 4-year-old daughter into protective custody. "
        "The caseworker claimed the home was unsafe, which is a complete lie. "
        "I believe this violates my Fourth Amendment rights. "
        "Our hearing is scheduled for tomorrow morning. My mother is ready to take my daughter right now."
    )

    report: LegalNavigationReport = PublicLegalNavigator.navigate(narrative)

    # 1. What I understand
    assert len(report.what_i_understand) > 20
    assert "Washington" in report.what_i_understand

    # 2. Facts provided
    assert len(report.facts_provided) >= 1

    # 3. Allegations
    assert len(report.allegations) >= 1

    # 4. Unknowns
    assert isinstance(report.unknowns, list)

    # 5. Jurisdiction
    assert report.jurisdiction.state == "WA"
    assert report.jurisdiction.county == "Skagit"
    assert report.jurisdiction.is_known is True

    # 6. Relevant legal domains
    assert len(report.relevant_legal_domains) >= 1

    # 7. Procedural posture
    assert report.procedural_posture.posture is not None

    # 8. Potentially relevant authority (Verified citations)
    assert len(report.potentially_relevant_authority) >= 1
    assert any("RCW" in a for a in report.potentially_relevant_authority)

    # 9. Potential rights and duties
    assert len(report.potential_rights_and_duties) >= 1
    rights_names = [r["right_name"] for r in report.potential_rights_and_duties]
    assert any("Counsel" in r or "Notice" in r for r in rights_names)

    # 10. Potential procedural requirements
    assert len(report.potential_procedural_requirements) >= 1

    # 11. Important dates
    assert len(report.important_dates) >= 1

    # 12. Evidence & questions to investigate (What would change analysis)
    assert len(report.evidence_and_questions_to_investigate) >= 3

    # 13. Conflicting or uncertain authority
    assert isinstance(report.conflicting_or_uncertain_authority, list)

    # 14. Available public resources
    assert report.available_public_resources.total_found >= 1

    # 15. Questions for qualified counsel
    assert len(report.questions_for_qualified_counsel) >= 4

    # 16. Verification status
    assert report.verification_status["authority_verified"] == "VERIFIED_OFFICIAL_REGISTRY"
    assert report.verification_status["jurisdiction_lock"] == "US-WA"

    # Render Markdown test
    md = report.render_markdown()
    assert "# Legal Navigation Report" in md
    assert "## 1. What I Understand" in md
    assert "## 2. Facts Provided" in md
    assert "## 3. Allegations & Disputed Claims" in md
    assert "## 4. Critical Unknowns" in md
    assert "## 5. Jurisdiction" in md
    assert "## 6. Relevant Legal Domains" in md
    assert "## 7. Procedural Posture" in md
    assert "## 8. Potentially Relevant Controlling Authority" in md
    assert "## 9. Potential Rights and Duties" in md
    assert "## 10. Potential Procedural Requirements & Deadlines" in md
    assert "## 11. Important Dates" in md
    assert "## 12. Evidence & Questions to Investigate" in md
    assert "## 13. Conflicting or Uncertain Authority" in md
    assert "## 14. Available Verified Public Resources" in md
    assert "## 15. Targeted Questions for Your Court-Appointed Attorney" in md
    assert "## 16. Verification Status & Integrity Audit" in md


def test_navigator_fastapi_endpoint():
    """Verify the FastAPI POST /api/v1/public/navigate endpoint returns structured report and markdown."""
    from fastapi.testclient import TestClient
    from api.server import app

    client = TestClient(app)
    payload = {
        "narrative": "A DCFS caseworker in Cook County, Illinois removed my child on Tuesday without a warrant.",
        "state": "IL",
        "county": "Cook"
    }

    response = client.post("/api/v1/public/navigate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "report" in data
    assert "markdown" in data

    report_obj = data["report"]
    assert report_obj["jurisdiction"]["state"] == "IL"
    assert report_obj["jurisdiction"]["county"] == "Cook"
    assert report_obj["jurisdiction"]["is_known"] is True
    assert "# Legal Navigation Report" in data["markdown"]
    assert "## 1. What I Understand" in data["markdown"]
