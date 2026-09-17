"""Adversarial and Functional Test Suite for Legal-GPT Rights Discovery Subsystem.

Mission Requirements Tested:
1. Zero violation declarations (The engine must NOT declare that a right was violated).
2. Epistemic distinction: Distinguishes "law recognizes this right" from "facts establish violation".
3. Adversarial Case 1: A right appears relevant but is not (e.g. 6th Amendment criminal counsel in civil dependency; ADA claimed with no disability facts).
4. Adversarial Case 2: Wrong jurisdiction has similar language (e.g. IL statutory right cited in WA jurisdiction).
5. Adversarial Case 3: Statute changed over time (temporal validity before effective date).
6. Adversarial Case 4: Known exception applies (e.g. exigent circumstances / emergency medical necessity).
7. Adversarial Case 5: Constitutional right conflicts with statutory procedure (e.g. 4th/14th Amendment vs summary administrative detention).
8. Adversarial Case 6: User assertion is unsupported by factual predicates (e.g. 1st Amendment speech retaliation with no speech facts).
9. Full coverage of all 20 canonical rights categories.
"""

import pytest
from datetime import date
from core.rights.models import (
    LegalBasis,
    RightCategory,
    RightVerificationStatus,
    PotentialRightEvaluation,
    RightsDiscoveryInput,
    RightsDiscoveryResult,
)
from core.rights.registry import RightsRegistry, CANONICAL_RIGHTS
from core.rights.engine import RightsDiscoveryEngine


def test_zero_violation_adjudication_rule():
    """Verify the engine NEVER declares that a user's rights were violated across all outputs."""
    input_data = RightsDiscoveryInput(
        facts=[
            "Caseworker entered my home without a warrant.",
            "Police took my daughter without any court order or notice.",
            "No attorney was present for me."
        ],
        jurisdiction="US-WA",
        date=date(2024, 5, 10),
        procedure="EMERGENCY_REMOVAL",
        user_allegations=["CPS completely violated my constitutional rights!"]
    )

    res: RightsDiscoveryResult = RightsDiscoveryEngine.discover_rights(input_data)

    # 1. Epistemic warning must be explicitly present
    assert "Legal-GPT does not declare legal violations" in res.epistemic_warning
    assert "distinguishes between 'the law recognizes this right'" in res.epistemic_warning
    assert "the supplied facts establish that the right was violated" in res.epistemic_warning

    # 2. Check every evaluated right: Status must NEVER be VIOLATED or VIOLATION_SUSPECTED
    for r in res.potentially_relevant_rights:
        assert r.verification_status != "VIOLATED"
        assert r.verification_status != "VIOLATION_SUSPECTED"
        assert "does NOT adjudicate whether this right was violated" in r.epistemic_distinction
        assert "judicial finding" in r.epistemic_distinction

    for r in res.inapplicable_or_excluded_rights:
        assert r.verification_status != "VIOLATED"
        assert r.verification_status != "VIOLATION_SUSPECTED"


def test_adversarial_right_appears_relevant_but_is_not_sixth_amendment():
    """Adversarial Scenario 1: User asserts 6th Amendment right to counsel in a civil dependency investigation.
    
    The 6th Amendment guarantees counsel exclusively in 'all criminal prosecutions.'
    In civil CPS dependency, counsel is rooted in 14th Amendment Due Process (Lassiter) or state statutes,
    not the 6th Amendment.
    """
    input_data = RightsDiscoveryInput(
        facts=[
            "A DCFS worker interviewed me at my home regarding a child neglect investigation.",
            "I asked for a Sixth Amendment court-appointed attorney during the interview."
        ],
        jurisdiction="US-IL",
        date=date(2024, 1, 15),
        procedure="INVESTIGATION",
        asserted_rights=["Sixth Amendment Right to Counsel"]
    )

    res = RightsDiscoveryEngine.discover_rights(input_data)

    # The Sixth Amendment check should be classified under inapplicable_or_excluded as RECOGNIZED_FACTS_INSUFFICIENT
    sixth_eval = next((r for r in res.inapplicable_or_excluded_rights if "Sixth Amendment" in r.right_name), None)
    assert sixth_eval is not None
    assert sixth_eval.verification_status == RightVerificationStatus.RECOGNIZED_FACTS_INSUFFICIENT
    assert "criminal prosecutions" in sixth_eval.applicability_rationale
    assert "civil" in sixth_eval.epistemic_distinction


