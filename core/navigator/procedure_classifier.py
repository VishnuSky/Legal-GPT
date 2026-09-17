"""Procedural Posture, Hearing, and Deadline Classifier for Public Legal Navigator."""

import re
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from core.navigator.issue_classifier import LegalDomain


class ProceduralPosture(str, Enum):
    INVESTIGATION = "INVESTIGATION"                    # Pre-filing agency inquiry, interviews, home visits
    NOTICE_CITATION = "NOTICE_CITATION"                # Written notice received, notice to vacate, summons delivered
    COMPLAINT_PETITION = "COMPLAINT_PETITION"          # Formal petition or civil complaint filed in court
    AGENCY_ACTION = "AGENCY_ACTION"                    # Emergency administrative removal, finding entered, license suspended
    PRELIMINARY_HEARING = "PRELIMINARY_HEARING"        # Immediate shelter care hearing, detention hearing, initial appearance
    TRIAL_ADJUDICATION = "TRIAL_ADJUDICATION"          # Fact-finding hearing, contested evidentiary trial, disposition
    APPEAL_REVIEW = "APPEAL_REVIEW"                    # Adverse order entered, seeking rehearing, reconsideration, or appeal
    SETTLEMENT_AGREEMENT = "SETTLEMENT_AGREEMENT"      # Safety plan signed, agreed order, mediation, voluntary services
    ENFORCEMENT_EXECUTION = "ENFORCEMENT_EXECUTION"    # Writ issued, termination of rights order, judgment enforcement


class ProcedureClassificationResult(BaseModel):
    posture: ProceduralPosture
    posture_description: str
    typical_next_event: str
    urgent_deadlines: List[str] = Field(default_factory=list)
    mandatory_notices: List[str] = Field(default_factory=list)
    available_motions_or_pleadings: List[str] = Field(default_factory=list)
    immediate_procedural_steps: List[str] = Field(default_factory=list)


