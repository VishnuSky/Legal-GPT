"""Jurisdiction Lock, Routing, and Contamination Detector."""

from typing import List, Optional, Set
from pydantic import BaseModel, Field


class JurisdictionContext(BaseModel):
    primary_state: Optional[str] = None # e.g. "WA", "IL", "OH"
    county: Optional[str] = None # e.g. "Skagit", "Cook", "Cuyahoga"
    court_level: Optional[str] = None # e.g. "juvenile_dependency", "superior", "appellate"
    federal_district: Optional[str] = None
    is_tribal_matter: bool = False
    tribe_name: Optional[str] = None
    is_interstate: bool = False
    secondary_states: List[str] = Field(default_factory=list)
    locked: bool = False


class JurisdictionEngine:
    STATE_CITATION_PREFIXES = {
        "WA": ["RCW", "WAC", "Wn.2d", "Wn. App.", "Washington"],
        "IL": ["ILCS", "Ill. Adm. Code", "Ill. S. Ct.", "IL App", "Illinois"],
        "OH": ["ORC", "OAC", "Ohio St.3d", "Ohio App.", "Ohio Juv. R.", "Ohio"],
        "CA": ["Cal.", "Cal. App.", "Cal. Civ. Code", "Cal. Welf. & Inst. Code", "California"],
        "NY": ["N.Y.", "N.Y.S.", "NY CLS", "New York"],
        "TX": ["Tex.", "Tex. Fam. Code", "Texas"],
        "US": ["U.S.C.", "C.F.R.", "U.S.", "F.4th", "F.3d", "F. Supp.", "Fed. Reg."],
    }

    TRIBAL_CITATION_PREFIXES = {
        "TRIBAL-NAVAJO": ["N.N.C.", "Navajo Nation Code", "Navajo"],
        "TRIBAL-PUYALLUP": ["PTC", "Puyallup Tribal Code", "Puyallup"],
        "TRIBAL-CHEROKEE": ["C.N.C.A.", "Cherokee Nation Code", "Cherokee"],
    }

    @classmethod
    def lock_jurisdiction(
        cls,
        state: str,
        county: Optional[str] = None,
        is_tribal: bool = False,
        tribe_name: Optional[str] = None
    ) -> JurisdictionContext:
        state_code = state.strip().upper()
        # If state starts with TRIBAL- or tribe_name is provided, set is_tribal=True
        tribal_flag = is_tribal or state_code.startswith("TRIBAL") or bool(tribe_name)
        inferred_tribe = tribe_name
        if state_code.startswith("TRIBAL-"):
            inferred_tribe = state_code.split("TRIBAL-", 1)[1]

        return JurisdictionContext(
            primary_state=state_code,
            county=county,
            is_tribal_matter=tribal_flag,
            tribe_name=inferred_tribe,
            locked=True
        )

    @classmethod
    def evaluate_jurisdiction_completeness(cls, context: JurisdictionContext) -> dict:
        """Evaluates whether jurisdiction is sufficiently specific or requires abstention/clarification."""
        if not context.locked or not context.primary_state or context.primary_state in ("UNKNOWN", "UNSPECIFIED", ""):
            return {
                "valid": False,
                "status": "ABSTAIN",
                "reason": "Jurisdiction is unknown or unspecified. A controlling state or sovereign tribal nation must be provided to prevent legal contamination."
            }
        return {"valid": True, "status": "PROCEED", "reason": None}

    @classmethod
    def classify_authority_layer(cls, citation: str) -> dict:
        """Classifies a legal citation into its governing authority layer and jurisdiction."""
        upper_cite = citation.upper()

        # Check Treaties
        if "STAT." in upper_cite:
            return {
                "layer": "TREATY",
                "jurisdiction": "US-TREATY",
                "label": "FEDERAL_TREATY",
                "description": "Article VI Supremacy Clause Treaty Authority"
            }

        # Check Tribal Codes
        for t_nation, prefixes in cls.TRIBAL_CITATION_PREFIXES.items():
            for p in prefixes:
                if p.upper() in upper_cite:
                    return {
                        "layer": "TRIBAL",
                        "jurisdiction": t_nation,
                        "label": f"TRIBAL_{t_nation.replace('TRIBAL-', '')}",
                        "description": f"Sovereign Tribal Law ({t_nation})"
                    }

        # Check Federal ICWA & Federal authorities
        if any(fed in upper_cite for fed in ("U.S.C.", "C.F.R.", "U.S.", "F.4TH", "F.3D", "F. SUPP.", "FED. REG.")):
            is_icwa = "25 U.S.C." in upper_cite or "25 C.F.R." in upper_cite
            return {
                "layer": "FEDERAL",
                "jurisdiction": "US",
                "label": "FEDERAL_ICWA" if is_icwa else "FEDERAL",
                "description": "Federal Statutory / Regulatory Floor"
            }

        # Check State Authorities
        for st, prefixes in cls.STATE_CITATION_PREFIXES.items():
            if st == "US":
                continue
            for p in prefixes:
                if p.upper() in upper_cite:
                    is_state_icwa = (st == "WA" and "13.38" in upper_cite) or (st == "CA" and ("224" in upper_cite or "CAL-ICWA" in upper_cite))
                    return {
                        "layer": "STATE",
                        "jurisdiction": f"US-{st}",
                        "label": f"STATE_ICWA_{st}" if is_state_icwa else f"STATE_{st}",
                        "description": f"State Law Overlay ({st})"
                    }

        return {
            "layer": "UNKNOWN",
            "jurisdiction": "UNKNOWN",
            "label": "UNCLASSIFIED",
            "description": "Unclassified Legal Authority"
        }

    @classmethod
    def detect_cross_contamination(cls, context: JurisdictionContext, citations: List[str]) -> List[str]:
        """Detects if citations from other non-applicable jurisdictions are erroneously included."""
        if not context.locked or not context.primary_state:
            return []

        violations = []
        target_state = context.primary_state
        is_tribal = context.is_tribal_matter or target_state.startswith("TRIBAL")

        for cite in citations:
            classification = cls.classify_authority_layer(cite)

            # Rule 1: Tribal Law Request cannot silently substitute state law
            if is_tribal:
                if classification["layer"] == "STATE":
                    allowed_state = classification["jurisdiction"].replace("US-", "") in context.secondary_states
                    if not allowed_state:
                        violations.append(
                            f"Contamination error: State law citation '{cite}' cannot silently substitute for Tribal law in {context.tribe_name or target_state}."
                        )
                        continue

                # Rule 2: Request involving one Nation cannot silently use another Nation's code
                if classification["layer"] == "TRIBAL":
                    cite_nation = classification["jurisdiction"]
                    target_nation_norm = target_state if target_state.startswith("TRIBAL-") else f"TRIBAL-{(context.tribe_name or '').upper()}"
                    if cite_nation != target_nation_norm and cite_nation not in context.secondary_states:
                        violations.append(
                            f"Cross-nation contamination error: Citation '{cite}' belongs to {cite_nation}, which cannot be applied to sovereign nation {context.tribe_name or target_state}."
                        )
                        continue

            # Rule 3: State Law Request cannot silently include other state laws
            elif not is_tribal:
                target_norm = target_state.replace("US-", "")
                for other_state, prefixes in cls.STATE_CITATION_PREFIXES.items():
                    if other_state in (target_state, target_norm, "US"):
                        continue  # Federal or target state is applicable
                    if other_state in context.secondary_states or f"US-{other_state}" in context.secondary_states:
                        continue  # Allowed if explicitly multi-state matter
                    for prefix in prefixes:
                        if prefix in cite:
                            violations.append(
                                f"Contamination error: Citation '{cite}' belongs to {other_state}, but jurisdiction is locked to {target_state}."
                            )
                            break

                # State law cannot silently use tribal code without explicit tribal overlay
                if classification["layer"] == "TRIBAL" and classification["jurisdiction"] not in context.secondary_states:
                    violations.append(
                        f"Contamination error: Tribal code citation '{cite}' belongs to {classification['jurisdiction']}, but jurisdiction is locked to state {target_state}."
                    )

        return violations

    @classmethod
    def filter_out_of_jurisdiction_citations(cls, citations: List[str], target_state: str) -> List[str]:
        """Returns list of cross-contamination violation messages for out-of-jurisdiction citations."""
        ctx = cls.lock_jurisdiction(target_state)
        return cls.detect_cross_contamination(ctx, citations)
