"""Legal Truth Objects and Structured Authority Packages for Two-Brain Architecture."""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
import hashlib
from datetime import datetime, timezone


@dataclass
class LegalTruthObject:
    claim: str
    citation: str
    source_url: str
    authority_type: str  # statute | regulation | case | constitution | policy
    authority_tier: int  # 0-13
    jurisdiction: str
    effective_from: str  # ISO date YYYY-MM-DD
    effective_to: Optional[str] = None
    verified: bool = True
    retrieved_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_hash: str = ""
    document_hash: str = ""
    conflict_status: str = "NONE"  # NONE | DETECTED | UNRESOLVED
    confidence: float = 1.0

    def compute_hashes(self, text_content: str):
        self.document_hash = hashlib.sha256(text_content.encode("utf-8")).hexdigest()
        self.source_hash = hashlib.sha256(f"{self.citation}:{self.source_url}:{self.jurisdiction}".encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LegalAuthorityPackage:
    """Structured container delivered by Brain 2 (Authority Engine) to Brain 1 (Model Reasoning)."""
    query: str
    jurisdiction: str
    authorities: List[LegalTruthObject] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    retrieved_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def format_for_model_prompt(self) -> str:
        """Formats the structured authority package for the model reasoning context."""
        lines = [
            "=== LEGAL AUTHORITY PACKAGE ===",
            f"JURISDICTION: {self.jurisdiction}",
            f"RETRIEVED AT: {self.retrieved_at}",
            f"CONFLICTS DETECTED: {len(self.conflicts)}",
            ""
        ]
        for idx, auth in enumerate(self.authorities, 1):
            lines.append(f"[{idx}] CLAIM: {auth.claim}")
            lines.append(f"    CITATION: {auth.citation}")
            lines.append(f"    AUTHORITY TIER: Tier {auth.authority_tier} ({auth.authority_type.upper()})")
            lines.append(f"    EFFECTIVE: {auth.effective_from} to {auth.effective_to or 'PRESENT'}")
            lines.append(f"    VERIFICATION: {'VERIFIED' if auth.verified else 'UNVERIFIED'}")
            lines.append(f"    CONFLICT STATUS: {auth.conflict_status}")
            lines.append(f"    SOURCE HASH: {auth.source_hash[:16]}...")
            lines.append("")
        lines.append("=== END AUTHORITY PACKAGE ===")
        return "\n".join(lines)
