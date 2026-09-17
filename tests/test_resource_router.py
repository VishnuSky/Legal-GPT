"""Unit and integration tests for the Public Legal Resource Router Subsystem."""

import pytest
from datetime import date, timedelta

from legal_registry.resources.resource_schema import (
    OrganizationType,
    ResourceState,
    VerificationMethod,
    PublicLegalResource,
)
from legal_registry.resources.resource_verifier import ResourceVerifier
from legal_registry.resources.resource_registry import (
    ResourceRegistry,
    SEED_RESOURCES,
)
from legal_registry.resources.resource_search import ResourceSearchEngine
from legal_registry.resources.resource_ranker import ResourceRanker


def test_coverage_of_all_18_organization_types():
    """Verify that the schema and seed registry cover all 18 required organization types."""
    assert len(OrganizationType) == 18

    registered_types = {r.organization_type for r in ResourceRegistry.get_all()}
    
    expected_types = [
        OrganizationType.LEGAL_AID,
        OrganizationType.COURT_SELF_HELP,
        OrganizationType.PUBLIC_DEFENDER,
        OrganizationType.BAR_REFERRAL,
        OrganizationType.CIVIL_RIGHTS_ORGANIZATIONS,
        OrganizationType.CHILD_ADVOCACY,
        OrganizationType.DOMESTIC_VIOLENCE_SERVICES,
        OrganizationType.DISABILITY_SERVICES,
        OrganizationType.MENTAL_HEALTH_SERVICES,
        OrganizationType.SUBSTANCE_USE_SERVICES,
        OrganizationType.HOUSING_SERVICES,
        OrganizationType.EDUCATION_ADVOCACY,
        OrganizationType.VETERANS_SERVICES,
        OrganizationType.TRIBAL_SERVICES,
        OrganizationType.IMMIGRATION_SERVICES,
        OrganizationType.MEDIATION,
        OrganizationType.OMBUDS,
        OrganizationType.GOVERNMENT_AGENCIES,
    ]

    for exp_type in expected_types:
        assert exp_type in registered_types, f"Missing coverage for organization type: {exp_type}"


def test_resource_states_and_verification_rules():
    """Verify that all 5 resource states exist and resource_verifier correctly audits them."""
    assert len(ResourceState) == 5
    states = {s.value for s in ResourceState}
    assert {"VERIFIED", "STALE", "UNVERIFIED", "CLOSED", "TEMPORARILY_UNAVAILABLE"}.issubset(states)

    # Valid resource should verify clean
    valid_res = ResourceRegistry.get_by_id("WA-RES-NJP-01")
    assert valid_res is not None
    state, flags = ResourceVerifier.verify(valid_res, reference_date=valid_res.last_verified)
    assert state == ResourceState.VERIFIED
    assert any("verified against primary source" in f.lower() for f in flags)


def test_staleness_transition_after_180_days():
    """Verify that records older than 180 days automatically transition to STALE."""
    valid_res = ResourceRegistry.get_by_id("WA-RES-NJP-01")
    assert valid_res is not None

    # Reference date is 200 days after last_verified
    future_date = valid_res.last_verified + timedelta(days=200)
    state, flags = ResourceVerifier.verify(valid_res, reference_date=future_date)
    
    assert state == ResourceState.STALE
    assert any("stale" in f.lower() for f in flags)


def test_zero_invention_rejection_of_fictitious_data():
    """Verify that fake phone numbers, missing sources, and invalid URLs are rejected as UNVERIFIED."""
    # 1. Dummy 555-0199 phone number
    fake_phone_res = PublicLegalResource(
        resource_id="TEST-FAKE-PHONE",
        name="Invented Legal Help",
        organization_type=OrganizationType.LEGAL_AID,
        jurisdiction="US-WA",
        service_area=["Statewide"],
        eligibility="Everyone",
        services=["Free Legal Help"],
        website="https://legalaid.example.org",
        phone="555-0199",  # Dummy North American number
        verification_source="State Bar Directory",
        last_verified=date.today(),
        verification_method=VerificationMethod.BAR_ASSOCIATION_ROSTER
    )
    state, flags = ResourceVerifier.verify(fake_phone_res)
    assert state == ResourceState.UNVERIFIED
    assert any("fictitious or dummy" in f.lower() for f in flags)

    # 2. Missing or placeholder verification source
    no_source_res = fake_phone_res.model_copy(update={
        "phone": "(206) 555-1212",
        "verification_source": "Placeholder TBD"
    })
    state, flags = ResourceVerifier.verify(no_source_res)
    assert state == ResourceState.UNVERIFIED
    assert any("invalid or ungrounded" in f.lower() for f in flags)

    # 3. Invalid website protocol
    bad_url_res = fake_phone_res.model_copy(update={
        "phone": "(206) 555-1212",
        "verification_source": "Official State Register",
        "website": "not-a-valid-url"
    })
    state, flags = ResourceVerifier.verify(bad_url_res)
    assert state == ResourceState.UNVERIFIED
    assert any("lacks valid http" in f.lower() for f in flags)


