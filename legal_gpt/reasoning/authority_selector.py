"""Authority Selector for dynamic 14-tier legal authority discovery."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class SelectedAuthority(BaseModel):
    citation: str
    authority_tier: str  # TIER_0 to TIER_13
    weight: float
    is_binding: bool
    rationale: str


class AuthoritySelector:
    """Selects and ranks governing legal authority according to the dynamic 14-tier hierarchy."""

    @classmethod
    def select_governing_authorities(
        cls,
        jurisdiction: str,
        category: str,
        primary_citations: List[str]
    ) -> List[SelectedAuthority]:
        selected = []
        for cite in primary_citations:
            is_us_const = "U.S. Const" in cite or "US Const" in cite
            is_federal_statute = "U.S.C." in cite or "USC" in cite
            is_state_statute = any(prefix in cite for prefix in ["RCW", "ILCS", "R.C.", "WIC", "Tex. Fam. Code", "N.Y. Fam. Ct."])

            if is_us_const:
                selected.append(SelectedAuthority(
                    citation=cite,
                    authority_tier="TIER_0",
                    weight=1.00,
                    is_binding=True,
                    rationale="Supreme Law of the Land (Article VI Supremacy Clause)"
                ))
            elif is_federal_statute:
                selected.append(SelectedAuthority(
                    citation=cite,
                    authority_tier="TIER_0",
                    weight=1.00,
                    is_binding=True,
                    rationale="Federal statutory mandate binding across all states"
                ))
            elif is_state_statute:
                selected.append(SelectedAuthority(
                    citation=cite,
                    authority_tier="TIER_0",
                    weight=0.98,
                    is_binding=True,
                    rationale=f"Controlling primary statute within {jurisdiction}"
                ))
            else:
                selected.append(SelectedAuthority(
                    citation=cite,
                    authority_tier="TIER_1",
                    weight=0.90,
                    is_binding=True,
                    rationale="Primary judicial or administrative authority"
                ))

        return selected
