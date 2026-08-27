"""Automated Parent Rights Audit & Comprehensive Due Process Report Engine."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class DueProcessRightCheck(BaseModel):
    right_name: str
    status: str  # COMPLIANT, POTENTIAL_VIOLATION, CRITICAL_VIOLATION, INSUFFICIENT_INFORMATION
    severity_rating: str  # HIGH, MEDIUM, LOW
    guaranteeing_authority: str
    statutory_standard: str
    factual_findings: str
    recommended_remedy: str


class DueProcessAuditReport(BaseModel):
    jurisdiction: str
    cps_stage: str
    total_checks: int
    compliant_count: int
    violations_count: int
    overall_due_process_health_score: float
    checks: List[DueProcessRightCheck] = Field(default_factory=list)
    summary_narrative: str


class DueProcessAuditor:
    """Performs an exhaustive audit of parental and family due process protections across all 14 CPS stages."""

    @classmethod
    def audit_case(
        cls,
        state: str,
        stage: str = "EMERGENCY_REMOVAL",
        notice_served_personally: bool = True,
        notice_served_hours_before_hearing: Optional[int] = 24,
        counsel_appointed: bool = True,
        counsel_present_at_hearing: bool = True,
        relative_placement_explored: bool = True,
        services_tailored_and_offered: bool = True,
        family_visitation_ordered: bool = True,
        is_icwa_eligible: bool = False,
        tribal_notice_registered_mail: bool = True,
        statutory_deadline_met: bool = True
    ) -> DueProcessAuditReport:
        checks: List[DueProcessRightCheck] = []

        # Pillar 1: Notice & Personal Service
        if not notice_served_personally or (notice_served_hours_before_hearing is not None and notice_served_hours_before_hearing < 24):
            checks.append(DueProcessRightCheck(
                right_name="Right to Timely Notice & Personal Service",
                status="CRITICAL_VIOLATION",
                severity_rating="HIGH",
                guaranteeing_authority=f"{state} Juvenile Court Rules & 14th Amendment Due Process",
                statutory_standard="Written summons and petition must be served in advance of preliminary hearing.",
                factual_findings="Parent was not personally served or received insufficient advance notice of the initial hearing.",
                recommended_remedy="File Motion & Affidavit for Rehearing based on lack of notice; move to vacate preliminary detention findings."
            ))
        else:
            checks.append(DueProcessRightCheck(
                right_name="Right to Timely Notice & Personal Service",
                status="COMPLIANT",
                severity_rating="LOW",
                guaranteeing_authority=f"{state} Juvenile Court Rules",
                statutory_standard="Timely personal service.",
                factual_findings="Notice served in compliance with statutory notice rules.",
                recommended_remedy="Maintain service records on file."
            ))

        # Pillar 2: Right to Appointed Counsel
        if not counsel_appointed or not counsel_present_at_hearing:
            checks.append(DueProcessRightCheck(
                right_name="Right to Court-Appointed Legal Counsel",
                status="CRITICAL_VIOLATION",
                severity_rating="HIGH",
                guaranteeing_authority="Lassiter v. DSS (452 U.S. 18) & State Right to Counsel Statutes",
                statutory_standard="Immediate appointment of independent legal counsel for indigent parents at all critical stages.",
                factual_findings="Parent appeared at a critical hearing without legal representation or advisement of counsel rights.",
                recommended_remedy="Demand immediate appointment of counsel on the record and request a brief recess/continuance to consult."
            ))
        else:
            checks.append(DueProcessRightCheck(
                right_name="Right to Court-Appointed Legal Counsel",
                status="COMPLIANT",
                severity_rating="LOW",
                guaranteeing_authority="State Right to Counsel Statutes",
                statutory_standard="Representation by appointed or retained counsel.",
                factual_findings="Parent is represented by counsel on the docket.",
                recommended_remedy="Coordinate defense strategy with attorney."
            ))

        # Pillar 3: Relative / Kinship Placement Preference
        if not relative_placement_explored:
            checks.append(DueProcessRightCheck(
                right_name="Kinship Placement Preference & Relative Search Duty",
                status="POTENTIAL_VIOLATION",
                severity_rating="MEDIUM",
                guaranteeing_authority="42 U.S.C. § 671(a)(29) & State Relative Placement Preferences",
                statutory_standard="Agency must identify and notify adult relatives within 30 days of removal and prioritize kinship placement.",
                factual_findings="Agency placed child in stranger foster care without documenting inquiry into willing fit relatives.",
                recommended_remedy="File Motion for Change of Placement to Fit Relative pursuant to state kinship preference statutes."
            ))
        else:
            checks.append(DueProcessRightCheck(
                right_name="Kinship Placement Preference & Relative Search Duty",
                status="COMPLIANT",
                severity_rating="LOW",
                guaranteeing_authority="42 U.S.C. § 671(a)(29)",
                statutory_standard="Kinship placement exploration.",
                factual_findings="Relative placement search documented.",
                recommended_remedy="Ensure relative home study is completed promptly."
            ))

        # Pillar 4: Reasonable Efforts Standard
        if not services_tailored_and_offered:
            checks.append(DueProcessRightCheck(
                right_name="Reasonable Efforts to Prevent Removal / Reunify",
                status="POTENTIAL_VIOLATION",
                severity_rating="HIGH",
                guaranteeing_authority="42 U.S.C. § 671(a)(15) & In re Dependency of K.N.J. (171 Wn.2d 568)",
                statutory_standard="Agency must make reasonable, tailored remedial efforts to prevent removal and alleviate safety concerns.",
                factual_findings="Services offered were generic or agency failed to offer active remedial services to address alleged deficiencies.",
                recommended_remedy="Request specific 'No Reasonable Efforts' finding on the record at next court review hearing."
            ))
        else:
            checks.append(DueProcessRightCheck(
                right_name="Reasonable Efforts to Prevent Removal / Reunify",
                status="COMPLIANT",
                severity_rating="LOW",
                guaranteeing_authority="42 U.S.C. § 671(a)(15)",
                statutory_standard="Reasonable efforts provision.",
                factual_findings="Remedial services offered to parent.",
                recommended_remedy="Document attendance and compliance with service referrals."
            ))

        # Pillar 5: Family Visitation / Parent-Child Contact
        if not family_visitation_ordered:
            checks.append(DueProcessRightCheck(
                right_name="Right to Frequent Family Visitation / Family Time",
                status="POTENTIAL_VIOLATION",
                severity_rating="MEDIUM",
                guaranteeing_authority="State CPS Visitation Policies & Due Process Family Integrity",
                statutory_standard="First visit must occur within 72 hours of removal with a minimum schedule of weekly contact.",
                factual_findings="Court or agency restricted or failed to schedule parent-child visitation without evidence of actual harm.",
                recommended_remedy="File Motion for Immediate Family Visitation and liberalized parenting time."
            ))
        else:
            checks.append(DueProcessRightCheck(
                right_name="Right to Frequent Family Visitation / Family Time",
                status="COMPLIANT",
                severity_rating="LOW",
                guaranteeing_authority="State Visitation Policy",
                statutory_standard="Regular family visitation.",
                factual_findings="Family visitation schedule ordered.",
                recommended_remedy="Maintain regular visitation log with dates, notes, and photos."
            ))

        # Pillar 6: ICWA Invalidation Triggers (if applicable)
        if is_icwa_eligible:
            if not tribal_notice_registered_mail:
                checks.append(DueProcessRightCheck(
                    right_name="ICWA Mandatory Registered Mail Notice & Active Efforts",
                    status="CRITICAL_VIOLATION",
                    severity_rating="HIGH",
                    guaranteeing_authority="25 U.S.C. §§ 1912(a), 1914 & Haaland v. Brackeen (599 U.S. 255)",
                    statutory_standard="Notice must be served by registered mail with return receipt requested; 10-day waiting period before hearing.",
                    factual_findings="Designated tribal agent was not served by registered mail or statutory waiting period was ignored.",
                    recommended_remedy="File Petition to Invalidate State Custody Proceedings under 25 U.S.C. § 1914."
                ))
            else:
                checks.append(DueProcessRightCheck(
                    right_name="ICWA Mandatory Registered Mail Notice & Active Efforts",
                    status="COMPLIANT",
                    severity_rating="LOW",
                    guaranteeing_authority="25 U.S.C. § 1912",
                    statutory_standard="ICWA notice compliance.",
                    factual_findings="Registered mail notice verified on court record.",
                    recommended_remedy="Coordinate with Tribal ICWA Representative."
                ))

        # Pillar 7: Statutory Hearing Deadlines
        if not statutory_deadline_met:
            checks.append(DueProcessRightCheck(
                right_name="Statutory Emergency Hearing Deadline Compliance",
                status="CRITICAL_VIOLATION",
                severity_rating="HIGH",
                guaranteeing_authority=f"{state} Emergency Custody Statutes (e.g. 72h WA/OH, 48h IL, 3d NY)",
                statutory_standard="Preliminary adversary hearing held within strict hours/days.",
                factual_findings="Child held in custody beyond the statutory deadline without timely hearing or good cause continuance.",
                recommended_remedy="File Motion for Immediate Release of Child due to expiration of statutory detention authority."
            ))
        else:
            checks.append(DueProcessRightCheck(
                right_name="Statutory Emergency Hearing Deadline Compliance",
                status="COMPLIANT",
                severity_rating="LOW",
                guaranteeing_authority=f"{state} Statutes",
                statutory_standard="Statutory timeline compliance.",
                factual_findings="Hearing held within statutory deadline.",
                recommended_remedy="Verify calculation of judicial days vs calendar days."
            ))

        violations = [c for c in checks if "VIOLATION" in c.status]
        compliant = [c for c in checks if c.status == "COMPLIANT"]
        score = round(len(compliant) / max(1, len(checks)), 2)

        summary = (
            f"Due Process Audit for {state} ({stage}): Evaluated {len(checks)} core procedural pillars. "
            f"Result: {len(compliant)} Compliant, {len(violations)} Violations/Risks Identified. "
            f"Overall Due Process Health Score: {score * 100:.0f}%."
        )

        return DueProcessAuditReport(
            jurisdiction=state,
            cps_stage=stage,
            total_checks=len(checks),
            compliant_count=len(compliant),
            violations_count=len(violations),
            overall_due_process_health_score=score,
            checks=checks,
            summary_narrative=summary
        )
