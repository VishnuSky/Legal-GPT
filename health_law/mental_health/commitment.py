"""Mental health civil commitment legal standards."""

from typing import List, Dict, Any
from pydantic import BaseModel


class CommitmentStandard(BaseModel):
    jurisdiction: str
    statute: str
    evidentiary_burden: str  # e.g. Clear, cogent, and convincing evidence (Addington v. Texas)
    grounds: List[str]
    max_initial_hold_hours: int


class MentalHealthCommitmentRegistry:
    STANDARDS = {
        "WA": CommitmentStandard(
            jurisdiction="WA",
            statute="RCW 71.05.150 / RCW 71.05.153 (Involuntary Treatment Act)",
            evidentiary_burden="Clear, cogent, and convincing evidence",
            grounds=["Imminent danger to self", "Imminent danger to others", "Grave disability"],
            max_initial_hold_hours=120  # 120-hour hold in WA
        ),
        "IL": CommitmentStandard(
            jurisdiction="IL",
            statute="405 ILCS 5/3-600 (Mental Health and Developmental Disabilities Code)",
            evidentiary_burden="Clear and convincing evidence",
            grounds=["Immediate danger of physical harm to self or others", "Unable to care for basic needs"],
            max_initial_hold_hours=24
        ),
        "OH": CommitmentStandard(
            jurisdiction="OH",
            statute="R.C. 5122.10 (Emergency Hospitalization)",
            evidentiary_burden="Clear and convincing evidence",
            grounds=["Substantial risk of physical harm to self or others", "Grave impairment"],
            max_initial_hold_hours=72
        )
    }

    @classmethod
    def get_standard(cls, state: str) -> CommitmentStandard:
        return cls.STANDARDS.get(state.upper(), cls.STANDARDS["WA"])
