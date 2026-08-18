"""Tests for Temporal Law & Policy Engine."""

from datetime import date
from core.temporal import TemporalEngine
from normalization.models import TemporalMetadata


def test_temporal_validity_active_law():
    meta = TemporalMetadata(
        enacted_date=date(2020, 1, 1),
        effective_date=date(2020, 7, 1),
        repealed_date=None,
        is_current=True
    )
    # Query for 2022-06-15 (should be valid)
    result = TemporalEngine.check_validity_on_date(meta, date(2022, 6, 15))
    assert result.is_valid_on_date is True


def test_temporal_validity_before_effective_date():
    meta = TemporalMetadata(
        enacted_date=date(2024, 1, 1),
        effective_date=date(2024, 7, 1),
        repealed_date=None,
        is_current=True
    )
    # Query for 2023-05-01 (should NOT be valid yet)
    result = TemporalEngine.check_validity_on_date(meta, date(2023, 5, 1))
    assert result.is_valid_on_date is False
    assert "not yet in effect" in result.reason


def test_temporal_validity_after_repeal():
    meta = TemporalMetadata(
        enacted_date=date(2010, 1, 1),
        effective_date=date(2010, 6, 1),
        repealed_date=date(2021, 12, 31),
        is_current=False
    )
    # Query for 2023-01-01 (should be invalid due to repeal)
    result = TemporalEngine.check_validity_on_date(meta, date(2023, 1, 1))
    assert result.is_valid_on_date is False
    assert "repealed" in result.reason
