"""Contribution Workflow Engine: State machine managing review lifecycle and quarantine firewall."""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone

from core.contributions.models import (
    CommunityContribution,
    ContributionState,
    ContributionType,
    ReviewEvent,
)
from core.contributions.validator import ContributionValidator
from core.contributions.provenance_graph import ContributionProvenanceGraph


class ContributionWorkflowEngine:
    """Manages community contribution submissions, reviews, transitions, and quarantine isolation."""

    def __init__(self, provenance_graph: Optional[ContributionProvenanceGraph] = None):
        self.provenance_graph = provenance_graph or ContributionProvenanceGraph()
        
        # Quarantine storage: items in PROPOSED, UNDER_REVIEW, REJECTED
        self._quarantine: Dict[str, CommunityContribution] = {}
        
        # Verified authoritative storage: ONLY items certified as VERIFIED
        self._verified_registry: Dict[str, CommunityContribution] = {}
        
        # Inactive/historical storage: SUPERSEDED or ARCHIVED items
        self._archive_registry: Dict[str, CommunityContribution] = {}
        
        # Immutable event ledger
        self._event_ledger: List[ReviewEvent] = []

    def submit(self, contribution: CommunityContribution) -> Dict[str, Any]:
        """Submits a new community contribution into quarantine after validation."""
        # 1. Validate schema, PII, licenses, and domains
        is_valid, errors = ContributionValidator.validate(contribution)
        if not is_valid:
            return {
                "success": False,
                "status": "VALIDATION_FAILED",
                "errors": errors,
                "contribution_id": contribution.contribution_id,
            }

        # 2. Compute cryptographic content hash
        if not contribution.provenance.content_hash:
            contribution.provenance.content_hash = contribution.calculate_hash()

        # 3. Strictly quarantine
        contribution.verification_state = ContributionState.PROPOSED
        self._quarantine[contribution.contribution_id] = contribution

        # 4. Record in Provenance Graph
        self.provenance_graph.record_contribution(contribution)

        # 5. Log audit event
        event = ReviewEvent(
            contribution_id=contribution.contribution_id,
            actor_id=f"SYSTEM-INGEST-{contribution.submitter}",
            previous_state=ContributionState.PROPOSED,
            new_state=ContributionState.PROPOSED,
            action="INGEST_QUARANTINE",
            notes="Submission passed automated validation gates and entered quarantine staging.",
        )
        self._event_ledger.append(event)

        return {
            "success": True,
            "status": ContributionState.PROPOSED.value,
            "contribution_id": contribution.contribution_id,
            "content_hash": contribution.provenance.content_hash,
            "message": "Contribution safely placed in quarantine. An audit is required before promotion.",
        }

    def begin_review(self, contribution_id: str, reviewer_id: str, notes: str = "") -> CommunityContribution:
        """Transitions a quarantined contribution from PROPOSED to UNDER_REVIEW."""
        contrib = self._get_from_any_stage(contribution_id)
        if not contrib:
            raise KeyError(f"Contribution '{contribution_id}' not found.")

        if contrib.verification_state != ContributionState.PROPOSED:
            raise ValueError(
                f"Cannot begin review on contribution in state '{contrib.verification_state.value}'. Must be 'PROPOSED'."
            )

        prev_state = contrib.verification_state
        contrib.verification_state = ContributionState.UNDER_REVIEW
        contrib.updated_at = datetime.now(timezone.utc)

        event = ReviewEvent(
            contribution_id=contribution_id,
            actor_id=reviewer_id,
            previous_state=prev_state,
            new_state=ContributionState.UNDER_REVIEW,
            action="BEGIN_REVIEW",
            notes=notes or "Assigned to reviewer for formal legal validation.",
        )
        self._event_ledger.append(event)
        self.provenance_graph.record_review_event(event)
        return contrib

    def verify(
        self,
        contribution_id: str,
        reviewer_id: str,
        notes: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CommunityContribution:
        """Certifies and promotes a contribution from UNDER_REVIEW to VERIFIED authoritative law."""
        contrib = self._get_from_any_stage(contribution_id)
        if not contrib:
            raise KeyError(f"Contribution '{contribution_id}' not found.")

        if contrib.verification_state != ContributionState.UNDER_REVIEW:
            raise ValueError(
                f"Cannot verify contribution in state '{contrib.verification_state.value}'. Must be 'UNDER_REVIEW'."
            )

        prev_state = contrib.verification_state
        contrib.verification_state = ContributionState.VERIFIED
        contrib.updated_at = datetime.now(timezone.utc)

        # Remove from quarantine and promote to live verified registry
        if contribution_id in self._quarantine:
            del self._quarantine[contribution_id]
        self._verified_registry[contribution_id] = contrib

        event = ReviewEvent(
            contribution_id=contribution_id,
            actor_id=reviewer_id,
            previous_state=prev_state,
            new_state=ContributionState.VERIFIED,
            action="PROMOTE_TO_VERIFIED",
            notes=notes,
            metadata=metadata or {},
        )
        self._event_ledger.append(event)
        self.provenance_graph.record_review_event(event)
        return contrib

    def reject(self, contribution_id: str, reviewer_id: str, reason: str) -> CommunityContribution:
        """Rejects a submission, ensuring it never enters the live verified registry."""
        contrib = self._get_from_any_stage(contribution_id)
        if not contrib:
            raise KeyError(f"Contribution '{contribution_id}' not found.")

        if contrib.verification_state not in (ContributionState.PROPOSED, ContributionState.UNDER_REVIEW):
            raise ValueError(
                f"Cannot reject contribution in state '{contrib.verification_state.value}'."
            )

        prev_state = contrib.verification_state
        contrib.verification_state = ContributionState.REJECTED
        contrib.updated_at = datetime.now(timezone.utc)

        # Remains in quarantine under REJECTED status
        self._quarantine[contribution_id] = contrib

        event = ReviewEvent(
            contribution_id=contribution_id,
            actor_id=reviewer_id,
            previous_state=prev_state,
            new_state=ContributionState.REJECTED,
            action="REJECT_CONTRIBUTION",
            notes=reason,
        )
        self._event_ledger.append(event)
        self.provenance_graph.record_review_event(event)
        return contrib

    def supersede(
        self,
        prior_contribution_id: str,
        successor_contribution_id: str,
        reviewer_id: str,
        notes: str,
    ) -> CommunityContribution:
        """Retires a previously verified contribution when superseded by newer legislation/rule."""
        prior_contrib = self._verified_registry.get(prior_contribution_id)
        if not prior_contrib:
            raise KeyError(f"Prior verified contribution '{prior_contribution_id}' not found in active registry.")

        successor_contrib = self._get_from_any_stage(successor_contribution_id)
        if not successor_contrib:
            raise KeyError(f"Successor contribution '{successor_contribution_id}' not found.")

        prev_state = prior_contrib.verification_state
        prior_contrib.verification_state = ContributionState.SUPERSEDED
        prior_contrib.updated_at = datetime.now(timezone.utc)

        # Move from verified to archived
        del self._verified_registry[prior_contribution_id]
        self._archive_registry[prior_contribution_id] = prior_contrib

        event = ReviewEvent(
            contribution_id=prior_contribution_id,
            actor_id=reviewer_id,
            previous_state=prev_state,
            new_state=ContributionState.SUPERSEDED,
            action="SUPERSEDE_ENACTMENT",
            notes=notes,
            metadata={"successor_contribution_id": successor_contribution_id},
        )
        self._event_ledger.append(event)
        self.provenance_graph.record_review_event(event)
        return prior_contrib

    def archive(self, contribution_id: str, reviewer_id: str, notes: str) -> CommunityContribution:
        """Archives a contribution for historical preservation only."""
        contrib = self._get_from_any_stage(contribution_id)
        if not contrib:
            raise KeyError(f"Contribution '{contribution_id}' not found.")

        prev_state = contrib.verification_state
        contrib.verification_state = ContributionState.ARCHIVED
        contrib.updated_at = datetime.now(timezone.utc)

        # Move out of active registries if present
        if contribution_id in self._verified_registry:
            del self._verified_registry[contribution_id]
        if contribution_id in self._quarantine:
            del self._quarantine[contribution_id]
        self._archive_registry[contribution_id] = contrib

        event = ReviewEvent(
            contribution_id=contribution_id,
            actor_id=reviewer_id,
            previous_state=prev_state,
            new_state=ContributionState.ARCHIVED,
            action="ARCHIVE_ENTRY",
            notes=notes,
        )
        self._event_ledger.append(event)
        self.provenance_graph.record_review_event(event)
        return contrib

    # =========================================================================
    # QUARANTINE FIREWALL ENFORCEMENT
    # =========================================================================

    def get_authoritative_verified_sources(
        self,
        jurisdiction: Optional[str] = None,
        contribution_type: Optional[ContributionType] = None,
    ) -> List[CommunityContribution]:
        """STRICT FIREWALL: Retrieves ONLY certified VERIFIED contributions.
        
        Submissions in PROPOSED, UNDER_REVIEW, REJECTED, SUPERSEDED, or ARCHIVED
        states are NEVER returned by this query method.
        """
        results = []
        for contrib in self._verified_registry.values():
            # Security double check
            if contrib.verification_state != ContributionState.VERIFIED:
                continue
            if jurisdiction and contrib.jurisdiction.upper() != jurisdiction.upper():
                continue
            if contribution_type and contrib.contribution_type != contribution_type:
                continue
            results.append(contrib)
        return results

    def get_quarantined_submissions(
        self,
        state: Optional[ContributionState] = None,
    ) -> List[CommunityContribution]:
        """Inspection method for auditors and reviewers to audit quarantined items."""
        if state:
            return [c for c in self._quarantine.values() if c.verification_state == state]
        return list(self._quarantine.values())

    def get_audit_history(self, contribution_id: str) -> List[ReviewEvent]:
        """Returns the complete sequence of audit events for a contribution."""
        return [e for e in self._event_ledger if e.contribution_id == contribution_id]

    def _get_from_any_stage(self, contribution_id: str) -> Optional[CommunityContribution]:
        """Internal helper to locate a contribution across all tiers."""
        if contribution_id in self._quarantine:
            return self._quarantine[contribution_id]
        if contribution_id in self._verified_registry:
            return self._verified_registry[contribution_id]
        if contribution_id in self._archive_registry:
            return self._archive_registry[contribution_id]
        return None
