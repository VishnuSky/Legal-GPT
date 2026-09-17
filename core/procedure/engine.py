"""Procedural Pathway Engine: Maps legal narratives into structured, source-backed procedural tracks."""

from datetime import date
from typing import Dict, List, Optional, Tuple, Any

from core.procedure.models import (
    LegalTrack,
    StageDefinition,
    ProceduralPathwayInput,
    ProceduralPathwayReport,
)
from core.procedure.pathways import PathwayRegistry, ALL_STAGES


class ProceduralPathwayEngine:
    """Orchestrates procedural pathway mapping, stage identification, branching, and deadline resolution."""

    @classmethod
    def map_pathway(cls, input_data: ProceduralPathwayInput) -> ProceduralPathwayReport:
        """Analyzes input facts and narrative to generate a non-predictive procedural pathway report."""
        # 1. Determine Track
        track = input_data.track or cls._detect_track(input_data.narrative, input_data.facts)
        norm_jurisdiction = cls._normalize_jurisdiction(input_data.jurisdiction)

        # 2. Determine Current Stage
        current_stage = cls._resolve_current_stage(
            track=track,
            narrative=input_data.narrative,
            facts=input_data.facts,
            hint=input_data.current_stage_hint
        )

        # 3. Resolve Possible Next Stages
        next_stages = cls._resolve_next_stages(current_stage)

        # 4. Resolve State-Specific Authorities & Deadlines
        authorities, important_dates = cls._resolve_authorities_and_deadlines(
            stage=current_stage,
            jurisdiction=norm_jurisdiction
        )

        # 5. Required Verification Predicates
        verification_items = cls._compile_required_verification(current_stage, input_data)

        # 6. Assemble Report
        return ProceduralPathwayReport(
            track=track,
            jurisdiction=norm_jurisdiction,
            current_stage=current_stage,
            possible_next_stages=next_stages,
            authority=authorities,
            required_verification=verification_items,
            important_dates=important_dates,
            questions_to_ask=current_stage.questions_to_ask,
            documents_to_locate=current_stage.critical_documents_to_locate,
            available_review_mechanisms=current_stage.review_mechanisms,
            unknown_facts=current_stage.unknown_facts_to_investigate
        )

    @classmethod
    def _detect_track(cls, narrative: str, facts: List[str]) -> LegalTrack:
        """Classifies the legal track based on keyword density and terminology."""
        text = (narrative + " " + " ".join(facts)).lower()

        # Score tracks
        cps_terms = ["cps", "dcyf", "dcfs", "caseworker", "child welfare", "dependency", "foster", "shelter care", "custody", "removal", "parental rights", "kinship", "neglect"]
        crim_terms = ["police", "arrest", "arrested", "jail", "booking", "miranda", "prosecutor", "bail", "arraignment", "felony", "misdemeanor", "criminal", "plea", "indictment", "public defender"]
        admin_terms = ["administrative", "alj", "hearing officer", "agency", "license", "oah", "apa", "revocation", "permit", "central registry", "audit", "investigator"]
        civil_terms = ["lawsuit", "complaint", "summons", "plaintiff", "defendant", "breach of contract", "interrogatories", "deposition", "summary judgment", "eviction", "damages", "small claims"]

        cps_score = sum(text.count(t) for t in cps_terms)
        crim_score = sum(text.count(t) for t in crim_terms)
        admin_score = sum(text.count(t) for t in admin_terms)
        civil_score = sum(text.count(t) for t in civil_terms)

        # Check for highest score
        scores = [
            (LegalTrack.CPS_DEPENDENCY, cps_score),
            (LegalTrack.CRIMINAL, crim_score),
            (LegalTrack.ADMINISTRATIVE, admin_score),
            (LegalTrack.CIVIL_LITIGATION, civil_score)
        ]
        scores.sort(key=lambda x: x[1], reverse=True)

        if scores[0][1] > 0:
            return scores[0][0]

        # Default fallback
        return LegalTrack.CPS_DEPENDENCY

    @classmethod
    def _resolve_current_stage(
        cls,
        track: LegalTrack,
        narrative: str,
        facts: List[str],
        hint: Optional[str] = None
    ) -> StageDefinition:
        """Resolves the current stage within the track based on factual clues and stage hints."""
        stages = PathwayRegistry.get_by_track(track)
        if not stages:
            # Fallback
            return ALL_STAGES[0]

        # If user explicitly supplied a stage hint
        if hint:
            hint_clean = hint.strip().upper().replace(" ", "_")
            for s in stages:
                if s.stage_id == hint_clean or hint_clean in s.stage_id:
                    return s

        text = (narrative + " " + " ".join(facts)).lower()

        # Track-specific stage resolvers
        if track == LegalTrack.CPS_DEPENDENCY:
            if any(term in text for term in ["appeal", "appellate brief", "court of appeals"]):
                return cls._get_stage_or_first(stages, "CPS_APPEAL")
            if any(term in text for term in ["terminate my rights", "termination petition", "sever my parental rights", "tpr"]):
                return cls._get_stage_or_first(stages, "TERMINATION")
            if any(term in text for term in ["permanency", "6-month review", "reunification review", "trial return"]):
                return cls._get_stage_or_first(stages, "REUNIFICATION")
            if any(term in text for term in ["visitation", "family time", "supervised visits"]):
                return cls._get_stage_or_first(stages, "VISITATION")
            if any(term in text for term in ["disposition", "service plan ordered", "case plan"]):
                return cls._get_stage_or_first(stages, "DISPOSITION")
            if any(term in text for term in ["fact-finding", "adjudication trial", "found dependent"]):
                return cls._get_stage_or_first(stages, "ADJUDICATION")
            if any(term in text for term in ["shelter hearing", "shelter care", "48-hour hearing", "72-hour hearing", "temporary custody hearing"]):
                return cls._get_stage_or_first(stages, "SHELTER_HEARING")
            if any(term in text for term in ["took my", "removed my", "protective custody", "taken into custody", "yesterday", "without warrant"]):
                return cls._get_stage_or_first(stages, "CPS_REMOVAL")
            if any(term in text for term in ["petition filed", "summons served"]):
                return cls._get_stage_or_first(stages, "DEPENDENCY_PETITION")
            return cls._get_stage_or_first(stages, "CPS_INVESTIGATION")

        elif track == LegalTrack.ADMINISTRATIVE:
            if any(term in text for term in ["judicial review", "superior court appeal", "circuit court appeal"]):
                return cls._get_stage_or_first(stages, "JUDICIAL_REVIEW")
            if any(term in text for term in ["administrative appeal", "petition for review", "appeals board"]):
                return cls._get_stage_or_first(stages, "ADMIN_APPEAL")
            if any(term in text for term in ["initial order", "final order", "alj decision", "findings of fact"]):
                return cls._get_stage_or_first(stages, "ADMIN_DECISION")
            if any(term in text for term in ["hearing scheduled", "evidentiary hearing", "alj hearing"]):
                return cls._get_stage_or_first(stages, "ADMIN_HEARING")
            if any(term in text for term in ["notice of intent", "notice of proposed", "indicated finding", "opportunity to request hearing"]):
                return cls._get_stage_or_first(stages, "ADMIN_NOTICE")
            return cls._get_stage_or_first(stages, "ADMIN_INVESTIGATION")

        elif track == LegalTrack.CRIMINAL:
            if any(term in text for term in ["appeal", "appellate"]):
                return cls._get_stage_or_first(stages, "CRIMINAL_APPEAL")
            if any(term in text for term in ["sentencing", "sentenced", "presentence report", "psi"]):
                return cls._get_stage_or_first(stages, "SENTENCING")
            if any(term in text for term in ["jury trial", "bench trial", "guilty verdict", "trial scheduled"]):
                return cls._get_stage_or_first(stages, "TRIAL")
            if any(term in text for term in ["suppression motion", "discovery", "omnibus hearing", "plea offer"]):
                return cls._get_stage_or_first(stages, "PRETRIAL")
            if any(term in text for term in ["arraignment", "pleaded not guilty", "set bail", "bail hearing"]):
                return cls._get_stage_or_first(stages, "ARRAIGNMENT")
            if any(term in text for term in ["formal charges filed", "information filed", "indicted", "indictment"]):
                return cls._get_stage_or_first(stages, "CHARGING")
            if any(term in text for term in ["arrested", "in jail", "booked", "citation", "ticket"]):
                return cls._get_stage_or_first(stages, "CITATION_OR_ARREST")
            return cls._get_stage_or_first(stages, "CRIMINAL_INVESTIGATION")

        elif track == LegalTrack.CIVIL_LITIGATION:
            if any(term in text for term in ["appeal", "notice of appeal"]):
                return cls._get_stage_or_first(stages, "CIVIL_APPEAL")
            if any(term in text for term in ["judgment entered", "motion for new trial", "rule 59", "bill of costs"]):
                return cls._get_stage_or_first(stages, "CIVIL_JUDGMENT")
            if any(term in text for term in ["trial", "jury", "verdict"]):
                return cls._get_stage_or_first(stages, "CIVIL_TRIAL")
            if any(term in text for term in ["summary judgment", "rule 56"]):
                return cls._get_stage_or_first(stages, "SUMMARY_JUDGMENT")
            if any(term in text for term in ["interrogatories", "requests for production", "deposition", "discovery"]):
                return cls._get_stage_or_first(stages, "CIVIL_DISCOVERY")
            if any(term in text for term in ["answer", "rule 12", "motion to dismiss", "default judgment"]):
                return cls._get_stage_or_first(stages, "ANSWER_OR_MOTION")
            if any(term in text for term in ["served with summons", "process server", "proof of service"]):
                return cls._get_stage_or_first(stages, "SERVICE_OF_PROCESS")
            return cls._get_stage_or_first(stages, "CIVIL_COMPLAINT")

        return stages[0]

    @classmethod
    def _resolve_next_stages(cls, current_stage: StageDefinition) -> List[StageDefinition]:
        """Resolves target next stage definitions."""
        next_defs = []
        for nxt_id in current_stage.possible_next_stages:
            target = PathwayRegistry.get_by_id(nxt_id)
            if target:
                next_defs.append(target)
            else:
                # Synthetic descriptor if not a full registered stage
                next_defs.append(StageDefinition(
                    stage_id=nxt_id,
                    track=current_stage.track,
                    stage_name=nxt_id.replace("_", " ").title(),
                    order=current_stage.order + 1,
                    description=f"Potential subsequent procedural milestone: {nxt_id.replace('_', ' ').title()}."
                ))
        return next_defs

    @classmethod
    def _resolve_authorities_and_deadlines(
        cls,
        stage: StageDefinition,
        jurisdiction: str
    ) -> Tuple[List[str], List[Dict[str, Any]]]:
        """Injects state-specific statutory deadlines and primary authorities."""
        authorities = list(stage.governing_authority)
        dates: List[Dict[str, Any]] = []

        norm_j = jurisdiction.upper()

        if stage.stage_id in ("CPS_REMOVAL", "SHELTER_HEARING"):
            if "WA" in norm_j:
                dates.append({
                    "label": "Washington 72-Hour Shelter Care Hearing",
                    "description": "Court must hold shelter care hearing within 72 hours of custody, excluding weekends and court holidays.",
                    "statutory_citation": "RCW 13.34.065(1)"
                })
            elif "IL" in norm_j:
                dates.append({
                    "label": "Illinois 48-Hour Temporary Custody Hearing",
                    "description": "Minor must be brought before judicial officer within 48 hours of temporary custody, excluding weekends and court holidays.",
                    "statutory_citation": "705 ILCS 405/2-9(1)"
                })
            elif "FL" in norm_j:
                dates.append({
                    "label": "Florida 24-Hour Shelter Hearing",
                    "description": "Child cannot be held in emergency shelter longer than 24 hours without a judicial shelter hearing.",
                    "statutory_citation": "Fla. Stat. § 39.402(1)"
                })
            elif "TX" in norm_j:
                dates.append({
                    "label": "Texas 14-Day Full Adversary Hearing",
                    "description": "Full adversary hearing must be held within 14 days of emergency removal.",
                    "statutory_citation": "Tex. Fam. Code § 262.201"
                })

        if stage.stage_id == "ANSWER_OR_MOTION":
            if "WA" in norm_j:
                dates.append({
                    "label": "Washington Civil Answer Deadline",
                    "description": "Defendant must file and serve responsive pleading within 20 days of service of summons.",
                    "statutory_citation": "CR 12(a)"
                })
            elif "IL" in norm_j:
                dates.append({
                    "label": "Illinois Civil Answer Deadline",
                    "description": "Defendant must answer or move within 30 days of service.",
                    "statutory_citation": "735 ILCS 5/2-602"
                })
            else:
                dates.append({
                    "label": "Federal Rule 12 Answer Deadline",
                    "description": "Defendant must serve answer within 21 days of service of summons.",
                    "statutory_citation": "Fed. R. Civ. P. 12(a)(1)(A)(i)"
                })

        if stage.stage_id == "ADMIN_NOTICE":
            dates.append({
                "label": "Administrative Hearing Request Window",
                "description": "Written request for administrative hearing must be received within statutory window (typically 20 to 30 days from service).",
                "statutory_citation": "State Administrative Procedure Act"
            })

        if "APPEAL" in stage.stage_id:
            dates.append({
                "label": "Jurisdictional Notice of Appeal Deadline",
                "description": "Notice of Appeal must be filed within 30 days of final judgment or decree.",
                "statutory_citation": "Rules of Appellate Procedure (RAP 5.2 / FRAP 4(a))"
            })

        return authorities, dates

    @classmethod
    def _compile_required_verification(
        cls,
        stage: StageDefinition,
        input_data: ProceduralPathwayInput
    ) -> List[str]:
        """Compiles concrete factual predicates to verify before assuming this posture."""
        items = []
        for pred in stage.required_factual_predicates:
            items.append(f"Verify on official record: {pred}")

        items.append("Confirm formal cause / docket number and assigned judicial officer with court clerk")
        items.append("Confirm date and proof of service of original initiating petition or summons")
        return items

    @classmethod
    def _get_stage_or_first(cls, stages: List[StageDefinition], stage_id: str) -> StageDefinition:
        """Helper to find stage by ID or return first stage."""
        for s in stages:
            if s.stage_id == stage_id:
                return s
        return stages[0]

    @classmethod
    def _normalize_jurisdiction(cls, jurisdiction: str) -> str:
        j = jurisdiction.strip().upper()
        if j == "US":
            return "US"
        if not j.startswith("US-"):
            return f"US-{j}"
        return j
