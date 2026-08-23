"""Structure-aware legal chunkers for statutes, court opinions, and agency policies."""

import re
from typing import List, Optional
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


class OpinionChunker(LegalChunker):
    """Chunks appellate court opinions into Syllabus, Holding, and Reasoning blocks."""

    @classmethod
    def chunk_opinion(
        cls,
        document_id: str,
        case_name: str,
        full_text: str,
        holding: Optional[str] = None
    ) -> List[LegalChunk]:
        chunks = []
        idx = 1

        # Section extraction by standard keywords
        sections = {"SYLLABUS": "", "HOLDING": "", "REASONING & OPINION": ""}
        current_sec = "REASONING & OPINION"
        lines = full_text.splitlines()

        for line in lines:
            line_clean = line.strip()
            if line_clean.startswith("SYLLABUS:"):
                current_sec = "SYLLABUS"
                continue
            elif line_clean.startswith("HOLDING:"):
                current_sec = "HOLDING"
                continue
            elif line_clean.startswith("REASONING & OPINION:"):
                current_sec = "REASONING & OPINION"
                continue

            sections[current_sec] += line + "\n"

        if sections["SYLLABUS"].strip():
            s_text = sections["SYLLABUS"].strip()
            chunks.append(LegalChunk(
                chunk_id=f"{document_id}_{idx:03d}",
                document_id=document_id,
                chunk_type="syllabus",
                heading=f"{case_name} - Syllabus",
                text=s_text,
                tokens_estimate=cls.estimate_tokens(s_text),
                hierarchy_path=[case_name, "Syllabus"],
            ))
            idx += 1

        if sections["HOLDING"].strip() or holding:
            h_text = sections["HOLDING"].strip() or holding or ""
            chunks.append(LegalChunk(
                chunk_id=f"{document_id}_{idx:03d}",
                document_id=document_id,
                chunk_type="holding",
                heading=f"{case_name} - Holding",
                text=h_text,
                tokens_estimate=cls.estimate_tokens(h_text),
                hierarchy_path=[case_name, "Holding"],
            ))
            idx += 1

        if sections["REASONING & OPINION"].strip():
            r_text = sections["REASONING & OPINION"].strip()
            chunks.append(LegalChunk(
                chunk_id=f"{document_id}_{idx:03d}",
                document_id=document_id,
                chunk_type="reasoning",
                heading=f"{case_name} - Reasoning & Analysis",
                text=r_text,
                tokens_estimate=cls.estimate_tokens(r_text),
                hierarchy_path=[case_name, "Reasoning"],
            ))
            idx += 1

        if not chunks:
            chunks.append(LegalChunk(
                chunk_id=f"{document_id}_001",
                document_id=document_id,
                chunk_type="reasoning",
                heading=case_name,
                text=full_text.strip(),
                tokens_estimate=cls.estimate_tokens(full_text),
                hierarchy_path=[case_name],
            ))

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
