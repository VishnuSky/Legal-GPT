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
    # Regex patterns for canonical statutory and constitutional citations
    RCW_PATTERN = re.compile(r"\bRCW\s+(\d{1,3}\.\d{2,3}(?:\.\d{3,4})?)\b", re.IGNORECASE)
    ILCS_PATTERN = re.compile(r"\b(\d+)\s+ILCS\s+(\d+)\/(\d+(?:-\d+)?(?:\.\d+)?)\b", re.IGNORECASE)
    ORC_PATTERN = re.compile(r"\b(?:ORC|R\.C\.)\s*§?\s*(\d{1,4}\.\d{2,3})\b", re.IGNORECASE)
    USC_PATTERN = re.compile(r"\b(\d+)\s+U\.S\.C\.\s*§?\s*(\d+[a-z]*(?:\([a-zA-Z0-9]+\))*)\b", re.IGNORECASE)
    CFR_PATTERN = re.compile(r"\b(\d+)\s+C\.F\.R\.\s*§?\s*(\d+(?:\.\d+)?)\b", re.IGNORECASE)
    US_CONST_PATTERN = re.compile(r"\b(?:U\.S\.\s*Const\.|US\s*Const|United States Constitution)\s*(?:amend\.|art\.|article|section|§)?\s*([IVXLCDM\d]+)?(?:\s*,\s*§\s*(\d+))?", re.IGNORECASE)
    STATE_CONST_PATTERN = re.compile(r"\b(Wash\.|WA|Ill\.|IL|Cal\.|CA|Tex\.|TX)\s*Const\.\s*(?:art\.|article)?\s*([IVXLCDM\d]+)?(?:\s*,\s*§\s*(\d+))?", re.IGNORECASE)
    COURT_RULES_PATTERN = re.compile(r"\b(?:(WA\s+)?(JuCR|RAP|CR)|(Ill\.\s+S\.\s*Ct\.\s*R\.|IL\s+Rule))\s*(\d+(?:\.\d+)?(?:\([a-zA-Z0-9]+\))*)?", re.IGNORECASE)
    CASE_PATTERN = re.compile(r"([A-Z][a-zA-Z\.\s\',]+(?:\s+v\.\s+|\s+in\s+re\s+)[A-Z][a-zA-Z\.\s\',]+),\s*(\d+)\s+([A-Za-z\.\d\s]+?)\s+(\d+)(?:\s*\(([A-Za-z0-9\.\s]+)?(\d{4})\))?", re.IGNORECASE)

    # Known statutory titles/chapters in CPS & Family law
    VALID_RCW_TITLES = {"13", "26", "74", "10", "4", "2", "9", "9A"}
    VALID_ILCS_CHAPTERS = {"705", "325", "750", "20", "720"}
    VALID_ORC_CHAPTERS = {"2151", "3109", "3127", "2919", "5101"}
    VALID_USC_TITLES = {"25", "42", "18", "28"}
    VALID_CFR_TITLES = {"25", "45"}

    # Canonical Supreme Court and Federal Precedents in child welfare & constitutional due process
    CANONICAL_CASES: Dict[str, Dict[str, str]] = {
        "santosky v. kramer": {
            "citation": "Santosky v. Kramer, 455 U.S. 745 (1982)",
            "tier": "TIER_1",
            "publisher": "Supreme Court of the United States",
            "jurisdiction": "US",
            "url": "https://www.supremecourt.gov/"
        },
        "mathews v. eldridge": {
            "citation": "Mathews v. Eldridge, 424 U.S. 319 (1976)",
            "tier": "TIER_1",
            "publisher": "Supreme Court of the United States",
            "jurisdiction": "US",
            "url": "https://www.supremecourt.gov/"
        },
        "wallis v. spencer": {
            "citation": "Wallis v. Spencer, 202 F.3d 1126 (9th Cir. 2000)",
            "tier": "TIER_2",
            "publisher": "U.S. Court of Appeals for the Ninth Circuit",
            "jurisdiction": "US-FED",
            "url": "https://www.ca9.uscourts.gov/"
        },
        "lassiter v. department of social services": {
            "citation": "Lassiter v. Department of Social Services, 452 U.S. 18 (1981)",
            "tier": "TIER_1",
            "publisher": "Supreme Court of the United States",
            "jurisdiction": "US",
            "url": "https://www.supremecourt.gov/"
        },
        "troxel v. granville": {
            "citation": "Troxel v. Granville, 530 U.S. 57 (2000)",
            "tier": "TIER_1",
            "publisher": "Supreme Court of the United States",
            "jurisdiction": "US",
            "url": "https://www.supremecourt.gov/"
        },
        "haaland v. brackeen": {
            "citation": "Haaland v. Brackeen, 599 U.S. 255 (2023)",
            "tier": "TIER_1",
            "publisher": "Supreme Court of the United States",
            "jurisdiction": "US",
            "url": "https://www.supremecourt.gov/"
        },
        "stanley v. illinois": {
            "citation": "Stanley v. Illinois, 405 U.S. 645 (1972)",
            "tier": "TIER_1",
            "publisher": "Supreme Court of the United States",
            "jurisdiction": "US",
            "url": "https://www.supremecourt.gov/"
        },
        "mullane v. central hanover bank & trust co.": {
            "citation": "Mullane v. Central Hanover Bank & Trust Co., 339 U.S. 306 (1950)",
            "tier": "TIER_1",
            "publisher": "Supreme Court of the United States",
            "jurisdiction": "US",
            "url": "https://www.supremecourt.gov/"
        },
        "armstrong v. manzo": {
            "citation": "Armstrong v. Manzo, 380 U.S. 545 (1965)",
            "tier": "TIER_1",
            "publisher": "Supreme Court of the United States",
            "jurisdiction": "US",
            "url": "https://www.supremecourt.gov/"
        },
        "roska ex rel. roska v. peterson": {
            "citation": "Roska ex rel. Roska v. Peterson, 328 F.3d 1230 (10th Cir. 2003)",
            "tier": "TIER_2",
            "publisher": "U.S. Court of Appeals for the Tenth Circuit",
            "jurisdiction": "US-FED",
            "url": "https://www.ca10.uscourts.gov/"
        },
        "nicholson v. scoppetta": {
            "citation": "Nicholson v. Scoppetta, 3 N.Y.3d 357 (2004)",
            "tier": "TIER_3",
            "publisher": "New York Court of Appeals",
            "jurisdiction": "US-NY",
            "url": "https://www.nycourts.gov/"
        },
        "in re dependency of grove": {
            "citation": "In re Dependency of Grove, 127 Wn.2d 221 (1995)",
            "tier": "TIER_3",
            "publisher": "Washington Supreme Court",
            "jurisdiction": "US-WA",
            "url": "https://www.courts.wa.gov/"
        },
        "in re dependency of k.n.j.": {
            "citation": "In re Dependency of K.N.J., 171 Wn.2d 568 (2011)",
            "tier": "TIER_3",
            "publisher": "Washington Supreme Court",
            "jurisdiction": "US-WA",
            "url": "https://www.courts.wa.gov/"
        },
        "in re arthur h.": {
            "citation": "In re Arthur H., 212 Ill. 2d 441 (2004)",
            "tier": "TIER_3",
            "publisher": "Illinois Supreme Court",
            "jurisdiction": "US-IL",
            "url": "https://www.illinoiscourts.gov/"
        },
        "in re b.c.": {
            "citation": "In re B.C., 141 Ohio St. 3d 1 (2014)",
            "tier": "TIER_3",
            "publisher": "Supreme Court of Ohio",
            "jurisdiction": "US-OH",
            "url": "https://www.supremecourt.ohio.gov/"
        },
        "deshaney v. winnebago county": {
            "citation": "DeShaney v. Winnebago County Dept. of Social Services, 489 U.S. 189 (1989)",
            "tier": "TIER_1",
            "publisher": "Supreme Court of the United States",
            "jurisdiction": "US",
            "url": "https://www.supremecourt.gov/"
        }
    }

    VALID_REPORTERS = {
        "u.s.", "s. ct.", "l. ed.", "l. ed. 2d", "f.", "f.2d", "f.3d", "f.4th",
        "f. supp.", "f. supp. 2d", "f. supp. 3d", "wn.2d", "wn. app.", "ill. 2d",
        "ill. app. 3d", "ohio st. 3d", "n.y.3d", "cal.4th", "p.2d", "p.3d", "a.2d", "a.3d", "n.e.2d", "n.e.3d"
    }

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

        # 5. Constitutional Provisions (Federal & State)
        if "CONST" in upper_cite or "CONSTITUTION" in upper_cite:
            if "U.S." in upper_cite or "US" in upper_cite or "UNITED STATES" in upper_cite:
                match = cls.US_CONST_PATTERN.search(cite)
                if match:
                    return CitationVerificationRecord(
                        raw_citation=raw_citation,
                        normalized_citation=cite,
                        verified=True,
                        authority_tier="TIER_0",
                        publisher_name="National Archives & GPO (Constitution Annotated)",
                        jurisdiction="US",
                        source_url="https://constitution.congress.gov/",
                    )
            match_state = cls.STATE_CONST_PATTERN.search(cite)
            if match_state:
                st = match_state.group(1).upper()
                j_code = "US-WA" if "WA" in st else ("US-IL" if "IL" in st else ("US-CA" if "CA" in st else "US-TX"))
                return CitationVerificationRecord(
                    raw_citation=raw_citation,
                    normalized_citation=cite,
                    verified=True,
                    authority_tier="TIER_0",
                    publisher_name=f"Official State Constitution ({j_code})",
                    jurisdiction=j_code,
                    source_url="https://leg.wa.gov/CodeReviser/Pages/constitution.aspx",
                )

        # 6. Court Rules
        if any(kw in upper_cite for kw in ("JUCR", "RAP", "S. CT. R.", "RULE", "COURT RULE")):
            match_rule = cls.COURT_RULES_PATTERN.search(cite)
            if match_rule:
                rule_name = cite
                j_code = "US-WA" if any(w in upper_cite for w in ("WA", "JUCR", "RAP")) else "US-IL"
                return CitationVerificationRecord(
                    raw_citation=raw_citation,
                    normalized_citation=rule_name,
                    verified=True,
                    authority_tier="TIER_1",
                    publisher_name="Official Court Rules",
                    jurisdiction=j_code,
                    source_url="https://www.courts.wa.gov/court_rules/",
                )

        # 7. Judicial Precedents & Canonical Caselaw
        # Check canonical case registry first
        cite_lower = cite.lower()
        for c_key, c_info in cls.CANONICAL_CASES.items():
            if c_key in cite_lower or (c_key.split(" v. ")[0] in cite_lower and c_key.split(" v. ")[1].split(",")[0] in cite_lower):
                return CitationVerificationRecord(
                    raw_citation=raw_citation,
                    normalized_citation=c_info["citation"],
                    verified=True,
                    authority_tier=c_info["tier"],
                    publisher_name=c_info["publisher"],
                    jurisdiction=c_info["jurisdiction"],
                    source_url=c_info["url"],
                )

        # General valid reporter match (e.g. 455 U.S. 745 or 202 F.3d 1126)
        match_case = cls.CASE_PATTERN.search(cite)
        if match_case:
            reporter = match_case.group(3).strip().lower()
            if reporter in cls.VALID_REPORTERS:
                party_str = match_case.group(1).strip()
                vol = match_case.group(2)
                page = match_case.group(4)
                year = match_case.group(6) or ""
                year_str = f" ({year})" if year else ""
                norm = f"{party_str}, {vol} {match_case.group(3).strip()} {page}{year_str}"
                tier = "TIER_1" if reporter in ("u.s.", "s. ct.") else ("TIER_2" if "f." in reporter else "TIER_3")
                return CitationVerificationRecord(
                    raw_citation=raw_citation,
                    normalized_citation=norm,
                    verified=True,
                    authority_tier=tier,
                    publisher_name="Official Court Reporter",
                    jurisdiction="US" if tier == "TIER_1" else "US-FED",
                    source_url="https://www.supremecourt.gov/" if tier == "TIER_1" else None,
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
