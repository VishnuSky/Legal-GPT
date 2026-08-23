"""Unified Ingestion Pipeline Orchestrator for Multi-Source Legal Ingestion."""

import time
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from storage.db import LegalDatabase
from storage.vector_store import SimpleHybridStore
from normalization.models import LegalDocument
from ingestion.govinfo import GovInfoConnector
from ingestion.courtlistener import CourtListenerConnector
from ingestion.state_crawlers.washington import WashingtonLegConnector
from ingestion.state_crawlers.illinois import IllinoisLegConnector
from ingestion.state_crawlers.ohio import OhioLegConnector
from ingestion.state_crawlers.california import CaliforniaLegConnector
from ingestion.state_crawlers.texas import TexasLegConnector
from ingestion.state_crawlers.new_york import NewYorkLegConnector
from ingestion.cps_policy_crawlers.wa_dcyf import WashingtonDCYFPolicyConnector
from ingestion.cps_policy_crawlers.il_dcfs import IllinoisDCFSPolicyConnector
from ingestion.cps_policy_crawlers.oh_odjfs import OhioODJFSPolicyConnector
from ingestion.cps_policy_crawlers.ca_cdss import CaliforniaCDSSPolicyConnector
from ingestion.cps_policy_crawlers.tx_dfps import TexasDFPSPolicyConnector
from ingestion.cps_policy_crawlers.ny_ocfs import NewYorkOCFSPolicyConnector

logger = logging.getLogger("legal_gpt.pipeline")


@dataclass
class IngestionManifest:
    started_at: datetime
    completed_at: datetime
    duration_seconds: float
    total_documents: int
    total_chunks: int
    by_category: Dict[str, int]
    by_jurisdiction: Dict[str, int]
    status: str = "SUCCESS"


class IngestionPipeline:
    """Orchestrates authoritative legal data extraction, chunking, hashing, and hybrid storage."""

    def __init__(self, db: Optional[LegalDatabase] = None, vector_store: Optional[SimpleHybridStore] = None):
        self.db = db or LegalDatabase()
        self.vector_store = vector_store or SimpleHybridStore()

        # Connectors
        self.govinfo = GovInfoConnector()
        self.courtlistener = CourtListenerConnector()
        self.state_crawlers = {
            "WA": WashingtonLegConnector(),
            "IL": IllinoisLegConnector(),
            "OH": OhioLegConnector(),
            "CA": CaliforniaLegConnector(),
            "TX": TexasLegConnector(),
            "NY": NewYorkLegConnector(),
        }
        self.policy_crawlers = {
            "WA": WashingtonDCYFPolicyConnector(),
            "IL": IllinoisDCFSPolicyConnector(),
            "OH": OhioODJFSPolicyConnector(),
            "CA": CaliforniaCDSSPolicyConnector(),
            "TX": TexasDFPSPolicyConnector(),
            "NY": NewYorkOCFSPolicyConnector(),
        }

    def run_sync(self, categories: Optional[List[str]] = None) -> IngestionManifest:
        """Executes ingestion pipeline across specified categories ('federal', 'caselaw', 'states', 'policies', or all)."""
        start_time = datetime.now(timezone.utc)
        target_cats = set(categories or ["federal", "caselaw", "states", "policies"])
        if "all" in target_cats:
            target_cats = {"federal", "caselaw", "states", "policies"}

        collected_docs: List[LegalDocument] = []
        by_category_counts: Dict[str, int] = {}
        by_jurisdiction_counts: Dict[str, int] = {}

        # 1. Federal Statutes & Regulations
        if "federal" in target_cats:
            fed_docs = self.govinfo.ingest()
            collected_docs.extend(fed_docs)
            by_category_counts["federal"] = len(fed_docs)

        # 2. Case Law & Precedent Opinions
        if "caselaw" in target_cats:
            case_docs = self.courtlistener.ingest()
            collected_docs.extend(case_docs)
            by_category_counts["caselaw"] = len(case_docs)

        # 3. State Statutes
        if "states" in target_cats:
            state_count = 0
            for state_code, crawler in self.state_crawlers.items():
                docs = crawler.ingest()
                collected_docs.extend(docs)
                state_count += len(docs)
            by_category_counts["states"] = state_count

        # 4. CPS Agency Policies
        if "policies" in target_cats:
            policy_count = 0
            for state_code, crawler in self.policy_crawlers.items():
                docs = crawler.ingest()
                collected_docs.extend(docs)
                policy_count += len(docs)
            by_category_counts["policies"] = policy_count

        # Save into SQLite Database and Vector Store
        total_chunks = 0
        for doc in collected_docs:
            self.db.insert_document(doc)
            self.vector_store.add_chunks(doc.chunks)
            total_chunks += len(doc.chunks)

            juris = doc.jurisdiction
            by_jurisdiction_counts[juris] = by_jurisdiction_counts.get(juris, 0) + 1

        end_time = datetime.now(timezone.utc)
        duration = (end_time - start_time).total_seconds()

        manifest = IngestionManifest(
            started_at=start_time,
            completed_at=end_time,
            duration_seconds=duration,
            total_documents=len(collected_docs),
            total_chunks=total_chunks,
            by_category=by_category_counts,
            by_jurisdiction=by_jurisdiction_counts,
            status="SUCCESS"
        )
        logger.info(f"Ingestion pipeline completed: {len(collected_docs)} docs, {total_chunks} chunks in {duration:.2f}s")
        return manifest
