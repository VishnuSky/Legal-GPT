"""Deadline Renderer: Generates formatted Markdown summaries for Deadline Reports."""

from core.deadlines.models import DeadlineReport


class DeadlineRenderer:
    """Renders deadline calculation reports as structured Markdown or plain text."""

    @staticmethod
    def render_markdown(report: DeadlineReport) -> str:
        """Renders a DeadlineReport into an auditable Markdown summary."""
        lines = []
        lines.append(f"## ⏱️ Procedural Deadline Calculation: {report.event_type.replace('_', ' ').title()}")
        lines.append("")
        lines.append(f"- **Triggering Event Date:** `{report.event_date}`")
        lines.append(f"- **Jurisdiction:** `{report.jurisdiction}`" + (f" ({report.county} County)" if report.county else ""))
        lines.append("")

        if report.error:
            lines.append(f"> [!CAUTION]\n> **Calculation Error:** {report.error}\n")
            return "\n".join(lines)

        if report.warnings:
            for w in report.warnings:
                lines.append(f"> [!WARNING]\n> {w}\n")

        if not report.deadlines:
            lines.append("_No applicable statutory deadlines identified._")
            return "\n".join(lines)

        lines.append("| Milestone / Deadline | Due Date | Calculation Mode | Governing Authority | Citation | Verification |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")

        for d in report.deadlines:
            due_badge = f"**`{d.due_date}`**" if d.due_date != "UNKNOWN" else "`UNKNOWN`"
            lines.append(
                f"| {d.name} | {due_badge} | {d.calendar_or_court_days} | {d.authority} | `{d.citation}` | {d.verification_status} |"
            )

        lines.append("")
        for d in report.deadlines:
            if d.notes:
                lines.append(f"- **{d.name}:** {d.notes}")

        lines.append("")
        lines.append(
            "> [!NOTE]\n"
            "> **Disclaimer:** Deadlines are computed based on primary statutory sources and standard court day rules. "
            "> Local court rules, judicial discretion, emergency continuances, or county-level administrative orders may alter dates."
        )

        return "\n".join(lines)
