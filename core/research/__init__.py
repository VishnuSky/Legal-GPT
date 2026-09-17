"""Legal Research Copilot: 18-step Research Planning and Source Hierarchy Subsystem."""

from core.research.models import (
    LegalSystem,
    SourcePriorityTier,
    AuthoritySearchTarget,
    ResearchSearchResult,
    AuthorityConflictItem,
    ResearchPlan18Steps,
    ResearchPlanOutput,
)
from core.research.source_ranker import SourcePriorityRanker
from core.research.planner import LegalResearchPlanner
from core.research.renderer import ResearchPlanRenderer

__all__ = [
    "LegalSystem",
    "SourcePriorityTier",
    "AuthoritySearchTarget",
    "ResearchSearchResult",
    "AuthorityConflictItem",
    "ResearchPlan18Steps",
    "ResearchPlanOutput",
    "SourcePriorityRanker",
    "LegalResearchPlanner",
    "ResearchPlanRenderer",
]
