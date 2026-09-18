"""Unit tests for DatasetBuilder seed generation and dataset schema validation."""

import pytest
from pathlib import Path
from legal_gpt.training.dataset_builder import DatasetBuilder
from training.schemas.dataset_schema import DatasetSchema, LegalTrainingExample
from legal_registry.loader import default_registry

PRIORITY_FAMILIES = [
    "02_temporal_law",
    "03_authority_ranking",
    "04_citation_verification",
    "05_issue_spotting",
    "06_rule_extraction",
    "07_fact_application",
    "08_counterargument",
    "09_uncertainty",
    "13_parent_rights",
    "14_human_rights",
    "15_drug_policy",
    "16_mental_health",
    "17_due_process",
    "18_equal_protection",
    "19_search_seizure",
    "20_family_integrity",
    "21_administrative_law",
    "22_civil_rights",
    "23_procedural_rights",
]


def test_generate_seeds_produces_requested_count():
    """Verify generate_seeds produces the exact requested number of examples."""
    for family in PRIORITY_FAMILIES:
        seeds_5 = DatasetBuilder.generate_seeds(family, count=5)
        assert len(seeds_5) == 5

        seeds_10 = DatasetBuilder.generate_seeds(family, count=10)
        assert len(seeds_10) == 10

    # Also check fallback non-priority family
    fallback_seeds = DatasetBuilder.generate_seeds("01_jurisdiction", count=7)
    assert len(fallback_seeds) == 7


def test_every_generated_example_passes_dataset_schema_validate():
    """Verify that every generated example across all priority families strictly passes DatasetSchema.validate()."""
    for family in PRIORITY_FAMILIES:
        seeds = DatasetBuilder.generate_seeds(family, count=10)
        for ex in seeds:
            assert DatasetSchema.validate(ex) is True
            # Also verify pydantic instantiation directly
            model = LegalTrainingExample(**ex)
            assert model.reasoning_task == family
            assert len(model.expected_behavior.controlling_citations) > 0


def test_citations_in_examples_exist_in_legal_registry():
    """Verify that all controlling citations in generated seeds exist in legal_registry."""
    # Build complete index of known statutory citations from registry
    registered_sections = set()
    for entry in default_registry.cps_sources.values():
        if hasattr(entry, "key_statutory_sections"):
            for sec in entry.key_statutory_sections:
                registered_sections.add(sec.strip())

    for entries in default_registry.state_sources.values():
        for entry in entries:
            if hasattr(entry, "key_statutory_sections"):
                for sec in entry.key_statutory_sections:
                    registered_sections.add(sec.strip())

    for entry in default_registry.federal_sources.values():
        if hasattr(entry, "key_statutory_sections"):
            for sec in entry.key_statutory_sections:
                registered_sections.add(sec.strip())

    # Check each priority seed example's controlling citations
    for family in PRIORITY_FAMILIES:
        seeds = DatasetBuilder.generate_seeds(family, count=10)
        for ex in seeds:
            citations = ex["expected_behavior"]["controlling_citations"]
            for cite in citations:
                assert cite in registered_sections, (
                    f"Citation '{cite}' in family '{family}' was not found in legal_registry key_statutory_sections."
                )


def test_jurisdiction_code_is_valid():
    """Verify that all generated examples have valid jurisdiction codes present in state matrix or federal."""
    valid_states = set(default_registry.state_matrix.keys())
    valid_jurisdictions = valid_states | {"US", "TRIBAL"}

    for family in PRIORITY_FAMILIES:
        seeds = DatasetBuilder.generate_seeds(family, count=10)
        for ex in seeds:
            juris = ex["jurisdiction"]
            clean_juris = juris.replace("US-", "")
            assert clean_juris in valid_jurisdictions, (
                f"Jurisdiction '{juris}' is not a recognized state code or federal jurisdiction."
            )
            assert ex["input"]["state"].replace("US-", "") in valid_jurisdictions
            assert ex["expected_behavior"]["jurisdiction"].replace("US-", "") in valid_jurisdictions


def test_dataset_files_on_disk_are_valid():
    """Verify that the 5 priority dataset files on disk exist and are valid JSONL."""
    repo_root = Path(__file__).parent.parent
    for family in PRIORITY_FAMILIES:
        file_path = repo_root / "training" / "datasets" / family / "examples.jsonl"
        assert file_path.exists(), f"Dataset file {file_path} does not exist"
        from training.schemas.dataset_schema import validate_jsonl_dataset
        report = validate_jsonl_dataset(str(file_path))
        assert report["valid"] is True
        assert report["count"] >= 10
        assert len(report["errors"]) == 0
