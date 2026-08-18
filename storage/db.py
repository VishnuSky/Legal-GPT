"""Relational Database Layer for Documents, Citations, and Temporal Versions."""

import sqlite3
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import date
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore, LegalChunk


class LegalDatabase:
    def __init__(self, db_path: str = "legal_gpt.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Documents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS legal_documents (
                    document_id TEXT PRIMARY KEY,
                    source_id TEXT,
                    jurisdiction TEXT,
                    level TEXT,
                    document_type TEXT,
                    title TEXT,
                    citation TEXT,
                    full_text TEXT,
                    enacted_date TEXT,
                    effective_date TEXT,
                    repealed_date TEXT,
                    is_current INTEGER,
                    authority_tier TEXT,
                    authority_weight REAL,
                    provider_name TEXT,
                    source_url TEXT,
                    content_hash TEXT,
                    retrieved_at TEXT,
                    cps_topics TEXT,
                    metadata_json TEXT
                )
            """)

            # Chunks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS legal_chunks (
                    chunk_id TEXT PRIMARY KEY,
                    document_id TEXT,
                    chunk_type TEXT,
                    heading TEXT,
                    text TEXT,
                    hierarchy_path TEXT,
                    citations_mentioned TEXT,
                    FOREIGN KEY (document_id) REFERENCES legal_documents(document_id)
                )
            """)

            # Precedent & Citation relationships
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS citation_graph (
                    source_citation TEXT,
                    target_citation TEXT,
                    relationship_type TEXT, -- cites, interprets, overrules, distinguishes, applies
                    jurisdiction TEXT,
                    PRIMARY KEY (source_citation, target_citation, relationship_type)
                )
            """)
            conn.commit()

    def insert_document(self, doc: LegalDocument):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO legal_documents (
                    document_id, source_id, jurisdiction, level, document_type,
                    title, citation, full_text, enacted_date, effective_date,
                    repealed_date, is_current, authority_tier, authority_weight,
                    provider_name, source_url, content_hash, retrieved_at,
                    cps_topics, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                doc.document_id,
                doc.source_id,
                doc.jurisdiction,
                doc.level,
                doc.document_type,
                doc.title,
                doc.citation,
                doc.full_text,
                doc.temporal.enacted_date.isoformat() if doc.temporal.enacted_date else None,
                doc.temporal.effective_date.isoformat() if doc.temporal.effective_date else None,
                doc.temporal.repealed_date.isoformat() if doc.temporal.repealed_date else None,
                1 if doc.temporal.is_current else 0,
                doc.authority.tier,
                doc.authority.weight,
                doc.authority.provider_name,
                doc.source_url,
                doc.content_hash,
                doc.retrieved_at.isoformat(),
                json.dumps(doc.cps_topics),
                json.dumps(doc.metadata)
            ))

            for chunk in doc.chunks:
                cursor.execute("""
                    INSERT OR REPLACE INTO legal_chunks (
                        chunk_id, document_id, chunk_type, heading, text, hierarchy_path, citations_mentioned
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    chunk.chunk_id,
                    doc.document_id,
                    chunk.chunk_type,
                    chunk.heading,
                    chunk.text,
                    json.dumps(chunk.hierarchy_path),
                    json.dumps(chunk.citations_mentioned)
                ))
            conn.commit()

    def query_statute_by_citation(self, citation: str) -> Optional[LegalDocument]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM legal_documents WHERE citation = ?", (citation,))
            row = cursor.fetchone()
            if not row:
                return None
            return self._row_to_document(row)

    def _row_to_document(self, row: sqlite3.Row) -> LegalDocument:
        temporal = TemporalMetadata(
            enacted_date=date.fromisoformat(row["enacted_date"]) if row["enacted_date"] else None,
            effective_date=date.fromisoformat(row["effective_date"]) if row["effective_date"] else None,
            repealed_date=date.fromisoformat(row["repealed_date"]) if row["repealed_date"] else None,
            is_current=bool(row["is_current"])
        )
        authority = AuthorityScore(
            tier=row["authority_tier"],
            weight=row["authority_weight"],
            official_source=True,
            provider_name=row["provider_name"]
        )
        return LegalDocument(
            document_id=row["document_id"],
            source_id=row["source_id"],
            jurisdiction=row["jurisdiction"],
            level=row["level"],
            document_type=row["document_type"],
            title=row["title"],
            citation=row["citation"],
            full_text=row["full_text"],
            temporal=temporal,
            authority=authority,
            source_url=row["source_url"],
            content_hash=row["content_hash"],
            cps_topics=json.loads(row["cps_topics"]) if row["cps_topics"] else [],
            metadata=json.loads(row["metadata_json"]) if row["metadata_json"] else {}
        )
