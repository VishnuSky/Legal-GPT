"""Final Review Agent: Inspects, validates, and gates generated legal responses.

Operates as a rigorous proposition validator and safety filter before response delivery.
Does NOT generate new legal authority.
"""

import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from core.jurisdiction import JurisdictionEngine
from core.citation_verifier import CitationVerifier
from core.legal_truth import LegalTruthObject


class FinalReviewResult(BaseModel):
    passed: bool
    failures: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    jurisdiction_confirmed: bool = False
    citation_coverage: float = 0.0

    # Fields for backward compatibility with FinalReviewVerdict
    is_approved: bool = True
    verified_citations: List[str] = Field(default_factory=list)
    rejected_citations: List[str] = Field(default_factory=list)
    jurisdiction_safe: bool = True
    hallucination_detected: bool = False
    epistemic_safety_passed: bool = True
    actionable_warnings: List[str] = Field(default_factory=list)


# Alias for backward compatibility
FinalReviewVerdict = FinalReviewResult


class FinalReviewAgent:
    """Structured proposition validator and final safety gatekeeper."""

    UNCERTAINTY_MARKERS = [
        "this is an inference",
        "not yet established",
        "likely",
        "uncertain",
        "estimated",
        "potential",
        "unconfirmed",
        "inferred",
        "hypothetical",
        "probable",
        "probability",
        "may",
        "might",
        "could indicate"
    ]

    CONSTITUTIONAL_PATTERNS = [
        re.compile(r"\bconstitutional\b", re.IGNORECASE),
        re.compile(r"\bdue process\b", re.IGNORECASE),
        re.compile(r"\bfourth amendment\b", re.IGNORECASE),
        re.compile(r"\bfourteenth amendment\b", re.IGNORECASE),
        re.compile(r"\bfifth amendment\b", re.IGNORECASE),
        re.compile(r"\bequal protection\b", re.IGNORECASE),
        re.compile(r"\bstrict scrutiny\b", re.IGNORECASE),
        re.compile(r"\bfundamental liberty interest\b", re.IGNORECASE),
        re.compile(r"\bfundamental right\b", re.IGNORECASE),
    ]

    T0_CONSTITUTIONAL_AUTHORITIES = [
        "U.S. Const",
        "U.S. Constitution",
        "United States Constitution",
        "Amend. XIV",
        "Amend. IV",
        "Santosky v. Kramer",
        "Troxel v. Granville",
        "Stanley v. Illinois",
        "Haaland v. Brackeen",
        "Mathews v. Eldridge",
        "Lassiter v. Department of Social Services",
        "In re Gault"
    ]

    @classmethod
    def review_response(
        cls,
        jurisdiction: str,
        citations: Optional[List[str]] = None,
        response_text: str = "",
        statements: Optional[List[Dict[str, Any]]] = None,
        truth_objects: Optional[List[LegalTruthObject]] = None,
        allow_unverified: bool = False
    ) -> FinalReviewResult:
        """Executes structured 5-point proposition validation:
        1. Every HOLDING or LAW statement has an associated authoritative citation.
        2. No INFERENCE statement is presented without an explicit uncertainty marker.
        3. No ALLEGATION statement is presented as FACT or LAW.
        4. Response contains at least one explicit jurisdiction statement.
        5. If a constitutional claim is made, at least one T0-tier authority reference is cited.
        """
        # Extract individual citations from compound strings
        raw_citations = citations or []
        normalized_cites: List[str] = []
        for c in raw_citations:
            extracted = CitationVerifier.extract_citations(c)
            if extracted:
                normalized_cites.extend(extracted)
            else:
                normalized_cites.append(c)
        normalized_cites = list(dict.fromkeys(normalized_cites))

        failures: List[str] = []
        warnings: List[str] = []
        verified: List[str] = []
        rejected: List[str] = []

        # 1. Verify citations
        for c in normalized_cites:
            rec = CitationVerifier.verify_citation(c)
            if rec.verified:
                verified.append(c)
            else:
                rejected.append(c)
                warnings.append(f"Rejected unverified citation: {c}")

        alien_cites = JurisdictionEngine.filter_out_of_jurisdiction_citations(normalized_cites, jurisdiction)
        jurisdiction_safe = len(alien_cites) == 0
        if not jurisdiction_safe:
            failures.append(f"Jurisdiction contamination detected: {alien_cites} found in {jurisdiction} context.")

        # 2. Extract and structure propositions if not provided explicitly
        props = list(statements) if statements else cls._extract_propositions_from_text(response_text)

        # Check 1: Every HOLDING or LAW statement has an associated citation
        holding_or_law_count = 0
        cited_holding_or_law_count = 0

        for p in props:
            p_type = p.get("classification") or p.get("type") or ""
            p_type_upper = p_type.upper()
            p_text = p.get("text") or p.get("claim") or ""
            p_cite = p.get("citation")

            if p_type_upper in ("HOLDING", "LAW"):
                holding_or_law_count += 1
                has_inline_cite = bool(p_cite) or cls._has_citation(p_text)
                if has_inline_cite:
                    cited_holding_or_law_count += 1
                else:
                    failures.append(
                        f"Check 1 Failure: {p_type_upper} statement lacks an associated authoritative citation: '{p_text[:80]}...'"
                    )

            # Check 2: No INFERENCE statement presented without an uncertainty marker
            if p_type_upper == "INFERENCE":
                has_marker = any(m in p_text.lower() for m in cls.UNCERTAINTY_MARKERS)
                if not has_marker:
                    failures.append(
                        f"Check 2 Failure: INFERENCE statement presented without explicit uncertainty marker: '{p_text[:80]}...'"
                    )

            # Check 3: No ALLEGATION presented as FACT or LAW (and no INFERENCE presented as LAW)
            presented_as = (p.get("presented_as") or "").upper()
            if p_type_upper == "ALLEGATION" and presented_as in ("FACT", "LAW"):
                failures.append(
                    f"Check 3 Failure: ALLEGATION statement presented as {presented_as}: '{p_text[:80]}...'"
                )
            elif p_type_upper == "INFERENCE" and presented_as == "LAW":
                failures.append(
                    f"Check 3 Failure: INFERENCE statement presented as LAW: '{p_text[:80]}...'"
                )

        # Check 4: Explicit jurisdiction statement present
        jurisdiction_confirmed = cls._check_jurisdiction_present(jurisdiction, response_text, citations)
        if not jurisdiction_confirmed:
            failures.append(
                f"Check 4 Failure: Response lacks an explicit jurisdiction statement for '{jurisdiction or 'UNSPECIFIED'}'."
            )

        # Check 5: Constitutional claim requires at least one T0-tier authority reference
        has_const_claim = any(pat.search(response_text) for pat in cls.CONSTITUTIONAL_PATTERNS)
        for p in props:
            if "constitutional" in (p.get("category") or "").lower() or (p.get("classification") or "").upper() == "CONSTITUTIONAL_STANDARD":
                has_const_claim = True
                break

        if has_const_claim:
            has_t0_ref = cls._check_t0_constitutional_authority(citations, truth_objects, response_text)
            if not has_t0_ref:
                failures.append(
                    "Check 5 Failure: Constitutional claim presented without at least one verified T0-tier constitutional authority reference."
                )

        # Citation coverage metric
        if holding_or_law_count > 0:
            coverage = round(cited_holding_or_law_count / holding_or_law_count, 3)
        elif citations:
            coverage = 1.0 if len(rejected) == 0 else round(len(verified) / max(1, len(citations)), 3)
        else:
            coverage = 0.0

        # Disclaimer check (warning only)
        has_disclaimer = any(w in response_text.lower() for w in ["legal advice", "research", "disclaimer", "informational"])
        if not has_disclaimer:
            warnings.append("Disclaimer missing in generated response.")

        passed = (len(failures) == 0) and (len(rejected) == 0 or allow_unverified)

        return FinalReviewResult(
            passed=passed,
            failures=failures,
            warnings=warnings,
            jurisdiction_confirmed=jurisdiction_confirmed,
            citation_coverage=coverage,
            is_approved=passed,
            verified_citations=verified,
            rejected_citations=rejected,
            jurisdiction_safe=jurisdiction_safe,
            hallucination_detected=len(rejected) > 0,
            epistemic_safety_passed=has_disclaimer,
            actionable_warnings=warnings
        )

    @classmethod
    def _extract_propositions_from_text(cls, text: str) -> List[Dict[str, Any]]:
        """Parses bracketed tags or sentences to identify proposition types."""
        props = []
        lines = text.split("\n")
        tag_pattern = re.compile(r"\[(HOLDING|LAW|INFERENCE|ALLEGATION|FACT)\]\s*(.*)", re.IGNORECASE)

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            match = tag_pattern.match(line_str)
            if match:
                ptype = match.group(1).upper()
                body = match.group(2).strip()

                # Check if tagged with secondary presented_as e.g. [INFERENCE] presented as [LAW]
                presented_as = None
                pres_match = re.search(r"presented as\s*\[?(LAW|FACT)\]?", body, re.IGNORECASE)
                if pres_match:
                    presented_as = pres_match.group(1).upper()

                props.append({
                    "classification": ptype,
                    "text": body,
                    "presented_as": presented_as,
                    "citation": None
                })
            else:
                # Heuristic proposition spotting for plain untagged text
                lower_l = line_str.lower()
                if "the court held that" in lower_l or "held that" in lower_l:
                    props.append({
                        "classification": "HOLDING",
                        "text": line_str,
                        "citation": None
                    })
                elif "is the governing law" in lower_l and "inference" in lower_l:
                    props.append({
                        "classification": "INFERENCE",
                        "text": line_str,
                        "presented_as": "LAW",
                        "citation": None
                    })

        return props

    @classmethod
    def _has_citation(cls, text: str) -> bool:
        """Detects whether text has an inline citation."""
        return len(CitationVerifier.extract_citations(text)) > 0 or "§" in text or "U.S." in text or "RCW" in text or "ILCS" in text or "ORC" in text

    @classmethod
    def _check_jurisdiction_present(cls, jurisdiction: str, text: str, citations: Optional[List[str]] = None) -> bool:
        """Verifies explicit jurisdiction confirmation in the response or verified citations."""
        if not jurisdiction or jurisdiction.upper() in ("UNKNOWN", "NONE", ""):
            return False

        clean_j = jurisdiction.strip().upper()
        lower_text = text.lower()

        # State code match e.g. "US-WA", "WA"
        state_code = clean_j.replace("US-", "")
        if f"us-{state_code.lower()}" in lower_text or f"jurisdiction: {state_code.lower()}" in lower_text:
            return True

        # State name match
        state_names = {
            "WA": "washington",
            "IL": "illinois",
            "OH": "ohio",
            "CA": "california",
            "TX": "texas",
            "NY": "new york",
            "FL": "florida",
            "US": "federal"
        }
        name = state_names.get(state_code, state_code.lower())
        if name in lower_text:
            return True

        # Explicit jurisdiction header match
        if "jurisdiction" in lower_text and state_code.lower() in lower_text:
            return True

        # Verified citation jurisdiction match
        if citations:
            matching_cites = [
                c for c in citations
                if CitationVerifier.verify_citation(c).jurisdiction in (f"US-{state_code}", state_code, "US")
            ]
            if len(matching_cites) > 0 and len(matching_cites) == len(citations):
                return True

        return False

    @classmethod
    def _check_t0_constitutional_authority(
        cls,
        citations: List[str],
        truth_objects: Optional[List[LegalTruthObject]],
        text: str
    ) -> bool:
        """Verifies at least one T0-tier constitutional reference exists."""
        # 1. Check citations list
        for c in citations:
            for auth in cls.T0_CONSTITUTIONAL_AUTHORITIES:
                if auth.lower() in c.lower():
                    return True

        # 2. Check truth objects
        if truth_objects:
            for t in truth_objects:
                if t.authority_tier == 0 or t.authority_type in ("constitution", "scotus_case"):
                    for auth in cls.T0_CONSTITUTIONAL_AUTHORITIES:
                        if auth.lower() in t.citation.lower() or auth.lower() in t.claim.lower():
                            return True

        # 3. Check inline text for explicit T0 citation
        for auth in cls.T0_CONSTITUTIONAL_AUTHORITIES:
            if auth.lower() in text.lower():
                return True

        return False

