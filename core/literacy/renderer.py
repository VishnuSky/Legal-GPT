"""Renderer for Legal Literacy Engine outputs."""

from typing import Optional
from core.literacy.models import (
    LiteracyLevel,
    DrillDownAction,
    DrillDownResult,
    LegalConceptExploration,
)


class LiteracyRenderer:
    """Formats LegalConceptExploration and DrillDownResult into clear markdown."""

    @classmethod
    def render_exploration(
        cls,
        exploration: LegalConceptExploration,
        requested_level: Optional[LiteracyLevel] = None
    ) -> str:
        """Renders either a specific level or the entire 5-level progressive breakdown."""
        lines = []
        lines.append(f"# Legal Literacy Guide: {exploration.concept_name}")
        lines.append(f"**Jurisdiction**: `{exploration.jurisdiction}`")
        if exploration.situational_context:
            lines.append(f"**Context / Situation**: {exploration.situational_context}")
        lines.append("")

        if requested_level == LiteracyLevel.LEVEL_1_PLAIN_ENGLISH or requested_level == 1:
            lines.append("## LEVEL 1: Plain English")
            lines.append(exploration.level_1_plain_english)
            return "\n".join(lines)

        if requested_level == LiteracyLevel.LEVEL_2_PRACTICAL or requested_level == 2:
            lines.append("## LEVEL 2: Practical Explanation")
            lines.append(exploration.level_2_practical)
            return "\n".join(lines)

        if requested_level == LiteracyLevel.LEVEL_3_TERMINOLOGY or requested_level == 3:
            lines.append("## LEVEL 3: Legal Terminology")
            lines.append(exploration.level_3_terminology)
            return "\n".join(lines)

        if requested_level == LiteracyLevel.LEVEL_4_PRIMARY_AUTHORITY or requested_level == 4:
            lines.append("## LEVEL 4: Primary Authority")
            for auth in exploration.level_4_primary_authority:
                lines.append(f"### `{auth.citation}` ({auth.source_type})")
                lines.append(f"- **Official Portal**: {auth.official_portal_url}")
                lines.append(f"- **Key Holding / Text**: \"{auth.key_holding_or_text}\"")
                lines.append("")
            return "\n".join(lines)

        if requested_level == LiteracyLevel.LEVEL_5_ADVANCED_ANALYSIS or requested_level == 5:
            lines.append("## LEVEL 5: Advanced Legal Analysis")
            lines.append(exploration.level_5_advanced_analysis)
            return "\n".join(lines)

        # If no specific level requested, render all 5 levels progressively
        lines.append("## LEVEL 1: Plain English")
        lines.append(f"{exploration.level_1_plain_english}\n")

        lines.append("## LEVEL 2: Practical Explanation")
        lines.append(f"{exploration.level_2_practical}\n")

        lines.append("## LEVEL 3: Legal Terminology")
        lines.append(f"{exploration.level_3_terminology}\n")

        lines.append("## LEVEL 4: Primary Authority")
        for auth in exploration.level_4_primary_authority:
            lines.append(f"- **`{auth.citation}`** [{auth.source_type}]: \"{auth.key_holding_or_text}\" *(Official: {auth.official_portal_url})*")
        lines.append("")

        lines.append("## LEVEL 5: Advanced Legal Analysis")
        lines.append(f"{exploration.level_5_advanced_analysis}\n")

        lines.append("---")
        lines.append("### Available On-Demand Drill-Downs:")
        lines.append("- *\"Show me the source.\"* (`SHOW_SOURCE`)")
        lines.append("- *\"Show me the statute.\"* (`SHOW_STATUTE`)")
        lines.append("- *\"Show me the case.\"* (`SHOW_CASE`)")
        lines.append("- *\"Explain the opposing interpretation.\"* (`EXPLAIN_OPPOSING`)")
        lines.append("- *\"Show me what changed over time.\"* (`SHOW_TEMPORAL_CHANGE`)")

        return "\n".join(lines)

    @classmethod
    def render_drill_down(cls, result: DrillDownResult) -> str:
        """Renders the result of an on-demand drill-down query."""
        lines = []
        lines.append(f"## Drill-Down: {result.title}")
        lines.append(f"**Action**: `{result.action.value}`\n")
        lines.append(result.content)
        lines.append("")

        if result.citations:
            lines.append("**Key Citations Referenced**:")
            for cite in result.citations:
                lines.append(f"- `{cite}`")
            lines.append("")

        if result.official_sources:
            lines.append("**Official Government/Court Portals**:")
            for src in result.official_sources:
                lines.append(f"- {src}")
            lines.append("")

        return "\n".join(lines)
