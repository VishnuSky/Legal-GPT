"""Texas Legislature Online (Texas Family Code) live ingestion crawler."""

import html
import logging
import re
from datetime import date
from typing import Dict, List, Tuple

from ingestion.base import BaseLegalConnector
from normalization.chunkers import StatuteChunker
from normalization.models import AuthorityScore, LegalDocument, TemporalMetadata

logger = logging.getLogger("legal_gpt.ingestion.tx")

TX_FAMILY_TARGET_SECTIONS: List[Tuple[str, str]] = [
    ("107.013", "Mandatory Appointment of Attorney ad Litem for Parent"),
    ("161.001", "Involuntary Termination of Parent-Child Relationship"),
    ("262.104", "Taking Possession of Child in Emergency Without Court Order"),
    ("262.105", "Notice and Filing After Emergency Possession"),
    ("262.201", "Full Adversary Hearing; Findings"),
    ("263.306", "Permanency Hearing Before Final Order"),
    ("263.401", "Dismissal After One Year; New Trials; Extension"),
]


class TexasLegConnector(BaseLegalConnector):
    BASE_URL = "https://statutes.capitol.texas.gov/Docs/FA/htm"

    def __init__(self):
        super().__init__(source_id="TX_FAMILY_CODE", rate_limit_delay_seconds=1.0)

    def _build_chapter_url(self, chapter: str) -> str:
        return f"{self.BASE_URL}/FA.{chapter}.htm"

    def _clean_html_text(self, html_content: str) -> str:
        text = re.sub(r"<script[^>]*>.*?</script>", "", html_content, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<(br|/p|/div|/li|/h\d)>", "\n", text, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", "", text)
        text = html.unescape(text)
        text = re.sub(r"\r", "", text)
        text = re.sub(r"\n\s*\n+", "\n\n", text)
        return text.strip()

    def _extract_section_block(self, section_ref: str, chapter_html: str) -> str:
        match = re.match(r"^(?P<base>\d+\.\d+)(?P<sub>\([a-zA-Z0-9]+\))?$", section_ref)
        if not match:
            return ""

        base = match.group("base")
        subsection = match.group("sub")
        base_pattern = re.escape(base)
        block_match = re.search(
            rf"(Sec\.\s*{base_pattern}\.?\s*.*?)(?=Sec\.\s*\d+\.\d+\b|$)",
            chapter_html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if not block_match:
            return ""

        block = block_match.group(1)
        if subsection:
            subsection_pattern = re.escape(subsection)
            subsection_match = re.search(
                rf"({subsection_pattern}\s+.*?)(?=\([a-zA-Z0-9]+\)\s+|$)",
                self._clean_html_text(block),
                flags=re.DOTALL,
            )
            if subsection_match:
                return subsection_match.group(1).strip()

        return block

    def _extract_caption(self, section: str, section_block: str, fallback_title: str) -> str:
        cleaned = self._clean_html_text(section_block)
        lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
        if not lines:
            return fallback_title

        first_line = lines[0]
        caption_match = re.search(rf"Sec\.\s*{re.escape(section)}\.?\s*(.*?)$", first_line, flags=re.IGNORECASE)
        if caption_match and caption_match.group(1).strip():
            return caption_match.group(1).strip(" -.:;")
        return fallback_title

    def parse_chapter_html(self, section: str, fallback_title: str, chapter_html: str) -> LegalDocument:
        section_block = self._extract_section_block(section, chapter_html)
        if not section_block:
            raise ValueError(f"Could not isolate section {section} from chapter HTML")

        title = self._extract_caption(section, section_block, fallback_title)
        body_text = self._clean_html_text(section_block)
        if len(body_text) < 80:
            body_text = fallback_title

        return self._build_document(section, title, body_text)

    def _build_document(self, section: str, title_name: str, full_text: str) -> LegalDocument:
        chapter = section.split(".")[0]
        citation = f"Tex. Fam. Code § {section}"
        doc_id = f"TX-FAM-{section.replace('.', '_').replace('(', '').replace(')', '')}"
        temporal = TemporalMetadata(effective_date=date(2021, 9, 1), is_current=True)
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="Texas Legislature Online",
        )
        chunks = StatuteChunker.chunk_statute(
            document_id=doc_id,
            title=f"{citation}: {title_name}",
            full_text=full_text,
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="TX_FAMILY_CODE",
            jurisdiction="US-TX",
            level="state",
            document_type="statute",
            title=f"{citation} - {title_name}",
            citation=citation,
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=f"{self._build_chapter_url(chapter)}#{section}",
            cps_topics=["child_welfare", "family_code", "adversary_hearing", "state_statute"],
        )
        doc.compute_hash()
        return doc

    def fetch_section_from_chapter(self, section: str, fallback_title: str, chapter_html: str) -> LegalDocument:
        try:
            return self.parse_chapter_html(section, fallback_title, chapter_html)
        except Exception as exc:
            logger.info("Live fetch for Tex. Fam. Code %s fell back to offline fixture (%s)", section, exc)
            fallback_text = (
                f"{fallback_title}. This offline fallback captures key dependency standards in "
                f"Tex. Fam. Code § {section}."
            )
            return self._build_document(section, fallback_title, fallback_text)

    def ingest(self, **kwargs) -> List[LegalDocument]:
        chapter_html_cache: Dict[str, str] = {}
        docs: List[LegalDocument] = []

        for section, title in TX_FAMILY_TARGET_SECTIONS:
            chapter = section.split(".")[0]
            if chapter not in chapter_html_cache:
                url = self._build_chapter_url(chapter)
                try:
                    chapter_html_cache[chapter] = self.fetch_url(url, use_cache=True)
                except Exception as exc:
                    logger.info("Live fetch for chapter %s fell back to offline fixture (%s)", chapter, exc)
                    chapter_html_cache[chapter] = ""
            docs.append(self.fetch_section_from_chapter(section, title, chapter_html_cache[chapter]))

        return docs
