"""Fact, Allegation, Interpretation, and Unknown Extraction Classifier for Public Legal Navigator."""

import re
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel, Field


class StatementType(str, Enum):
    FACT = "FACT"                                  # Objective, stated verifiable events, actions, or documents
    USER_ALLEGATION = "USER_ALLEGATION"            # Disputed accusations, claims against third parties, unverified statements
    USER_INTERPRETATION = "USER_INTERPRETATION"    # User's personal deductions, legal opinions, beliefs, or emotional inferences
    UNKNOWN = "UNKNOWN"                            # Critical factual or legal prerequisites missing from the narrative


class DateCategory(str, Enum):
    EVENT_DATE = "EVENT_DATE"                      # Date of the core incident, removal, arrest, or notice
    FILING_DATE = "FILING_DATE"                    # Date court petition or lawsuit was filed
    HEARING_DATE = "HEARING_DATE"                  # Date of scheduled or past court appearance
    DECISION_DATE = "DECISION_DATE"                # Date order, judgment, or finding was entered
    LAW_EFFECTIVE_DATE = "LAW_EFFECTIVE_DATE"      # Date governing statute or regulation took effect


class ClassifiedStatement(BaseModel):
    statement_id: str
    text: str
    category: StatementType
    confidence: float = 0.9
    rationale: str


class ExtractedDate(BaseModel):
    raw_text: str
    iso_date: Optional[str] = None
    category: DateCategory
    description: str


class FactExtractionResult(BaseModel):
    facts: List[ClassifiedStatement] = Field(default_factory=list)
    allegations: List[ClassifiedStatement] = Field(default_factory=list)
    interpretations: List[ClassifiedStatement] = Field(default_factory=list)
    unknowns: List[str] = Field(default_factory=list)
    extracted_dates: List[ExtractedDate] = Field(default_factory=list)


