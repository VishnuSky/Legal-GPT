"""Tests for new CLI commands (deadline, timeline, explain-doc, questions)."""

import json
import pytest
from typer.testing import CliRunner
from cli import app

runner = CliRunner()


def test_cli_deadline_formatted():
    """Verify legal-gpt deadline command outputs formatted table/markdown."""
    result = runner.invoke(app, [
        "deadline",
        "--state", "WA",
        "--event", "emergency_removal",
        "--date", "2026-09-17"
    ])
    assert result.exit_code == 0
    assert "Procedural Deadline Calculation" in result.stdout
    assert "RCW 13.34.065" in result.stdout


def test_cli_deadline_json():
    """Verify legal-gpt deadline command with --json outputs valid JSON."""
    result = runner.invoke(app, [
        "deadline",
        "--state", "WA",
        "--event", "emergency_removal",
        "--date", "2026-09-17",
        "--json"
    ])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["event_type"] == "emergency_removal"
    assert data["jurisdiction"] == "WA"
    assert len(data["deadlines"]) >= 1
    assert "RCW 13.34.065" in data["deadlines"][0]["citation"]


def test_cli_timeline_formatted(tmp_path):
    """Verify legal-gpt timeline command processes a JSON file and outputs formatted timeline."""
    events = [
        {"id": "ev-1", "date": "2026-09-17", "title": "Emergency Removal", "category": "REMOVAL", "jurisdiction": "WA"},
        {"id": "ev-2", "date": "2026-09-21", "title": "Shelter Care Hearing", "category": "HEARING", "jurisdiction": "WA"}
    ]
    file_path = tmp_path / "events.json"
    file_path.write_text(json.dumps(events), encoding="utf-8")

    result = runner.invoke(app, [
        "timeline",
        "--file", str(file_path),
        "--state", "WA"
    ])
    assert result.exit_code == 0
    assert "Procedural Case Timeline Analysis" in result.stdout
    assert "Emergency Removal" in result.stdout


def test_cli_timeline_json(tmp_path):
    """Verify legal-gpt timeline command with --json outputs structured JSON."""
    events = {
        "events": [
            {"id": "ev-1", "date": "2026-09-17", "title": "Emergency Removal", "category": "REMOVAL", "jurisdiction": "WA"}
        ]
    }
    file_path = tmp_path / "events.json"
    file_path.write_text(json.dumps(events), encoding="utf-8")

    result = runner.invoke(app, [
        "timeline",
        "--file", str(file_path),
        "--state", "WA",
        "--json"
    ])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["total_events"] == 1
    assert len(data["chronological_events"]) == 1


def test_cli_explain_doc_formatted():
    """Verify legal-gpt explain-doc outputs structured literacy breakdown."""
    result = runner.invoke(app, [
        "explain-doc",
        "--type", "shelter_care_order",
        "--state", "WA"
    ])
    assert result.exit_code == 0
    assert "Legal Document Breakdown" in result.stdout
    assert "Temporary Custody" in result.stdout or "Shelter" in result.stdout
    assert "LEGAL INFORMATION ONLY" in result.stdout


def test_cli_explain_doc_json():
    """Verify legal-gpt explain-doc with --json outputs valid JSON."""
    result = runner.invoke(app, [
        "explain-doc",
        "--type", "summons_and_complaint",
        "--state", "WA",
        "--json"
    ])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["document_title"] == "Summons and Complaint"
    assert len(data["deadlines"]) >= 1


def test_cli_questions_formatted():
    """Verify legal-gpt questions outputs tactical question checklist."""
    result = runner.invoke(app, [
        "questions",
        "--situation", "cps_removal",
        "--audience", "attorney",
        "--state", "WA"
    ])
    assert result.exit_code == 0
    assert "Tactical Question Builder" in result.stdout
    assert "TIER 1" in result.stdout
    assert "RIGHTS" in result.stdout


def test_cli_questions_json():
    """Verify legal-gpt questions with --json outputs valid JSON."""
    result = runner.invoke(app, [
        "questions",
        "--situation", "cps_removal",
        "--audience", "attorney",
        "--state", "WA",
        "--json"
    ])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert len(data["prioritized_questions"]) >= 4
    assert len(data["documents_to_request"]) >= 1
