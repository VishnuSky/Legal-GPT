"""Provenance Graph: Directed Acyclic Graph (DAG) for tracking community contribution lineage and audit history."""

import json
from typing import Dict, List, Optional, Any, Set
from enum import Enum
from pydantic import BaseModel, Field

from core.contributions.models import (
    CommunityContribution,
    ContributionState,
    ContributionType,
    ReviewEvent,
)


class EdgeType(str, Enum):
    """Supported provenance graph edge types."""
    SUBMITTED_BY = "SUBMITTED_BY"
    ORIGINATES_FROM = "ORIGINATES_FROM"
    REVIEWED_BY = "REVIEWED_BY"
    VERIFIED_BY = "VERIFIED_BY"
    REJECTED_BY = "REJECTED_BY"
    SUPERSEDES = "SUPERSEDES"
    CITES = "CITES"


class ContributionNode(BaseModel):
    """Graph node representing a submitted contribution."""
    id: str
    contribution_type: ContributionType
    source: str
    jurisdiction: str
    authority_type: str
    verification_state: ContributionState
    content_hash: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SubmitterNode(BaseModel):
    """Graph node representing a submitter."""
    id: str
    organization: Optional[str] = None


class ReviewerNode(BaseModel):
    """Graph node representing an auditor or legal reviewer."""
    id: str
    credentials: Optional[str] = None
    role: Optional[str] = None


class OfficialSourceNode(BaseModel):
    """Graph node representing an authentic government or court publisher."""
    id: str
    official_portal_url: str
    publisher_name: str