class FactClassifier:
    """Extracts and separates objective facts, user allegations, subjective interpretations, and missing unknowns."""

    ALLEGATION_MARKERS = [
        "alleged", "alleging", "allegation", "claimed", "claims", "accused", "accusing",
        "lied", "lying", "false report", "falsely stated", "told the judge that",
        "caseworker claimed", "officer claimed", "said that i", "stated that i",
        "they said", "they claim", "he claimed", "she claimed", "maliciously",
        "unfounded report", "bogus report", "fabricated"
    ]

    INTERPRETATION_MARKERS = [
        "i feel", "i believe", "i think", "in my opinion", "they had no right",
        "they have no right", "they violated my rights", "this is unconstitutional",
        "this is illegal", "they are out to get me", "unfair", "unlawful",
        "kidnapped", "stolen from me", "corrupt", "railroaded", "set me up",
        "framed", "entitled to", "should not be allowed"
    ]

    DATE_PATTERNS = [
        (r'\b(20\d\d-\d{1,2}-\d{1,2})\b', "%Y-%m-%d"),
        (r'\b(\d{1,2}/\d{1,2}/20\d\d)\b', "%m/%d/%Y"),
        (r'\b((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+20\d\d)\b', "%B %d, %Y")
    ]

    @classmethod
    def classify_narrative(cls, narrative: str) -> FactExtractionResult:
        """Splits narrative into discrete sentences/clauses and categorizes each into FACT, ALLEGATION, INTERPRETATION, UNKNOWN."""
        if not narrative or not narrative.strip():
            return FactExtractionResult(
                unknowns=["No narrative supplied. Please provide a description of your situation."]
            )

        # 1. Normalize and split sentences
        raw_sentences = cls._split_into_propositions(narrative)
        facts: List[ClassifiedStatement] = []
        allegations: List[ClassifiedStatement] = []
        interpretations: List[ClassifiedStatement] = []

        for idx, sentence in enumerate(raw_sentences, 1):
            s_clean = sentence.strip()
            if not s_clean:
                continue

            s_lower = s_clean.lower()
            stmt_id = f"STMT-{idx:03d}"

            # Check Interpretation
            if any(marker in s_lower for marker in cls.INTERPRETATION_MARKERS):
                interpretations.append(ClassifiedStatement(
                    statement_id=stmt_id,
                    text=s_clean,
                    category=StatementType.USER_INTERPRETATION,
                    confidence=0.88,
                    rationale="Contains subjective deductions, emotional framing, or lay legal conclusions."
                ))
            # Check Allegation
            elif any(marker in s_lower for marker in cls.ALLEGATION_MARKERS):
                allegations.append(ClassifiedStatement(
                    statement_id=stmt_id,
                    text=s_clean,
                    category=StatementType.USER_ALLEGATION,
                    confidence=0.85,
                    rationale="Contains disputed accusations or unverified assertions about other parties."
                ))
            # Default Fact
            else:
                facts.append(ClassifiedStatement(
                    statement_id=stmt_id,
                    text=s_clean,
                    category=StatementType.FACT,
                    confidence=0.90,
                    rationale="States an objective occurrence, observation, or receipt of documents."
                ))

        # 2. Extract Dates
        extracted_dates = cls._extract_dates(narrative)

        # 3. Identify Missing Critical Unknowns
        unknowns = cls._identify_missing_unknowns(narrative, facts, extracted_dates)

        return FactExtractionResult(
            facts=facts,
            allegations=allegations,
            interpretations=interpretations,
            unknowns=unknowns,
            extracted_dates=extracted_dates
        )

    @classmethod
    def _split_into_propositions(cls, text: str) -> List[str]:
        """Splits narrative into discrete clauses and sentences using punctuation and conjunctions."""
        # Split on period, exclamation, semicolon, or newline
        raw_parts = re.split(r'[\r\n]+|[.;!]+', text)
        sentences = []
        for part in raw_parts:
            part = part.strip()
            if len(part) >= 4:
                sentences.append(part)
        return sentences

    @classmethod
    def _extract_dates(cls, text: str) -> List[ExtractedDate]:
        """Extracts date strings and attempts to categorize them based on sentence context."""
        dates_found: List[ExtractedDate] = []
        lower_text = text.lower()

        # Regex searches
        for pattern, date_fmt in cls.DATE_PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                raw_str = match.group(1).replace(",", "")
                iso_str = None
                try:
                    # Clean up month format
                    if "%B" in date_fmt:
                        parts = raw_str.split()
                        cleaned = f"{parts[0]} {parts[1]} {parts[2]}"
                        dt = datetime.strptime(cleaned, "%B %d %Y")
                        iso_str = dt.strftime("%Y-%m-%d")
                    else:
                        dt = datetime.strptime(raw_str, date_fmt)
                        iso_str = dt.strftime("%Y-%m-%d")
                except Exception:
                    iso_str = None

                # Determine context category
                surrounding = text[max(0, match.start() - 50):min(len(text), match.end() + 50)].lower()
                cat = DateCategory.EVENT_DATE
                desc = f"Date referenced in narrative: '{raw_str}'"

                if "hearing" in surrounding or "court date" in surrounding or "docket" in surrounding:
                    cat = DateCategory.HEARING_DATE
                    desc = f"Scheduled court appearance on {iso_str or raw_str}"
                elif "filed" in surrounding or "petition" in surrounding or "summons" in surrounding:
                    cat = DateCategory.FILING_DATE
                    desc = f"Document filing referenced on {iso_str or raw_str}"
                elif "order" in surrounding or "signed" in surrounding or "decision" in surrounding:
                    cat = DateCategory.DECISION_DATE
                    desc = f"Judicial order or agency decision date on {iso_str or raw_str}"
                elif "removed" in surrounding or "took" in surrounding or "visited" in surrounding or "arrived" in surrounding:
                    cat = DateCategory.EVENT_DATE
                    desc = f"Incident or removal occurrence on {iso_str or raw_str}"

                dates_found.append(ExtractedDate(
                    raw_text=raw_str,
                    iso_date=iso_str,
                    category=cat,
                    description=desc
                ))

        # Check for day of week mentions (e.g. "Tuesday afternoon")
        day_pattern = r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b(?:\s+(morning|afternoon|evening|night))?'
        for match in re.finditer(day_pattern, text, re.IGNORECASE):
            day_str = match.group(0)
            surrounding = text[max(0, match.start() - 40):min(len(text), match.end() + 40)].lower()
            cat = DateCategory.EVENT_DATE
            if "hearing" in surrounding:
                cat = DateCategory.HEARING_DATE
            dates_found.append(ExtractedDate(
                raw_text=day_str,
                iso_date=None,
                category=cat,
                description=f"Day of week referenced: {day_str}"
            ))

        return dates_found

    @classmethod
    def _identify_missing_unknowns(
        cls,
        narrative: str,
        facts: List[ClassifiedStatement],
        extracted_dates: List[ExtractedDate]
    ) -> List[str]:
        """Identifies critical unknowns that the user should be prompted to clarify."""
        unknowns = []
        low = narrative.lower()

        # 1. Court Order / Warrant presence
        if any(term in low for term in ["removed", "took my", "seized", "entered", "cps", "police"]):
            if not any(term in low for term in ["warrant", "court order", "order signed", "pick-up order", "ex parte"]):
                unknowns.append("Did the caseworker or police officer present a signed judicial warrant or emergency court order before entry/removal?")

        # 2. Formal Notice / Papers Served
        if not any(term in low for term in ["served", "summons", "petition copy", "formal notice", "papers", "paperwork"]):
            unknowns.append("Have you received formal written court papers, a copy of the petition, or an official notice of hearing?")

        # 3. Attorney Representation
        if not any(term in low for term in ["attorney", "lawyer", "public defender", "counsel", "represented"]):
            unknowns.append("Do you currently have an appointed attorney, public defender, or private counsel representing you?")

        # 4. Tribal / ICWA inquiry
        if any(term in low for term in ["child", "cps", "custody", "removal", "baby", "son", "daughter"]):
            if not any(term in low for term in ["tribe", "tribal", "indian", "native", "icwa", "enrolled"]):
                unknowns.append("Is the child or either parent an enrolled member or eligible for membership in a federally recognized Indian tribe (ICWA)?")

        # 5. Exact Dates
        if not any(d.iso_date for d in extracted_dates):
            unknowns.append("What is the exact calendar date (YYYY-MM-DD) when the key event or removal took place?")

        # 6. Prior Safety Plans
        if "cps" in low or "caseworker" in low:
            if "safety plan" not in low:
                unknowns.append("Did you sign any voluntary safety plan or agreement with the agency prior to this event?")

        return unknowns
