"""Legal Literacy Engine: Multi-Level Concept Breakdown & On-Demand Drill-Down Actions."""

from typing import Optional, Dict, Any, List, Tuple
from core.literacy.models import (
    LiteracyLevel,
    DrillDownAction,
    DrillDownResult,
    LegalConceptExploration,
    PrimaryAuthorityReference,
)
from core.literacy.registry import LegalConceptRegistry
from core.citation_verifier import CitationVerifier
from core.temporal_graph import temporal_graph
from core.explanation_trace.engine import ExplanationTraceEngine
from core.explanation_trace.models import (
    ExplanationTraceRecord,
    InterrogativeTraceType,
    InterrogativeTraceResult,
)
from knowledge_graph.relational_graph import citator_graph
from legal_registry.loader import default_registry


class LegalLiteracyEngine:
    """Core engine for progressive legal literacy and interactive legal exploration."""

    @classmethod
    def explain(
        cls,
        concept: str,
        level: Optional[LiteracyLevel] = None,
        jurisdiction: Optional[str] = None,
        situation: Optional[str] = None
    ) -> LegalConceptExploration:
        """Retrieves or synthesizes a 5-level exploration for a legal concept, verified against primary law."""
        exploration = LegalConceptRegistry.get_concept(
            concept_query=concept,
            jurisdiction=jurisdiction,
            situation=situation
        )

        # Truth Engine Wire: Verify all Level 4 authority rows against CitationVerifier
        failed_citations = []
        for auth in exploration.level_4_primary_authority:
            v_record = CitationVerifier.verify_citation(auth.citation)
            if not v_record.verified:
                auth.verification_status = "UNVERIFIED"
                failed_citations.append(auth.citation)
            else:
                if auth.verification_status != "UNVERIFIED":
                    auth.verification_status = "VERIFIED"
                if not auth.official_portal_url and v_record.source_url:
                    auth.official_portal_url = v_record.source_url

        if failed_citations:
            req_j = (exploration.jurisdiction or "").upper().replace("US-", "")
            has_valid_state = any(
                a.verification_status == "VERIFIED" and (a.jurisdiction or "").upper().replace("US-", "") == req_j
                for a in exploration.level_4_primary_authority
            )
            has_valid_fed = any(
                a.verification_status == "VERIFIED" and (a.jurisdiction or "").upper().replace("US-", "") in ("US", "FED")
                for a in exploration.level_4_primary_authority
            )
            if not has_valid_state and not has_valid_fed:
                exploration.verification_status = "ABSTAIN"
                exploration.abstention_reason = (
                    f"Controlling citations failed registry verification: {', '.join(failed_citations)}."
                )
            elif not has_valid_state:
                exploration.verification_status = "PARTIAL"
                exploration.abstention_reason = (
                    f"State-level citations failed registry verification ({', '.join(failed_citations)}); only verified federal authority remains."
                )
            else:
                exploration.verification_status = "PARTIAL"
                exploration.abstention_reason = (
                    f"Citations failed verification: {', '.join(failed_citations)}."
                )

        return exploration

    @classmethod
    def drill_down(
        cls,
        concept: str,
        action: DrillDownAction,
        jurisdiction: Optional[str] = None,
        situation: Optional[str] = None
    ) -> DrillDownResult:
        """Executes one of the 5 on-demand drill-down queries for the concept."""
        exploration = cls.explain(concept=concept, jurisdiction=jurisdiction, situation=situation)

        # Temporal drill-down handling
        if action == DrillDownAction.SHOW_TEMPORAL_CHANGE:
            if exploration.verification_status == "ABSTAIN":
                return DrillDownResult(
                    action=action,
                    title=f"Temporal Evolution & Statutory History: {exploration.concept_name}",
                    content=(
                        f"Abstain: No verified primary authority or temporal version chain is available for '{exploration.concept_name}' "
                        f"in jurisdiction {exploration.jurisdiction}. Temporal applicability cannot be established without verified enactment dates."
                    ),
                    citations=[],
                    official_sources=[]
                )

            precomputed = exploration.drill_downs.get(action)
            has_temporal_content = (
                precomputed is not None
                and len(precomputed.citations) > 0
                and not any(phrase in precomputed.content.lower() for phrase in ["no temporal", "abstain", "not tracked"])
            )

            # Query temporal_graph for version records
            graph_versions = []
            for auth in exploration.level_4_primary_authority:
                norm_c = auth.citation.upper().strip()
                if norm_c in temporal_graph.version_history:
                    graph_versions.extend(temporal_graph.version_history[norm_c])

            if not has_temporal_content and not graph_versions:
                return DrillDownResult(
                    action=action,
                    title=f"Temporal Evolution & Statutory History: {exploration.concept_name}",
                    content=(
                        f"Abstain: Temporal version history and statutory enactment records are missing or unverified for '{exploration.concept_name}'. "
                        "Point-in-time applicability cannot be determined without verified historical revisions."
                    ),
                    citations=[],
                    official_sources=[]
                )

            if graph_versions:
                lines = [f"**Temporal Version History for {exploration.concept_name}**:"]
                citations = []
                for v in graph_versions:
                    end_str = v.effective_end.isoformat() if v.effective_end else "Present"
                    lines.append(f"- **{v.version_id}** ({v.citation}): Effective {v.effective_start.isoformat()} to {end_str}. {v.text}")
                    citations.append(v.citation)

                if precomputed and precomputed.content:
                    lines.append("\n**Historical Evolution Context**:\n" + precomputed.content)
                    citations.extend(precomputed.citations)

                citations = list(dict.fromkeys(citations))
                official_sources = precomputed.official_sources if precomputed else []
                return DrillDownResult(
                    action=action,
                    title=f"Temporal Evolution & Statutory History: {exploration.concept_name}",
                    content="\n".join(lines),
                    citations=citations,
                    official_sources=official_sources
                )

            if precomputed:
                return precomputed

        # Other pre-computed drill-downs
        if action in exploration.drill_downs:
            return exploration.drill_downs[action]

        # Dynamic fallbacks
        if action == DrillDownAction.SHOW_SOURCE:
            return DrillDownResult(
                action=action,
                title=f"Verified Primary Sources: {concept}",
                content=f"Official government repository references for {concept} in {jurisdiction or 'US'}.",
                citations=[auth.citation for auth in exploration.level_4_primary_authority if auth.verification_status != "UNVERIFIED"],
                official_sources=[auth.official_portal_url for auth in exploration.level_4_primary_authority if auth.official_portal_url]
            )

        elif action == DrillDownAction.SHOW_STATUTE:
            return DrillDownResult(
                action=action,
                title=f"Controlling Statutory Authority: {concept}",
                content=f"Statutory text and elements governing {concept}.",
                citations=[auth.citation for auth in exploration.level_4_primary_authority if auth.source_type in ("STATUTE", "CONSTITUTION") and auth.verification_status != "UNVERIFIED"],
                official_sources=[auth.official_portal_url for auth in exploration.level_4_primary_authority if auth.source_type in ("STATUTE", "CONSTITUTION") and auth.official_portal_url]
            )

        elif action == DrillDownAction.SHOW_CASE:
            return DrillDownResult(
                action=action,
                title=f"Controlling Caselaw & Precedents: {concept}",
                content=f"Judicial precedents and holdings defining {concept}.",
                citations=[auth.citation for auth in exploration.level_4_primary_authority if auth.source_type == "CASELAW" and auth.verification_status != "UNVERIFIED"],
                official_sources=[auth.official_portal_url for auth in exploration.level_4_primary_authority if auth.source_type == "CASELAW" and auth.official_portal_url]
            )

        elif action == DrillDownAction.EXPLAIN_OPPOSING:
            return DrillDownResult(
                action=action,
                title=f"Opposing Interpretation & Counterarguments: {concept}",
                content=f"Adversarial and government counter-theories regarding {concept}.",
                citations=[],
                official_sources=[]
            )

        raise ValueError(f"Unknown drill down action: {action}")

    @classmethod
    def get_explanation_trace(
        cls,
        concept: str,
        jurisdiction: Optional[str] = None
    ) -> ExplanationTraceRecord:
        """Generates an auditable 10-field ExplanationTraceRecord grounded in verified authority."""
        exploration = cls.explain(concept=concept, jurisdiction=jurisdiction)
        proposition = exploration.level_5_advanced_analysis or exploration.level_3_terminology
        return ExplanationTraceEngine.trace_conclusion(
            conclusion_query=f"{concept}: {proposition[:200]}",
            jurisdiction=exploration.jurisdiction
        )

    @classmethod
    def interrogate_concept(
        cls,
        concept: str,
        query_type: InterrogativeTraceType,
        jurisdiction: Optional[str] = None,
        scenario_context: Optional[str] = None
    ) -> InterrogativeTraceResult:
        """Executes one of the 8 interrogative trace queries (WHY, SOURCE, WHEN, WHERE, etc.)."""
        trace = cls.get_explanation_trace(concept=concept, jurisdiction=jurisdiction)
        return ExplanationTraceEngine.interrogate(
            conclusion_or_record=trace,
            query_type=query_type,
            scenario_context=scenario_context,
            jurisdiction=jurisdiction
        )
