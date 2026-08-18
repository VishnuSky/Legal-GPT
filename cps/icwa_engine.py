"""Indian Child Welfare Act (ICWA) & State ICWA Engine."""

from typing import List, Optional
from pydantic import BaseModel, Field


class ICWAComplianceEvaluation(BaseModel):
    is_icwa_eligible: bool
    tribal_inquiry_completed: bool
    mandatory_notice_sent: bool
    active_efforts_required: bool
    qew_required: bool # Qualified Expert Witness
    standard_of_proof_foster: str
    standard_of_proof_tpr: str
    statutory_authorities: List[str] = Field(default_factory=list)
    compliance_issues: List[str] = Field(default_factory=list)


class ICWAEngine:
    @classmethod
    def evaluate_icwa(
        cls,
        state: str,
        reason_to_know_indian_child: bool,
        tribal_inquiry_on_record: bool,
        tribe_notified_registered_mail: bool,
        stage: str # "foster_care", "tpr"
    ) -> ICWAComplianceEvaluation:
        state_code = state.upper()
        compliance_issues = []

        if not reason_to_know_indian_child:
            return ICWAComplianceEvaluation(
                is_icwa_eligible=False,
                tribal_inquiry_completed=tribal_inquiry_on_record,
                mandatory_notice_sent=False,
                active_efforts_required=False,
                qew_required=False,
                standard_of_proof_foster="Preponderance / Clear & Convincing (State Standard)",
                standard_of_proof_tpr="Clear & Convincing (State Standard)",
                compliance_issues=["Mandatory ICWA inquiry should still be documented on the court record in every child custody proceeding."] if not tribal_inquiry_on_record else []
            )

        # Child is or may be an Indian child
        if not tribal_inquiry_on_record:
            compliance_issues.append("Violation: Failure to document initial ICWA inquiry pursuant to 25 C.F.R. § 23.107.")

        if not tribe_notified_registered_mail:
            compliance_issues.append("Violation: Mandatory formal notice by registered mail (return receipt requested) to tribe/BIA not documented (25 U.S.C. § 1912(a)).")

        authorities = [
            "25 U.S.C. § 1901 et seq. (ICWA)",
            "25 C.F.R. Part 23 (BIA Regulations)",
        ]
        if state_code == "WA":
            authorities.append("RCW 13.38 (Washington State Indian Child Welfare Act - WICWA)")

        return ICWAComplianceEvaluation(
            is_icwa_eligible=True,
            tribal_inquiry_completed=tribal_inquiry_on_record,
            mandatory_notice_sent=tribe_notified_registered_mail,
            active_efforts_required=True,
            qew_required=True,
            standard_of_proof_foster="Clear and Convincing Evidence with Qualified Expert Witness (25 U.S.C. § 1912(e))",
            standard_of_proof_tpr="Beyond a Reasonable Doubt with Qualified Expert Witness (25 U.S.C. § 1912(f))",
            statutory_authorities=authorities,
            compliance_issues=compliance_issues
        )
