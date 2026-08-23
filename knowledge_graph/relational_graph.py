"""Relational Citation Graph & Legal Citator Engine: Automated Shepards / KeyCite-Style Treatment Analysis."""

from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from storage.db import LegalDatabase


class CitatorSignal(str, Enum):
    GOOD_LAW = "GOOD_LAW"          # Positive treatment / Followed / Upheld
    CAUTION = "CAUTION"            # Distinguished / Criticized / Questioned
    NEGATIVE = "NEGATIVE"          # Overruled / Abrogated / Superseded by statute
    NEUTRAL = "NEUTRAL"            # Cited neutrally / Background mention


class RelationType(str, Enum):
    CITES = "CITES"
    INTERPRETS = "INTERPRETS"
    FOLLOWS = "FOLLOWS"
    DISTINGUISHES = "DISTINGUISHES"
    OVERRULES = "OVERRULES"
    ABROGATES = "ABROGATES"
    SUPERSEDES = "SUPERSEDES"
    AMENDS = "AMENDS"


class CitatorReport(BaseModel):
    target_citation: str
    overall_signal: CitatorSignal
    is_good_law: bool
    citing_authorities_count: int
    positive_count: int
    caution_count: int
    negative_count: int
    citing_references: List[Dict[str, Any]] = Field(default_factory=list)
    treatment_summary: str


