"""Legal Literacy Agent for progressive multi-tier explanation and on-demand drill-downs."""

from typing import Optional
from core.literacy.models import (
    LiteracyLevel,
    DrillDownAction,
    DrillDownResult,
    LegalConceptExploration,
)
from core.literacy.engine import LegalLiteracyEngine
from core.literacy.renderer import LiteracyRenderer


class LegalLiteracyAgent:
    """Agent interface for multi-level legal concept explanations and interactive drill-downs."""

    def __init__(self):
        self.engine = LegalLiteracyEngine
        self.renderer = LiteracyRenderer

    def explain(
        self,
        concept: str,
        level: Optional[int] = None,
        jurisdiction: Optional[str] = None,
        situation: Optional[str] = None
    ) -> LegalConceptExploration:
        """Explains a legal concept across 5 progressive levels."""
        lit_level = LiteracyLevel(level) if level in (1, 2, 3, 4, 5) else None
        return self.engine.explain(
            concept=concept,
            level=lit_level,
            jurisdiction=jurisdiction,
            situation=situation
        )

    def explain_and_render(
        self,
        concept: str,
        level: Optional[int] = None,
        jurisdiction: Optional[str] = None,
        situation: Optional[str] = None
    ) -> str:
        """Explains a concept and returns formatted Markdown."""
        lit_level = LiteracyLevel(level) if level in (1, 2, 3, 4, 5) else None
        exploration = self.explain(
            concept=concept,
            level=level,
            jurisdiction=jurisdiction,
            situation=situation
        )
        return self.renderer.render_exploration(exploration, requested_level=lit_level)

    def drill_down(
        self,
        concept: str,
        action: DrillDownAction,
        jurisdiction: Optional[str] = None,
        situation: Optional[str] = None
    ) -> DrillDownResult:
        """Executes one of the 5 on-demand drill-down requests."""
        return self.engine.drill_down(
            concept=concept,
            action=action,
            jurisdiction=jurisdiction,
            situation=situation
        )

    def drill_down_and_render(
        self,
        concept: str,
        action: DrillDownAction,
        jurisdiction: Optional[str] = None,
        situation: Optional[str] = None
    ) -> str:
        """Executes a drill-down and returns formatted Markdown."""
        result = self.drill_down(
            concept=concept,
            action=action,
            jurisdiction=jurisdiction,
            situation=situation
        )
        return self.renderer.render_drill_down(result)
