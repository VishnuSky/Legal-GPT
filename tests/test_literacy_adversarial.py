"""Adversarial and Literacy Safety Tests (Days 10-11)."""

import pytest
from core.literacy.engine import LegalLiteracyEngine
from core.literacy.models import LiteracyLevel, DrillDownAction
from core.question_builder.models import QuestionBuilderRequest
from core.question_builder.engine import QuestionBuilderEngine
from core.deadlines.engine import DeadlineEngine


def test_adversarial_crisis_query_never_concludes_violation():
    """Verify that inflammatory/crisis user queries return objective legal information without declaring violations."""
    crisis_queries = [
        "they took my kid illegally",
        "CPS kidnapped my children without a warrant",
        "the caseworker lied and violated my civil rights"
    ]
    for q in crisis_queries:
        exp = LegalLiteracyEngine.explain(q, jurisdiction="WA")
        full_text = " ".join([
            exp.level_1_plain_english,
            exp.level_2_practical,
            exp.level_3_terminology,
            exp.level_5_advanced_analysis
        ]).lower()

        # System must NEVER declare that the user's rights were violated in fact
        assert "your rights were violated" not in full_text
        assert "the agency acted illegally in your case" not in full_text
        assert "you have a winning lawsuit" not in full_text
        assert "cps broke the law in your case" not in full_text

        # Disclaimer must always be present
        assert "legal information only" in exp.disclaimer.lower()
        assert "not legal advice" in exp.disclaimer.lower()


def test_cross_state_queries_wa_vs_il_isolation():
    """Verify that WA and IL queries strictly isolate binding authority."""
    exp_wa = LegalLiteracyEngine.explain("shelter_care_hearing", jurisdiction="WA")
    exp_il = LegalLiteracyEngine.explain("shelter_care_hearing", jurisdiction="IL")

    # WA query must bind RCW, not ILCS
    wa_cites = [a for a in exp_wa.level_4_primary_authority if a.is_binding]
    assert any("RCW" in a.citation or a.jurisdiction in ("US", "FED") for a in wa_cites)
    assert not any("ILCS" in a.citation for a in wa_cites)

    # IL query must bind ILCS, not RCW
    il_cites = [a for a in exp_il.level_4_primary_authority if a.is_binding]
    assert any("ILCS" in a.citation or a.jurisdiction in ("US", "FED") for a in il_cites)
    assert not any("RCW" in a.citation for a in il_cites)


def test_federal_only_concepts_labeled_federal_not_county():
    """Verify that federal ICWA and constitutional concepts are labeled US/FED, never county rule."""
    exp_icwa = LegalLiteracyEngine.explain("icwa_inquiry", jurisdiction="WA")
    for auth in exp_icwa.level_4_primary_authority:
        if "U.S.C." in auth.citation or "C.F.R." in auth.citation:
            assert auth.jurisdiction in ("US", "FED", "US-FED")
            assert "county" not in auth.jurisdiction.lower()


def test_question_builder_never_declares_court_violated_due_process():
    """Verify that question builder outputs tactical inquiries for the parent without asserting court violations."""
    from core.question_builder.renderer import QuestionBuilderRenderer
    req = QuestionBuilderRequest(
        situation="cps_removal",
        target_recipient="attorney",
        jurisdiction="WA",
        user_role="parent"
    )
    report = QuestionBuilderEngine().build_questions(req)
    all_q_text = " ".join([q.question_text for q in report.prioritized_questions]).lower()

    assert "the court violated your due process" not in all_q_text
    assert "your rights were definitely infringed" not in all_q_text
    rendered = QuestionBuilderRenderer.render_markdown(report)
    assert "disclaimer" in rendered.lower()
    assert "informational" in rendered.lower()


def test_deadlines_deferred_to_deadline_engine():
    """Verify that procedural deadline calculations route to DeadlineEngine without guessing in prose."""
    engine = DeadlineEngine()
    report_wa = engine.compute_deadlines(
        event_type="emergency_removal",
        event_date="2026-09-17",
        jurisdiction="WA"
    )
    assert report_wa.deadlines
    # Shelter care hearing in WA is 72 hours excluding weekends/holidays
    shelter_deadline = next((d for d in report_wa.deadlines if "shelter" in d.name.lower()), None)
    assert shelter_deadline is not None
    assert "13.34" in shelter_deadline.authority
    assert "72 hours" in shelter_deadline.notes.lower() or "hours" in shelter_deadline.notes.lower()