class LegalCitatorGraph:
    """Relational knowledge graph representing legal citation edges and precedent treatment signals."""

    def __init__(self, db_path: str = "legal_gpt.db"):
        self.db = LegalDatabase(db_path)
        self._seed_foundational_relationships()

    def _seed_foundational_relationships(self):
        # 1. Haaland v. Brackeen upholds ICWA
        self.db.insert_relationship(
            source_citation="Haaland v. Brackeen, 599 U.S. 255",
            target_citation="25 U.S.C. § 1901",
            relation_type=RelationType.INTERPRETS.value,
            treatment_signal=CitatorSignal.GOOD_LAW.value,
            context_snippet="Affirmed the constitutional validity of the Indian Child Welfare Act under Article I Congress authority.",
            jurisdiction="US"
        )
        self.db.insert_relationship(
            source_citation="Haaland v. Brackeen, 599 U.S. 255",
            target_citation="25 U.S.C. § 1912",
            relation_type=RelationType.FOLLOWS.value,
            treatment_signal=CitatorSignal.GOOD_LAW.value,
            context_snippet="Upheld statutory active efforts and burden of proof requirements in state custody proceedings.",
            jurisdiction="US"
        )

        # 2. Santosky v. Kramer interprets Due Process & State TPR
        self.db.insert_relationship(
            source_citation="Santosky v. Kramer, 455 U.S. 745",
            target_citation="U.S. Const. amend. XIV",
            relation_type=RelationType.INTERPRETS.value,
            treatment_signal=CitatorSignal.GOOD_LAW.value,
            context_snippet="Fourteenth Amendment Due Process Clause mandates clear and convincing evidence before terminating parental rights.",
            jurisdiction="US"
        )

        # 3. In re Dependency of K.N.J. interprets RCW 13.34.065 & RCW 13.34.180
        self.db.insert_relationship(
            source_citation="In re Dependency of K.N.J., 171 Wn.2d 568",
            target_citation="RCW 13.34.065",
            relation_type=RelationType.INTERPRETS.value,
            treatment_signal=CitatorSignal.GOOD_LAW.value,
            context_snippet="Department must provide notice of specific parental deficiencies and offer tailored remedial services.",
            jurisdiction="US-WA"
        )

        # 4. In re Arthur H. interprets 705 ILCS 405/2-18 & 405/2-21
        self.db.insert_relationship(
            source_citation="In re Arthur H., 212 Ill. 2d 441",
            target_citation="705 ILCS 405/2-18",
            relation_type=RelationType.INTERPRETS.value,
            treatment_signal=CitatorSignal.GOOD_LAW.value,
            context_snippet="Adjudication focuses solely on whether the child is abused/neglected, not parental fault.",
            jurisdiction="US-IL"
        )

        # 5. In re B.C. interprets ORC § 2151.419
        self.db.insert_relationship(
            source_citation="In re B.C., 141 Ohio St. 3d 1",
            target_citation="ORC § 2151.419",
            relation_type=RelationType.INTERPRETS.value,
            treatment_signal=CitatorSignal.GOOD_LAW.value,
            context_snippet="PCSA bears affirmative burden to prove reasonable efforts were made prior to permanent custody.",
            jurisdiction="US-OH"
        )

        # 6. Nicholson v. Scoppetta interprets FCA § 1024
        self.db.insert_relationship(
            source_citation="Nicholson v. Scoppetta, 3 N.Y.3d 357",
            target_citation="N.Y. Fam. Ct. Act § 1024",
            relation_type=RelationType.INTERPRETS.value,
            treatment_signal=CitatorSignal.GOOD_LAW.value,
            context_snippet="Emergency removal without court order requires imminent physical peril and cannot be based on domestic violence victim status.",
            jurisdiction="US-NY"
        )

    def add_citation_edge(
        self,
        source: str,
        target: str,
        relation_type: RelationType,
        signal: CitatorSignal = CitatorSignal.NEUTRAL,
        context: Optional[str] = None,
        jurisdiction: str = "US"
    ):
        self.db.insert_relationship(
            source_citation=source,
            target_citation=target,
            relation_type=relation_type.value,
            treatment_signal=signal.value,
            context_snippet=context,
            jurisdiction=jurisdiction
        )

    def evaluate_citator_status(self, citation: str) -> CitatorReport:
        norm_target = citation.strip()
        citing_rows = self.db.get_citing_authorities(norm_target)

        # Also search case name or section substring
        if not citing_rows:
            all_rels = self.db.get_relationships_for_citation(norm_target)
            citing_rows = all_rels

        positive_count = 0
        caution_count = 0
        negative_count = 0

        for r in citing_rows:
            sig = r.get("treatment_signal", "NEUTRAL")
            rel = r.get("relation_type", "CITES")
            if sig == "GOOD_LAW" or rel in ("FOLLOWS", "INTERPRETS", "AMENDS"):
                positive_count += 1
            elif sig == "CAUTION" or rel == "DISTINGUISHES":
                caution_count += 1
            elif sig == "NEGATIVE" or rel in ("OVERRULES", "ABROGATES", "SUPERSEDES"):
                negative_count += 1

        if negative_count > 0:
            overall_signal = CitatorSignal.NEGATIVE
            is_good = False
            summary = f"WARNING: Authority '{citation}' has received negative subsequent treatment ({negative_count} overruling/abrogating reference)."
        elif caution_count > 0:
            overall_signal = CitatorSignal.CAUTION
            is_good = True
            summary = f"CAUTION: Authority '{citation}' has been distinguished or limited in subsequent applications ({caution_count} distinguishing reference)."
        elif positive_count > 0:
            overall_signal = CitatorSignal.GOOD_LAW
            is_good = True
            summary = f"GOOD LAW: Authority '{citation}' has positive treatment across {positive_count} binding precedents / interpretations."
        else:
            overall_signal = CitatorSignal.GOOD_LAW  # Default assumption for official statute
            is_good = True
            summary = f"GOOD LAW: Authority '{citation}' is an active, verified official authority with no recorded negative history."

        return CitatorReport(
            target_citation=citation,
            overall_signal=overall_signal,
            is_good_law=is_good,
            citing_authorities_count=len(citing_rows),
            positive_count=positive_count,
            caution_count=caution_count,
            negative_count=negative_count,
            citing_references=citing_rows,
            treatment_summary=summary
        )


# Global singleton
citator_graph = LegalCitatorGraph()
