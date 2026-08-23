"""Adversarial / Counterargument Reviewer Agent: Proactively Challenges Arguments Before Output."""

import uuid
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AdversarialCounterargument(BaseModel):
    counterargument_id: str = Field(default_factory=lambda: f"ADV-{uuid.uuid4().hex[:6].upper()}")
    claim_challenged: str
    challenge_category: str  # PROCEDURAL_POSTURE, STATUTORY_EXCEPTION, BURDEN_NOT_MET, EVIDENCE_INSUFFICIENT, LIMITED_PRECEDENT
    opposing_argument: str
    opposing_authority: Optional[str] = None
    risk_level: str  # LOW, MODERATE, HIGH
    rebuttal_strategy: str


class AdversarialReviewer:
    """Simulates opposing counsel and judicial skepticism: 'Why might this legal position fail?'"""

    @classmethod
    def review_case_theory(
        cls,
        state: str,
        stage: str,
        notice_given: bool = True,
        counsel_present: bool = True,
        services_offered: bool = True,
        is_icwa: bool = False,
        facts_summary: Optional[str] = None
    ) -> List[AdversarialCounterargument]:
        counterarguments = []

        # 1. Challenge on Emergency Removal Exigency
        if "REMOVAL" in stage.upper():
            counterarguments.append(AdversarialCounterargument(
                claim_challenged="State lacked lawful authority to remove child without prior court order.",
                challenge_category="STATUTORY_EXCEPTION",
                opposing_argument=(
                    "The child protective agency or law enforcement officer will assert the 'imminent danger / exigent harm' exception, "
                    "arguing there was insufficient time to seek a warrant because the child was in immediate physical peril."
                ),
                opposing_authority=f"{state} Emergency Removal Statutes (e.g., RCW 13.34.055 / FCA § 1024 / WIC § 305)",
                risk_level="HIGH",
                rebuttal_strategy=(
                    "Demand specific, contemporaneous factual evidence of an immediate physical threat occurring at the time of seizure, "
                    "rather than generalized historical allegations or non-exigent conditions (Nicholson v. Scoppetta)."
                )
            ))

        # 2. Challenge on Reasonable Efforts
        if services_offered:
            counterarguments.append(AdversarialCounterargument(
                claim_challenged="Agency failed to provide adequate reasonable efforts to prevent removal or reunify.",
                challenge_category="BURDEN_NOT_MET",
                opposing_argument=(
                    "The Department will introduce documentation showing service referrals were provided, and argue that the parent "
                    "failed to actively engage or complete the offered programs in a timely manner."
                ),
                opposing_authority="42 U.S.C. § 671(a)(15) & State Reasonable Efforts Standards",
                risk_level="MODERATE",
                rebuttal_strategy=(
                    "Argue services were generic rather than tailored to the specific parental deficiencies identified in the court petition, "
                    "or demonstrate that practical barriers (lack of transportation, housing, scheduling) prevented participation (In re Dependency of K.N.J.)."
                )
            ))

        # 3. Challenge on ICWA Inquiry
        if is_icwa:
            counterarguments.append(AdversarialCounterargument(
                claim_challenged="State court failed to conduct complete ICWA inquiry and send registered mail notice.",
                challenge_category="EVIDENCE_INSUFFICIENT",
                opposing_argument=(
                    "The State may argue the parent failed to provide specific tribal affiliation or enrollment documentation, "
                    "rendering ICWA inapplicable at preliminary stages."
                ),
                opposing_authority="25 CFR § 23.107 & 25 U.S.C. § 1912(a)",
                risk_level="MODERATE",
                rebuttal_strategy=(
                    "Cite 25 CFR § 23.107(b): When there is 'reason to know', the court and agency have an affirmative, ongoing duty of due diligence "
                    "to contact the Tribe and treat the child as an Indian child pending formal determination."
                )
            ))

        # 4. Challenge on 72-Hour / 48-Hour Deadline Computation
        counterarguments.append(AdversarialCounterargument(
            claim_challenged="The statutory deadline for the shelter care / detention hearing was violated.",
            challenge_category="PROCEDURAL_POSTURE",
            opposing_argument=(
                "The State will argue statutory time computation rules exclude Saturdays, Sundays, and legal court holidays, "
                "or that preliminary good cause extensions were granted."
            ),
            opposing_authority=f"{state} Court Rules & Time Computation Statutes",
            risk_level="LOW",
            rebuttal_strategy=(
                "Review the exact court clerk time stamp of physical removal and petition filing, counting only legitimate judicial days."
            )
        ))

        return counterarguments
