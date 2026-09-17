"""Verified Public Legal Resource Router Subsystem.

Provides zero-invention discovery, verification, search, and ranking across
18 canonical organization types of public legal aid, court self-help, and social advocacy.
"""

from legal_registry.resources.resource_schema import (
    OrganizationType,
    ResourceState,
    VerificationMethod,
    PublicLegalResource,
)
from legal_registry.resources.resource_verifier import ResourceVerifier
from legal_registry.resources.resource_registry import (
    SEED_RESOURCES,
    ResourceRegistry,
)
from legal_registry.resources.resource_search import ResourceSearchEngine
from legal_registry.resources.resource_ranker import ResourceRanker

__all__ = [
    "OrganizationType",
    "ResourceState",
    "VerificationMethod",
    "PublicLegalResource",
    "ResourceVerifier",
    "SEED_RESOURCES",
    "ResourceRegistry",
    "ResourceSearchEngine",
    "ResourceRanker",
]
