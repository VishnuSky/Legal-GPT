"""Unit tests for Final Review Agent NLI-style proposition validator."""

from agents.final_review_agent import FinalReviewAgent, FinalReviewResult


def test_clean_response_passes_all_checks():
    """A clean response that passes all 5 proposition checks."""
    result: FinalReviewResult = FinalReviewAgent.review_response(
        jurisdiction="WA",
        citations=["RCW 13.34.065"],
        response_text=(
            "In Washington State (jurisdiction: US-WA), under RCW 13.34.065, the juvenile court must hold "
            "a shelter care hearing within 72 hours of emergency removal. [INFERENCE] It is likely that "
            "the court will evaluate whether reasonable efforts were made (this is an inference, not yet established). "
            "This research summary is for informational purposes and does not constitute legal advice."
        ),
        statements=[
            {
                "classification": "LAW",
                "text": "The juvenile court must hold a shelter care hearing within 72 hours under RCW 13.34.065.",
                "citation": "RCW 13.34.065"
            },
            {
                "classification": "INFERENCE",
                "text": "It is likely that the court will evaluate reasonable efforts (this is an inference, not yet established).",
                "citation": None
            }
        ]
    )
    assert result.passed is True
    assert result.is_approved is True
    assert len(result.failures) == 0
    assert result.jurisdiction_confirmed is True
    assert result.citation_coverage == 1.0


def test_response_with_uncited_holding_fails_check_1():
    """A response with an uncited HOLDING fails check 1."""
    result: FinalReviewResult = FinalReviewAgent.review_response(
        jurisdiction="WA",
        citations=[],
        response_text=(
            "In Washington (jurisdiction: US-WA), the court held that parents have a fundamental liberty interest "
            "in the care and custody of their children without citing any governing authority. "
            "This summary does not constitute legal advice."
        ),
        statements=[
            {
                "classification": "HOLDING",
                "text": "The court held that parents have a fundamental liberty interest in the care and custody of their children.",
                "citation": None
            }
        ]
    )
    assert result.passed is False
    assert result.is_approved is False
    assert any("Check 1 Failure" in f for f in result.failures)
    assert any("HOLDING" in f for f in result.failures)


def test_response_with_inference_presented_as_law_fails_check_3():
    """A response with an INFERENCE presented as LAW fails check 3."""
    result: FinalReviewResult = FinalReviewAgent.review_response(
        jurisdiction="IL",
        citations=["705 ILCS 405/2-10"],
        response_text=(
            "In Illinois (jurisdiction: US-IL), under 705 ILCS 405/2-10, [INFERENCE] presented as [LAW] "
            "caseworkers have absolute statutory immunity to seize children without cause. "
            "This summary does not constitute legal advice."
        ),
        statements=[
            {
                "classification": "INFERENCE",
                "presented_as": "LAW",
                "text": "Caseworkers have absolute statutory immunity to seize children without cause.",
                "citation": None
            }
        ]
    )
    assert result.passed is False
    assert result.is_approved is False
    assert any("Check 3 Failure" in f for f in result.failures)
    assert any("INFERENCE statement presented as LAW" in f for f in result.failures)


def test_response_missing_jurisdiction_fails_check_4():
    """A response missing explicit jurisdiction fails check 4."""
    result: FinalReviewResult = FinalReviewAgent.review_response(
        jurisdiction="",
        citations=["RCW 13.34.065"],
        response_text=(
            "Under RCW 13.34.065, a shelter care hearing must be held within 72 hours. "
            "This summary does not constitute legal advice."
        ),
        statements=[
            {
                "classification": "LAW",
                "text": "A shelter care hearing must be held within 72 hours under RCW 13.34.065.",
                "citation": "RCW 13.34.065"
            }
        ]
    )
    assert result.passed is False
    assert result.jurisdiction_confirmed is False
    assert any("Check 4 Failure" in f for f in result.failures)


def test_constitutional_claim_without_t0_authority_fails_check_5():
    """A constitutional claim with no T0 authority reference fails check 5."""
    result: FinalReviewResult = FinalReviewAgent.review_response(
        jurisdiction="WA",
        citations=["RCW 13.34.050"],  # State statute only; no T0 constitutional authority (U.S. Const. / SCOTUS)
        response_text=(
            "In Washington State (jurisdiction: US-WA), emergency removal without notice directly violates "
            "the parent's procedural due process and Fourteenth Amendment constitutional rights. "
            "Controlling state authority is RCW 13.34.050. This is not legal advice."
        ),
        statements=[
            {
                "classification": "LAW",
                "text": "Emergency removal without notice violates procedural due process.",
                "citation": "RCW 13.34.050"
            }
        ]
    )
    assert result.passed is False
    assert any("Check 5 Failure" in f for f in result.failures)
    assert any("T0-tier constitutional authority" in f for f in result.failures)
