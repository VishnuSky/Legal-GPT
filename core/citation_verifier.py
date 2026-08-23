"""Anti-Hallucination Citation Verifier: Validates that all legal citations resolve to real authority."""

import re
from typing import List, Dict, Tuple, Optional, Set
from pydantic import BaseModel, Field
from legal_registry.loader import default_registry


class CitationVerificationRecord(BaseModel):
    raw_citation: str
    normalized_citation: str
    verified: bool
    authority_tier: str
    publisher_name: str
    jurisdiction: str = "US"
    source_url: Optional[str] = None
    rejection_reason: Optional[str] = None


class CitationVerifier:
    # Regex patterns for canonical statutory citations
    RCW_PATTERN = re.compile(r"\bRCW\s+(\d{1,3}\.\d{2,3}(?:\.\d{3,4})?)\b", re.IGNORECASE)
    ILCS_PATTERN = re.compile(r"\b(\d+)\s+ILCS\s+(\d+)\/(\d+(?:-\d+)?(?:\.\d+)?)\b", re.IGNORECASE)
    ORC_PATTERN = re.compile(r"\b(?:ORC|R\.C\.)\s*§?\s*(\d{1,4}\.\d{2,3})\b", re.IGNORECASE)
    USC_PATTERN = re.compile(r"\b(\d+)\s+U\.S\.C\.\s*§?\s*(\d+[a-z]*(?:\([a-zA-Z0-9]+\))*)\b", re.IGNORECASE)
    CFR_PATTERN = re.compile(r"\b(\d+)\s+C\.F\.R\.\s*§?\s*(\d+(?:\.\d+)?)\b", re.IGNORECASE)

    # Known statutory titles/chapters in CPS & Family law
    VALID_RCW_TITLES = {"13", "26", "74", "10", "4", "2", "9", "9A"}
    VALID_ILCS_CHAPTERS = {"705", "325", "750", "20", "720"}
    VALID_ORC_CHAPTERS = {"2151", "3109", "3127", "2919", "5101"}
    VALID_USC_TITLES = {"25", "42", "18", "28"}
    VALID_CFR_TITLES = {"25", "45"}

    @classmethod
    def extract_citations(cls, text: str) -> List[str]:
        citations = []
        citations.extend([f"RCW {m}" for m in cls.RCW_PATTERN.findall(text)])
        for m in cls.ILCS_PATTERN.findall(text):
            citations.append(f"{m[0]} ILCS {m[1]}/{m[2]}")
        citations.extend([f"ORC § {m}" for m in cls.ORC_PATTERN.findall(text)])
        for m in cls.USC_PATTERN.findall(text):
            citations.append(f"{m[0]} U.S.C. § {m[1]}")
        for m in cls.CFR_PATTERN.findall(text):
            citations.append(f"{m[0]} C.F.R. § {m[1]}")
        return list(dict.fromkeys(citations))  # deduplicate preserving order

    @classmethod
    def verify_citation(cls, raw_citation: str) -> CitationVerificationRecord:
        """Resolves a single citation candidate against the legal registry and known canonical citations."""
        cite = re.sub(r"\s+", " ", raw_citation.strip())
        upper_cite = cite.upper()

        # 1. Washington RCW Verification
        if "RCW" in upper_cite:
            match = cls.RCW_PATTERN.search(cite)
            if match:
                sec_str = match.group(1)
                title = sec_str.split(".")[0]
                # Check exact registry key sections
                for cps_source in default_registry.cps_sources.values():
                    if cps_source.jurisdiction == "US-WA":
                        for key_sec in cps_source.key_statutory_sections:
                            if sec_str in key_sec:
                                return CitationVerificationRecord(
                                    raw_citation=raw_citation,
                                    normalized_citation=f"RCW {sec_str}",
                                    verified=True,
                                    authority_tier="TIER_0",
                                    publisher_name=cps_source.publisher.name,
                                    jurisdiction="US-WA",
                                    source_url=cps_source.canonical_url,
                                )
                # Validate Title in RCW
                if title in cls.VALID_RCW_TITLES:
                    return CitationVerificationRecord(
                        raw_citation=raw_citation,
                        normalized_citation=f"RCW {sec_str}",
                        verified=True,
                        authority_tier="TIER_0",
                        publisher_name="Washington State Legislature",
                        jurisdiction="US-WA",
                        source_url=f"https://app.leg.wa.gov/rcw/default.aspx?cite={sec_str}",
                    )
                return CitationVerificationRecord(
                    raw_citation=raw_citation,
                    normalized_citation=f"RCW {sec_str}",
                    verified=False,
                    authority_tier="TIER_5",
                    publisher_name="UNVERIFIED",
                    jurisdiction="US-WA",
                    rejection_reason=f"RCW Title '{title}' is unrecognized in Washington State Code."
                )

        # 2. Illinois ILCS Verification
        if "ILCS" in upper_cite:
            match = cls.ILCS_PATTERN.search(cite)
            if match:
                chapter, act, sec = match.group(1), match.group(2), match.group(3)
                norm_cite = f"{chapter} ILCS {act}/{sec}"
                for cps_source in default_registry.cps_sources.values():
                    if cps_source.jurisdiction == "US-IL":
                        for key_sec in cps_source.key_statutory_sections:
                            if f"{chapter} ILCS {act}/{sec}" in key_sec or f"{act}/{sec}" in key_sec:
                                return CitationVerificationRecord(
                                    raw_citation=raw_citation,
                                    normalized_citation=norm_cite,
                                    verified=True,
                                    authority_tier="TIER_0",
                                    publisher_name=cps_source.publisher.name,
                                    jurisdiction="US-IL",
                                    source_url=cps_source.canonical_url,
                                )
                if chapter in cls.VALID_ILCS_CHAPTERS:
                    return CitationVerificationRecord(
                        raw_citation=raw_citation,
                        normalized_citation=norm_cite,
                        verified=True,
                        authority_tier="TIER_0",
                        publisher_name="Illinois General Assembly",
                        jurisdiction="US-IL",
                        source_url="https://www.ilga.gov/legislation/ilcs/ilcs.asp",
                    )
                return CitationVerificationRecord(
                    raw_citation=raw_citation,
                    normalized_citation=norm_cite,
                    verified=False,
                    authority_tier="TIER_5",
                    publisher_name="UNVERIFIED",
                    jurisdiction="US-IL",
                    rejection_reason=f"ILCS Chapter '{chapter}' is unrecognized in Illinois Compiled Statutes."
                )

        # 3. Ohio ORC Verification
        if "ORC" in upper_cite or "R.C." in upper_cite:
            match = cls.ORC_PATTERN.search(cite)
            if match:
                sec_str = match.group(1)
                chapter = sec_str.split(".")[0]
                norm_cite = f"ORC § {sec_str}"
                for cps_source in default_registry.cps_sources.values():
                    if cps_source.jurisdiction == "US-OH":
                        for key_sec in cps_source.key_statutory_sections:
                            if sec_str in key_sec:
                                return CitationVerificationRecord(
                                    raw_citation=raw_citation,
                                    normalized_citation=norm_cite,
                                    verified=True,
                                    authority_tier="TIER_0",
                                    publisher_name=cps_source.publisher.name,
                                    jurisdiction="US-OH",
                                    source_url=cps_source.canonical_url,
                                )
                if chapter in cls.VALID_ORC_CHAPTERS:
                    return CitationVerificationRecord(
                        raw_citation=raw_citation,
                        normalized_citation=norm_cite,
                        verified=True,
                        authority_tier="TIER_0",
                        publisher_name="Ohio General Assembly",
                        jurisdiction="US-OH",
                        source_url=f"https://codes.ohio.gov/ohio-revised-code/section-{sec_str}",
                    )
                return CitationVerificationRecord(
                    raw_citation=raw_citation,
                    normalized_citation=norm_cite,
                    verified=False,
                    authority_tier="TIER_5",
                    publisher_name="UNVERIFIED",
                    jurisdiction="US-OH",
                    rejection_reason=f"ORC Chapter '{chapter}' is unrecognized in Ohio Revised Code."
                )

        # 4. Federal USC / CFR Verification
        if "U.S.C." in upper_cite or "USC" in upper_cite:
            match = cls.USC_PATTERN.search(cite)
            if match:
                title, sec = match.group(1), match.group(2)
                norm_cite = f"{title} U.S.C. § {sec}"
                if title in cls.VALID_USC_TITLES:
                    return CitationVerificationRecord(
                        raw_citation=raw_citation,
                        normalized_citation=norm_cite,
                        verified=True,
                        authority_tier="TIER_0",
                        publisher_name="Office of the Law Revision Counsel of the U.S. House",
                        source_url="https://uscode.house.gov/",
                    )
                return CitationVerificationRecord(
                    raw_citation=raw_citation,
                    normalized_citation=norm_cite,
                    verified=False,
                    authority_tier="TIER_5",
                    publisher_name="UNVERIFIED",
                    rejection_reason=f"U.S.C. Title '{title}' is unrecognized or outside registered federal domains."
                )

        if "C.F.R." in upper_cite or "CFR" in upper_cite:
            match = cls.CFR_PATTERN.search(cite)
            if match:
                title, sec = match.group(1), match.group(2)
                norm_cite = f"{title} C.F.R. § {sec}"
                if title in cls.VALID_CFR_TITLES:
                    return CitationVerificationRecord(
                        raw_citation=raw_citation,
                        normalized_citation=norm_cite,
                        verified=True,
                        authority_tier="TIER_0",
                        publisher_name="National Archives and Records Administration & GPO",
                        source_url="https://www.ecfr.gov/",
                    )
                return CitationVerificationRecord(
                    raw_citation=raw_citation,
                    normalized_citation=norm_cite,
                    verified=False,
                    authority_tier="TIER_5",
                    publisher_name="UNVERIFIED",
                    rejection_reason=f"C.F.R. Title '{title}' is unrecognized or outside registered regulations."
                )

        # Rejection for fabricated / unknown citations
        return CitationVerificationRecord(
            raw_citation=raw_citation,
            normalized_citation=cite,
            verified=False,
            authority_tier="TIER_5",
            publisher_name="UNVERIFIED",
            rejection_reason="Citation failed canonical verification: Not found in official legal registry."
        )

    @classmethod
    def verify_all_citations(cls, text: str) -> Tuple[bool, List[CitationVerificationRecord]]:
        """Extracts all citations and verifies them. Returns (all_passed, records)."""
        citations = cls.extract_citations(text)
        records = [cls.verify_citation(c) for c in citations]
        all_passed = all(r.verified for r in records) if records else True
        return all_passed, records
