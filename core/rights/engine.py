"""Rights Discovery Engine for Legal-GPT.

NON-ADJUDICATIVE CORE PRINCIPLE:
The engine identifies POTENTIALLY RELEVANT RIGHTS and the controlling authority supporting those rights.
It strictly distinguishes between:
  "The law recognizes this right"
and:
  "The supplied facts establish that the right was violated."

It NEVER declares or concludes that a user's rights were violated.
"""

from datetime import date
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from core.rights.models import (
    LegalBasis,
    RightCategory,
    RightDefinition,
    RightVerificationStatus,
    PotentialRightEvaluation,
    RightsDiscoveryInput,
    RightsDiscoveryResult,
)
from core.rights.registry import CANONICAL_RIGHTS, RightsRegistry
from core.temporal import TemporalEngine, TemporalValidityResult
from normalization.models import TemporalMetadata


class RightsDiscoveryEngine:
    """Discovers and evaluates potentially relevant legal rights based on facts, jurisdiction, date, and procedure."""

    @classmethod
    def discover_rights(cls, input_data: RightsDiscoveryInput) -> RightsDiscoveryResult:
        """Executes full discovery and analysis across canonical rights."""
        norm_jurisdiction = cls._normalize_jurisdiction(input_data.jurisdiction)
        all_facts_text = " ".join(input_data.facts).lower()
        narrative_all = (all_facts_text + " " + " ".join(input_data.user_allegations or [])).lower()
        target_date = input_data.date or date.today()

        potentially_relevant: List[PotentialRightEvaluation] = []
        inapplicable_or_excluded: List[PotentialRightEvaluation] = []
        conflicts: List[Dict[str, Any]] = []

        # 1. Evaluate every canonical right
        for right in CANONICAL_RIGHTS:
            eval_result = cls._evaluate_single_right(
                right=right,
                input_data=input_data,
                norm_jurisdiction=norm_jurisdiction,
                target_date=target_date,
                all_facts_text=all_facts_text,
                narrative_all=narrative_all
            )

            # Check if this right involves a constitutional-statutory tension
            if right.conflicting_procedures and eval_result.verification_status in (
                RightVerificationStatus.RECOGNIZED_POTENTIALLY_IMPLICATED,
                RightVerificationStatus.POTENTIALLY_CONFLICTING_AUTHORITY,
            ):
                conflicts.append({
                    "constitutional_right": right.right_name,
                    "authority": right.authority,
                    "conflicting_statutory_procedure": right.conflicting_procedures[0],
                    "nature_of_conflict": (
                        "Tension between constitutional requirement (judicial warrant or strict imminent bodily peril) "
                        "and state statutory summary protective custody provisions."
                    ),
                    "epistemic_note": "A conflict between a statute and the Constitution must be resolved through judicial review under the Supremacy Clause."
                })

            if eval_result.verification_status in (
                RightVerificationStatus.RECOGNIZED_POTENTIALLY_IMPLICATED,
                RightVerificationStatus.POTENTIALLY_CONFLICTING_AUTHORITY,
            ):
                potentially_relevant.append(eval_result)
            else:
                inapplicable_or_excluded.append(eval_result)

        # 2. Check explicitly asserted adversarial rights (e.g., 6th Amendment in civil, out-of-state citations)
        cls._evaluate_asserted_anomalies(
            input_data=input_data,
            norm_jurisdiction=norm_jurisdiction,
            potentially_relevant=potentially_relevant,
            inapplicable_or_excluded=inapplicable_or_excluded
        )

        # Summary counts
        summary = {
            "total_rights_analyzed": len(potentially_relevant) + len(inapplicable_or_excluded),
            "potentially_relevant": len(potentially_relevant),
            "inapplicable_or_excluded": len(inapplicable_or_excluded),
            "conflicts_identified": len(conflicts),
        }

        return RightsDiscoveryResult(
            input_context=input_data,
            potentially_relevant_rights=potentially_relevant,
            inapplicable_or_excluded_rights=inapplicable_or_excluded,
            constitutional_statutory_conflicts=conflicts,
            summary_counts=summary
        )

    @classmethod
    def _evaluate_single_right(
        cls,
        right: RightDefinition,
        input_data: RightsDiscoveryInput,
        norm_jurisdiction: str,
        target_date: date,
        all_facts_text: str,
        narrative_all: str
    ) -> PotentialRightEvaluation:
        """Evaluates a single canonical right against the user input context."""
        effective_range_str = cls._format_effective_date(right)

        # 1. JURISDICTION CHECK
        if right.jurisdiction != "US" and right.jurisdiction != norm_jurisdiction:
            epistemic = (
                f"The law recognizes '{right.right_name}' under {right.authority}, but that authority belongs "
                f"to jurisdiction {right.jurisdiction}, which does not control in {norm_jurisdiction}."
            )
            return PotentialRightEvaluation(
                right_name=right.right_name,
                category=right.category,
                legal_basis=right.legal_basis,
                authority=right.authority,
                authority_tier=right.authority_tier,
                jurisdiction=right.jurisdiction,
                effective_date=effective_range_str,
                procedural_context=input_data.procedure,
                required_facts=right.required_facts,
                known_exceptions=right.known_exceptions,
                counterarguments=right.counterarguments,
                verification_status=RightVerificationStatus.NOT_APPLICABLE_JURISDICTION_MISMATCH,
                epistemic_distinction=epistemic,
                facts_implicated=[],
                exceptions_triggered=[],
                applicability_rationale=f"Jurisdiction mismatch: Statute is enacted in {right.jurisdiction}, but target jurisdiction is {norm_jurisdiction}.",
                literacy_concept_id=right.literacy_concept_id
            )

        # 2. TEMPORAL CHECK
        temporal_meta = TemporalMetadata(
            effective_date=right.effective_date_start,
            repealed_date=right.effective_date_end,
            version_id=right.right_id
        )
        temp_res: TemporalValidityResult = TemporalEngine.check_validity_on_date(temporal_meta, target_date)
        if not temp_res.is_valid_on_date:
            epistemic = (
                f"The authority '{right.authority}' was not legally valid on {target_date.isoformat()}: {temp_res.reason}"
            )
            return PotentialRightEvaluation(
                right_name=right.right_name,
                category=right.category,
                legal_basis=right.legal_basis,
                authority=right.authority,
                authority_tier=right.authority_tier,
                jurisdiction=right.jurisdiction,
                effective_date=effective_range_str,
                procedural_context=input_data.procedure,
                required_facts=right.required_facts,
                known_exceptions=right.known_exceptions,
                counterarguments=right.counterarguments,
                verification_status=RightVerificationStatus.NOT_APPLICABLE_TEMPORAL_INVALID,
                epistemic_distinction=epistemic,
                facts_implicated=[],
                exceptions_triggered=[],
                applicability_rationale=temp_res.reason,
                literacy_concept_id=right.literacy_concept_id
            )

        # 3. PROCEDURAL CONTEXT MATCH
        context_match = False
        norm_proc = input_data.procedure.upper()
        if not right.procedural_context or norm_proc in right.procedural_context or norm_proc == "ALL":
            context_match = True

        # 4. FACTUAL PREDICATE MATCHING
        facts_implicated = cls._match_required_facts(right, all_facts_text, narrative_all)
        has_factual_basis = len(facts_implicated) > 0 or context_match

        # 5. EXCEPTIONS TRIGGER CHECK
        exceptions_triggered = cls._detect_exceptions(right, all_facts_text)

        # 6. STATUS DETERMINATION
        if exceptions_triggered:
            status = RightVerificationStatus.POTENTIALLY_BARRED_EXCEPTION_APPLIES
            rationale = (
                f"Right is recognized under controlling law, but supplied facts explicitly indicate circumstances "
                f"triggering a recognized legal exception: {'; '.join(exceptions_triggered)}."
            )
        elif not has_factual_basis and len(right.required_facts) > 0:
            status = RightVerificationStatus.RECOGNIZED_FACTS_INSUFFICIENT
            rationale = (
                f"The law recognizes this right, but the supplied facts do not establish the necessary "
                f"factual predicates ({'; '.join(right.required_facts)})."
            )
        elif right.conflicting_procedures and norm_proc in ("EMERGENCY_REMOVAL", "INVESTIGATION"):
            status = RightVerificationStatus.POTENTIALLY_CONFLICTING_AUTHORITY
            rationale = (
                f"Right recognized under constitutional Tier-0 authority, but state administrative procedures "
                f"may conflict with full judicial warrant requirements."
            )
        else:
            status = RightVerificationStatus.RECOGNIZED_POTENTIALLY_IMPLICATED
            rationale = (
                f"Right recognized under controlling authority in {right.jurisdiction} and potentially implicated "
                f"by procedural posture ({input_data.procedure}) and supplied facts."
            )

        # 7. CRITICAL EPISTEMIC SEPARATION TEXT
        epistemic = (
            f"The law recognizes the '{right.right_name}' under {right.authority}. "
            f"Legal-GPT identifies this as a potentially relevant right for legal research. "
            f"However, Legal-GPT does NOT adjudicate whether this right was violated. "
            f"A legal violation is a judicial finding requiring evidentiary proof, judicial credibility determinations, "
            f"and resolving potential affirmative defenses (such as: {', '.join(right.known_exceptions[:2])})."
        )

        return PotentialRightEvaluation(
            right_name=right.right_name,
            category=right.category,
            legal_basis=right.legal_basis,
            authority=right.authority,
            authority_tier=right.authority_tier,
            jurisdiction=right.jurisdiction,
            effective_date=effective_range_str,
            procedural_context=input_data.procedure,
            required_facts=right.required_facts,
            known_exceptions=right.known_exceptions,
            counterarguments=right.counterarguments,
            verification_status=status,
            epistemic_distinction=epistemic,
            facts_implicated=facts_implicated,
            exceptions_triggered=exceptions_triggered,
            applicability_rationale=rationale,
            literacy_concept_id=right.literacy_concept_id
        )

    @classmethod
    def _evaluate_asserted_anomalies(
        cls,
        input_data: RightsDiscoveryInput,
        norm_jurisdiction: str,
        potentially_relevant: List[PotentialRightEvaluation],
        inapplicable_or_excluded: List[PotentialRightEvaluation]
    ) -> None:
        """Evaluates adversarial user assertions (e.g. 6th Amendment criminal counsel in civil CPS, out-of-state statutes)."""
        narrative_lower = (" ".join(input_data.facts) + " " + " ".join(input_data.user_allegations or []) + " " + " ".join(input_data.asserted_rights or [])).lower()

        # ADVERSARIAL CASE 1: 6th Amendment Criminal Right to Counsel in Civil Matter
        if "sixth amendment" in narrative_lower or "6th amendment" in narrative_lower:
            epistemic = (
                "The Sixth Amendment guarantees the right to counsel in 'all criminal prosecutions.' "
                "Child dependency and child welfare actions are civil proceedings, so the Sixth Amendment "
                "does not directly apply. However, counsel in dependency is protected either by the Fourteenth "
                "Amendment Due Process Clause (Lassiter) or state statutory guarantees."
            )
            inapplicable_or_excluded.append(PotentialRightEvaluation(
                right_name="Sixth Amendment Right to Counsel (Criminal)",
                category=RightCategory.COUNSEL_RIGHTS,
                legal_basis=LegalBasis.CONSTITUTIONAL,
                authority="U.S. Const. amend. VI; Lassiter v. Dept. of Social Services, 452 U.S. 18 (1981)",
                authority_tier="TIER_0",
                jurisdiction="US",
                effective_date="1791-12-15 to Present",
                procedural_context=input_data.procedure,
                required_facts=["Formal criminal prosecution or custodial interrogation on criminal charges"],
                known_exceptions=["Civil proceedings, including dependency, termination, and custody"],
                counterarguments=["Matter is civil in nature; Sixth Amendment is inapplicable to non-criminal proceedings"],
                verification_status=RightVerificationStatus.RECOGNIZED_FACTS_INSUFFICIENT,
                epistemic_distinction=epistemic,
                facts_implicated=[],
                exceptions_triggered=["Civil dependency matter exempt from 6th Amendment criminal scope"],
                applicability_rationale="Sixth Amendment applies exclusively to criminal prosecutions, not civil dependency cases."
            ))

        # ADVERSARIAL CASE 2: Free Speech Retaliation Asserted Without Factual Basis
        if "first amendment" in narrative_lower or "freedom of speech" in narrative_lower:
            has_speech_facts = any(k in narrative_lower for k in ["criticized", "spoke out", "post", "facebook", "petition", "retaliation"])
            if not has_speech_facts:
                epistemic = (
                    "The First Amendment protects freedom of speech and prohibits state retaliation for protected expression. "
                    "However, the supplied narrative contains zero factual allegations involving speech, criticism, or retaliatory motives."
                )
                inapplicable_or_excluded.append(PotentialRightEvaluation(
                    right_name="First Amendment Protection Against Retaliation",
                    category=RightCategory.CONSTITUTIONAL_RIGHTS,
                    legal_basis=LegalBasis.CONSTITUTIONAL,
                    authority="U.S. Const. amend. I; Hartman v. Moore, 547 U.S. 250 (2006)",
                    authority_tier="TIER_0",
                    jurisdiction="US",
                    effective_date="1791-12-15 to Present",
                    procedural_context=input_data.procedure,
                    required_facts=["Plaintiff engaged in constitutionally protected speech", "State took adverse action motivated by protected speech"],
                    known_exceptions=["Independent, non-retaliatory safety justification exists"],
                    counterarguments=["Adverse action based strictly on objective child welfare risk, not speech"],
                    verification_status=RightVerificationStatus.RECOGNIZED_FACTS_INSUFFICIENT,
                    epistemic_distinction=epistemic,
                    facts_implicated=[],
                    exceptions_triggered=[],
                    applicability_rationale="First Amendment recognized in law, but user assertion is unsupported by factual predicates."
                ))

    @classmethod
    def _match_required_facts(cls, right: RightDefinition, facts_text: str, narrative_all: str) -> List[str]:
        """Identifies which required facts find support in the user narrative."""
        implicated = []
        low = narrative_all.lower()

        # Keyword heuristics for required facts
        kw_map = {
            "Parent-child": ["daughter", "son", "child", "children", "mother", "father", "parent", "kid", "baby"],
            "State interference": ["cps", "dcyf", "dcfs", "caseworker", "police", "officer", "removed", "took", "custody", "investigation"],
            "warrantless": ["no warrant", "without warrant", "without a warrant", "didn't have a warrant", "forced their way", "entered"],
            "residence": ["home", "house", "apartment", "residence", "door", "inside"],
            "indigent": ["indigent", "poor", "cannot afford", "public defender", "no money", "low income"],
            "relative": ["grandma", "grandmother", "grandpa", "aunt", "uncle", "relative", "kinship", "sister", "brother"],
            "disability": ["disabled", "disability", "autism", "bipolar", "depression", "wheelchair", "accommodation", "mental illness"],
            "indian": ["tribe", "tribal", "indian", "icwa", "native american", "reservation"],
            "notice": ["notice", "served", "summons", "letter", "papers", "call", "told"],
            "hearing": ["court", "judge", "hearing", "docket", "bench", "trial"]
        }

        for rf in right.required_facts:
            for kw_key, terms in kw_map.items():
                if kw_key.lower() in rf.lower():
                    if any(t in low for t in terms):
                        implicated.append(rf)
                        break

        return list(dict.fromkeys(implicated))

    @classmethod
    def _detect_exceptions(cls, right: RightDefinition, facts_text: str) -> List[str]:
        """Detects whether supplied facts trigger any recognized exceptions."""
        triggered = []
        low = facts_text.lower()

        # Exigent circumstances / emergency aid exception triggers
        exigency_keywords = [
            "screaming", "screaming inside", "gunshot", "bleeding", "active fire",
            "medical emergency", "unconscious", "immediate danger", "threat of death",
            "overdose", "physical assault in progress"
        ]
        if any(e in low for e in exigency_keywords):
            for exc in right.known_exceptions:
                if any(w in exc.lower() for w in ["exigent", "imminent", "emergency", "danger"]):
                    triggered.append(f"{exc} (Triggered by facts mentioning immediate physical peril/screaming)")

        # Consent exception
        if any(c in low for c in ["i let them in", "invited them in", "gave consent", "signed consent"]):
            for exc in right.known_exceptions:
                if "consent" in exc.lower():
                    triggered.append(f"{exc} (Triggered by facts mentioning voluntary consent)")

        # Court holiday / weekend deadline extension
        if any(h in low for h in ["weekend", "saturday", "sunday", "holiday", "thanksgiving", "christmas"]):
            for exc in right.known_exceptions:
                if any(w in exc.lower() for w in ["saturday", "sunday", "holiday"]):
                    triggered.append(f"{exc} (Triggered by facts referencing weekend or court holiday)")

        return triggered

    @classmethod
    def _normalize_jurisdiction(cls, jurisdiction: str) -> str:
        """Normalizes jurisdiction string to ISO/FIPS format (e.g. 'WA' -> 'US-WA')."""
        j = jurisdiction.strip().upper()
        if j == "US":
            return "US"
        if not j.startswith("US-"):
            return f"US-{j}"
        return j

    @classmethod
    def _format_effective_date(cls, right: RightDefinition) -> str:
        """Formats the effective date range into a readable string."""
        if not right.effective_date_start and not right.effective_date_end:
            return "Historical Precedent / Active"
        start_str = right.effective_date_start.isoformat() if right.effective_date_start else "Historical"
        end_str = right.effective_date_end.isoformat() if right.effective_date_end else "Present"
        return f"{start_str} to {end_str}"
