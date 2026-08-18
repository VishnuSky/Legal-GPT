"""Legal GPT Master Multi-Agent Orchestrator."""

from datetime import date
from typing import Optional, Dict, Any
from agents.intake_classifier import IntakeClassifier, IntakeClassificationResult
from agents.response_formatter import StandardLegalResponse
from core.jurisdiction import JurisdictionEngine, JurisdictionContext
from core.temporal import TemporalEngine
from core.citation_verifier import CitationVerifier
from cps.lifecycle import CPSLifecycleEngine, CPSStage
from cps.parent_rights import ParentRightsAuditor
from cps.icwa_engine import ICWAEngine
from cps.interstate import InterstateEngine
from legal_registry.loader import default_registry


class LegalGPTOrchestrator:
    def __init__(self):
        self.registry = default_registry

    def process_query(
        self,
        query: str,
        override_state: Optional[str] = None,
        override_county: Optional[str] = None,
        event_date: Optional[date] = None
    ) -> StandardLegalResponse:
        # Step 1: Intake & Classification
        intake: IntakeClassificationResult = IntakeClassifier.classify(query)
        target_state = override_state or intake.primary_state or "WA" # Default to WA reference if unassigned
        target_county = override_county or intake.county

        # Step 2: Jurisdiction Lock
        jurisdiction_ctx = JurisdictionEngine.lock_jurisdiction(
            state=target_state,
            county=target_county,
            is_tribal=intake.is_tribal_icwa_matter
        )

        # Step 3: Domain / CPS Specific Reasoning
        legal_issues = []
        controlling_auth = []
        analysis_parts = []
        facts_change = []
        verify_items = []

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

        # ICWA Check
        if intake.is_tribal_icwa_matter:
            legal_issues.append("Indian Child Welfare Act (ICWA) & Tribal Jurisdiction")
            icwa_eval = ICWAEngine.evaluate_icwa(
                state=target_state,
                reason_to_know_indian_child=True,
                tribal_inquiry_on_record=True,
                tribe_notified_registered_mail=False, # Flag notice verification
                stage="foster_care"
            )
            controlling_auth.extend(icwa_eval.statutory_authorities)
            analysis_parts.append(
                f"ICWA Standards Apply: Active efforts ({icwa_eval.standard_of_proof_foster}) are mandated. "
                "Notice must be served by registered mail (return receipt requested) to the designated tribal agent."
            )
            if icwa_eval.compliance_issues:
                facts_change.extend(icwa_eval.compliance_issues)

        # Interstate Check
        if intake.is_interstate_matter:
            legal_issues.append("Interstate Child Custody Jurisdiction (UCCJEA)")
            interstate_eval = InterstateEngine.evaluate_interstate_custody(
                child_current_state=target_state,
                months_in_current_state=6,
                is_emergency_protection_needed=True
            )
            controlling_auth.extend(interstate_eval.statutory_citations)
            analysis_parts.append(interstate_eval.analysis)

        # Default fallbacks if domain is general
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

        facts_change.extend([
            "Whether formal written notice and summons were personally served on the parent.",
            "Whether the child or either parent is an enrolled member or eligible for membership in a federally recognized Indian tribe.",
            "Whether an existing custody or dependency order was previously entered in another state."
        ])

        verify_items.extend([
            f"The specific local court rules for {target_county or 'the local county'} Superior/Circuit Court.",
            "The exact date and time the child was removed or petition filed to calculate deadline compliance.",
            "Active attorney representation status on the court docket."
        ])

        # Step 4: Verification & Anti-Hallucination Audit
        citations_to_verify = []
        for auth_str in controlling_auth:
            citations_to_verify.extend(CitationVerifier.extract_citations(auth_str))

        verified_records = [CitationVerifier.verify_citation(c) for c in set(citations_to_verify)]

        # Step 5: Contamination Check
        contamination_errors = JurisdictionEngine.detect_cross_contamination(
            context=jurisdiction_ctx,
            citations=citations_to_verify
        )
        if contamination_errors:
            analysis_parts.append("\n[WARNING: Potential Cross-Jurisdiction Conflicts Detected]: " + " ".join(contamination_errors))

        jurisdiction_desc = f"{target_state} (State)" + (f" / {target_county} County" if target_county else "")

        return StandardLegalResponse(
            jurisdiction=jurisdiction_desc,
            legal_issues=legal_issues,
            short_answer=f"Under {target_state} law, actions in this matter are governed by strict statutory timeframes, mandatory parent notice, and required court hearings.",
            controlling_authority=controlling_auth,
            analysis="\n\n".join(analysis_parts),
            facts_that_could_change_result=facts_change,
            confidence_level="High" if all(r.verified for r in verified_records) else "Medium",
            what_user_should_verify=verify_items,
            verified_sources=verified_records
        )
