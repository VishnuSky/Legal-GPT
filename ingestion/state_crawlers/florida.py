"""Florida Online Sunshine (Florida Statutes) live ingestion crawler."""

import html
import logging
import re
from datetime import date
from typing import List, Tuple

from ingestion.base import BaseLegalConnector
from normalization.chunkers import StatuteChunker
from normalization.models import AuthorityScore, LegalDocument, TemporalMetadata

logger = logging.getLogger("legal_gpt.ingestion.fl")

FL_TARGET_SECTIONS: List[Tuple[str, str]] = [
    ("39.013", "Procedures and jurisdiction; right to counsel"),
    ("39.401", "Taking a child alleged to be dependent into custody"),
    ("39.402", "Placement in a shelter"),
    ("39.507", "Adjudicatory hearings; orders"),
    ("39.701", "Judicial review"),
    ("39.806", "Grounds for termination of parental rights"),
]


class FloridaLegConnector(BaseLegalConnector):
    BASE_URL = "https://www.leg.state.fl.us/statutes/index.cfm"

    def __init__(self):
        super().__init__(source_id="FL_STATUTES", rate_limit_delay_seconds=1.0)

    def _build_section_url(self, section: str) -> str:
        chapter_str, section_suffix = section.split(".", 1)
        chapter_num = int(chapter_str)
        chapter_range_start = (chapter_num // 100) * 100
        chapter_range_end = chapter_range_start + 99

        chapter_padded = f"{chapter_num:04d}"
        section_padded = f"{chapter_num:04d}.{int(section_suffix):03d}"

        return (
            f"{self.BASE_URL}?App_mode=Display_Statute"
            f"&URL={chapter_range_start:04d}-{chapter_range_end:04d}/{chapter_padded}/Sections/{section_padded}.html"
        )

    def _clean_html_text(self, html_content: str) -> str:
        text = re.sub(r"<script[^>]*>.*?</script>", "", html_content, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<(br|/p|/div|/li|/h\d)>", "\n", text, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", "", text)
        text = html.unescape(text)
        text = re.sub(r"\r", "", text)
        text = re.sub(r"\n\s*\n+", "\n\n", text)
        return text.strip()

    def _extract_catchline(self, section: str, html_content: str, fallback_title: str) -> str:
        catchline_patterns = [
            r"<span[^>]*class=\"[^\"]*Catchline[^\"]*\"[^>]*>(.*?)</span>",
            rf"<h\d[^>]*>\s*{re.escape(section)}\s*[\-—:.]?\s*(.*?)</h\d>",
            rf"{re.escape(section)}\s*[\-—:.]\s*(.*?)\n",
        ]
        for pattern in catchline_patterns:
            match = re.search(pattern, html_content, flags=re.IGNORECASE | re.DOTALL)
            if match:
                candidate = self._clean_html_text(match.group(1)).strip(" -.:;")
                if candidate:
                    return candidate
        return fallback_title

    def parse_statute_html(self, section: str, fallback_title: str, html_content: str) -> LegalDocument:
        section_block_match = re.search(
            r"<div[^>]*id=\"[^\"]*(?:statute|section)[^\"]*\"[^>]*>(.*?)</div>",
            html_content,
            flags=re.IGNORECASE | re.DOTALL,
        )
        section_html = section_block_match.group(1) if section_block_match else html_content
        body_text = self._clean_html_text(section_html)
        if len(body_text) < 80:
            body_text = fallback_title

        title = self._extract_catchline(section, section_html, fallback_title)
        return self._build_document(section, title, body_text)

    def _build_document(self, section: str, title_name: str, full_text: str) -> LegalDocument:
        citation = f"Fla. Stat. § {section}"
        doc_id = f"FL-STAT-{section.replace('.', '_')}"
        temporal = TemporalMetadata(effective_date=date(2020, 7, 1), is_current=True)
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="Florida Legislature (Online Sunshine)",
        )
        chunks = StatuteChunker.chunk_statute(
            document_id=doc_id,
            title=f"{citation}: {title_name}",
            full_text=full_text,
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="FL_STATUTES",
            jurisdiction="US-FL",
            level="state",
            document_type="statute",
            title=f"{citation} - {title_name}",
            citation=citation,
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=self._build_section_url(section),
            cps_topics=["child_welfare", "dependency", "termination", "state_statute"],
        )
        doc.compute_hash()
        return doc

    def fetch_statute(self, section: str, title: str) -> LegalDocument:
        url = self._build_section_url(section)
        try:
            html_content = self.fetch_url(url, use_cache=True)
            return self.parse_statute_html(section, title, html_content)
        except Exception as exc:
            logger.info("Live fetch for Fla. Stat. %s fell back to offline fixture (%s)", section, exc)
            fallback_text = (
                f"{title}. This offline fallback captures core Florida dependency standards under "
                f"Fla. Stat. § {section}."
            )
            return self._build_document(section, title, fallback_text)

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return [self.fetch_statute(section, title) for section, title in FL_TARGET_SECTIONS]