class GraphEdge(BaseModel):
    """Directed edge linking two nodes in the provenance DAG."""
    source_id: str
    target_id: str
    edge_type: EdgeType
    timestamp: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ContributionProvenanceGraph:
    """Manages the Directed Acyclic Graph (DAG) of contribution provenance, custody, and supersession."""

    def __init__(self):
        self.nodes: Dict[str, BaseModel] = {}
        self.edges: List[GraphEdge] = []
        self._adjacency: Dict[str, List[GraphEdge]] = {}
        self._reverse_adjacency: Dict[str, List[GraphEdge]] = {}

    def add_node(self, node: BaseModel, node_id: str) -> None:
        """Registers a node in the graph."""
        self.nodes[node_id] = node
        if node_id not in self._adjacency:
            self._adjacency[node_id] = []
        if node_id not in self._reverse_adjacency:
            self._reverse_adjacency[node_id] = []

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        edge_type: EdgeType,
        timestamp: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Adds a directed relationship between two nodes in the graph."""
        edge = GraphEdge(
            source_id=source_id,
            target_id=target_id,
            edge_type=edge_type,
            timestamp=timestamp,
            metadata=metadata or {},
        )
        self.edges.append(edge)
        self._adjacency.setdefault(source_id, []).append(edge)
        self._reverse_adjacency.setdefault(target_id, []).append(edge)

    def record_contribution(self, contribution: CommunityContribution) -> None:
        """Indexes a new contribution and generates its origin nodes and custody edges."""
        # 1. Add ContributionNode
        content_hash = contribution.provenance.content_hash or contribution.calculate_hash()
        c_node = ContributionNode(
            id=contribution.contribution_id,
            contribution_type=contribution.contribution_type,
            source=contribution.source,
            jurisdiction=contribution.jurisdiction,
            authority_type=contribution.authority_type,
            verification_state=contribution.verification_state,
            content_hash=content_hash,
            metadata={"license": contribution.license, "date": contribution.date},
        )
        self.add_node(c_node, contribution.contribution_id)

        # 2. Add SubmitterNode & Edge
        submitter_id = f"SUBMITTER-{contribution.submitter}"
        s_node = SubmitterNode(id=submitter_id)
        self.add_node(s_node, submitter_id)
        self.add_edge(
            source_id=contribution.contribution_id,
            target_id=submitter_id,
            edge_type=EdgeType.SUBMITTED_BY,
            timestamp=contribution.created_at.isoformat(),
        )

        # 3. Add OfficialSourceNode & Edge
        source_id = f"OFFICIAL-{contribution.provenance.publisher}"
        o_node = OfficialSourceNode(
            id=source_id,
            official_portal_url=contribution.provenance.origin_url,
            publisher_name=contribution.provenance.publisher,
        )
        self.add_node(o_node, source_id)
        self.add_edge(
            source_id=contribution.contribution_id,
            target_id=source_id,
            edge_type=EdgeType.ORIGINATES_FROM,
            timestamp=contribution.created_at.isoformat(),
            metadata={"verification_method": contribution.provenance.verification_method},
        )

        # 4. Handle Supersession Link if parent specified
        if contribution.provenance.parent_contribution_id:
            parent_id = contribution.provenance.parent_contribution_id
            self.add_edge(
                source_id=contribution.contribution_id,
                target_id=parent_id,
                edge_type=EdgeType.SUPERSEDES,
                timestamp=contribution.created_at.isoformat(),
            )

    def record_review_event(self, event: ReviewEvent) -> None:
        """Records a review audit event and updates the node state in the graph."""
        # 1. Add ReviewerNode if absent
        rev_node_id = f"REV-{event.actor_id}"
        if rev_node_id not in self.nodes:
            r_node = ReviewerNode(
                id=rev_node_id,
                credentials=event.metadata.get("credentials", "Peer Reviewer"),
                role=event.metadata.get("role", "Auditor"),
            )
            self.add_node(r_node, rev_node_id)

        # 2. Determine edge type based on action/new state
        if event.new_state == ContributionState.VERIFIED:
            edge_type = EdgeType.VERIFIED_BY
        elif event.new_state == ContributionState.REJECTED:
            edge_type = EdgeType.REJECTED_BY
        else:
            edge_type = EdgeType.REVIEWED_BY

        self.add_edge(
            source_id=event.contribution_id,
            target_id=rev_node_id,
            edge_type=edge_type,
            timestamp=event.timestamp.isoformat(),
            metadata={
                "event_id": event.event_id,
                "action": event.action,
                "notes": event.notes,
                "previous_state": event.previous_state.value,
                "new_state": event.new_state.value,
            },
        )

        # 3. Update ContributionNode state in graph
        if event.contribution_id in self.nodes:
            node = self.nodes[event.contribution_id]
            if isinstance(node, ContributionNode):
                node.verification_state = event.new_state

    def get_lineage(self, contribution_id: str) -> Dict[str, Any]:
        """Retrieves comprehensive provenance lineage for a given contribution."""
        if contribution_id not in self.nodes:
            return {"error": f"Contribution '{contribution_id}' not found in provenance graph."}

        node = self.nodes[contribution_id]
        out_edges = self._adjacency.get(contribution_id, [])
        in_edges = self._reverse_adjacency.get(contribution_id, [])

        submitters = [e.target_id for e in out_edges if e.edge_type == EdgeType.SUBMITTED_BY]
        sources = [e.target_id for e in out_edges if e.edge_type == EdgeType.ORIGINATES_FROM]
        reviewers = [
            {"reviewer": e.target_id, "type": e.edge_type.value, "timestamp": e.timestamp, "notes": e.metadata.get("notes", "")}
            for e in out_edges
            if e.edge_type in (EdgeType.REVIEWED_BY, EdgeType.VERIFIED_BY, EdgeType.REJECTED_BY)
        ]
        supersedes = [e.target_id for e in out_edges if e.edge_type == EdgeType.SUPERSEDES]
        superseded_by = [e.source_id for e in in_edges if e.edge_type == EdgeType.SUPERSEDES]

        return {
            "contribution_id": contribution_id,
            "node": node.model_dump() if hasattr(node, "model_dump") else node.dict(),
            "submitters": submitters,
            "official_sources": sources,
            "review_audit_trail": reviewers,
            "supersedes": supersedes,
            "superseded_by": superseded_by,
        }

    def get_ancestry_chain(self, contribution_id: str) -> List[str]:
        """Traces the backward supersession chain to find prior versions of an authority."""
        chain = [contribution_id]
        curr = contribution_id
        visited: Set[str] = {contribution_id}

        while True:
            out_edges = self._adjacency.get(curr, [])
            parent_edges = [e for e in out_edges if e.edge_type == EdgeType.SUPERSEDES]
            if not parent_edges:
                break
            parent_id = parent_edges[0].target_id
            if parent_id in visited:
                # Cycle detected
                break
            visited.add(parent_id)
            chain.append(parent_id)
            curr = parent_id

        return chain

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the full graph to a dictionary."""
        return {
            "nodes": {
                nid: n.model_dump() if hasattr(n, "model_dump") else n.dict()
                for nid, n in self.nodes.items()
            },
            "edges": [
                e.model_dump() if hasattr(e, "model_dump") else e.dict()
                for e in self.edges
            ],
        }

    def to_json(self, indent: int = 2) -> str:
        """Serializes the full graph to formatted JSON."""
        return json.dumps(self.to_dict(), indent=indent, default=str)
