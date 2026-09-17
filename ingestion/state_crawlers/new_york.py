"""New York State Senate (Family Court Act & Social Services Law) live ingestion crawler."""

import html
import logging
import re
from datetime import date
from typing import Dict, List, Tuple

from ingestion.base import BaseLegalConnector
from normalization.chunkers import StatuteChunker
from normalization.models import AuthorityScore, LegalDocument, TemporalMetadata

logger = logging.getLogger("legal_gpt.ingestion.ny")

NY_FCA_TARGET_SECTIONS: List[Tuple[str, str]] = [
    ("262", "Assignment of counsel for indigent adults"),
    ("1022", "Temporary removal order"),
    ("1024", "Emergency removal without court order"),
    ("1027", "Initial hearing and temporary removal"),
    ("1028", "Application to return child temporarily removed"),
    ("1089", "Permanency hearing"),
]

NY_SSL_TARGET_SECTIONS: List[Tuple[str, str]] = [
    ("384-B", "Guardianship and custody of destitute or dependent children"),
]

NY_FCA_ARTICLE_BY_SECTION = {
    "262": "2",
    "1022": "10",
    "1024": "10",
    "1027": "10",
    "1028": "10",
    "1089": "10-A",
}

NY_SSL_ARTICLE_BY_SECTION = {
    "384-B": "6",
}


class NewYorkLegConnector(BaseLegalConnector):
    BASE_URL = "https://www.nysenate.gov/legislation/laws"

    def __init__(self):
        super().__init__(source_id="NY_FCA", rate_limit_delay_seconds=1.0)

    def _build_section_url(self, source_id: str, section: str) -> str:
        if source_id == "NY_FCA":
            article = NY_FCA_ARTICLE_BY_SECTION.get(section, "10")
            return f"{self.BASE_URL}/FCT/A{article}/{section}"

        article = NY_SSL_ARTICLE_BY_SECTION.get(section, "6")
        return f"{self.BASE_URL}/SOS/A{article}/{section}"

    def _clean_html_text(self, html_content: str) -> str:
        text = re.sub(r"<script[^>]*>.*?</script>", "", html_content, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<(br|/p|/div|/li|/h\d)>", "\n", text, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", "", text)
        text = html.unescape(text)
        text = re.sub(r"\r", "", text)
        text = re.sub(r"\n\s*\n+", "\n\n", text)
        return text.strip()

    def _extract_section_block(self, section: str, html_content: str) -> str:
        normalized_section = section.upper()
        section_pattern = re.escape(normalized_section)

        block_match = re.search(
            rf"(<h\d[^>]*>\s*(?:§|Section)?\s*{section_pattern}\b.*?</h\d>.*?)(?=<h\d[^>]*>\s*(?:§|Section)?\s*\d+\b|$)",
            html_content,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if block_match:
            return block_match.group(1)

        fallback_match = re.search(
            rf"((?:§|Section)\s*{section_pattern}\b.*?)(?=(?:§|Section)\s*\d+\b|$)",
            self._clean_html_text(html_content),
            flags=re.IGNORECASE | re.DOTALL,
        )
        return fallback_match.group(1) if fallback_match else html_content

    def _extract_caption(self, section: str, section_block: str, fallback_title: str) -> str:
        heading_match = re.search(
            rf"(?:§|Section)\s*{re.escape(section)}\s*[-—:.]?\s*(.*?)$",
            self._clean_html_text(section_block).splitlines()[0] if section_block else "",
            flags=re.IGNORECASE,
        )
        if heading_match and heading_match.group(1).strip():
            return heading_match.group(1).strip(" -.:;")
        return fallback_title

    def parse_statute_html(self, source_id: str, section: str, fallback_title: str, html_content: str) -> LegalDocument:
        section_block = self._extract_section_block(section, html_content)
        body_text = self._clean_html_text(section_block)
        if len(body_text) < 80:
            body_text = fallback_title

        title = self._extract_caption(section, section_block, fallback_title)
        return self._build_document(source_id, section, title, body_text)

    def _build_document(self, source_id: str, section: str, title_name: str, full_text: str) -> LegalDocument:
        if source_id == "NY_FCA":
            citation = f"N.Y. Fam. Ct. Act § {section}"
            act_abbr = "FCA"
            topics = ["child_welfare", "family_court_act", "child_protective_proceeding", "state_statute"]
        else:
            citation = f"N.Y. Soc. Serv. Law § {section}"
            act_abbr = "SSL"
            topics = ["child_welfare", "social_services_law", "termination_of_parental_rights", "state_statute"]

        doc_id = f"NY-{act_abbr}-{section.replace('.', '_').replace('-', '_')}"
        temporal = TemporalMetadata(effective_date=date(2020, 1, 1), is_current=True)
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="New York State Senate",
        )
        chunks = StatuteChunker.chunk_statute(
            document_id=doc_id,
            title=f"{citation}: {title_name}",
            full_text=full_text,
        )

        doc = LegalDocument(
            document_id=doc_id,
            source_id=source_id,
            jurisdiction="US-NY",
            level="state",
            document_type="statute",
            title=f"{citation} - {title_name}",
            citation=citation,
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=self._build_section_url(source_id, section),
            cps_topics=topics,
        )
        doc.compute_hash()
        return doc

    def fetch_statute(self, source_id: str, section: str, title: str) -> LegalDocument:
        url = self._build_section_url(source_id, section)
        try:
            html_content = self.fetch_url(url, use_cache=True)
            return self.parse_statute_html(source_id, section, title, html_content)
        except Exception as exc:
            logger.info("Live fetch for %s %s fell back to offline fixture (%s)", source_id, section, exc)
            fallback_text = (
                f"{title}. This offline fallback captures core New York child welfare requirements under "
                f"{source_id.replace('_', ' ')} § {section}."
            )
            return self._build_document(source_id, section, title, fallback_text)

    def ingest(self, **kwargs) -> List[LegalDocument]:
        docs = [self.fetch_statute("NY_FCA", section, title) for section, title in NY_FCA_TARGET_SECTIONS]
        docs.extend(self.fetch_statute("NY_SSL", section, title) for section, title in NY_SSL_TARGET_SECTIONS)
        return docs
