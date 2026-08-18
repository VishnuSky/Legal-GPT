"""Tests for Legal Source Registry integrity and schema compliance."""

from legal_registry.loader import default_registry


def test_federal_sources_loaded():
    assert len(default_registry.federal_sources) >= 5
    assert "FED_USCODE" in default_registry.federal_sources
    assert "FED_GOVINFO" in default_registry.federal_sources
    assert "FED_COURTLISTENER" in default_registry.federal_sources


def test_50_state_matrix_completeness():
    # Verify all 50 states + DC are present
    assert len(default_registry.state_matrix) >= 51
    assert "WA" in default_registry.state_matrix
    assert "IL" in default_registry.state_matrix
    assert "OH" in default_registry.state_matrix
    assert "CA" in default_registry.state_matrix
    assert "NY" in default_registry.state_matrix
    assert "TX" in default_registry.state_matrix


def test_cps_sources_loaded():
    assert len(default_registry.cps_sources) >= 5
    assert "CPS_FED_CAPTA" in default_registry.cps_sources
    assert "CPS_FED_ICWA" in default_registry.cps_sources
    assert "CPS_WA_RCW_13_34" in default_registry.cps_sources
    assert "CPS_IL_705_ILCS_405" in default_registry.cps_sources
    assert "CPS_OH_ORC_2151" in default_registry.cps_sources


def test_court_registry():
    assert len(default_registry.courts) >= 5
    assert "FED-SCOTUS" in default_registry.courts
    assert "WA-SKAGIT-SUPERIOR" in default_registry.courts
    assert "IL-COOK-JUVENILE" in default_registry.courts
