"""New York State Senate (Family Court Act & Social Services Law) Ingestion Crawler."""

from typing import List
from datetime import date
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import StatuteChunker


class NewYorkLegConnector(BaseLegalConnector):
    def __init__(self):
        super().__init__(source_id="NY_FCA", rate_limit_delay_seconds=1.0)

    def parse_ny_statute(self, act_abbr: str, section: str, title_name: str, full_text: str, effective_date: date) -> LegalDocument:
        if act_abbr == "FCA":
            citation = f"N.Y. Fam. Ct. Act § {section}"
            source_id = "NY_FCA"
        else:
            citation = f"N.Y. Soc. Serv. Law § {section}"
            source_id = "NY_SSL"

        doc_id = f"NY-{act_abbr}-{section.replace('.', '_')}"
        temporal = TemporalMetadata(
            effective_date=effective_date,
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="New York State Senate"
        )
        chunks = StatuteChunker.chunk_statute(
            document_id=doc_id,
            title=f"{citation}: {title_name}",
            full_text=full_text
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id=source_id,
            jurisdiction="US-NY",
            level="state",
            document_type="statute",
            title=f"{citation} - {title_name}",
            citation=citation,
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=f"https://www.nysenate.gov/legislation/laws/{'FCT' if act_abbr == 'FCA' else 'SOS'}/{section}",
            cps_topics=["child_welfare", "family_court_act", "child_protective_proceeding", "state_statute"]
        )
        doc.compute_hash()
        return doc

    def get_canonical_statutes(self) -> List[LegalDocument]:
        docs = []

        # FCA § 1024 - Emergency removal without court order
        docs.append(self.parse_ny_statute(
            act_abbr="FCA",
            section="1024",
            title_name="Emergency removal without court order",
            full_text=(
                "(a) A peace officer, a police officer, or an agent of a duly authorized society for the prevention of cruelty to children "
                "or a designated employee of a city or county child protective agency may take a child into protective custody without the consent "
                "of the parent and without a court order only if: (i) the person has reasonable cause to believe that the child's life or health "
                "is in imminent danger; and (ii) there is not enough time to apply for an order under section 1022."
            ),
            effective_date=date(2020, 1, 1)
        ))

        # FCA § 1028 - Application to return child temporarily removed (3 Court Days)
        docs.append(self.parse_ny_statute(
            act_abbr="FCA",
            section="1028",
            title_name="Application to return child temporarily removed",
            full_text=(
                "(a) Upon the application of the parent or other person legally responsible for the care of a child who has been temporarily "
                "removed under this part, the court shall hold a hearing to determine whether the child should be returned. The hearing shall "
                "be held within three court days of the application and shall not be adjourned for more than three court days, except by consent "
                "of the parties. The court shall grant the application and return the child unless it finds that the return presents an imminent "
                "risk to the child's life or health. Reasonable efforts must be evaluated to determine whether the child could safely remain at home."
            ),
            effective_date=date(2020, 1, 1)
        ))

        # FCA § 262 - Assignment of counsel for indigent adults
        docs.append(self.parse_ny_statute(
            act_abbr="FCA",
            section="262",
            title_name="Assignment of counsel for indigent adults",
            full_text=(
                "(a) Each of the persons described below in this subdivision has the right to the assistance of counsel. When such person first "
                "appears in court, the judge shall advise such person before proceeding that he or she has the right to be represented by counsel of "
                "his or her own choosing, of the right to have an adjournment to confer with counsel, and of the right to have counsel assigned by "
                "the court in any case where he or she is financially unable to obtain the same: (i) the respondent in any proceeding under article ten."
            ),
            effective_date=date(2020, 1, 1)
        ))

        return docs

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return self.get_canonical_statutes()
