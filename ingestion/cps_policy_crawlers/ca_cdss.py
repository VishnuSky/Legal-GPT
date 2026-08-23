"""California CDSS Child Welfare Services Manual Ingestion Crawler."""

from typing import List
from datetime import date
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import PolicyChunker


class CaliforniaCDSSPolicyConnector(BaseLegalConnector):
    def __init__(self):
        super().__init__(source_id="CA_CDSS_MANUAL", rate_limit_delay_seconds=1.0)

    def parse_cdss_section(self, section: str, title: str, full_text: str, effective_date: date) -> LegalDocument:
        doc_id = f"CA-CDSS-MPP-{section.replace('-', '_').replace('.', '_')}"
        temporal = TemporalMetadata(
            effective_date=effective_date,
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="California Department of Social Services (CDSS)"
        )
        chunks = PolicyChunker.chunk_policy(
            document_id=doc_id,
            title=f"CDSS MPP Division 31 Section {section}: {title}",
            full_text=full_text
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="CA_CDSS_MANUAL",
            jurisdiction="US-CA",
            level="state",
            document_type="agency_policy",
            title=f"CDSS MPP {section} - {title}",
            citation=f"CDSS MPP § {section}",
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=f"https://www.cdss.ca.gov/inforesources/letters-regulations/legislation-and-regulations/child-welfare-services-manual",
            cps_topics=["child_welfare", "agency_policy", "cdss_mpp", "division_31"]
        )
        doc.compute_hash()
        return doc

    def get_canonical_policies(self) -> List[LegalDocument]:
        docs = []

        # Division 31 Section 31-125 - Emergency Response Protocol
        docs.append(self.parse_cdss_section(
            section="31-125",
            title="Emergency Response Protocol and Immediate In-Person Response",
            full_text=(
                "Section 31-125.1: The county social worker shall conduct an immediate in-person response when allegations indicate an "
                "imminent danger to the child's physical safety or life, or within 10 calendar days when the allegations do not indicate "
                "imminent danger. Initial contact must include private, separate interview with the child."
            ),
            effective_date=date(2021, 1, 1)
        ))

        # Division 31 Section 31-340 - Family Reunification and Visitation
        docs.append(self.parse_cdss_section(
            section="31-340",
            title="Family Reunification and Contact Plan",
            full_text=(
                "Section 31-340.1: The county child welfare agency shall arrange for frequent parent-child visitation (at least weekly "
                "unless detrimental to child welfare). The case plan must provide tailored remedial services to assist parents in correcting "
                "the problems that led to child removal."
            ),
            effective_date=date(2021, 1, 1)
        ))

        return docs

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return self.get_canonical_policies()
