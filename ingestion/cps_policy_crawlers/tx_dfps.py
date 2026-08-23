"""Texas DFPS Child Protective Services Handbook Crawler."""

from typing import List
from datetime import date
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import PolicyChunker


class TexasDFPSPolicyConnector(BaseLegalConnector):
    def __init__(self):
        super().__init__(source_id="TX_DFPS_HANDBOOK", rate_limit_delay_seconds=1.0)

    def parse_dfps_section(self, section: str, title: str, full_text: str, effective_date: date) -> LegalDocument:
        doc_id = f"TX-DFPS-HB-{section.replace('.', '_')}"
        temporal = TemporalMetadata(
            effective_date=effective_date,
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="Texas Department of Family and Protective Services (DFPS)"
        )
        chunks = PolicyChunker.chunk_policy(
            document_id=doc_id,
            title=f"Texas DFPS Handbook Section {section}: {title}",
            full_text=full_text
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="TX_DFPS_HANDBOOK",
            jurisdiction="US-TX",
            level="state",
            document_type="agency_policy",
            title=f"DFPS Handbook {section} - {title}",
            citation=f"Texas DFPS Handbook § {section}",
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=f"https://www.dfps.texas.gov/handbooks/CPS/Files/CPS_pg_{section}.asp",
            cps_topics=["child_welfare", "agency_policy", "dfps_handbook", "investigation_priority"]
        )
        doc.compute_hash()
        return doc

    def get_canonical_policies(self) -> List[LegalDocument]:
        docs = []

        # DFPS Handbook 2100 - Investigation Priorities
        docs.append(self.parse_dfps_section(
            section="2100",
            title="Intake Priority and Response Times",
            full_text=(
                "Section 2120: Priority I reports require an immediate in-person response within 24 hours when allegations indicate that "
                "a child is in immediate danger of serious physical harm or sexual abuse. Priority II reports require an in-person response "
                "within 72 hours."
            ),
            effective_date=date(2022, 9, 1)
        ))

        # DFPS Handbook 6200 - Parent-Child Visitation
        docs.append(self.parse_dfps_section(
            section="6200",
            title="Parent-Child and Sibling Visitation",
            full_text=(
                "Section 6210: The primary purpose of parent-child visitation is to maintain and strengthen the bond between the child and parents. "
                "The initial visit must occur within 5 calendar days of the date the child was taken into temporary custody. Regular visits must occur "
                "at least bi-weekly, or weekly whenever possible."
            ),
            effective_date=date(2022, 9, 1)
        ))

        return docs

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return self.get_canonical_policies()
