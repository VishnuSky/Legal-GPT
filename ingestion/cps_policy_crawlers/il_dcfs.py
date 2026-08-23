"""Illinois DCFS Child Welfare Policy & Procedures Ingestion Crawler."""

from typing import List
from datetime import date
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import PolicyChunker


class IllinoisDCFSPolicyConnector(BaseLegalConnector):
    def __init__(self):
        super().__init__(source_id="IL_DCFS_POLICY", rate_limit_delay_seconds=1.0)

    def parse_dcfs_policy(self, procedure_number: str, title: str, full_text: str, effective_date: date) -> LegalDocument:
        doc_id = f"IL-DCFS-PROC-{procedure_number.replace('.', '_')}"
        temporal = TemporalMetadata(
            effective_date=effective_date,
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="Illinois Department of Children and Family Services (DCFS)"
        )
        chunks = PolicyChunker.chunk_policy(
            document_id=doc_id,
            title=f"DCFS Procedure {procedure_number}: {title}",
            full_text=full_text
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="IL_DCFS_POLICY",
            jurisdiction="US-IL",
            level="state",
            document_type="agency_policy",
            title=f"DCFS Procedure {procedure_number} - {title}",
            citation=f"IL DCFS Procedure {procedure_number}",
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=f"https://dcfs.illinois.gov/about-us/policy-rules/procedures/{procedure_number}",
            cps_topics=["child_welfare", "agency_policy", "child_protection", "intake_investigation"]
        )
        doc.compute_hash()
        return doc

    def get_canonical_policies(self) -> List[LegalDocument]:
        docs = []

        # Procedure 300 - Reports of Child Abuse and Neglect
        docs.append(self.parse_dcfs_policy(
            procedure_number="300",
            title="Reports of Child Abuse and Neglect",
            full_text=(
                "Section 300.70 - Timeframes for Investigation: Child Protection Specialists must begin an investigation within 24 hours "
                "of receiving a report alleging child abuse or neglect. If the report indicates imminent danger of serious physical harm, "
                "the investigation must commence immediately upon receipt. Investigations must be completed within 60 days unless an extension "
                "is approved for good cause."
            ),
            effective_date=date(2022, 5, 1)
        ))

        # Procedure 301 - Placement and Visitation Services
        docs.append(self.parse_dcfs_policy(
            procedure_number="301",
            title="Placement and Family Visitation",
            full_text=(
                "Section 301.60 - Family Visitation: Visitation between a child in placement and parents must occur within the first two "
                "weeks of initial placement, and at least weekly thereafter, unless court order specifies otherwise. Visits must be designed "
                "to encourage bonding and maintain family relationships."
            ),
            effective_date=date(2022, 5, 1)
        ))

        return docs

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return self.get_canonical_policies()
