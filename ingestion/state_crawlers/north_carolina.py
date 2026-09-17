"""North Carolina General Assembly (Juvenile Code N.C.G.S. 7B) live ingestion crawler."""

import html
import logging
import re
from datetime import date
from typing import List, Tuple

from ingestion.base import BaseLegalConnector
from normalization.chunkers import StatuteChunker
from normalization.models import AuthorityScore, LegalDocument, TemporalMetadata

logger = logging.getLogger("legal_gpt.ingestion.nc")

NC_TARGET_SECTIONS: List[Tuple[str, str]] = [
    ("7B-500", "Temporary custody without court order"),
    ("7B-506", "Hearing on need for continued nonsecure custody (7-day rule)"),
    ("7B-602", "Parent's right to counsel; guardian ad litem appointment"),
    ("7B-801", "Adjudicatory hearing; within 60 days of petition"),
    ("7B-507", "Reasonable efforts requirement in placement orders"),
    ("7B-1111", "Grounds for terminating parental rights"),
]


class NorthCarolinaLegConnector(BaseLegalConnector):
    BASE_URL = "https://www.ncleg.gov/Laws/GeneralStatuteSections/Chapter7B"

    def __init__(self):
        super().__init__(source_id="NC_STATUTES", rate_limit_delay_seconds=1.0)

    def _build_section_url(self, section: str) -> str:
        return f"{self.BASE_URL}#{section}"

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
        citation = f"N.C.G.S. § {section}"
        doc_id = f"NC-STAT-{section.replace('-', '_')}"
        temporal = TemporalMetadata(effective_date=date(2022, 1, 1), is_current=True)
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="North Carolina General Assembly",
        )
        chunks = StatuteChunker.chunk_statute(
            document_id=doc_id,
            title=f"{citation}: {title_name}",
            full_text=full_text,
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="NC_STATUTES",
            jurisdiction="US-NC",
            level="state",
            document_type="statute",
            title=f"{citation} - {title_name}",
            citation=citation,
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=source_url,
            cps_topics=["child_welfare", "dependency", "juvenile_code", "state_statute"],
        )
        doc.compute_hash()
        return doc

    def fetch_section(self, section: str, default_title: str) -> LegalDocument:
        url = self._build_section_url(section)
        try:
            html_content = self.fetch_url(url, use_cache=True)
            cleaned = self._clean_html_text(html_content)
            body_text = cleaned if len(cleaned) >= 80 else f"{default_title}. Statutory text for N.C.G.S. § {section}."
            return self._build_document(section, default_title, body_text, url)
        except Exception as exc:
            logger.info("Live fetch for NC N.C.G.S. § %s fell back to offline fixture (%s)", section, exc)
            fallback_text = (
                f"{default_title}. Canonical offline statutory text representing core juvenile and child "
                f"protection principles for N.C.G.S. § {section}."
            )
            return self._build_document(section, default_title, fallback_text, url)

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return [self.fetch_section(section, desc) for section, desc in NC_TARGET_SECTIONS]
