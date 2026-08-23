"""New York OCFS Child Protective Services Manual Ingestion Crawler."""

from typing import List
from datetime import date
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import PolicyChunker


class NewYorkOCFSPolicyConnector(BaseLegalConnector):
    def __init__(self):
        super().__init__(source_id="NY_OCFS_POLICY", rate_limit_delay_seconds=1.0)

    def parse_ocfs_section(self, chapter: str, section: str, title: str, full_text: str, effective_date: date) -> LegalDocument:
        doc_id = f"NY-OCFS-CPSM-{chapter}_{section.replace('.', '_')}"
        temporal = TemporalMetadata(
            effective_date=effective_date,
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="New York State Office of Children and Family Services (OCFS)"
        )
        chunks = PolicyChunker.chunk_policy(
            document_id=doc_id,
            title=f"OCFS CPS Manual Chapter {chapter} § {section}: {title}",
            full_text=full_text
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="NY_OCFS_POLICY",
            jurisdiction="US-NY",
            level="state",
            document_type="agency_policy",
            title=f"OCFS CPS Manual Ch. {chapter} § {section} - {title}",
            citation=f"NY OCFS CPS Manual Ch. {chapter} § {section}",
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=f"https://ocfs.ny.gov/programs/cps/manual/{chapter}-{section}",
            cps_topics=["child_welfare", "agency_policy", "ocfs_manual", "emergency_removal"]
        )
        doc.compute_hash()
        return doc

    def get_canonical_policies(self) -> List[LegalDocument]:
        docs = []

        # Chapter 6 Section 3 - Emergency Removal Standards
        docs.append(self.parse_ocfs_section(
            chapter="6",
            section="3",
            title="Emergency Removal Without Court Order",
            full_text=(
                "Chapter 6 Section 3.2: Caseworkers may remove a child without a court order under FCA § 1024 only when there is reasonable "
                "cause to believe that the child's life or health is in imminent danger and there is insufficient time to apply for a court order "
                "under § 1022. Caseworkers must file an Article 10 petition on the next court day following removal."
            ),
            effective_date=date(2021, 6, 1)
        ))

        # Chapter 7 Section 4 - Family Visiting and Parent-Child Contact
        docs.append(self.parse_ocfs_section(
            chapter="7",
            section="4",
            title="Visiting and Parent-Child Contact Standards",
            full_text=(
                "Chapter 7 Section 4.1: The local department of social services must arrange for visits between parents and children in foster "
                "care at least bi-weekly, and weekly whenever feasible. The initial visit must take place within the first 7 calendar days of placement."
            ),
            effective_date=date(2021, 6, 1)
        ))

        return docs

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return self.get_canonical_policies()
