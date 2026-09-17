"""Renderer for Legal Explanation Trace records and interrogative inquiries."""

from core.explanation_trace.models import (
    ExplanationTraceRecord,
    InterrogativeTraceResult,
    ExplanationTraceReport,
)


class ExplanationTraceRenderer:
    """Renders 10-field trace records and interrogative trace inquiries into structured markdown."""

    @classmethod
    def render_trace_record(cls, record: ExplanationTraceRecord) -> str:
        """Renders all 10 required fields of a substantive legal conclusion trace."""
        lines = [
            "## LEGAL EXPLANATION TRACE",
            "",
            f"### 1. CLAIM",
            f"{record.claim}\n",
            f"### 2. SOURCE",
            f"`{record.source}`\n",
            f"### 3. AUTHORITY LEVEL",
            f"`{record.authority_level}`\n",
            f"### 4. JURISDICTION",
            f"`{record.jurisdiction}`\n",
            f"### 5. EFFECTIVE DATE",
            f"{record.effective_date}\n",
            f"### 6. RELEVANT TEXT",
            f"> \"{record.relevant_text}\"\n",
            f"### 7. REASONING STEP",
            f"{record.reasoning_step}\n",
            f"### 8. CONFIDENCE / VERIFICATION",
            f"`{record.confidence_verification}`\n",
            f"### 9. COUNTERARGUMENT",
            f"{record.counterargument}\n",
            f"### 10. LIMITATION",
            f"{record.limitation}\n",
            "---",
            "### Available Interrogative Traces:",
            "- `WHY?` — Underlying justification and policy rationale",
            "- `SOURCE?` — Exact primary authority, publisher, and official portal",
            "- `WHEN?` — Temporal validity, effective dates, and statutory deadlines",
            "- `WHERE?` — Forum locking, jurisdictional limits, and court rules",
            "- `WHAT IF?` — Counterfactual analysis under altered facts",
            "- `WHAT CHANGED?` — Evolution of the doctrine and statutory reforms",
            "- `WHAT DISAGREES?` — Competing theories, circuit splits, and opposing views",
            "- `WHAT IS MISSING?` — Missing factual predicates and unverified records"
        ]
        return "\n".join(lines)

    @classmethod
    def render_interrogative_result(cls, result: InterrogativeTraceResult) -> str:
        """Renders an interrogative trace query result."""
        lines = [
            f"## INTERROGATIVE TRACE: [{result.trace_type.value}]",
            f"**Inquiry**: *{result.inquiry}*",
            f"**Claim Target**: \"{result.claim}\"\n",
            result.concise_auditable_summary,
            ""
        ]

        if result.supporting_authority:
            lines.append("### Supporting Legal Authority:")
            for auth in result.supporting_authority:
                lines.append(f"- `{auth}`")
            lines.append("")

        if result.factual_predicates_required:
            lines.append("### Required Factual / Evidentiary Predicates:")
            for pred in result.factual_predicates_required:
                lines.append(f"- [ ] {pred}")
            lines.append("")

        if result.official_portal_url:
            lines.append(f"**Official Source Portal**: {result.official_portal_url}\n")

        return "\n".join(lines)
