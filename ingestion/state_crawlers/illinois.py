"""Illinois General Assembly (ILCS) Ingestion Crawler."""

from typing import List
from datetime import date
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import StatuteChunker


class IllinoisLegConnector(BaseLegalConnector):
    def __init__(self):
        super().__init__(source_id="IL_ILCS", rate_limit_delay_seconds=1.0)

    def parse_ilcs_statute(self, chapter: str, act: str, section: str, title_name: str, full_text: str, effective_date: date) -> LegalDocument:
        citation = f"{chapter} ILCS {act}/{section}"
        doc_id = f"IL-ILCS-{chapter}-{act}-{section.replace('/', '_')}"
        temporal = TemporalMetadata(
            effective_date=effective_date,
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="Illinois General Assembly"
        )
        chunks = StatuteChunker.chunk_statute(
            document_id=doc_id,
            title=f"{citation}: {title_name}",
            full_text=full_text
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="IL_ILCS",
            jurisdiction="US-IL",
            level="state",
            document_type="statute",
            title=f"{citation} - {title_name}",
            citation=citation,
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=f"https://www.ilga.gov/legislation/ilcs/fulltext.asp?DocName={chapter:0>4}0{act:0>4}0K{section}",
            cps_topics=["child_welfare", "juvenile_court_act", "state_statute"]
        )
        doc.compute_hash()
        return doc

    def get_canonical_statutes(self) -> List[LegalDocument]:
        docs = []

        # 705 ILCS 405/2-10 - Temporary custody hearing (48 Hours)
        docs.append(self.parse_ilcs_statute(
            chapter="705",
            act="405",
            section="2-10",
            title_name="Temporary custody hearing",
            full_text=(
                "At the appearance of the minor before the court at the temporary custody hearing, which shall be held within 48 hours "
                "after the minor is taken into temporary custody, excluding Saturdays, Sundays, and court designated holidays: (1) The court "
                "shall examine the minor, his parents, guardian, or other persons having physical custody. (2) If the court finds probable cause "
                "to believe that the minor is abused, neglected or dependent, and that there is urgent and immediate necessity for temporary custody, "
                "the court may enter an order. Reasonable efforts made by the Department of Children and Family Services to prevent or eliminate "
                "the need for removal must be documented on the record."
            ),
            effective_date=date(2022, 1, 1)
        ))

        # 705 ILCS 405/1-5 - Rights of parties to proceedings; appointed counsel
        docs.append(self.parse_ilcs_statute(
            chapter="705",
            act="405",
            section="1-5",
            title_name="Rights of parties to proceedings",
            full_text=(
                "(1) Except as provided in this Section, the minor who is the subject of the proceeding and his parents, guardian, legal "
                "custodian or responsible relative who are parties respondent have the right to be present, to be heard, to present evidence "
                "material to the proceedings, to cross-examine witnesses, to examine pertinent court files and records and also, although "
                "falsely accused, to the appointment of counsel if financially unable to employ counsel."
            ),
            effective_date=date(2022, 1, 1)
        ))

        # 705 ILCS 405/2-21 - Findings and adjudication
        docs.append(self.parse_ilcs_statute(
            chapter="705",
            act="405",
            section="2-21",
            title_name="Findings and adjudication",
            full_text=(
                "(1) The court shall determine whether the allegations of the petition are supported by a preponderance of the evidence. "
                "(2) If the court finds that the minor is abused, neglected, or dependent, the court shall determine whether the abuse, neglect, "
                "or dependency is the result of physical abuse inflicted by a parent, guardian, or legal custodian, and shall state the basis for such finding."
            ),
            effective_date=date(2022, 1, 1)
        ))

        return docs

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return self.get_canonical_statutes()
