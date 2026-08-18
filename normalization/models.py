"""Canonical Legal Document Models and Data Structures."""

from datetime import date, datetime, timezone
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
import hashlib


class TemporalMetadata(BaseModel):
    enacted_date: Optional[date] = None
    effective_date: Optional[date] = None
    repealed_date: Optional[date] = None
    last_amended_date: Optional[date] = None
    version_id: Optional[str] = None
    is_current: bool = True


class AuthorityScore(BaseModel):
    tier: Literal["TIER_0", "TIER_1", "TIER_2", "TIER_3", "TIER_4", "TIER_5"]
    weight: float = Field(..., ge=0.0, le=1.0)
    official_source: bool = True
    provider_name: str


class Citation(BaseModel):
    raw_citation: str
    normalized_citation: str
    jurisdiction: str
    document_type: Literal["statute", "constitution", "regulation", "case_opinion", "court_rule", "agency_policy", "form"]
    title: Optional[str] = None
    section_or_pinpoint: Optional[str] = None
    verified: bool = False
    source_url: Optional[str] = None
    authority_tier: Optional[str] = None


class LegalChunk(BaseModel):
    chunk_id: str
    document_id: str
    chunk_type: Literal["chapter", "section", "subsection", "holding", "reasoning", "syllabus", "policy_rule", "procedure", "form_field"]
    heading: Optional[str] = None
    text: str
    tokens_estimate: int = 0
    hierarchy_path: List[str] = Field(default_factory=list) # e.g. ["Title 13", "Chapter 13.34", "Section 13.34.050", "(1)"]
    citations_mentioned: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LegalDocument(BaseModel):
    document_id: str
    source_id: str
    jurisdiction: str # e.g. US-WA, US-IL, US-OH, US
    level: Literal["federal", "state", "county", "municipal", "tribal"]
    document_type: Literal["statute", "constitution", "regulation", "court_opinion", "court_rule", "agency_policy", "form", "ethics_opinion"]
    title: str
    citation: str
    full_text: str
    chunks: List[LegalChunk] = Field(default_factory=list)
    temporal: TemporalMetadata = Field(default_factory=TemporalMetadata)
    authority: AuthorityScore
    source_url: str
    content_hash: str = ""
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    cps_topics: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def compute_hash(self) -> str:
        self.content_hash = hashlib.sha256(self.full_text.encode("utf-8")).hexdigest()
        return self.content_hash
