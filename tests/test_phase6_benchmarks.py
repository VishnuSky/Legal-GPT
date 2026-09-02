"""Unit and Integration Tests for Phase 6: 50-Scenario Benchmark Suite & Continuous Scaling."""

import pytest
from benchmarks.scenarios import (
    BENCHMARK_SCENARIOS,
    BenchmarkScenario,
    BenchmarkReport,
    BenchmarkEvaluator,
)


def test_benchmark_scenario_suite_completeness():
    assert len(BENCHMARK_SCENARIOS) == 50
    categories = set(s.category for s in BENCHMARK_SCENARIOS)
    assert "CPS_EMERGENCY" in categories
    assert "PARENT_RIGHTS" in categories
    assert "PROCEDURAL" in categories
    assert "DUE_PROCESS" in categories
    assert "ICWA" in categories
    assert "UCCJEA" in categories
    assert "TEMPORAL" in categories


def test_benchmark_evaluator_all_scenarios_pass():
    report: BenchmarkReport = BenchmarkEvaluator.run_benchmark(category="ALL")
    assert report.total_scenarios == 50
    assert report.scenarios_passed == 50
    assert report.scenarios_failed == 0
    assert report.accuracy_rate == 1.0


def test_benchmark_evaluator_by_category():
    # ICWA Category
    icwa_report = BenchmarkEvaluator.run_benchmark(category="ICWA")
    assert icwa_report.total_scenarios == 6
    assert icwa_report.scenarios_passed == 6
    assert icwa_report.accuracy_rate == 1.0

    # UCCJEA Category
    uccjea_report = BenchmarkEvaluator.run_benchmark(category="UCCJEA")
    assert uccjea_report.total_scenarios == 5
    assert uccjea_report.scenarios_passed == 5
    assert uccjea_report.accuracy_rate == 1.0

    # Due Process Category
    due_report = BenchmarkEvaluator.run_benchmark(category="DUE_PROCESS")
    assert due_report.total_scenarios == 11
    assert due_report.scenarios_passed == 11
    assert due_report.accuracy_rate == 1.0
