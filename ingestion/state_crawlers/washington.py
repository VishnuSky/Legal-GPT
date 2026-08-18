import re
from typing import List, Optional
from datetime import date
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import StatuteChunker


class WashingtonLegConnector(BaseLegalConnector):
    BASE_URL = "https://app.leg.wa.gov/rcw/default.aspx"

    def __init__(self):
        super().__init__(source_id="WA_RCW", rate_limit_delay_seconds=1.0)

    def parse_rcw_html(self, section: str, title_name: str, html_text: str) -> LegalDocument:
        """Parses RCW statute HTML content into standardized LegalDocument."""
        clean_text = re.sub(r"<[^>]+>", "\n", html_text)
        clean_text = re.sub(r"\n\s*\n", "\n\n", clean_text).strip()

        citation = f"RCW {section}"
        doc_id = f"WA-RCW-{section}"
        temporal = TemporalMetadata(
            effective_date=date(2021, 7, 1),
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="Washington State Legislature"
        )
        chunks = StatuteChunker.chunk_statute(
            document_id=doc_id,
            title=f"{citation} - {title_name}",
            full_text=clean_text
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="WA_RCW",
            jurisdiction="US-WA",
            level="state",
            document_type="statute",
            title=title_name,
            citation=citation,
            full_text=clean_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=f"https://app.leg.wa.gov/rcw/default.aspx?cite={section}",
            cps_topics=["child_welfare", "dependency", "state_statute"]
        )
        doc.compute_hash()
        return doc

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return []
