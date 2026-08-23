"""Human Review Layer: 4 Dedicated Persona Rendering Modes for Legal Outputs."""

from typing import List, Optional, Dict, Any
from agents.response_formatter import StandardLegalResponse
from core.proposition_verifier import PropositionVerificationReport
from agents.adversarial_reviewer import AdversarialCounterargument


class PersonaRenderer:
    """Renders tailored legal analysis across 4 operational human review personas."""

    @classmethod
    def render_self_represented(
        cls,
        resp: StandardLegalResponse,
        counterarguments: Optional[List[AdversarialCounterargument]] = None
    ) -> str:
        """Mode 1: Plain-English explanation for parents and self-represented litigants."""
        lines = [
            f"# Plain-Language Legal Guide: Child Welfare & Parental Rights",
            f"**Jurisdiction**: {resp.jurisdiction}\n",
            f"## 1. What You Need to Know Right Now",
            f"{resp.short_answer}\n",
            f"## 2. Explanation of Your Rights",
            f"{resp.analysis}\n",
            f"## 3. Important Deadlines & Things to Investigate",
        ]
        for item in resp.what_user_should_verify:
            lines.append(f"- [ ] {item}")

        lines.extend([
            "\n## 4. Documents & Evidence You Should Gather",
            "- Copy of the petition, court summons, and notice of hearing.",
            "- In-home safety plan with names and contact information of reliable relatives.",
            "- Proof of housing stability, employment, or completed assessments.",
            "- Case logs of all communications with caseworkers and visits with your child.\n",
            "## 5. Potential Pitfalls to Avoid (What the Agency Might Argue)"
        ])
        if counterarguments:
            for adv in counterarguments:
                lines.append(f"- **Warning**: {adv.opposing_argument}")
                lines.append(f"  *How to respond*: {adv.rebuttal_strategy}")

        lines.append(
            "\n> **⚠️ IMPORTANT**: This is for educational and research purposes. Always request your court-appointed attorney at your very first hearing."
        )
        return "\n".join(lines)

    @classmethod
    def render_investigator(
        cls,
        resp: StandardLegalResponse,
        facts_summary: Optional[str] = None
    ) -> str:
        """Mode 2: Evidence-focused layout for paralegals, social workers, and factual investigators."""
        lines = [
            f"# Fact & Evidence Investigation Brief",
            f"**Jurisdiction**: {resp.jurisdiction} | **Confidence**: {resp.confidence_level}\n",
            f"## 1. Primary Legal Issues & CPS Stage",
        ]
        for issue in resp.legal_issues:
            lines.append(f"- {issue}")

        lines.extend([
            "\n## 2. Controlling Authority & Statutory Standards",
        ])
        for auth in resp.controlling_authority:
            lines.append(f"- `{auth}`")

        lines.extend([
            "\n## 3. Factual Ambiguities & Missing Evidence Checklist",
        ])
        for fact in resp.facts_that_could_change_result:
            lines.append(f"- [ ] **Investigate**: {fact}")

        lines.extend([
            "\n## 4. Field Verification Action Items",
        ])
        for item in resp.what_user_should_verify:
            lines.append(f"- [ ] {item}")

        return "\n".join(lines)

    @classmethod
    def render_attorney_memo(
        cls,
        resp: StandardLegalResponse,
        counterarguments: Optional[List[AdversarialCounterargument]] = None
    ) -> str:
        """Mode 3: Formal Legal Research Memorandum for licensed attorneys."""
        lines = [
            f"# CONFIDENTIAL ATTORNEY WORK PRODUCT / LEGAL RESEARCH MEMORANDUM",
            f"**TO**: Supervising Attorney / Legal Team",
            f"**FROM**: Legal-GPT Core Research Engine",
            f"**JURISDICTION**: {resp.jurisdiction}",
            f"**CONFIDENCE LEVEL**: {resp.confidence_level}\n",
            f"## I. QUESTIONS PRESENTED",
        ]
        for idx, issue in enumerate(resp.legal_issues, 1):
            lines.append(f"{idx}. {issue}")

        lines.extend([
            "\n## II. BRIEF ANSWER",
            f"{resp.short_answer}\n",
            f"## III. CONTROLLING LEGAL AUTHORITIES",
        ])
        for auth in resp.controlling_authority:
            lines.append(f"- {auth}")

        lines.extend([
            "\n## IV. LEGAL ANALYSIS & STATUTORY FRAMEWORK",
            f"{resp.analysis}\n",
            f"## V. ADVERSARIAL COUNTERARGUMENTS & VULNERABILITIES",
        ])
        if counterarguments:
            for adv in counterarguments:
                lines.append(f"### Challenge [{adv.challenge_category}]: {adv.claim_challenged}")
                lines.append(f"- **Opposing Theory**: {adv.opposing_argument}")
                lines.append(f"- **Authority**: `{adv.opposing_authority or 'State/Federal Rules'}`")
                lines.append(f"- **Rebuttal Strategy**: {adv.rebuttal_strategy}\n")
        else:
            lines.append("No immediate structural counterarguments identified.")

        lines.extend([
            "## VI. CITATION VERIFICATION & CITATOR AUDIT",
        ])
        for src in resp.verified_sources:
            lines.append(f"- [VERIFIED: {src.authority_tier}] `{src.normalized_citation}` ({src.publisher_name})")

        return "\n".join(lines)

    @classmethod
    def render_court_review(
        cls,
        resp: StandardLegalResponse,
        session_id: str = "SESSION-UNKNOWN"
    ) -> str:
        """Mode 4: Judicial/Professional Review layout with human sign-off blocks and audit log."""
        lines = [
            f"# Court & Professional AI Verification Record",
            f"**Session ID**: `{session_id}` | **Forum**: {resp.jurisdiction}\n",
            f"## 1. Verified Controlling Authority Table",
            f"| Citation | Authority Level | Publisher | Verified Status |",
            f"|---|---|---|---|"
        ]
        for src in resp.verified_sources:
            lines.append(f"| `{src.normalized_citation}` | {src.authority_tier} | {src.publisher_name} | ✅ PASS |")

        lines.extend([
            "\n## 2. Substantive Analysis Summary",
            f"{resp.analysis}\n",
            f"## 3. Human Attorney Review & Certification Block",
            f"```",
            f"I, the undersigned attorney/reviewer, hereby certify pursuant to Federal Rule of Civil Procedure 11",
            f"and ABA Formal Opinion 512 that I have independently verified all legal citations, quotations,",
            f"and statutory authorities referenced in this document against primary official legal sources.",
            f"",
            f"Reviewer Name:  ____________________________________",
            f"Bar Number:     ____________________________________",
            f"Date Reviewed:  ____________________________________",
            f"Signature:      ____________________________________",
            f"```"
        ])
        return "\n".join(lines)
