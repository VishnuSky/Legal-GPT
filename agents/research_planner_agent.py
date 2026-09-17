"""Research Planning Agent for Legal-GPT.

Generates an exhaustive 18-step research plan before any substantive answer
is constructed, enforcing source hierarchy and identifying unverified gaps.
"""

from typing import Optional, Dict, Any
from core.research.models import ResearchPlanOutput
from core.research.planner import LegalResearchPlanner
from core.research.renderer import ResearchPlanRenderer
from agents.intake_classifier import IntakeClassifier


class LegalResearchPlannerAgent:
    """Autonomous research planning agent that structures the investigation strategy."""

    def __init__(self):
        self.planner = LegalResearchPlanner

    def create_research_plan(
        self,
        query: str,
        state: Optional[str] = None,
        date_context: Optional[str] = None,
        posture: Optional[str] = None,
        is_tribal: Optional[bool] = None
    ) -> ResearchPlanOutput:
        """Constructs an 18-step research plan from a legal question and factual context."""
        # If state or tribal status not explicitly passed, run intake classifier
        target_state = state
        target_tribal = is_tribal

        if not target_state or target_tribal is None:
            intake = IntakeClassifier.classify(query)
            if not target_state:
                target_state = intake.primary_state
            if target_tribal is None:
                target_tribal = intake.is_tribal_icwa_matter

        return self.planner.generate_plan(
            question=query,
            jurisdiction=target_state,
            date_context=date_context,
            procedural_posture=posture,
            is_tribal=target_tribal
        )

    def plan_and_render(
        self,
        query: str,
        state: Optional[str] = None,
        date_context: Optional[str] = None,
        posture: Optional[str] = None,
        is_tribal: Optional[bool] = None
    ) -> str:
        """Generates research plan and renders Markdown with all 10 required sections."""
        plan = self.create_research_plan(
            query=query,
            state=state,
            date_context=date_context,
            posture=posture,
            is_tribal=is_tribal
        )
        return ResearchPlanRenderer.render_markdown(plan)
