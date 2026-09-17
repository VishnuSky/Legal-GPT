"""Legal Evidence Bridge: Connects evidence records to legal elements, authority, missing proof, and research questions."""

import re
from typing import Dict, List, Optional, Any

from core.evidence.models import (
    EpistemicClassification,
    EvidenceVerificationState,
    EvidenceRecord,
    LegalElement,
    LegalBridgeLink,
    EvidenceBridgeEvaluation,
)
from core.evidence.registry import LegalElementRegistry


class LegalEvidenceBridge:
    """Safely bridges evidence descriptions to statutory elements and missing proof analysis."""

    # Public-safety pattern checks: Detect real SSNs or confidential file paths
    SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
    PRIVATE_PATH_PATTERN = re.compile(r"(?:/private_case_vault/|/confidential_evidence/|[a-zA-Z]:[\\/](?!scratch)).*\.(?:pdf|docx|jpg|png|mp3|wav|eml)", re.IGNORECASE)

    @classmethod
    def bridge_record(
        cls,
        evidence: EvidenceRecord,
        custom_element: Optional[LegalElement] = None
    ) -> LegalBridgeLink:
        """Executes the 6-stage legal bridge for a single evidence item:
        Evidence -> Fact -> Legal Element -> Authority -> Missing Evidence -> Research Question
        """
        cls._verify_public_data_safety(evidence)

        # 1. Fact Statement derivation
        fact_statement = cls._derive_fact_statement(evidence)

        # 2. Legal Element & Authority resolution
        element = custom_element or LegalElementRegistry.find_matching_element(evidence.associated_issue)
        authority = element.governing_authority

        # 3. Missing Evidence analysis
        missing_evidence = cls._analyze_missing_evidence(evidence, element)

        # 4. Research Questions
        research_questions = list(element.standard_research_questions)

        return LegalBridgeLink(
            evidence=evidence,
            fact_statement=fact_statement,
            legal_element=element.element_name,
            authority=authority,
            missing_evidence=missing_evidence,
            research_questions=research_questions,
            epistemic_classification=evidence.classification
        )

    @classmethod
    def evaluate_collection(
        cls,
        case_reference: str,
        jurisdiction: str,
        records: List[EvidenceRecord]
    ) -> EvidenceBridgeEvaluation:
        """Evaluates an array of evidence records, building bridge links and aggregating evidentiary gaps."""
        bridge_links: List[LegalBridgeLink] = []
        classification_counts: Dict[str, int] = {c.value: 0 for c in EpistemicClassification}
        missing_summary: List[Dict[str, Any]] = []
        all_research_questions: List[str] = []

        for record in records:
            cls._verify_public_data_safety(record)
            classification_counts[record.classification.value] += 1

            link = cls.bridge_record(record)
            bridge_links.append(link)

            if link.missing_evidence:
                missing_summary.append({
                    "evidence_id": record.id,
                    "associated_issue": record.associated_issue,
                    "legal_element": link.legal_element,
                    "missing_predicates": link.missing_evidence
                })

            for rq in link.research_questions:
                if rq not in all_research_questions:
                    all_research_questions.append(rq)

        return EvidenceBridgeEvaluation(
            case_reference=case_reference,
            jurisdiction=jurisdiction,
            evidence_records=records,
            bridge_links=bridge_links,
            missing_evidence_summary=missing_summary,
            research_questions_summary=all_research_questions,
            classification_counts=classification_counts
        )

    @classmethod
    def _derive_fact_statement(cls, evidence: EvidenceRecord) -> str:
        """Derives structural fact statement based on classification."""
        prefix_map = {
            EpistemicClassification.FACT: "Established fact",
            EpistemicClassification.DOCUMENTED_FACT: "Documented fact verified by records",
            EpistemicClassification.ALLEGATION: "Party allegation requiring proof",
            EpistemicClassification.TESTIMONY: "Witness testimonial statement",
            EpistemicClassification.OPINION: "Professional / subjective opinion",
            EpistemicClassification.INFERENCE: "Investigative inference from circumstances",
            EpistemicClassification.UNKNOWN: "Unverified factual proposition",
        }
        prefix = prefix_map.get(evidence.classification, "Factual proposition")
        date_str = f" on {evidence.date}" if evidence.date else " (undated)"
        return f"{prefix}: {evidence.description}{date_str}."

    @classmethod
    def _analyze_missing_evidence(cls, evidence: EvidenceRecord, element: LegalElement) -> List[str]:
        """Detects missing evidentiary predicates based on the legal element requirements."""
        missing = []
        desc_lower = evidence.description.lower()
        src_lower = evidence.source_type.lower()

        if element.element_id == "NOTICE_REQUIREMENT":
            # Check standard 5 notice predicates
            if not evidence.date or "undated" in desc_lower:
                missing.append("Date (When was notice sent/delivered?)")
            if not any(k in desc_lower for k in ["mother", "father", "parent", "guardian", "served on", "recipient"]):
                missing.append("Recipient (Who was formally addressed/served?)")
            if not any(k in desc_lower for k in ["personal service", "certified mail", "hand delivered", "process server", "by mail"]):
                missing.append("Method (Personal service, certified mail, or verbal?)")
            if not any(k in desc_lower for k in ["allegation", "hearing location", "date and time", "grounds", "charges"]):
                missing.append("Content (Did notice contain specific statutory grounds and hearing location?)")
            if not any(k in desc_lower for k in ["affidavit of service", "proof of service", "certificate of service", "signed receipt"]):
                missing.append("Proof of service (Was proof of service filed with the court clerk?)")

        elif element.element_id == "WARRANT_REQUIREMENT":
            if not any(k in desc_lower for k in ["signed by judge", "magistrate signed", "signed warrant", "search warrant"]):
                missing.append("Signed judicial search warrant or court order")
            if not any(k in desc_lower for k in ["sworn affidavit", "probable cause statement", "officer declaration"]):
                missing.append("Sworn probable cause affidavit supporting warrant application")
            if not any(k in desc_lower for k in ["imminent bodily harm", "screaming inside", "medical emergency", "active danger"]):
                missing.append("Contemporaneous facts establishing an exigent circumstances exception")

        elif element.element_id == "REASONABLE_EFFORTS":
            if not any(k in desc_lower for k in ["referral letter", "written referral", "enrollment"]):
                missing.append("Written service referral documentation provided to parent")
            if not any(k in desc_lower for k in ["transportation voucher", "agency funded", "bus pass", "gas card"]):
                missing.append("Proof that agency offered transportation or financial assistance to remove barriers")
            if not any(k in desc_lower for k in ["attendance log", "progress report", "provider evaluation"]):
                missing.append("Service provider attendance records and progress evaluations")

        else:
            # Fallback to default missing elements from registry if specific predicates absent
            missing.extend(element.default_missing_elements)

        return missing

    @classmethod
    def _verify_public_data_safety(cls, evidence: EvidenceRecord) -> None:
        """Enforces public-data safety by rejecting unredacted SSNs or private filesystem paths."""
        text = f"{evidence.description} {evidence.relevance} {evidence.author or ''} {evidence.custodian or ''}"
        if cls.SSN_PATTERN.search(text):
            raise ValueError(f"Public data safety violation: Evidence record '{evidence.id}' contains an unredacted Social Security Number.")
        if cls.PRIVATE_PATH_PATTERN.search(text):
            raise ValueError(f"Public data safety violation: Evidence record '{evidence.id}' references a private local filesystem path.")
