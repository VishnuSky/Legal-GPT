"""Tests for Parent Rights & Reasonable Efforts Auditor."""

from cps.parent_rights import ParentRightsAuditor


def test_parent_rights_full_compliance():
    checks = ParentRightsAuditor.evaluate_parent_rights(
        state="WA",
        notice_given=True,
        counsel_present=True,
        services_offered=True,
        is_icwa=False
    )
    assert len(checks) == 3
    assert all(c.status == "COMPLIANT" for c in checks)


def test_parent_rights_notice_violation():
    checks = ParentRightsAuditor.evaluate_parent_rights(
        state="IL",
        notice_given=False,
        counsel_present=True,
        services_offered=True,
        is_icwa=False
    )
    notice_check = next(c for c in checks if "Notice" in c.right_name)
    assert notice_check.status == "VIOLATION_SUSPECTED"
    assert "705 ILCS 405/2-15" in notice_check.statutory_citations[0]


def test_parent_rights_counsel_violation():
    checks = ParentRightsAuditor.evaluate_parent_rights(
        state="OH",
        notice_given=True,
        counsel_present=False,
        services_offered=True,
        is_icwa=False
    )
    counsel_check = next(c for c in checks if "Counsel" in c.right_name)
    assert counsel_check.status == "VIOLATION_SUSPECTED"
    assert "ORC § 2151.352" in counsel_check.statutory_citations[0]


def test_parent_rights_icwa_active_efforts():
    checks = ParentRightsAuditor.evaluate_parent_rights(
        state="WA",
        notice_given=True,
        counsel_present=True,
        services_offered=False,
        is_icwa=True
    )
    efforts_check = next(c for c in checks if "Efforts" in c.right_name)
    assert efforts_check.status == "VIOLATION_SUSPECTED"
    assert "Active Efforts" in efforts_check.right_name
    assert "25 U.S.C. § 1912(d)" in efforts_check.statutory_citations