def test_adversarial_wrong_jurisdiction_with_similar_language():
    """Adversarial Scenario 2: User in Washington State asserts Illinois statutory right (705 ILCS 405/2-9).
    
    The engine must recognize that 705 ILCS 405/2-9 is a real statute, but identify a JURISDICTION MISMATCH
    because Illinois law does not control in Washington State.
    """
    input_data = RightsDiscoveryInput(
        facts=[
            "Child was removed yesterday by DCYF in Seattle, King County, Washington.",
            "I want the 48-hour temporary custody hearing required by 705 ILCS 405/2-9."
        ],
        jurisdiction="US-WA",
        date=date(2024, 6, 1),
        procedure="EMERGENCY_REMOVAL"
    )

    res = RightsDiscoveryEngine.discover_rights(input_data)

    # 1. Illinois statute must be flagged as NOT_APPLICABLE_JURISDICTION_MISMATCH
    il_eval = next((r for r in res.inapplicable_or_excluded_rights if "705 ILCS" in r.authority), None)
    assert il_eval is not None
    assert il_eval.verification_status == RightVerificationStatus.NOT_APPLICABLE_JURISDICTION_MISMATCH
    assert "US-IL" in il_eval.jurisdiction
    assert "does not control in US-WA" in il_eval.epistemic_distinction

    # 2. Washington's controlling statute (RCW 13.34.065 72-hour shelter hearing) must be recognized
    wa_eval = next((r for r in res.potentially_relevant_rights if "RCW 13.34.065" in r.authority), None)
    assert wa_eval is not None
    assert wa_eval.verification_status == RightVerificationStatus.RECOGNIZED_POTENTIALLY_IMPLICATED
    assert wa_eval.jurisdiction == "US-WA"


def test_adversarial_statute_changed_over_time_temporal_invalidity():
    """Adversarial Scenario 3: Event occurred prior to statute effective date.
    
    ADA Title II (42 U.S.C. § 12132) became effective on January 26, 1992.
    If the event date is January 15, 1985, the engine must flag NOT_APPLICABLE_TEMPORAL_INVALID.
    """
    input_data = RightsDiscoveryInput(
        facts=[
            "In January 1985, state social services denied me accommodations for my physical disability."
        ],
        jurisdiction="US",
        date=date(1985, 1, 15),
        procedure="INVESTIGATION"
    )

    res = RightsDiscoveryEngine.discover_rights(input_data)

    ada_eval = next((r for r in res.inapplicable_or_excluded_rights if "42 U.S.C. § 12132" in r.authority), None)
    assert ada_eval is not None
    assert ada_eval.verification_status == RightVerificationStatus.NOT_APPLICABLE_TEMPORAL_INVALID
    assert "not yet in effect on 1985-01-15" in ada_eval.applicability_rationale


def test_adversarial_exception_applies_exigent_circumstances():
    """Adversarial Scenario 4: User asserts 4th Amendment home entry right, but facts establish recognized exception.
    
    Facts state officers heard screaming inside / active physical violence, triggering the exigent circumstances
    / emergency aid doctrine. The engine must identify the right is recognized, but flag that facts trigger an exception.
    """
    input_data = RightsDiscoveryInput(
        facts=[
            "Officers arrived at my door after a neighbor reported screaming inside.",
            "They heard shouting and immediate danger to the infant, so they pushed open the door without a warrant."
        ],
        jurisdiction="US-WA",
        date=date(2024, 4, 10),
        procedure="EMERGENCY_REMOVAL"
    )

    res = RightsDiscoveryEngine.discover_rights(input_data)

    fourth_eval = next((r for r in res.inapplicable_or_excluded_rights if "Fourth Amendment" in r.right_name or "U.S. Const. amend. IV" in r.authority), None)
    assert fourth_eval is not None
    assert fourth_eval.verification_status == RightVerificationStatus.POTENTIALLY_BARRED_EXCEPTION_APPLIES
    assert len(fourth_eval.exceptions_triggered) > 0
    assert any("exigent" in exc.lower() or "imminent" in exc.lower() or "screaming" in exc.lower() for exc in fourth_eval.exceptions_triggered)


