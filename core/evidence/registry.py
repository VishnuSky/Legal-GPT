"""Pre-seeded canonical legal elements and missing evidence templates."""

from typing import Dict, List, Optional
from core.evidence.models import LegalElement


CANONICAL_LEGAL_ELEMENTS: List[LegalElement] = [
    LegalElement(
        element_id="NOTICE_REQUIREMENT",
        element_name="Notice Requirement",
        governing_authority="U.S. Const. amend. XIV (Due Process; Mullane v. Central Hanover Bank); RCW 13.34.070; 705 ILCS 405/2-15; Fla. Stat. § 39.402",
        authority_tier="TIER_0",
        required_proof_standard="Preponderance of the Evidence / Procedural Due Process",
        standard_evidentiary_predicates=[
            "Date notice was issued and delivered",
            "Identified recipient (parent, custodian, or designated legal guardian)",
            "Authorized delivery method (personal service, certified mail, or court-ordered publication)",
            "Substantive content specifying factual allegations, statutory grounds, and hearing location",
            "Proof of service affidavit signed by authorized process server"
        ],
        default_missing_elements=[
            "Date",
            "Recipient",
            "Method",
            "Content",
            "Proof of service"
        ],
        standard_research_questions=[
            "Was legally required notice provided to the parent in compliance with statutory service standards?",
            "Did the notice contain specific factual allegations or merely uncorroborated statutory boilerplate?",
            "Was proof of service filed with the court clerk prior to the preliminary hearing?"
        ]
    ),

    LegalElement(
        element_id="WARRANT_REQUIREMENT",
        element_name="Fourth Amendment Warrant Requirement / Home Entry",
        governing_authority="U.S. Const. amend. IV; Doe v. Heck, 327 F.3d 492; Camara v. Municipal Court, 387 U.S. 523",
        authority_tier="TIER_0",
        required_proof_standard="Probable Cause / Strict Exigency Exception",
        standard_evidentiary_predicates=[
            "Signed judicial warrant or emergency court order authorizing entry",
            "Sworn probable cause affidavit reviewed by neutral judicial magistrate",
            "Date, timestamp, and specific physical location authorized for search",
            "Specific documented exigent circumstances if entry occurred without a warrant",
            "Written inventory / return of search warrant filed with court clerk"
        ],
        default_missing_elements=[
            "Signed judicial search warrant",
            "Sworn officer / caseworker probable cause affidavit",
            "Contemporaneous facts establishing imminent bodily peril prior to entry",
            "Formal return of warrant"
        ],
        standard_research_questions=[
            "Did the caseworker or law enforcement officer possess a valid judicial warrant prior to entering the residence?",
            "If warrantless, what specific articulable facts established an imminent threat of severe physical harm before a warrant could be secured?",
            "Did the occupant give free, voluntary, and uncoerced consent to enter?"
        ]
    ),

    LegalElement(
        element_id="REASONABLE_EFFORTS",
        element_name="Reasonable / Active Efforts Requirement",
        governing_authority="Title IV-E 42 U.S.C. § 671(a)(15); RCW 13.34.180(1)(d); 705 ILCS 405/2-10; ICWA 25 U.S.C. § 1912(d)",
        authority_tier="TIER_0",
        required_proof_standard="Clear and Convincing Evidence (or Beyond a Reasonable Doubt for ICWA)",
        standard_evidentiary_predicates=[
            "Written referral letters for court-ordered remedial services",
            "Evidence of agency financial assistance, transportation, or language accommodations",
            "Caseworker engagement logs detailing proactive assistance",
            "Provider attendance, progress, and discharge reports",
            "Active efforts documentation involving Indian child's tribe"
        ],
        default_missing_elements=[
            "Written service referral documentation",
            "Proof that agency offered transportation, language, or financial assistance",
            "Caseworker service coordination logs",
            "Provider progress evaluations"
        ],
        standard_research_questions=[
            "Did the agency make affirmative, tailored, and timely efforts to provide remedial services to prevent removal?",
            "Were the offered services tailored to the parent's specific language, disability, and cultural needs?",
            "If the child is an Indian child, did the agency satisfy the heightened active efforts standard under 25 U.S.C. § 1912(d)?"
        ]
    ),

    LegalElement(
        element_id="IMMINENT_PHYSICAL_DANGER",
        element_name="Imminent Physical Danger / Emergency Removal Standard",
        governing_authority="RCW 13.34.050; 705 ILCS 405/2-8; Fla. Stat. § 39.401; Tex. Fam. Code § 262.104",
        authority_tier="TIER_0",
        required_proof_standard="Reasonable Cause to Believe Immediate Serious Physical Danger Exists",
        standard_evidentiary_predicates=[
            "Contemporaneous physical observations of severe injury or immediate threat",
            "Independent law enforcement or medical physician report",
            "Elimination of reasonable in-home safety plan alternatives",
            "Immediate risk assessment conducted prior to custodial removal"
        ],
        default_missing_elements=[
            "Objective medical or forensic evaluation of alleged injury",
            "Contemporaneous photographic evidence of physical hazard",
            "Explanation of why child could not remain safely with non-offending parent or relative"
        ],
        standard_research_questions=[
            "Was the child in immediate danger of serious physical harm at the exact moment of emergency removal?",
            "Could the perceived safety risk have been mitigated through an in-home safety plan or relative placement without removal?",
            "What objective corroborating evidence supports the caseworker's emergency determination?"
        ]
    )
]


class LegalElementRegistry:
    """Indexed lookup for canonical legal elements and missing evidence templates."""

    _ELEMENTS_BY_ID: Dict[str, LegalElement] = {e.element_id: e for e in CANONICAL_LEGAL_ELEMENTS}

    @classmethod
    def get_all(cls) -> List[LegalElement]:
        return list(cls._ELEMENTS_BY_ID.values())

    @classmethod
    def get_by_id(cls, element_id: str) -> Optional[LegalElement]:
        return cls._ELEMENTS_BY_ID.get(element_id)

    @classmethod
    def find_matching_element(cls, issue_text: str) -> LegalElement:
        """Finds closest legal element matching an issue string or falls back to Notice."""
        low = issue_text.lower()
        if any(term in low for term in ["warrant", "fourth amendment", "search", "home entry"]):
            return cls._ELEMENTS_BY_ID["WARRANT_REQUIREMENT"]
        if any(term in low for term in ["effort", "services", "active effort", "remedial"]):
            return cls._ELEMENTS_BY_ID["REASONABLE_EFFORTS"]
        if any(term in low for term in ["imminent", "danger", "harm", "removal", "emergency"]):
            return cls._ELEMENTS_BY_ID["IMMINENT_PHYSICAL_DANGER"]
        return cls._ELEMENTS_BY_ID["NOTICE_REQUIREMENT"]
