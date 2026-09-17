"""Patient and disability rights under mental health laws."""

from typing import List
from pydantic import BaseModel


class PatientRight(BaseModel):
    right_name: str
    controlling_authority: str
    scope: str


class MentalHealthRights:
    RIGHTS = [
        PatientRight(
            right_name="Right to Contest Involuntary Hospitalization",
            controlling_authority="Fourteenth Amendment Due Process & Addington v. Texas, 441 U.S. 418 (1979)",
            scope="Mandatory judicial hearing with representation by counsel before prolonged commitment."
        ),
        PatientRight(
            right_name="Right to Refuse Antipsychotic Medication",
            controlling_authority="Washington v. Harper, 494 U.S. 210 (1990); Sell v. United States, 539 U.S. 166 (2003)",
            scope="Substantive liberty interest requiring independent administrative or judicial determination of necessity."
        ),
        PatientRight(
            right_name="Right to Community-Based Services (Olmstead Mandate)",
            controlling_authority="Americans with Disabilities Act (ADA Title II) & Olmstead v. L.C., 527 U.S. 581 (1999)",
            scope="Unjustified institutional isolation constitutes unlawful discrimination under Title II."
        )
    ]
