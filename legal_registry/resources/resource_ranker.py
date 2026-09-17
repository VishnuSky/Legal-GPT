"""Ranking and relevance scoring engine for public legal resources."""

from typing import List, Optional
from legal_registry.resources.resource_schema import (
    PublicLegalResource,
    OrganizationType,
    ResourceState,
)


class ResourceRanker:
    """Ranks discovered public legal resources based on geographic proximity, verification tier, and eligibility alignment."""

    @classmethod
    def score_resource(
        cls,
        resource: PublicLegalResource,
        target_county: Optional[str] = None,
        preferred_types: Optional[List[OrganizationType]] = None,
        is_low_income: bool = True,
        preferred_languages: Optional[List[str]] = None
    ) -> float:
        """Calculates numerical score for a candidate resource."""
        score = 0.0

        # 1. Geographic Proximity Tier
        norm_county = target_county.strip().lower() if target_county else None
        if norm_county:
            # Check for direct county coverage
            direct_county_hit = any(norm_county in area.lower() for area in resource.service_area)
            if direct_county_hit:
                score += 100.0
            elif any("statewide" in area.lower() for area in resource.service_area):
                score += 50.0
            elif resource.jurisdiction == "US":
                score += 20.0
        else:
            if any("statewide" in area.lower() for area in resource.service_area):
                score += 50.0
            elif resource.jurisdiction == "US":
                score += 20.0

        # 2. Preferred Organization Type
        if preferred_types and resource.organization_type in preferred_types:
            score += 40.0

        # 3. Verification State Tier
        if resource.state == ResourceState.VERIFIED:
            score += 30.0
        elif resource.state == ResourceState.STALE:
            score -= 10.0
        elif resource.state == ResourceState.UNVERIFIED:
            score -= 50.0
        elif resource.state in (ResourceState.CLOSED, ResourceState.TEMPORARILY_UNAVAILABLE):
            score -= 100.0

        # 4. Low-Income / Indigency Alignment
        if is_low_income:
            if resource.organization_type in (
                OrganizationType.LEGAL_AID,
                OrganizationType.PUBLIC_DEFENDER,
                OrganizationType.COURT_SELF_HELP,
                OrganizationType.OMBUDS
            ):
                score += 35.0
            if "none" in (resource.income_requirements or "").lower() or "free" in (resource.eligibility or "").lower():
                score += 15.0

        # 5. Language Alignment
        if preferred_languages:
            res_langs = [l.lower() for l in resource.languages]
            for plang in preferred_languages:
                if plang.lower() in res_langs:
                    score += 15.0
                    break

        # 6. Complete Direct Contact Information Bonus
        if resource.phone and resource.website:
            score += 10.0

        return score

    @classmethod
    def rank_resources(
        cls,
        resources: List[PublicLegalResource],
        target_county: Optional[str] = None,
        preferred_types: Optional[List[OrganizationType]] = None,
        is_low_income: bool = True,
        preferred_languages: Optional[List[str]] = None
    ) -> List[PublicLegalResource]:
        """Ranks a list of candidate resources in descending order of relevance score."""
        scored = [
            (
                r,
                cls.score_resource(
                    resource=r,
                    target_county=target_county,
                    preferred_types=preferred_types,
                    is_low_income=is_low_income,
                    preferred_languages=preferred_languages
                )
            )
            for r in resources
        ]
        # Sort descending by score
        scored.sort(key=lambda item: item[1], reverse=True)
        return [item[0] for item in scored]