def test_strict_jurisdiction_isolation_in_search():
    """Verify that searching for Washington resources never leaks Illinois or Ohio resources."""
    wa_results = ResourceSearchEngine.search(jurisdiction="US-WA")
    
    assert len(wa_results) > 0
    for r in wa_results:
        # Must be either WA or National US
        assert r.jurisdiction in ("US-WA", "US"), f"Leaked out-of-state resource: {r.resource_id} ({r.jurisdiction})"

    # Verify no Illinois or Ohio IDs in Washington results
    wa_ids = {r.resource_id for r in wa_results}
    assert "IL-RES-LAC-01" not in wa_ids
    assert "IL-RES-COOK-PD-01" not in wa_ids
    assert "OH-RES-LASC-01" not in wa_ids

    # Conversely, Illinois search must not leak Washington resources
    il_results = ResourceSearchEngine.search(jurisdiction="US-IL")
    il_ids = {r.resource_id for r in il_results}
    assert "WA-RES-NJP-01" not in il_ids
    assert "IL-RES-LAC-01" in il_ids


def test_search_county_and_type_filtering():
    """Verify searching for specific county and organization type."""
    results = ResourceSearchEngine.search(
        jurisdiction="US-WA",
        county="Skagit",
        organization_types=[OrganizationType.LEGAL_AID, OrganizationType.OMBUDS]
    )

    assert len(results) >= 2
    types = {r.organization_type for r in results}
    assert OrganizationType.LEGAL_AID in types
    assert OrganizationType.OMBUDS in types

    # NJP covers Skagit County directly or statewide
    njp = next((r for r in results if r.resource_id == "WA-RES-NJP-01"), None)
    assert njp is not None
    assert "Skagit County" in njp.service_area


def test_resource_ranker_proximity_and_income_weighting():
    """Verify that ResourceRanker orders local county resources and legal aid higher for low-income users."""
    skagit_results = ResourceSearchEngine.search(jurisdiction="US-WA", county="Skagit")
    
    ranked = ResourceRanker.rank_resources(
        resources=skagit_results,
        target_county="Skagit",
        preferred_types=[OrganizationType.LEGAL_AID],
        is_low_income=True
    )

    assert len(ranked) >= 2
    # Northwest Justice Project (direct county match + legal aid + low income) should rank at the very top
    top_resource = ranked[0]
    assert top_resource.resource_id == "WA-RES-NJP-01"
    assert top_resource.organization_type == OrganizationType.LEGAL_AID


def test_suppression_of_unverified_and_closed_by_default():
    """Verify that unverified and closed resources are suppressed by default in search."""
    all_res = ResourceRegistry.get_all()
    # Create an unverified copy
    unverified_res = all_res[0].model_copy(update={"state": ResourceState.UNVERIFIED, "resource_id": "TEST-UNVER"})
    closed_res = all_res[0].model_copy(update={"state": ResourceState.CLOSED, "resource_id": "TEST-CLOSED"})

    # Temporarily mock into registry
    ResourceRegistry._RESOURCES_BY_ID["TEST-UNVER"] = unverified_res
    ResourceRegistry._RESOURCES_BY_ID["TEST-CLOSED"] = closed_res

    try:
        # Default search should NOT return unverified or closed
        standard_search = ResourceSearchEngine.search(jurisdiction="US-WA")
        found_ids = {r.resource_id for r in standard_search}
        assert "TEST-UNVER" not in found_ids
        assert "TEST-CLOSED" not in found_ids

        # Explicitly requesting unverified
        with_unverified = ResourceSearchEngine.search(jurisdiction="US-WA", include_unverified=True)
        assert "TEST-UNVER" in {r.resource_id for r in with_unverified}
    finally:
        # Clean up mock items
        ResourceRegistry._RESOURCES_BY_ID.pop("TEST-UNVER", None)
        ResourceRegistry._RESOURCES_BY_ID.pop("TEST-CLOSED", None)
