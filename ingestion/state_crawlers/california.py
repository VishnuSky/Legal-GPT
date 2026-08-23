"""California State Legislature (Welfare & Institutions Code) Ingestion Crawler."""

from typing import List
from datetime import date
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import StatuteChunker


class CaliforniaLegConnector(BaseLegalConnector):
    def __init__(self):
        super().__init__(source_id="CA_CODES", rate_limit_delay_seconds=1.0)

    def parse_wic_statute(self, section: str, title_name: str, full_text: str, effective_date: date) -> LegalDocument:
        citation = f"Cal. Welf. & Inst. Code § {section}"
        doc_id = f"CA-WIC-{section.replace('.', '_')}"
        temporal = TemporalMetadata(
            effective_date=effective_date,
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="California Office of Legislative Counsel"
        )
        chunks = StatuteChunker.chunk_statute(
            document_id=doc_id,
            title=f"{citation}: {title_name}",
            full_text=full_text
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
            source_url=f"https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=WIC&sectionNum={section}",
            cps_topics=["child_welfare", "dependency", "juvenile_court", "state_statute"]
        )
        doc.compute_hash()
        return doc

    def get_canonical_statutes(self) -> List[LegalDocument]:
        docs = []

        # WIC § 300 - Grounds for juvenile court dependency jurisdiction
        docs.append(self.parse_wic_statute(
            section="300",
            title_name="Persons subject to jurisdiction of juvenile court",
            full_text=(
                "Any child who comes within any of the following descriptions is within the jurisdiction of the juvenile court which may "
                "adjudge that person to be a dependent child of the court: (a) The child has suffered, or there is a substantial risk that the "
                "child will suffer, serious physical harm inflicted nonaccidentally upon the child by the child's parent or guardian. "
                "(b)(1) The child has suffered, or there is a substantial risk that the child will suffer, serious physical harm or illness, "
                "as a result of the failure or inability of the child's parent or guardian to adequately supervise or protect the child. "
                "(g) The child has been left without any provision for support."
            ),
            effective_date=date(2020, 1, 1)
        ))

        # WIC § 315 - Detention hearing time limits (48 to 72 hours)
        docs.append(self.parse_wic_statute(
            section="315",
            title_name="Detention hearing; setting; time limits",
            full_text=(
                "If a child has been taken into custody, the juvenile court shall hold a hearing (detention hearing) to determine whether the "
                "child shall be further detained. This hearing shall be set as soon as possible, but in no event later than the expiration of the "
                "next judicial day after a petition to declare the child a dependent has been filed. If the hearing is not commenced within that "
                "time, the child shall be released from custody."
            ),
            effective_date=date(2020, 1, 1)
        ))

        # WIC § 317 - Appointment of counsel
        docs.append(self.parse_wic_statute(
            section="317",
            title_name="Appointment of counsel for parent or guardian",
            full_text=(
                "(a) When it appears to the court that a parent or guardian of the child is unable to afford counsel, the court shall appoint "
                "counsel other than the county counsel for the parent or guardian. (b) Counsel shall be appointed to represent the child unless "
                "the court finds that the child would not benefit from the appointment of counsel."
            ),
            effective_date=date(2020, 1, 1)
        ))

        # WIC § 366.26 - Termination of parental rights and permanency plan
        docs.append(self.parse_wic_statute(
            section="366.26",
            title_name="Hearings terminating parental rights or establishing guardianship",
            full_text=(
                "(b) At the hearing, the court shall terminate parental rights and order that the child be placed for adoption if the court "
                "determines, by a clear and convincing standard, that it is likely the child will be adopted. Termination of parental rights "
                "shall not occur if the parent establishes a statutory exception (such as regular visitation and contact that confers a beneficial relationship)."
            ),
            effective_date=date(2020, 1, 1)
        ))

        return docs

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return self.get_canonical_statutes()
