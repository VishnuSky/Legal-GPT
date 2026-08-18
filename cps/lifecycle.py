"""CPS / Child Welfare Case Lifecycle Engine (18 Stages)."""

from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field


class CPSStage(str, Enum):
    ALLEGATION = "ALLEGATION"
    SCREENING = "SCREENING"
    INTAKE = "INTAKE"
    INVESTIGATION = "INVESTIGATION"
    SAFETY_DECISION = "SAFETY_DECISION"
    VOLUNTARY_SERVICES = "VOLUNTARY_SERVICES"
    EMERGENCY_REMOVAL = "EMERGENCY_REMOVAL"
    SHELTER_CARE_HEARING = "SHELTER_CARE_HEARING"
    DEPENDENCY_PETITION = "DEPENDENCY_PETITION"
    FACT_FINDING_ADJUDICATION = "FACT_FINDING_ADJUDICATION"
    DISPOSITION = "DISPOSITION"
    PLACEMENT = "PLACEMENT"
    VISITATION_FAMILY_TIME = "VISITATION_FAMILY_TIME"
    CASE_PLAN = "CASE_PLAN"
    PERIODIC_REVIEW = "PERIODIC_REVIEW"
    PERMANENCY_PLANNING = "PERMANENCY_PLANNING"
    TPR_OR_GUARDIANSHIP = "TPR_OR_GUARDIANSHIP"
    APPEAL = "APPEAL"


class CPSStageRequirements(BaseModel):
    stage: CPSStage
    state: str
    required_notice_hours_or_days: Optional[str] = None
    right_to_counsel_appointed: bool = True
    standard_of_proof: Optional[str] = None
    mandatory_findings: List[str] = Field(default_factory=list)
    controlling_statute: Optional[str] = None


