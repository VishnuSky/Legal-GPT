"""Legal issue spotting and claim categorization."""

import re
from typing import List, Dict, Any
from pydantic import BaseModel, Field


class LegalIssue(BaseModel):
    issue_id: str
    category: str  # CPS, CONSTITUTIONAL, HUMAN_RIGHTS, HEALTH_LAW, PROCEDURAL
    subcategory: str
    title: str
    material_facts: List[str] = Field(default_factory=list)
    controlling_legal_standards: List[str] = Field(default_factory=list)
    confidence: float = 1.0


class IssueSpotter:
    """Extracts substantive and procedural legal issues from fact patterns."""

    @classmethod
    def spot_issues(cls, text: str, jurisdiction: str = "US") -> List[LegalIssue]:
        issues = []
        text_lower = text.lower()

        # 1. CPS / Emergency Removal
        if any(w in text_lower for w in ["cps", "removal", "remove", "removed", "caseworker", "shelter care", "custody", "dependency", "dcyf", "dcfs", "child welfare"]):
            issues.append(LegalIssue(
                issue_id="ISSUE-CPS-01",
                category="CPS",
                subcategory="emergency_custody_due_process",
                title="Emergency Child Removal and Statutory Shelter Care Timelines",
                material_facts=["Alleged child removal or dependency intervention"],
                controlling_legal_standards=["Probable cause / imminent physical danger", "72-hour shelter care hearing standard"]
            ))

        # 2. Parental Rights / Counsel
        if any(w in text_lower for w in ["counsel", "attorney", "lawyer", "indigent", "rights"]):
            issues.append(LegalIssue(
                issue_id="ISSUE-PARENT-01",
                category="PARENT_RIGHTS",
                subcategory="statutory_right_to_counsel",
                title="Right to Representation and Timely Appointment of Counsel",
                controlling_legal_standards=["Fourteenth Amendment Due Process", "State statutory right to counsel"]
            ))

        # 3. ICWA Inquiry & Notice
        if any(w in text_lower for w in ["icwa", "indian child", "tribe", "tribal"]):
            issues.append(LegalIssue(
                issue_id="ISSUE-ICWA-01",
                category="ICWA",
                subcategory="mandatory_tribal_notice",
                title="ICWA Inquiry and Mandatory Tribal Notice Compliance",
                controlling_legal_standards=["25 U.S.C. § 1912(a)", "Active efforts standard"]
            ))

        # 4. UCCJEA Home State Jurisdiction
        if any(w in text_lower for w in ["uccjea", "interstate", "moved to", "different state"]):
            issues.append(LegalIssue(
                issue_id="ISSUE-UCCJEA-01",
                category="PROCEDURAL",
                subcategory="interstate_jurisdiction",
                title="UCCJEA Home State and Emergency Jurisdiction Assessment",
                controlling_legal_standards=["UCCJEA § 201 Home State rule (6 months)", "UCCJEA § 204 Temporary Emergency Jurisdiction"]
            ))

        if not issues:
            issues.append(LegalIssue(
                issue_id="ISSUE-GEN-01",
                category="GENERAL_CIVIL",
                subcategory="statutory_interpretation",
                title="General Legal Inquiry & Authority Identification",
                controlling_legal_standards=["Applicable jurisdictional statutes and regulations"]
            ))

        return issues
