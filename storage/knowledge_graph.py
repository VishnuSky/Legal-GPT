"""Legal Precedent & Statutory Knowledge Graph."""

from typing import List, Dict, Set, Optional
import networkx as nx
from pydantic import BaseModel


class CitationRelationship(BaseModel):
    source_citation: str
    target_citation: str
    relation: str # "CITES", "INTERPRETS", "APPLIES", "OVERRULES", "DISTINGUISHES", "AMENDS"


class LegalKnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_relation(self, source: str, target: str, relation: str):
        self.graph.add_edge(source, target, relation=relation)

    def get_citations_by_case(self, citation: str) -> List[Dict[str, str]]:
        """Returns all citations that this case cites."""
        results = []
        if citation in self.graph:
            for neighbor in self.graph.successors(citation):
                rel = self.graph[citation][neighbor].get("relation", "CITES")
                results.append({"target": neighbor, "relation": rel})
        return results

    def get_authorities_citing(self, citation: str) -> List[Dict[str, str]]:
        """Returns all cases/authorities that cite this statute or case."""
        results = []
        if citation in self.graph:
            for predecessor in self.graph.predecessors(citation):
                rel = self.graph[predecessor][citation].get("relation", "CITES")
                results.append({"source": predecessor, "relation": rel})
        return results

    def is_overruled(self, citation: str) -> tuple:
        """Checks if any case has overruled this precedent."""
        if citation in self.graph:
            for pred in self.graph.predecessors(citation):
                if self.graph[pred][citation].get("relation") == "OVERRULES":
                    return True, pred
        return False, None
