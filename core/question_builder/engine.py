"""Question Builder Engine: Generates prioritized tactical questions and document checklists."""

from typing import List, Optional, Dict, Any

from legal_registry.loader import RegistryLoader, default_registry
from core.question_builder.models import (
    TargetRecipient,
    QuestionPriorityTier,
    QuestionItem,
    QuestionBuilderRequest,
    QuestionBuilderReport,
)


class QuestionBuilderEngine:
    """Builds prioritized question sets and document checklists grounded in procedural authority."""

    def __init__(self, registry: Optional[RegistryLoader] = None):
        self.registry = registry or default_registry

    def _normalize_recipient(self, recipient: Optional[str]) -> str:
        if not recipient:
            return TargetRecipient.ATTORNEY.value
        clean = recipient.upper().strip()
        for r in TargetRecipient:
            if r.value == clean or r.name == clean:
                return r.value
        return TargetRecipient.ATTORNEY.value

    def build_questions(self, request: QuestionBuilderRequest) -> QuestionBuilderReport:
        """Generates prioritized questions strictly tiered: Rights -> Deadlines -> Procedure -> Documentation."""
        sit = request.situation.lower().replace("-", "_").strip()
        recipient = self._normalize_recipient(request.target_recipient)
        state = (request.jurisdiction or "US").upper().replace("US-", "").strip()

        questions: List[QuestionItem] = []
        docs_to_request: List[str] = []
        docs_to_bring: List[str] = []
        tactical_tips: List[str] = []

        # =========================================================================
        # SITUATION: EMERGENCY REMOVAL / SHELTER HEARING / CPS
        # =========================================================================
        if any(term in sit for term in ("removal", "shelter", "cps", "dependency", "detention")):
            # TIER 1: RIGHTS
            if recipient in (TargetRecipient.ATTORNEY.value, TargetRecipient.ALL.value):
                questions.append(QuestionItem(
                    id="q-attorney-rights-1",
                    target_recipient=TargetRecipient.ATTORNEY.value,
                    priority_tier=QuestionPriorityTier.TIER_1_RIGHTS.value,
                    category="RIGHTS",
                    question_text="Will you request immediate return of my child today under the statutory standard of imminent risk of harm, or argue for immediate kinship placement with family?",
                    rationale="Forces counsel to confront whether the state has met its heavy burden for continued detention.",
                    statutory_hook="Fourteenth Amendment Substantive Due Process; State Removal Standards",
                    expected_response_type="Specific legal argument strategy"
                ))
                questions.append(QuestionItem(
                    id="q-attorney-rights-2",
                    target_recipient=TargetRecipient.ATTORNEY.value,
                    priority_tier=QuestionPriorityTier.TIER_1_RIGHTS.value,
                    category="RIGHTS",
                    question_text="Has the court formally inquired into Indian Child Welfare Act (ICWA) eligibility, and should we assert tribal affiliation?",
                    rationale="ICWA triggers heightened standards of proof (clear and convincing evidence / beyond reasonable doubt) and mandatory tribal notice.",
                    statutory_hook="25 U.S.C. § 1912(a); Mississippi Band of Choctaw Indians v. Holyfield",
                    expected_response_type="Confirmation of ICWA inquiry"
                ))

            if recipient in (TargetRecipient.CASEWORKER.value, TargetRecipient.ALL.value):
                questions.append(QuestionItem(
                    id="q-caseworker-rights-1",
                    target_recipient=TargetRecipient.CASEWORKER.value,
                    priority_tier=QuestionPriorityTier.TIER_1_RIGHTS.value,
                    category="RIGHTS",
                    question_text="Have you conducted the mandatory statutory background checks on the relatives whose names and phone numbers I provided for kinship placement?",
                    rationale="State agencies are federally mandated to prioritize adult relatives before stranger foster care.",
                    statutory_hook="42 U.S.C. § 671(a)(29); State Kinship Preference Statutes",
                    expected_response_type="Status of relative home assessments"
                ))
                questions.append(QuestionItem(
                    id="q-caseworker-rights-2",
                    target_recipient=TargetRecipient.CASEWORKER.value,
                    priority_tier=QuestionPriorityTier.TIER_1_RIGHTS.value,
                    category="RIGHTS",
                    question_text="What is the schedule for my legally mandated parent-child visitation, and when does the first visit take place?",
                    rationale="Frequent parent-child visitation is critical to preserving attachment and reunifying the family.",
                    statutory_hook="State Child Welfare Visitation Guidelines",
                    expected_response_type="Specific calendar dates and times"
                ))

            if recipient in (TargetRecipient.COURT.value, TargetRecipient.ALL.value):
                questions.append(QuestionItem(
                    id="q-court-rights-1",
                    target_recipient=TargetRecipient.COURT.value,
                    priority_tier=QuestionPriorityTier.TIER_1_RIGHTS.value,
                    category="RIGHTS",
                    question_text="Your Honor, will the Court order the agency to evaluate the maternal/paternal relatives for immediate temporary custody today?",
                    rationale="Kinship placement minimizes trauma and keeps children within family networks.",
                    statutory_hook="Federal Fostering Connections Act / State Placement Statutes",
                    expected_response_type="Judicial ruling on kinship assessment"
                ))

            # TIER 2: DEADLINES
            if recipient in (TargetRecipient.ATTORNEY.value, TargetRecipient.ALL.value):
                questions.append(QuestionItem(
                    id="q-attorney-deadlines-1",
                    target_recipient=TargetRecipient.ATTORNEY.value,
                    priority_tier=QuestionPriorityTier.TIER_2_DEADLINES.value,
                    category="DEADLINES",
                    question_text="What is the exact statutory deadline for the state to file its formal petition and for the court to conduct the adjudicatory fact-finding trial?",
                    rationale="Ensures counsel monitors statutory speedy adjudication clocks and preserves motions to dismiss for untimely proceedings.",
                    statutory_hook="State Juvenile Court Statutory Timeframes (e.g. 705 ILCS 405/2-14, RCW 13.34.110)",
                    expected_response_type="Calendar date and citation"
                ))

            if recipient in (TargetRecipient.CASEWORKER.value, TargetRecipient.ALL.value):
                questions.append(QuestionItem(
                    id="q-caseworker-deadlines-1",
                    target_recipient=TargetRecipient.CASEWORKER.value,
                    priority_tier=QuestionPriorityTier.TIER_2_DEADLINES.value,
                    category="DEADLINES",
                    question_text="When will the written Family Service Plan / Case Plan be provided to me and my attorney for review?",
                    rationale="Agencies must establish individualized service plans within 30-60 days of removal.",
                    statutory_hook="42 U.S.C. § 675(1); State Case Planning Rules",
                    expected_response_type="Written delivery date"
                ))

            # TIER 3: PROCEDURAL STATUS
            if recipient in (TargetRecipient.ATTORNEY.value, TargetRecipient.ALL.value):
                questions.append(QuestionItem(
                    id="q-attorney-proc-1",
                    target_recipient=TargetRecipient.ATTORNEY.value,
                    priority_tier=QuestionPriorityTier.TIER_3_PROCEDURAL_STATUS.value,
                    category="PROCEDURE",
                    question_text="Are you filing a motion for formal discovery to obtain all caseworker field notes, audio recordings, and medical reports?",
                    rationale="Formal discovery is essential to prevent trial by ambush and expose contradictory caseworker narratives.",
                    statutory_hook="Juvenile Court Discovery Rules",
                    expected_response_type="Discovery timeline and subpoena plan"
                ))

            if recipient in (TargetRecipient.CASEWORKER.value, TargetRecipient.ALL.value):
                questions.append(QuestionItem(
                    id="q-caseworker-proc-1",
                    target_recipient=TargetRecipient.CASEWORKER.value,
                    priority_tier=QuestionPriorityTier.TIER_3_PROCEDURAL_STATUS.value,
                    category="PROCEDURE",
                    question_text="What specific safety concerns does the agency claim prevent my child from remaining safely at home under a protective supervision order?",
                    rationale="Forces caseworker to articulate concrete facts rather than vague generalized safety claims.",
                    statutory_hook="Reasonable Efforts Doctrine; 42 U.S.C. § 671(a)(15)",
                    expected_response_type="Factual explanation of immediate danger"
                ))

            # TIER 4: EVIDENCE & DOCUMENTATION
            if recipient in (TargetRecipient.ATTORNEY.value, TargetRecipient.ALL.value):
                questions.append(QuestionItem(
                    id="q-attorney-evidence-1",
                    target_recipient=TargetRecipient.ATTORNEY.value,
                    priority_tier=QuestionPriorityTier.TIER_4_EVIDENCE_DOCUMENTATION.value,
                    category="DOCUMENTATION",
                    question_text="How can we submit my evidence (proof of stable housing, employment, drug screens, and character references) into the court record today?",
                    rationale="Puts affirmative evidence of parental fitness directly into the record to rebut state assertions.",
                    statutory_hook="Rules of Evidence - Authentication & Admissibility",
                    expected_response_type="Document filing procedure"
                ))

            if recipient in (TargetRecipient.CASEWORKER.value, TargetRecipient.ALL.value):
                questions.append(QuestionItem(
                    id="q-caseworker-evidence-1",
                    target_recipient=TargetRecipient.CASEWORKER.value,
                    priority_tier=QuestionPriorityTier.TIER_4_EVIDENCE_DOCUMENTATION.value,
                    category="DOCUMENTATION",
                    question_text="Can you provide me with written confirmation and agency referral forms for all required classes, drug tests, or evaluations?",
                    rationale="Prevents caseworker from later alleging non-compliance when the agency failed to make timely referrals.",
                    statutory_hook="Mandatory Reasonable Efforts Provision",
                    expected_response_type="Written referral packets"
                ))

            # Checklists
            docs_to_request = [
                "Copy of Dependency / Temporary Custody Petition",
                "Law Enforcement Incident Report and Field Notes",
                "Affidavit of Imminent Danger or Removal Warrant",
                "Temporary Custody Order signed by Judge",
                "Relative Kinship Placement Screening Packet",
                "Initial Child Welfare Investigation Summary / Screener Intake Report"
            ]

            docs_to_bring = [
                "Government-issued photo identification",
                "Child's birth certificate and Social Security card (if in parent's possession)",
                "Written list of 3-5 responsible adult relatives (names, addresses, phone numbers, relationship)",
                "Proof of current stable residence (lease, deed, or utility bill in parent's name)",
                "Proof of employment or income (recent paystubs, benefits statement)",
                "Medical or prescription records (showing any positive test was medically prescribed)"
            ]

            tactical_tips = [
                "Never attend a court hearing or agency meeting without taking detailed notes.",
                "Always communicate with caseworkers via email or text to create an auditable written record.",
                "Never sign an agreement, service plan, or admission of neglect without your attorney reviewing it first.",
                "Present relative placement options to the agency and court at the earliest possible hour."
            ]

        # =========================================================================
        # SITUATION: SERVICE PLAN MEETING (CPS CASEWORKER)
        # =========================================================================
        elif any(term in sit for term in ("service_plan", "isp", "case_plan", "team_decision")):
            # TIER 1: RIGHTS
            questions.append(QuestionItem(
                id="q-plan-rights-1",
                target_recipient=TargetRecipient.CASEWORKER.value,
                priority_tier=QuestionPriorityTier.TIER_1_RIGHTS.value,
                category="RIGHTS",
                question_text="How does each required service specifically address the reason the court assumed jurisdiction over my child?",
                rationale="Services must be reasonably tailored to remedy the specific allegations, not generic punitive assignments.",
                statutory_hook="42 U.S.C. § 675; State Reasonable Efforts Mandate",
                expected_response_type="Nexus explanation for each service"
            ))
            questions.append(QuestionItem(
                id="q-plan-rights-2",
                target_recipient=TargetRecipient.CASEWORKER.value,
                priority_tier=QuestionPriorityTier.TIER_1_RIGHTS.value,
                category="RIGHTS",
                question_text="Will our visitation schedule expand to unsupervised or overnight visits once I complete the initial phase of the plan?",
                rationale="Reunification requires a progressive step-up in visitation frequency and duration.",
                statutory_hook="Family Preservation and Reunification Doctrine",
                expected_response_type="Milestones for increasing visitation"
            ))

            # TIER 2: DEADLINES
            questions.append(QuestionItem(
                id="q-plan-deadlines-1",
                target_recipient=TargetRecipient.CASEWORKER.value,
                priority_tier=QuestionPriorityTier.TIER_2_DEADLINES.value,
                category="DEADLINES",
                question_text="What is the target completion date for each service, and when is the next formal court review hearing?",
                rationale="Prevents endless delays that run the 15/22 month ASFA termination clock.",
                statutory_hook="Adoption and Safe Families Act (ASFA), 42 U.S.C. § 675(5)(E)",
                expected_response_type="Target dates in writing"
            ))

            # TIER 3: PROCEDURE
            questions.append(QuestionItem(
                id="q-plan-proc-1",
                target_recipient=TargetRecipient.CASEWORKER.value,
                priority_tier=QuestionPriorityTier.TIER_3_PROCEDURAL_STATUS.value,
                category="PROCEDURE",
                question_text="If I encounter a waiting list for a required service, what alternative provider will the agency pay for and approve?",
                rationale="Protects parent from being penalized for community agency provider waiting lists.",
                statutory_hook="State Agency Service Availability Obligations",
                expected_response_type="Alternative provider protocol"
            ))

            # TIER 4: DOCUMENTATION
            questions.append(QuestionItem(
                id="q-plan-doc-1",
                target_recipient=TargetRecipient.CASEWORKER.value,
                priority_tier=QuestionPriorityTier.TIER_4_EVIDENCE_DOCUMENTATION.value,
                category="DOCUMENTATION",
                question_text="Can you provide me with written proof of service referrals and confirming that the state is covering the cost of these services?",
                rationale="Documents compliance and prevents financial barriers from obstructing reunification.",
                statutory_hook="Title IV-E State Plan Requirements",
                expected_response_type="Written referral documentation"
            ))

            docs_to_request = [
                "Draft Individualized Service Plan (ISP)",
                "Written Visitation Schedule and Rules",
                "Service Provider Referral Authorization Letters",
                "Contact names and phone numbers for all designated service providers"
            ]

            docs_to_bring = [
                "Work schedule and transportation availability details",
                "Certificates or records of any programs or classes already attended",
                "List of family support network members who can assist with transportation or childcare"
            ]

            tactical_tips = [
                "Request that your attorney participate in all service plan conferences.",
                "Ensure services fit your work schedule so you are not set up to fail.",
                "Obtain written attendance records from every class or therapy session you attend."
            ]

        # =========================================================================
        # GENERAL / CIVIL / CRIMINAL FALLBACK
        # =========================================================================
        else:
            questions.append(QuestionItem(
                id="q-general-rights-1",
                target_recipient=recipient,
                priority_tier=QuestionPriorityTier.TIER_1_RIGHTS.value,
                category="RIGHTS",
                question_text="What constitutional and statutory rights apply to my current procedural posture, and how are we asserting them?",
                rationale="Fundamental rights must be affirmatively invoked to avoid waiver.",
                statutory_hook="Due Process of Law",
                expected_response_type="Analysis of rights"
            ))
            questions.append(QuestionItem(
                id="q-general-deadlines-1",
                target_recipient=recipient,
                priority_tier=QuestionPriorityTier.TIER_2_DEADLINES.value,
                category="DEADLINES",
                question_text="What is the next mandatory statutory filing or appearance deadline in this case?",
                rationale="Missing a court deadline can result in default, waiver, or sanctions.",
                statutory_hook="Rules of Procedure",
                expected_response_type="Exact date and filing rule"
            ))
            questions.append(QuestionItem(
                id="q-general-proc-1",
                target_recipient=recipient,
                priority_tier=QuestionPriorityTier.TIER_3_PROCEDURAL_STATUS.value,
                category="PROCEDURE",
                question_text="What specific order or pleading was entered most recently, and what is our procedural response?",
                rationale="Maintains tactical command over case progression.",
                statutory_hook="Governing Procedural Code",
                expected_response_type="Case status review"
            ))
            questions.append(QuestionItem(
                id="q-general-doc-1",
                target_recipient=recipient,
                priority_tier=QuestionPriorityTier.TIER_4_EVIDENCE_DOCUMENTATION.value,
                category="DOCUMENTATION",
                question_text="What specific documentary evidence or records do we need to obtain immediately to support our position?",
                rationale="Evidence must be gathered before it is altered, lost, or made inaccessible.",
                statutory_hook="Evidentiary Proof Standards",
                expected_response_type="Evidentiary checklist"
            ))

            docs_to_request = ["Complete copy of court docket", "Copies of all filed pleadings and orders"]
            docs_to_bring = ["All notices, correspondence, and court papers received to date", "Personal timeline of key dates"]
            tactical_tips = ["Keep all court documents organized in chronological order in a dedicated binder."]

        # Sort questions strictly by priority tier (1 -> 2 -> 3 -> 4)
        sorted_questions = sorted(questions, key=lambda q: q.priority_tier)

        summary = (
            f"Generated {len(sorted_questions)} prioritized question(s) for {recipient} regarding {sit} "
            f"in jurisdiction {state}. Ordered strictly by priority hierarchy: Rights -> Deadlines -> Procedure -> Documentation."
        )

        return QuestionBuilderReport(
            situation=request.situation,
            target_recipient=recipient,
            jurisdiction=state,
            user_role=request.user_role or "parent",
            prioritized_questions=sorted_questions,
            documents_to_request=docs_to_request,
            documents_to_bring=docs_to_bring,
            tactical_tips=tactical_tips,
            summary=summary
        )
