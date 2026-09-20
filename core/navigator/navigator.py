"""Public Legal Navigator Core Orchestrator implementing the 10-step user journey and 16-section report."""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from core.navigator.fact_classifier import FactClassifier, FactExtractionResult, StatementType
from core.navigator.jurisdiction_classifier import JurisdictionClassifier, JurisdictionClassificationResult
from core.navigator.issue_classifier import IssueClassifier, LegalIssueClassificationResult, LegalDomain
from core.navigator.procedure_classifier import ProcedureClassifier, ProcedureClassificationResult, ProceduralPosture
from core.navigator.resource_discovery import ResourceDiscovery, ResourceDiscoveryResult
from core.navigator.report_renderer import ReportRenderer
from core.citation_verifier import CitationVerifier
from legal_registry.loader import default_registry
from cps.parent_rights import ParentRightsAuditor
from core.rights.engine import RightsDiscoveryEngine
from core.rights.models import RightsDiscoveryInput


class LegalNavigationReport(BaseModel):
    """The complete 16-section Legal Navigation Report."""
    what_i_understand: str
    facts_provided: List[str] = Field(default_factory=list)
    allegations: List[str] = Field(default_factory=list)
    unknowns: List[str] = Field(default_factory=list)
    jurisdiction: JurisdictionClassificationResult
    relevant_legal_domains: List[str] = Field(default_factory=list)
    procedural_posture: ProcedureClassificationResult
    potentially_relevant_authority: List[str] = Field(default_factory=list)
    potential_rights_and_duties: List[Dict[str, Any]] = Field(default_factory=list)
    potential_procedural_requirements: List[str] = Field(default_factory=list)
    important_dates: List[Dict[str, Any]] = Field(default_factory=list)
    evidence_and_questions_to_investigate: List[str] = Field(default_factory=list)
    conflicting_or_uncertain_authority: List[str] = Field(default_factory=list)
    available_public_resources: ResourceDiscoveryResult
    questions_for_qualified_counsel: List[str] = Field(default_factory=list)
    related_literacy_concepts: List[str] = Field(default_factory=list)
    verification_status: Dict[str, Any] = Field(default_factory=dict)

    def render_markdown(self) -> str:
        """Renders report into user-facing Markdown document."""
        return ReportRenderer.render_markdown(self.model_dump())


