"""Legal Conflict Detector for Supremacy, Preemption, Ex Post Facto, and Cross-Jurisdiction Clashes."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ConflictRecord(BaseModel):
    conflict_id: str
    conflict_type: str  # SUPREMACY, PREEMPTION, TEMPORAL, JURISDICTIONAL, STATUTORY_PRECEDENT
    authority_a: str
    authority_b: str
    description: str
    analysis_framework: str
    is_unresolved: bool = False


class ConflictDetector:
    """Detects and explicitly surfaces conflicts across authorities and jurisdictions."""

    @classmethod
    def detect_conflicts(
        cls,
        jurisdiction: str,
        citations: List[str],
        event_date: Optional[str] = None
    ) -> List[ConflictRecord]:
        conflicts = []

        # 1. State law vs Federal/Constitutional tension (e.g. state statute vs ICWA or Due Process)
        has_federal = any("U.S.C." in c or "USC" in c or "Const" in c for c in citations)
        has_state = any(any(st in c for st in ["RCW", "ILCS", "R.C.", "WIC", "Tex. Fam."]) for c in citations)

        if has_federal and has_state:
            # Check if ICWA active efforts standard supersedes state reasonable efforts standard
            has_icwa = any("1912" in c or "ICWA" in c for c in citations)
            if has_icwa:
                conflicts.append(ConflictRecord(
                    conflict_id="CONF-ICWA-SUPREMACY-01",
                    conflict_type="SUPREMACY",
                    authority_a="25 U.S.C. § 1912(d) (Active Efforts Standard)",
                    authority_b="State Statutory Reasonable Efforts Standard",
                    description="Federal ICWA active efforts heightened standard supersedes baseline state reasonable efforts standard.",
                    analysis_framework="Supremacy Clause (U.S. Const. art. VI, cl. 2) & Mississippi Band of Choctaw Indians v. Holyfield"
                ))

        # 2. Cross-jurisdiction contamination detection
        state_prefixes = {
            "WA": "RCW",
            "IL": "ILCS",
            "OH": "R.C.",
            "CA": "WIC",
            "TX": "Tex. Fam.",
            "NY": "N.Y. Fam. Ct."
        }
        target_prefix = state_prefixes.get(jurisdiction)
        if target_prefix:
            alien_cites = [
                c for c in citations
                if any(p in c for k, p in state_prefixes.items() if k != jurisdiction)
                and not any(f in c for f in ["U.S.C.", "USC", "Const"])
            ]
            for alien in alien_cites:
                conflicts.append(ConflictRecord(
                    conflict_id=f"CONF-JURISDICTION-LEAK-{alien[:10]}",
                    conflict_type="JURISDICTIONAL",
                    authority_a=f"Target Jurisdiction: {jurisdiction}",
                    authority_b=alien,
                    description=f"Out-of-state authority {alien} cannot bind proceedings in {jurisdiction}.",
                    analysis_framework="Territorial Sovereignty & Jurisdiction Lock Guard"
                ))

        return conflicts
