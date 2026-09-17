"""Unit and integration tests for the Public-Data-Safe Legal Evidence Bridge."""

import pytest
from core.evidence.models import (
    EpistemicClassification,
    EvidenceVerificationState,
    EvidenceRecord,
    LegalElement,
    LegalBridgeLink,
    EvidenceBridgeEvaluation,
)
from core.evidence.registry import LegalElementRegistry, CANONICAL_LEGAL_ELEMENTS
from core.evidence.bridge import LegalEvidenceBridge


def test_coverage_of_all_seven_epistemic_classifications():
    """Verify that all 7 required classifications are defined and supported."""
    assert len(EpistemicClassification) == 7
    classifications = {c.value for c in EpistemicClassification}
    expected = {"FACT", "ALLEGATION", "DOCUMENTED_FACT", "TESTIMONY", "OPINION", "INFERENCE", "UNKNOWN"}
    assert classifications == expected


def test_evidence_record_mandatory_fields():
    """Verify that EvidenceRecord validates all 9 required fields."""
    record = EvidenceRecord(
        id="EV-001",
        description="Caseworker investigative interview summary",
        source_type="CASEWORKER_NOTE",
        date="2024-03-12",
        author="Child Welfare Caseworker",
        custodian="DCYF Records Dept",
        relevance="Alleges inadequate food in the residence",
        associated_issue="Neglect / Food Insecurity",
        verification_state=EvidenceVerificationState.UNVERIFIED_ASSERTION,
        classification=EpistemicClassification.ALLEGATION
    )

    assert record.id == "EV-001"
    assert record.description != ""
    assert record.source_type == "CASEWORKER_NOTE"
    assert record.date == "2024-03-12"
    assert record.author == "Child Welfare Caseworker"
    assert record.custodian == "DCYF Records Dept"
    assert record.relevance != ""
    assert record.associated_issue == "Neglect / Food Insecurity"
    assert record.verification_state == EvidenceVerificationState.UNVERIFIED_ASSERTION
    assert record.classification == EpistemicClassification.ALLEGATION


def test_prompt_example_notice_requirement_bridge():
    """Verify the exact prompt example:
    LEGAL ELEMENT: Notice requirement
    EVIDENCE: Notice document
    QUESTION: Was legally required notice provided?
    MISSING: Date, Recipient, Method, Content, Proof of service
    """
    # Create bare notice document without complete predicates
    bare_notice = EvidenceRecord(
        id="EV-NOTICE-01",
        description="Undated agency intake form labeled Notice of Temporary Custody",
        source_type="NOTICE_DOCUMENT",
        date=None,  # Missing date
        author="Child Protective Services",
        custodian="County Juvenile Court",
        relevance="Determines whether statutory procedural due process notice was provided prior to hearing",
        associated_issue="Notice Requirement",
        verification_state=EvidenceVerificationState.UNVERIFIED_ASSERTION,
        classification=EpistemicClassification.ALLEGATION
    )

    link: LegalBridgeLink = LegalEvidenceBridge.bridge_record(bare_notice)

    # 1. Evidence
    assert link.evidence.id == "EV-NOTICE-01"
    # 2. Fact
    assert "Party allegation" in link.fact_statement or "undated" in link.fact_statement
    # 3. Legal Element
    assert link.legal_element == "Notice Requirement"
    # 4. Authority
    assert "Due Process" in link.authority
    assert "Mullane" in link.authority

    # 5. Missing Evidence (All 5 prompt elements detected!)
    missing_str = " ".join(link.missing_evidence)
    assert "Date" in missing_str
    assert "Recipient" in missing_str
    assert "Method" in missing_str
    assert "Content" in missing_str
    assert "Proof of service" in missing_str

    # 6. Research Questions
    questions_str = " ".join(link.research_questions)
    assert "Was legally required notice provided" in questions_str


