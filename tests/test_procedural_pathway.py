"""Unit and integration tests for the Legal-GPT Procedural Pathway Engine."""

import pytest
from datetime import date

from core.procedure.models import (
    LegalTrack,
    StageDefinition,
    ProceduralPathwayInput,
    ProceduralPathwayReport,
)
from core.procedure.pathways import PathwayRegistry, ALL_STAGES
from core.procedure.engine import ProceduralPathwayEngine


def test_pathway_registry_coverage_of_all_four_tracks():
    """Verify that the registry contains complete stage sequences for all 4 tracks."""
    all_stages = PathwayRegistry.get_all_stages()
    assert len(all_stages) >= 25

    cps_stages = PathwayRegistry.get_by_track(LegalTrack.CPS_DEPENDENCY)
    assert len(cps_stages) >= 9
    cps_ids = [s.stage_id for s in cps_stages]
    assert "CPS_INVESTIGATION" in cps_ids
    assert "CPS_REMOVAL" in cps_ids
    assert "SHELTER_HEARING" in cps_ids
    assert "ADJUDICATION" in cps_ids
    assert "TERMINATION" in cps_ids
    assert "CPS_APPEAL" in cps_ids

    admin_stages = PathwayRegistry.get_by_track(LegalTrack.ADMINISTRATIVE)
    assert len(admin_stages) >= 5
    admin_ids = [s.stage_id for s in admin_stages]
    assert "ADMIN_NOTICE" in admin_ids
    assert "ADMIN_HEARING" in admin_ids
    assert "JUDICIAL_REVIEW" in admin_ids

    crim_stages = PathwayRegistry.get_by_track(LegalTrack.CRIMINAL)
    assert len(crim_stages) >= 7
    crim_ids = [s.stage_id for s in crim_stages]
    assert "CITATION_OR_ARREST" in crim_ids
    assert "ARRAIGNMENT" in crim_ids
    assert "TRIAL" in crim_ids

    civil_stages = PathwayRegistry.get_by_track(LegalTrack.CIVIL_LITIGATION)
    assert len(civil_stages) >= 7
    civil_ids = [s.stage_id for s in civil_stages]
    assert "CIVIL_COMPLAINT" in civil_ids
    assert "ANSWER_OR_MOTION" in civil_ids
    assert "CIVIL_DISCOVERY" in civil_ids


def test_non_predictive_outcome_rule():
    """Verify that the engine strictly refuses to predict case outcomes or probabilities of success."""
    input_data = ProceduralPathwayInput(
        narrative="CPS removed my 3-year-old child yesterday in Skagit County WA without a warrant. What are my chances of getting my kid back tomorrow?",
        jurisdiction="US-WA"
    )

    report: ProceduralPathwayReport = ProceduralPathwayEngine.map_pathway(input_data)

    # Must contain explicit non-predictive notice
    assert "Legal-GPT does NOT predict case outcomes" in report.epistemic_notice
    assert "Determining the legal result of any stage requires formal judicial adjudication" in report.epistemic_notice

    # Render markdown and verify no predictive language
    md = report.render_markdown()
    assert "## 1. Current Stage" in md
    assert "## 2. Possible Next Stages" in md
    assert "chance of winning" not in md.lower()
    assert "probability of success" not in md.lower()


def test_cps_removal_and_state_specific_statutory_deadlines():
    """Verify CPS emergency removal posture identifies exact state-specific statutory deadlines."""
    # 1. Washington State: 72-hour shelter hearing (RCW 13.34.065)
    wa_input = ProceduralPathwayInput(
        narrative="DCYF caseworkers and police removed my child yesterday afternoon in Seattle.",
        jurisdiction="US-WA"
    )
    wa_report = ProceduralPathwayEngine.map_pathway(wa_input)
    assert wa_report.track == LegalTrack.CPS_DEPENDENCY
    assert wa_report.current_stage.stage_id == "CPS_REMOVAL"
    assert any("72-Hour" in d["label"] or "RCW 13.34.065" in d["statutory_citation"] for d in wa_report.important_dates)
    next_stage_ids = [s.stage_id for s in wa_report.possible_next_stages]
    assert "SHELTER_HEARING" in next_stage_ids

    # 2. Illinois: 48-hour temporary custody hearing (705 ILCS 405/2-9)
    il_input = ProceduralPathwayInput(
        narrative="DCFS investigator took custody of my daughter yesterday in Chicago, Cook County.",
        jurisdiction="US-IL"
    )
    il_report = ProceduralPathwayEngine.map_pathway(il_input)
    assert il_report.track == LegalTrack.CPS_DEPENDENCY
    assert any("48-Hour" in d["label"] or "705 ILCS 405/2-9" in d["statutory_citation"] for d in il_report.important_dates)

    # 3. Florida: 24-hour shelter hearing (Fla. Stat. § 39.402)
    fl_input = ProceduralPathwayInput(
        narrative="DCF took my son into protective custody in Miami Florida.",
        jurisdiction="US-FL"
    )
    fl_report = ProceduralPathwayEngine.map_pathway(fl_input)
    assert any("24-Hour" in d["label"] or "39.402" in d["statutory_citation"] for d in fl_report.important_dates)


