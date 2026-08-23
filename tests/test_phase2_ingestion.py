"""Unit and Integration Tests for Phase 2 Connectors, Ingestion Pipeline, and Search."""

import pytest
from fastapi.testclient import TestClient
from api.server import app
from ingestion.govinfo import GovInfoConnector
from ingestion.courtlistener import CourtListenerConnector
from ingestion.pipeline import IngestionPipeline, IngestionManifest
from storage.vector_store import SimpleHybridStore
from storage.db import LegalDatabase


@pytest.fixture
def client():
    return TestClient(app)


def test_govinfo_federal_corpus_ingestion():
    govinfo = GovInfoConnector()
    docs = govinfo.ingest()
    assert len(docs) >= 11

    # Verify ICWA statutes
    citations = [d.citation for d in docs]
    assert "25 U.S.C. § 1901" in citations
    assert "25 U.S.C. § 1912" in citations
    assert "25 U.S.C. § 1915" in citations
    assert "25 CFR § 23.107" in citations

    # Verify CAPTA & Title IV-E
    assert "42 U.S.C. § 5106a" in citations
    assert "42 U.S.C. § 671" in citations
    assert "42 U.S.C. § 675" in citations

    # Check authority score
    for d in docs:
        assert d.authority.tier == "TIER_0"
        assert d.authority.weight == 1.0


def test_courtlistener_precedents_ingestion():
    cl = CourtListenerConnector()
    opinions = cl.ingest()
    assert len(opinions) >= 10

    case_names = [o.title for o in opinions]
    assert any("Santosky v. Kramer" in t for t in case_names)
    assert any("Troxel v. Granville" in t for t in case_names)
    assert any("Stanley v. Illinois" in t for t in case_names)
    assert any("Lassiter v. Department of Social Services" in t for t in case_names)
    assert any("Haaland v. Brackeen" in t for t in case_names)
    assert any("In re Dependency of K.N.J." in t for t in case_names)
    assert any("In re Arthur H." in t for t in case_names)
    assert any("In re B.C." in t for t in case_names)
    assert any("In re Marilyn H." in t for t in case_names)
    assert any("Nicholson v. Scoppetta" in t for t in case_names)

    # Check opinion chunking
    for op in opinions:
        assert len(op.chunks) >= 1
        assert any(c.chunk_type in ("holding", "reasoning", "syllabus") for c in op.chunks)


def test_ingestion_pipeline_full_sync():
    pipeline = IngestionPipeline()
    manifest: IngestionManifest = pipeline.run_sync(categories=["all"])

    assert manifest.status == "SUCCESS"
    assert manifest.total_documents >= 50
    assert manifest.total_chunks >= 60
    assert "federal" in manifest.by_category
    assert "caselaw" in manifest.by_category
    assert "states" in manifest.by_category
    assert "policies" in manifest.by_category


def test_hybrid_search_with_jurisdiction_isolation():
    store = SimpleHybridStore()
    store.load_from_database("legal_gpt.db")

    # Search for emergency removal in New York
    ny_results = store.search(query="emergency removal imminent risk", jurisdiction="US-NY", top_k=3)
    assert len(ny_results) >= 1
    assert all(r.jurisdiction in ("US-NY", "US", None) for r in ny_results)

    # Search for ICWA active efforts
    icwa_results = store.search(query="active efforts remedial services", jurisdiction="US", top_k=3)
    assert len(icwa_results) >= 1
    assert any("1912" in (r.citation or "") or "active efforts" in r.text.lower() for r in icwa_results)


def test_api_ingest_sync_endpoint(client):
    response = client.post("/api/v1/ingest/sync", json={"categories": ["federal", "caselaw"]})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["total_documents"] >= 20
    assert "federal" in data["by_category"]
    assert "caselaw" in data["by_category"]


def test_api_search_endpoint(client):
    response = client.get("/api/v1/search?query=shelter+care+hearing&jurisdiction=US-WA&top_k=3")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "shelter care hearing"
    assert data["jurisdiction"] == "US-WA"
    assert data["count"] >= 1
    assert len(data["results"]) >= 1
