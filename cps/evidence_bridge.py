"""Controlled Evidence Manager Bridge Interface (Public-Safe Contract Boundary)."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from cps.evidence_matrix import EvidenceType, CaseEvidenceItem, EvidenceMatrixEngine, EvidentiaryMatrixEvaluation


class ExternalEvidenceContract(BaseModel):
    """Clean data contract for external Evidence Manager systems to submit evidence collections for legal audit."""
    contract_version: str = "1.0.0"
    external_case_id: str = Field(..., description="Synthetic / anonymized external case reference")
    jurisdiction: str = Field("US-WA", description="State or Federal jurisdiction e.g. US-WA, US-IL, US-OH, US-CA, US-TX, US-NY")
    cps_stage: str = Field("EMERGENCY_REMOVAL", description="Active child welfare lifecycle stage")
    items: List[Dict[str, Any]] = Field(default_factory=list, description="Array of evidence elements")


class EvidenceBridgeEngine:
    """Safely bridges external evidence manager payloads into Legal-GPT evidentiary matrices."""

    @classmethod
    def ingest_and_evaluate_contract(
        cls,
        contract: ExternalEvidenceContract
    ) -> EvidentiaryMatrixEvaluation:
        case_items: List[CaseEvidenceItem] = []

        for idx, raw_item in enumerate(contract.items, 1):
            raw_type = str(raw_item.get("type", "UNVERIFIED_ALLEGATION")).upper()

            # Map raw string type to enum
            if "EXHIBIT" in raw_type or "DOCUMENT" in raw_type:
                ev_type = EvidenceType.DOCUMENTED_EXHIBIT
            elif "ESTABLISHED" in raw_type or "ADMITTED" in raw_type:
                ev_type = EvidenceType.ESTABLISHED_FACT
            elif "DISPUTED" in raw_type or "CONTESTED" in raw_type:
                ev_type = EvidenceType.DISPUTED_FACT
            else:
                ev_type = EvidenceType.UNVERIFIED_ALLEGATION

            case_items.append(CaseEvidenceItem(
                item_id=raw_item.get("id", f"EV-{idx:03d}"),
                description=raw_item.get("description", "Unspecified factual statement"),
                evidence_type=ev_type,
                source_agency_or_person=raw_item.get("source", "Agency Caseworker"),
                date_recorded=raw_item.get("date"),
                supporting_exhibit_reference=raw_item.get("exhibit_ref"),
                statutory_element_targeted=raw_item.get("statutory_element", "Imminent Danger / Parental Fitness"),
                is_contested=raw_item.get("is_contested", True),
                notes=raw_item.get("notes")
            ))

        return EvidenceMatrixEngine.evaluate_evidence_items(
            jurisdiction=contract.jurisdiction,
            stage=contract.cps_stage,
            evidence_items=case_items
        )
