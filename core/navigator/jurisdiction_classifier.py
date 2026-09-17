"""Jurisdiction Classification and Clarification Engine for Public Legal Navigator."""

import re
from typing import Optional, List, Dict, Any, Tuple
from pydantic import BaseModel, Field
from legal_registry.loader import default_registry


class JurisdictionClassificationResult(BaseModel):
    country: str = "US"
    state: Optional[str] = None                     # 2-letter state code e.g. "WA", "IL", "OH"
    state_name: Optional[str] = None                # Full state name e.g. "Washington"
    tribal_jurisdiction: Optional[str] = None       # e.g. "Puyallup Tribe", "Navajo Nation"
    county: Optional[str] = None                    # e.g. "Skagit", "Cook", "Cuyahoga"
    city: Optional[str] = None                      # e.g. "Mount Vernon", "Chicago"
    court: Optional[str] = None                     # e.g. "Superior Court (Juvenile Division)"
    agency: Optional[str] = None                    # e.g. "DCYF", "DCFS", "CPS", "Police"
    administrative_body: Optional[str] = None       # e.g. "Office of Administrative Hearings"
    is_known: bool = False
    clarification_questions: List[str] = Field(default_factory=list)
    normalized_code: str = "UNKNOWN"                # e.g. "US-WA", "US-IL", "UNKNOWN"


