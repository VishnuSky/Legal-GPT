"""Contribution Validator: Schema integrity, PII scan, license compliance, and domain verification."""

import re
from typing import List, Tuple
from core.contributions.models import (
    CommunityContribution,
    ContributionState,
    ContributionType,
)


class ContributionValidator:
    """Validates community contributions before entry into the quarantine workflow."""

    ALLOWED_LICENSES = {
        "CC0-1.0",
        "CC0",
        "Public Domain",
        "Apache-2.0",
        "MIT",
        "ODbL-1.0"
    }

    OFFICIAL_DOMAINS = [
        ".gov",
        ".courts.gov",
        "govinfo.gov",
        "supremecourt.gov",
        "congress.gov",
        "courtlistener.com",
        "leg.wa.gov",
        "ilga.gov",
        "codes.ohio.gov",
        "statutes.capitol.texas.gov",
        "nysenate.gov",
        "flsenate.gov",
        "leginfo.legislature.ca.gov"
    ]

    DISALLOWED_PATTERNS = [
        r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
        r"reddit\.com",
        r"quora\.com",
        r"facebook\.com",
        r"chatgpt",
        r"claude\.ai",
        r"confidential case file",
        r"sealed record",
        r"under seal",
        r"/private_case_vault/",
        r"/confidential_evidence/"
    ]

    @classmethod
    def validate(cls, contribution: CommunityContribution) -> Tuple[bool, List[str]]:
        """Performs rigorous validation across all 9 mandatory fields and safety rules."""
        issues = []

        # 1. Source check
        if not contribution.source or len(contribution.source.strip()) < 3:
            issues.append("Mandatory field 'source' must be at least 3 characters.")

        # 2. Submitter check
        if not contribution.submitter or len(contribution.submitter.strip()) < 2:
            issues.append("Mandatory field 'submitter' must identify contributor.")

        # 3. Date check
        if not contribution.date:
            issues.append("Mandatory field 'date' must be specified.")

        # 4. Jurisdiction check
        if not contribution.jurisdiction:
            issues.append("Mandatory field 'jurisdiction' must be provided.")

        # 5. Authority type check
        if not contribution.authority_type:
            issues.append("Mandatory field 'authority_type' must be specified.")

        # 6. Provenance check
        if not contribution.provenance:
            issues.append("Mandatory field 'provenance' is required.")
        else:
            if not contribution.provenance.origin_url:
                issues.append("Provenance must contain a valid 'origin_url'.")
            if not contribution.provenance.publisher:
                issues.append("Provenance must identify the official 'publisher'.")
            if not contribution.provenance.verification_method:
                issues.append("Provenance must describe the 'verification_method'.")

        # 7. License check
        if contribution.license not in cls.ALLOWED_LICENSES:
            issues.append(
                f"License '{contribution.license}' is not permitted. Must be one of: {', '.join(cls.ALLOWED_LICENSES)}"
            )

        # 8. Initial state rule: new community submissions must start in PROPOSED
        if contribution.verification_state != ContributionState.PROPOSED:
            issues.append(
                f"Initial submission state must be 'PROPOSED', not '{contribution.verification_state.value}'."
            )

        # 9. Deep PII and Disallowed content scan
        text_to_scan = f"{contribution.source} {contribution.submitter} {contribution.provenance.origin_url} {str(contribution.payload)}"
        for pat in cls.DISALLOWED_PATTERNS:
            if re.search(pat, text_to_scan, re.IGNORECASE):
                issues.append(f"Security/Privacy violation: Content matches prohibited pattern '{pat}'.")

        # 10. For primary legal sources, verify official domain
        if contribution.contribution_type in (
            ContributionType.STATUTE,
            ContributionType.REGULATION,
            ContributionType.CASE,
            ContributionType.COURT_RULE
        ):
            origin_lower = contribution.provenance.origin_url.lower()
            is_official = any(dom in origin_lower for dom in cls.OFFICIAL_DOMAINS)
            if not is_official:
                issues.append(
                    f"Primary legal source '{contribution.contribution_type.value}' must originate from an official government or court repository (.gov, .courts.gov, etc.)."
                )

        return (len(issues) == 0, issues)
