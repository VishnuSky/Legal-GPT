"""Explanation Trace Agent for Legal-GPT."""

from typing import Optional, Any
from core.explanation_trace.models import (
    InterrogativeTraceType,
    ExplanationTraceRecord,
    InterrogativeTraceResult,
)
from core.explanation_trace.engine import ExplanationTraceEngine
from core.explanation_trace.renderer import ExplanationTraceRenderer


class ExplanationTraceAgent:
    """Agent that traces legal conclusions across 10 structured fields and executes 8 interrogatives."""

    def __init__(self):
        self.engine = ExplanationTraceEngine
        self.renderer = ExplanationTraceRenderer

    def trace_conclusion(
        self,
        conclusion: str,
        jurisdiction: Optional[str] = None
    ) -> ExplanationTraceRecord:
        """Generates a 10-field explanation trace for a substantive legal conclusion."""
        return self.engine.trace_conclusion(conclusion, jurisdiction=jurisdiction)

    def trace_and_render(
        self,
        conclusion: str,
        jurisdiction: Optional[str] = None
    ) -> str:
        """Generates a 10-field explanation trace and returns Markdown."""
        record = self.trace_conclusion(conclusion, jurisdiction=jurisdiction)
        return self.renderer.render_trace_record(record)

    def interrogate(
        self,
        conclusion: str,
        trace_type: InterrogativeTraceType,
        scenario_context: Optional[str] = None,
        jurisdiction: Optional[str] = None
    ) -> InterrogativeTraceResult:
        """Interrogates a conclusion with one of the 8 queries without revealing hidden CoT."""
        return self.engine.interrogate(
            conclusion_or_record=conclusion,
            query_type=trace_type,
            scenario_context=scenario_context,
            jurisdiction=jurisdiction
        )

    def interrogate_and_render(
        self,
        conclusion: str,
        trace_type: InterrogativeTraceType,
        scenario_context: Optional[str] = None,
        jurisdiction: Optional[str] = None
    ) -> str:
        """Interrogates a conclusion and renders Markdown."""
        result = self.interrogate(
            conclusion=conclusion,
            trace_type=trace_type,
            scenario_context=scenario_context,
            jurisdiction=jurisdiction
        )
        return self.renderer.render_interrogative_result(result)
