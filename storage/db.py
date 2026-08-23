"""Relational Database Layer for Documents, Citations, Citator Graphs, and Temporal Versions."""

import sqlite3
import json
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from datetime import date, datetime, timezone
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

            # Precedent, Citation & Citator relationships table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS legal_relationships (
                    source_citation TEXT,
                    target_citation TEXT,
                    relation_type TEXT, -- cites, interprets, follows, distinguishes, overrules, abrogates, supersedes, amends
                    treatment_signal TEXT, -- POSITIVE, CAUTION, NEGATIVE, NEUTRAL
                    pinpoint_citation TEXT,
                    context_snippet TEXT,
                    jurisdiction TEXT,
                    created_at TEXT,
                    PRIMARY KEY (source_citation, target_citation, relation_type)
                )
            """)

            # Historical Revisions & Law-At-Date table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS legal_historical_revisions (
                    version_id TEXT PRIMARY KEY,
                    citation TEXT,
                    jurisdiction TEXT,
                    title TEXT,
                    full_text TEXT,
                    effective_start TEXT,
                    effective_end TEXT,
                    is_current INTEGER,
                    enacted_bill TEXT,
                    repealed_by TEXT,
                    superseded_by TEXT,
                    amendment_notes TEXT
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

    def insert_relationship(
        self,
        source_citation: str,
        target_citation: str,
        relation_type: str,
        treatment_signal: str = "NEUTRAL",
        pinpoint_citation: Optional[str] = None,
        context_snippet: Optional[str] = None,
        jurisdiction: str = "US"
    ):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO legal_relationships (
                    source_citation, target_citation, relation_type, treatment_signal,
                    pinpoint_citation, context_snippet, jurisdiction, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                source_citation,
                target_citation,
                relation_type.upper(),
                treatment_signal.upper(),
                pinpoint_citation,
                context_snippet,
                jurisdiction,
                datetime.now(timezone.utc).isoformat()
            ))
            conn.commit()

    def get_relationships_for_citation(self, citation: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            pattern = f"%{citation.strip()}%"
            cursor.execute("""
                SELECT * FROM legal_relationships
                WHERE source_citation LIKE ? OR target_citation LIKE ?
            """, (pattern, pattern))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_citing_authorities(self, target_citation: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            pattern = f"%{target_citation.strip()}%"
            cursor.execute("""
                SELECT * FROM legal_relationships
                WHERE target_citation LIKE ?
            """, (pattern,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def insert_historical_revision(
        self,
        version_id: str,
        citation: str,
        jurisdiction: str,
        title: str,
        full_text: str,
        effective_start: date,
        effective_end: Optional[date] = None,
        is_current: bool = True,
        enacted_bill: Optional[str] = None,
        repealed_by: Optional[str] = None,
        superseded_by: Optional[str] = None,
        amendment_notes: Optional[str] = None
    ):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO legal_historical_revisions (
                    version_id, citation, jurisdiction, title, full_text,
                    effective_start, effective_end, is_current, enacted_bill,
                    repealed_by, superseded_by, amendment_notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                version_id,
                citation,
                jurisdiction,
                title,
                full_text,
                effective_start.isoformat(),
                effective_end.isoformat() if effective_end else None,
                1 if is_current else 0,
                enacted_bill,
                repealed_by,
                superseded_by,
                amendment_notes
            ))
            conn.commit()

    def get_historical_revisions(self, citation: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM legal_historical_revisions
                WHERE citation = ?
                ORDER BY effective_start ASC
            """, (citation,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_revision_at_date(self, citation: str, target_date: date) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            target_str = target_date.isoformat()
            cursor.execute("""
                SELECT * FROM legal_historical_revisions
                WHERE citation = ?
                  AND effective_start <= ?
                  AND (effective_end IS NULL OR effective_end >= ?)
                ORDER BY effective_start DESC
                LIMIT 1
            """, (citation, target_str, target_str))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

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
            retrieved_at=datetime.fromisoformat(row["retrieved_at"]) if "retrieved_at" in row.keys() and row["retrieved_at"] else datetime.now(timezone.utc),
            cps_topics=json.loads(row["cps_topics"]) if row["cps_topics"] else [],
            metadata=json.loads(row["metadata_json"]) if row["metadata_json"] else {}
        )

    def get_all_documents(self) -> List[LegalDocument]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM legal_documents")
            rows = cursor.fetchall()
            docs = []
            for row in rows:
                doc = self._row_to_document(row)
                cursor.execute("SELECT * FROM legal_chunks WHERE document_id = ?", (doc.document_id,))
                chunk_rows = cursor.fetchall()
                for cr in chunk_rows:
                    doc.chunks.append(LegalChunk(
                        chunk_id=cr["chunk_id"],
                        document_id=cr["document_id"],
                        chunk_type=cr["chunk_type"],
                        heading=cr["heading"],
                        text=cr["text"],
                        hierarchy_path=json.loads(cr["hierarchy_path"]) if cr["hierarchy_path"] else [],
                        citations_mentioned=json.loads(cr["citations_mentioned"]) if cr["citations_mentioned"] else []
                    ))
                docs.append(doc)
            return docs

    def get_document_count(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM legal_documents")
            return cursor.fetchone()[0]
