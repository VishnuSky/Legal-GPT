"""Standard Legal Response Formatter enforcing strict legal structure and disclaimers."""

from typing import List, Optional
from pydantic import BaseModel, Field
from core.citation_verifier import CitationVerificationRecord


class StandardLegalResponse(BaseModel):
    jurisdiction: str # e.g. "Washington (State) / Skagit County"
    legal_issues: List[str]
    short_answer: str
    controlling_authority: List[str]
    analysis: str
    facts_that_could_change_result: List[str]
    conflicting_or_distinguishing_authority: Optional[str] = None
    confidence_level: str = "Medium" # High, Medium, Low
    what_user_should_verify: List[str]
    verified_sources: List[CitationVerificationRecord]
    disclaimer: str = (
        "IMPORTANT LEGAL DISCLAIMER: This information is provided for legal research, educational, and informational "
        "purposes only and does NOT constitute legal advice or create an attorney-client relationship. Legal outcomes depend "
        "on specific facts, local court rules, and judicial discretion. If you are facing a child welfare proceeding, court "
        "hearing, or statutory deadline, consult promptly with a licensed attorney or your court-appointed counsel."
    )

    def render_markdown(self) -> str:
        lines = [
            f"### **JURISDICTION**\n{self.jurisdiction}\n",
            "### **LEGAL ISSUES IDENTIFIED**",
        ]
        for i, issue in enumerate(self.legal_issues, 1):
            lines.append(f"{i}. {issue}")
        lines.append("")

        lines.append(f"### **SHORT ANSWER**\n{self.short_answer}\n")

        lines.append("### **CONTROLLING LEGAL AUTHORITY**")
        for auth in self.controlling_authority:
            lines.append(f"- **{auth}**")
        lines.append("")

        lines.append(f"### **LEGAL ANALYSIS**\n{self.analysis}\n")

        if self.facts_that_could_change_result:
            lines.append("### **FACTS THAT COULD CHANGE THE RESULT**")
            for fact in self.facts_that_could_change_result:
                lines.append(f"- {fact}")
            lines.append("")

        if self.conflicting_or_distinguishing_authority:
            lines.append(f"### **CONFLICTING OR DISTINGUISHING AUTHORITY**\n{self.conflicting_or_distinguishing_authority}\n")

        lines.append(f"### **CONFIDENCE LEVEL**\n**{self.confidence_level}**\n")

        if self.what_user_should_verify:
            lines.append("### **WHAT YOU SHOULD VERIFY BEFORE RELYING ON THIS INFORMATION**")
            for item in self.what_user_should_verify:
                lines.append(f"- {item}")
            lines.append("")

        lines.append("### **SOURCES & VERIFICATION STATUS**")
        for src in self.verified_sources:
            status_tag = "VERIFIED (Tier 0/1)" if src.verified else "FAILED VERIFICATION"
            lines.append(f"- [{status_tag}] **{src.normalized_citation}** ({src.publisher_name}) - {src.source_url or 'Registry Reference'}")
        lines.append("")

        lines.append(f"> **{self.disclaimer}**")

        return "\n".join(lines)
