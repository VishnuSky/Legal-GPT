"""Washington DCYF Child Welfare Policy Manual Ingestion Crawler."""

from typing import List
from datetime import date
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import PolicyChunker


class WashingtonDCYFPolicyConnector(BaseLegalConnector):
    def __init__(self):
        super().__init__(source_id="WA_DCYF_POLICY", rate_limit_delay_seconds=1.0)

    def parse_dcyf_policy(self, policy_number: str, title: str, full_text: str, effective_date: date) -> LegalDocument:
        doc_id = f"WA-DCYF-POL-{policy_number.replace('.', '_')}"
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

    def get_canonical_policies(self) -> List[LegalDocument]:
        docs = []

        # DCYF Policy 1110 - Present Danger Assessment
        docs.append(self.parse_dcyf_policy(
            policy_number="1110",
            title="Present Danger Assessment and Safety Planning",
            full_text=(
                "Purpose: Caseworkers must immediately assess for Present Danger threats to child safety at the initial contact with "
                "the family or child. Scope: Applies to all child protective services investigations. Policy: (1) Caseworkers must "
                "determine if an immediate, significant, and clearly observable threat to child safety is occurring in the present. "
                "(2) If Present Danger is identified, the caseworker must take immediate protective action to control the threat, "
                "including implementing an in-home safety plan with non-offending caregivers or seeking an emergency law enforcement removal "
                "only when safety cannot be managed in the home."
            ),
            effective_date=date(2023, 1, 1)
        ))

        # DCYF Policy 4254 - Family Time and Sibling Visits
        docs.append(self.parse_dcyf_policy(
            policy_number="4254",
            title="Family Time and Sibling and Relative Visits",
            full_text=(
                "Purpose: Family time is a fundamental right of children and families in out-of-home care. Policy: (1) The initial family time "
                "visit between the child and parents must occur within 72 hours of the child entering out-of-home placement, excluding weekends "
                "and holidays, unless court-ordered otherwise. (2) Family time must occur in the least restrictive setting possible. "
                "(3) Family time cannot be used as a sanction or reward for parental compliance with services."
            ),
            effective_date=date(2023, 7, 1)
        ))

        return docs

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return self.get_canonical_policies()
