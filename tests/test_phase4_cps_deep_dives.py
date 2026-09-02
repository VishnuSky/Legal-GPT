"""Unit and Integration Tests for Phase 4: CPS Domain Deep Dives & Evidence Manager Bridge."""

import pytest
from cps.evidence_matrix import (
    EvidenceType,
    EvidentiarySufficiencyLevel,
    CaseEvidenceItem,
    EvidenceMatrixEngine,
    EvidentiaryMatrixEvaluation,
)
from cps.evidence_bridge import ExternalEvidenceContract, EvidenceBridgeEngine
from cps.pleading_generator import (
    PleadingDraftRequest,
    PleadingDraftResponse,
    PleadingGenerator,
)
from cps.due_process_audit import (
    DueProcessAuditor,
    DueProcessAuditReport,
    DueProcessRightCheck,
)


def test_evidence_matrix_classification_and_gaps():
    items = [
        CaseEvidenceItem(
            item_id="ITEM-001",
            description="Uncorroborated intake allegation regarding home condition.",
            evidence_type=EvidenceType.UNVERIFIED_ALLEGATION,
            source_agency_or_person="Intake Worker",
            statutory_element_targeted="Imminent Physical Danger"
        ),
        CaseEvidenceItem(
            item_id="ITEM-002",
            description="Contested neighbor statement regarding noise.",
            evidence_type=EvidenceType.DISPUTED_FACT,
            source_agency_or_person="Anonymous Report",
            statutory_element_targeted="Environmental Safety"
        ),
        CaseEvidenceItem(
            item_id="ITEM-003",
            description="Certified negative urinalysis toxicology laboratory report.",
            evidence_type=EvidenceType.DOCUMENTED_EXHIBIT,
            source_agency_or_person="Certified Laboratory Exhibit A",
            statutory_element_targeted="Substance Impairment"
        )
    ]

    evaluation = EvidenceMatrixEngine.evaluate_evidence_items(
        jurisdiction="US-WA",
        stage="EMERGENCY_REMOVAL",
        evidence_items=items
    )

    assert evaluation.total_items_analyzed == 3
    assert evaluation.unverified_allegations_count == 1
    assert evaluation.disputed_facts_count == 1
    assert evaluation.documented_exhibits_count == 1
    assert evaluation.sufficiency_rating == EvidentiarySufficiencyLevel.MARGINAL
    assert len(evaluation.evidentiary_gaps) >= 1
    assert "Motion to Preclude" in evaluation.evidentiary_gaps[0].rebuttal_strategy


def test_evidence_bridge_contract_parsing():
    contract = ExternalEvidenceContract(
        external_case_id="[ANONYMIZED_CASE_REFERENCE]",
        jurisdiction="US-IL",
        cps_stage="TEMPORARY_CUSTODY",
        items=[
            {
                "id": "ITEM-1",
                "description": "Allegation of inadequate food",
                "type": "UNVERIFIED_ALLEGATION",
                "statutory_element": "Physical Neglect"
            },
            {
                "id": "ITEM-2",
                "description": "Doctor physical examination report confirming healthy child",
                "type": "DOCUMENTED_EXHIBIT",
                "statutory_element": "Medical Health"
            }
        ]
    )

    evaluation = EvidenceBridgeEngine.ingest_and_evaluate_contract(contract)
    assert evaluation.jurisdiction == "US-IL"
    assert evaluation.total_items_analyzed == 2
    assert evaluation.documented_exhibits_count == 1
    assert evaluation.unverified_allegations_count == 1


def test_pleading_generator_multi_state():
    # Washington State Shelter Rehearing
    wa_req = PleadingDraftRequest(
        state="WA",
        motion_type="shelter_rehearing",
        county="District 1",
        case_number="[CAUSE_NO_REDACTED]",
        factual_basis="Parent lacked notice and relative home is available."
    )
    wa_draft = PleadingGenerator.generate_pleading(wa_req)
    assert "MOTION AND AFFIDAVIT FOR REHEARING" in wa_draft.title
    assert "13.34.065" in wa_draft.governing_rule_and_statute
    assert "SUPERIOR COURT" in wa_draft.caption
    assert "JuCR 2.4" in wa_draft.governing_rule_and_statute

    # New York Section 1028 Application
    ny_req = PleadingDraftRequest(
        state="NY",
        motion_type="section_1028",
        county="District 2",
        case_number="[CAUSE_NO_REDACTED]",
        factual_basis="No imminent risk to life or health under Nicholson standard."
    )
    ny_draft = PleadingGenerator.generate_pleading(ny_req)
    assert "APPLICATION FOR RETURN" in ny_draft.title
    assert "1028" in ny_draft.governing_rule_and_statute
    assert "Nicholson v. Scoppetta" in ny_draft.body_markdown

    # ICWA Intervention & Invalidation
    icwa_req = PleadingDraftRequest(
        state="ICWA",
        motion_type="icwa_intervention",
        county="District 3",
        case_number="[CAUSE_NO_REDACTED]",
        factual_basis="State court failed to send registered mail notice to Tribe."
    )
    icwa_draft = PleadingGenerator.generate_pleading(icwa_req)
    assert "TRIBAL INTERVENTION" in icwa_draft.title
    assert "1914" in icwa_draft.governing_rule_and_statute
    assert "Haaland v. Brackeen" in icwa_draft.body_markdown


def test_due_process_auditor_all_pillars():
    # Case with full compliance
    compliant_report: DueProcessAuditReport = DueProcessAuditor.audit_case(
        state="WA",
        stage="EMERGENCY_REMOVAL",
        notice_served_personally=True,
        counsel_appointed=True,
        counsel_present_at_hearing=True,
        relative_placement_explored=True,
        services_tailored_and_offered=True,
        family_visitation_ordered=True,
        is_icwa_eligible=False,
        statutory_deadline_met=True
    )
    assert compliant_report.violations_count == 0
    assert compliant_report.overall_due_process_health_score == 1.0

    # Case with multiple due process violations (Notice, Counsel, Deadlines)
    violation_report: DueProcessAuditReport = DueProcessAuditor.audit_case(
        state="WA",
        stage="EMERGENCY_REMOVAL",
        notice_served_personally=False,
        counsel_appointed=False,
        counsel_present_at_hearing=False,
        relative_placement_explored=False,
        services_tailored_and_offered=False,
        family_visitation_ordered=False,
        is_icwa_eligible=True,
        tribal_notice_registered_mail=False,
        statutory_deadline_met=False
    )
    assert violation_report.violations_count >= 5
    assert violation_report.overall_due_process_health_score <= 0.20
    assert any("1914" in c.guaranteeing_authority for c in violation_report.checks)
    assert any("Lassiter" in c.guaranteeing_authority for c in violation_report.checks)
