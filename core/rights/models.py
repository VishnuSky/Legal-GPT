import datetime
from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class LegalBasis(str, Enum):
    CONSTITUTIONAL = "CONSTITUTIONAL"
    STATUTORY = "STATUTORY"
    PROCEDURAL = "PROCEDURAL"
    ADMINISTRATIVE = "ADMINISTRATIVE"
    COMMON_LAW = "COMMON_LAW"


class RightCategory(str, Enum):
    CONSTITUTIONAL_RIGHTS = "constitutional_rights"
    STATUTORY_RIGHTS = "statutory_rights"
    PROCEDURAL_RIGHTS = "procedural_rights"
    ADMINISTRATIVE_RIGHTS = "administrative_rights"
    PARENTAL_RIGHTS = "parental_rights"
    CHILD_RIGHTS = "child_rights"
    CIVIL_RIGHTS = "civil_rights"
    DISABILITY_RIGHTS = "disability_rights"
    PRIVACY_RIGHTS = "privacy_rights"
    PROPERTY_INTERESTS = "property_interests"
    LIBERTY_INTERESTS = "liberty_interests"
    DUE_PROCESS_PROTECTIONS = "due_process_protections"
    EQUAL_PROTECTION_CONCERNS = "equal_protection_concerns"
    FAMILY_ASSOCIATION_INTERESTS = "family_association_interests"
    RELIGIOUS_RIGHTS = "religious_rights"
    SEARCH_SEIZURE_PROTECTIONS = "search_seizure_protections"
    COUNSEL_RIGHTS = "counsel_rights"
    NOTICE_RIGHTS = "notice_rights"
    HEARING_RIGHTS = "hearing_rights"
    APPEAL_RIGHTS = "appeal_rights"


class RightVerificationStatus(str, Enum):
    RECOGNIZED_POTENTIALLY_IMPLICATED = "RECOGNIZED_POTENTIALLY_IMPLICATED"
    RECOGNIZED_FACTS_INSUFFICIENT = "RECOGNIZED_FACTS_INSUFFICIENT"
    NOT_APPLICABLE_JURISDICTION_MISMATCH = "NOT_APPLICABLE_JURISDICTION_MISMATCH"
    NOT_APPLICABLE_TEMPORAL_INVALID = "NOT_APPLICABLE_TEMPORAL_INVALID"
    POTENTIALLY_BARRED_EXCEPTION_APPLIES = "POTENTIALLY_BARRED_EXCEPTION_APPLIES"
    POTENTIALLY_CONFLICTING_AUTHORITY = "POTENTIALLY_CONFLICTING_AUTHORITY"


class RightDefinition(BaseModel):
    """Canonical definition of a recognized legal right in the law."""
    right_id: str
    right_name: str
    category: RightCategory
    legal_basis: LegalBasis
    authority_tier: str = "TIER_0"
    authority: str
    citation: str
    jurisdiction: str = "US"  # "US" or state code e.g. "US-WA", "US-IL"
    effective_date_start: Optional[date] = None
    effective_date_end: Optional[date] = None
    procedural_context: List[str] = Field(default_factory=list)
    required_facts: List[str] = Field(default_factory=list)
    known_exceptions: List[str] = Field(default_factory=list)
    counterarguments: List[str] = Field(default_factory=list)
    core_holding: str = ""
    conflicting_procedures: List[str] = Field(default_factory=list)


class PotentialRightEvaluation(BaseModel):
    """Evaluation of a potentially relevant right against user context.
    
    CRITICAL PRINCIPLE:
    This model explicitly documents that the engine evaluates potential relevance
    under recognized law, and NEVER concludes that a violation has occurred.
    """
    right_name: str
    category: RightCategory
    legal_basis: LegalBasis
    authority: str
    authority_tier: str
    jurisdiction: str
    effective_date: str
    procedural_context: str
    required_facts: List[str] = Field(default_factory=list)
    known_exceptions: List[str] = Field(default_factory=list)
    counterarguments: List[str] = Field(default_factory=list)
    verification_status: RightVerificationStatus
    epistemic_distinction: str
    facts_implicated: List[str] = Field(default_factory=list)
    exceptions_triggered: List[str] = Field(default_factory=list)
    applicability_rationale: str


class RightsDiscoveryInput(BaseModel):
    """Input payload for the Rights Discovery Engine."""
    facts: List[str] = Field(default_factory=list)
    jurisdiction: str = "US"
    date: Optional[datetime.date] = Field(default=None)
    procedure: str = "INVESTIGATION"
    user_allegations: Optional[List[str]] = Field(default_factory=list)
    asserted_rights: Optional[List[str]] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class RightsDiscoveryResult(BaseModel):
    """Comprehensive output of the Rights Discovery Engine."""
    input_context: RightsDiscoveryInput
    potentially_relevant_rights: List[PotentialRightEvaluation] = Field(default_factory=list)
    inapplicable_or_excluded_rights: List[PotentialRightEvaluation] = Field(default_factory=list)
    constitutional_statutory_conflicts: List[Dict[str, Any]] = Field(default_factory=list)
    epistemic_warning: str = (
        "NON-ADJUDICATIVE NOTICE: The Legal-GPT Rights Discovery Engine identifies potentially relevant rights "
        "recognized under governing constitutions, statutes, and judicial precedents. This system distinguishes "
        "between 'the law recognizes this right' and 'the supplied facts establish that the right was violated.' "
        "Determining whether a legal violation occurred requires formal judicial findings, evidentiary cross-examination, "
        "and resolving affirmative defenses or statutory exceptions. Legal-GPT does not declare legal violations."
    )
    summary_counts: Dict[str, int] = Field(default_factory=dict)
