"""Curriculum schedule and task family weights for multi-stage SFT/LoRA training."""

from typing import List, Dict, Any
from pydantic import BaseModel, Field


class TrainingStage(BaseModel):
    stage_id: int
    name: str
    description: str
    task_families: List[str]
    epochs: int = 1
    learning_rate: float = 2e-4


class CurriculumManager:
    """Manages the 4-stage legal reasoning training curriculum."""

    STAGES: List[TrainingStage] = [
        TrainingStage(
            stage_id=1,
            name="Foundational Legal Epistemology & Jurisdiction",
            description="Teaches statement classification, jurisdiction boundaries, and authority hierarchy.",
            task_families=["01_jurisdiction", "02_temporal_law", "03_authority_ranking", "04_citation_verification"],
            epochs=1,
            learning_rate=2e-4
        ),
        TrainingStage(
            stage_id=2,
            name="Core Reasoning & Analysis",
            description="Teaches IRAC/CRAC application, counterarguments, and uncertainty bounding.",
            task_families=["05_issue_spotting", "06_rule_extraction", "07_fact_application", "08_counterargument", "09_uncertainty"],
            epochs=2,
            learning_rate=1.5e-4
        ),
        TrainingStage(
            stage_id=3,
            name="Vertical Substantive Domains",
            description="Deep dive into CPS, Constitutional, ICWA, Human Rights, and Health Law.",
            task_families=[
                "10_constitutional", "11_cps", "12_icwa", "13_parent_rights",
                "14_human_rights", "15_drug_policy", "16_mental_health"
            ],
            epochs=2,
            learning_rate=1e-4
        ),
        TrainingStage(
            stage_id=4,
            name="Complex Intersections & Procedural Rights",
            description="Overlapping statutory systems, search & seizure, and procedural due process.",
            task_families=[
                "17_due_process", "18_equal_protection", "19_search_seizure",
                "20_family_integrity", "21_administrative_law", "22_civil_rights", "23_procedural_rights"
            ],
            epochs=1,
            learning_rate=5e-5
        )
    ]

    @classmethod
    def get_stages(cls) -> List[TrainingStage]:
        return cls.STAGES
