"""Source Priority Ranker for Legal Research Copilot.

Enforces strict source hierarchy:
PREFER:
  1. Primary authority (Constitutions, statutes, regulations, binding precedent)
  2. Official government sources (.gov, official legislative portals, eCFR)
  3. Official court sources (.courts.gov, official court slip opinions/reporters)
  4. Official agency sources (official agency policy manuals)

OVER:
  - Secondary summaries (treatises, law review articles, restatements)
  - Blogs (unverified legal blogs, firm marketing pages)
  - Forums (Reddit, Quora, discussion boards)
  - AI-generated material (synthetic text, unverified LLM answers)
"""

import re
from typing import Tuple, Optional
from core.research.models import SourcePriorityTier


class SourcePriorityRanker:
    """Classifies and ranks sources based on epistemic priority and official status."""

    # Numeric score: higher is more preferred (0 to 100)
    TIER_SCORES = {
        SourcePriorityTier.PRIMARY_CONSTITUTIONAL: 100,
        SourcePriorityTier.PRIMARY_CASELAW_BINDING: 95,
        SourcePriorityTier.PRIMARY_STATUTORY: 90,
        SourcePriorityTier.PRIMARY_REGULATORY: 85,
        SourcePriorityTier.OFFICIAL_COURT_RULES: 80,
        SourcePriorityTier.OFFICIAL_AGENCY_POLICY: 75,
        SourcePriorityTier.PRIMARY_CASELAW_PERSUASIVE: 65,
        SourcePriorityTier.SECONDARY_SUMMARY: 40,
        SourcePriorityTier.DISALLOWED_BLOG_OR_FORUM: 10,
        SourcePriorityTier.DISALLOWED_AI_GENERATED: 0,
    }

    OFFICIAL_DOMAINS = [
        ".gov",
        ".courts.gov",
        "supremecourt.gov",
        "govinfo.gov",
        "congress.gov",
        "law.cornell.edu", # LII (official mirror)
        "courtlistener.com",
        "courts.wa.gov",
        "illinoiscourts.gov",
        "txcourts.gov",
        "courts.state.ny.us",
        "leg.wa.gov",
        "ilga.gov",
        "statutes.capitol.texas.gov",
        "nysenate.gov",
        "codes.ohio.gov",
        "leginfo.legislature.ca.gov",
        "flsenate.gov"
    ]

    DISALLOWED_PATTERNS = [
        r"reddit\.com",
        r"quora\.com",
        r"facebook\.com",
        r"medium\.com",
        r"substack\.com",
        r"blog\.",
        r"/blog/",
        r"chatgpt",
        r"claude\.ai",
        r"openai\.com",
        r"gemini\.google\.com",
        r"perplexity\.ai",
        r"lawyer-marketing",
        r"forum"
    ]

    @classmethod
    def evaluate_source(
        cls,
        source_url_or_description: str,
        declared_tier: Optional[SourcePriorityTier] = None
    ) -> Tuple[SourcePriorityTier, int, bool, str]:
        """Evaluates a source string/URL and returns:
        (SourcePriorityTier, priority_score, is_official, audit_rationale)
        """
        lower = source_url_or_description.lower()

        # Check for disallowed patterns
        for pat in cls.DISALLOWED_PATTERNS:
            if re.search(pat, lower):
                if any(kw in lower for kw in ["chatgpt", "claude", "openai", "gemini", "perplexity", "synthetic", "ai-generated"]):
                    return (
                        SourcePriorityTier.DISALLOWED_AI_GENERATED,
                        0,
                        False,
                        "REJECTED: Source contains AI-generated or synthetic content, which is prohibited."
                    )
                return (
                    SourcePriorityTier.DISALLOWED_BLOG_OR_FORUM,
                    10,
                    False,
                    "DEPRECATED: Source is an unverified blog, forum, or marketing summary. Official primary sources preferred."
                )

        # Check for official government / court sources
        is_official = any(dom in lower for dom in cls.OFFICIAL_DOMAINS)

        # If declared tier provided, check compatibility
        if declared_tier:
            score = cls.TIER_SCORES.get(declared_tier, 50)
            rationale = f"Classified as {declared_tier.value} (score={score}, official={is_official})."
            return (declared_tier, score, is_official, rationale)

        # Infer based on patterns
        if any(kw in lower for kw in ["constitution", "conan", "amend. iv", "amend. xiv", "art.", "article i"]):
            return (SourcePriorityTier.PRIMARY_CONSTITUTIONAL, 100, True, "Primary Federal or State Constitutional Authority.")
        if any(kw in lower for kw in ["u.s.c.", "rcw", "ilcs", "tex. fam. code", "cal. welf", "n.y. fam", "orc §", "fla. stat."]):
            return (SourcePriorityTier.PRIMARY_STATUTORY, 90, True, "Primary Statutory Authority.")
        if any(kw in lower for kw in ["c.f.r.", "wac", "oac", "ccr", "admin. code"]):
            return (SourcePriorityTier.PRIMARY_REGULATORY, 85, True, "Primary Administrative Regulation.")
        if any(kw in lower for kw in [" u.s. ", " s. ct. ", " f.3d ", " f.4th ", " wash. 2d ", " ill. 2d "]):
            return (SourcePriorityTier.PRIMARY_CASELAW_BINDING, 95, True, "Primary Binding Caselaw Precedent.")
        if any(kw in lower for kw in ["manual", "policy handbook", "dcyf policy", "cdss manual", "dfps handbook"]):
            return (SourcePriorityTier.OFFICIAL_AGENCY_POLICY, 75, True, "Official Agency Policy / Administrative Guidelines.")

        # If domain is official government/court, treat as official primary government publication
        if is_official:
            if any(c_dom in lower for c_dom in [".courts.", "supremecourt", "courtlistener"]):
                return (SourcePriorityTier.PRIMARY_CASELAW_BINDING, 95, True, "Official Court Source / Judicial Opinion.")
            return (SourcePriorityTier.PRIMARY_STATUTORY, 90, True, "Official Government Primary Source Repository.")

        # Default fallback to secondary summary
        return (
            SourcePriorityTier.SECONDARY_SUMMARY,
            40,
            False,
            "Secondary analysis or summary. Primary government authority should be searched."
        )

    @classmethod
    def is_source_acceptable(cls, tier: SourcePriorityTier) -> bool:
        """Returns True if the source meets minimum standards for primary legal research."""
        return tier not in [
            SourcePriorityTier.DISALLOWED_BLOG_OR_FORUM,
            SourcePriorityTier.DISALLOWED_AI_GENERATED,
        ]