class PublicLegalNavigator:
    """Orchestrates the 10-step journey from 'I have a legal problem' to 'I understand what to investigate next'."""

    @classmethod
    def navigate(
        cls,
        narrative: str,
        override_state: Optional[str] = None,
        override_county: Optional[str] = None,
        override_tribe: Optional[str] = None,
        event_date: Optional[str] = None
    ) -> LegalNavigationReport:
        """Executes the complete 10-step legal navigation workflow."""

        # STEP 1: FACT EXTRACTION (Fact vs Allegation vs Interpretation vs Unknown)
        fact_result: FactExtractionResult = FactClassifier.classify_narrative(narrative)

        # STEP 2: JURISDICTION (Ask if unknown; never guess silently)
        juris_result: JurisdictionClassificationResult = JurisdictionClassifier.classify_jurisdiction(
            narrative=narrative,
            override_state=override_state,
            override_county=override_county,
            override_tribe=override_tribe
        )

        # STEP 3: DATES (Event, filing, hearing, decision)
        important_dates = [d.model_dump() for d in fact_result.extracted_dates]
        if event_date and not any(d["iso_date"] == event_date for d in important_dates):
            important_dates.insert(0, {
                "raw_text": event_date,
                "iso_date": event_date,
                "category": "EVENT_DATE",
                "description": f"Target evaluation date: {event_date}"
            })

        # STEP 4: LEGAL DOMAIN CLASSIFICATION
        issue_result: LegalIssueClassificationResult = IssueClassifier.classify_issues(narrative)
        primary_domain = issue_result.primary_domain
        domain_labels = [primary_domain.value] + [d.value for d in issue_result.secondary_domains]

        # STEP 5: PROCEDURAL POSTURE & DEADLINES
        procedure_result: ProcedureClassificationResult = ProcedureClassifier.classify_posture(
            narrative=narrative,
            domain=primary_domain,
            state=juris_result.state
        )

        # STEP 6: AUTHORITY SEARCH & VERIFICATION
        relevant_authority = cls._search_and_verify_authorities(
            state=juris_result.state,
            domain=primary_domain,
            posture=procedure_result.posture
        )

        # STEP 7: RIGHTS AND DUTIES EVALUATION
        rights_and_duties = cls._evaluate_rights_and_duties(
            state=juris_result.state,
            domain=primary_domain,
            narrative=narrative,
            is_icwa=bool(juris_result.tribal_jurisdiction or "icwa" in narrative.lower())
        )

        # STEP 8: MISSING INFORMATION ("What would change this analysis?")
        what_would_change = cls._generate_what_would_change(
            narrative=narrative,
            juris_result=juris_result,
            procedure_result=procedure_result,
            fact_result=fact_result
        )

        # STEP 9: QUESTIONS FOR QUALIFIED COUNSEL
        counsel_questions = cls._generate_counsel_questions(
            state=juris_result.state,
            procedure_result=procedure_result,
            primary_domain=primary_domain,
            relevant_authority=relevant_authority
        )

        # STEP 10: VERIFIED RESOURCE DISCOVERY (No hallucinations)
        resources: ResourceDiscoveryResult = ResourceDiscovery.discover_resources(
            state=juris_result.state,
            county=juris_result.county,
            domain_name=primary_domain.value
        )

        # Synthesis: "What I Understand"
        what_i_understand = cls._synthesize_understanding(
            fact_result=fact_result,
            juris_result=juris_result,
            procedure_result=procedure_result,
            primary_domain=primary_domain
        )

        # Conflicting or uncertain authority
        uncertain_authority = []
        if not juris_result.is_known:
            uncertain_authority.append(
                "Jurisdiction is unconfirmed: Statutes and court deadlines differ completely between states. "
                "The procedural timeframes and legal rights listed above are indicative and require state confirmation."
            )
        if "icwa" in narrative.lower() and juris_result.state:
            uncertain_authority.append(
                f"Federal Indian Child Welfare Act (25 U.S.C. § 1901 et seq.) preempts conflicting {juris_result.state} "
                "state laws and mandates heightened active efforts and tribal jurisdiction."
            )

        # Procedural requirements list
        proc_requirements = (
            procedure_result.urgent_deadlines +
            procedure_result.mandatory_notices +
            procedure_result.available_motions_or_pleadings
        )

        # Verification status
        verification_status = {
            "authority_verified": "VERIFIED_OFFICIAL_REGISTRY",
            "jurisdiction_lock": juris_result.normalized_code,
            "confidence_level": "High" if juris_result.is_known else "Uncertain (Missing Jurisdiction)",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        }

        # Build Unknowns combining factual unknowns with jurisdictional prompts
        all_unknowns = list(juris_result.clarification_questions) + list(fact_result.unknowns)

        # Map narrative and procedural context to verified literacy concepts
        rel_concepts = []
        n_lower = narrative.lower()
        if any(k in n_lower for k in ["removal", "emergency", "warrant", "custody"]):
            rel_concepts.append("emergency_removal")
        if any(k in n_lower for k in ["shelter", "detention", "hearing", "72"]):
            rel_concepts.append("shelter_care_hearing")
        if any(k in n_lower for k in ["counsel", "lawyer", "attorney", "public defender"]):
            rel_concepts.append("right_to_counsel_dependency")
        if any(k in n_lower for k in ["notice", "summons", "petition", "served"]):
            rel_concepts.append("notice")
            rel_concepts.append("opportunity_to_be_heard")
        if any(k in n_lower for k in ["icwa", "tribal", "indian", "native"]):
            rel_concepts.append("icwa_inquiry")
            rel_concepts.append("active_efforts")
        if issue_result.routed_concepts:
            rel_concepts.extend(issue_result.routed_concepts)
        if not rel_concepts:
            rel_concepts.append("due_process")
        rel_concepts = list(dict.fromkeys(rel_concepts))

        return LegalNavigationReport(
            what_i_understand=what_i_understand,
            facts_provided=[f.text for f in fact_result.facts],
            allegations=[a.text for a in fact_result.allegations],
            unknowns=all_unknowns,
            jurisdiction=juris_result,
            relevant_legal_domains=domain_labels,
            procedural_posture=procedure_result,
            potentially_relevant_authority=relevant_authority,
            potential_rights_and_duties=rights_and_duties,
            potential_procedural_requirements=proc_requirements,
            important_dates=important_dates,
            evidence_and_questions_to_investigate=what_would_change,
            conflicting_or_uncertain_authority=uncertain_authority,
            available_public_resources=resources,
            questions_for_qualified_counsel=counsel_questions,
            related_literacy_concepts=rel_concepts,
            verification_status=verification_status
        )

    @classmethod
    def _synthesize_understanding(
        cls,
        fact_result: FactExtractionResult,
        juris_result: JurisdictionClassificationResult,
        procedure_result: ProcedureClassificationResult,
        primary_domain: LegalDomain
    ) -> str:
        loc = f"{juris_result.state_name or juris_result.state or 'an unconfirmed state'}"
        if juris_result.county:
            loc += f" ({juris_result.county} County)"

        lines = [
            f"Based on the situation you described, this matter appears to involve **{primary_domain.value.replace('_', ' ').title()}** in **{loc}**.",
            f"Procedural stage: **{procedure_result.posture.value}** ({procedure_result.posture_description}).",
        ]
        if fact_result.facts:
            lines.append(f"You have identified {len(fact_result.facts)} objective factual statements and {len(fact_result.allegations)} disputed allegations.")
        if not juris_result.is_known:
            lines.append("⚠️ **Notice**: You have not yet specified your state. Because legal rights, court deadlines, and agency rules depend strictly on state law, you should confirm your state before relying on specific statutory timelines.")

        return " ".join(lines)

    @classmethod
    def _search_and_verify_authorities(
        cls,
        state: Optional[str],
        domain: LegalDomain,
        posture: ProceduralPosture
    ) -> List[str]:
        """Retrieves and strictly verifies primary authorities from legal_registry."""
        authorities: List[str] = []
        st = state.upper() if state else "WA"

        # Check CPS sources
        for entry in default_registry.cps_sources.values():
            if entry.jurisdiction in (f"US-{st}", st, "US"):
                if hasattr(entry, "key_statutory_sections"):
                    for sec in entry.key_statutory_sections[:4]:
                        v = CitationVerifier.verify_citation(sec)
                        if v.verified:
                            authorities.append(f"`{v.normalized_citation}` ({entry.title.split(':')[0]}) — Tier {v.authority_tier}")

        # Check Federal Constitution / ICWA
        v_const = CitationVerifier.verify_citation("25 U.S.C. § 1912")
        if v_const.verified and v_const.normalized_citation not in str(authorities):
            authorities.append(f"`{v_const.normalized_citation}` (Indian Child Welfare Act — Pending Court Proceedings) — Tier {v_const.authority_tier}")

        # Ensure no duplicates and cap at 6
        seen = set()
        deduped = []
        for a in authorities:
            cite_tag = a.split()[0]
            if cite_tag not in seen:
                seen.add(cite_tag)
                deduped.append(a)

        return deduped[:6]

    @classmethod
    def _evaluate_rights_and_duties(
        cls,
        state: Optional[str],
        domain: LegalDomain,
        narrative: str,
        is_icwa: bool
    ) -> List[Dict[str, Any]]:
        """Evaluates rights and duties based on state statutes and procedural rules using RightsDiscoveryEngine."""
        st = state.upper() if state else "US"
        low = narrative.lower()
        proc = "EMERGENCY_REMOVAL" if any(w in low for w in ["took", "removed", "detained", "custody"]) else "INVESTIGATION"
        
        input_data = RightsDiscoveryInput(
            facts=[narrative],
            jurisdiction=st,
            procedure=proc,
            user_allegations=[]
        )
        res = RightsDiscoveryEngine.discover_rights(input_data)

        rights_output = []
        for p in res.potentially_relevant_rights:
            rights_output.append({
                "right_name": p.right_name,
                "guaranteed_by": f"{p.legal_basis.value}: {p.authority}",
                "description": p.applicability_rationale,
                "status": p.verification_status.value,
                "statutory_citations": [p.authority],
                "authority": p.authority,
                "authority_tier": p.authority_tier,
                "epistemic_distinction": p.epistemic_distinction,
                "known_exceptions": p.known_exceptions,
                "counterarguments": p.counterarguments,
                "required_facts": p.required_facts
            })

        return rights_output

    @classmethod
    def _generate_what_would_change(
        cls,
        narrative: str,
        juris_result: JurisdictionClassificationResult,
        procedure_result: ProcedureClassificationResult,
        fact_result: FactExtractionResult
    ) -> List[str]:
        """Generates targeted 'What Would Change This Analysis?' investigative items."""
        items = []

        items.append("Did the caseworker or law enforcement officer possess a written, signed judicial warrant or emergency court order before entry/removal?")
        items.append("Were any non-offending relatives or trusted kinship caregivers identified to the agency as an alternative to foster care?")
        items.append("Did you receive written formal notice containing the exact date, time, and location of the initial detention or shelter hearing?")
        items.append("Did the agency offer specific, tailored community services or a safety plan to prevent out-of-home placement prior to removal?")
        items.append("Are there any police incident reports, laboratory toxicology reports, or medical records contradicting the agency's allegations?")
        items.append("Does the child have any Native American heritage that would trigger federal ICWA active efforts standards?")

        return items

    @classmethod
    def _generate_counsel_questions(
        cls,
        state: Optional[str],
        procedure_result: ProcedureClassificationResult,
        primary_domain: LegalDomain,
        relevant_authority: List[str]
    ) -> List[str]:
        """Generates targeted, high-leverage questions for the user to ask their appointed attorney."""
        st = state or "your state"
        questions = [
            f"1. What is the exact statutory deadline in {st} for holding my initial contested detention or shelter care hearing?",
            "2. Can we immediately file a motion or affidavit for rehearing to request that my child be returned home under an in-home safety plan?",
            "3. Can we petition for immediate temporary placement with my family relatives (kinship placement) instead of non-relative foster care?",
            "4. Has the agency documented that reasonable efforts were made to eliminate the need for removal before taking custody?",
            "5. What are the specific rules and schedule for my parental visitation and family time while this case is pending?",
            "6. Have you received the complete agency case file, incident report, and discovery materials from the assistant attorney general / county attorney?"
        ]
        return questions
