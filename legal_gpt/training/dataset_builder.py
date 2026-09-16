"""Dataset builder converting canonical legal documents into SFT instruction records."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class DatasetRecord(BaseModel):
    instruction: str
    input: Dict[str, Any]
    reasoning_task: str
    expected_behavior: Dict[str, Any]
    source: str
    jurisdiction: str
    legal_date: str
    authority_level: str
    dataset_version: str = "0.3.0"


class DatasetBuilder:
    """Builds synthetic instruction dataset records adhering to the 23 task family schema."""

    @classmethod
    def build_record(
        cls,
        instruction: str,
        facts: str,
        state: str,
        county: Optional[str],
        event_date: str,
        reasoning_task: str,
        expected_behavior: Dict[str, Any],
        source: str,
        authority_level: str = "T0"
    ) -> DatasetRecord:
        return DatasetRecord(
            instruction=instruction,
            input={
                "state": state,
                "county": county,
                "event_date": event_date,
                "facts": facts
            },
            reasoning_task=reasoning_task,
            expected_behavior=expected_behavior,
            source=source,
            jurisdiction=state,
            legal_date=event_date,
            authority_level=authority_level,
            dataset_version="0.3.0"
        )
