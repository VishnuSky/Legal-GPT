"""Service Registry Loader & Query Engine for Official Civil Legal Aid and Public Support Directories."""

import os
import yaml
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any, Union

from services.models import (
    PublicServiceRecord,
    CivilMatterType,
    ServiceType,
    ServiceJurisdiction,
    ServiceContact
)

logger = logging.getLogger("legal_gpt.services")


class ServiceRegistry:
    """Manages and queries official civil legal aid and public institutional service records."""

    def __init__(self, seeds_dir: Optional[str] = None):
        self.seeds_dir = Path(seeds_dir) if seeds_dir else Path(__file__).parent / "seeds"
        self.services_by_id: Dict[str, PublicServiceRecord] = {}
        self.load_all_seeds()

    def load_all_seeds(self):
        """Loads all YAML seed files in the seeds directory."""
        if not self.seeds_dir.exists():
            logger.warning(f"Services seeds directory not found: {self.seeds_dir}")
            return

        loaded_count = 0
        for yaml_file in self.seeds_dir.glob("*.yaml"):
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    items = data.get("services") or data.get("records") or []
                    if not items:
                        continue

                    for item in items:
                        matters = [CivilMatterType(m) for m in item.get("matters", []) if m in CivilMatterType.__members__]
                        s_type = ServiceType(item["service_type"])
                        juris_data = item.get("jurisdiction", {})
                        raw_state = juris_data.get("state", "US")
                        if raw_state and not raw_state.startswith("US-") and raw_state != "US":
                            norm_state = f"US-{raw_state.upper()}"
                        else:
                            norm_state = raw_state or "US"
                        juris = ServiceJurisdiction(
                            country=juris_data.get("country", "US"),
                            state=norm_state,
                            county=juris_data.get("county"),
                            tribe=juris_data.get("tribe")
                        )
                        contact_data = item.get("contact", {})
                        contact = ServiceContact(
                            phone=contact_data.get("phone"),
                            website=contact_data.get("website", ""),
                            address=contact_data.get("address"),
                            intake_url=contact_data.get("intake_url"),
                            email=contact_data.get("email"),
                            hours=contact_data.get("hours")
                        )

                        rec = PublicServiceRecord(
                            service_id=item["service_id"],
                            name=item["name"],
                            jurisdiction=juris,
                            matters=matters,
                            service_type=s_type,
                            description=item.get("description", ""),
                            contact=contact,
                            eligibility_summary=item.get("eligibility_summary", ""),
                            source_url=item.get("source_url", ""),
                            is_official=item.get("is_official", True)
                        )
                        rec.compute_hash()
                        self.services_by_id[rec.service_id] = rec
                        loaded_count += 1
            except Exception as e:
                logger.error(f"Error loading service seed file {yaml_file}: {e}")

        logger.info(f"ServiceRegistry: Loaded {loaded_count} official public service records.")

    def query_services(
        self,
        state: Optional[str] = None,
        county: Optional[str] = None,
        tribe: Optional[str] = None,
        matter: Optional[Union[CivilMatterType, str]] = None,
        service_type: Optional[Union[ServiceType, str]] = None
    ) -> List[PublicServiceRecord]:
        """Queries services matching jurisdiction, matter, and service type filters."""
        results: List[PublicServiceRecord] = []
        
        # Normalize state string (e.g. "WA" -> "US-WA")
        norm_state = None
        if state:
            s_clean = state.strip().upper()
            norm_state = f"US-{s_clean}" if not s_clean.startswith("US-") and s_clean != "US" else s_clean

        norm_matter = None
        if matter:
            if isinstance(matter, CivilMatterType):
                norm_matter = matter
            else:
                m_upper = str(matter).strip().upper()
                # support human friendly mappings
                if "CPS" in m_upper or "FAMILY" in m_upper or "CHILD" in m_upper:
                    norm_matter = CivilMatterType.FAMILY_CPS
                elif "HOUSE" in m_upper or "RENT" in m_upper or "EVICT" in m_upper:
                    norm_matter = CivilMatterType.HOUSING
                elif "DEBT" in m_upper or "CONSUMER" in m_upper or "BANKRUPT" in m_upper:
                    norm_matter = CivilMatterType.CONSUMER_DEBT
                elif "JOB" in m_upper or "EMPLOY" in m_upper or "WAGE" in m_upper:
                    norm_matter = CivilMatterType.EMPLOYMENT
                elif "BENEFIT" in m_upper or "SNAP" in m_upper or "MEDICAID" in m_upper or "SSI" in m_upper:
                    norm_matter = CivilMatterType.BENEFITS
                elif "DISAB" in m_upper or "ADA" in m_upper:
                    norm_matter = CivilMatterType.DISABILITY
                elif "EDUCAT" in m_upper or "SCHOOL" in m_upper:
                    norm_matter = CivilMatterType.EDUCATION
                elif "IMMIGRAT" in m_upper:
                    norm_matter = CivilMatterType.IMMIGRATION
                elif "SMALL" in m_upper or "CLAIM" in m_upper:
                    norm_matter = CivilMatterType.SMALL_CLAIMS
                elif "RECORD" in m_upper or "FOIA" in m_upper:
                    norm_matter = CivilMatterType.PUBLIC_RECORDS
                elif m_upper in CivilMatterType.__members__:
                    norm_matter = CivilMatterType(m_upper)

        norm_type = None
        if service_type:
            if isinstance(service_type, ServiceType):
                norm_type = service_type
            else:
                t_upper = str(service_type).strip().upper()
                if t_upper in ServiceType.__members__:
                    norm_type = ServiceType(t_upper)

        for rec in self.services_by_id.values():
            # Jurisdiction matching: match state (or federal US level)
            if norm_state:
                if rec.jurisdiction.state not in (norm_state, "US"):
                    continue

            # County matching: if county specified, match county or statewide (null county)
            if county:
                c_clean = county.strip().lower()
                if rec.jurisdiction.county and rec.jurisdiction.county.lower() != c_clean:
                    continue

            # Tribe matching
            if tribe:
                t_clean = tribe.strip().lower()
                if rec.jurisdiction.tribe and t_clean not in rec.jurisdiction.tribe.lower():
                    continue

            # Matter matching
            if norm_matter:
                if norm_matter not in rec.matters:
                    continue

            # Service type matching
            if norm_type:
                if rec.service_type != norm_type:
                    continue

            results.append(rec)

        # Sort: local county first, then state, then federal
        def sort_priority(r: PublicServiceRecord) -> int:
            if county and r.jurisdiction.county:
                return 0
            if norm_state and r.jurisdiction.state == norm_state:
                return 1
            return 2

        results.sort(key=sort_priority)
        return results

    def get_service_by_id(self, service_id: str) -> Optional[PublicServiceRecord]:
        return self.services_by_id.get(service_id)

    def list_all(self) -> List[PublicServiceRecord]:
        return list(self.services_by_id.values())


# Global singleton instance
default_service_registry = ServiceRegistry()