class CPSLifecycleEngine:
    # State-specific statutory mappings for stages
    STAGE_RULES = {
        "WA": {
            CPSStage.EMERGENCY_REMOVAL: CPSStageRequirements(
                stage=CPSStage.EMERGENCY_REMOVAL,
                state="WA",
                required_notice_hours_or_days="Immediate notice upon removal",
                standard_of_proof="Probable cause of imminent danger (court order) / imminent harm (police)",
                mandatory_findings=["Imminent danger to child's health, safety, or welfare", "Reasonable efforts made to prevent removal or lack of efforts reasonable"],
                controlling_statute="RCW 13.34.050 & RCW 13.34.055"
            ),
            CPSStage.SHELTER_CARE_HEARING: CPSStageRequirements(
                stage=CPSStage.SHELTER_CARE_HEARING,
                state="WA",
                required_notice_hours_or_days="Within 72 hours of removal (excluding weekends/holidays)",
                right_to_counsel_appointed=True,
                standard_of_proof="Reasonable cause",
                mandatory_findings=["Reasonable cause to believe child is dependent", "Release of child would present serious threat of substantial harm"],
                controlling_statute="RCW 13.34.065"
            ),
            CPSStage.FACT_FINDING_ADJUDICATION: CPSStageRequirements(
                stage=CPSStage.FACT_FINDING_ADJUDICATION,
                state="WA",
                required_notice_hours_or_days="Held within 75 days of petition filing",
                right_to_counsel_appointed=True,
                standard_of_proof="Preponderance of the evidence",
                mandatory_findings=["Child meets statutory definition of dependent under RCW 13.34.030"],
                controlling_statute="RCW 13.34.110"
            ),
            CPSStage.TPR_OR_GUARDIANSHIP: CPSStageRequirements(
                stage=CPSStage.TPR_OR_GUARDIANSHIP,
                state="WA",
                right_to_counsel_appointed=True,
                standard_of_proof="Clear, cogent, and convincing evidence (State) / Beyond a reasonable doubt (ICWA)",
                mandatory_findings=[
                    "Child has been found dependent",
                    "Court entered a dispositional order",
                    "Child removed for at least 6 months",
                    "Services offered/provided have been reasonable",
                    "Little likelihood conditions will be remedied in near future",
                    "Continuation of parent-child relationship clearly diminishes child's prospects for integration into a permanent home"
                ],
                controlling_statute="RCW 13.34.180 & RCW 13.34.190"
            )
        },
        "IL": {
            CPSStage.SHELTER_CARE_HEARING: CPSStageRequirements(
                stage=CPSStage.SHELTER_CARE_HEARING,
                state="IL",
                required_notice_hours_or_days="Within 48 hours of temporary custody (excluding weekends/holidays)",
                right_to_counsel_appointed=True,
                standard_of_proof="Probable cause & urgent and immediate necessity",
                mandatory_findings=["Probable cause that minor is abused/neglected/dependent", "Urgent and immediate necessity for temporary custody"],
                controlling_statute="705 ILCS 405/2-10"
            ),
            CPSStage.FACT_FINDING_ADJUDICATION: CPSStageRequirements(
                stage=CPSStage.FACT_FINDING_ADJUDICATION,
                state="IL",
                required_notice_hours_or_days="Held within 90 days of service of process",
                right_to_counsel_appointed=True,
                standard_of_proof="Preponderance of the evidence",
                mandatory_findings=["Minor is abused, neglected, or dependent"],
                controlling_statute="705 ILCS 405/2-14 & 2-18"
            )
        },
        "OH": {
            CPSStage.SHELTER_CARE_HEARING: CPSStageRequirements(
                stage=CPSStage.SHELTER_CARE_HEARING,
                state="OH",
                required_notice_hours_or_days="Held within 72 hours of taking into custody",
                right_to_counsel_appointed=True,
                standard_of_proof="Probable cause",
                mandatory_findings=["Probable cause that child is abused, neglected, or dependent", "Continuation in home contrary to child's welfare"],
                controlling_statute="ORC § 2151.314"
            ),
            CPSStage.FACT_FINDING_ADJUDICATION: CPSStageRequirements(
                stage=CPSStage.FACT_FINDING_ADJUDICATION,
                state="OH",
                required_notice_hours_or_days="Held within 30 days of complaint filing",
                right_to_counsel_appointed=True,
                standard_of_proof="Clear and convincing evidence",
                mandatory_findings=["Child is abused, neglected, or dependent under ORC 2151.03/2151.031/2151.04"],
                controlling_statute="ORC § 2151.35"
            )
        },
        "CA": {
            CPSStage.SHELTER_CARE_HEARING: CPSStageRequirements(
                stage=CPSStage.SHELTER_CARE_HEARING,
                state="CA",
                required_notice_hours_or_days="Detention hearing within 48 to 72 hours of removal (excluding nonjudicial days)",
                right_to_counsel_appointed=True,
                standard_of_proof="Prima facie showing of dependency",
                mandatory_findings=["Continuance in home contrary to child's welfare", "Reasonable efforts made to prevent removal"],
                controlling_statute="Cal. Welf. & Inst. Code § 315 & § 319"
            ),
            CPSStage.FACT_FINDING_ADJUDICATION: CPSStageRequirements(
                stage=CPSStage.FACT_FINDING_ADJUDICATION,
                state="CA",
                required_notice_hours_or_days="Jurisdictional hearing held within 30 days of detention",
                right_to_counsel_appointed=True,
                standard_of_proof="Preponderance of the evidence",
                mandatory_findings=["Child is described by one or more subdivisions of Section 300"],
                controlling_statute="Cal. Welf. & Inst. Code § 355"
            ),
            CPSStage.TPR_OR_GUARDIANSHIP: CPSStageRequirements(
                stage=CPSStage.TPR_OR_GUARDIANSHIP,
                state="CA",
                right_to_counsel_appointed=True,
                standard_of_proof="Clear and convincing evidence of adoptability",
                mandatory_findings=["Child is likely to be adopted", "Termination of parental rights not detrimental to child"],
                controlling_statute="Cal. Welf. & Inst. Code § 366.26"
            )
        },
        "TX": {
            CPSStage.SHELTER_CARE_HEARING: CPSStageRequirements(
                stage=CPSStage.SHELTER_CARE_HEARING,
                state="TX",
                required_notice_hours_or_days="Full Adversary Hearing held within 14 days of removal",
                right_to_counsel_appointed=True,
                standard_of_proof="Sufficient evidence to satisfy a person of ordinary prudence and caution",
                mandatory_findings=["Danger to physical health/safety caused by parent acts/omissions", "Reasonable efforts made to prevent removal"],
                controlling_statute="Tex. Fam. Code § 262.201"
            ),
            CPSStage.TPR_OR_GUARDIANSHIP: CPSStageRequirements(
                stage=CPSStage.TPR_OR_GUARDIANSHIP,
                state="TX",
                right_to_counsel_appointed=True,
                standard_of_proof="Clear and convincing evidence",
                mandatory_findings=["Parent committed one or more predicate acts under § 161.001(b)(1)", "Termination is in child's best interest"],
                controlling_statute="Tex. Fam. Code § 161.001"
            )
        },
        "NY": {
            CPSStage.SHELTER_CARE_HEARING: CPSStageRequirements(
                stage=CPSStage.SHELTER_CARE_HEARING,
                state="NY",
                required_notice_hours_or_days="Section 1028 hearing held within 3 court days of parent application",
                right_to_counsel_appointed=True,
                standard_of_proof="Imminent risk to child's life or health",
                mandatory_findings=["Imminent risk to child", "Reasonable efforts made to eliminate need for removal"],
                controlling_statute="N.Y. Fam. Ct. Act § 1027 & § 1028"
            ),
            CPSStage.FACT_FINDING_ADJUDICATION: CPSStageRequirements(
                stage=CPSStage.FACT_FINDING_ADJUDICATION,
                state="NY",
                right_to_counsel_appointed=True,
                standard_of_proof="Preponderance of the evidence",
                mandatory_findings=["Child is abused or neglected as defined in § 1012"],
                controlling_statute="N.Y. Fam. Ct. Act § 1046"
            )
        }
    }

    @classmethod
    def get_stage_requirements(cls, state: str, stage: CPSStage) -> Optional[CPSStageRequirements]:
        state_code = state.upper()
        return cls.STAGE_RULES.get(state_code, {}).get(stage)
