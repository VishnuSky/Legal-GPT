"""Tests for CPS Case Lifecycle & Stage Requirements."""

from cps.lifecycle import CPSLifecycleEngine, CPSStage


def test_wa_shelter_care_requirements():
    req = CPSLifecycleEngine.get_stage_requirements("WA", CPSStage.SHELTER_CARE_HEARING)
    assert req is not None
    assert "72 hours" in req.required_notice_hours_or_days
    assert req.controlling_statute == "RCW 13.34.065"
    assert req.right_to_counsel_appointed is True


def test_il_shelter_care_requirements():
    req = CPSLifecycleEngine.get_stage_requirements("IL", CPSStage.SHELTER_CARE_HEARING)
    assert req is not None
    assert "48 hours" in req.required_notice_hours_or_days
    assert "705 ILCS 405/2-10" in req.controlling_statute


def test_oh_shelter_care_requirements():
    req = CPSLifecycleEngine.get_stage_requirements("OH", CPSStage.SHELTER_CARE_HEARING)
    assert req is not None
    assert "72 hours" in req.required_notice_hours_or_days
    assert "ORC § 2151.314" in req.controlling_statute
