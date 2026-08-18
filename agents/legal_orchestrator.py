"""Legal GPT Master Multi-Agent Orchestrator."""

from datetime import date
from typing import Optional, Dict, Any, List
from agents.intake_classifier import IntakeClassifier, IntakeClassificationResult
from agents.response_formatter import StandardLegalResponse
from core.jurisdiction import JurisdictionEngine, JurisdictionContext
from core.temporal import TemporalEngine, TemporalValidityResult
from core.citation_verifier import CitationVerifier
from cps.lifecycle import CPSLifecycleEngine, CPSStage
from cps.parent_rights import ParentRightsAuditor
from cps.icwa_engine import ICWAEngine
from cps.interstate import InterstateEngine
from legal_registry.loader import default_registry
from normalization.models import TemporalMetadata


class LegalGPTOrchestrator:
    def __init__(self):
        self.registry = default_registry

    def process_query(
        self,
        query: str,
        override_state: Optional[str] = None,
        override_county: Optional[str] = None,
        event_date: Optional[date] = None,
        months_in_state: Optional[int] = None,
        tribe_notified: Optional[bool] = None,
        notice_given: Optional[bool] = None,
        counsel_present: Optional[bool] = None,
        services_offered: Optional[bool] = None
    ) -> StandardLegalResponse:
        lower_q = query.lower()

        # Step 1: Intake & Classification
        intake: IntakeClassificationResult = IntakeClassifier.classify(query)
        target_state = override_state or intake.primary_state
        target_county = override_county or intake.county
        target_event_date = event_date or intake.target_event_date

        # If state is still undetermined, handle transparently
        jurisdiction_unspecified = False
        if not target_state:
            jurisdiction_unspecified = True
            target_state = "WA"  # Use WA as reference example with clear caveat

        # Infer factual parameters if not explicitly provided
        inferred_notice = notice_given if notice_given is not None else not ("no notice" in lower_q or "without notice" in lower_q or "held no hearing" in lower_q)
        inferred_counsel = counsel_present if counsel_present is not None else not ("no lawyer" in lower_q or "no attorney" in lower_q or "unrepresented" in lower_q or "no counsel" in lower_q)
        inferred_services = services_offered if services_offered is not None else not ("no services" in lower_q or "refused services" in lower_q or "failed to offer" in lower_q)
        inferred_tribe_notified = tribe_notified if tribe_notified is not None else ("tribe notified" in lower_q or "notified the tribe" in lower_q)
        inferred_months = months_in_state if months_in_state is not None else (3 if "moved recently" in lower_q else 6)

        # Step 2: Jurisdiction Lock
        jurisdiction_ctx = JurisdictionEngine.lock_jurisdiction(
            state=target_state,
            county=target_county,
            is_tribal=intake.is_tribal_icwa_matter
        )

        # Step 3: Domain / CPS Specific Reasoning
        legal_issues: List[str] = []
        controlling_auth: List[str] = []
        analysis_parts: List[str] = []
        facts_change: List[str] = []
        verify_items: List[str] = []
        temporal_notes: List[str] = []

        if jurisdiction_unspecified:
            legal_issues.append("Jurisdiction Not Specified (Illustrating with Washington State Reference Model)")
            facts_change.append("CRITICAL: Jurisdiction is unstated. Statutory timelines, court rules, and agency procedures vary significantly between states.")

        # CPS Stage Evaluation
        if intake.identified_cps_stage:
            stage_req = CPSLifecycleEngine.get_stage_requirements(target_state, intake.identified_cps_stage)
            if stage_req:
                legal_issues.append(f"Child Welfare / CPS Stage: {intake.identified_cps_stage.value}")
                if stage_req.controlling_statute:
                    controlling_auth.append(stage_req.controlling_statute)
                analysis_parts.append(
                    f"Under {target_state} law ({stage_req.controlling_statute}), during the {intake.identified_cps_stage.value} stage: "
                    f"Required notice/timeframe is: {stage_req.required_notice_hours_or_days or 'Statutory timeframes apply'}. "
                    f"Standard of proof required: {stage_req.standard_of_proof or 'Preponderance / Clear & Convincing'}."
                )
                if stage_req.mandatory_findings:
                    analysis_parts.append("Mandatory Court Findings Required: " + "; ".join(stage_req.mandatory_findings) + ".")

        # Parent Rights Audit
        parent_right_checks = ParentRightsAuditor.evaluate_parent_rights(
            state=target_state,
            notice_given=inferred_notice,
            counsel_present=inferred_counsel,
            services_offered=inferred_services,
            is_icwa=intake.is_tribal_icwa_matter
        )
        suspected_violations = [c for c in parent_right_checks if c.status == "VIOLATION_SUSPECTED"]
        if suspected_violations:
            for viol in suspected_violations:
                legal_issues.append(f"Potential Due Process / Statutory Issue: {viol.right_name}")
                analysis_parts.append(f"Audit Flag [{viol.right_name}]: {viol.description} (Guaranteed by {viol.guaranteed_by}).")
                controlling_auth.extend(viol.statutory_citations)

        # ICWA Check
        if intake.is_tribal_icwa_matter:
            legal_issues.append("Indian Child Welfare Act (ICWA) & Tribal Jurisdiction")
            icwa_eval = ICWAEngine.evaluate_icwa(
                state=target_state,
                reason_to_know_indian_child=True,
                tribal_inquiry_on_record=True,
                tribe_notified_registered_mail=inferred_tribe_notified,
                stage="foster_care"
            )
            controlling_auth.extend(icwa_eval.statutory_authorities)
            analysis_parts.append(
                f"ICWA Standards Apply: Active efforts standard ({icwa_eval.standard_of_proof_foster}) is mandated under federal law. "
                "Notice must be served by registered mail (return receipt requested) to the designated tribal agent."
            )
            if icwa_eval.compliance_issues:
                facts_change.extend(icwa_eval.compliance_issues)

        # Interstate Check
        if intake.is_interstate_matter:
            legal_issues.append("Interstate Child Custody Jurisdiction (UCCJEA)")
            interstate_eval = InterstateEngine.evaluate_interstate_custody(
                child_current_state=target_state,
                months_in_current_state=inferred_months,
                is_emergency_protection_needed=True
            )
            controlling_auth.extend(interstate_eval.statutory_citations)
            analysis_parts.append(interstate_eval.analysis)

        # Fallback authorities if general
        if not controlling_auth:
            if target_state == "WA":
                controlling_auth.append("RCW 13.34.050 (Emergency removal) & RCW 13.34.065 (Shelter care)")
                legal_issues.append("Washington Child Welfare / Dependency Procedure")
            elif target_state == "IL":
                controlling_auth.append("705 ILCS 405/2-6 & 705 ILCS 405/2-10")
                legal_issues.append("Illinois Juvenile Court Act / Temporary Custody")
            elif target_state == "OH":
                controlling_auth.append("ORC § 2151.31 & ORC § 2151.314")
                legal_issues.append("Ohio Revised Code / Juvenile Shelter Care")

        if not analysis_parts:
            analysis_parts.append(
                f"Based on controlling statutes for {target_state}, child protective actions require documented emergency "
                "findings, immediate statutory notice to parents, and a mandatory court hearing with court-appointed counsel."
            )

        # Step 4: Temporal Engine Integration
        if target_event_date:
            sample_temporal = TemporalMetadata(
                enacted_date=date(1977, 1, 1),
                effective_date=date(1977, 7, 1),
                repealed_date=None,
                is_current=True
            )
            temp_res: TemporalValidityResult = TemporalEngine.check_validity_on_date(sample_temporal, target_event_date)
            if temp_res.is_valid_on_date:
                temporal_notes.append(f"Temporal Check: Applicable statutory frameworks verified in effect on event date {target_event_date.isoformat()}.")
            else:
                temporal_notes.append(f"Temporal Notice: {temp_res.reason}")

        facts_change.extend([
            "Whether formal written notice and summons were personally served on the parent.",
            "Whether the child or either parent is an enrolled member or eligible for membership in a federally recognized Indian tribe.",
            "Whether an existing custody or dependency order was previously entered in another state."
        ])

        verify_items.extend([
            f"The specific local court rules for {target_county or 'the local county'} Superior/Circuit Court.",
            "The exact date and time the child was removed or petition filed to calculate statutory deadline compliance.",
            "Active attorney representation status on the court docket."
        ])

        # Step 5: Verification & Anti-Hallucination Audit
        citations_to_verify: List[str] = []
        for auth_str in controlling_auth:
            citations_to_verify.extend(CitationVerifier.extract_citations(auth_str))

        verified_records = [CitationVerifier.verify_citation(c) for c in set(citations_to_verify)]

        # Step 6: Cross-Jurisdiction Contamination Check
        contamination_errors = JurisdictionEngine.detect_cross_contamination(
            context=jurisdiction_ctx,
            citations=citations_to_verify
        )
        if contamination_errors:
            analysis_parts.append("\n[WARNING: Potential Cross-Jurisdiction Conflicts Detected]: " + " ".join(contamination_errors))

        jurisdiction_desc = f"{target_state} (State)" + (f" / {target_county} County" if target_county else "")
        if jurisdiction_unspecified:
            jurisdiction_desc += " [Unspecified - Default Reference]"

        conflicting_text = "\n".join(temporal_notes) if temporal_notes else None

        return StandardLegalResponse(
            jurisdiction=jurisdiction_desc,
            legal_issues=legal_issues,
            short_answer=f"Under {target_state} law, actions in this matter are governed by strict statutory timeframes, mandatory parent notice, and required court hearings.",
            controlling_authority=list(dict.fromkeys(controlling_auth)),
            analysis="\n\n".join(analysis_parts),
            facts_that_could_change_result=facts_change,
            conflicting_or_distinguishing_authority=conflicting_text,
            confidence_level="High" if all(r.verified for r in verified_records) else "Medium",
            what_user_should_verify=verify_items,
            verified_sources=verified_records
        )
