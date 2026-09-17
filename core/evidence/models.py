"""Data models and schemas for the Public-Data-Safe Legal Evidence Bridge."""

from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EpistemicClassification(str, Enum):
    """The seven required epistemic classifications for legal facts and evidence."""
    FACT = "FACT"
    ALLEGATION = "ALLEGATION"
    DOCUMENTED_FACT = "DOCUMENTED_FACT"
    TESTIMONY = "TESTIMONY"
    OPINION = "OPINION"
    INFERENCE = "INFERENCE"
    UNKNOWN = "UNKNOWN"


class EvidenceVerificationState(str, Enum):
    """Verification provenance state of an evidence record."""
    VERIFIED_PRIMARY_DOCUMENT = "VERIFIED_PRIMARY_DOCUMENT"
    CORROBORATED_BY_RECORDS = "CORROBORATED_BY_RECORDS"
    UNVERIFIED_ASSERTION = "UNVERIFIED_ASSERTION"
    CONTESTED_OR_DISPUTED = "CONTESTED_OR_DISPUTED"
    UNKNOWN_INSUFFICIENT_PROVENANCE = "UNKNOWN_INSUFFICIENT_PROVENANCE"


class EvidenceRecord(BaseModel):
    """Public-data-safe record describing an item of evidence or documentary exhibit.
    
    CRITICAL PRIVACY MANDATE:
    This schema operates on metadata, document categories, and structural factual statements.
    It does NOT store private case records, actual sensitive files, or confidential PII.
    """
    id: str = Field(..., description="Unique evidence identifier, e.g. EV-001")
    description: str = Field(..., description="Factual description of the document or exhibit")
    source_type: str = Field(..., description="Document or source type, e.g. NOTICE_DOCUMENT, POLICE_REPORT, MEDICAL_RECORD")
    date: Optional[str] = Field(None, description="Date of document or event creation")
    author: Optional[str] = Field(None, description="Authoring role, agency, or official title, e.g. Caseworker, Physician, Officer")
    custodian: Optional[str] = Field(None, description="Agency or institutional custodian of record")
    relevance: str = Field(..., description="Explanation of legal relevance to the pending matter")
    associated_issue: str = Field(..., description="Legal issue or statutory claim this evidence relates to")
    verification_state: EvidenceVerificationState = EvidenceVerificationState.UNVERIFIED_ASSERTION
    classification: EpistemicClassification = EpistemicClassification.ALLEGATION


class LegalElement(BaseModel):
    """Definition of a statutory or constitutional legal element requiring evidentiary proof."""
    element_id: str
    element_name: str
    governing_authority: str
    authority_tier: str = "TIER_0"
    required_proof_standard: str
    standard_evidentiary_predicates: List[str] = Field(default_factory=list)
    default_missing_elements: List[str] = Field(default_factory=list)
    standard_research_questions: List[str] = Field(default_factory=list)


class LegalBridgeLink(BaseModel):
    """The 6-stage bridge connecting evidence to research questions:
    Evidence -> Fact -> Legal Element -> Authority -> Missing Evidence -> Research Question
    """
    evidence: EvidenceRecord
    fact_statement: str
    legal_element: str
    authority: str
    missing_evidence: List[str] = Field(default_factory=list)
    research_questions: List[str] = Field(default_factory=list)
    epistemic_classification: EpistemicClassification


class EvidenceBridgeEvaluation(BaseModel):
    """Comprehensive evaluation returned by the Legal Evidence Bridge."""
    case_reference: str
    jurisdiction: str
    evidence_records: List[EvidenceRecord] = Field(default_factory=list)
    bridge_links: List[LegalBridgeLink] = Field(default_factory=list)
    missing_evidence_summary: List[Dict[str, Any]] = Field(default_factory=list)
    research_questions_summary: List[str] = Field(default_factory=list)
    classification_counts: Dict[str, int] = Field(default_factory=dict)
    public_data_safety_notice: str = (
        "PUBLIC-DATA-SAFE NOTICE: This evidence evaluation operates strictly upon structural metadata, "
        "document types, and legal issue mapping. Legal-GPT does not store or process confidential case evidence, "
        "unredacted medical files, or private individual records."
    )
