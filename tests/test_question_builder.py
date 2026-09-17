"""Tests for Question Builder Module (core/question_builder)."""

import pytest
from fastapi.testclient import TestClient

from core.question_builder.models import (
    TargetRecipient,
    QuestionPriorityTier,
    QuestionBuilderRequest,
    QuestionBuilderReport,
)
from core.question_builder.engine import QuestionBuilderEngine
from core.question_builder.renderer import QuestionBuilderRenderer
from api.server import app


@pytest.fixture
def question_engine():
    return QuestionBuilderEngine()


@pytest.fixture
def test_client():
    return TestClient(app)


def test_attorney_emergency_removal_priority_hierarchy(question_engine):
    """Verifies questions for attorney in emergency removal follow strict 4-tier priority order."""
    req = QuestionBuilderRequest(
        situation="emergency_removal",
        target_recipient="ATTORNEY",
        jurisdiction="WA",
        user_role="parent"
    )
    report = question_engine.build_questions(req)

    assert len(report.prioritized_questions) >= 4
    tiers = [q.priority_tier for q in report.prioritized_questions]
    # Verify non-decreasing order (1 <= 2 <= 3 <= 4)
    assert tiers == sorted(tiers)

    # Verify Tier 1 is Rights
    tier_1_items = [q for q in report.prioritized_questions if q.priority_tier == 1]
    assert len(tier_1_items) >= 1
    assert all(q.category == "RIGHTS" for q in tier_1_items)
    assert any("ICWA" in q.question_text or "imminent risk" in q.question_text for q in tier_1_items)

    # Verify Tier 2 is Deadlines
    tier_2_items = [q for q in report.prioritized_questions if q.priority_tier == 2]
    assert len(tier_2_items) >= 1
    assert all(q.category == "DEADLINES" for q in tier_2_items)


def test_caseworker_service_plan_meeting(question_engine):
    """Verifies caseworker questions focus on visitation, service nexus, and provider waiting lists."""
    req = QuestionBuilderRequest(
        situation="service_plan_meeting",
        target_recipient="CASEWORKER",
        jurisdiction="IL",
        user_role="parent"
    )
    report = question_engine.build_questions(req)

    assert report.target_recipient == "CASEWORKER"
    questions_text = " ".join(q.question_text.lower() for q in report.prioritized_questions)
    assert "visitation" in questions_text
    assert "service" in questions_text

    # Check documentation request
    assert any("Individualized Service Plan" in d or "ISP" in d for d in report.documents_to_request)


def test_checklists_and_tactical_tips(question_engine):
    """Verifies document checklists and tactical tips are properly populated."""
    req = QuestionBuilderRequest(
        situation="shelter_hearing",
        target_recipient="ALL",
        jurisdiction="FL",
        user_role="parent"
    )
    report = question_engine.build_questions(req)

    assert len(report.documents_to_request) >= 3
    assert any("Petition" in d for d in report.documents_to_request)
    assert len(report.documents_to_bring) >= 3
    assert any("relatives" in d.lower() or "identification" in d.lower() for d in report.documents_to_bring)
    assert len(report.tactical_tips) >= 2


def test_question_builder_renderer_markdown(question_engine):
    req = QuestionBuilderRequest(
        situation="emergency_removal",
        target_recipient="ATTORNEY",
        jurisdiction="WA",
        user_role="parent"
    )
    report = question_engine.build_questions(req)
    md = QuestionBuilderRenderer.render_markdown(report)

    assert "Tactical Question Builder: Emergency Removal" in md
    assert "TIER 1 — RIGHTS" in md
    assert "TIER 2 — DEADLINES" in md
    assert "Documents to Request From Agency" in md
    assert "Documents to Bring / Prepare" in md
    assert "Tactical Tips & Best Practices" in md


def test_question_builder_public_api_endpoint(test_client):
    """Tests POST /api/v1/public/question-builder endpoint."""
    payload = {
        "situation": "emergency_removal",
        "target_recipient": "ATTORNEY",
        "jurisdiction": "WA",
        "user_role": "parent"
    }
    response = test_client.post("/api/v1/public/question-builder", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["prioritized_questions"]) >= 4
    assert len(data["documents_to_request"]) >= 1
    assert "markdown" in data
