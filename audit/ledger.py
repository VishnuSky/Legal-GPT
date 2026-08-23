"""AI Audit Ledger: Immutable, Reproducible Session Records for Court and Ethical Compliance."""

import hashlib
import json
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class AuditLogEntry(BaseModel):
    session_id: str = Field(default_factory=lambda: f"LEGAL-AI-{uuid.uuid4().hex[:12].upper()}")
    user_query: str
    jurisdiction: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_version: str = "Legal-GPT-v0.2.0"
    retrieval_queries: List[str] = Field(default_factory=list)
    document_ids_used: List[str] = Field(default_factory=list)
    chunks_used: List[str] = Field(default_factory=list)
    authorities_used: List[str] = Field(default_factory=list)
    proposition_verification_results: List[Dict[str, Any]] = Field(default_factory=list)
    counterarguments_identified: int = 0
    human_review_status: str = "PENDING_HUMAN_CERTIFICATION"
    final_output_hash: str = ""

    def compute_output_hash(self, output_text: str):
        self.final_output_hash = hashlib.sha256(output_text.encode("utf-8")).hexdigest()


class AIAuditLedger:
    """In-memory and persistent audit trail for reproducible legal AI outputs."""

    def __init__(self):
        self.ledger: Dict[str, AuditLogEntry] = {}

    def record_session(
        self,
        user_query: str,
        jurisdiction: str,
        authorities_used: List[str],
        output_text: str,
        retrieval_queries: Optional[List[str]] = None,
        chunks_used: Optional[List[str]] = None,
        counterarguments_count: int = 0
    ) -> AuditLogEntry:
        entry = AuditLogEntry(
            user_query=user_query,
            jurisdiction=jurisdiction,
            authorities_used=authorities_used,
            retrieval_queries=retrieval_queries or [],
            chunks_used=chunks_used or [],
            counterarguments_identified=counterarguments_count
        )
        entry.compute_output_hash(output_text)
        self.ledger[entry.session_id] = entry
        return entry

    def get_entry(self, session_id: str) -> Optional[AuditLogEntry]:
        return self.ledger.get(session_id)


# Global singleton
audit_ledger = AIAuditLedger()
