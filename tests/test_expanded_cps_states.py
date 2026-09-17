"""Unit tests for expanded CPS states (PA, GA, NC, MI, NJ, VA).

Verifies:
- Each new state registry loads successfully via RegistryLoader
- Each new state has required fields (removal, shelter hearing, right to counsel, ICWA)
- Each crawler initializes and offline fallback returns valid LegalDocument
- Pipeline registers all new state crawlers without import/registration gaps
"""

import pytest
from legal_registry.loader import RegistryLoader
from ingestion.pipeline import IngestionPipeline
from ingestion.state_crawlers.pennsylvania import PennsylvaniaLegConnector
from ingestion.state_crawlers.georgia import GeorgiaLegConnector
from ingestion.state_crawlers.north_carolina import NorthCarolinaLegConnector
from ingestion.state_crawlers.michigan import MichiganLegConnector
from ingestion.state_crawlers.new_jersey import NewJerseyLegConnector
from ingestion.state_crawlers.virginia import VirginiaLegConnector
from normalization.models import LegalDocument

EXPANDED_STATES = ["PA", "GA", "NC", "MI", "NJ", "VA"]


@pytest.fixture(scope="module")
def registry():
    """Initializes and returns the complete registry loader."""
    loader = RegistryLoader()
    return loader


def test_each_new_state_cps_registry_loads_successfully(registry):
    """Verify that CPS registry entries load for PA, GA, NC, MI, NJ, VA without errors."""
    assert len(registry.load_errors) == 0, f"Registry had load errors: {registry.load_errors}"

    for st in EXPANDED_STATES:
        jurisdiction = f"US-{st}"
        matching_sources = [
            source for source in registry.cps_sources.values()
            if source.jurisdiction == jurisdiction
        ]
        assert len(matching_sources) > 0, f"No CPS sources loaded for {jurisdiction}"
        entry = matching_sources[0]
        assert entry.level == "state"
        assert entry.active is True
        assert len(entry.key_statutory_sections) >= 5


def test_each_new_state_has_required_statutory_fields(registry):
    """Verify each new state has emergency removal, shelter hearing, right to counsel, and ICWA."""
    for st in EXPANDED_STATES:
        jurisdiction = f"US-{st}"
        entry = next(s for s in registry.cps_sources.values() if s.jurisdiction == jurisdiction)

        # 1. Topics coverage
        assert entry.topics.emergency_removal is True, f"{st} missing emergency_removal topic"
        assert entry.topics.shelter_care_hearing is True, f"{st} missing shelter_care_hearing topic"
        assert entry.topics.parent_rights_counsel is True, f"{st} missing parent_rights_counsel topic"
        assert entry.topics.reasonable_efforts is True, f"{st} missing reasonable_efforts topic"
        assert entry.topics.termination_parental_rights is True, f"{st} missing termination_parental_rights topic"

        # 2. Mandatory timeframes
        assert "shelter_hearing_hours" in entry.mandatory_timeframes_days, f"{st} missing shelter_hearing_hours"
        assert entry.mandatory_timeframes_days["shelter_hearing_hours"] > 0

        # 3. Rich metadata fields
        meta = entry.metadata
        assert "emergency_removal" in meta, f"{st} missing metadata.emergency_removal"
        assert "citation" in meta["emergency_removal"]
        assert "text_excerpt" in meta["emergency_removal"]

        assert "shelter_hearing_deadline_hours" in meta, f"{st} missing metadata.shelter_hearing_deadline_hours"
        assert "right_to_counsel" in meta, f"{st} missing metadata.right_to_counsel"
        assert "icwa_inquiry_requirement" in meta, f"{st} missing metadata.icwa_inquiry_requirement"
        assert "reasonable_efforts_requirement" in meta, f"{st} missing metadata.reasonable_efforts_requirement"
        assert "relative_placement_preference" in meta, f"{st} missing metadata.relative_placement_preference"
        assert "tpr_grounds" in meta, f"{st} missing metadata.tpr_grounds"


def test_each_new_state_in_state_matrix(registry):
    """Verify all 6 expanded states are active in state_matrix with deep_implementation=True."""
    for st in EXPANDED_STATES:
        assert st in registry.state_matrix, f"{st} not found in state_matrix"
        assert registry.state_matrix[st]["deep_implementation"] is True


def test_each_crawler_initializes_and_offline_fallback():
    """Verify each state crawler initializes and returns valid LegalDocument from offline fallback."""
    from unittest.mock import patch

    crawler_classes = [
        PennsylvaniaLegConnector,
        GeorgiaLegConnector,
        NorthCarolinaLegConnector,
        MichiganLegConnector,
        NewJerseyLegConnector,
        VirginiaLegConnector,
    ]

    for cls in crawler_classes:
        crawler = cls()
        assert crawler.source_id is not None
        with patch.object(crawler, "fetch_url", side_effect=RuntimeError("offline network")):
            docs = crawler.ingest()
        assert len(docs) > 0
        for doc in docs:
            assert isinstance(doc, LegalDocument)
            assert doc.document_id is not None
            assert len(doc.full_text) > 20
            assert doc.content_hash is not None
            assert len(doc.chunks) > 0


def test_pipeline_has_no_import_registration_gaps():
    """Verify IngestionPipeline has registered crawlers for all 6 expanded states."""
    pipeline = IngestionPipeline()
    for st in EXPANDED_STATES:
        assert st in pipeline.state_crawlers, f"Pipeline missing state crawler for {st}"
        crawler = pipeline.state_crawlers[st]
        assert crawler is not None
