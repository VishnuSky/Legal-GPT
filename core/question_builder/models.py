"""Data models for the Legal-GPT Question Builder Module."""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TargetRecipient(str, Enum):
    ATTORNEY = "ATTORNEY"
    CASEWORKER = "CASEWORKER"
    COURT = "COURT"
    AGENCY_SUPERVISOR = "AGENCY_SUPERVISOR"
    INVESTIGATOR = "INVESTIGATOR"
    ALL = "ALL"


class QuestionPriorityTier(int, Enum):
    TIER_1_RIGHTS = 1
    TIER_2_DEADLINES = 2
    TIER_3_PROCEDURAL_STATUS = 3
    TIER_4_EVIDENCE_DOCUMENTATION = 4


class QuestionItem(BaseModel):
    """An individual tactical question for a legal meeting or hearing."""
    id: str = Field(..., description="Unique question identifier")
    target_recipient: str = Field(..., description="'ATTORNEY', 'CASEWORKER', 'COURT', etc.")
    priority_tier: int = Field(..., description="1=Rights, 2=Deadlines, 3=Procedure, 4=Documentation")
    category: str = Field(..., description="'RIGHTS', 'DEADLINES', 'PROCEDURE', or 'DOCUMENTATION'")
    question_text: str = Field(..., description="Verbatim phrasing to ask")
    rationale: str = Field(..., description="Why this question is legally critical")
    statutory_hook: Optional[str] = Field(None, description="Controlling constitutional or statutory reference")
    expected_response_type: str = Field("Verbal explanation", description="Expected form of answer or record")


class QuestionBuilderRequest(BaseModel):
    """Request payload for generating customized legal questions."""
    situation: str = Field(..., description="e.g. 'emergency_removal', 'shelter_hearing', 'service_plan', 'arraignment'")
    target_recipient: Optional[str] = Field("ATTORNEY", description="'ATTORNEY', 'CASEWORKER', 'COURT', or 'ALL'")
    jurisdiction: Optional[str] = Field("US", description="Controlling jurisdiction code (e.g. 'WA', 'IL', 'US')")
    user_role: Optional[str] = Field("parent", description="'parent', 'self_represented', 'advocate', 'client'")


class QuestionBuilderReport(BaseModel):
    """Complete customized question and document checklist report."""
    situation: str
    target_recipient: str
    jurisdiction: str
    user_role: str
    prioritized_questions: List[QuestionItem] = Field(default_factory=list)
    documents_to_request: List[str] = Field(default_factory=list)
    documents_to_bring: List[str] = Field(default_factory=list)
    tactical_tips: List[str] = Field(default_factory=list)
    summary: str = ""
