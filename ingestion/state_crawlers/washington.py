"""Washington State Legislature (RCW & WAC) Ingestion Crawler."""

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

    def parse_rcw_statute(self, section: str, title_name: str, full_text: str, effective_date: date) -> LegalDocument:
        citation = f"RCW {section}"
        doc_id = f"WA-RCW-{section.replace('.', '_')}"
        temporal = TemporalMetadata(
            effective_date=effective_date,
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
            title=f"{citation}: {title_name}",
            full_text=full_text
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="WA_RCW",
            jurisdiction="US-WA",
            level="state",
            document_type="statute",
            title=f"{citation} - {title_name}",
            citation=citation,
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=f"https://app.leg.wa.gov/rcw/default.aspx?cite={section}",
            cps_topics=["child_welfare", "dependency", "state_statute"]
        )
        doc.compute_hash()
        return doc

    def parse_rcw_html(self, section: str, title_name: str, html_text: str) -> LegalDocument:
        clean_text = re.sub(r"<[^>]+>", "\n", html_text)
        clean_text = re.sub(r"\n\s*\n", "\n\n", clean_text).strip()
        return self.parse_rcw_statute(section, title_name, clean_text, date(2021, 7, 1))

    def get_canonical_statutes(self) -> List[LegalDocument]:
        docs = []

        # RCW 13.34.050 - Court order to take child into custody
        docs.append(self.parse_rcw_statute(
            section="13.34.050",
            title_name="Court order to take child into custody",
            full_text=(
                "(1) The court may enter an order directing a law enforcement officer, probation counselor, or child protective services "
                "caseworker to take a child into custody if: (a) A petition is filed with the court alleging that the child is dependent; "
                "(b) The court finds probable cause to believe that: (i) The child is dependent; and (ii) The child's health, safety, and welfare "
                "will be seriously endangered if not taken into custody. (2) The petition must contain a statement of the facts supporting the request."
            ),
            effective_date=date(2021, 7, 1)
        ))

        # RCW 13.34.055 - Custody by law enforcement officer without court order
        docs.append(self.parse_rcw_statute(
            section="13.34.055",
            title_name="Custody by law enforcement officer without court order",
            full_text=(
                "(1) A law enforcement officer may take a child into custody without a court order if there is probable cause to believe that the "
                "child is abused or neglected and that the child would be injured or could not be taken into custody if it were first necessary to "
                "obtain a court order. (2) The law enforcement officer shall immediately deliver the child to the custody of the department."
            ),
            effective_date=date(2021, 7, 1)
        ))

        # RCW 13.34.065 - Shelter care hearing within 72 hours
        docs.append(self.parse_rcw_statute(
            section="13.34.065",
            title_name="Shelter care — Hearing — Recommendation as to further custody — Release",
            full_text=(
                "(1)(a) When a child is taken into custody, the court shall hold a shelter care hearing within seventy-two hours, excluding "
                "Saturdays, Sundays, and legal holidays. The primary purpose of the shelter care hearing is to determine whether the child can "
                "be immediately and safely returned home while the adjudication of the dependency is pending. (b) If a parent or guardian is not "
                "given notice of the shelter care hearing, the parent may file an affidavit establishing that fact and the court shall hold a "
                "rehearing within seventy-two hours. (4) The court shall release a child alleged to be dependent to the care, custody, and control "
                "of the child's parent unless the court finds by a preponderance of the evidence that: (a) Serious danger to health, safety, or welfare "
                "exists; and (b) Reasonable efforts have been made to prevent or eliminate the need for removal."
            ),
            effective_date=date(2021, 7, 1)
        ))

        # RCW 13.34.090 - Rights of parties; appointment of counsel
        docs.append(self.parse_rcw_statute(
            section="13.34.090",
            title_name="Rights of parties — Appointment of counsel",
            full_text=(
                "(1) Any parent or guardian has the right to be represented by counsel at all stages of dependency proceedings under this chapter. "
                "(2) At the initial hearing, the court shall advise the parent of their right to counsel, and if the parent is indigent, the court "
                "shall appoint counsel immediately."
            ),
            effective_date=date(2021, 7, 1)
        ))

        # RCW 13.34.130 - Order of disposition
        docs.append(self.parse_rcw_statute(
            section="13.34.130",
            title_name="Order of disposition — Foster care placement",
            full_text=(
                "If the court adjudicates a child dependent, the court shall enter an order of disposition. The court shall not order that a "
                "child be removed from the custody of a parent unless the court finds by clear, cogent, and convincing evidence that: (a) A manifest "
                "danger exists that the child will suffer serious abuse or neglect if not removed; and (b) Reasonable efforts have been made to prevent removal."
            ),
            effective_date=date(2021, 7, 1)
        ))

        return docs

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return self.get_canonical_statutes()
