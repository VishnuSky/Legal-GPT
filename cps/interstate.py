"""Interstate Child Custody (UCCJEA) and Interstate Placement (ICPC) Engine."""

from typing import List, Optional
from pydantic import BaseModel, Field


class UCCJEAEvaluation(BaseModel):
    home_state: Optional[str] = None
    has_home_state_jurisdiction: bool
    is_emergency_jurisdiction: bool
    exclusive_continuing_jurisdiction_state: Optional[str] = None
    icpc_compliance_required: bool
    statutory_citations: List[str] = Field(default_factory=list)
    analysis: str


class InterstateEngine:
    @classmethod
    def evaluate_interstate_custody(
        cls,
        child_current_state: str,
        months_in_current_state: int,
        prior_orders_state: Optional[str] = None,
        is_emergency_protection_needed: bool = False,
        is_interstate_foster_placement: bool = False
    ) -> UCCJEAEvaluation:
        citations = []
        state_curr = child_current_state.upper()

        if state_curr == "WA":
            citations.append("RCW 26.27 (Uniform Child Custody Jurisdiction and Enforcement Act)")
        elif state_curr == "IL":
            citations.append("750 ILCS 35 (Uniform Child-Custody Jurisdiction and Enforcement Act)")
        elif state_curr == "OH":
            citations.append("ORC Chapter 3127 (Uniform Child Custody Jurisdiction and Enforcement Act)")

        if is_interstate_foster_placement:
            citations.append("Interstate Compact on the Placement of Children (ICPC)")

        # UCCJEA 6-month rule
        is_home_state = months_in_current_state >= 6

        if is_emergency_protection_needed:
            analysis = (
                f"Temporary Emergency Jurisdiction exists in {state_curr} under UCCJEA § 204 to protect the child "
                f"from immediate mistreatment or abuse. However, orders are temporary until communication with the "
                f"home state court ({prior_orders_state or 'original home state'})."
            )
            return UCCJEAEvaluation(
                home_state=state_curr if is_home_state else prior_orders_state,
                has_home_state_jurisdiction=is_home_state,
                is_emergency_jurisdiction=True,
                exclusive_continuing_jurisdiction_state=prior_orders_state,
                icpc_compliance_required=is_interstate_foster_placement,
                statutory_citations=citations,
                analysis=analysis
            )

        if prior_orders_state and prior_orders_state != state_curr and not is_home_state:
            analysis = (
                f"{prior_orders_state} retains Exclusive, Continuing Jurisdiction under UCCJEA § 202 until "
                f"that court determines neither child nor parents have a significant connection or reside there."
            )
            return UCCJEAEvaluation(
                home_state=prior_orders_state,
                has_home_state_jurisdiction=False,
                is_emergency_jurisdiction=False,
                exclusive_continuing_jurisdiction_state=prior_orders_state,
                icpc_compliance_required=is_interstate_foster_placement,
                statutory_citations=citations,
                analysis=analysis
            )

        analysis = (
            f"{state_curr} qualifies as the child's Home State under UCCJEA § 201 because the child has resided "
            f"in {state_curr} for {months_in_current_state} months (>= 6 months required)."
        )
        return UCCJEAEvaluation(
            home_state=state_curr,
            has_home_state_jurisdiction=True,
            is_emergency_jurisdiction=False,
            exclusive_continuing_jurisdiction_state=state_curr,
            icpc_compliance_required=is_interstate_foster_placement,
            statutory_citations=citations,
            analysis=analysis
        )
