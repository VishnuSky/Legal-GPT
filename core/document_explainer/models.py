"""Data models for the Legal-GPT Document Explainer Module."""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    SUMMONS_AND_COMPLAINT = "SUMMONS_AND_COMPLAINT"
    DEPENDENCY_PETITION = "DEPENDENCY_PETITION"
    TEMPORARY_CUSTODY_ORDER = "TEMPORARY_CUSTODY_ORDER"
    NOTICE_OF_INVESTIGATION = "NOTICE_OF_INVESTIGATION"
    SUBPOENA = "SUBPOENA"
    MOTION_TO_TERMINATE_PARENTAL_RIGHTS = "MOTION_TO_TERMINATE_PARENTAL_RIGHTS"
    PROTECTIVE_ORDER = "PROTECTIVE_ORDER"
    UNKNOWN = "UNKNOWN"


class DeadlineItem(BaseModel):
    """A critical procedural deadline identified in or applicable to the document."""
    name: str
    timeframe: str
    citation: str
    consequence_of_missing: str


class RightItem(BaseModel):
    """A fundamental legal or procedural right triggered by this document."""
    right_name: str
    description: str
    authority: str


class ActionItem(BaseModel):
    """A concrete, prioritized next action for the recipient."""
    step: str
    priority: str = Field("IMPORTANT", description="'URGENT', 'IMPORTANT', or 'ROUTINE'")
    description: str


class DocumentExplanationRequest(BaseModel):
    """Request payload for analyzing and explaining a legal document."""
    document_type: Optional[str] = Field(None, description="Known document type e.g. 'summons_and_complaint', 'dependency_petition'")
    document_text: Optional[str] = Field(None, description="Text excerpt or content of the legal document")
    jurisdiction: Optional[str] = Field("US", description="Controlling jurisdiction code (e.g. 'US-WA', 'IL', 'US')")
    literacy_level: Optional[int] = Field(1, description="1 = Plain English, 2 = Practical Explanation, 3 = Legal Terminology")


class DocumentExplanationReport(BaseModel):
    """Structured report explaining the purpose, deadlines, rights, and actions for a document."""
    document_title: str
    document_category: str
    jurisdiction: str
    issuing_body: str
    purpose_summary: str
    literacy_level: int
    plain_english_explanation: str
    practical_explanation: str
    legal_terminology_explanation: str
    deadlines: List[DeadlineItem] = Field(default_factory=list)
    rights: List[RightItem] = Field(default_factory=list)
    consequences_of_inaction: List[str] = Field(default_factory=list)
    recommended_actions: List[ActionItem] = Field(default_factory=list)
    related_concept_ids: List[str] = Field(default_factory=list)
    disclaimer: str = (
        "LEGAL INFORMATION ONLY — NOT LEGAL ADVICE: This document breakdown is generated for informational and "
        "legal literacy purposes only. It does not constitute legal advice and does not establish an attorney-client relationship. "
        "Consult a qualified attorney or your local legal aid organization regarding your specific case deadlines."
    )
    verification_status: str = "VERIFIED"
