"""Texas Legislature Online (Texas Family Code) Ingestion Crawler."""

from typing import List
from datetime import date
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import StatuteChunker


class TexasLegConnector(BaseLegalConnector):
    def __init__(self):
        super().__init__(source_id="TX_FAMILY_CODE", rate_limit_delay_seconds=1.0)

    def parse_texas_statute(self, section: str, title_name: str, full_text: str, effective_date: date) -> LegalDocument:
        citation = f"Tex. Fam. Code § {section}"
        doc_id = f"TX-FAM-{section.replace('.', '_')}"
        temporal = TemporalMetadata(
            effective_date=effective_date,
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="Texas Legislature Online"
        )
        chunks = StatuteChunker.chunk_statute(
            document_id=doc_id,
            title=f"{citation}: {title_name}",
            full_text=full_text
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
            source_url=f"https://statutes.capitol.texas.gov/Docs/FA/htm/FA.{section.split('.')[0]}.htm#{section}",
            cps_topics=["child_welfare", "family_code", "adversary_hearing", "state_statute"]
        )
        doc.compute_hash()
        return doc

    def get_canonical_statutes(self) -> List[LegalDocument]:
        docs = []

        # Tex. Fam. Code § 262.201 - Full Adversary Hearing (14 Days)
        docs.append(self.parse_texas_statute(
            section="262.201",
            title_name="Full Adversary Hearing; Findings",
            full_text=(
                "(a) Unless the child has already been returned to the parent, managing conservator, possessory conservator, guardian, caretaker, "
                "or custodian entitled to possession and the temporary order has been dissolved, a full adversary hearing shall be held not later than "
                "the 14th day after the date the child was taken into possession by the governmental entity. (g) In a suit filed under Section 262.101 "
                "or 262.105, at the conclusion of the full adversary hearing, the court shall order the return of the child unless the court finds "
                "sufficient evidence to satisfy a person of ordinary prudence and caution that: (1) there was a danger to the physical health or "
                "safety of the child; (2) reasonable efforts were made to prevent or eliminate the need for removal; and (3) there is a substantial "
                "risk of continuing danger if the child is returned."
            ),
            effective_date=date(2021, 9, 1)
        ))

        # Tex. Fam. Code § 107.013 - Mandatory appointment of attorney ad litem for parent
        docs.append(self.parse_texas_statute(
            section="107.013",
            title_name="Mandatory Appointment of Attorney ad Litem for Parent",
            full_text=(
                "(a) In a suit filed by a governmental entity under Subtitle E in which termination of the parent-child relationship or the appointment "
                "of a conservator for a child is requested, the court shall appoint an attorney ad litem to represent the interests of: (1) an indigent "
                "parent of the child who responds in opposition to the termination or appointment; (2) a parent served by citation by publication."
            ),
            effective_date=date(2021, 9, 1)
        ))

        # Tex. Fam. Code § 161.001 - Involuntary termination of parental rights
        docs.append(self.parse_texas_statute(
            section="161.001",
            title_name="Involuntary Termination of Parent-Child Relationship",
            full_text=(
                "(b) The court may order termination of the parent-child relationship if the court finds by clear and convincing evidence: "
                "(1) that the parent has committed one or more enumerated statutory predicate acts (such as knowingly placing or knowingly "
                "allowing the child to remain in conditions which endanger physical or emotional well-being); and (2) that termination is in "
                "the best interest of the child."
            ),
            effective_date=date(2021, 9, 1)
        ))

        # Tex. Fam. Code § 263.401 - Dismissal after one year (12-Month Rule)
        docs.append(self.parse_texas_statute(
            section="263.401",
            title_name="Dismissal After One Year; New Trials; Extension",
            full_text=(
                "(a) Unless the court has commenced the trial on the merits or granted an extension under Subsection (b) or (b-1), on the first "
                "Monday after the first anniversary of the date the court rendered a temporary order appointing the department as temporary managing "
                "conservator, the court's jurisdiction over the suit affecting the parent-child relationship filed by the department is terminated "
                "and the suit is automatically dismissed without a court order."
            ),
            effective_date=date(2021, 9, 1)
        ))

        return docs

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return self.get_canonical_statutes()
