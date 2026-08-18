"""Pydantic schemas for machine-readable legal source registry entries."""

from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, HttpUrl


class PublisherInfo(BaseModel):
    name: str
    official: bool = True
    entity_type: Literal["legislature", "court", "executive_agency", "bar_association", "non_profit", "commercial"]
    contact_url: Optional[str] = None


class TemporalCapability(BaseModel):
    versioned: bool = True
    effective_dates_available: bool = True
    historical_versions_available: bool = False
    earliest_available_date: Optional[str] = None
    latest_available_date: Optional[str] = None


class ApiAccess(BaseModel):
    available: bool = False
    api_type: Optional[Literal["REST", "GraphQL", "SOAP", "RSS", "SITEMAP", "BULK_DOWNLOAD", "NONE"]] = "NONE"
    auth_required: bool = False
    auth_env_var: Optional[str] = None
    rate_limit_rpm: Optional[int] = None
    bulk_download_url: Optional[str] = None
    documentation_url: Optional[str] = None


class LegalSourceEntry(BaseModel):
    source_id: str = Field(..., description="Unique machine-readable ID e.g. WA_RCW, FED_USCODE")
    jurisdiction: str = Field(..., description="ISO or standardized code e.g. US, US-WA, US-IL, US-OH, TRIBAL")
    level: Literal["federal", "state", "county", "municipal", "tribal", "territory", "international"]
    authority_tier: Literal["TIER_0", "TIER_1", "TIER_2", "TIER_3", "TIER_4", "TIER_5"]
    legal_domain: List[str] = Field(default_factory=list, description="Domains e.g. ['statutes', 'child_welfare', 'family_law']")
    source_type: Literal["statute", "constitution", "regulation", "court_opinion", "court_rule", "agency_policy", "form", "ethics_opinion", "secondary_treatise"]
    title: str
    citation_format: Optional[str] = None
    publisher: PublisherInfo
    canonical_url: str
    search_url: Optional[str] = None
    api: ApiAccess = Field(default_factory=ApiAccess)
    temporal: TemporalCapability = Field(default_factory=TemporalCapability)
    acquisition_method: Literal["api", "bulk_download", "html_scrape", "pdf_parse", "rss_feed", "manual_seed"] = "html_scrape"
    parser_name: str
    update_frequency: Literal["realtime", "daily", "weekly", "monthly", "annually", "static"] = "daily"
    cps_priority: int = Field(default=0, ge=0, le=10, description="Priority weight for Child Welfare pipeline (0-10)")
    active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
