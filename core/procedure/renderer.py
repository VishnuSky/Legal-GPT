"""Markdown renderer for Procedural Pathway reports."""

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.procedure.models import ProceduralPathwayReport


class ProceduralReportRenderer:
    """Renders ProceduralPathwayReport into structured, user-facing Markdown."""

    @classmethod
    def render_markdown(cls, report: "ProceduralPathwayReport") -> str:
        lines = []

        # Header & Non-Predictive Notice
        lines.append(f"# Procedural Pathway Report: {report.current_stage.stage_name}")
        lines.append(f"**Track**: `{report.track.value}` | **Jurisdiction**: `{report.jurisdiction}`\n")
        lines.append(f"> ℹ️ **Notice**: {report.epistemic_notice}\n")

        # 1. CURRENT STAGE
        lines.append("## 1. Current Stage")
        lines.append(f"### {report.current_stage.stage_name} (Stage #{report.current_stage.order})")
        lines.append(f"{report.current_stage.description}\n")
        if report.current_stage.decision_makers:
            lines.append(f"- **Primary Decision-Makers**: {', '.join(report.current_stage.decision_makers)}")
        if report.current_stage.notice_requirements:
            lines.append("- **Notice Requirements**:")
            for n in report.current_stage.notice_requirements:
                lines.append(f"  - 📋 {n}")
        if report.current_stage.hearing_opportunities:
            lines.append("- **Hearing Opportunities**:")
            for h in report.current_stage.hearing_opportunities:
                lines.append(f"  - ⚖️ {h}")
        lines.append("")

        # 2. POSSIBLE NEXT STAGES
        lines.append("## 2. Possible Next Stages")
        if report.possible_next_stages:
            for nxt in report.possible_next_stages:
                lines.append(f"- **{nxt.stage_name}** (Stage #{nxt.order})")
                lines.append(f"  - *Overview*: {nxt.description}")
        else:
            lines.append("- *This is a concluding or post-appeal stage.*")
        lines.append("")

        # 3. AUTHORITY
        lines.append("## 3. Governing Legal Authority")
        if report.authority:
            for auth in report.authority:
                lines.append(f"- 🏛️ `{auth}`")
        else:
            lines.append("- *General procedural rules apply.*")
        lines.append("")

        # 4. REQUIRED VERIFICATION
        lines.append("## 4. Required Procedural Verification")
        if report.required_verification:
            for req in report.required_verification:
                lines.append(f"- [ ] {req}")
        else:
            lines.append("- [ ] Verify formal case caption, cause number, and assigned division.")
        lines.append("")

        # 5. IMPORTANT DATES & DEADLINES
        lines.append("## 5. Important Dates & Statutory Deadlines")
        if report.important_dates:
            for d in report.important_dates:
                lines.append(f"- ⏱️ **{d.get('label', 'Deadline')}**: {d.get('description', '')}")
                if d.get("statutory_citation"):
                    lines.append(f"  - *Authority*: `{d.get('statutory_citation')}`")
        elif report.current_stage.statutory_deadlines:
            for dl in report.current_stage.statutory_deadlines:
                lines.append(f"- ⏱️ {dl}")
        else:
            lines.append("- *No automatic statutory clock detected. Confirm with court scheduling order.*")
        lines.append("")

        # 6. QUESTIONS TO ASK
        lines.append("## 6. Questions to Ask an Attorney or Court Clerk")
        if report.questions_to_ask:
            for idx, q in enumerate(report.questions_to_ask, 1):
                lines.append(f"{idx}. {q}")
        lines.append("")

        # 7. DOCUMENTS TO LOCATE
        lines.append("## 7. Critical Documents to Locate and Preserve")
        if report.documents_to_locate:
            for doc in report.documents_to_locate:
                lines.append(f"- 📄 **{doc}**")
        lines.append("")

        # 8. AVAILABLE REVIEW / CHALLENGE MECHANISMS
        lines.append("## 8. Available Review and Challenge Mechanisms")
        if report.available_review_mechanisms:
            for rev in report.available_review_mechanisms:
                lines.append(f"- 🛡️ {rev}")
        lines.append("")

        # 9. UNKNOWN FACTS
        lines.append("## 9. Unknown Facts Dictating Pathway Branches")
        lines.append("The answers to the following unknown facts determine which branch this case will take:")
        if report.unknown_facts:
            for uf in report.unknown_facts:
                lines.append(f"- ❓ {uf}")
        else:
            lines.append("- ❓ Whether formal summons and petition have been served on all parties.")
        lines.append("")

        return "\n".join(lines)
