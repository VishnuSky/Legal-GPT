"""Legal Literacy Engine: Multi-Level Concept Breakdown & On-Demand Drill-Down Actions."""

from typing import Optional, Dict, Any, List
from core.literacy.models import (
    LiteracyLevel,
    DrillDownAction,
    DrillDownResult,
    LegalConceptExploration,
    PrimaryAuthorityReference,
)
from core.literacy.registry import LegalConceptRegistry
from core.temporal_graph import temporal_graph
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
        """Retrieves or synthesizes a 5-level exploration for a legal concept."""
        exploration = LegalConceptRegistry.get_concept(
            concept_query=concept,
            jurisdiction=jurisdiction,
            situation=situation
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
        
        # Check if pre-computed in exploration
        if action in exploration.drill_downs:
            return exploration.drill_downs[action]

        # Fallback dynamic drill-down resolution
        if action == DrillDownAction.SHOW_SOURCE:
            return DrillDownResult(
                action=action,
                title=f"Verified Primary Sources: {concept}",
                content=f"Official government repository references for {concept} in {jurisdiction or 'US'}.",
                citations=[auth.citation for auth in exploration.level_4_primary_authority],
                official_sources=[auth.official_portal_url for auth in exploration.level_4_primary_authority]
            )

        elif action == DrillDownAction.SHOW_STATUTE:
            return DrillDownResult(
                action=action,
                title=f"Controlling Statutory Authority: {concept}",
                content=f"Statutory text and elements governing {concept}.",
                citations=[auth.citation for auth in exploration.level_4_primary_authority if auth.source_type in ("STATUTE", "CONSTITUTION")],
                official_sources=[]
            )

        elif action == DrillDownAction.SHOW_CASE:
            return DrillDownResult(
                action=action,
                title=f"Controlling Caselaw & Precedents: {concept}",
                content=f"Judicial precedents and holdings defining {concept}.",
                citations=[auth.citation for auth in exploration.level_4_primary_authority if auth.source_type == "CASELAW"],
                official_sources=[]
            )

        elif action == DrillDownAction.EXPLAIN_OPPOSING:
            return DrillDownResult(
                action=action,
                title=f"Opposing Interpretation & Counterarguments: {concept}",
                content=f"Adversarial and government counter-theories regarding {concept}.",
                citations=[],
                official_sources=[]
            )

        elif action == DrillDownAction.SHOW_TEMPORAL_CHANGE:
            return DrillDownResult(
                action=action,
                title=f"Temporal Evolution & Statutory History: {concept}",
                content=f"Point-in-time amendments and historical evolution of {concept}.",
                citations=[],
                official_sources=[]
            )

        raise ValueError(f"Unknown drill down action: {action}")
