"""Public-Data-Safe Legal Evidence Bridge Subsystem.

Connects evidence metadata to legal elements, governing authority,
missing proof analysis, and research questions without storing private case files.
"""

from core.evidence.models import (
    EpistemicClassification,
    EvidenceVerificationState,
    EvidenceRecord,
    LegalElement,
    LegalBridgeLink,
    EvidenceBridgeEvaluation,
)
from core.evidence.registry import (
    CANONICAL_LEGAL_ELEMENTS,
    LegalElementRegistry,
)
from core.evidence.bridge import LegalEvidenceBridge

__all__ = [
    "EpistemicClassification",
    "EvidenceVerificationState",
    "EvidenceRecord",
    "LegalElement",
    "LegalBridgeLink",
    "EvidenceBridgeEvaluation",
    "CANONICAL_LEGAL_ELEMENTS",
    "LegalElementRegistry",
    "LegalEvidenceBridge",
]
