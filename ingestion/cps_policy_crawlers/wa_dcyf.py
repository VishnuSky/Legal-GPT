"""Washington DCYF Child Welfare Policy Manual Crawler."""

import re
from typing import List
from datetime import date
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import PolicyChunker


class WashingtonDCYFPolicyConnector(BaseLegalConnector):
    def __init__(self):
        super().__init__(source_id="WA_DCYF_POLICY", rate_limit_delay_seconds=1.0)

    def parse_dcyf_policy(self, policy_number: str, title: str, full_text: str, effective_date: date) -> LegalDocument:
        doc_id = f"WA-DCYF-POL-{policy_number}"
        temporal = TemporalMetadata(
            effective_date=effective_date,
            is_current=True
        )
        authority = AuthorityScore(
            tier="TIER_0",
            weight=1.00,
            official_source=True,
            provider_name="Washington Department of Children, Youth, and Families (DCYF)"
        )
        chunks = PolicyChunker.chunk_policy(
            document_id=doc_id,
            title=f"DCYF Policy {policy_number}: {title}",
            full_text=full_text
        )
        doc = LegalDocument(
            document_id=doc_id,
            source_id="WA_DCYF_POLICY",
            jurisdiction="US-WA",
            level="state",
            document_type="agency_policy",
            title=f"DCYF Policy {policy_number} - {title}",
            citation=f"WA DCYF Policy {policy_number}",
            full_text=full_text,
            chunks=chunks,
            temporal=temporal,
            authority=authority,
            source_url=f"https://dcyf.wa.gov/practices-and-instruction/{policy_number}",
            cps_topics=["child_welfare", "agency_policy", "present_danger", "safety_assessment"]
        )
        doc.compute_hash()
        return doc

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return []
