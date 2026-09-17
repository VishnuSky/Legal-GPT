"""Data models for the Legal-GPT Community Contribution Framework."""

import uuid
import hashlib
import json
from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ContributionType(str, Enum):
    """The 16 supported community contribution categories."""
    LEGAL_SOURCE = "LEGAL_SOURCE"
    SOURCE_METADATA = "SOURCE_METADATA"
    JURISDICTION = "JURISDICTION"
    CASE = "CASE"
    STATUTE = "STATUTE"
    REGULATION = "REGULATION"
    COURT_RULE = "COURT_RULE"
    AGENCY_POLICY = "AGENCY_POLICY"
    RESOURCE = "RESOURCE"
    DATASET = "DATASET"
    TEST_CASE = "TEST_CASE"
    BENCHMARK = "BENCHMARK"
    BUG_REPORT = "BUG_REPORT"
    DOCUMENTATION = "DOCUMENTATION"
    TRANSLATION = "TRANSLATION"
    LEGAL_LITERACY_MATERIAL = "LEGAL_LITERACY_MATERIAL"


class ContributionState(str, Enum):
    """The 6 lifecycle states for community submissions."""
    PROPOSED = "PROPOSED"           # Initial intake state (strictly quarantined)
    UNDER_REVIEW = "UNDER_REVIEW"   # Automated and human review in progress
    VERIFIED = "VERIFIED"           # Authenticated and certified as authoritative
    REJECTED = "REJECTED"           # Failed verification or policy checks
    SUPERSEDED = "SUPERSEDED"       # Replaced by a newer verified enactment
    ARCHIVED = "ARCHIVED"           # Retired or historical reference only


class ProvenanceMetadata(BaseModel):
    """Detailed origin and cryptographic provenance trace."""
    origin_url: str = Field(..., description="Official government or court repository URL")
    publisher: str = Field(..., description="Official publishing body or authority")
    verification_method: str = Field(..., description="Method used to extract or verify text")
    content_hash: Optional[str] = Field(None, description="SHA-256 cryptographic digest of payload")
    parent_contribution_id: Optional[str] = Field(None, description="ID of superseded prior version, if any")


class CommunityContribution(BaseModel):
    """The formal contribution record requiring all 9 mandatory fields."""
    contribution_id: str = Field(default_factory=lambda: f"CONTRIB-{uuid.uuid4().hex[:8].upper()}")
    contribution_type: ContributionType
    
    # The 9 mandatory fields
    source: str = Field(..., description="1. Primary legal citation, official title, or identifier")
    submitter: str = Field(..., description="2. Identity, handle, or organization of submitter")
    date: str = Field(default_factory=lambda: date.today().isoformat(), description="3. Submission date (YYYY-MM-DD)")
    jurisdiction: str = Field(..., description="4. Controlling jurisdiction code e.g. US-WA, US-IL, US")
    authority_type: str = Field(..., description="5. Hierarchical authority type e.g. T5_STATE_STATUTE")
    effective_date: Optional[str] = Field(None, description="6. Enactment or effective date if applicable")
    provenance: ProvenanceMetadata = Field(..., description="7. Full origin and verification provenance")
    license: str = Field(..., description="8. Permissive open data license (e.g. CC0-1.0, Apache-2.0)")
    verification_state: ContributionState = Field(ContributionState.PROPOSED, description="9. Current verification state")

    # Additional payload
    payload: Dict[str, Any] = Field(default_factory=dict, description="Substantive content payload")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def calculate_hash(self) -> str:
        """Computes SHA-256 digest over core immutable fields."""
        serialized = json.dumps(
            {
                "source": self.source,
                "jurisdiction": self.jurisdiction,
                "authority_type": self.authority_type,
                "effective_date": self.effective_date,
                "payload": self.payload,
                "license": self.license
            },
            sort_keys=True
        )
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


class ReviewEvent(BaseModel):
    """Immutable log entry for a review or state transition event."""
    event_id: str = Field(default_factory=lambda: f"EVT-{uuid.uuid4().hex[:8].upper()}")
    contribution_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actor_id: str
    previous_state: ContributionState
    new_state: ContributionState
    action: str
    notes: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
