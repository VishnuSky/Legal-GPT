"""Local Semantic & Lexical Hybrid Vector Store with BM25 Search."""

import math
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from normalization.models import LegalChunk, LegalDocument


class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    heading: Optional[str] = None
    text: str
    score: float
    citation: Optional[str] = None
    jurisdiction: Optional[str] = None


class SimpleHybridStore:
    """Lightweight in-memory BM25 + keyword search engine for local development & zero-dependency testing."""

    def __init__(self):
        self.chunks: Dict[str, LegalChunk] = {}
        self.doc_index: Dict[str, Dict[str, Any]] = {}
        self.term_freqs: Dict[str, Dict[str, int]] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_len: float = 0.0

    def add_chunks(self, chunks: List[LegalChunk], doc_metadata: Optional[Dict[str, Any]] = None):
        meta = doc_metadata or {}
        for c in chunks:
            self.chunks[c.chunk_id] = c
            self.doc_index[c.chunk_id] = meta

            tokens = self._tokenize(c.text + " " + (c.heading or ""))
            self.doc_lengths[c.chunk_id] = len(tokens)
            tf = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1
            self.term_freqs[c.chunk_id] = tf

        total_len = sum(self.doc_lengths.values())
        self.avg_doc_len = total_len / max(len(self.doc_lengths), 1)

    def add_document(self, doc: LegalDocument):
        doc_meta = {
            "citation": doc.citation,
            "jurisdiction": doc.jurisdiction,
            "document_type": doc.document_type,
            "title": doc.title,
            "source_url": doc.source_url
        }
        self.add_chunks(doc.chunks, doc_metadata=doc_meta)

    def load_from_database(self, db_path: str = "legal_gpt.db"):
        from storage.db import LegalDatabase
        db = LegalDatabase(db_path=db_path)
        docs = db.get_all_documents()
        for doc in docs:
            self.add_document(doc)

    def _tokenize(self, text: str) -> List[str]:
        return [w.lower() for w in re.findall(r"\b\w+\b", text)]

    def search(self, query: str, jurisdiction: Optional[str] = None, top_k: int = 5) -> List[SearchResult]:
        q_tokens = self._tokenize(query)
        scores: Dict[str, float] = {}

        k1 = 1.5
        b = 0.75
        N = len(self.chunks)
        if N == 0:
            return []

        for token in q_tokens:
            df = sum(1 for cid in self.chunks if token in self.term_freqs.get(cid, {}))
            if df == 0:
                continue
            idf = math.log((N - df + 0.5) / (df + 0.5) + 1.0)

            for cid, chunk in self.chunks.items():
                if jurisdiction:
                    doc_meta = self.doc_index.get(cid, {})
                    doc_juris = doc_meta.get("jurisdiction")
                    if doc_juris and doc_juris not in (jurisdiction, "US", "TRIBAL"):
                        continue

                tf = self.term_freqs.get(cid, {}).get(token, 0)
                doc_len = self.doc_lengths.get(cid, 1)
                num = tf * (k1 + 1)
                denom = tf + k1 * (1 - b + b * (doc_len / max(self.avg_doc_len, 1)))
                scores[cid] = scores.get(cid, 0.0) + (idf * (num / denom))

        sorted_cids = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        results = []
        for cid, score in sorted_cids:
            chunk = self.chunks[cid]
            doc_meta = self.doc_index.get(cid, {})
            results.append(SearchResult(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                heading=chunk.heading,
                text=chunk.text,
                score=round(score, 4),
                citation=doc_meta.get("citation"),
                jurisdiction=doc_meta.get("jurisdiction")
            ))
        return results
