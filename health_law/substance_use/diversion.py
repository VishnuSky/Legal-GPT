"""Substance use diversion and treatment alternatives."""

from typing import List, Dict, Any
from pydantic import BaseModel


class DiversionFramework(BaseModel):
    program_type: str  # Family Treatment Court, Pre-Trial Diversion, Statutory Deferred Prosecution
    statutory_basis: str
    target_population: str
    rights_retained: List[str]


class SubstanceUseDiversionRegistry:
    PROGRAMS = [
        DiversionFramework(
            program_type="Family Treatment Court (FTC)",
            statutory_basis="State Judicial Administrative Rules & Family Court Standards",
            target_population="Parents facing child dependency proceedings with substance use allegations.",
            rights_retained=["Right to appointed counsel", "Regular family visitation", "Supportive remedial services under Title IV-E"]
        ),
        DiversionFramework(
            program_type="Confidentiality & Medical Treatment Privacy",
            statutory_basis="42 C.F.R. Part 2 & HIPAA (45 C.F.R. Part 164)",
            target_population="Individuals undergoing substance use disorder (SUD) clinical treatment.",
            rights_retained=["Prohibition against disclosure of SUD patient records in civil/criminal proceedings without express consent or specific court order"]
        )
    ]
