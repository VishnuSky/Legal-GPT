"""Unit tests for dataset schema validation, SFT pipeline, and GGUF exporter."""

from training.schemas.dataset_schema import validate_jsonl_dataset, LegalTrainingExample
from training.train_sft import SFTTrainingPipeline
from training.export.gguf_pipeline import GGUFExportPipeline
from evaluation.benchmark import LegalBenchmarkRunner


def test_jsonl_dataset_schema_validation():
    res = validate_jsonl_dataset("training/datasets/05_issue_spotting/examples.jsonl")
    assert res["valid"] is True
    assert res["count"] >= 2

    res_cps = validate_jsonl_dataset("training/datasets/11_cps/examples.jsonl")
    assert res_cps["valid"] is True
    assert res_cps["count"] >= 1


def test_sft_pipeline_simulation():
    pipeline = SFTTrainingPipeline()
    res = pipeline.run_training_simulation()
    assert res["status"] == "TRAINED_AND_VALIDATED"
    assert len(res["stages"]) == 4
    assert res["evaluation"]["overall_score"] >= 0.90


def test_gguf_export_pipeline():
    pipeline = GGUFExportPipeline()
    res = pipeline.run_export_pipeline()
    assert res["lm_studio_compatible"] is True
    assert len(res["artifacts"]) == 3


def test_benchmark_runner():
    runner = LegalBenchmarkRunner()
    report = runner.run_full_benchmark()
    assert report["citation_accuracy"] >= 0.90
    assert report["jurisdiction_accuracy"] >= 0.95
    assert report["target_thresholds_met"] is True


def test_external_benchmark_runner():
    from evaluation.external_benchmark import ExternalBenchmarkRunner
    runner = ExternalBenchmarkRunner()
    report = runner.run_benchmark()
    assert report["total_cases"] == 10
    assert report["accuracy_rate"] >= 0.85
    assert report["failures"] == 0


TASK_FAMILIES_19 = [
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


def test_all_19_task_families_datasets_valid():
    """Verify that all 19 task family JSONL datasets on disk exist, are schema-valid, and meet minimum counts."""
    from pathlib import Path
    for family in TASK_FAMILIES_19:
        path = Path(f"training/datasets/{family}/examples.jsonl")
        assert path.exists(), f"Dataset file {path} does not exist"
        res = validate_jsonl_dataset(str(path))
        assert res["valid"] is True, f"Dataset {family} is invalid: {res.get('errors')}"
        if family == "17_due_process":
            assert res["count"] >= 25, f"Expected at least 25 examples for {family}, found {res['count']}"
        else:
            assert res["count"] >= 10, f"Expected at least 10 examples for {family}, found {res['count']}"
