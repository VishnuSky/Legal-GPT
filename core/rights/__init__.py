"""Legal-GPT Rights Discovery Subsystem.

Identifies potentially relevant legal rights and controlling authority across
20 constitutional, statutory, administrative, and procedural categories.
Explicitly distinguishes rights recognition from legal violation determination.
"""

from core.rights.models import (
    LegalBasis,
    RightCategory,
    RightDefinition,
    RightVerificationStatus,
    PotentialRightEvaluation,
    RightsDiscoveryInput,
    RightsDiscoveryResult,
)
from core.rights.registry import CANONICAL_RIGHTS, RightsRegistry
from core.rights.engine import RightsDiscoveryEngine

__all__ = [
    "LegalBasis",
    "RightCategory",
    "RightDefinition",
    "RightVerificationStatus",
    "PotentialRightEvaluation",
    "RightsDiscoveryInput",
    "RightsDiscoveryResult",
    "CANONICAL_RIGHTS",
    "RightsRegistry",
    "RightsDiscoveryEngine",
]
