"""Unit tests for the multi-dimensional Legal Conflict Engine."""

from core.conflicts import (
    AuthorityConflictAnalyzer,
    TemporalConflictAnalyzer,
    JurisdictionConflictAnalyzer,
    StatutoryConflictAnalyzer,
    PrecedentConflictAnalyzer,
    UnresolvedConflictEngine,
)


def test_authority_supremacy_conflict():
    report = AuthorityConflictAnalyzer.evaluate(
        federal_cite="25 U.S.C. § 1912(d)",
        state_cite="RCW 13.34.136",
        topic="active_efforts"
    )
    assert report.conflict_detected is True
    assert report.preemption_type == "EXPRESS"
    assert "Supremacy Clause" in report.supremacy_analysis


def test_temporal_conflict():
    report = TemporalConflictAnalyzer.evaluate(
        event_date_str="2020-01-01",
        effective_date_str="2021-07-01",
        repealed_date_str=None
    )
    assert report.conflict_detected is True
    assert report.is_valid_at_date is False
    assert "TEMPORAL CONFLICT" in report.analysis


def test_jurisdiction_conflict():
    report = JurisdictionConflictAnalyzer.evaluate(
        child_home_state="WA",
        filing_state="IL",
        is_emergency=True
    )
    assert report.conflict_detected is True
    assert report.home_state == "WA"
    assert report.emergency_state == "IL"
    assert "Temporary Emergency Jurisdiction" in report.analysis


def test_statutory_and_precedent_conflicts():
    stat_report = StatutoryConflictAnalyzer.evaluate(
        general_cite="RCW Title 13 General Juvenile Rules",
        specific_cite="RCW 13.34.065 Shelter Care Specific Hearing Rule"
    )
    assert stat_report.conflict_detected is True
    assert "Specific over General" in stat_report.canon_applied

    prec_report = PrecedentConflictAnalyzer.evaluate(
        precedent_a="In re Custody of S.M., 9th Cir.",
        precedent_b="In re Child Custody, 5th Cir.",
        jurisdiction="US-WA"
    )
    assert prec_report.conflict_detected is True
    assert "CIRCUIT_SPLIT" in prec_report.conflict_nature


def test_unresolved_conflict_disclosure():
    disclosure = UnresolvedConflictEngine.disclose(
        topic="Standard for Virtual Family Time as Substitute for In-Person Visitation",
        theory_a="Permissible when public health emergency exists",
        theory_b="Violates statutory right to meaningful family time absent finding of imminent harm"
    )
    assert disclosure.is_unresolved is True
    assert len(disclosure.competing_theories) == 2
    assert "explicitly disclose" in disclosure.abstention_recommendation
