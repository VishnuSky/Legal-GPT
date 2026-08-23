"""Unit and Integration Tests for Phase 3 Relational Citation Graph & Citator Engine."""

import pytest
from datetime import date
from knowledge_graph.relational_graph import (
    LegalCitatorGraph,
    CitatorReport,
    CitatorSignal,
    RelationType,
    citator_graph,
)
from knowledge_graph.point_in_time_diff import PointInTimeDiffEngine, StatutoryDiffResult
from storage.db import LegalDatabase


def test_citator_good_law_evaluation():
    report: CitatorReport = citator_graph.evaluate_citator_status("25 U.S.C. § 1901")
    assert report.is_good_law is True
    assert report.overall_signal == CitatorSignal.GOOD_LAW
    assert report.positive_count >= 1
    assert any("Haaland v. Brackeen" in r["source_citation"] for r in report.citing_references)


def test_citator_interpreting_statute_evaluation():
    report: CitatorReport = citator_graph.evaluate_citator_status("RCW 13.34.065")
    assert report.is_good_law is True
    assert report.citing_authorities_count >= 1
    assert any("In re Dependency of K.N.J." in r["source_citation"] for r in report.citing_references)


def test_citator_negative_treatment_handling():
    # Insert a simulated overruled case edge
    db = LegalDatabase()
    db.insert_relationship(
        source_citation="Overruling Court Decision, 999 U.S. 1",
        target_citation="Old Overruled Case, 100 U.S. 50",
        relation_type=RelationType.OVERRULES.value,
        treatment_signal=CitatorSignal.NEGATIVE.value,
        context_snippet="Expressly overruled on Due Process grounds."
    )

    report = citator_graph.evaluate_citator_status("Old Overruled Case, 100 U.S. 50")
    assert report.is_good_law is False
    assert report.overall_signal == CitatorSignal.NEGATIVE
    assert report.negative_count >= 1
    assert "WARNING" in report.treatment_summary


def test_point_in_time_statutory_diff():
    diff_res: StatutoryDiffResult = PointInTimeDiffEngine.diff_statute_at_dates(
        citation="RCW 13.34.065",
        date_a=date(2015, 1, 1),
        date_b=date(2024, 1, 1),
        jurisdiction="US-WA"
    )
    assert diff_res.has_differences is True
    assert diff_res.version_a_id == "WA-RCW-13.34.065-2009"
    assert diff_res.version_b_id == "WA-RCW-13.34.065-2021"
    assert "SB 5118" in diff_res.analysis or "+" in diff_res.diff_unified_text


def test_point_in_time_identical_dates():
    diff_res: StatutoryDiffResult = PointInTimeDiffEngine.diff_statute_at_dates(
        citation="RCW 13.34.065",
        date_a=date(2023, 1, 1),
        date_b=date(2024, 1, 1),
        jurisdiction="US-WA"
    )
    assert diff_res.has_differences is False
    assert diff_res.additions_count == 0
    assert diff_res.deletions_count == 0
    assert "identical" in diff_res.analysis
