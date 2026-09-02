"""Procedural and Court Rule Engine (Phase 3.5): Motions, Deadlines, Service, and Exhibits."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ProceduralMotionGuide(BaseModel):
    motion_name: str
    case_type: str  # Child Dependency, Custody, Child Protection, Civil
    jurisdiction: str
    court_level: str
    procedural_posture: str
    governing_court_rule: str
    governing_statute: str
    statutory_deadline: str
    prerequisites: List[str]
    service_requirements: str
    filing_requirements: str
    required_exhibits_and_forms: List[str]
    hearing_standards_and_burden: str
    possible_outcomes: List[str]


class ProceduralEngine:
    """Answers: What can a litigant/attorney do, where, how, and by when?"""

    def __init__(self):
        self.guides: Dict[str, List[ProceduralMotionGuide]] = {}
        self._init_core_procedural_guides()

    def _init_core_procedural_guides(self):
        # 1. Washington State: Rehearing / Contest Shelter Care
        self.add_guide(ProceduralMotionGuide(
            motion_name="Affidavit for Rehearing of Shelter Care Order & Motion for Release",
            case_type="Child Dependency",
            jurisdiction="US-WA",
            court_level="Superior Court (Juvenile Division)",
            procedural_posture="Post-Emergency Removal / 72-Hour Shelter Care",
            governing_court_rule="JuCR 2.4 & Local Juvenile Rule 2.4",
            governing_statute="RCW 13.34.065(1)(b) & RCW 13.34.065(4)",
            statutory_deadline="Rehearing must be held within 72 hours of filing parent affidavit",
            prerequisites=[
                "Parent establishes lack of actual notice of initial shelter care hearing, OR",
                "Parent presents newly discovered evidence showing safety threat eliminated."
            ],
            service_requirements="Personal service on DCYF Assistant Attorney General (AAG) and Child's Attorney/CASA within 24 hours.",
            filing_requirements="File with Superior Court Clerk; note motion on the Juvenile Dependency Motion Docket.",
            required_exhibits_and_forms=[
                "Affidavit of Parent establishing lack of notice or changed circumstances",
                "Proposed In-Home Safety Plan with non-offending relatives / caregivers",
                "Proof of Clean Urinalysis or Completed Safety Assessment (if substance alleged)"
            ],
            hearing_standards_and_burden="Department bears burden of proving by a preponderance of the evidence that serious danger exists and reasonable efforts cannot prevent removal.",
            possible_outcomes=[
                "Immediate release of child to parent custody with in-home safety plan",
                "Placement with approved relative (kinship placement)",
                "Continuation of out-of-home shelter care with expanded family visitation"
            ]
        ))

        # 2. New York State: Application to Return Child Temporarily Removed (§ 1028)
        self.add_guide(ProceduralMotionGuide(
            motion_name="Section 1028 Application for Immediate Return of Temporarily Removed Child",
            case_type="Child Protective Proceeding",
            jurisdiction="US-NY",
            court_level="Family Court",
            procedural_posture="Emergency Removal under FCA § 1024 or § 1027",
            governing_court_rule="Uniform Rules for the Family Court (22 NYCRR Part 205)",
            governing_statute="N.Y. Fam. Ct. Act § 1028",
            statutory_deadline="Hearing MUST be held within 3 court days of filing application (cannot adjourn > 3 days without consent)",
            prerequisites=[
                "Child was removed without court order under § 1024 or preliminary order under § 1027",
                "Parent or person legally responsible applies for immediate return"
            ],
            service_requirements="Immediate service upon County Attorney / ACS and Attorney for the Child (AFC).",
            filing_requirements="Written or oral application made in Family Court on the record.",
            required_exhibits_and_forms=[
                "Form 10-14 (Application for Return of Child)",
                "Evidence showing removal was not necessary to prevent imminent risk to life/health (Nicholson v. Scoppetta)",
                "Safety plan documentation"
            ],
            hearing_standards_and_burden="Court shall grant application and return child unless agency proves by a preponderance that return presents imminent risk to child's life or health.",
            possible_outcomes=[
                "Immediate return of child to parent custody with protective supervision",
                "Denial of application; continuation of temporary remand to ACS"
            ]
        ))

        # 3. Illinois: Motion for Rehearing on Temporary Custody
        self.add_guide(ProceduralMotionGuide(
            motion_name="Motion for Rehearing on Temporary Custody",
            case_type="Child Protection / Juvenile Court",
            jurisdiction="US-IL",
            court_level="Circuit Court (Child Protection Division)",
            procedural_posture="Post-48-Hour Temporary Custody Hearing",
            governing_court_rule="Illinois Supreme Court Rules Part F (Child Protection)",
            governing_statute="705 ILCS 405/2-10(b)",
            statutory_deadline="Within 14 days of the entry of the temporary custody order",
            prerequisites=[
                "Parent was not personally served or had no actual notice of the 48-hour hearing",
                "Affidavit establishing lack of notice filed"
            ],
            service_requirements="Service upon State's Attorney and Public Guardian / Child's Attorney.",
            filing_requirements="File with Clerk of the Circuit Court (Cook County or local county).",
            required_exhibits_and_forms=[
                "Affidavit of Parent / Guardian",
                "Motion to Vacate Temporary Custody Order"
            ],
            hearing_standards_and_burden="State must re-establish probable cause and urgent/immediate necessity for continuing custody.",
            possible_outcomes=[
                "Vacating of temporary custody order and return of minor to parental home",
                "Order of Protection entered under 705 ILCS 405/2-25"
            ]
        ))

        # 4. Texas: Contest at Full Adversary Hearing (14-Day Hearing)
        self.add_guide(ProceduralMotionGuide(
            motion_name="Special Appearance / Motion to Return Child at Full Adversary Hearing",
            case_type="Suit Affecting Parent-Child Relationship (SAPCR)",
            jurisdiction="US-TX",
            court_level="District Court / County Court at Law",
            procedural_posture="Emergency Removal under Chapter 262",
            governing_court_rule="Texas Rules of Civil Procedure Rule 120a",
            governing_statute="Tex. Fam. Code § 262.201",
            statutory_deadline="Mandatory hearing held not later than the 14th day after emergency removal",
            prerequisites=[
                "DFPS took possession under ex parte emergency order without parent present"
            ],
            service_requirements="Citation and notice served on parent at least 3 days prior to hearing.",
            filing_requirements="Answer and Counter-Pleading for Return filed with District Clerk.",
            required_exhibits_and_forms=[
                "Parent Sworn Statement",
                "Relative Caregiver Home Assessment Request"
            ],
            hearing_standards_and_burden="Court shall order return of child unless DFPS proves sufficient evidence to satisfy a person of ordinary prudence that continuing danger exists.",
            possible_outcomes=[
                "Full return of child to parent",
                "Monitored return under DFPS supervision",
                "Temporary Managing Conservatorship (TMC) awarded to DFPS"
            ]
        ))

    def add_guide(self, guide: ProceduralMotionGuide):
        key = f"{guide.jurisdiction}:{guide.procedural_posture.upper()}"
        if key not in self.guides:
            self.guides[key] = []
        self.guides[key].append(guide)

    def get_guides_for_posture(self, jurisdiction: str, posture: str) -> List[ProceduralMotionGuide]:
        results = []
        for key, guide_list in self.guides.items():
            if jurisdiction in key or "US:" in key:
                for g in guide_list:
                    if posture.lower() in g.procedural_posture.lower() or posture.lower() in g.case_type.lower():
                        results.append(g)
        return results


# Global singleton
procedural_engine = ProceduralEngine()
