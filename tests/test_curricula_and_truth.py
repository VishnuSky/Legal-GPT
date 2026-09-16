"""Unit tests for Legal Truth Objects, Curricula, and Final Review Agent."""

from core.legal_truth import LegalTruthObject, LegalAuthorityPackage
from constitutional import ConstitutionalPipeline
from human_rights import HumanRightsClassifier, HumanRightsAuthorityTier
from health_law import MentalHealthCommitmentRegistry, SystemIntersectionClassifier
from agents.final_review_agent import FinalReviewAgent


def test_legal_truth_object_and_package():
    truth = LegalTruthObject(
        claim="Shelter care hearing must be held within 72 hours of emergency removal",
        citation="RCW 13.34.065",
        source_url="https://app.leg.wa.gov/rcw/default.aspx?cite=13.34.065",
        authority_type="statute",
        authority_tier=0,
        jurisdiction="US-WA",
        effective_from="2021-07-01",
        verified=True
    )
    truth.compute_hashes("Test statutory full text content")
    assert truth.document_hash != ""
    assert truth.source_hash != ""

    package = LegalAuthorityPackage(
        query="What is the shelter care deadline in Washington?",
        jurisdiction="US-WA",
        authorities=[truth]
    )
    prompt_str = package.format_for_model_prompt()
    assert "=== LEGAL AUTHORITY PACKAGE ===" in prompt_str
    assert "RCW 13.34.065" in prompt_str
    assert "Tier 0" in prompt_str


def test_constitutional_pipeline():
    analysis = ConstitutionalPipeline.analyze_claim(
        provision="Fourteenth Amendment",
        government_action="Emergency removal of child without warrant",
        asserted_right="Parental fundamental liberty interest",
        facts="Child was taken from home without imminent danger."
    )
    assert "Troxel v. Granville" in analysis.controlling_precedent[0]
    assert "Strict Scrutiny" in analysis.standard_of_review
    assert len(analysis.governmental_counterarguments) >= 1


def test_human_rights_classifier():
    c1 = HumanRightsClassifier.classify("RCW 13.34.065")
    assert c1.tier == HumanRightsAuthorityTier.BINDING_DOMESTIC_LAW
    assert c1.is_legally_binding_in_us_court is True

    c2 = HumanRightsClassifier.classify("UN Convention on the Rights of the Child")
    assert c2.tier == HumanRightsAuthorityTier.INTERNATIONAL_DECLARATION
    assert c2.is_legally_binding_in_us_court is False


def test_health_law_registries_and_intersections():
    std = MentalHealthCommitmentRegistry.get_standard("WA")
    assert "RCW 71.05" in std.statute
    assert std.max_initial_hold_hours == 120

    inter = SystemIntersectionClassifier.classify_context("Parent arrested during child welfare investigation with substance use allegations.")
    assert "CHILD_WELFARE_CPS" in inter.overlapping_systems
    assert "CRIMINAL_JUSTICE" in inter.overlapping_systems
    assert "HEALTHCARE_DISABILITY" in inter.overlapping_systems


def test_final_review_agent():
    verdict = FinalReviewAgent.review_response(
        jurisdiction="WA",
        citations=["RCW 13.34.065"],
        response_text="This research summary is for informational purposes and does not constitute legal advice."
    )
    assert verdict.is_approved is True
    assert verdict.jurisdiction_safe is True
    assert verdict.hallucination_detected is False
