"""Ohio Revised Code (ORC) Ingestion Crawler."""

from typing import List
from datetime import date
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import StatuteChunker


class OhioLegConnector(BaseLegalConnector):
    def __init__(self):
        super().__init__(source_id="OH_ORC", rate_limit_delay_seconds=1.0)

    def parse_orc_statute(self, section: str, title_name: str, full_text: str, effective_date: date) -> LegalDocument:
        citation = f"ORC § {section}"
        doc_id = f"OH-ORC-{section.replace('.', '_')}"
        temporal = TemporalMetadata(
            effective_date=effective_date,
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="Ohio General Assembly"
        )
        chunks = StatuteChunker.chunk_statute(
            document_id=doc_id,
            title=f"{citation}: {title_name}",
            full_text=full_text
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="OH_ORC",
            jurisdiction="US-OH",
            level="state",
            document_type="statute",
            title=f"{citation} - {title_name}",
            citation=citation,
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=f"https://codes.ohio.gov/ohio-revised-code/section-{section}",
            cps_topics=["child_welfare", "juvenile_court", "state_statute"]
        )
        doc.compute_hash()
        return doc

    def get_canonical_statutes(self) -> List[LegalDocument]:
        docs = []

        # ORC § 2151.314 - Detention hearing; shelter care hearing (72 Hours)
        docs.append(self.parse_orc_statute(
            section="2151.314",
            title_name="Detention hearing; shelter care hearing",
            full_text=(
                "When a child is taken into custody, the court shall hold a detention or shelter care hearing not later than seventy-two "
                "hours after the child is placed in shelter care or detention. The court shall determine whether there is probable cause to believe "
                "that the child is an abused, neglected, or dependent child and whether detention or shelter care is required to prevent immediate "
                "or threatened physical or emotional harm."
            ),
            effective_date=date(2025, 9, 30)
        ))

        # ORC § 2151.419 - Reasonable efforts determination
        docs.append(self.parse_orc_statute(
            section="2151.419",
            title_name="Determination of whether agency made reasonable efforts",
            full_text=(
                "(A)(1) Except as provided in division (A)(2) of this section, at any hearing held pursuant to section 2151.28, 2151.314, "
                "2151.33, or 2151.353 of the Revised Code at which the court removes a child to shelter care or continuing custody, the court "
                "shall determine whether the public children services agency made reasonable efforts to prevent the removal of the child from the "
                "child's home, to eliminate the continued removal of the child from the child's home, or to make it possible for the child to return "
                "safely home. The agency shall have the burden of proving that it made those reasonable efforts."
            ),
            effective_date=date(2025, 9, 30)
        ))

        # ORC § 2151.352 - Right to counsel
        docs.append(self.parse_orc_statute(
            section="2151.352",
            title_name="Right to counsel",
            full_text=(
                "A child, the child's parents or custodian, or any other person in loco parentis of the child is entitled to representation by "
                "legal counsel at all stages of the proceedings under this chapter. If, as an indigent person, a party is unable to employ counsel, "
                "the party is entitled to have counsel provided for the person pursuant to Chapter 120. of the Revised Code."
            ),
            effective_date=date(2025, 9, 30)
        ))

        return docs

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return self.get_canonical_statutes()
