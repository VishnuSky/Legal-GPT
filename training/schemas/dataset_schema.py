"""Strict Schema Definition and Validator for 23 Legal Reasoning Task Families."""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, field_validator


class DatasetInputPayload(BaseModel):
    state: str = Field(..., description="Target jurisdiction state code e.g. WA, IL, OH, US")
    county: Optional[str] = Field(None, description="County name if local law/court involved")
    event_date: str = Field(..., description="ISO 8601 Date YYYY-MM-DD")
    facts: str = Field(..., description="Symbolic factual narrative")


class ExpectedBehaviorPayload(BaseModel):
    jurisdiction: str
    temporal_validation: bool = True
    authority_tier: int = Field(0, ge=0, le=13)
    citation_required: bool = True
    controlling_citations: List[str] = Field(default_factory=list)
    epistemic_classification: List[str] = Field(default_factory=lambda: ["LAW", "INTERPRETATION"])


class LegalTrainingExample(BaseModel):
    instruction: str
    input: DatasetInputPayload
    reasoning_task: str
    expected_behavior: ExpectedBehaviorPayload
    source: str
    jurisdiction: str
    legal_date: str
    authority_level: str = "T0"
    dataset_version: str = "0.3.0"

    @field_validator("jurisdiction")
    def validate_jurisdiction(cls, v):
        if not v or len(v) < 2:
            raise ValueError("Jurisdiction must be a valid 2+ char code")
        return v.upper()


def validate_jsonl_dataset(file_path: str) -> Dict[str, Any]:
    """Validates that a JSONL dataset file strictly complies with the schema."""
    valid_count = 0
    errors = []
    from pathlib import Path
    path = Path(file_path)
    if not path.exists():
        return {"valid": False, "count": 0, "errors": [f"File {file_path} does not exist"]}

    with open(path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            line_str = line.strip()
            if not line_str:
                continue
            try:
                import json
                raw = json.loads(line_str)
                LegalTrainingExample(**raw)
                valid_count += 1
            except Exception as e:
                errors.append(f"Line {idx}: {e}")

    return {
        "valid": len(errors) == 0,
        "count": valid_count,
        "errors": errors
    }
