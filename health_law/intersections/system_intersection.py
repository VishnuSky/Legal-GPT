"""Multi-system intersection classifier (Criminal, Civil, Family, Healthcare, Disability)."""

from typing import List, Dict, Any
from pydantic import BaseModel, Field


class SystemIntersection(BaseModel):
    overlapping_systems: List[str]  # e.g. ["CPS", "CRIMINAL", "DISABILITY", "HEALTHCARE"]
    governing_statutes: List[str]
    confidentiality_walls: List[str]
    due_process_guardrails: List[str]


class SystemIntersectionClassifier:
    """Classifies overlapping multi-system legal contexts."""

    @classmethod
    def classify_context(cls, narrative: str) -> SystemIntersection:
        n_lower = narrative.lower()
        systems = []
        statutes = []
        confidentiality = []
        guardrails = []

        if any(w in n_lower for w in ["cps", "child", "custody", "removal"]):
            systems.append("CHILD_WELFARE_CPS")
            statutes.append("State Juvenile Court Act & Title IV-E Social Security Act")
            guardrails.append("Notice of shelter care hearing and right to counsel")

        if any(w in n_lower for w in ["police", "arrest", "charges", "criminal"]):
            systems.append("CRIMINAL_JUSTICE")
            statutes.append("State Penal Code & Fifth Amendment Privilege against Self-Incrimination")
            guardrails.append("Statements in dependency cannot automatically waive Fifth Amendment rights")

        if any(w in n_lower for w in ["mental health", "hospital", "psychiatric", "treatment", "disability", "substance"]):
            systems.append("HEALTHCARE_DISABILITY")
            statutes.append("Americans with Disabilities Act (ADA Title II) & 42 CFR Part 2")
            confidentiality.append("Strict statutory medical/SUD record confidentiality")
            guardrails.append("Reasonable accommodation in parenting remedial services under ADA Title II")

        if not systems:
            systems.append("GENERAL_CIVIL")

        return SystemIntersection(
            overlapping_systems=systems,
            governing_statutes=statutes,
            confidentiality_walls=confidentiality,
            due_process_guardrails=guardrails
        )
