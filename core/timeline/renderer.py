"""Timeline Renderer: Generates formatted Markdown summaries and visual representations of legal timelines."""

from core.timeline.models import TimelineReport, SequenceFlag


class TimelineRenderer:
    """Renders a TimelineReport into an auditable Markdown summary and diagram."""

    @staticmethod
    def render_markdown(report: TimelineReport) -> str:
        lines = []
        lines.append("## 📅 Procedural Case Timeline Analysis")
        lines.append("")
        lines.append(f"- **Total Events:** {report.total_events}")
        lines.append(f"- **Jurisdictions Involved:** {', '.join(report.jurisdictions_involved) if report.jurisdictions_involved else 'Unspecified'}")
        lines.append(f"- **Compliance Score:** `{int(report.procedural_compliance_score * 100)}%`")
        lines.append(f"- **Summary:** {report.summary}")
        lines.append("")

        if report.detected_issues:
            lines.append("### ⚠️ Detected Procedural Sequence Issues")
            for issue in report.detected_issues:
                badge = "🔴 **CRITICAL DEFECT**" if issue.severity == "CRITICAL" else "🟡 **WARNING**"
                lines.append(f"- {badge}: `{issue.issue_type}`")
                lines.append(f"  - **Details:** {issue.description}")
                if issue.governing_authority:
                    lines.append(f"  - **Authority:** {issue.governing_authority}")
                if issue.affected_events:
                    lines.append(f"  - **Affected Event IDs:** {', '.join(issue.affected_events)}")
            lines.append("")

        lines.append("### 📜 Chronological Sequence of Events")
        lines.append("")
        lines.append("| Date | Category | Title | Flags | Jurisdiction | Notes |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")

        for ev in report.chronological_events:
            flags_str = ", ".join(f"`{f}`" for f in ev.flags) if ev.flags else "—"
            jur_str = ev.jurisdiction or "—"
            notes_str = ev.notes or ev.description or "—"
            lines.append(f"| `{ev.date}` | **{ev.category}** | {ev.title} | {flags_str} | {jur_str} | {notes_str} |")

        lines.append("")
        lines.append("### 📊 Procedural Flow Diagram")
        lines.append("```text")
        for i, ev in enumerate(report.chronological_events):
            flag_marker = " [!]" if ev.flags else ""
            lines.append(f"[{ev.date}] -- ({ev.category}) --> {ev.title}{flag_marker}")
            if i < len(report.chronological_events) - 1:
                lines.append("     │")
                lines.append("     ▼")
        lines.append("```")

        lines.append("")
        lines.append(
            "> [!NOTE]\n"
            "> **Disclaimer:** Timeline sequence analysis reflects general procedural statutory requirements. "
            "> Judicial continuances, statutory tolling, or local court scheduling orders may validate apparent gaps."
        )

        return "\n".join(lines)
