"""Illinois General Assembly (ILCS) Ingestion Crawler."""

import re
from typing import List
from datetime import date
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import StatuteChunker


class IllinoisLegConnector(BaseLegalConnector):
    def __init__(self):
        super().__init__(source_id="IL_ILCS", rate_limit_delay_seconds=1.0)

    def parse_ilcs_text(self, chapter: str, act: str, section: str, title_name: str, text: str) -> LegalDocument:
        citation = f"{chapter} ILCS {act}/{section}"
        doc_id = f"IL-ILCS-{chapter}-{act}-{section}"
        temporal = TemporalMetadata(
            effective_date=date(2022, 1, 1),
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="Illinois General Assembly"
        )
        chunks = StatuteChunker.chunk_statute(
            document_id=doc_id,
            title=f"{citation} - {title_name}",
            full_text=text
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="IL_ILCS",
            jurisdiction="US-IL",
            level="state",
            document_type="statute",
            title=title_name,
            citation=citation,
            full_text=text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url="https://www.ilga.gov/legislation/ilcs/ilcs.asp",
            cps_topics=["child_welfare", "juvenile_court_act", "state_statute"]
        )
        doc.compute_hash()
        return doc

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return []
