"""Renderer for Legal Research Copilot Plan conforming strictly to required output sections."""

from core.research.models import ResearchPlanOutput


class ResearchPlanRenderer:
    """Formats ResearchPlanOutput into markdown with the 10 required output sections."""

    @classmethod
    def render_markdown(cls, plan: ResearchPlanOutput) -> str:
        lines = []

        # SECTION 1: RESEARCH QUESTION
        lines.append("## RESEARCH QUESTION")
        lines.append(f"{plan.research_question}\n")

        # SECTION 2: JURISDICTION
        lines.append("## JURISDICTION")
        lines.append(f"**Governing Jurisdiction**: `{plan.jurisdiction}`")
        lines.append(f"**Legal System**: `{plan.plan_steps.step_2_legal_system.value}`")
        lines.append(f"**Forum Analysis**: {plan.plan_steps.step_15_jurisdiction_check}\n")

        # SECTION 3: DATE
        lines.append("## DATE")
        lines.append(f"**Temporal Context**: {plan.date}")
        if plan.plan_steps.step_14_temporal_validity:
            lines.append("**Statutory Temporal Validity Checks**:")
            for cite, status in plan.plan_steps.step_14_temporal_validity.items():
                lines.append(f"- `{cite}`: {status}")
        lines.append("")

        # SECTION 4: ISSUES
        lines.append("## ISSUES")
        lines.append(f"**Procedural Posture**: {plan.plan_steps.step_4_procedural_posture}")
        lines.append("**Identified Legal Issues**:")
        for idx, issue in enumerate(plan.issues, 1):
            lines.append(f"{idx}. {issue}")
        lines.append("")

        # SECTION 5: AUTHORITIES TO SEARCH
        lines.append("## AUTHORITIES TO SEARCH")
        lines.append("*(Ranked in accordance with Source Priority Rules: Primary & Official Government Sources preferred)*\n")
        lines.append("| Type | Authority / Query | Priority Tier | Official Government/Court Source | Purpose |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for target in plan.authorities_to_search:
            type_str = target.authority_type
            cite_str = f"`{target.citation_or_query}`"
            tier_str = f"**{target.source_priority.value}**"
            portal_str = target.preferred_official_source
            purpose_str = target.purpose
            lines.append(f"| {type_str} | {cite_str} | {tier_str} | {portal_str} | {purpose_str} |")
        lines.append("")

        # SECTION 6: SEARCH RESULTS
        lines.append("## SEARCH RESULTS")
        if plan.search_results:
            for res in plan.search_results:
                official_badge = "✅ OFFICIAL GOVERNMENT/COURT SOURCE" if res.is_official_government_source else "⚠️ SECONDARY SOURCE"
                lines.append(f"### `{res.citation}` — {official_badge}")
                lines.append(f"- **Title**: {res.title}")
                lines.append(f"- **Source Priority Tier**: `{res.source_tier.value}`")
                lines.append(f"- **Official Portal**: {res.official_source_url_or_portal}")
                lines.append(f"- **Subsequent Treatment**: `{res.subsequent_treatment}`")
                lines.append(f"- **Temporal Status**: `{res.temporal_status}`")
                lines.append(f"- **Exemplar Authoritative Rule**: \"{res.key_excerpt}\"")
                lines.append("")
        else:
            lines.append("*No search results currently retrieved.*\n")

        # SECTION 7: AUTHORITY CONFLICTS
        lines.append("## AUTHORITY CONFLICTS")
        if plan.authority_conflicts:
            for conflict in plan.authority_conflicts:
                lines.append(f"### Conflict Type: `{conflict.conflict_type}` [{conflict.status}]")
                lines.append(f"- **Controlling Authority**: `{conflict.primary_authority}`")
                lines.append(f"- **Conflicting Authority**: `{conflict.conflicting_authority}`")
                lines.append(f"- **Supremacy / Conflict Analysis**: {conflict.explanation}")
                lines.append("")
        else:
            lines.append("Zero authority conflicts detected between applicable statutory provisions.\n")

        # SECTION 8: UNANSWERED QUESTIONS
        lines.append("## UNANSWERED QUESTIONS")
        lines.append("*(Critical factual and legal predicates required before a substantive answer can be generated)*:\n")
        for idx, uq in enumerate(plan.unanswered_questions, 1):
            lines.append(f"{idx}. {uq}")
        lines.append("")

        # SECTION 9: VERIFICATION STATUS
        lines.append("## VERIFICATION STATUS")
        lines.append(f"**Status**: `{plan.verification_status}`")
        if plan.plan_steps.step_13_subsequent_treatment:
            lines.append("**Citator Verification Signals**:")
            for cite, sig in plan.plan_steps.step_13_subsequent_treatment.items():
                lines.append(f"- `{cite}`: {sig}")
        lines.append("")

        # SECTION 10: RESEARCH COMPLETE / INCOMPLETE
        lines.append(f"## {plan.completeness_status}")
        if plan.completeness_status == "RESEARCH COMPLETE":
            lines.append("✅ **All 18 research planning steps fulfilled.** Primary controlling authorities located, temporal validity verified, and conflicts addressed. Ready for substantive analysis.")
        else:
            lines.append("⚠️ **Research plan remains incomplete.** Substantive conclusions must not be drafted until unanswered questions are clarified, jurisdiction is locked, or missing authorities are inspected.")
        lines.append("")

        return "\n".join(lines)
