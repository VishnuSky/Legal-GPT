"""Question Builder Renderer: Formats question sets and document checklists into Markdown."""

from core.question_builder.models import QuestionBuilderReport


class QuestionBuilderRenderer:
    """Renders customized question reports into structured, printable Markdown checklists."""

    @staticmethod
    def render_markdown(report: QuestionBuilderReport) -> str:
        lines = []
        lines.append(f"## 📝 Tactical Question Builder: {report.situation.replace('_', ' ').title()}")
        lines.append("")
        lines.append(f"- **Target Recipient:** `{report.target_recipient}`")
        lines.append(f"- **Jurisdiction:** `{report.jurisdiction}`")
        lines.append(f"- **Role:** `{report.user_role}`")
        lines.append(f"- **Summary:** {report.summary}")
        lines.append("")

        lines.append("### 🎯 Prioritized Question Checklist")
        lines.append("_Questions are structured strictly: (1) Rights First, (2) Deadlines Second, (3) Procedure Third, (4) Documentation Fourth._")
        lines.append("")

        for q in report.prioritized_questions:
            tier_badge = {
                1: "🔴 **TIER 1 — RIGHTS**",
                2: "🟠 **TIER 2 — DEADLINES**",
                3: "🟡 **TIER 3 — PROCEDURAL STATUS**",
                4: "🟢 **TIER 4 — EVIDENCE & DOCUMENTATION**"
            }.get(q.priority_tier, f"Tier {q.priority_tier}")

            lines.append(f"#### {tier_badge}: {q.category}")
            lines.append(f"> **Ask:** \"{q.question_text}\"")
            lines.append(f"- **Why Ask:** {q.rationale}")
            if q.statutory_hook:
                lines.append(f"- **Legal Authority:** `{q.statutory_hook}`")
            lines.append(f"- **Expected Response Type:** `{q.expected_response_type}`")
            lines.append("")

        if report.documents_to_request:
            lines.append("### 📥 Documents to Request From Agency / Other Party")
            for doc in report.documents_to_request:
                lines.append(f"- [ ] **Request:** {doc}")
            lines.append("")

        if report.documents_to_bring:
            lines.append("### 💼 Documents to Bring / Prepare")
            for doc in report.documents_to_bring:
                lines.append(f"- [ ] **Prepare:** {doc}")
            lines.append("")

        if report.tactical_tips:
            lines.append("### 💡 Tactical Tips & Best Practices")
            for tip in report.tactical_tips:
                lines.append(f"- {tip}")
            lines.append("")

        lines.append(
            "> [!NOTE]\n"
            "> **Disclaimer:** These questions are prepared for informational and advocacy preparation purposes. "
            "> Always review case-specific strategy with your licensed legal counsel before formal court proceedings."
        )

        return "\n".join(lines)