def test_adversarial_constitutional_statutory_conflict():
    """Adversarial Scenario 5: Constitutional right tensions with statutory emergency removal procedure.
    
    Fourth Amendment and Fourteenth Amendment Due Process (*Doe v. Heck*, *Camara*) require a judicial warrant
    or strict exigency before seizing a child from the home. State laws sometimes authorize administrative detention.
    The engine must detect and document this constitutional-statutory tension.
    """
    input_data = RightsDiscoveryInput(
        facts=[
            "DCYF caseworker entered my apartment without a warrant or court order and took my child into custody."
        ],
        jurisdiction="US-WA",
        date=date(2024, 7, 1),
        procedure="EMERGENCY_REMOVAL"
    )

    res = RightsDiscoveryEngine.discover_rights(input_data)

    assert len(res.constitutional_statutory_conflicts) > 0
    conflict = res.constitutional_statutory_conflicts[0]
    assert "constitutional_right" in conflict
    assert "conflicting_statutory_procedure" in conflict
    assert "Supremacy Clause" in conflict["epistemic_note"]


def test_adversarial_user_assertion_is_unsupported_free_speech():
    """Adversarial Scenario 6: User asserts 1st Amendment speech retaliation, but narrative has zero speech facts.
    
    The engine must evaluate the asserted right, note that the 1st Amendment is recognized law,
    but flag RECOGNIZED_FACTS_INSUFFICIENT because the narrative contains no protected speech or retaliation predicates.
    """
    input_data = RightsDiscoveryInput(
        facts=[
            "Caseworker inspected my refrigerator and said there was not enough food.",
            "They scheduled a follow-up visit for next week."
        ],
        jurisdiction="US",
        date=date(2024, 3, 1),
        procedure="INVESTIGATION",
        asserted_rights=["First Amendment Freedom of Speech"]
    )

    res = RightsDiscoveryEngine.discover_rights(input_data)

    speech_eval = next((r for r in res.inapplicable_or_excluded_rights if "First Amendment" in r.right_name), None)
    assert speech_eval is not None
    assert speech_eval.verification_status == RightVerificationStatus.RECOGNIZED_FACTS_INSUFFICIENT
    assert "unsupported by factual predicates" in speech_eval.applicability_rationale


def test_canonical_rights_registry_20_categories_coverage():
    """Verify the RightsRegistry covers all 20 required categories of rights."""
    all_rights = RightsRegistry.get_all()
    assert len(all_rights) >= 20

    registered_categories = {r.category for r in all_rights}
    
    required_categories = [
        RightCategory.CONSTITUTIONAL_RIGHTS,
        RightCategory.STATUTORY_RIGHTS,
        RightCategory.PROCEDURAL_RIGHTS,
        RightCategory.ADMINISTRATIVE_RIGHTS,
        RightCategory.PARENTAL_RIGHTS,
        RightCategory.CHILD_RIGHTS,
        RightCategory.CIVIL_RIGHTS,
        RightCategory.DISABILITY_RIGHTS,
        RightCategory.PRIVACY_RIGHTS,
        RightCategory.PROPERTY_INTERESTS,
        RightCategory.LIBERTY_INTERESTS,
        RightCategory.DUE_PROCESS_PROTECTIONS,
        RightCategory.EQUAL_PROTECTION_CONCERNS,
        RightCategory.FAMILY_ASSOCIATION_INTERESTS,
        RightCategory.RELIGIOUS_RIGHTS,
        RightCategory.SEARCH_SEIZURE_PROTECTIONS,
        RightCategory.COUNSEL_RIGHTS,
        RightCategory.NOTICE_RIGHTS,
        RightCategory.HEARING_RIGHTS,
        RightCategory.APPEAL_RIGHTS,
    ]

    for req_cat in required_categories:
        assert req_cat in registered_categories, f"Missing coverage for category: {req_cat}"


def test_icwa_and_tribal_child_rights_discovery():
    """Verify that when Indian child welfare facts are present, ICWA 25 U.S.C. § 1912 active efforts rights are discovered."""
    input_data = RightsDiscoveryInput(
        facts=[
            "My daughter is enrolled with the Lummi Nation tribe.",
            "State workers initiated an emergency removal in Washington."
        ],
        jurisdiction="US-WA",
        date=date(2024, 2, 20),
        procedure="EMERGENCY_REMOVAL"
    )

    res = RightsDiscoveryEngine.discover_rights(input_data)

    icwa_right = next((r for r in res.potentially_relevant_rights if "25 U.S.C. § 1912" in r.authority), None)
    assert icwa_right is not None
    assert icwa_right.category == RightCategory.CHILD_RIGHTS
    assert icwa_right.authority_tier == "TIER_0"
    assert icwa_right.verification_status == RightVerificationStatus.RECOGNIZED_POTENTIALLY_IMPLICATED
    assert "Active Efforts" in icwa_right.right_name
