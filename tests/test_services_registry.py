"""Unit tests for Civil Services Registry (WA, IL, OH, Federal)."""

from services.models import CivilMatterType, ServiceType, PublicServiceRecord
from services.registry import default_service_registry, ServiceRegistry


def test_service_registry_loaded():
    all_services = default_service_registry.list_all()
    assert len(all_services) >= 15
    for s in all_services:
        assert s.service_id != ""
        assert s.name != ""
        assert s.source_url.startswith("http")
        assert len(s.matters) >= 1
        assert s.is_official is True
        assert s.content_sha256 != ""


def test_query_washington_skagit_cps():
    results = default_service_registry.query_services(
        state="WA",
        county="Skagit",
        matter=CivilMatterType.FAMILY_CPS
    )
    assert len(results) >= 2
    service_names = [r.name for r in results]
    assert any("Skagit County" in name for name in service_names)
    assert any("Northwest Justice Project" in name or "Washington LawHelp" in name for name in service_names)


def test_query_illinois_cook_housing():
    results = default_service_registry.query_services(
        state="IL",
        county="Cook",
        matter=CivilMatterType.HOUSING
    )
    assert len(results) >= 2
    names = [r.name for r in results]
    assert any("Legal Aid Chicago" in name for name in names)
    assert any("Illinois Legal Aid Online" in name for name in names)


def test_query_ohio_consumer():
    results = default_service_registry.query_services(
        state="OH",
        matter=CivilMatterType.CONSUMER_DEBT
    )
    assert len(results) >= 2
    names = [r.name for r in results]
    assert any("Legal Aid Society of Cleveland" in name or "Ohio Attorney General" in name for name in names)


def test_query_tribal_icwa_services():
    results = default_service_registry.query_services(
        service_type=ServiceType.TRIBAL_ICWA
    )
    assert len(results) >= 2
    ids = [r.service_id for r in results]
    assert "WA-SERV-PUYALLUP-ICWA" in ids
    assert "FED-SERV-BIA-ICWA" in ids
