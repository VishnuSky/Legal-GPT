"""Tests for Deadline Engine (core/deadlines)."""

import pytest
from datetime import date
from fastapi.testclient import TestClient

from core.deadlines.models import DeadlineRequest, DeadlineReport, Deadline
from core.deadlines.calculator import DeadlineCalculator
from core.deadlines.engine import DeadlineEngine
from core.deadlines.renderer import DeadlineRenderer
from api.server import app


@pytest.fixture
def deadline_engine():
    return DeadlineEngine()


@pytest.fixture
def test_client():
    return TestClient(app)


def test_calculator_court_days_skips_weekends():
    # 2026-03-06 is a Friday.
    friday = date(2026, 3, 6)
    # Adding 1 court day should land on Monday 2026-03-09
    next_day = DeadlineCalculator.add_court_days(friday, 1)
    assert next_day == date(2026, 3, 9)

    # Adding 3 court days from Friday (72 hours court time):
    # Friday -> Day 1 (Mon 3/9), Day 2 (Tue 3/10), Day 3 (Wed 3/11)
    three_court_days = DeadlineCalculator.add_court_days(friday, 3)
    assert three_court_days == date(2026, 3, 11)


def test_washington_emergency_removal_72h(deadline_engine):
    """WA emergency removal triggers 72h shelter hearing under RCW 13.34.065."""
    # 2026-03-04 is a Wednesday. 72 hours = 3 court days -> Monday 2026-03-09 (skips Sat/Sun)
    report = deadline_engine.compute_deadlines(
        event_type="emergency_removal",
        event_date="2026-03-04",
        jurisdiction="WA",
        county="King"
    )
    assert report.is_known_event is True
    assert len(report.deadlines) >= 1

    shelter = next((d for d in report.deadlines if "Shelter" in d.name), None)
    assert shelter is not None
    assert "RCW 13.34.065" in shelter.citation
    assert shelter.due_date == "2026-03-09"
    assert shelter.calendar_or_court_days == "court_days"
    assert shelter.verification_status == "VERIFIED"


def test_illinois_petition_filed_30d(deadline_engine):
    """IL dependency petition triggers 30-day adjudicatory hearing under 705 ILCS 405/2-14."""
    report = deadline_engine.compute_deadlines(
        event_type="petition_filed",
        event_date="2026-04-01",
        jurisdiction="IL",
        county="Cook"
    )
    assert report.is_known_event is True
    assert len(report.deadlines) >= 1

    adjudication = next((d for d in report.deadlines if "Adjudicatory" in d.name), None)
    assert adjudication is not None
    assert "705 ILCS 405/2-14" in adjudication.citation
    assert adjudication.due_date == "2026-05-01"
    assert adjudication.verification_status == "VERIFIED"


def test_florida_emergency_removal_24h(deadline_engine):
    """FL requires shelter hearing strictly within 24 hours under Fla. Stat. § 39.402."""
    report = deadline_engine.compute_deadlines(
        event_type="emergency_removal",
        event_date="2026-05-10",
        jurisdiction="FL"
    )
    assert report.is_known_event is True
    shelter = report.deadlines[0]
    assert "39.402" in shelter.citation
    assert shelter.due_date == "2026-05-11"
    assert shelter.calendar_or_court_days == "calendar_days"


def test_unknown_jurisdiction_zero_guessing(deadline_engine):
    """Unknown jurisdiction returns UNKNOWN with authority gap notes, never inventing deadlines."""
    report = deadline_engine.compute_deadlines(
        event_type="emergency_removal",
        event_date="2026-03-01",
        jurisdiction="XX_FANTASY_LAND"
    )
    assert report.is_known_event is False
    assert len(report.deadlines) == 1
    d = report.deadlines[0]
    assert d.due_date == "UNKNOWN"
    assert d.verification_status == "UNKNOWN_AUTHORITY_GAP"
    assert "refuses to guess" in d.notes


def test_invalid_event_date(deadline_engine):
    """Malformed event dates are caught and returned with validation error."""
    report = deadline_engine.compute_deadlines(
        event_type="emergency_removal",
        event_date="not-a-real-date",
        jurisdiction="WA"
    )
    assert report.is_known_event is False
    assert report.error is not None
    assert len(report.warnings) > 0


def test_deadline_renderer_markdown(deadline_engine):
    report = deadline_engine.compute_deadlines(
        event_type="emergency_removal",
        event_date="2026-03-04",
        jurisdiction="WA"
    )
    md = DeadlineRenderer.render_markdown(report)
    assert "Procedural Deadline Calculation" in md
    assert "RCW 13.34.065" in md
    assert "VERIFIED" in md
    assert "2026-03-09" in md


def test_public_deadlines_api_endpoint(test_client):
    """Verify POST /api/v1/public/deadlines endpoint returns valid response."""
    payload = {
        "event_type": "emergency_removal",
        "event_date": "2026-03-04",
        "jurisdiction": "WA",
        "county": "King"
    }
    response = test_client.post("/api/v1/public/deadlines", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "deadlines" in data
    assert len(data["deadlines"]) >= 1
    assert data["deadlines"][0]["due_date"] == "2026-03-09"
    assert "markdown" in data
