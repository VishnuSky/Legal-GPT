"""Multi-criteria search engine for verified public legal resources with strict jurisdiction isolation."""

from typing import List, Optional
from legal_registry.resources.resource_schema import (
    PublicLegalResource,
    OrganizationType,
    ResourceState,
)
from legal_registry.resources.resource_registry import ResourceRegistry
from legal_registry.resources.resource_verifier import ResourceVerifier


class ResourceSearchEngine:
    """Executes multi-criteria search and retrieval over public legal resources."""

    @classmethod
    def search(
        cls,
        jurisdiction: Optional[str] = None,
        county: Optional[str] = None,
        organization_types: Optional[List[OrganizationType]] = None,
        query: Optional[str] = None,
        languages: Optional[List[str]] = None,
        allow_stale: bool = True,
        include_unverified: bool = False,
        include_closed: bool = False,
        include_unavailable: bool = False
    ) -> List[PublicLegalResource]:
        """Searches resources with strict jurisdiction isolation and anti-hallucination filtering.
        
        CRITICAL RULE:
        By default, UNVERIFIED and CLOSED resources are strictly suppressed from public search results.
        """
        all_resources = ResourceRegistry.get_all()
        candidates: List[PublicLegalResource] = []

        norm_jurisdiction: Optional[str] = None
        if jurisdiction:
            j_clean = jurisdiction.strip().upper()
            if j_clean == "US":
                norm_jurisdiction = "US"
            elif not j_clean.startswith("US-"):
                norm_jurisdiction = f"US-{j_clean}"
            else:
                norm_jurisdiction = j_clean

        norm_county = county.strip().title() if county else None

        for res in all_resources:
            # 1. State / Freshness Filtering
            if res.state == ResourceState.CLOSED and not include_closed:
                continue
            if res.state == ResourceState.TEMPORARILY_UNAVAILABLE and not include_unavailable:
                continue
            if res.state == ResourceState.UNVERIFIED and not include_unverified:
                continue
            if res.state == ResourceState.STALE and not allow_stale:
                continue

            # 2. Strict Jurisdiction Isolation
            if norm_jurisdiction:
                # Allowed: exactly matching state or federal/national "US"
                if res.jurisdiction != "US" and res.jurisdiction != norm_jurisdiction:
                    continue

            # 3. County / Service Area Filtering
            if norm_county and res.jurisdiction != "US":
                # Check if resource is Statewide or explicitly covers the county
                county_match = False
                for area in res.service_area:
                    area_clean = area.lower()
                    if "statewide" in area_clean or "all" in area_clean:
                        county_match = True
                        break
                    if norm_county.lower() in area_clean:
                        county_match = True
                        break
                if not county_match:
                    continue

            # 4. Organization Type Filtering
            if organization_types:
                if res.organization_type not in organization_types:
                    continue

            # 5. Language Requirement
            if languages:
                res_langs = [l.lower() for l in res.languages]
                has_lang = any(req.lower() in res_langs for req in languages)
                if not has_lang and "interpretation available" not in " ".join(res_langs):
                    continue

            # 6. Text Query Matching
            if query:
                q_terms = query.lower().split()
                searchable_corpus = (
                    f"{res.name} {res.organization_type.value} {' '.join(res.services)} "
                    f"{res.eligibility} {' '.join(res.service_area)}"
                ).lower()
                if not any(term in searchable_corpus for term in q_terms):
                    continue

            candidates.append(res)

        return candidates
