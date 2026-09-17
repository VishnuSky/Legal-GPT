"""Resource Verifier: Enforces strict grounding and zero-invention policies for public legal resources."""

from datetime import date
import re
from typing import Dict, List, Optional, Tuple, Any
from legal_registry.resources.resource_schema import PublicLegalResource, ResourceState, VerificationMethod


class ResourceVerifier:
    """Validates public legal resource records against anti-hallucination policies and freshness standards."""

    # Valid North American phone regex (E.164, 10-digit formats)
    PHONE_REGEX = re.compile(
        r"^(?:\+?1[-.\s]?)?(?:\(?([2-9][0-8][0-9])\)?[-.\s]?)?([2-9][0-9]{2})[-.\s]?([0-9]{4})(?:\s*(?:ext|x|ext.)\s*(\d+))?$"
    )
    
    # Obvious dummy / test prefixes (Fictitious 555 numbers, 000 area codes)
    INVALID_PHONE_PREFIXES = ["555-01", "000-", "123-456", "999-999"]

    # Maximum age in days before a verified resource is considered STALE
    MAX_VERIFIED_AGE_DAYS = 180

    @classmethod
    def verify(
        cls,
        resource: PublicLegalResource,
        reference_date: Optional[date] = None
    ) -> Tuple[ResourceState, List[str]]:
        """Evaluates a resource record against primary source rules and recency thresholds.
        
        Returns:
            Tuple[ResourceState, List[str]]: (Assigned state, List of verification reasons/flags)
        """
        ref_date = reference_date or date.today()
        flags: List[str] = []

        # If already manually flagged as closed, maintain closed status
        if resource.state == ResourceState.CLOSED:
            return ResourceState.CLOSED, ["Resource confirmed permanently closed."]

        # If temporarily unavailable (e.g. intake closed, waitlist frozen)
        if resource.state == ResourceState.TEMPORARILY_UNAVAILABLE:
            return ResourceState.TEMPORARILY_UNAVAILABLE, ["Resource currently not accepting new intakes/cases."]

        # 1. Verification Source Mandate
        if not resource.verification_source or len(resource.verification_source.strip()) < 5:
            flags.append("Missing or ungrounded verification_source: Cannot verify against primary authority.")
            return ResourceState.UNVERIFIED, flags

        source_lower = resource.verification_source.lower()
        if any(term in source_lower for term in ["placeholder", "unverified", "tbd", "unknown", "fake", "none"]):
            flags.append(f"Verification source '{resource.verification_source}' is invalid or ungrounded.")
            return ResourceState.UNVERIFIED, flags

        # 2. Website Validation
        if resource.website:
            if not (resource.website.startswith("http://") or resource.website.startswith("https://")):
                flags.append(f"Website '{resource.website}' lacks valid HTTP/HTTPS protocol.")
                return ResourceState.UNVERIFIED, flags
            if "example.com" in resource.website or "placeholder" in resource.website:
                flags.append(f"Website '{resource.website}' is an ungrounded placeholder domain.")
                return ResourceState.UNVERIFIED, flags

        # 3. Phone Number Grounding Check
        if resource.phone:
            clean_phone = resource.phone.strip()
            if any(dummy in clean_phone for dummy in cls.INVALID_PHONE_PREFIXES):
                flags.append(f"Phone number '{resource.phone}' matches fictitious or dummy number pattern.")
                return ResourceState.UNVERIFIED, flags
            if not cls.PHONE_REGEX.match(clean_phone):
                flags.append(f"Phone number '{resource.phone}' fails canonical North American telephone validation.")
                return ResourceState.UNVERIFIED, flags

        # 4. Mandatory Core Fields Check
        if not resource.name or len(resource.name.strip()) < 3:
            flags.append("Organization name is missing or too short.")
            return ResourceState.UNVERIFIED, flags

        if not resource.eligibility or len(resource.eligibility.strip()) < 3:
            flags.append("Eligibility guidelines are missing or ungrounded.")
            return ResourceState.UNVERIFIED, flags

        if not resource.services or len(resource.services) == 0:
            flags.append("Services list is empty: Resource specifies no concrete services.")
            return ResourceState.UNVERIFIED, flags

        # 5. Temporal Staleness Check (> 180 days)
        age_days = (ref_date - resource.last_verified).days
        if age_days > cls.MAX_VERIFIED_AGE_DAYS:
            flags.append(f"Resource verification is STALE ({age_days} days old > {cls.MAX_VERIFIED_AGE_DAYS} day limit).")
            return ResourceState.STALE, flags

        # All grounding checks passed
        flags.append(f"Resource verified against primary source: {resource.verification_source} via {resource.verification_method.value}.")
        return ResourceState.VERIFIED, flags

    @classmethod
    def audit_resource(
        cls,
        resource: PublicLegalResource,
        reference_date: Optional[date] = None
    ) -> PublicLegalResource:
        """Applies verification and returns an updated copy of the resource."""
        state, flags = cls.verify(resource, reference_date)
        updated = resource.model_copy(deep=True)
        updated.state = state
        updated.verification_notes = "; ".join(flags)
        return updated

    @classmethod
    def audit_collection(
        cls,
        resources: List[PublicLegalResource],
        reference_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Audits a collection of resources and returns summary statistics."""
        summary = {
            "total": len(resources),
            "VERIFIED": 0,
            "STALE": 0,
            "UNVERIFIED": 0,
            "CLOSED": 0,
            "TEMPORARILY_UNAVAILABLE": 0,
            "issues": []
        }
        for r in resources:
            state, flags = cls.verify(r, reference_date)
            summary[state.value] += 1
            if state in (ResourceState.UNVERIFIED, ResourceState.STALE):
                summary["issues"].append({
                    "resource_id": r.resource_id,
                    "name": r.name,
                    "state": state.value,
                    "reasons": flags
                })
        return summary
