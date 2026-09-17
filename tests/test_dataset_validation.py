"""Unit tests for dataset schema validation, SFT pipeline, and GGUF exporter."""

from training.schemas.dataset_schema import validate_jsonl_dataset, LegalTrainingExample
from training.train_sft import SFTTrainingPipeline
from training.export.gguf_pipeline import GGUFExportPipeline
from evaluation.benchmark import LegalBenchmarkRunner


def test_jsonl_dataset_schema_validation():
    res = validate_jsonl_dataset("training/datasets/01_jurisdiction/examples.jsonl")
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
