"""Specialized Pydantic schemas for CPS / Child Welfare legal sources and policy manuals."""

from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from legal_registry.schemas.registry_entry import LegalSourceEntry


class CPSTopicCoverage(BaseModel):
    intake_screening: bool = False
    investigation_assessment: bool = False
    safety_planning: bool = False
    emergency_removal: bool = False
    shelter_care_hearing: bool = False
    dependency_petition: bool = False
    fact_finding_adjudication: bool = False
    disposition_placement: bool = False
    visitation_family_time: bool = False
    case_planning_services: bool = False
    reasonable_efforts: bool = False
    permanency_planning: bool = False
    termination_parental_rights: bool = False
    guardianship_adoption: bool = False
    parent_rights_counsel: bool = False
    records_discovery: bool = False
    icwa_tribal_welfare: bool = False
    uccjea_interstate: bool = False
    icpc_interstate_placement: bool = False


class CPSSourceEntry(LegalSourceEntry):
    cps_subdomain: Literal[
        "federal_statute",
        "federal_regulation",
        "federal_guidance",
        "state_statute",
        "state_administrative_code",
        "state_agency_policy",
        "state_agency_manual",
        "court_rule",
        "court_form",
        "appellate_precedent",
        "tribal_code",
        "interstate_compact",
        "practice_advisory"
    ] = "state_statute"
    topics: CPSTopicCoverage = Field(default_factory=CPSTopicCoverage)
    key_statutory_sections: List[str] = Field(default_factory=list, description="Specific sections e.g. ['RCW 13.34.050', 'RCW 13.34.065']")
    standard_of_proof: Optional[str] = Field(None, description="Preponderance, Clear and Convincing, Beyond Reasonable Doubt")
    mandatory_timeframes_days: Dict[str, int] = Field(default_factory=dict, description="e.g. {'shelter_care_hearing': 3, 'fact_finding': 75}")
    icwa_specific: bool = False
