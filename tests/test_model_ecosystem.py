"""Unit tests for Legal-GPT model ecosystem and reasoning subpackage."""

from legal_gpt.model import (
    ModelCapability,
    ModelSpecs,
    ModelManifest,
    ModelRegistry,
    LegalModelClient,
    InferenceRequest,
)
from legal_gpt.reasoning import (
    IssueSpotter,
    AuthoritySelector,
    ConflictDetector,
    UncertaintyEngine,
    AnswerPlanner,
)


def test_model_specs_and_capabilities():
    specs = ModelSpecs()
    assert specs.name == "Legal-GPT"
    assert ModelCapability.LEGAL_REASONING in specs.capabilities
    assert ModelCapability.JURISDICTION_ISOLATION in specs.capabilities
    assert "Q4_K_M" in specs.quantizations_supported


def test_model_manifest_validation():
    manifest = ModelManifest()
    assert manifest.is_valid() is True
    assert manifest.version == "0.3.0-alpha"
    assert "Qwen" in manifest.base_model_name


def test_model_inference_client():
    client = LegalModelClient()
    req = InferenceRequest(
        prompt="What is the shelter care deadline in Washington?",
        jurisdiction_lock="WA"
    )
    res = client.generate(req)
    assert res.model_name == "Legal-GPT-14B"
    assert "JURISDICTION: WA" in res.text
    assert len(res.epistemic_classifications) >= 1


def test_issue_spotter():
    issues = IssueSpotter.spot_issues("The caseworker removed the child without notice or counsel under ICWA.")
    assert len(issues) >= 2
    categories = [i.category for i in issues]
    assert "CPS" in categories
    assert "ICWA" in categories or "PARENT_RIGHTS" in categories


def test_authority_selector():
    authorities = AuthoritySelector.select_governing_authorities(
        jurisdiction="WA",
        category="CPS",
        primary_citations=["U.S. Const. amend. XIV", "25 U.S.C. § 1912", "RCW 13.34.065"]
    )
    assert len(authorities) == 3
    assert all(a.authority_tier == "TIER_0" for a in authorities)
    assert all(a.is_binding is True for a in authorities)


def test_conflict_detector():
    conflicts = ConflictDetector.detect_conflicts(
        jurisdiction="WA",
        citations=["25 U.S.C. § 1912(d)", "RCW 13.34.065", "705 ILCS 405/2-9"]
    )
    assert len(conflicts) >= 2
    types = [c.conflict_type for c in conflicts]
    assert "SUPREMACY" in types
    assert "JURISDICTIONAL" in types


def test_uncertainty_and_answer_planner():
    assessment = UncertaintyEngine.evaluate_uncertainty(
        jurisdiction="WA",
        material_facts_present=["Emergency removal on Tuesday"],
        verified_authorities=["RCW 13.34.065"]
    )
    assert assessment.confidence_score >= 0.70
    assert assessment.abstention_warranted is False

    issues = IssueSpotter.spot_issues("Removal of child in Skagit County", "WA")
    auths = AuthoritySelector.select_governing_authorities("WA", "CPS", ["RCW 13.34.065"])
    plan = AnswerPlanner.construct_plan(
        issue=issues[0],
        jurisdiction="WA",
        authorities=auths,
        conflicts=[],
        uncertainty=assessment,
        facts=["Child removed on Tuesday"]
    )
    assert plan.jurisdiction == "WA"
    assert "RCW 13.34.065" in plan.primary_authorities
    assert len(plan.counterarguments) >= 1
    assert len(plan.next_research_steps) >= 1
