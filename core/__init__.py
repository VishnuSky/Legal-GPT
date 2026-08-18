from core.authority import AuthorityEngine, TIER_WEIGHTS
from core.jurisdiction import JurisdictionEngine, JurisdictionContext
from core.temporal import TemporalEngine, TemporalValidityResult
from core.citation_verifier import CitationVerifier, CitationVerificationRecord
from core.hallucination_detector import HallucinationDetector, LegalPropositionCheck

__all__ = [
    "AuthorityEngine",
    "TIER_WEIGHTS",
    "JurisdictionEngine",
    "JurisdictionContext",
    "TemporalEngine",
    "TemporalValidityResult",
    "CitationVerifier",
    "CitationVerificationRecord",
    "HallucinationDetector",
    "LegalPropositionCheck",
]
