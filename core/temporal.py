"""Temporal Law & Policy Engine: Resolves law in effect on specific historical dates."""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field
from normalization.models import LegalDocument, TemporalMetadata


class TemporalValidityResult(BaseModel):
    is_valid_on_date: bool
    target_date: date
    effective_date: Optional[date] = None
    repealed_date: Optional[date] = None
    version_id: Optional[str] = None
    reason: str


class TemporalEngine:
    @staticmethod
    def check_validity_on_date(doc_temporal: TemporalMetadata, target_date: date) -> TemporalValidityResult:
        """Determines if a document/statute was legally in effect on a given target date."""
        # 1. Check if effective date is after target date (not yet in effect)
        if doc_temporal.effective_date and doc_temporal.effective_date > target_date:
            return TemporalValidityResult(
                is_valid_on_date=False,
                target_date=target_date,
                effective_date=doc_temporal.effective_date,
                repealed_date=doc_temporal.repealed_date,
                version_id=doc_temporal.version_id,
                reason=f"Law was not yet in effect on {target_date.isoformat()} (effective date: {doc_temporal.effective_date.isoformat()})."
            )

        # 2. Check if repealed before target date
        if doc_temporal.repealed_date and doc_temporal.repealed_date <= target_date:
            return TemporalValidityResult(
                is_valid_on_date=False,
                target_date=target_date,
                effective_date=doc_temporal.effective_date,
                repealed_date=doc_temporal.repealed_date,
                version_id=doc_temporal.version_id,
                reason=f"Law was repealed on {doc_temporal.repealed_date.isoformat()} prior to {target_date.isoformat()}."
            )

        # Valid on date
        return TemporalValidityResult(
            is_valid_on_date=True,
            target_date=target_date,
            effective_date=doc_temporal.effective_date,
            repealed_date=doc_temporal.repealed_date,
            version_id=doc_temporal.version_id,
            reason=f"Law was legally valid and in effect on {target_date.isoformat()}."
        )

    @classmethod
    def resolve_effective_version(cls, versions: List[LegalDocument], target_date: date) -> Optional[LegalDocument]:
        """Given multiple historical versions of a statute/policy, finds the one valid on target_date."""
        valid_versions = []
        for doc in versions:
            res = cls.check_validity_on_date(doc.temporal, target_date)
            if res.is_valid_on_date:
                valid_versions.append(doc)

        if not valid_versions:
            return None

        # Return the version whose effective_date is closest (most recent) to target_date
        valid_versions.sort(
            key=lambda d: d.temporal.effective_date if d.temporal.effective_date else date.min,
            reverse=True
        )
        return valid_versions[0]