def test_warrant_requirement_bridge_and_missing_proof():
    """Verify Fourth Amendment warrant bridge flags missing judicial search warrant and probable cause."""
    warrantless_entry = EvidenceRecord(
        id="EV-SEARCH-01",
        description="Caseworker notes stating worker and police entered the home after knocking",
        source_type="CASEWORKER_NOTE",
        date="2024-04-10",
        author="Caseworker Jones",
        custodian="State Agency",
        relevance="Fourth Amendment home entry and child seizure legality",
        associated_issue="Fourth Amendment Warrant Requirement / Home Entry",
        verification_state=EvidenceVerificationState.UNVERIFIED_ASSERTION,
        classification=EpistemicClassification.ALLEGATION
    )

    link = LegalEvidenceBridge.bridge_record(warrantless_entry)
    assert link.legal_element == "Fourth Amendment Warrant Requirement / Home Entry"
    assert "Doe v. Heck" in link.authority
    assert any("Signed judicial search warrant" in m for m in link.missing_evidence)
    assert any("Sworn probable cause affidavit" in m for m in link.missing_evidence)


def test_collection_evaluation_and_classification_counting():
    """Verify evaluate_collection builds bridge links and counts classifications correctly."""
    records = [
        EvidenceRecord(
            id="EV-1",
            description="Hospital discharge summary showing child in good physical health",
            source_type="MEDICAL_RECORD",
            date="2024-02-01",
            author="Attending Pediatrician",
            custodian="Children's Hospital",
            relevance="Rebuts allegation of severe physical neglect",
            associated_issue="Imminent Physical Danger / Emergency Removal Standard",
            verification_state=EvidenceVerificationState.VERIFIED_PRIMARY_DOCUMENT,
            classification=EpistemicClassification.DOCUMENTED_FACT
        ),
        EvidenceRecord(
            id="EV-2",
            description="Anonymous caller statement alleging loud yelling from residence",
            source_type="HOTLINE_REPORT",
            date="2024-02-02",
            author="Anonymous Intake Caller",
            custodian="Child Welfare Intake Division",
            relevance="Initial referral trigger",
            associated_issue="Notice Requirement",
            verification_state=EvidenceVerificationState.UNVERIFIED_ASSERTION,
            classification=EpistemicClassification.ALLEGATION
        ),
        EvidenceRecord(
            id="EV-3",
            description="Parent testified in open court that caseworker never offered transportation assistance",
            source_type="COURT_TRANSCRIPT",
            date="2024-02-15",
            author="Parent",
            custodian="Superior Court Clerk",
            relevance="Reasonable efforts compliance",
            associated_issue="Reasonable / Active Efforts Requirement",
            verification_state=EvidenceVerificationState.CORROBORATED_BY_RECORDS,
            classification=EpistemicClassification.TESTIMONY
        )
    ]

    evaluation: EvidenceBridgeEvaluation = LegalEvidenceBridge.evaluate_collection(
        case_reference="REF-2024-001",
        jurisdiction="US-WA",
        records=records
    )

    assert len(evaluation.bridge_links) == 3
    assert evaluation.classification_counts[EpistemicClassification.DOCUMENTED_FACT.value] == 1
    assert evaluation.classification_counts[EpistemicClassification.ALLEGATION.value] == 1
    assert evaluation.classification_counts[EpistemicClassification.TESTIMONY.value] == 1
    assert len(evaluation.missing_evidence_summary) > 0
    assert len(evaluation.research_questions_summary) > 0


def test_public_data_safety_rejection_of_private_data():
    """Verify that unredacted SSNs or private filesystem paths are rejected under the zero-private-data mandate."""
    # 1. Unredacted SSN rejection
    bad_ssn_record = EvidenceRecord(
        id="EV-BAD-SSN",
        description="Client background check with SSN 123-45-6789",
        source_type="BACKGROUND_CHECK",
        relevance="Identity check",
        associated_issue="Notice Requirement"
    )
    with pytest.raises(ValueError, match="Social Security Number"):
        LegalEvidenceBridge.bridge_record(bad_ssn_record)

    # 2. Private filesystem path rejection
    bad_path_record = EvidenceRecord(
        id="EV-BAD-PATH",
        description="Private evidence document located at /private_case_vault/secret_case.pdf",
        source_type="FILE_PATH",
        relevance="Document location",
        associated_issue="Notice Requirement"
    )
    with pytest.raises(ValueError, match="private local filesystem path"):
        LegalEvidenceBridge.bridge_record(bad_path_record)
