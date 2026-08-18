"""Authority Ranking and Scoring Engine (Tiers 0 to 5)."""

from typing import Dict
from normalization.models import AuthorityScore


TIER_WEIGHTS: Dict[str, float] = {
    "TIER_0": 1.00,  # Official government (statutes, constitutions, official slip opinions)
    "TIER_1": 0.95,  # CourtListener, CAP, GovInfo, Congress.gov, BIA/ACF
    "TIER_2": 0.90,  # ABA, State Bar Associations, Legal Aid, Academic Law Reviews
    "TIER_3": 0.80,  # Cornell LII, Justia, FindLaw, Nolo
    "TIER_4": 0.50,  # Law firm commentary, legal blogs
    "TIER_5": 0.00,  # Forums, Social media, Ungrounded LLM completions (BARRED)
}


class AuthorityEngine:
    @staticmethod
    def get_tier_weight(tier: str) -> float:
        return TIER_WEIGHTS.get(tier, 0.0)

    @staticmethod
    def is_controlling_authority(tier: str) -> bool:
        """Returns True if the authority tier represents primary controlling law (Tier 0 or 1)."""
        return tier in ("TIER_0", "TIER_1")

    @staticmethod
    def score_source(tier: str, provider_name: str, official: bool = True) -> AuthorityScore:
        weight = TIER_WEIGHTS.get(tier, 0.0)
        return AuthorityScore(
            tier=tier,
            weight=weight,
            official_source=official,
            provider_name=provider_name
        )
