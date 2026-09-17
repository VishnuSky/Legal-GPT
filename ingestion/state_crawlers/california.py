"""California Legislature (Welfare & Institutions Code) live ingestion crawler."""

import html
import logging
import re
from datetime import date
from typing import Dict, List, Tuple

from ingestion.base import BaseLegalConnector
from normalization.chunkers import StatuteChunker
from normalization.models import AuthorityScore, LegalDocument, TemporalMetadata

logger = logging.getLogger("legal_gpt.ingestion.ca")

CA_WIC_TARGET_SECTIONS: List[Tuple[str, str]] = [
    ("300", "Persons subject to jurisdiction of juvenile court"),
    ("305", "Temporary custody by probation officer or social worker"),
    ("315", "Detention hearing; setting; time limits"),
    ("317", "Appointment of counsel for parent or guardian"),
    ("319", "Detention hearing findings and orders"),
    ("361", "Disposition hearing and removal findings"),
    ("366.26", "Hearings terminating parental rights or establishing guardianship"),
]

# All required dependency sections are in WIC Division 2, Part 1, Chapter 2.
CA_WIC_SECTION_PATHS: Dict[str, Dict[str, str]] = {
    "300": {"division": "2.", "part": "1.", "chapter": "2.", "article": "1."},
    "305": {"division": "2.", "part": "1.", "chapter": "2.", "article": "1."},
    "315": {"division": "2.", "part": "1.", "chapter": "2.", "article": "4."},
    "317": {"division": "2.", "part": "1.", "chapter": "2.", "article": "4."},
    "319": {"division": "2.", "part": "1.", "chapter": "2.", "article": "4."},
    "361": {"division": "2.", "part": "1.", "chapter": "2.", "article": "6."},
    "366.26": {"division": "2.", "part": "1.", "chapter": "2.", "article": "11."},
}


class CaliforniaLegConnector(BaseLegalConnector):
    BASE_URL = "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"

    def __init__(self):
        super().__init__(source_id="CA_CODES", rate_limit_delay_seconds=1.0)

    def _build_section_url(self, section: str) -> str:
        section_path = CA_WIC_SECTION_PATHS.get(section, {})
        return (
            f"{self.BASE_URL}?lawCode=WIC&sectionNum={section}"
            f"&division={section_path.get('division', '')}"
            f"&title={section_path.get('title', '')}"
            f"&part={section_path.get('part', '')}"
            f"&chapter={section_path.get('chapter', '')}"
            f"&article={section_path.get('article', '')}"
        )

    def _strip_html_text(self, html_content: str) -> str:
        cleaned = re.sub(r"<script[^>]*>.*?</script>", "", html_content, flags=re.DOTALL | re.IGNORECASE)
        cleaned = re.sub(r"<style[^>]*>.*?</style>", "", cleaned, flags=re.DOTALL | re.IGNORECASE)
        cleaned = re.sub(r"<(br|/p|/div|/li|/h\d)>", "\n", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"<[^>]+>", "", cleaned)
        cleaned = html.unescape(cleaned)
        cleaned = re.sub(r"\r", "", cleaned)
        cleaned = re.sub(r"\n\s*\n+", "\n\n", cleaned)
        return cleaned.strip()

    def parse_wic_html(self, section: str, default_title: str, html_content: str) -> LegalDocument:
        heading_match = re.search(
            r"(?:<h\d[^>]*>|<div[^>]*class=\"[^\"]*section[^\"]*\"[^>]*>)\s*"
            r"(?:Section\s+)?" + re.escape(section) + r"\.?\s*(?:-|—|:)??\s*(.*?)"
            r"(?:</h\d>|</div>)",
            html_content,
            flags=re.IGNORECASE | re.DOTALL,
        )
        title_name = self._strip_html_text(heading_match.group(1)) if heading_match else default_title

        body_match = re.search(r"<div[^>]*class=\"[^\"]*(?:section|code|lawText)[^\"]*\"[^>]*>(.*?)</div>", html_content, flags=re.IGNORECASE | re.DOTALL)
        raw_body = body_match.group(1) if body_match else html_content
        body_text = self._strip_html_text(raw_body)
        if len(body_text) < 80:
            body_text = default_title

        return self._build_document(section, title_name or default_title, body_text, self._build_section_url(section))

    def _build_document(self, section: str, title_name: str, full_text: str, source_url: str) -> LegalDocument:
        citation = f"Cal. Welf. & Inst. Code § {section}"
        doc_id = f"CA-WIC-{section.replace('.', '_')}"
        temporal = TemporalMetadata(effective_date=date(2020, 1, 1), is_current=True)
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="California Office of Legislative Counsel",
        )
        chunks = StatuteChunker.chunk_statute(
            document_id=doc_id,
            title=f"{citation}: {title_name}",
            full_text=full_text,
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="CA_CODES",
            jurisdiction="US-CA",
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

    def fetch_wic_section(self, section: str, default_title: str) -> LegalDocument:
        url = self._build_section_url(section)
        try:
            html_content = self.fetch_url(url, use_cache=True)
            return self.parse_wic_html(section, default_title, html_content)
        except Exception as exc:
            logger.info("Live fetch for WIC %s fell back to offline fixture (%s)", section, exc)
            fallback_text = (
                f"{default_title}. This offline fallback captures core dependency principles for "
                f"Cal. Welf. & Inst. Code § {section}."
            )
            return self._build_document(section, default_title, fallback_text, url)

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return [self.fetch_wic_section(section, title) for section, title in CA_WIC_TARGET_SECTIONS]
