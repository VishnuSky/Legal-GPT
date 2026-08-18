"""Parent Rights & Reasonable Efforts Engine."""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class ParentRightCheck(BaseModel):
    right_name: str
    guaranteed_by: str # e.g. "RCW 13.34.090", "705 ILCS 405/2-9", "Due Process Clause"
    description: str
    status: str # "COMPLIANT", "VIOLATION_SUSPECTED", "INCOMPLETE_FACTS"
    statutory_citations: List[str] = Field(default_factory=list)


class ParentRightsAuditor:
    @staticmethod
    def evaluate_parent_rights(
        state: str,
        notice_given: bool,
        counsel_present: bool,
        services_offered: bool,
        is_icwa: bool = False
    ) -> List[ParentRightCheck]:
        checks = []
        state_code = state.upper()

        # 1. Right to Notice
        if notice_given:
            checks.append(ParentRightCheck(
                right_name="Right to Timely Notice",
                guaranteed_by=f"{state_code} Dependency Statutes & 14th Amendment Due Process",
                description="Parent must receive formal written summons and timely notice of all hearings.",
                status="COMPLIANT",
                statutory_citations=["RCW 13.34.070" if state_code == "WA" else "705 ILCS 405/2-15" if state_code == "IL" else "ORC § 2151.28"]
            ))
        else:
            checks.append(ParentRightCheck(
                right_name="Right to Timely Notice",
                guaranteed_by=f"{state_code} Dependency Statutes & 14th Amendment Due Process",
                description="Failure to provide notice violates statutory requirements and procedural due process.",
                status="VIOLATION_SUSPECTED",
                statutory_citations=["RCW 13.34.070" if state_code == "WA" else "705 ILCS 405/2-15" if state_code == "IL" else "ORC § 2151.28"]
            ))

        # 2. Right to Appointed Counsel
        if counsel_present:
            checks.append(ParentRightCheck(
                right_name="Right to Legal Counsel",
                guaranteed_by=f"{state_code} Indigent Defense Statutes",
                description="Parent is represented by counsel at all critical stages of child welfare proceedings.",
                status="COMPLIANT",
                statutory_citations=["RCW 13.34.090" if state_code == "WA" else "705 ILCS 405/2-9" if state_code == "IL" else "ORC § 2151.352"]
            ))
        else:
            checks.append(ParentRightCheck(
                right_name="Right to Legal Counsel",
                guaranteed_by=f"{state_code} Indigent Defense Statutes",
                description="Unrepresented indigent parent in dependency proceeding requires immediate court appointment of counsel.",
                status="VIOLATION_SUSPECTED",
                statutory_citations=["RCW 13.34.090" if state_code == "WA" else "705 ILCS 405/2-9" if state_code == "IL" else "ORC § 2151.352"]
            ))

        # 3. Reasonable Efforts / Active Efforts (ICWA)
        efforts_std = "Active Efforts" if is_icwa else "Reasonable Efforts"
        citation = "25 U.S.C. § 1912(d)" if is_icwa else ("RCW 13.34.180(1)(d)" if state_code == "WA" else "705 ILCS 405/2-10" if state_code == "IL" else "ORC § 2151.419")

        if services_offered:
            checks.append(ParentRightCheck(
                right_name=f"{efforts_std} by Child Welfare Agency",
                guaranteed_by=f"Title IV-E (42 U.S.C. § 671) & {citation}",
                description="Agency must provide all reasonably available remedial services capable of correcting parental deficiencies.",
                status="COMPLIANT",
                statutory_citations=[citation]
            ))
        else:
            checks.append(ParentRightCheck(
                right_name=f"{efforts_std} by Child Welfare Agency",
                guaranteed_by=f"Title IV-E (42 U.S.C. § 671) & {citation}",
                description="Agency's failure to offer tailored remedial services constitutes lack of required reasonable/active efforts.",
                status="VIOLATION_SUSPECTED",
                statutory_citations=[citation]
            ))

        return checks
