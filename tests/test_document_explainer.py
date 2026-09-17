"""Tests for Document Explainer Module (core/document_explainer)."""

import pytest
from fastapi.testclient import TestClient

from core.document_explainer.models import (
    DocumentType,
    DocumentExplanationRequest,
    DocumentExplanationReport,
)
from core.document_explainer.engine import DocumentExplainerEngine
from core.document_explainer.renderer import DocumentExplainerRenderer
from api.server import app


@pytest.fixture
def explainer_engine():
    return DocumentExplainerEngine()


@pytest.fixture
def test_client():
    return TestClient(app)


def test_summons_and_complaint_explanation(explainer_engine):
    """Verifies that summons & complaint identifies answer deadline and default judgment risk."""
    req = DocumentExplanationRequest(
        document_type="summons_and_complaint",
        jurisdiction="WA",
        literacy_level=1
    )
    report = explainer_engine.explain_document(req)

    assert report.document_title == "Summons and Complaint"
    assert report.verification_status == "VERIFIED"
    assert any("Answer" in d.name for d in report.deadlines)
    assert any("Default Judgment" in c for c in report.consequences_of_inaction)
    assert "sued" in report.plain_english_explanation.lower()
    assert "LEGAL INFORMATION ONLY" in report.disclaimer


def test_dependency_petition_explanation(explainer_engine):
    """Verifies dependency petition identifies right to appointed counsel and shelter hearing."""
    req = DocumentExplanationRequest(
        document_type="dependency_petition",
        jurisdiction="WA",
        literacy_level=2
    )
    report = explainer_engine.explain_document(req)

    assert "Dependency Petition" in report.document_title
    assert any("Shelter Care" in d.name for d in report.deadlines)
    assert any("Counsel" in r.right_name or "Attorney" in r.right_name for r in report.rights)
    assert any("ICWA" in r.right_name for r in report.rights)
    assert any("Request Court-Appointed Counsel" in a.step for a in report.recommended_actions)


def test_temporary_custody_order_explanation(explainer_engine):
    """Verifies emergency temporary custody order identifies immediate hearing & kinship rights."""
    req = DocumentExplanationRequest(
        document_text="Temporary Order for Immediate Custody of Child pending shelter hearing",
        jurisdiction="FL",
        literacy_level=1
    )
    report = explainer_engine.explain_document(req)

    assert "Temporary Custody" in report.document_title
    assert any("Shelter Care" in d.name for d in report.deadlines)
    assert any("Kinship" in r.right_name or "Relative" in r.right_name for r in report.rights)


def test_subpoena_explanation(explainer_engine):
    """Verifies subpoena identifies appearance date and motion to quash / Fifth Amendment."""
    req = DocumentExplanationRequest(
        document_type="subpoena",
        jurisdiction="US"
    )
    report = explainer_engine.explain_document(req)

    assert "Subpoena" in report.document_title
    assert any("Quash" in r.right_name for r in report.rights)
    assert any("Fifth Amendment" in r.right_name for r in report.rights)


def test_unknown_document_fallback_zero_guessing(explainer_engine):
    """Unrecognized document types fall back to UNKNOWN_AUTHORITY_GAP without guessing."""
    req = DocumentExplanationRequest(
        document_text="Miscellaneous handwritten letter regarding neighborhood dispute",
        jurisdiction="US"
    )
    report = explainer_engine.explain_document(req)

    assert report.verification_status == "UNKNOWN_AUTHORITY_GAP"
    assert report.document_title == "Unrecognized Legal Document"
    assert "could not identify this document" in report.plain_english_explanation.lower()


def test_document_explainer_renderer_markdown(explainer_engine):
    req = DocumentExplanationRequest(
        document_type="dependency_petition",
        jurisdiction="WA",
        literacy_level=1
    )
    report = explainer_engine.explain_document(req)
    md = DocumentExplainerRenderer.render_markdown(report)

    assert "Legal Document Breakdown: Child Dependency Petition" in md
    assert "Plain English:" in md
    assert "Critical Deadlines & Response Windows" in md
    assert "Rights & Legal Protections" in md
    assert "Recommended Next Steps" in md
    assert "LEGAL INFORMATION ONLY" in md


def test_document_explainer_api_endpoint(test_client):
    """Tests POST /api/v1/public/explain-document endpoint."""
    payload = {
        "document_type": "summons_and_complaint",
        "jurisdiction": "WA",
        "literacy_level": 1
    }
    response = test_client.post("/api/v1/public/explain-document", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["document_title"] == "Summons and Complaint"
    assert len(data["deadlines"]) >= 1
    assert "markdown" in data