class ProcedureClassifier:
    """Classifies case procedural posture and identifies statutory deadlines, required notices, and motions."""

    @classmethod
    def classify_posture(
        cls,
        narrative: str,
        domain: LegalDomain = LegalDomain.CPS_CHILD_WELFARE,
        state: Optional[str] = None
    ) -> ProcedureClassificationResult:
        """Determines the apparent procedural stage from factual keywords and context."""
        low = narrative.lower()
        st = state.upper() if state else "WA"

        # 1. Appeal / Rehearing
        if any(term in low for term in ["appeal", "appealing", "order entered", "lost at trial", "rehearing", "reconsideration"]):
            return ProcedureClassificationResult(
                posture=ProceduralPosture.APPEAL_REVIEW,
                posture_description="Final or interlocutory court order entered; litigant is seeking appellate or rehearing review.",
                typical_next_event="Filing Notice of Appeal or Motion for Rehearing with the trial/appellate court clerk.",
                urgent_deadlines=[
                    "Notice of Appeal deadline: Typically 30 days from entry of final written order",
                    "Motion for Rehearing on Shelter Care: Within 72 hours of filing parent affidavit (WA RCW 13.34.065(1)(b))",
                    "Section 1028 Rehearing: Hearing within 3 court days of application (NY Fam. Ct. Act § 1028)"
                ],
                mandatory_notices=["Written notice of appeal served on all opposing counsel and the court clerk"],
                available_motions_or_pleadings=[
                    "Motion and Affidavit for Rehearing of Order",
                    "Notice of Appeal / Motion for Discretionary Review",
                    "Motion for Stay of Order Pending Appeal"
                ],
                immediate_procedural_steps=[
                    "Request a certified copy of the written order and judge's findings of fact immediately.",
                    "Request trial court transcripts / verbatim report of proceedings from the court reporter.",
                    "Note the jurisdictional 30-day appeal deadline; courts strictly enforce this deadline."
                ]
            )

        # 2. Preliminary Hearing / Shelter Care / Detention
        if any(term in low for term in ["hearing tomorrow", "court tomorrow", "shelter care hearing", "detention hearing", "initial hearing", "hearing on"]):
            return cls._build_preliminary_hearing_result(st)

        # 3. Emergency Removal / Agency Action
        if any(term in low for term in ["removed", "took my child", "taken into custody", "protective custody", "emergency custody"]):
            return ProcedureClassificationResult(
                posture=ProceduralPosture.AGENCY_ACTION,
                posture_description="Emergency intervention or custody seizure has taken place; statutory hearing clocks are actively running.",
                typical_next_event="Emergency initial detention or shelter care hearing before a juvenile/family court judge.",
                urgent_deadlines=cls._get_emergency_removal_deadlines(st),
                mandatory_notices=[
                    "Immediate formal written notice of child removal and reason for custody",
                    "Notice of exact date, time, and courtroom for initial emergency hearing",
                    "Notice of statutory right to court-appointed indigent counsel"
                ],
                available_motions_or_pleadings=[
                    "Motion for Immediate Return of Minor / Emergency Rehearing",
                    "Notice of Appearance & Request for Appointed Counsel",
                    "Proposed Kinship Placement Affidavit"
                ],
                immediate_procedural_steps=[
                    "Contact the juvenile/family court clerk immediately to find out the scheduled hearing time.",
                    "Arrive at the courtroom early and formally request court-appointed legal counsel on the record.",
                    "Identify non-offending family relatives with clean backgrounds and submit an In-Home Safety Plan."
                ]
            )

        # 4. Formal Petition / Summons Served
        if any(term in low for term in ["served", "summons", "petition filed", "lawsuit", "complaint"]):
            return ProcedureClassificationResult(
                posture=ProceduralPosture.COMPLAINT_PETITION,
                posture_description="Formal legal complaint or dependency petition has been filed and summons served.",
                typical_next_event="Initial appearance, arraignment, or filing formal responsive answer/motion.",
                urgent_deadlines=[
                    "Filing formal written Answer or Notice of Appearance: Typically 20–30 days from service",
                    "Fact-Finding Adjudication: 75 days in WA (RCW 13.34.070), 90 days in IL (705 ILCS 405/2-14)"
                ],
                mandatory_notices=["Formal personal service of process with court seal, case caption, and summons"],
                available_motions_or_pleadings=[
                    "Notice of Appearance & Demand for Copy of Complaint",
                    "Motion to Quash Defective Service",
                    "Answer and Affirmative Defenses"
                ],
                immediate_procedural_steps=[
                    "Preserve the exact envelope and date on which papers were handed to you or found.",
                    "Calendar the appearance deadline immediately.",
                    "Consult an attorney or court facilitator before filing formal written answers."
                ]
            )

        # 5. Pre-filing Investigation / Safety Plan
        if any(term in low for term in ["investigation", "interview", "caseworker visited", "safety plan", "home visit", "hotline", "drug test"]):
            return ProcedureClassificationResult(
                posture=ProceduralPosture.INVESTIGATION,
                posture_description="Agency is conducting pre-petition administrative investigation; no court petition is currently active.",
                typical_next_event="Agency makes formal finding (founded/unfounded) or refers case for court petition filing.",
                urgent_deadlines=[
                    "Statutory investigation completion: Typically 30 to 60 days to close investigation or file petition",
                    "Voluntary safety plan duration: Typically 30 days unless extended by mutual consent"
                ],
                mandatory_notices=[
                    "Written advisement of interview purpose and parent rights under state administrative rules",
                    "Written notification of central registry finding if substantiated"
                ],
                available_motions_or_pleadings=[
                    "Written Request for Agency Referral Documentation",
                    "Administrative Appeal of Founded Finding",
                    "Revocation of Voluntary Release / Consent"
                ],
                immediate_procedural_steps=[
                    "Request all caseworker communications, safety expectations, and drug screen referrals in writing.",
                    "Remember that voluntary safety plans cannot be enforced by law enforcement without a court order.",
                    "Document every interaction in a private journal (date, time, caseworker name, statements made)."
                ]
            )

        # 6. Default Notice / Citation
        return ProcedureClassificationResult(
            posture=ProceduralPosture.NOTICE_CITATION,
            posture_description="Initial notice or dispute received; early stage of procedural progression.",
            typical_next_event="Deadline to respond or formal court filing if unresolved.",
            urgent_deadlines=["Check the face of the notice for any specific 3-day, 10-day, or 14-day response deadlines."],
            mandatory_notices=["Written notice setting forth specific factual basis for the claim or action."],
            available_motions_or_pleadings=["Written Response / Dispute Letter", "Notice of Representation / Self-Representation"],
            immediate_procedural_steps=[
                "Carefully inspect the notice for governing deadlines, statutory citations, and court case numbers.",
                "Seek legal aid consultation prior to the response deadline."
            ]
        )

    @classmethod
    def _build_preliminary_hearing_result(cls, state: str) -> ProcedureClassificationResult:
        deadlines = cls._get_emergency_removal_deadlines(state)
        return ProcedureClassificationResult(
            posture=ProceduralPosture.PRELIMINARY_HEARING,
            posture_description="Initial emergency detention or shelter care hearing scheduled within hours or days.",
            typical_next_event="Judicial shelter care hearing to determine temporary custody pending trial.",
            urgent_deadlines=deadlines,
            mandatory_notices=[
                "Summons and written notice of hearing time and location",
                "Notice of parent right to appointed counsel and right to cross-examine"
            ],
            available_motions_or_pleadings=[
                "Affidavit of In-Home Safety Plan",
                "Motion for Immediate Kinship Placement",
                "Request for Continuance to Retain/Consult Appointed Counsel"
            ],
            immediate_procedural_steps=[
                "Be present in the assigned courtroom at least 30 minutes before the scheduled time.",
                "Immediately state to the court clerk or judge: 'I am the respondent parent, I am indigent, and I request court-appointed counsel.'",
                "Do not agree to temporary custody or stipulate to allegations without consulting counsel on the record."
            ]
        )

    @classmethod
    def _get_emergency_removal_deadlines(cls, state: str) -> List[str]:
        if state == "WA":
            return [
                "Emergency custody without court order: 48 hours maximum (RCW 13.34.055)",
                "Mandatory Shelter Care Hearing: Within 72 hours excluding weekends/holidays (RCW 13.34.065)",
                "Rehearing upon Parent Affidavit: Within 72 hours of filing affidavit (JuCR 2.4)"
            ]
        elif state == "IL":
            return [
                "Temporary Custody Hearing: Within 48 hours of removal excluding weekends/holidays (705 ILCS 405/2-9)",
                "Adjudicatory Hearing: Within 90 days of service of summons (705 ILCS 405/2-14)"
            ]
        elif state == "OH":
            return [
                "Shelter Care / Detention Hearing: Within 72 hours of apprehension (ORC § 2151.314)",
                "Adjudicatory Hearing: Within 30 days of complaint (ORC § 2151.35)"
            ]
        elif state == "CA":
            return [
                "Detention Hearing: Within 48 to 72 hours excluding nonjudicial days (Cal. Welf. & Inst. Code § 315)",
                "Jurisdictional Hearing: Within 15 to 30 days of detention"
            ]
        elif state == "TX":
            return [
                "Full Adversary Hearing: Mandatory within 14 days of removal (Tex. Fam. Code § 262.201)",
                "Mandatory Suit Dismissal: Within 365 days if no trial commenced (Tex. Fam. Code § 263.401)"
            ]
        elif state == "NY":
            return [
                "Section 1028 Return Hearing: Mandatory within 3 court days of application (N.Y. Fam. Ct. Act § 1028)",
                "Preliminary Removal Hearing: Next court day following removal (N.Y. Fam. Ct. Act § 1027)"
            ]
        elif state == "FL":
            return [
                "Shelter Hearing: Mandatory within 24 hours of placement in shelter (Fla. Stat. § 39.402)",
                "Arraignment Hearing: Within 28 days of shelter hearing"
            ]
        else:
            return [
                "Initial Detention/Shelter Hearing: Typically within 24–72 hours of emergency removal under state law.",
                "Full Adjudication: Typically within 60–90 days of petition filing."
            ]
