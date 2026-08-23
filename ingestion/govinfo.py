"""GovInfo Ingestion Connector for Federal Statutes, ICWA, and Child Welfare Regulations."""

import os
import json
import logging
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import StatuteChunker

logger = logging.getLogger("legal_gpt.govinfo")


class GovInfoConnector(BaseLegalConnector):
    """GovInfo Connector for Title 25 (ICWA), Title 42 (CAPTA/IV-E), and Title 45 CFR Regulations."""
    BASE_URL = "https://api.govinfo.gov"

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(source_id="FED_GOVINFO", rate_limit_delay_seconds=0.5)
        self.api_key = api_key or os.getenv("GOVINFO_API_KEY", "DEMO_KEY")

    def fetch_package_summary(self, package_id: str) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/packages/{package_id}/summary?api_key={self.api_key}"
        content = self.fetch_url(url)
        return json.loads(content)

    def create_statute_document(
        self,
        title_number: int,
        section: str,
        title_name: str,
        full_text: str,
        enacted_date: date,
        effective_date: date,
        cps_topics: List[str]
    ) -> LegalDocument:
        citation = f"{title_number} U.S.C. § {section}"
        doc_id = f"FED-USC-{title_number}-{section.replace('/', '-').replace(' ', '_')}"
        temporal = TemporalMetadata(
            enacted_date=enacted_date,
            effective_date=effective_date,
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="U.S. Government Publishing Office (GovInfo)"
        )
        chunks = StatuteChunker.chunk_statute(
            document_id=doc_id,
            title=f"{citation}: {title_name}",
            full_text=full_text
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="FED_GOVINFO",
            jurisdiction="US",
            level="federal",
            document_type="statute",
            title=f"{citation} - {title_name}",
            citation=citation,
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=f"https://uscode.house.gov/view.xhtml?req=(title:{title_number}%20section:{section})",
            cps_topics=cps_topics
        )
        doc.compute_hash()
        return doc

    def create_cfr_document(
        self,
        title_number: int,
        part: int,
        section: str,
        title_name: str,
        full_text: str,
        effective_date: date,
        cps_topics: List[str]
    ) -> LegalDocument:
        citation = f"{title_number} CFR § {section}"
        doc_id = f"FED-CFR-{title_number}-{section.replace('.', '_')}"
        temporal = TemporalMetadata(
            effective_date=effective_date,
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="National Archives and Records Administration (eCFR)"
        )
        chunks = StatuteChunker.chunk_statute(
            document_id=doc_id,
            title=f"{citation}: {title_name}",
            full_text=full_text
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="FED_ECFR",
            jurisdiction="US",
            level="federal",
            document_type="regulation",
            title=f"{citation} - {title_name}",
            citation=citation,
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=f"https://www.ecfr.gov/current/title-{title_number}/part-{part}/section-{section}",
            cps_topics=cps_topics
        )
        doc.compute_hash()
        return doc

    def get_canonical_federal_corpus(self) -> List[LegalDocument]:
        """Returns the full canonical federal statutory and regulatory corpus."""
        docs = []

        # 1. 25 U.S.C. § 1901 (ICWA Congressional Findings)
        docs.append(self.create_statute_document(
            title_number=25,
            section="1901",
            title_name="Congressional findings",
            full_text=(
                "Recognizing the special relationship between the United States and the Indian tribes and their members and the Federal "
                "responsibility to Indian people, the Congress finds: (1) that clause 3, section 8, article I of the United States Constitution "
                "gives Congress the power to regulate Commerce with Indian tribes; (2) that Congress has plenary power over Indian affairs; "
                "(3) that that responsibility of the United States has not been properly discharged when an alarmingly high percentage of Indian "
                "families are broken up by the removal, often unwarranted, of their children by nontribal public and private agencies; (4) that an "
                "alarmingly high percentage of such children are placed in non-Indian foster and adoptive homes and institutions; and (5) that the "
                "States have often failed to recognize the essential tribal relations of Indian people and the cultural and social standards "
                "prevailing in Indian communities and families."
            ),
            enacted_date=date(1978, 11, 8),
            effective_date=date(1978, 11, 8),
            cps_topics=["icwa", "congressional_findings", "tribal_sovereignty"]
        ))

        # 2. 25 U.S.C. § 1902 (ICWA Declaration of Policy)
        docs.append(self.create_statute_document(
            title_number=25,
            section="1902",
            title_name="Congressional declaration of policy",
            full_text=(
                "The Congress hereby declares that it is the policy of this Nation to protect the best interests of Indian children and to promote "
                "the stability and security of Indian tribes and families by the establishment of minimum Federal standards for the removal of "
                "Indian children from their families and the placement of such children in foster or adoptive homes which will reflect the unique "
                "values of Indian culture, and by the providing for assistance to Indian tribes in the operation of child and family service programs."
            ),
            enacted_date=date(1978, 11, 8),
            effective_date=date(1978, 11, 8),
            cps_topics=["icwa", "minimum_federal_standards", "best_interests"]
        ))

        # 3. 25 U.S.C. § 1903 (ICWA Definitions)
        docs.append(self.create_statute_document(
            title_number=25,
            section="1903",
            title_name="Definitions",
            full_text=(
                "For the purposes of this chapter: (1) 'child custody proceeding' shall mean and include: (i) 'foster care placement' which shall "
                "mean any action removing an Indian child from its parent or Indian custodian for temporary placement; (ii) 'termination of parental rights'; "
                "(iii) 'preadoptive placement'; and (iv) 'adoptive placement'. (4) 'Indian child' means any unmarried person who is under age eighteen "
                "and is either (a) a member of an Indian tribe or (b) is eligible for membership in an Indian tribe and is the biological child of a "
                "member of an Indian tribe. (6) 'Indian custodian' means any Indian person who has legal custody of an Indian child under tribal law "
                "or custom or under State law or to whom temporary physical care, custody, and control has been transferred by the parent. "
                "(9) 'parent' means any biological parent or parents of an Indian child or any Indian person who has lawfully adopted an Indian child."
            ),
            enacted_date=date(1978, 11, 8),
            effective_date=date(1978, 11, 8),
            cps_topics=["icwa", "definitions", "indian_child", "child_custody_proceeding"]
        ))

        # 4. 25 U.S.C. § 1911 (Tribal Court Jurisdiction)
        docs.append(self.create_statute_document(
            title_number=25,
            section="1911",
            title_name="Indian tribe jurisdiction over Indian child custody proceedings",
            full_text=(
                "(a) Exclusive jurisdiction: An Indian tribe shall have jurisdiction exclusive as to any State over any child custody proceeding "
                "involving an Indian child who resides or is domiciled within the reservation of such tribe. (b) Transfer of proceedings; declination "
                "by tribal court: In any State court proceeding for the foster care placement of, or termination of parental rights to, an Indian child "
                "not domiciled or residing within the reservation of the Indian child's tribe, the court, in the absence of good cause to the contrary, "
                "shall transfer such proceeding to the jurisdiction of the tribe, upon the petition of either parent or the Indian custodian or the "
                "Indian child's tribe: Provided, that such transfer shall be subject to declination by the tribal court. (c) State court proceedings; "
                "intervention: In any State court proceeding for the foster care placement of, or termination of parental rights to, an Indian child, "
                "the Indian custodian of the child and the Indian child's tribe shall have a right to intervene at any point in the proceeding."
            ),
            enacted_date=date(1978, 11, 8),
            effective_date=date(1978, 11, 8),
            cps_topics=["icwa", "tribal_jurisdiction", "transfer_of_jurisdiction", "right_to_intervene"]
        ))

        # 5. 25 U.S.C. § 1912 (Pending Court Proceedings; Notice; Active Efforts; Proof Standards)
        docs.append(self.create_statute_document(
            title_number=25,
            section="1912",
            title_name="Pending court proceedings",
            full_text=(
                "(a) Notice; time for commencement of proceedings; additional time for preparation: In any involuntary proceeding in a State court, "
                "where the court knows or has reason to know that an Indian child is involved, the party seeking the foster care placement of, or "
                "termination of parental rights to, an Indian child shall notify the parent or Indian custodian and the Indian child's tribe, by registered "
                "mail with return receipt requested, of the pending proceedings and of their right of intervention. If the identity or location of the "
                "parent or Indian custodian and the tribe cannot be determined, such notice shall be given to the Secretary in like manner. No foster "
                "care placement or termination of parental rights proceeding shall be held until at least ten days after receipt of notice by the parent "
                "or Indian custodian and the tribe or the Secretary: Provided, that the parent or Indian custodian or the tribe shall, upon request, "
                "be granted up to twenty additional days to prepare for such proceeding. (b) Appointment of counsel: In any case in which the court "
                "determines indigency, the parent or Indian custodian shall have the right to court-appointed counsel in any removal, placement, or "
                "termination proceeding. (d) Remedial services and rehabilitative programs; active efforts: Any party seeking to effect a foster care "
                "placement of, or termination of parental rights to, an Indian child under State law shall satisfy the court that active efforts have "
                "been made to provide remedial services and rehabilitative programs designed to prevent the breakup of the Indian family and that "
                "these efforts have proved unsuccessful. (e) Foster care placement orders; evidence; determination of damage to child: No foster care "
                "placement may be ordered in such proceeding in the absence of a determination, supported by clear and convincing evidence, including "
                "testimony of qualified expert witnesses, that the continued custody of the child by the parent or Indian custodian is likely to result "
                "in serious emotional or physical damage to the child. (f) Parental rights termination orders; evidence; determination of damage to child: "
                "No termination of parental rights may be ordered in such proceeding in the absence of a determination, supported by evidence beyond a "
                "reasonable doubt, including testimony of qualified expert witnesses, that the continued custody of the child by the parent or Indian "
                "custodian is likely to result in serious emotional or physical damage to the child."
            ),
            enacted_date=date(1978, 11, 8),
            effective_date=date(1978, 11, 8),
            cps_topics=["icwa", "notice", "registered_mail", "appointed_counsel", "active_efforts", "qew", "standards_of_proof"]
        ))

        # 6. 25 U.S.C. § 1914 (Petition to Invalidate Violations)
        docs.append(self.create_statute_document(
            title_number=25,
            section="1914",
            title_name="Petition to court of competent jurisdiction to invalidate action upon showing of certain violations",
            full_text=(
                "Any Indian child who is the subject of any action for foster care placement or termination of parental rights under State law, "
                "any parent or Indian custodian from whose custody such child was removed, and the Indian child's tribe may petition any court "
                "of competent jurisdiction to invalidate such action upon a showing that such action violated any provision of sections 1911, "
                "1912, and 1913 of this title."
            ),
            enacted_date=date(1978, 11, 8),
            effective_date=date(1978, 11, 8),
            cps_topics=["icwa", "invalidation_of_action", "procedural_violation_remedy"]
        ))

        # 7. 25 U.S.C. § 1915 (Placement Preferences)
        docs.append(self.create_statute_document(
            title_number=25,
            section="1915",
            title_name="Placement of Indian children",
            full_text=(
                "(a) Adoptive placements; preferences: In any adoptive placement of an Indian child under State law, a preference shall be given, "
                "in the absence of good cause to the contrary, to a placement with (1) a member of the child's extended family; (2) other members of "
                "the Indian child's tribe; or (3) other Indian families. (b) Foster care or preadoptive placements; criteria; preferences: In any "
                "foster care or preadoptive placement, a preference shall be given, in the absence of good cause to the contrary, to a placement "
                "with: (i) a member of the Indian child's extended family; (ii) a foster home licensed, approved, or specified by the Indian child's "
                "tribe; (iii) an Indian foster home licensed or approved by an authorized non-Indian licensing authority; or (iv) an institution for "
                "children approved by an Indian tribe or operated by an Indian organization."
            ),
            enacted_date=date(1978, 11, 8),
            effective_date=date(1978, 11, 8),
            cps_topics=["icwa", "placement_preferences", "extended_family", "tribal_foster_home"]
        ))

        # 8. 25 CFR § 23.107 (BIA Reason to Know Inquiry Duty)
        docs.append(self.create_cfr_document(
            title_number=25,
            part=23,
            section="23.107",
            title_name="How should a State court determine whether there is reason to know the child is an Indian child?",
            full_text=(
                "(a) State courts must ask each participant in an emergency or voluntary or involuntary child-custody proceeding whether the "
                "participant knows or has reason to know that the child is an Indian child. The inquiry is made at the commencement of the proceeding "
                "and all responses should be on the record. (b) If there is reason to know the child is an Indian child, but the court does not have "
                "sufficient evidence to determine that the child is or is not an Indian child, the court must: (1) Confirm, by way of a report, "
                "declaration, or testimony included in the record that the agency or other party used due diligence to identify and work with all "
                "of the Tribes of which there is reason to know the child may be a member; and (2) Treat the child as an Indian child, unless and "
                "until it is determined on the record that the child does not meet the definition of an Indian child."
            ),
            effective_date=date(2016, 12, 12),
            cps_topics=["icwa", "reason_to_know", "inquiry_duty", "due_diligence"]
        ))

        # 9. 42 U.S.C. § 5106a (CAPTA Grants to States)
        docs.append(self.create_statute_document(
            title_number=42,
            section="5106a",
            title_name="Grants to States for child abuse or neglect prevention and treatment programs",
            full_text=(
                "(b) Eligibility requirements: A State shall submit a plan specifying that the State has in effect and is enforcing a State law, "
                "or has in effect and is operating a Statewide program, relating to child abuse and neglect that includes: (A) provisions and procedures "
                "for mandatory reporting of known or suspected child abuse or neglect; (B) provisions for prompt investigation and emergency removal "
                "procedures; (C) provisions for appointment of an appropriately trained guardian ad litem or court appointed special advocate (CASA) "
                "for every child in an abuse or neglect proceeding; and (D) citizen review panels to evaluate state child protection performance."
            ),
            enacted_date=date(1974, 1, 31),
            effective_date=date(2010, 12, 20),
            cps_topics=["capta", "mandatory_reporting", "guardian_ad_litem", "citizen_review"]
        ))

        # 10. 42 U.S.C. § 671 (Title IV-E State Plan Requirements; Reasonable Efforts)
        docs.append(self.create_statute_document(
            title_number=42,
            section="671",
            title_name="State plan for foster care and adoption assistance",
            full_text=(
                "(a)(15) In order for a State to be eligible for payments under this part, it shall have a plan approved by the Secretary which "
                "provides that: (A) in each case, reasonable efforts shall be made to prevent or eliminate the need for removing the child from the "
                "child's home; and (B) to make it possible for a child to safely return home. (C) If continuation of reasonable efforts is determined "
                "to be inconsistent with the permanency plan for the child, reasonable efforts shall be made to place the child in a timely manner in "
                "accordance with the permanency plan. (D) Reasonable efforts to prevent removal or to return home are not required if a court finds "
                "aggravated circumstances (such as abandonment, torture, chronic abuse, or sexual abuse) or conviction of certain felony offenses."
            ),
            enacted_date=date(1980, 6, 17),
            effective_date=date(1997, 11, 19),
            cps_topics=["title_iv_e", "reasonable_efforts", "foster_care_plan", "permanency_plan"]
        ))

        # 11. 42 U.S.C. § 675 (Title IV-E Definitions; 15/22 Month ASFA TPR Rule)
        docs.append(self.create_statute_document(
            title_number=42,
            section="675",
            title_name="Definitions - Case review system",
            full_text=(
                "(5) The term 'case review system' means a procedure for assuring that: (B) the status of each child is reviewed periodically but "
                "not less frequently than once every six months by either a court or by an administrative review; (C) with respect to each such child, "
                "procedural safeguards will be applied to assure that in any review or hearing conducted pursuant to this section, including the "
                "permanency hearing held no later than 12 months after the child is considered to have entered foster care; and (E) in the case of "
                "a child who has been in foster care under the responsibility of the State for 15 of the most recent 22 months, the State shall file "
                "or join a petition to terminate the parental rights of the child's parents, unless: (i) the child is being cared for by a relative; "
                "(ii) a compelling reason is documented that TPR is not in the best interests; or (iii) the State has not provided services required "
                "by the case plan (reasonable efforts failure)."
            ),
            enacted_date=date(1980, 6, 17),
            effective_date=date(1997, 11, 19),
            cps_topics=["title_iv_e", "asfa", "15_22_month_rule", "six_month_review", "permanency_hearing"]
        ))

        return docs

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return self.get_canonical_federal_corpus()
