"""Document Explainer Renderer: Generates formatted Markdown summaries for Document Explanation Reports."""

from core.document_explainer.models import DocumentExplanationReport


class DocumentExplainerRenderer:
    """Renders document explanations into clear, accessible Markdown format."""

    @staticmethod
    def render_markdown(report: DocumentExplanationReport) -> str:
        lines = []
        lines.append(f"## 📑 Legal Document Breakdown: {report.document_title}")
        lines.append("")
        lines.append(f"- **Category:** `{report.document_category}`")
        lines.append(f"- **Jurisdiction:** `{report.jurisdiction}`")
        lines.append(f"- **Issuing Body:** {report.issuing_body}")
        lines.append(f"- **Purpose:** {report.purpose_summary}")
        lines.append("")

        if report.verification_status == "UNKNOWN_AUTHORITY_GAP":
            lines.append("> [!WARNING]\n> **Authority Gap:** Unrecognized document format. No verified statutory deadlines could be matched.\n")

        lines.append("### 💡 Explanation")
        if report.literacy_level == 1:
            lines.append(f"**Plain English:**\n{report.plain_english_explanation}\n")
        elif report.literacy_level == 2:
            lines.append(f"**Practical Guide:**\n{report.practical_explanation}\n")
        else:
            lines.append(f"**Legal Analysis:**\n{report.legal_terminology_explanation}\n")

        if report.deadlines:
            lines.append("### ⏱️ Critical Deadlines & Response Windows")
            lines.append("| Milestone / Action | Statutory Timeframe | Governing Authority | Consequence of Missing |")
            lines.append("| :--- | :--- | :--- | :--- |")
            for d in report.deadlines:
                lines.append(f"| **{d.name}** | `{d.timeframe}` | `{d.citation}` | {d.consequence_of_missing} |")
            lines.append("")

        if report.rights:
            lines.append("### ⚖️ Rights & Legal Protections")
            for r in report.rights:
                lines.append(f"- **{r.right_name}** (`{r.authority}`): {r.description}")
            lines.append("")

        if report.consequences_of_inaction:
            lines.append("### ⚠️ Potential Consequences of Inaction")
            for c in report.consequences_of_inaction:
                lines.append(f"- {c}")
            lines.append("")

        if report.recommended_actions:
            lines.append("### ✅ Recommended Next Steps")
            for a in report.recommended_actions:
                badge = "🔴 `URGENT`" if a.priority == "URGENT" else "🟡 `IMPORTANT`"
                lines.append(f"- {badge} **{a.step}:** {a.description}")
            lines.append("")

        lines.append(f"> [!NOTE]\n> {report.disclaimer}")

        return "\n".join(lines)
