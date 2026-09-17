"""Tests for Timeline Construction Engine (core/timeline)."""

import pytest
from fastapi.testclient import TestClient

from core.timeline.models import (
    TimelineEvent,
    TimelineRequest,
    TimelineReport,
    EventCategory,
    SequenceFlag,
)
from core.timeline.engine import TimelineEngine
from core.timeline.renderer import TimelineRenderer
from api.server import app


@pytest.fixture
def timeline_engine():
    return TimelineEngine()


@pytest.fixture
def test_client():
    return TestClient(app)


def test_unordered_events_sorted_chronologically(timeline_engine):
    """Verifies that events provided out of chronological order are sorted properly."""
    raw_events = [
        TimelineEvent(
            id="ev-3",
            date="2026-04-10",
            title="Adjudicatory Hearing",
            category=EventCategory.HEARING.value
        ),
        TimelineEvent(
            id="ev-1",
            date="2026-03-01",
            title="Emergency Removal",
            category=EventCategory.REMOVAL.value
        ),
        TimelineEvent(
            id="ev-2",
            date="2026-03-04",
            title="Shelter Care Hearing",
            category=EventCategory.HEARING.value
        ),
    ]

    req = TimelineRequest(events=raw_events, default_jurisdiction="WA")
    report = timeline_engine.construct_timeline(req)

    assert report.total_events == 3
    event_ids = [e.id for e in report.chronological_events]
    assert event_ids == ["ev-1", "ev-2", "ev-3"]


def test_missing_shelter_hearing_flagged(timeline_engine):
    """Removal without a subsequent judicial shelter hearing triggers a CRITICAL defect."""
    raw_events = [
        TimelineEvent(
            id="ev-1",
            date="2026-03-01",
            title="Emergency Protective Custody Removal",
            category=EventCategory.REMOVAL.value,
            jurisdiction="WA"
        ),
        TimelineEvent(
            id="ev-2",
            date="2026-03-20",
            title="Permanency Planning Conference",
            category=EventCategory.CONFERENCE.value,
            jurisdiction="WA"
        ),
    ]

    req = TimelineRequest(events=raw_events, default_jurisdiction="WA")
    report = timeline_engine.construct_timeline(req)

    assert any(i.issue_type == "MISSING_SHELTER_HEARING" for i in report.detected_issues)
    critical_issue = next(i for i in report.detected_issues if i.issue_type == "MISSING_SHELTER_HEARING")
    assert critical_issue.severity == "CRITICAL"
    assert "ev-1" in critical_issue.affected_events
    assert report.chronological_events[0].flags == [SequenceFlag.MISSING_REQUIRED_EVENT.value]


def test_out_of_sequence_adjudication_before_petition(timeline_engine):
    """Adjudicatory trial conducted before any dependency petition is filed triggers a defect."""
    raw_events = [
        TimelineEvent(
            id="ev-1",
            date="2026-03-01",
            title="Emergency Removal",
            category=EventCategory.REMOVAL.value
        ),
        TimelineEvent(
            id="ev-2",
            date="2026-03-04",
            title="Shelter Care Hearing",
            category=EventCategory.HEARING.value
        ),
        TimelineEvent(
            id="ev-3",
            date="2026-03-15",
            title="Adjudicatory Trial",
            category=EventCategory.HEARING.value
        ),
    ]

    req = TimelineRequest(events=raw_events, default_jurisdiction="WA")
    report = timeline_engine.construct_timeline(req)

    assert any(i.issue_type == "OUT_OF_SEQUENCE_ADJUDICATION" for i in report.detected_issues)
    adj_issue = next(i for i in report.detected_issues if i.issue_type == "OUT_OF_SEQUENCE_ADJUDICATION")
    assert adj_issue.severity == "CRITICAL"
    assert "ev-3" in adj_issue.affected_events


def test_mid_case_jurisdiction_shift_uccjea(timeline_engine):
    """Timeline spanning multiple states triggers UCCJEA conflict warning."""
    raw_events = [
        TimelineEvent(
            id="ev-1",
            date="2026-01-10",
            title="Child Protective Investigation in Washington",
            category=EventCategory.INVESTIGATION.value,
            jurisdiction="WA"
        ),
        TimelineEvent(
            id="ev-2",
            date="2026-03-01",
            title="Emergency Custody Petition filed in Texas",
            category=EventCategory.PETITION.value,
            jurisdiction="TX"
        ),
    ]

    req = TimelineRequest(events=raw_events)
    report = timeline_engine.construct_timeline(req)

    assert report.has_jurisdiction_shift is True
    assert set(report.jurisdictions_involved) == {"WA", "TX"}
    uccjea_issue = next((i for i in report.detected_issues if i.issue_type == "JURISDICTION_SHIFT"), None)
    assert uccjea_issue is not None
    assert "UCCJEA" in uccjea_issue.description


def test_timeline_renderer_markdown(timeline_engine):
    raw_events = [
        TimelineEvent(
            id="ev-1",
            date="2026-03-01",
            title="Emergency Removal",
            category=EventCategory.REMOVAL.value,
            jurisdiction="WA"
        ),
        TimelineEvent(
            id="ev-2",
            date="2026-03-04",
            title="Shelter Hearing",
            category=EventCategory.HEARING.value,
            jurisdiction="WA"
        ),
    ]
    report = timeline_engine.construct_timeline(TimelineRequest(events=raw_events))
    md = TimelineRenderer.render_markdown(report)
    assert "Procedural Case Timeline Analysis" in md
    assert "Chronological Sequence of Events" in md
    assert "Procedural Flow Diagram" in md


def test_timeline_public_api_endpoint(test_client):
    """Tests POST /api/v1/public/timeline endpoint."""
    payload = {
        "events": [
            {
                "id": "ev-1",
                "date": "2026-03-01",
                "title": "Emergency Removal",
                "category": "REMOVAL",
                "jurisdiction": "WA"
            },
            {
                "id": "ev-2",
                "date": "2026-03-04",
                "title": "Shelter Hearing",
                "category": "HEARING",
                "jurisdiction": "WA"
            }
        ],
        "default_jurisdiction": "WA",
        "case_type": "cps_dependency"
    }

    response = test_client.post("/api/v1/public/timeline", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_events"] == 2
    assert len(data["chronological_events"]) == 2
    assert "markdown" in data