def test_administrative_pathway_mapping():
    """Verify mapping of an administrative agency action and appeal."""
    admin_input = ProceduralPathwayInput(
        narrative="I received a formal Notice of Proposed Action from the state licensing department proposing to revoke my day care license.",
        jurisdiction="US-WA"
    )
    report = ProceduralPathwayEngine.map_pathway(admin_input)

    assert report.track == LegalTrack.ADMINISTRATIVE
    assert report.current_stage.stage_id == "ADMIN_NOTICE"
    next_ids = [s.stage_id for s in report.possible_next_stages]
    assert "ADMIN_HEARING" in next_ids
    assert len(report.authority) > 0
    assert any("APA" in a or "34.05" in a or "Administrative" in a for a in report.authority)


def test_criminal_pathway_mapping():
    """Verify mapping of a criminal prosecution stage."""
    crim_input = ProceduralPathwayInput(
        narrative="I was arrested last night and booked into county jail on felony assault charges. I have not seen a judge yet.",
        jurisdiction="US-WA"
    )
    report = ProceduralPathwayEngine.map_pathway(crim_input)

    assert report.track == LegalTrack.CRIMINAL
    assert report.current_stage.stage_id == "CITATION_OR_ARREST"
    next_ids = [s.stage_id for s in report.possible_next_stages]
    assert "CHARGING" in next_ids or "ARRAIGNMENT" in next_ids
    assert any("Riverside" in a or "Probable Cause" in a or "CrR" in a for a in report.authority)


def test_civil_litigation_pathway_and_responsive_deadlines():
    """Verify mapping of civil litigation summons and responsive pleading deadlines."""
    civil_input = ProceduralPathwayInput(
        narrative="A process server served me yesterday with a summons and civil complaint for breach of contract in superior court.",
        jurisdiction="US-WA"
    )
    report = ProceduralPathwayEngine.map_pathway(civil_input)

    assert report.track == LegalTrack.CIVIL_LITIGATION
    assert report.current_stage.stage_id in ("SERVICE_OF_PROCESS", "ANSWER_OR_MOTION")
    assert len(report.documents_to_locate) > 0
    assert any("Summons" in doc for doc in report.documents_to_locate)
    assert len(report.questions_to_ask) > 0


def test_report_completeness_all_nine_required_sections():
    """Verify that the generated report populates all 9 required output sections."""
    input_data = ProceduralPathwayInput(
        narrative="We have our 72-hour shelter care hearing scheduled for tomorrow morning in juvenile court.",
        jurisdiction="US-WA"
    )
    report = ProceduralPathwayEngine.map_pathway(input_data)

    # 1. Current stage
    assert report.current_stage.stage_id == "SHELTER_HEARING"
    # 2. Possible next stages
    assert len(report.possible_next_stages) >= 1
    # 3. Authority
    assert len(report.authority) >= 1
    # 4. Required verification
    assert len(report.required_verification) >= 1
    # 5. Important dates
    assert len(report.important_dates) >= 1
    # 6. Questions to ask
    assert len(report.questions_to_ask) >= 1
    # 7. Documents to locate
    assert len(report.documents_to_locate) >= 1
    # 8. Available review / challenge mechanisms
    assert len(report.available_review_mechanisms) >= 1
    # 9. Unknown facts
    assert len(report.unknown_facts) >= 1

    # Check Markdown rendering contains all 9 sections
    md = report.render_markdown()
    assert "## 1. Current Stage" in md
    assert "## 2. Possible Next Stages" in md
    assert "## 3. Governing Legal Authority" in md
    assert "## 4. Required Procedural Verification" in md
    assert "## 5. Important Dates & Statutory Deadlines" in md
    assert "## 6. Questions to Ask an Attorney or Court Clerk" in md
    assert "## 7. Critical Documents to Locate and Preserve" in md
    assert "## 8. Available Review and Challenge Mechanisms" in md
    assert "## 9. Unknown Facts Dictating Pathway Branches" in md
