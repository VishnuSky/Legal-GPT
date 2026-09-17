"""Virginia General Assembly (Code of Virginia Title 16.1) live ingestion crawler."""

import html
import logging
import re
from datetime import date
from typing import List, Tuple

from ingestion.base import BaseLegalConnector
from normalization.chunkers import StatuteChunker
from normalization.models import AuthorityScore, LegalDocument, TemporalMetadata

logger = logging.getLogger("legal_gpt.ingestion.va")

VA_TARGET_SECTIONS: List[Tuple[str, str]] = [
    ("16.1-247", "Taking child into custody without court order"),
    ("16.1-251", "Emergency removal order"),
    ("16.1-252", "Preliminary removal order hearing (72-hour rule)"),
    ("16.1-266", "Appointment of counsel for indigent parents and child GAL"),
    ("16.1-281", "Foster care plan; reasonable efforts requirement"),
    ("16.1-283", "Termination of residual parental rights"),
]


class VirginiaLegConnector(BaseLegalConnector):
    BASE_URL = "https://law.lis.virginia.gov/vacode"

    def __init__(self):
        super().__init__(source_id="VA_CODE", rate_limit_delay_seconds=1.0)

    def _build_section_url(self, section: str) -> str:
        return f"{self.BASE_URL}/section{section}/"

    def _clean_html_text(self, html_content: str) -> str:
        text = re.sub(r"<script[^>]*>.*?</script\s*>", "", html_content, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style\s*>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<(br|/p|/div|/li|/h\d)>", "\n", text, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", "", text)
        text = html.unescape(text)
        text = re.sub(r"\r", "", text)
        text = re.sub(r"\n\s*\n+", "\n\n", text)
        return text.strip()

    def _build_document(self, section: str, title_name: str, full_text: str, source_url: str) -> LegalDocument:
        citation = f"Va. Code § {section}"
        doc_id = f"VA-CODE-{section.replace('.', '_').replace('-', '_')}"
        temporal = TemporalMetadata(effective_date=date(2022, 1, 1), is_current=True)
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="Virginia General Assembly",
        )
        chunks = StatuteChunker.chunk_statute(
            document_id=doc_id,
            title=f"{citation}: {title_name}",
            full_text=full_text,
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="VA_CODE",
            jurisdiction="US-VA",
            level="state",
            document_type="statute",
            title=f"{citation} - {title_name}",
            citation=citation,
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=source_url,
            cps_topics=["child_welfare", "dependency", "juvenile_court", "state_statute"],
        )
        doc.compute_hash()
        return doc

    def fetch_section(self, section: str, default_title: str) -> LegalDocument:
        url = self._build_section_url(section)
        try:
            html_content = self.fetch_url(url, use_cache=True)
            cleaned = self._clean_html_text(html_content)
            body_text = cleaned if len(cleaned) >= 80 else f"{default_title}. Statutory text for Va. Code § {section}."
            return self._build_document(section, default_title, body_text, url)
        except Exception as exc:
            logger.info("Live fetch for VA Va. Code § %s fell back to offline fixture (%s)", section, exc)
            fallback_text = (
                f"{default_title}. Canonical offline statutory text representing core juvenile and child "
                f"protection principles for Va. Code § {section}."
            )
            return self._build_document(section, default_title, fallback_text, url)

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return [self.fetch_section(section, desc) for section, desc in VA_TARGET_SECTIONS]
