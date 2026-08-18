"""Intake & Legal Issue Classifier (Facts, State, County, Court, Dates, Topics)."""

import re
from typing import List, Optional, Dict, Any
from datetime import date
from pydantic import BaseModel, Field
from cps.lifecycle import CPSStage


class IntakeClassificationResult(BaseModel):
    raw_query: str
    primary_state: Optional[str] = None # e.g. "WA", "IL", "OH"
    county: Optional[str] = None
    target_event_date: Optional[date] = None
    legal_domains: List[str] = Field(default_factory=list)
    identified_cps_stage: Optional[CPSStage] = None
    is_tribal_icwa_matter: bool = False
    is_interstate_matter: bool = False
    secondary_states: List[str] = Field(default_factory=list)
    extracted_facts: List[str] = Field(default_factory=list)
    needs_user_clarification: bool = False
    clarification_question: Optional[str] = None


class IntakeClassifier:
    STATE_KEYWORDS = {
        "WA": ["washington", "seattle", "skagit", "spokane", "tacoma", "king county", "pierce county", "snohomish", "olympia", "rcw", "dcyf"],
        "IL": ["illinois", "chicago", "cook county", "springfield", "dupage", "lake county", "peoria", "ilcs", "dcfs"],
        "OH": ["ohio", "columbus", "cleveland", "cuyahoga", "cincinnati", "franklin county", "hamilton county", "dayton", "orc", "odjfs"],
        "CA": ["california", "los angeles", "san francisco", "san diego", "sacramento", "orange county"],
        "TX": ["texas", "houston", "dallas", "austin", "san antonio", "travis county", "harris county"],
        "FL": ["florida", "miami", "orlando", "tampa", "jacksonville", "orange county fl"],
        "NY": ["new york", "nyc", "brooklyn", "queens", "manhattan", "bronx", "albany"],
    }

    COUNTY_KEYWORDS = {
        "Skagit": ["skagit", "mount vernon", "burlington", "sedro-woolley"],
        "Cook": ["cook county", "chicago"],
        "Cuyahoga": ["cuyahoga", "cleveland"],
        "King": ["king county", "seattle"],
    }

    @classmethod
    def classify(cls, query: str) -> IntakeClassificationResult:
        lower_q = query.lower()

        # 1. State detection
        detected_states = []
        for state_code, kws in cls.STATE_KEYWORDS.items():
            if any(kw in lower_q for kw in kws):
                detected_states.append(state_code)

        primary_state = detected_states[0] if detected_states else None
        secondary_states = detected_states[1:] if len(detected_states) > 1 else []

        # 2. County detection
        detected_county = None
        for county_name, kws in cls.COUNTY_KEYWORDS.items():
            if any(kw in lower_q for kw in kws):
                detected_county = county_name
                break

        # 3. Domain classification
        domains = []
        if any(w in lower_q for w in ["cps", "child", "custody", "removal", "foster", "shelter", "dependency", "dcyf", "dcfs", "tpr", "visitation", "parent"]):
            domains.append("child_welfare")
        if any(w in lower_q for w in ["divorce", "parenting plan", "child support", "custody"]):
            domains.append("family_law")

        # 4. CPS Stage detection
        stage = None
        if any(w in lower_q for w in ["took my child", "removed", "emergency custody", "police took", "without notice"]):
            stage = CPSStage.EMERGENCY_REMOVAL
        elif any(w in lower_q for w in ["72 hour", "shelter care", "temporary custody hearing", "48 hour"]):
            stage = CPSStage.SHELTER_CARE_HEARING
        elif any(w in lower_q for w in ["dependency petition", "fact finding", "adjudication", "allegations of abuse"]):
            stage = CPSStage.FACT_FINDING_ADJUDICATION
        elif any(w in lower_q for w in ["terminate", "tpr", "permanent custody", "termination of parental rights"]):
            stage = CPSStage.TPR_OR_GUARDIANSHIP

        # 5. ICWA & Interstate flags
        is_tribal = any(w in lower_q for w in ["tribal", "tribe", "indian child", "native american", "icwa", "wicwa", "reservation"])
        is_interstate = len(detected_states) > 1 or any(w in lower_q for w in ["another state", "moved to", "across state lines", "uccjea", "icpc"])

        needs_clarification = False
        clarification_q = None
        if not primary_state:
            needs_clarification = True
            clarification_q = "Please specify which state (and county, if applicable) your legal matter is in (e.g. Washington, Illinois, Ohio)."

        return IntakeClassificationResult(
            raw_query=query,
            primary_state=primary_state,
            county=detected_county,
            legal_domains=domains or ["general_legal"],
            identified_cps_stage=stage,
            is_tribal_icwa_matter=is_tribal,
            is_interstate_matter=is_interstate,
            secondary_states=secondary_states,
            extracted_facts=[query.strip()],
            needs_user_clarification=needs_clarification,
            clarification_question=clarification_q
        )
