"""Verified Public Resource and Legal Aid Discovery for Public Legal Navigator."""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from services.registry import default_service_registry
from services.models import CivilMatterType, ServiceType, PublicServiceRecord
from legal_registry.loader import default_registry


class VerifiedResourceCategory(str, Enum):
    LEGAL_AID = "LEGAL_AID"                          # LSC-funded civil legal aid programs
    GOVERNMENT_OMBUDSMAN = "GOVERNMENT_OMBUDSMAN"    # Official family advocacy ombudsman offices
    COURT_SELF_HELP = "COURT_SELF_HELP"              # Courthouse facilitators & pro se desks
    BAR_REFERRAL = "BAR_REFERRAL"                    # State and County bar pro bono referral
    TRIBAL_LIAISON = "TRIBAL_LIAISON"                # Designated tribal ICWA contacts
    ADVOCACY_ORG = "ADVOCACY_ORG"                    # Verified non-profit legal coalitions


class DiscoveredResource(BaseModel):
    resource_id: str
    name: str
    category: VerifiedResourceCategory
    jurisdiction_state: str
    county: Optional[str] = None
    phone: Optional[str] = None
    website: str
    intake_url: Optional[str] = None
    address: Optional[str] = None
    eligibility_summary: str
    is_official: bool = True


class ResourceDiscoveryResult(BaseModel):
    jurisdiction: str
    matter: str
    legal_aid_services: List[DiscoveredResource] = Field(default_factory=list)
    government_agencies: List[DiscoveredResource] = Field(default_factory=list)
    court_resources: List[DiscoveredResource] = Field(default_factory=list)
    advocacy_organizations: List[DiscoveredResource] = Field(default_factory=list)
    self_help_centers: List[DiscoveredResource] = Field(default_factory=list)
    total_found: int = 0


class ResourceDiscovery:
    """Discovers verified civil legal aid, ombudsman, and court resources. Never fabricates entries."""

    MATTER_MAP = {
        "CPS_CHILD_WELFARE": CivilMatterType.FAMILY_CPS,
        "FAMILY_LAW": CivilMatterType.FAMILY_CPS,
        "HOUSING_TENANT": CivilMatterType.HOUSING,
        "CONSUMER_DEBT": CivilMatterType.CONSUMER_DEBT,
        "EMPLOYMENT": CivilMatterType.EMPLOYMENT,
        "DISABILITY_RIGHTS": CivilMatterType.DISABILITY,
        "ADMINISTRATIVE": CivilMatterType.BENEFITS,
        "EDUCATION": CivilMatterType.EDUCATION
    }

    @classmethod
    def discover_resources(
        cls,
        state: Optional[str] = None,
        county: Optional[str] = None,
        domain_name: str = "CPS_CHILD_WELFARE"
    ) -> ResourceDiscoveryResult:
        """Queries the verified ServiceRegistry and registered courts. Only returns genuine verified entries."""
        target_state = state.upper() if state else None
        target_matter = cls.MATTER_MAP.get(domain_name, CivilMatterType.FAMILY_CPS)

        # Query services registry
        raw_services = default_service_registry.query_services(
            state=target_state,
            county=county,
            matter=target_matter
        )

        # Fallback to general statewide/national if no exact county match
        if not raw_services and county:
            raw_services = default_service_registry.query_services(
                state=target_state,
                county=None,
                matter=target_matter
            )

        # If still empty for this specific matter, query all matters in state
        if not raw_services and target_state:
            raw_services = default_service_registry.query_services(
                state=target_state,
                county=None
            )

        legal_aid: List[DiscoveredResource] = []
        gov_agencies: List[DiscoveredResource] = []
        court_res: List[DiscoveredResource] = []
        advocacy: List[DiscoveredResource] = []
        self_help: List[DiscoveredResource] = []

        for rec in raw_services:
            res_item = DiscoveredResource(
                resource_id=rec.service_id,
                name=rec.name,
                category=cls._map_service_type(rec.service_type),
                jurisdiction_state=rec.jurisdiction.state,
                county=rec.jurisdiction.county,
                phone=rec.contact.phone,
                website=rec.contact.website,
                intake_url=rec.contact.intake_url or rec.contact.website,
                address=rec.contact.address,
                eligibility_summary=rec.eligibility_summary,
                is_official=rec.is_official
            )

            if rec.service_type == ServiceType.LEGAL_AID:
                legal_aid.append(res_item)
            elif rec.service_type in (ServiceType.PUBLIC_CONTACT, ServiceType.AG_CONSUMER):
                gov_agencies.append(res_item)
            elif rec.service_type == ServiceType.COURT_SELF_HELP:
                court_res.append(res_item)
                self_help.append(res_item)
            elif rec.service_type == ServiceType.BAR_REFERRAL:
                advocacy.append(res_item)
            elif rec.service_type == ServiceType.TRIBAL_ICWA:
                gov_agencies.append(res_item)

        # Supplement with registered courts from legal_registry
        if target_state:
            matching_courts = default_registry.get_courts_for_jurisdiction(target_state, county)
            for c in matching_courts[:3]:
                court_res.append(DiscoveredResource(
                    resource_id=c.court_id,
                    name=c.name,
                    category=VerifiedResourceCategory.COURT_SELF_HELP,
                    jurisdiction_state=c.state or c.jurisdiction,
                    county=c.county,
                    phone=c.metadata.get("phone") if hasattr(c, "metadata") and isinstance(c.metadata, dict) else None,
                    website=c.official_url,
                    intake_url=c.forms_url or c.official_url,
                    address=c.metadata.get("address") if hasattr(c, "metadata") and isinstance(c.metadata, dict) else None,
                    eligibility_summary="Official courthouse clerk and self-help / forms desk.",
                    is_official=True
                ))

        total = len(legal_aid) + len(gov_agencies) + len(court_res) + len(advocacy)

        return ResourceDiscoveryResult(
            jurisdiction=target_state or "US",
            matter=target_matter.value,
            legal_aid_services=legal_aid,
            government_agencies=gov_agencies,
            court_resources=court_res,
            advocacy_organizations=advocacy,
            self_help_centers=self_help,
            total_found=total
        )

    @staticmethod
    def _map_service_type(st: ServiceType) -> VerifiedResourceCategory:
        if st == ServiceType.LEGAL_AID:
            return VerifiedResourceCategory.LEGAL_AID
        elif st in (ServiceType.PUBLIC_CONTACT, ServiceType.AG_CONSUMER):
            return VerifiedResourceCategory.GOVERNMENT_OMBUDSMAN
        elif st == ServiceType.COURT_SELF_HELP:
            return VerifiedResourceCategory.COURT_SELF_HELP
        elif st == ServiceType.BAR_REFERRAL:
            return VerifiedResourceCategory.BAR_REFERRAL
        elif st == ServiceType.TRIBAL_ICWA:
            return VerifiedResourceCategory.TRIBAL_LIAISON
        return VerifiedResourceCategory.LEGAL_AID
