"""Tests for 50-State + DC + Territories Registry Expansion (Mission 1)."""

import pytest
import yaml
from pathlib import Path
from legal_registry.loader import default_registry

REGISTRY_DIR = Path(__file__).resolve().parent.parent / "legal_registry"
STATES_DIR = REGISTRY_DIR / "states"
MATRIX_FILE = STATES_DIR / "matrix.yaml"

US_50_STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

GROUP_1_STATES = [
    "AZ", "CO", "WI", "MN", "MO", "IN", "TN", "MD", "OR", "NM", "WA_TRIBAL"
]

TERRITORIES_AND_SPECIAL = [
    "DC", "PR", "GU", "VI", "AS", "CNMI", "WA_TRIBAL"
]


def test_all_50_state_codes_in_matrix():
    """All 50 state codes must be present in matrix.yaml."""
    with open(MATRIX_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    states = data.get("states", {})
    for code in US_50_STATES:
        assert code in states, f"State code {code} missing from matrix.yaml"


def test_territories_and_dc_in_matrix():
    """DC and key territories must be present in matrix.yaml."""
    with open(MATRIX_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    states = data.get("states", {})
    for code in ["DC", "PR", "GU", "VI", "AS", "CNMI"]:
        assert code in states, f"Jurisdiction {code} missing from matrix.yaml"


def test_group_1_states_marked_verified():
    """GROUP 1 states must have verification_status VERIFIED and deep_implementation true."""
    with open(MATRIX_FILE, "r", encoding="utf-8") as f:
        matrix_data = yaml.safe_load(f).get("states", {})

    for code in GROUP_1_STATES:
        # Check matrix
        assert matrix_data.get(code, {}).get("deep_implementation") is True, (
            f"State {code} must have deep_implementation: true in matrix.yaml"
        )

        # Check state YAML
        yaml_file = STATES_DIR / f"{code}.yaml"
        assert yaml_file.exists(), f"State file {yaml_file} does not exist"
        with open(yaml_file, "r", encoding="utf-8") as f:
            state_data = yaml.safe_load(f)
        assert state_data.get("verification_status") == "VERIFIED", (
            f"State {code} verification_status is {state_data.get('verification_status')}, expected VERIFIED"
        )
        assert len(state_data.get("verified_sources", [])) > 0, (
            f"State {code} must have verified_sources list"
        )


def test_group_2_states_legislature_url_not_empty_status_partial():
    """GROUP 2 states must have non-empty legislature_url and verification_status PARTIAL."""
    verified_codes = set(GROUP_1_STATES) | {
        "WA", "IL", "OH", "CA", "TX", "NY", "FL", "PA", "GA", "NC", "MI", "NJ", "VA"
    }
    all_codes = set(US_50_STATES) | set(TERRITORIES_AND_SPECIAL)
    group_2_codes = all_codes - verified_codes

    for code in group_2_codes:
        yaml_file = STATES_DIR / f"{code}.yaml"
        assert yaml_file.exists(), f"Scaffold YAML missing for {code}"
        with open(yaml_file, "r", encoding="utf-8") as f:
            state_data = yaml.safe_load(f)

        assert state_data.get("verification_status") == "PARTIAL", (
            f"Group 2 jurisdiction {code} status is {state_data.get('verification_status')}, expected PARTIAL"
        )
        leg_url = state_data.get("legislature_url", "")
        assert leg_url and leg_url.startswith("https://"), (
            f"Group 2 jurisdiction {code} has invalid legislature_url: {leg_url}"
        )


def test_no_partial_state_has_citations_marked_verified():
    """No PARTIAL or UNVERIFIED state may have substantive citations marked VERIFIED."""
    for yaml_file in STATES_DIR.glob("*.yaml"):
        if yaml_file.name == "matrix.yaml":
            continue
        with open(yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        if data.get("verification_status") in ("PARTIAL", "UNVERIFIED"):
            for cite_field in [
                "emergency_removal_citation",
                "shelter_hearing_citation",
                "counsel_citation",
                "tpr_citation",
            ]:
                val = str(data.get(cite_field, "")).strip().upper()
                assert val == "UNVERIFIED" or val == "", (
                    f"Partial state {yaml_file.name} has citation field {cite_field} set to '{data.get(cite_field)}', must be UNVERIFIED"
                )


def test_icwa_inquiry_field_present_on_every_entry():
    """icwa_inquiry field must be present on every state entry in legal_registry/states/."""
    for yaml_file in STATES_DIR.glob("*.yaml"):
        if yaml_file.name == "matrix.yaml":
            continue
        with open(yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        assert "icwa_inquiry" in data, f"{yaml_file.name} missing 'icwa_inquiry' field"
        assert data["icwa_inquiry"] in ("required", "not_specified"), (
            f"{yaml_file.name} invalid icwa_inquiry value: {data['icwa_inquiry']}"
        )


def test_registry_loader_loads_all_states_without_error():
    """Verify default_registry loads states cleanly without fatal errors."""
    loader = default_registry
    assert len(loader.state_matrix) >= 50
    assert len(loader.load_errors) == 0, f"Registry load errors: {loader.load_errors}"
