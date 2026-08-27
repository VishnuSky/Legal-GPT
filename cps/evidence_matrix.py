"""Fact vs Allegation vs Documented Exhibit Matrix: Evidentiary Sufficiency Evaluation."""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class EvidenceType(str, Enum):
    UNVERIFIED_ALLEGATION = "UNVERIFIED_ALLEGATION"  # Agency assertion without supporting documentary proof
    DISPUTED_FACT = "DISPUTED_FACT"                  # Contested factual assertion requiring evidentiary hearing
    ESTABLISHED_FACT = "ESTABLISHED_FACT"            # Stipulated, admitted, or court-found fact
    DOCUMENTED_EXHIBIT = "DOCUMENTED_EXHIBIT"        # Admissible documentary or physical evidence with provenance


class EvidentiarySufficiencyLevel(str, Enum):
    DEFICIENT = "DEFICIENT"          # Lacks admissible supporting evidence
    MARGINAL = "MARGINAL"            # Bare uncorroborated hearsay or contested caseworker notes
    SUFFICIENT = "SUFFICIENT"        # Corroborated by objective documented exhibits
    OVERWHELMING = "OVERWHELMING"    # Multi-source documented proof meeting clear and convincing standard


class CaseEvidenceItem(BaseModel):
    item_id: str
    description: str
    evidence_type: EvidenceType
    source_agency_or_person: str
    date_recorded: Optional[str] = None
    supporting_exhibit_reference: Optional[str] = None
    statutory_element_targeted: str  # e.g., "Imminent Physical Harm", "Substance Impairment", "Reasonable Efforts"
    is_contested: bool = False
    notes: Optional[str] = None


class EvidentiaryGap(BaseModel):
    statutory_element: str
    burden_of_proof_required: str
    allegation_text: str
    missing_evidence_description: str
    rebuttal_strategy: str


class EvidentiaryMatrixEvaluation(BaseModel):
    case_summary: str
    jurisdiction: str
    burden_of_proof: str
    total_items_analyzed: int
    unverified_allegations_count: int
    disputed_facts_count: int
    documented_exhibits_count: int
    sufficiency_rating: EvidentiarySufficiencyLevel
    evidentiary_gaps: List[EvidentiaryGap] = Field(default_factory=list)
    strategic_recommendations: List[str] = Field(default_factory=list)


class EvidenceMatrixEngine:
    """Evaluates case narratives to separate unverified caseworker allegations from admissible exhibits."""

    @classmethod
    def evaluate_evidence_items(
        cls,
        jurisdiction: str,
        stage: str,
        evidence_items: List[CaseEvidenceItem],
        burden_of_proof: str = "Preponderance of the Evidence"
    ) -> EvidentiaryMatrixEvaluation:
        allegations = [i for i in evidence_items if i.evidence_type == EvidenceType.UNVERIFIED_ALLEGATION]
        disputed = [i for i in evidence_items if i.evidence_type == EvidenceType.DISPUTED_FACT]
        exhibits = [i for i in evidence_items if i.evidence_type == EvidenceType.DOCUMENTED_EXHIBIT]
        established = [i for i in evidence_items if i.evidence_type == EvidenceType.ESTABLISHED_FACT]

        gaps: List[EvidentiaryGap] = []
        recommendations: List[str] = []

        # Analyze unverified allegations for missing proof
        for item in allegations:
            gaps.append(EvidentiaryGap(
                statutory_element=item.statutory_element_targeted,
                burden_of_proof_required=burden_of_proof,
                allegation_text=item.description,
                missing_evidence_description=(
                    f"Agency relies on uncorroborated assertion '{item.description}' without objective medical, "
                    f"forensic, drug screen, or law enforcement exhibit."
                ),
                rebuttal_strategy=(
                    "File Motion to Preclude hearsay assertion or object under evidence rules; demand agency caseworker "
                    "produce original documentation and direct percipient witness testimony."
                )
            ))

        # Determine overall sufficiency
        total_items = len(evidence_items)
        exhibit_ratio = (len(exhibits) + len(established)) / max(1, total_items)

        if exhibit_ratio < 0.25 and len(allegations) > 0:
            sufficiency = EvidentiarySufficiencyLevel.DEFICIENT
            recommendations.append("Case against parent rests substantially on unverified allegations; strong basis for motion to dismiss or contest removal.")
        elif exhibit_ratio < 0.60:
            sufficiency = EvidentiarySufficiencyLevel.MARGINAL
            recommendations.append("Agency evidence has critical factual gaps; cross-examination and discovery requests should target lack of independent corroboration.")
        elif exhibit_ratio < 0.85:
            sufficiency = EvidentiarySufficiencyLevel.SUFFICIENT
            recommendations.append("Agency has documented exhibits for key claims; defense must focus on mitigating evidence, service completion, and kinship safety plan.")
        else:
            sufficiency = EvidentiarySufficiencyLevel.OVERWHELMING
            recommendations.append("Extensive documentary exhibits exist; focus on alternative disposition, relative guardianship, and tailored service plan.")

        summary = (
            f"Evidentiary Analysis for {jurisdiction} ({stage}): Analyzed {total_items} factual items. "
            f"Found {len(allegations)} unverified allegations, {len(disputed)} disputed facts, and {len(exhibits)} documented exhibits. "
            f"Overall Agency Evidentiary Sufficiency: {sufficiency.value}."
        )

        return EvidentiaryMatrixEvaluation(
            case_summary=summary,
            jurisdiction=jurisdiction,
            burden_of_proof=burden_of_proof,
            total_items_analyzed=total_items,
            unverified_allegations_count=len(allegations),
            disputed_facts_count=len(disputed),
            documented_exhibits_count=len(exhibits),
            sufficiency_rating=sufficiency,
            evidentiary_gaps=gaps,
            strategic_recommendations=recommendations
        )