class JurisdictionClassifier:
    """Classifies geographic, tribal, judicial, and agency jurisdiction. Never guesses silently."""

    STATE_NAMES: Dict[str, str] = {
        "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA",
        "colorado": "CO", "connecticut": "CT", "delaware": "DE", "florida": "FL", "georgia": "GA",
        "hawaii": "HI", "idaho": "ID", "illinois": "IL", "indiana": "IN", "iowa": "IA",
        "kansas": "KS", "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
        "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS", "missouri": "MO",
        "montana": "MT", "nebraska": "NE", "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ",
        "new mexico": "NM", "new york": "NY", "north carolina": "NC", "north dakota": "ND", "ohio": "OH",
        "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
        "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT", "vermont": "VT",
        "virginia": "VA", "washington": "WA", "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY",
        "district of columbia": "DC"
    }

    AGENCY_MAP = {
        "dcyf": ("WA", "Department of Children, Youth, and Families (DCYF)"),
        "dcfs": ("IL", "Department of Children and Family Services (DCFS)"),
        "dfps": ("TX", "Department of Family and Protective Services (DFPS)"),
        "acs": ("NY", "Administration for Children's Services (ACS)"),
        "cps": (None, "Child Protective Services (CPS)"),
        "dhs": (None, "Department of Human Services (DHS)"),
        "police": (None, "Law Enforcement / Police Department"),
        "sheriff": (None, "County Sheriff's Office"),
        "housing authority": (None, "Public Housing Authority (PHA)")
    }

    COURT_PATTERNS = [
        (r'\b(Superior Court(?:\s+of\s+[\w\s]+)?)\b', "Superior Court"),
        (r'\b(Circuit Court(?:\s+of\s+[\w\s]+)?)\b', "Circuit Court"),
        (r'\b(Family Court(?:\s+of\s+[\w\s]+)?)\b', "Family Court"),
        (r'\b(Juvenile Court(?:\s+of\s+[\w\s]+)?)\b', "Juvenile Court"),
        (r'\b(District Court(?:\s+of\s+[\w\s]+)?)\b', "District Court"),
        (r'\b(Tribal Court(?:\s+of\s+[\w\s]+)?)\b', "Tribal Court")
    ]

    COMMON_COUNTIES = [
        ("Skagit", "WA"), ("King", "WA"), ("Pierce", "WA"), ("Snohomish", "WA"), ("Spokane", "WA"), ("Clark", "WA"),
        ("Cook", "IL"), ("DuPage", "IL"), ("Lake", "IL"), ("Will", "IL"), ("Kane", "IL"),
        ("Cuyahoga", "OH"), ("Franklin", "OH"), ("Hamilton", "OH"), ("Montgomery", "OH"), ("Summit", "OH"),
        ("Los Angeles", "CA"), ("Orange", "CA"), ("San Diego", "CA"), ("Riverside", "CA"), ("Santa Clara", "CA"),
        ("Harris", "TX"), ("Dallas", "TX"), ("Tarrant", "TX"), ("Bexar", "TX"), ("Travis", "TX"),
        ("New York", "NY"), ("Kings", "NY"), ("Bronx", "NY"), ("Queens", "NY"), ("Suffolk", "NY"),
        ("Miami-Dade", "FL"), ("Broward", "FL"), ("Palm Beach", "FL"), ("Hillsborough", "FL"), ("Orange", "FL")
    ]

    TRIBAL_ENTITIES = [
        "Puyallup", "Yakama", "Tulalip", "Navajo", "Cherokee", "Sioux", "Blackfeet", "Lummi",
        "Muckleshoot", "Quinault", "Choctaw", "Chickasaw", "Muscogee", "Seminole", "Hopi", "Apache"
    ]

    @classmethod
    def classify_jurisdiction(
        cls,
        narrative: str,
        override_state: Optional[str] = None,
        override_county: Optional[str] = None,
        override_tribe: Optional[str] = None
    ) -> JurisdictionClassificationResult:
        """Determines target jurisdiction. If unknown, sets is_known=False and generates clarifying question."""
        text_lower = narrative.lower()

        # 1. State resolution
        detected_state: Optional[str] = None
        state_name: Optional[str] = None

        # Check explicit override first
        if override_state:
            norm_ov = override_state.strip().upper().replace("US-", "")
            if norm_ov in default_registry.state_matrix or norm_ov in ("US", "DC"):
                detected_state = norm_ov

        # Scan text for state names
        if not detected_state:
            for s_name, code in cls.STATE_NAMES.items():
                pattern = rf'\b{re.escape(s_name)}\b'
                if re.search(pattern, text_lower):
                    detected_state = code
                    state_name = s_name.title()
                    break

        # Scan text for standalone state postal codes (e.g. " in WA ", " Cook County, IL")
        if not detected_state:
            for code in cls.STATE_NAMES.values():
                pattern = rf'\b{code}\b'
                if re.search(pattern, narrative):
                    detected_state = code
                    break

        # 2. County resolution
        detected_county: Optional[str] = override_county
        if not detected_county:
            for c_name, c_state in cls.COMMON_COUNTIES:
                pattern = rf'\b{re.escape(c_name)}(?:\s+County)?\b'
                if re.search(pattern, narrative, re.IGNORECASE):
                    detected_county = c_name
                    # If state wasn't known yet, infer from distinct county
                    if not detected_state:
                        detected_state = c_state
                    break

        # If full state name not yet resolved
        if detected_state and not state_name:
            for s_name, code in cls.STATE_NAMES.items():
                if code == detected_state:
                    state_name = s_name.title()
                    break

        # 3. Tribal Jurisdiction
        detected_tribe: Optional[str] = override_tribe
        if not detected_tribe:
            for tribe in cls.TRIBAL_ENTITIES:
                if re.search(rf'\b{re.escape(tribe)}\b', narrative, re.IGNORECASE):
                    detected_tribe = f"{tribe} Tribe / Nation"
                    break
            if not detected_tribe and "tribal court" in text_lower:
                detected_tribe = "Federally Recognized Tribe (Unspecified)"

        # 4. Court resolution
        detected_court: Optional[str] = None
        for pattern, court_type in cls.COURT_PATTERNS:
            match = re.search(pattern, narrative, re.IGNORECASE)
            if match:
                detected_court = match.group(1).strip()
                break

        # 5. Agency resolution
        detected_agency: Optional[str] = None
        for kw, (implied_state, full_name) in cls.AGENCY_MAP.items():
            if re.search(rf'\b{re.escape(kw)}\b', text_lower):
                detected_agency = full_name
                if implied_state and not detected_state:
                    detected_state = implied_state
                    state_name = [k.title() for k, v in cls.STATE_NAMES.items() if v == implied_state][0]
                break

        # 6. Evaluate certainty & missing jurisdiction
        is_known = bool(detected_state)
        clarification_questions = []

        if not is_known:
            clarification_questions.append(
                "What state (and county or municipality) did this legal event occur in? "
                "Legal rights, court rules, and emergency deadlines differ dramatically between jurisdictions, "
                "and Legal-GPT cannot evaluate your rights without knowing your state."
            )
        elif not detected_county:
            clarification_questions.append(
                f"Which county in {state_name or detected_state} is handling this matter? "
                "Local court procedures, self-help facilitator desks, and legal aid programs are organized by county."
            )

        norm_code = f"US-{detected_state}" if detected_state else "UNKNOWN"

        return JurisdictionClassificationResult(
            country="US",
            state=detected_state,
            state_name=state_name,
            tribal_jurisdiction=detected_tribe,
            county=detected_county,
            court=detected_court,
            agency=detected_agency,
            is_known=is_known,
            clarification_questions=clarification_questions,
            normalized_code=norm_code
        )
