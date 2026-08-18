"""GovInfo API Connector for U.S. Code, CFR, and Federal Register."""

import os
import json
import logging
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import StatuteChunker

logger = logging.getLogger("legal_gpt.govinfo")


class GovInfoConnector(BaseLegalConnector):
    BASE_URL = "https://api.govinfo.gov"

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(source_id="FED_GOVINFO", rate_limit_delay_seconds=0.5)
        self.api_key = api_key or os.getenv("GOVINFO_API_KEY", "DEMO_KEY")

    def fetch_package_summary(self, package_id: str) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/packages/{package_id}/summary?api_key={self.api_key}"
        content = self.fetch_url(url)
        return json.loads(content)

    def ingest_sample_statute(self, title: int, section: str, full_text: str, title_name: str) -> LegalDocument:
        citation = f"{title} U.S.C. § {section}"
        doc_id = f"USC-TITLE-{title}-SEC-{section}"
        temporal = TemporalMetadata(
            enacted_date=date(1978, 11, 8),
            effective_date=date(1978, 11, 8),
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="U.S. Government Publishing Office (GovInfo)"
        )
        chunks = StatuteChunker.chunk_statute(
            document_id=doc_id,
            title=f"{citation}: {title_name}",
            full_text=full_text
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="FED_GOVINFO",
            jurisdiction="US",
            level="federal",
            document_type="statute",
            title=title_name,
            citation=citation,
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url="https://uscode.house.gov/",
            cps_topics=["child_welfare", "federal_statute"]
        )
        doc.compute_hash()
        return doc

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return []
