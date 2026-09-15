"""Pydantic Schemas for Official Civil Legal Aid and Public Service Registry."""

from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import hashlib
from pydantic import BaseModel, Field


class CivilMatterType(str, Enum):
    FAMILY_CPS = "FAMILY_CPS"                # Family, CPS, Dependency, Custody, Domestic Violence
    HOUSING = "HOUSING"                      # Eviction, Tenant Rights, Foreclosure, Habitability
    CONSUMER_DEBT = "CONSUMER_DEBT"          # Debt Collection, Scams, Bankruptcy, Credit
    EMPLOYMENT = "EMPLOYMENT"                # Wage Theft, Wrongful Termination, Worker Rights
    BENEFITS = "BENEFITS"                    # SNAP, Medicaid, SSI/SSDI, TANF, Unemployment
    EDUCATION = "EDUCATION"                  # Special Ed, IEP, Suspensions, School Access
    DISABILITY = "DISABILITY"                # ADA Accommodations, Physical/Mental Disability Rights
    IMMIGRATION = "IMMIGRATION"              # Naturalization, Public Process, Asylum Info (Public only)
    SMALL_CLAIMS = "SMALL_CLAIMS"            # Monetary Disputes, Security Deposits, Contracts
    PUBLIC_RECORDS = "PUBLIC_RECORDS"        # FOIA, State Open Records, Agency Records


class ServiceType(str, Enum):
    LEGAL_AID = "LEGAL_AID"                  # LSC-funded or IOLTA Civil Legal Aid Program
    COURT_SELF_HELP = "COURT_SELF_HELP"      # Court Facilitator / Self-Help Helpdesk
    BAR_REFERRAL = "BAR_REFERRAL"            # State / County Bar Association Referral & Pro Bono
    AG_CONSUMER = "AG_CONSUMER"              # Attorney General Consumer Protection / Civil Rights
    TRIBAL_ICWA = "TRIBAL_ICWA"              # Tribal Court / ICWA Designated Public Liaison
    PUBLIC_CONTACT = "PUBLIC_CONTACT"        # Official Agency Ombudsman / Family Advocacy Office


class ServiceContact(BaseModel):
    phone: Optional[str] = None
    website: str
    address: Optional[str] = None
    intake_url: Optional[str] = None
    email: Optional[str] = None
    hours: Optional[str] = None


class ServiceJurisdiction(BaseModel):
    country: str = "US"
    state: str                               # e.g. "US-WA", "US-IL", "US-OH", "US"
    county: Optional[str] = None             # e.g. "Skagit", "Cook", "Cuyahoga", or None for statewide
    tribe: Optional[str] = None              # e.g. "Puyallup Tribe", "Navajo Nation"


class PublicServiceRecord(BaseModel):
    service_id: str                          # e.g. "WA-SERV-NJP-01"
    name: str
    jurisdiction: ServiceJurisdiction
    matters: List[CivilMatterType]
    service_type: ServiceType
    description: str
    contact: ServiceContact
    eligibility_summary: str
    source_url: str
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    content_sha256: str = ""
    is_official: bool = True

    def compute_hash(self) -> str:
        """Computes SHA-256 integrity hash of core service payload."""
        payload = f"{self.service_id}:{self.name}:{self.jurisdiction.state}:{self.source_url}:{self.service_type.value}"
        self.content_sha256 = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return self.content_sha256
