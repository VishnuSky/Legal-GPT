"""Legal Precedent & Statutory Knowledge Graph (Pure Python Lightweight Graph)."""

from typing import List, Dict, Set, Optional, Tuple
from pydantic import BaseModel


class CitationRelationship(BaseModel):
    source_citation: str
    target_citation: str
    relation: str  # "CITES", "INTERPRETS", "APPLIES", "OVERRULES", "DISTINGUISHES", "AMENDS"


class LegalKnowledgeGraph:
    """Directed citation and authority graph implemented in pure Python."""

    def __init__(self):
        self._adj: Dict[str, Dict[str, Dict[str, str]]] = {}
        self._rev_adj: Dict[str, Dict[str, Dict[str, str]]] = {}

    def add_relation(self, source: str, target: str, relation: str):
        if source not in self._adj:
            self._adj[source] = {}
        if target not in self._adj:
            self._adj[target] = {}
        if source not in self._rev_adj:
            self._rev_adj[source] = {}
        if target not in self._rev_adj:
            self._rev_adj[target] = {}

        self._adj[source][target] = {"relation": relation}
        self._rev_adj[target][source] = {"relation": relation}

    def get_citations_by_case(self, citation: str) -> List[Dict[str, str]]:
        """Returns all citations that this case cites."""
        results = []
        if citation in self._adj:
            for neighbor, data in self._adj[citation].items():
                results.append({"target": neighbor, "relation": data.get("relation", "CITES")})
        return results

    def get_authorities_citing(self, citation: str) -> List[Dict[str, str]]:
        """Returns all cases/authorities that cite this statute or case."""
        results = []
        if citation in self._rev_adj:
            for predecessor, data in self._rev_adj[citation].items():
                results.append({"source": predecessor, "relation": data.get("relation", "CITES")})
        return results

    def is_overruled(self, citation: str) -> Tuple[bool, Optional[str]]:
        """Checks if any case has overruled this precedent."""
        citing = self.get_authorities_citing(citation)
        for c in citing:
            if c.get("relation") == "OVERRULES":
                return True, c.get("source")
        return False, None
