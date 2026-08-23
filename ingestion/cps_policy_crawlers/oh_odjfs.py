"""Ohio Department of Job and Family Services (ODJFS) Child Welfare Rules Crawler."""

from typing import List
from datetime import date
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import PolicyChunker


class OhioODJFSPolicyConnector(BaseLegalConnector):
    def __init__(self):
        super().__init__(source_id="OH_ODJFS_POLICY", rate_limit_delay_seconds=1.0)

    def parse_odjfs_rule(self, rule_number: str, title: str, full_text: str, effective_date: date) -> LegalDocument:
        doc_id = f"OH-OAC-{rule_number.replace(':', '_').replace('-', '_')}"
        temporal = TemporalMetadata(
            effective_date=effective_date,
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="Ohio Department of Job and Family Services (ODJFS)"
        )
        chunks = PolicyChunker.chunk_policy(
            document_id=doc_id,
            title=f"OAC {rule_number}: {title}",
            full_text=full_text
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="OH_ODJFS_POLICY",
            jurisdiction="US-OH",
            level="state",
            document_type="regulation",
            title=f"OAC {rule_number} - {title}",
            citation=f"OAC {rule_number}",
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=f"https://codes.ohio.gov/ohio-administrative-code/rule-{rule_number}",
            cps_topics=["child_welfare", "administrative_code", "family_visitation", "case_plan"]
        )
        doc.compute_hash()
        return doc

    def get_canonical_policies(self) -> List[LegalDocument]:
        docs = []

        # OAC 5101:2-38-01 - Requirements for PCSA case plan
        docs.append(self.parse_odjfs_rule(
            rule_number="5101:2-38-01",
            title="Requirements for Public Children Services Agency (PCSA) Case Plan",
            full_text=(
                "(A) The PCSA shall develop and implement a written case plan for the child and family within thirty days of the date "
                "a complaint was filed or the child was first placed in in-home or out-of-home placement. (B) The case plan shall be based on "
                "the comprehensive assessment and include specific, measurable objectives for reducing safety threats and addressing parental deficiencies."
            ),
            effective_date=date(2023, 3, 1)
        ))

        # OAC 5101:2-42-92 - Visitation and contact requirements
        docs.append(self.parse_odjfs_rule(
            rule_number="5101:2-42-92",
            title="Visitation and Contact Requirements for Children in Substitute Care",
            full_text=(
                "(A) The PCSA shall arrange for family visitation between the child and parents at least once every thirty days, with weekly visits "
                "encouraged whenever feasible to maintain parent-child bonds. (B) The PCSA shall not withhold visitation as a punitive measure or "
                "disciplinary action against a child or parent."
            ),
            effective_date=date(2023, 3, 1)
        ))

        return docs

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return self.get_canonical_policies()
