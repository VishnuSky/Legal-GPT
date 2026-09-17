"""Legal-GPT Community Contribution Framework.

Enables the public, researchers, attorneys, technologists, and advocates to submit
legal sources, metadata, test cases, and resources while guaranteeing that unverified
claims never become authoritative law.
"""

from core.contributions.models import (
    ContributionType,
    ContributionState,
    ProvenanceMetadata,
    CommunityContribution,
    ReviewEvent,
)
from core.contributions.validator import ContributionValidator
from core.contributions.provenance_graph import (
    ContributionProvenanceGraph,
    EdgeType,
    ContributionNode,
    SubmitterNode,
    ReviewerNode,
    OfficialSourceNode,
    GraphEdge,
)
from core.contributions.workflow import ContributionWorkflowEngine

__all__ = [
    "ContributionType",
    "ContributionState",
    "ProvenanceMetadata",
    "CommunityContribution",
    "ReviewEvent",
    "ContributionValidator",
    "ContributionProvenanceGraph",
    "EdgeType",
    "ContributionNode",
    "SubmitterNode",
    "ReviewerNode",
    "OfficialSourceNode",
    "GraphEdge",
    "ContributionWorkflowEngine",
]
