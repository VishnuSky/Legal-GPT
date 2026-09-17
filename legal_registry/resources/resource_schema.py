"""Pydantic schemas and enums for the Verified Public Legal Resource Router."""

from datetime import date
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class OrganizationType(str, Enum):
    """The 18 canonical organization types recognized by Legal-GPT."""
    LEGAL_AID = "LEGAL_AID"
    COURT_SELF_HELP = "COURT_SELF_HELP"
    PUBLIC_DEFENDER = "PUBLIC_DEFENDER"
    BAR_REFERRAL = "BAR_REFERRAL"
    CIVIL_RIGHTS_ORGANIZATIONS = "CIVIL_RIGHTS_ORGANIZATIONS"
    CHILD_ADVOCACY = "CHILD_ADVOCACY"
    DOMESTIC_VIOLENCE_SERVICES = "DOMESTIC_VIOLENCE_SERVICES"
    DISABILITY_SERVICES = "DISABILITY_SERVICES"
    MENTAL_HEALTH_SERVICES = "MENTAL_HEALTH_SERVICES"
    SUBSTANCE_USE_SERVICES = "SUBSTANCE_USE_SERVICES"
    HOUSING_SERVICES = "HOUSING_SERVICES"
    EDUCATION_ADVOCACY = "EDUCATION_ADVOCACY"
    VETERANS_SERVICES = "VETERANS_SERVICES"
    TRIBAL_SERVICES = "TRIBAL_SERVICES"
    IMMIGRATION_SERVICES = "IMMIGRATION_SERVICES"
    MEDIATION = "MEDIATION"
    OMBUDS = "OMBUDS"
    GOVERNMENT_AGENCIES = "GOVERNMENT_AGENCIES"


class ResourceState(str, Enum):
    """Lifecycle verification states for public legal resources."""
    VERIFIED = "VERIFIED"
    STALE = "STALE"
    UNVERIFIED = "UNVERIFIED"
    CLOSED = "CLOSED"
    TEMPORARILY_UNAVAILABLE = "TEMPORARILY_UNAVAILABLE"


class VerificationMethod(str, Enum):
    """Method utilized to verify resource legitimacy and operating status."""
    PRIMARY_SOURCE_SCRAPE = "PRIMARY_SOURCE_SCRAPE"
    OFFICIAL_GOVERNMENT_DIRECTORY = "OFFICIAL_GOVERNMENT_DIRECTORY"
    BAR_ASSOCIATION_ROSTER = "BAR_ASSOCIATION_ROSTER"
    LSC_GRANTEE_DATABASE = "LSC_GRANTEE_DATABASE"
    MANUAL_STAFF_AUDIT = "MANUAL_STAFF_AUDIT"
    AUTOMATED_HEALTH_CHECK = "AUTOMATED_HEALTH_CHECK"


class PublicLegalResource(BaseModel):
    """Canonical Public Legal Resource Record.
    
    CRITICAL ANTI-HALLUCINATION REQUIREMENT:
    Under no circumstances may an organization, phone number, website,
    eligibility requirement, office, or service be invented.
    If a resource cannot be verified against official primary sources,
    it must be marked as UNVERIFIED.
    """
    resource_id: str
    name: str
    organization_type: OrganizationType
    jurisdiction: str  # e.g. "US-WA", "US-IL", "US"
    service_area: List[str] = Field(default_factory=list)  # e.g. ["Skagit County", "Statewide"]
    eligibility: str
    services: List[str] = Field(default_factory=list)
    website: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    hours: Optional[str] = None
    languages: List[str] = Field(default_factory=lambda: ["English"])
    income_requirements: Optional[str] = None
    verification_source: str
    last_verified: date
    verification_method: VerificationMethod
    state: ResourceState = ResourceState.VERIFIED
    verification_notes: Optional[str] = None
