"""Structure-aware legal chunkers for statutes, court opinions, and agency policies."""

import re
from typing import List
from normalization.models import LegalChunk


class LegalChunker:
    """Base legal chunker."""
    @staticmethod
    def estimate_tokens(text: str) -> int:
        return len(text.split()) * 4 // 3


class StatuteChunker(LegalChunker):
    """Chunks statutory text by section and subsection hierarchy."""

    SUBSECTION_REGEX = re.compile(r"(?:\n|^)\s*(\([0-9a-zA-Z]+\))\s*")

    @classmethod
    def chunk_statute(cls, document_id: str, title: str, full_text: str) -> List[LegalChunk]:
        chunks = []
        raw_subsections = cls.SUBSECTION_REGEX.split(full_text)

        if len(raw_subsections) <= 1:
            # Single chunk for short statute
            chunk = LegalChunk(
                chunk_id=f"{document_id}_001",
                document_id=document_id,
                chunk_type="section",
                heading=title,
                text=full_text.strip(),
                tokens_estimate=cls.estimate_tokens(full_text),
                hierarchy_path=[title],
            )
            return [chunk]

        # Intro text before first subsection
        intro_text = raw_subsections[0].strip()
        idx = 1
        if intro_text:
            chunks.append(LegalChunk(
                chunk_id=f"{document_id}_{idx:03d}",
                document_id=document_id,
                chunk_type="section",
                heading=f"{title} (Intro)",
                text=intro_text,
                tokens_estimate=cls.estimate_tokens(intro_text),
                hierarchy_path=[title, "Intro"],
            ))
            idx += 1

        for i in range(1, len(raw_subsections), 2):
            label = raw_subsections[i].strip()
            body = raw_subsections[i + 1].strip() if (i + 1) < len(raw_subsections) else ""
            combined_text = f"{label} {body}"
            chunks.append(LegalChunk(
                chunk_id=f"{document_id}_{idx:03d}",
                document_id=document_id,
                chunk_type="subsection",
                heading=f"{title} {label}",
                text=combined_text,
                tokens_estimate=cls.estimate_tokens(combined_text),
                hierarchy_path=[title, label],
            ))
            idx += 1

        return chunks


class PolicyChunker(LegalChunker):
    """Chunks agency policies into Purpose, Policy, Procedure, and Authority blocks."""

    SECTION_REGEX = re.compile(r"(?:\n|^)(I{1,3}|IV|V|VI|VII|VIII|IX|X|\d+)\.\s+([A-Z\s]{3,})\b")

    @classmethod
    def chunk_policy(cls, document_id: str, title: str, full_text: str) -> List[LegalChunk]:
        chunks = []
        lines = full_text.splitlines()
        current_heading = "Overview"
        current_lines = []
        idx = 1

        for line in lines:
            if any(key in line.upper() for key in ["PURPOSE", "POLICY", "PROCEDURE", "AUTHORITY", "DEFINITIONS"]):
                if current_lines:
                    text = "\n".join(current_lines).strip()
                    if text:
                        chunks.append(LegalChunk(
                            chunk_id=f"{document_id}_{idx:03d}",
                            document_id=document_id,
                            chunk_type="procedure" if "PROCEDURE" in current_heading.upper() else "policy_rule",
                            heading=f"{title} - {current_heading}",
                            text=text,
                            tokens_estimate=cls.estimate_tokens(text),
                            hierarchy_path=[title, current_heading],
                        ))
                        idx += 1
                    current_lines = []
                current_heading = line.strip()
            else:
                current_lines.append(line)

        if current_lines:
            text = "\n".join(current_lines).strip()
            if text:
                chunks.append(LegalChunk(
                    chunk_id=f"{document_id}_{idx:03d}",
                    document_id=document_id,
                    chunk_type="policy_rule",
                    heading=f"{title} - {current_heading}",
                    text=text,
                    tokens_estimate=cls.estimate_tokens(text),
                    hierarchy_path=[title, current_heading],
                ))

        if not chunks:
            chunks.append(LegalChunk(
                chunk_id=f"{document_id}_001",
                document_id=document_id,
                chunk_type="policy_rule",
                heading=title,
                text=full_text.strip(),
                tokens_estimate=cls.estimate_tokens(full_text),
                hierarchy_path=[title],
            ))

        return chunks
