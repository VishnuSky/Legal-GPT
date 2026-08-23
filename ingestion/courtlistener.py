"""CourtListener Ingestion Connector for Landmark Precedent Opinions on Child Welfare & Due Process."""

import os
import json
import logging
from typing import List, Optional, Dict, Any
from datetime import date
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import OpinionChunker

logger = logging.getLogger("legal_gpt.courtlistener")


class CourtListenerConnector(BaseLegalConnector):
    """CourtListener Connector for U.S. Supreme Court and State Supreme Court precedent opinions."""
    BASE_URL = "https://www.courtlistener.com/api/rest/v4"

    def __init__(self, api_token: Optional[str] = None):
        super().__init__(source_id="FED_COURTLISTENER", rate_limit_delay_seconds=1.0)
        self.api_token = api_token or os.getenv("COURTLISTENER_API_TOKEN")

    def search_opinions(self, query: str, jurisdiction: Optional[str] = None, page_size: int = 5) -> Dict[str, Any]:
        """Searches CourtListener opinions with optional jurisdiction filter."""
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Token {self.api_token}"

        params = f"q={query}&type=o&order_by=score%20desc"
        if jurisdiction:
            params += f"&court={jurisdiction}"

        url = f"{self.BASE_URL}/search/?{params}"
        try:
            content = self.fetch_url(url, headers=headers)
            return json.loads(content)
        except Exception as e:
            logger.warning(f"CourtListener search failed: {e}")
            return {"count": 0, "results": []}

    def create_opinion_document(
        self,
        case_name: str,
        citation: str,
        jurisdiction: str,
        level: str,
        court_name: str,
        decision_date: date,
        syllabus: str,
        holding: str,
        reasoning: str,
        cps_topics: List[str]
    ) -> LegalDocument:
        doc_id = f"OPINION-{citation.replace(' ', '_').replace('.', '_').replace(',', '')}"
        temporal = TemporalMetadata(
            effective_date=decision_date,
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name=f"{court_name} (via CourtListener)"
        )
        full_text = (
            f"{case_name}, {citation}\n"
            f"Court: {court_name}\n"
            f"Decided: {decision_date.isoformat()}\n\n"
            f"SYLLABUS:\n{syllabus}\n\n"
            f"HOLDING:\n{holding}\n\n"
            f"REASONING & OPINION:\n{reasoning}"
        )
        chunks = OpinionChunker.chunk_opinion(
            document_id=doc_id,
            case_name=f"{case_name} ({citation})",
            full_text=full_text,
            holding=holding
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="FED_COURTLISTENER",
            jurisdiction=jurisdiction,
            level=level, # type: ignore
            document_type="court_opinion",
            title=f"{case_name} ({citation})",
            citation=citation,
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=f"https://www.courtlistener.com/c/{citation.replace(' ', '%20')}/",
            cps_topics=cps_topics
        )
        doc.compute_hash()
        return doc

    def get_canonical_precedents(self) -> List[LegalDocument]:
        """Returns foundational constitutional and statutory precedent cases across federal and anchor state jurisdictions."""
        docs = []

        # 1. Santosky v. Kramer, 455 U.S. 745 (1982) - Clear and Convincing Standard for TPR
        docs.append(self.create_opinion_document(
            case_name="Santosky v. Kramer",
            citation="455 U.S. 745",
            jurisdiction="US",
            level="federal",
            court_name="Supreme Court of the United States",
            decision_date=date(1982, 3, 24),
            syllabus=(
                "Under New York law, the State may terminate the parental rights of parents who have permanently neglected their child. "
                "The statute provided that the state must establish permanent neglect by a 'fair preponderance of the evidence'. Parents "
                "challenged the standard as violating the Fourteenth Amendment Due Process Clause."
            ),
            holding=(
                "Before a State may sever completely and irrevocably the rights of parents in their natural child, due process requires "
                "that the State support its allegations by at least clear and convincing evidence."
            ),
            reasoning=(
                "The fundamental liberty interest of natural parents in the care, custody, and management of their child is protected by the "
                "Fourteenth Amendment. Because the parents' interest in retaining their relationship with their child is commanding and the "
                "risk of erroneous factfinding under a preponderance standard is unacceptable in a permanent deprivation, the minimum standard "
                "demanded by due process is clear and convincing evidence."
            ),
            cps_topics=["tpr", "standard_of_proof", "due_process", "fourteenth_amendment", "clear_and_convincing"]
        ))

        # 2. Troxel v. Granville, 530 U.S. 57 (2000) - Fundamental Liberty Interest in Child Rearing
        docs.append(self.create_opinion_document(
            case_name="Troxel v. Granville",
            citation="530 U.S. 57",
            jurisdiction="US",
            level="federal",
            court_name="Supreme Court of the United States",
            decision_date=date(2000, 6, 5),
            syllabus=(
                "Paternal grandparents petitioned for visitation rights under Washington statute RCW 26.10.160(3), which allowed any person "
                "to petition for visitation at any time and authorized courts to grant visitation whenever it might serve the child's best interests."
            ),
            holding=(
                "The Washington visitation statute, as applied, unconstitutionally infringed on the fundamental right of parents to make decisions "
                "concerning the care, custody, and control of their children."
            ),
            reasoning=(
                "The Due Process Clause of the Fourteenth Amendment protects the fundamental right of parents to direct the upbringing of their "
                "children. There is a presumption that fit parents act in the best interests of their children. The State cannot inject itself into "
                "the private realm of the family simply because a judge believes a different decision would be better."
            ),
            cps_topics=["parent_rights", "due_process", "fit_parent_presumption", "fundamental_liberty_interest"]
        ))

        # 3. Stanley v. Illinois, 405 U.S. 645 (1972) - Unfit Parent Hearing Requirement
        docs.append(self.create_opinion_document(
            case_name="Stanley v. Illinois",
            citation="405 U.S. 645",
            jurisdiction="US",
            level="federal",
            court_name="Supreme Court of the United States",
            decision_date=date(1972, 4, 3),
            syllabus=(
                "Under Illinois law, children of unwed fathers, upon the death of the mother, were declared state wards without any hearing on "
                "the father's fitness, while married fathers and unwed mothers were entitled to fitness hearings before state removal."
            ),
            holding=(
                "Under the Due Process and Equal Protection Clauses, all parents are constitutionally entitled to a hearing on their fitness "
                "before their children are removed from their custody."
            ),
            reasoning=(
                "The private interest of a parent in the companionship, care, custody, and management of their children warrants deference and, "
                "absent a powerful countervailing interest, protection. The State may not conveniently presume unfitness without individualized process."
            ),
            cps_topics=["fitness_hearing", "due_process", "equal_protection", "unwed_fathers"]
        ))

        # 4. Lassiter v. Department of Social Services, 452 U.S. 18 (1981) - Right to Appointed Counsel
        docs.append(self.create_opinion_document(
            case_name="Lassiter v. Department of Social Services",
            citation="452 U.S. 18",
            jurisdiction="US",
            level="federal",
            court_name="Supreme Court of the United States",
            decision_date=date(1981, 6, 1),
            syllabus=(
                "An indigent mother had her parental rights terminated without the assistance of appointed counsel. She asserted a categorical "
                "right to appointed counsel under the Fourteenth Amendment Due Process Clause."
            ),
            holding=(
                "The Fourteenth Amendment Due Process Clause does not require the appointment of counsel in every parental termination proceeding, "
                "but rather leaves the decision to be made in the first instance by the trial court under the Eldridge balancing test, subject to "
                "appellate review. (Note: Most state statutes, including WA, IL, OH, CA, TX, NY, provide a mandatory statutory right to counsel)."
            ),
            reasoning=(
                "The pre-eminent generalization that emerges from precedent is that an indigent litigant has a right to appointed counsel only "
                "when, if he loses, he may be deprived of his physical liberty. In other cases, the Eldridge factors (private interests, risk of "
                "error, government interests) determine whether due process demands appointed counsel."
            ),
            cps_topics=["appointed_counsel", "indigent_parents", "due_process", "eldridge_test"]
        ))

        # 5. Haaland v. Brackeen, 599 U.S. 255 (2023) - Constitutionality of ICWA
        docs.append(self.create_opinion_document(
            case_name="Haaland v. Brackeen",
            citation="599 U.S. 255",
            jurisdiction="US",
            level="federal",
            court_name="Supreme Court of the United States",
            decision_date=date(2023, 6, 15),
            syllabus=(
                "Texas and individual foster parents challenged the Indian Child Welfare Act (ICWA) as exceeding Congress's Article I powers, "
                "violating the Tenth Amendment anti-commandeering doctrine, and violating the Equal Protection component of Fifth Amendment due process."
            ),
            holding=(
                "Congress acted within its broad Article I plenary power over Indian affairs in enacting ICWA, and its placement standards and "
                "procedural requirements do not violate the Tenth Amendment anti-commandeering doctrine."
            ),
            reasoning=(
                "Congress's power to legislate with respect to Indians is well established and broad. State court compliance with federal procedural "
                "standards under ICWA (active efforts, tribal notice, placement preferences) represents valid exercise of supremacy over state laws."
            ),
            cps_topics=["icwa", "constitutional_validity", "tenth_amendment", "article_i", "supremacy_clause"]
        ))

        # 6. In re Dependency of K.N.J., 171 Wn.2d 568 (2011) - Washington Notice & Due Process
        docs.append(self.create_opinion_document(
            case_name="In re Dependency of K.N.J.",
            citation="171 Wn.2d 568",
            jurisdiction="US-WA",
            level="state",
            court_name="Supreme Court of Washington",
            decision_date=date(2011, 6, 9),
            syllabus=(
                "In a dependency proceeding, a parent challenged an order where the specific parental deficiencies relied upon to terminate rights "
                "were not properly alleged in the dependency petition or adequately noticed."
            ),
            holding=(
                "Due process requires that parents receive adequate notice of the specific deficiencies alleged so they have a meaningful opportunity "
                "to defend and remedy them with offered services."
            ),
            reasoning=(
                "A termination order cannot be sustained on grounds never identified in the dependency proceedings. Providing clear notice is "
                "indispensable to the requirement that the State offer reasonable services tailored to remedy identified deficiencies."
            ),
            cps_topics=["notice_requirement", "due_process", "tailored_services", "washington_precedent"]
        ))

        # 7. In re Arthur H., 212 Ill. 2d 441 (2004) - Illinois Adjudication Standards
        docs.append(self.create_opinion_document(
            case_name="In re Arthur H.",
            citation="212 Ill. 2d 441",
            jurisdiction="US-IL",
            level="state",
            court_name="Supreme Court of Illinois",
            decision_date=date(2004, 10, 7),
            syllabus=(
                "The trial court adjudicated a minor neglected and found both mother and non-custodial father responsible for the neglect under "
                "the Illinois Juvenile Court Act (705 ILCS 405/2-18)."
            ),
            holding=(
                "Under the Juvenile Court Act, an adjudicatory hearing determines whether a minor is neglected or abused, not whether a specific "
                "parent is at fault. The adjudication relates to the status of the child, whereas parental fitness is determined at subsequent disposition."
            ),
            reasoning=(
                "The statutory framework separates the determination of whether a child is neglected from the determination of parental custody or "
                "fitness. Conflating these two stages undermines the two-step structure mandated by the General Assembly."
            ),
            cps_topics=["adjudication", "child_status", "two_step_procedure", "illinois_precedent"]
        ))

        # 8. In re B.C., 141 Ohio St. 3d 1 (2014) - Ohio Reasonable Efforts Standard
        docs.append(self.create_opinion_document(
            case_name="In re B.C.",
            citation="141 Ohio St. 3d 1",
            jurisdiction="US-OH",
            level="state",
            court_name="Supreme Court of Ohio",
            decision_date=date(2014, 10, 16),
            syllabus=(
                "Appellee mother challenged a permanent custody determination where children services agency failed to prove it made reasonable "
                "efforts to reunify the family prior to seeking permanent custody under ORC § 2151.419."
            ),
            holding=(
                "Except for statutory exceptions in ORC 2151.419(A)(2), the public children services agency has the burden of proving that it made "
                "reasonable efforts to prevent the removal of the child, eliminate continued removal, or make it possible for the child to return home."
            ),
            reasoning=(
                "The child welfare agency cannot bypass the reasonable efforts requirement. The trial court must make an explicit finding on whether "
                "reasonable efforts were made and specify the services provided."
            ),
            cps_topics=["reasonable_efforts", "agency_burden", "mandatory_findings", "ohio_precedent"]
        ))

        # 9. In re Marilyn H., 5 Cal. 4th 295 (1993) - California Permanency Planning & Due Process
        docs.append(self.create_opinion_document(
            case_name="In re Marilyn H.",
            citation="5 Cal. 4th 295",
            jurisdiction="US-CA",
            level="state",
            court_name="Supreme Court of California",
            decision_date=date(1993, 6, 3),
            syllabus=(
                "Parents challenged California Welfare & Institutions Code § 366.26 on due process grounds, arguing that terminating parental rights "
                "without a separate present unfitness finding at the permanency hearing violated the Fourteenth Amendment."
            ),
            holding=(
                "California's statutory dependency scheme satisfies due process because the prior series of review hearings and findings of detrimental "
                "return establish sufficient unfitness before the Section 366.26 hearing is reached."
            ),
            reasoning=(
                "The dependency process in California is cumulative. Once reunification services are terminated at a 12- or 18-month review, the focus "
                "shifts decisively from parental reunification to the child's compelling need for permanency and stability."
            ),
            cps_topics=["permanency_planning", "due_process", "section_366_26", "california_precedent"]
        ))

        # 10. Nicholson v. Scoppetta, 3 N.Y.3d 357 (2004) - New York Imminent Risk Standard for Emergency Removal
        docs.append(self.create_opinion_document(
            case_name="Nicholson v. Scoppetta",
            citation="3 N.Y.3d 357",
            jurisdiction="US-NY",
            level="state",
            court_name="New York Court of Appeals",
            decision_date=date(2004, 10, 26),
            syllabus=(
                "Class action challenging New York City ACS policy of automatically removing children under Family Court Act § 1024 from battered "
                "mothers solely on the ground that they had suffered domestic violence in the presence of the child."
            ),
            holding=(
                "Emergency removal without court order under FCA § 1024 requires imminent risk of harm and cannot be based solely on a parent's "
                "status as a victim of domestic violence. In an emergency removal application or Section 1028 hearing, ACS must establish that "
                "continuation in the home presents imminent danger to child's life or health and that removal is strictly necessary."
            ),
            reasoning=(
                "Holding a victimized mother per se unfit unfairly punishes the victim and traumatizes the child. The statutory standard demands "
                "an individualized showing of imminent harm, not sweeping administrative policy."
            ),
            cps_topics=["emergency_removal", "imminent_risk", "section_1028", "domestic_violence", "new_york_precedent"]
        ))

        return docs

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return self.get_canonical_precedents()
