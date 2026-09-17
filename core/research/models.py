"""Data models for the 18-step Legal Research Copilot planning subsystem."""

from datetime import date
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class LegalSystem(str, Enum):
    """Governing legal system for the question."""
    FEDERAL = "FEDERAL"
    STATE = "STATE"
    TRIBAL = "TRIBAL"
    ADMINISTRATIVE = "ADMINISTRATIVE"
    MUNICIPAL = "MUNICIPAL"
    MILITARY = "MILITARY"
    HYBRID = "HYBRID"
    UNKNOWN = "UNKNOWN"


class SourcePriorityTier(str, Enum):
    """Hierarchical source priority rating.
    
    Primary and official government/court/agency sources are preferred over
    secondary summaries, blogs, forums, and AI-generated material.
    """
    # Preferred: Primary & Official sources
    PRIMARY_CONSTITUTIONAL = "PRIMARY_CONSTITUTIONAL"       # Tier 0: Constitutions
    PRIMARY_STATUTORY = "PRIMARY_STATUTORY"                 # Tier 4/5: Federal & State Statutes
    PRIMARY_REGULATORY = "PRIMARY_REGULATORY"               # Tier 6/7: Federal & State Administrative Codes
    PRIMARY_CASELAW_BINDING = "PRIMARY_CASELAW_BINDING"     # Tier 1/2/3: SCOTUS & Binding Appellate Precedent
    OFFICIAL_COURT_RULES = "OFFICIAL_COURT_RULES"           # Tier 8: Federal & State Court Rules
    OFFICIAL_AGENCY_POLICY = "OFFICIAL_AGENCY_POLICY"       # Tier 10: Official Agency Manuals & Declaratory Orders
    PRIMARY_CASELAW_PERSUASIVE = "PRIMARY_CASELAW_PERSUASIVE" # Tier 11: Out-of-circuit / Non-binding caselaw

    # Deprecated / Lower Priority Sources
    SECONDARY_SUMMARY = "SECONDARY_SUMMARY"                 # Tier 12: Restatements, Law Reviews, Treatises
    DISALLOWED_BLOG_OR_FORUM = "DISALLOWED_BLOG_OR_FORUM"   # Blogs, reddit, quora, forums (unverified)
    DISALLOWED_AI_GENERATED = "DISALLOWED_AI_GENERATED"     # AI-generated hallucinations/unverified text


class AuthoritySearchTarget(BaseModel):
    """Represents a specific legal authority targeted for search during research planning."""
    authority_type: str = Field(..., description="CONSTITUTION, STATUTE, REGULATION, PRECEDENT, PERSUASIVE, POLICY, TRIBAL")
    citation_or_query: str = Field(..., description="Target citation or search phrase")
    source_priority: SourcePriorityTier = Field(..., description="Priority tier according to source hierarchy")
    preferred_official_source: str = Field(..., description="Official government/court portal or repository")
    purpose: str = Field(..., description="Specific proposition or element to establish")
    is_binding: bool = Field(True, description="Whether this authority is binding in forum")
    is_primary: bool = Field(True, description="Whether this is primary legal authority")


class ResearchSearchResult(BaseModel):
    """Result retrieved or identified for an authority search target."""
    authority_id: str
    citation: str
    title: str
    source_tier: SourcePriorityTier
    official_source_url_or_portal: str
    is_official_government_source: bool = True
    is_primary_authority: bool = True
    key_excerpt: str
    subsequent_treatment: str = "VALID"  # VALID, OVERRULED, ABROGATED, DISTINGUISHED, CRITICIZED, CAUTION
    temporal_status: str = "CURRENT"     # CURRENT, AMENDED, REPEALED, PENDING_EFFECTIVE
    jurisdiction: str


class AuthorityConflictItem(BaseModel):
    """Identified conflict between authorities, jurisdictions, or precedents."""
    conflict_type: str = Field(..., description="PREEMPTION, CIRCUIT_SPLIT, STATUTORY_AMBIGUITY, TEMPORAL_CHANGE, PRECEDENT_OVERRULE")
    primary_authority: str
    conflicting_authority: str
    explanation: str
    status: str = Field("UNRESOLVED", description="RESOLVED, UNRESOLVED, FORUM_DEPENDENT")


class ResearchPlan18Steps(BaseModel):
    """The complete 18-step Research Plan generated prior to substantive answer drafting."""
    step_1_jurisdiction: str = Field(..., description="Country, state, county, tribal area")
    step_2_legal_system: LegalSystem = Field(..., description="Governing legal system")
    step_3_date: str = Field(..., description="Relevant event date or governing statutory timeframe")
    step_4_procedural_posture: str = Field(..., description="Current procedural posture of the dispute")
    step_5_legal_issues: List[str] = Field(default_factory=list, description="Substantive and procedural legal issues")
    step_6_constitutional_provisions: List[str] = Field(default_factory=list, description="Federal and state constitutional provisions")
    step_7_statutes: List[str] = Field(default_factory=list, description="Controlling federal and state statutes")
    step_8_regulations: List[str] = Field(default_factory=list, description="Controlling administrative regulations")
    step_9_controlling_precedent: List[str] = Field(default_factory=list, description="Binding SCOTUS, Circuit, or State Supreme caselaw")
    step_10_persuasive_authority: List[str] = Field(default_factory=list, description="Persuasive out-of-jurisdiction or lower court caselaw")
    step_11_agency_policies: List[str] = Field(default_factory=list, description="Agency manuals, policy directives, or declaratory rulings")
    step_12_tribal_authority: List[str] = Field(default_factory=list, description="ICWA provisions, tribal codes, or tribal sovereign interests")
    step_13_subsequent_treatment: Dict[str, str] = Field(default_factory=dict, description="Citator signal/status for key citations")
    step_14_temporal_validity: Dict[str, str] = Field(default_factory=dict, description="Temporal status and effective date checks")
    step_15_jurisdiction_check: str = Field(..., description="Subject matter, personal, and forum appropriateness")
    step_16_conflicts_check: List[AuthorityConflictItem] = Field(default_factory=list, description="Detected conflicts")
    step_17_missing_authority: List[str] = Field(default_factory=list, description="Identified gaps in primary authority")
    step_18_unanswered_questions: List[str] = Field(default_factory=list, description="Critical factual and legal questions remaining")


class ResearchPlanOutput(BaseModel):
    """The structured 10-section output report required by the mission."""
    research_question: str
    jurisdiction: str
    date: str
    issues: List[str]
    authorities_to_search: List[AuthoritySearchTarget]
    search_results: List[ResearchSearchResult]
    authority_conflicts: List[AuthorityConflictItem]
    unanswered_questions: List[str]
    verification_status: str = Field(..., description="VERIFIED_PRIMARY, PARTIALLY_VERIFIED, UNVERIFIED")
    completeness_status: str = Field(..., description="RESEARCH COMPLETE or RESEARCH INCOMPLETE")

    # The detailed 18-step underlying plan
    plan_steps: ResearchPlan18Steps
