"""Dataset builder converting canonical legal documents into SFT instruction records."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from training.schemas.dataset_schema import (
    DatasetSchema,
    LegalTrainingExample,
    DatasetInputPayload,
    ExpectedBehaviorPayload,
)


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

    # Priority Task Family 05: Issue Spotting
    _SEEDS_05_ISSUE_SPOTTING = [
        {
            "instruction": "Identify threshold procedural and statutory issues regarding emergency removal and shelter care hearing timeline.",
            "input": {
                "state": "WA",
                "county": "Skagit",
                "event_date": "2024-03-12",
                "facts": "Caseworker took custody of two minors on Tuesday afternoon without a warrant. Shelter care hearing was scheduled for the following Monday morning."
            },
            "reasoning_task": "05_issue_spotting",
            "expected_behavior": {
                "jurisdiction": "WA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["RCW 13.34.065"],
                "epistemic_classification": ["ISSUE", "LAW", "ANALYSIS"]
            },
            "source": "Washington State Legislature RCW 13.34.065",
            "jurisdiction": "WA",
            "legal_date": "2024-03-12",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Spot jurisdictional and urgent necessity issues in temporary custody petition.",
            "input": {
                "state": "IL",
                "county": "Cook",
                "event_date": "2024-05-18",
                "facts": "Child welfare agency filed petition alleging neglect based solely on missed medical appointments; caseworker sought out-of-home placement without offering community medical transportation."
            },
            "reasoning_task": "05_issue_spotting",
            "expected_behavior": {
                "jurisdiction": "IL",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["705 ILCS 405/2-10"],
                "epistemic_classification": ["ISSUE", "LAW", "ANALYSIS"]
            },
            "source": "Illinois General Assembly 705 ILCS 405/2-10",
            "jurisdiction": "IL",
            "legal_date": "2024-05-18",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Spot statutory compliance issues regarding shelter care timing following emergency apprehension.",
            "input": {
                "state": "OH",
                "county": "Cuyahoga",
                "event_date": "2023-11-06",
                "facts": "Police officer apprehended minor under protective custody on Wednesday evening. Shelter care detention hearing was held the following Tuesday."
            },
            "reasoning_task": "05_issue_spotting",
            "expected_behavior": {
                "jurisdiction": "OH",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["ORC § 2151.314"],
                "epistemic_classification": ["ISSUE", "LAW", "ANALYSIS"]
            },
            "source": "Ohio Revised Code ORC § 2151.314",
            "jurisdiction": "OH",
            "legal_date": "2023-11-06",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Spot issues concerning warrantless removal standards and exigent circumstances.",
            "input": {
                "state": "CA",
                "county": "Los Angeles",
                "event_date": "2024-02-14",
                "facts": "Social worker conducted warrantless removal of youth from maternal home based on an anonymous referral of domestic dispute from the previous month."
            },
            "reasoning_task": "05_issue_spotting",
            "expected_behavior": {
                "jurisdiction": "CA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Cal. Welf. & Inst. Code § 306"],
                "epistemic_classification": ["ISSUE", "LAW", "ANALYSIS"]
            },
            "source": "California Welfare and Institutions Code § 306",
            "jurisdiction": "CA",
            "legal_date": "2024-02-14",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Spot adversary hearing deadline issues under Texas child protection procedure.",
            "input": {
                "state": "TX",
                "county": "Harris",
                "event_date": "2024-01-10",
                "facts": "DFPS removed minor in an emergency without prior court order on January 10; adversary hearing was set 21 days after removal without parent consent to extension."
            },
            "reasoning_task": "05_issue_spotting",
            "expected_behavior": {
                "jurisdiction": "TX",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Tex. Fam. Code § 262.201"],
                "epistemic_classification": ["ISSUE", "LAW", "ANALYSIS"]
            },
            "source": "Texas Family Code § 262.201",
            "jurisdiction": "TX",
            "legal_date": "2024-01-10",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Identify procedural relief available upon emergency removal under New York Family Court Act.",
            "input": {
                "state": "NY",
                "county": "Kings",
                "event_date": "2023-09-22",
                "facts": "Child protective service executed warrantless removal on Friday; Mother filed urgent application for immediate return of child on Monday morning."
            },
            "reasoning_task": "05_issue_spotting",
            "expected_behavior": {
                "jurisdiction": "NY",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["N.Y. Fam. Ct. Act § 1028"],
                "epistemic_classification": ["ISSUE", "LAW", "ANALYSIS"]
            },
            "source": "New York Family Court Act § 1028",
            "jurisdiction": "NY",
            "legal_date": "2023-09-22",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Spot shelter detention hearing timeline violations under Florida juvenile law.",
            "input": {
                "state": "FL",
                "county": "Miami-Dade",
                "event_date": "2024-06-05",
                "facts": "Officer placed youth into shelter care at 8:00 AM on Wednesday. Shelter hearing was not scheduled until Friday afternoon."
            },
            "reasoning_task": "05_issue_spotting",
            "expected_behavior": {
                "jurisdiction": "FL",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Fla. Stat. § 39.402"],
                "epistemic_classification": ["ISSUE", "LAW", "ANALYSIS"]
            },
            "source": "Florida Statutes § 39.402",
            "jurisdiction": "FL",
            "legal_date": "2024-06-05",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Spot threshold ICWA applicability and notice requirements in state custody proceeding.",
            "input": {
                "state": "US",
                "county": None,
                "event_date": "2023-08-15",
                "facts": "State agency initiated dependency proceeding where Mother stated the child was an enrolled member of a federally recognized Tribe, but no formal registered mail notice was sent to the Tribe."
            },
            "reasoning_task": "05_issue_spotting",
            "expected_behavior": {
                "jurisdiction": "US",
                "temporal_validation": True,
                "authority_tier": 0,
                "citation_required": True,
                "controlling_citations": ["25 U.S.C. § 1912"],
                "epistemic_classification": ["ISSUE", "LAW", "ANALYSIS"]
            },
            "source": "United States Code 25 U.S.C. § 1912",
            "jurisdiction": "US",
            "legal_date": "2023-08-15",
            "authority_level": "T0",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Spot issues regarding service of process and summons on non-custodial parent.",
            "input": {
                "state": "WA",
                "county": "Pierce",
                "event_date": "2024-04-02",
                "facts": "Dependency petition filed against Mother; Father was known and resided in adjacent county, but no summons or notice was issued to Father prior to shelter care hearing."
            },
            "reasoning_task": "05_issue_spotting",
            "expected_behavior": {
                "jurisdiction": "WA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["RCW 13.34.070"],
                "epistemic_classification": ["ISSUE", "LAW", "ANALYSIS"]
            },
            "source": "Washington State Legislature RCW 13.34.070",
            "jurisdiction": "WA",
            "legal_date": "2024-04-02",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Identify issues regarding reasonable efforts and preventive service obligations.",
            "input": {
                "state": "IL",
                "county": "Peoria",
                "event_date": "2023-12-01",
                "facts": "State filed for temporary custody without documenting any preventive services or efforts provided to alleviate housing instability prior to removal."
            },
            "reasoning_task": "05_issue_spotting",
            "expected_behavior": {
                "jurisdiction": "IL",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["705 ILCS 405/2-10"],
                "epistemic_classification": ["ISSUE", "LAW", "ANALYSIS"]
            },
            "source": "Illinois General Assembly 705 ILCS 405/2-10",
            "jurisdiction": "IL",
            "legal_date": "2023-12-01",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        }
    ]

    # Priority Task Family 06: Rule Extraction
    _SEEDS_06_RULE_EXTRACTION = [
        {
            "instruction": "Extract the statutory standard of proof required at a dependency fact-finding hearing under Washington law.",
            "input": {
                "state": "WA",
                "county": "Thurston",
                "event_date": "2024-01-20",
                "facts": "Court must adjudicate whether allegations in dependency petition are supported by sufficient evidence."
            },
            "reasoning_task": "06_rule_extraction",
            "expected_behavior": {
                "jurisdiction": "WA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["RCW 13.34.110"],
                "epistemic_classification": ["RULE", "STANDARD_OF_PROOF"]
            },
            "source": "Washington State Legislature RCW 13.34.110",
            "jurisdiction": "WA",
            "legal_date": "2024-01-20",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Extract the six statutory elements required to support petition for termination of parental rights in Washington.",
            "input": {
                "state": "WA",
                "county": "King",
                "event_date": "2024-04-10",
                "facts": "Agency seeks involuntary termination of parent-child relationship."
            },
            "reasoning_task": "06_rule_extraction",
            "expected_behavior": {
                "jurisdiction": "WA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["RCW 13.34.180"],
                "epistemic_classification": ["RULE", "ELEMENTS"]
            },
            "source": "Washington State Legislature RCW 13.34.180",
            "jurisdiction": "WA",
            "legal_date": "2024-04-10",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Extract the statutory standard for establishing urgent and immediate necessity for shelter custody in Illinois.",
            "input": {
                "state": "IL",
                "county": "Cook",
                "event_date": "2023-10-15",
                "facts": "Court conducting temporary custody hearing following emergency detention of minor."
            },
            "reasoning_task": "06_rule_extraction",
            "expected_behavior": {
                "jurisdiction": "IL",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["705 ILCS 405/2-10"],
                "epistemic_classification": ["RULE", "STANDARD"]
            },
            "source": "Illinois General Assembly 705 ILCS 405/2-10",
            "jurisdiction": "IL",
            "legal_date": "2023-10-15",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Extract the standard of proof and mandatory factors for permanent custody termination under Ohio law.",
            "input": {
                "state": "OH",
                "county": "Franklin",
                "event_date": "2024-02-05",
                "facts": "Public children services agency motions for permanent custody after 12 months in temporary custody."
            },
            "reasoning_task": "06_rule_extraction",
            "expected_behavior": {
                "jurisdiction": "OH",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["ORC § 2151.414"],
                "epistemic_classification": ["RULE", "STANDARD_OF_PROOF"]
            },
            "source": "Ohio Revised Code ORC § 2151.414",
            "jurisdiction": "OH",
            "legal_date": "2024-02-05",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Extract the statutory grounds and jurisdictional proof standard under California Welfare & Institutions Code Section 300.",
            "input": {
                "state": "CA",
                "county": "Orange",
                "event_date": "2023-11-20",
                "facts": "County department files petition asserting child falls within juvenile court dependency jurisdiction."
            },
            "reasoning_task": "06_rule_extraction",
            "expected_behavior": {
                "jurisdiction": "CA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Cal. Welf. & Inst. Code § 300"],
                "epistemic_classification": ["RULE", "ELEMENTS"]
            },
            "source": "California Welfare and Institutions Code § 300",
            "jurisdiction": "CA",
            "legal_date": "2023-11-20",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Extract the clear and convincing standard and adoptability finding required under California Section 366.26.",
            "input": {
                "state": "CA",
                "county": "San Diego",
                "event_date": "2024-05-02",
                "facts": "Selection and implementation hearing scheduled after termination of reunification services."
            },
            "reasoning_task": "06_rule_extraction",
            "expected_behavior": {
                "jurisdiction": "CA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Cal. Welf. & Inst. Code § 366.26"],
                "epistemic_classification": ["RULE", "BURDEN_OF_PROOF"]
            },
            "source": "California Welfare and Institutions Code § 366.26",
            "jurisdiction": "CA",
            "legal_date": "2024-05-02",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Extract the proof requirements for continuing child in temporary care at the 14-day adversary hearing in Texas.",
            "input": {
                "state": "TX",
                "county": "Dallas",
                "event_date": "2024-03-01",
                "facts": "Full adversary hearing conducted following ex parte emergency order under Chapter 262."
            },
            "reasoning_task": "06_rule_extraction",
            "expected_behavior": {
                "jurisdiction": "TX",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Tex. Fam. Code § 262.201"],
                "epistemic_classification": ["RULE", "BURDEN_OF_PROOF"]
            },
            "source": "Texas Family Code § 262.201",
            "jurisdiction": "TX",
            "legal_date": "2024-03-01",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Extract the legal standard for return of a child upon parent application under New York Family Court Act Section 1028.",
            "input": {
                "state": "NY",
                "county": "Bronx",
                "event_date": "2023-12-12",
                "facts": "Parent applies for immediate return of child temporarily removed without consent."
            },
            "reasoning_task": "06_rule_extraction",
            "expected_behavior": {
                "jurisdiction": "NY",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["N.Y. Fam. Ct. Act § 1028"],
                "epistemic_classification": ["RULE", "STANDARD"]
            },
            "source": "New York Family Court Act § 1028",
            "jurisdiction": "NY",
            "legal_date": "2023-12-12",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Extract the mandatory statutory timeframes and probable cause standard for shelter placement in Florida.",
            "input": {
                "state": "FL",
                "county": "Orange",
                "event_date": "2024-04-18",
                "facts": "Child placed in shelter care and court evaluates probable cause for continuing detention."
            },
            "reasoning_task": "06_rule_extraction",
            "expected_behavior": {
                "jurisdiction": "FL",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Fla. Stat. § 39.402"],
                "epistemic_classification": ["RULE", "TIMEFRAME"]
            },
            "source": "Florida Statutes § 39.402",
            "jurisdiction": "FL",
            "legal_date": "2024-04-18",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Extract the heightened evidentiary standard and qualified expert witness requirement under 25 U.S.C. Section 1912.",
            "input": {
                "state": "US",
                "county": None,
                "event_date": "2024-01-15",
                "facts": "State court considers involuntary foster care placement and parental rights termination involving Indian child."
            },
            "reasoning_task": "06_rule_extraction",
            "expected_behavior": {
                "jurisdiction": "US",
                "temporal_validation": True,
                "authority_tier": 0,
                "citation_required": True,
                "controlling_citations": ["25 U.S.C. § 1912"],
                "epistemic_classification": ["RULE", "EVIDENTIARY_BURDEN"]
            },
            "source": "United States Code 25 U.S.C. § 1912",
            "jurisdiction": "US",
            "legal_date": "2024-01-15",
            "authority_level": "T0",
            "dataset_version": "0.3.0"
        }
    ]

    # Priority Task Family 13: Parent Rights
    _SEEDS_13_PARENT_RIGHTS = [
        {
            "instruction": "Evaluate indigent parent's statutory right to appointed counsel and meaningful representation.",
            "input": {
                "state": "WA",
                "county": "Whatcom",
                "event_date": "2024-02-11",
                "facts": "Mother appeared at initial shelter care hearing without counsel due to lack of notice; court proceeded to enter out-of-home placement order without appointing counsel."
            },
            "reasoning_task": "13_parent_rights",
            "expected_behavior": {
                "jurisdiction": "WA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["RCW 13.34.090"],
                "epistemic_classification": ["RIGHT", "DUE_PROCESS"]
            },
            "source": "Washington State Legislature RCW 13.34.090",
            "jurisdiction": "WA",
            "legal_date": "2024-02-11",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Analyze parent's statutory right to visitation and family time during dependency proceedings.",
            "input": {
                "state": "WA",
                "county": "Snohomish",
                "event_date": "2024-05-15",
                "facts": "Caseworker unilaterally suspended Father's weekly visits after Father missed one drug screening test, without court order or finding of imminent harm."
            },
            "reasoning_task": "13_parent_rights",
            "expected_behavior": {
                "jurisdiction": "WA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["RCW 13.34.136"],
                "epistemic_classification": ["RIGHT", "VISITATION"]
            },
            "source": "Washington State Legislature RCW 13.34.136",
            "jurisdiction": "WA",
            "legal_date": "2024-05-15",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Determine statutory right of respondent parent to appointed attorney under Illinois Juvenile Court Act.",
            "input": {
                "state": "IL",
                "county": "Cook",
                "event_date": "2023-11-28",
                "facts": "Father was named as respondent in neglect petition but was told he must represent himself because he had part-time minimum wage employment."
            },
            "reasoning_task": "13_parent_rights",
            "expected_behavior": {
                "jurisdiction": "IL",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["705 ILCS 405/2-9"],
                "epistemic_classification": ["RIGHT", "COUNSEL"]
            },
            "source": "Illinois General Assembly 705 ILCS 405/2-9",
            "jurisdiction": "IL",
            "legal_date": "2023-11-28",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Evaluate parent's right to cross-examination and discovery in Ohio dependency adjudication.",
            "input": {
                "state": "OH",
                "county": "Hamilton",
                "event_date": "2024-03-25",
                "facts": "Agency submitted hearsay psychological evaluation without providing psychologist for cross-examination at adjudicatory hearing."
            },
            "reasoning_task": "13_parent_rights",
            "expected_behavior": {
                "jurisdiction": "OH",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["ORC § 2151.35"],
                "epistemic_classification": ["RIGHT", "CONFRONTATION"]
            },
            "source": "Ohio Revised Code ORC § 2151.35",
            "jurisdiction": "OH",
            "legal_date": "2024-03-25",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Analyze parent's statutory right to separate appointed counsel in California dependency proceedings.",
            "input": {
                "state": "CA",
                "county": "Riverside",
                "event_date": "2024-01-18",
                "facts": "One attorney was appointed to represent both Mother and Father despite conflicting factual defenses regarding non-accidental trauma."
            },
            "reasoning_task": "13_parent_rights",
            "expected_behavior": {
                "jurisdiction": "CA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Cal. Welf. & Inst. Code § 317"],
                "epistemic_classification": ["RIGHT", "CONFLICT_OF_INTEREST"]
            },
            "source": "California Welfare and Institutions Code § 317",
            "jurisdiction": "CA",
            "legal_date": "2024-01-18",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Evaluate parent's right to active reunification services under California child welfare law.",
            "input": {
                "state": "CA",
                "county": "Santa Clara",
                "event_date": "2023-12-05",
                "facts": "Agency failed to provide mental health referrals for 6 months while child was in foster care, then recommended terminating services."
            },
            "reasoning_task": "13_parent_rights",
            "expected_behavior": {
                "jurisdiction": "CA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Cal. Welf. & Inst. Code § 361.5"],
                "epistemic_classification": ["RIGHT", "REUNIFICATION"]
            },
            "source": "California Welfare and Institutions Code § 361.5",
            "jurisdiction": "CA",
            "legal_date": "2023-12-05",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Evaluate parent's right to prompt notice and advisement of rights upon emergency child removal in Texas.",
            "input": {
                "state": "TX",
                "county": "Travis",
                "event_date": "2024-04-22",
                "facts": "Agency removed child from school and did not inform Mother of child's whereabouts or her right to counsel until 5 days later."
            },
            "reasoning_task": "13_parent_rights",
            "expected_behavior": {
                "jurisdiction": "TX",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Tex. Fam. Code § 262.109"],
                "epistemic_classification": ["RIGHT", "NOTICE"]
            },
            "source": "Texas Family Code § 262.109",
            "jurisdiction": "TX",
            "legal_date": "2024-04-22",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Analyze parent's statutory entitlement to an immediate Section 1028 return hearing in New York.",
            "input": {
                "state": "NY",
                "county": "Queens",
                "event_date": "2024-03-08",
                "facts": "Mother filed petition for return of child; agency argued court should wait until regularly scheduled conference in 4 weeks."
            },
            "reasoning_task": "13_parent_rights",
            "expected_behavior": {
                "jurisdiction": "NY",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["N.Y. Fam. Ct. Act § 1028"],
                "epistemic_classification": ["RIGHT", "EXPEDITED_HEARING"]
            },
            "source": "New York Family Court Act § 1028",
            "jurisdiction": "NY",
            "legal_date": "2024-03-08",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Evaluate parent's right to appointed counsel at first shelter appearance in Florida.",
            "input": {
                "state": "FL",
                "county": "Hillsborough",
                "event_date": "2023-10-09",
                "facts": "Indigent Father was denied appointed counsel at emergency shelter placement hearing."
            },
            "reasoning_task": "13_parent_rights",
            "expected_behavior": {
                "jurisdiction": "FL",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Fla. Stat. § 39.402"],
                "epistemic_classification": ["RIGHT", "COUNSEL"]
            },
            "source": "Florida Statutes § 39.402",
            "jurisdiction": "FL",
            "legal_date": "2023-10-09",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Assess parent's federal statutory rights to court documents and appointed counsel under ICWA.",
            "input": {
                "state": "US",
                "county": None,
                "event_date": "2024-02-28",
                "facts": "Tribal parent was denied access to confidential social worker reports prior to involuntary foster care placement hearing."
            },
            "reasoning_task": "13_parent_rights",
            "expected_behavior": {
                "jurisdiction": "US",
                "temporal_validation": True,
                "authority_tier": 0,
                "citation_required": True,
                "controlling_citations": ["25 U.S.C. § 1912"],
                "epistemic_classification": ["RIGHT", "ACCESS_TO_RECORDS"]
            },
            "source": "United States Code 25 U.S.C. § 1912",
            "jurisdiction": "US",
            "legal_date": "2024-02-28",
            "authority_level": "T0",
            "dataset_version": "0.3.0"
        }
    ]

    # Priority Task Family 17: Due Process
    _SEEDS_17_DUE_PROCESS = [
        {
            "instruction": "Assess procedural due process violation where shelter care hearing held beyond 72 hours without parent notice.",
            "input": {
                "state": "WA",
                "county": "Clark",
                "event_date": "2024-03-05",
                "facts": "Child removed on Monday; shelter care hearing held the following Monday with no notice provided to Mother."
            },
            "reasoning_task": "17_due_process",
            "expected_behavior": {
                "jurisdiction": "WA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["RCW 13.34.065"],
                "epistemic_classification": ["DUE_PROCESS", "TIMEFRAME"]
            },
            "source": "Washington State Legislature RCW 13.34.065",
            "jurisdiction": "WA",
            "legal_date": "2024-03-05",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Evaluate due process necessity of notice and judicial review prior to entry of emergency custody order.",
            "input": {
                "state": "WA",
                "county": "Pierce",
                "event_date": "2024-06-12",
                "facts": "Court granted ex parte pick-up order without corroborating sworn affidavit demonstrating imminent danger."
            },
            "reasoning_task": "17_due_process",
            "expected_behavior": {
                "jurisdiction": "WA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["RCW 13.34.050"],
                "epistemic_classification": ["DUE_PROCESS", "EX_PARTE"]
            },
            "source": "Washington State Legislature RCW 13.34.050",
            "jurisdiction": "WA",
            "legal_date": "2024-06-12",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Analyze due process violation for failure to hold temporary custody hearing within statutory 48 hours.",
            "input": {
                "state": "IL",
                "county": "Cook",
                "event_date": "2023-11-14",
                "facts": "Minor detained by agency on Wednesday at noon; initial temporary custody hearing held Tuesday morning."
            },
            "reasoning_task": "17_due_process",
            "expected_behavior": {
                "jurisdiction": "IL",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["705 ILCS 405/2-10"],
                "epistemic_classification": ["DUE_PROCESS", "STATUTORY_DEADLINE"]
            },
            "source": "Illinois General Assembly 705 ILCS 405/2-10",
            "jurisdiction": "IL",
            "legal_date": "2023-11-14",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Evaluate mandatory 90-day adjudicatory hearing rule under Illinois child protection due process standards.",
            "input": {
                "state": "IL",
                "county": "Kane",
                "event_date": "2024-04-05",
                "facts": "Adjudicatory trial delayed beyond 90 days from service of petition without written waiver or good cause finding."
            },
            "reasoning_task": "17_due_process",
            "expected_behavior": {
                "jurisdiction": "IL",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["705 ILCS 405/2-14"],
                "epistemic_classification": ["DUE_PROCESS", "SPEEDY_ADJUDICATION"]
            },
            "source": "Illinois General Assembly 705 ILCS 405/2-14",
            "jurisdiction": "IL",
            "legal_date": "2024-04-05",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Assess due process notice and 72-hour hearing requirement under Ohio Revised Code Chapter 2151.",
            "input": {
                "state": "OH",
                "county": "Summit",
                "event_date": "2024-01-22",
                "facts": "Parent received no formal notice or summons prior to shelter care hearing held 5 days following child apprehension."
            },
            "reasoning_task": "17_due_process",
            "expected_behavior": {
                "jurisdiction": "OH",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["ORC § 2151.314"],
                "epistemic_classification": ["DUE_PROCESS", "NOTICE"]
            },
            "source": "Ohio Revised Code ORC § 2151.314",
            "jurisdiction": "OH",
            "legal_date": "2024-01-22",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Evaluate due process rights to notice and contested detention hearing under California juvenile court procedure.",
            "input": {
                "state": "CA",
                "county": "Fresno",
                "event_date": "2023-12-18",
                "facts": "Detention hearing conducted in parent's absence where agency failed to exercise due diligence to notify non-custodial parent."
            },
            "reasoning_task": "17_due_process",
            "expected_behavior": {
                "jurisdiction": "CA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Cal. Welf. & Inst. Code § 315"],
                "epistemic_classification": ["DUE_PROCESS", "NOTICE"]
            },
            "source": "California Welfare and Institutions Code § 315",
            "jurisdiction": "CA",
            "legal_date": "2023-12-18",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Evaluate statutory dismissal mandate under Texas Family Code Section 263.401 as a due process limitation.",
            "input": {
                "state": "TX",
                "county": "Bexar",
                "event_date": "2024-05-10",
                "facts": "Suit filed by DFPS exceeded 365 days without trial on the merits commencing or statutory extension granted."
            },
            "reasoning_task": "17_due_process",
            "expected_behavior": {
                "jurisdiction": "TX",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Tex. Fam. Code § 263.401"],
                "epistemic_classification": ["DUE_PROCESS", "MANDATORY_DISMISSAL"]
            },
            "source": "Texas Family Code § 263.401",
            "jurisdiction": "TX",
            "legal_date": "2024-05-10",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Assess due process limits on warrantless emergency child removals under New York law.",
            "input": {
                "state": "NY",
                "county": "New York",
                "event_date": "2024-02-16",
                "facts": "Caseworker removed children without court order where there was ample time to apply for judicial warrant under Section 1027."
            },
            "reasoning_task": "17_due_process",
            "expected_behavior": {
                "jurisdiction": "NY",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["N.Y. Fam. Ct. Act § 1024"],
                "epistemic_classification": ["DUE_PROCESS", "EXIGENCY"]
            },
            "source": "New York Family Court Act § 1024",
            "jurisdiction": "NY",
            "legal_date": "2024-02-16",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Evaluate statutory 24-hour hearing mandate as a constitutional procedural due process requirement in Florida.",
            "input": {
                "state": "FL",
                "county": "Broward",
                "event_date": "2023-11-30",
                "facts": "Child held in shelter care for 72 hours before parent was afforded any judicial review of the emergency removal."
            },
            "reasoning_task": "17_due_process",
            "expected_behavior": {
                "jurisdiction": "FL",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Fla. Stat. § 39.402"],
                "epistemic_classification": ["DUE_PROCESS", "HEARING_RIGHT"]
            },
            "source": "Florida Statutes § 39.402",
            "jurisdiction": "FL",
            "legal_date": "2023-11-30",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Evaluate active efforts mandate as an enforceable procedural due process prerequisite under ICWA.",
            "input": {
                "state": "US",
                "county": None,
                "event_date": "2024-03-20",
                "facts": "Agency sought foster placement of Indian child without demonstrating active remedial efforts provided to prevent breakup of Indian family."
            },
            "reasoning_task": "17_due_process",
            "expected_behavior": {
                "jurisdiction": "US",
                "temporal_validation": True,
                "authority_tier": 0,
                "citation_required": True,
                "controlling_citations": ["25 U.S.C. § 1912"],
                "epistemic_classification": ["DUE_PROCESS", "ACTIVE_EFFORTS"]
            },
            "source": "United States Code 25 U.S.C. § 1912",
            "jurisdiction": "US",
            "legal_date": "2024-03-20",
            "authority_level": "T0",
            "dataset_version": "0.3.0"
        }
    ]

    # Priority Task Family 19: Search & Seizure
    _SEEDS_19_SEARCH_SEIZURE = [
        {
            "instruction": "Evaluate Fourth Amendment standard for warrantless protective custody of a child under Washington law.",
            "input": {
                "state": "WA",
                "county": "Yakima",
                "event_date": "2024-02-08",
                "facts": "Police officer took child into custody without warrant upon parent refusal to allow voluntary drug screen, with no signs of physical abuse."
            },
            "reasoning_task": "19_search_seizure",
            "expected_behavior": {
                "jurisdiction": "WA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["RCW 13.34.055"],
                "epistemic_classification": ["FOURTH_AMENDMENT", "WARRANTLESS_SEIZURE"]
            },
            "source": "Washington State Legislature RCW 13.34.055",
            "jurisdiction": "WA",
            "legal_date": "2024-02-08",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Analyze judicial warrant requirement for child removal where imminent danger is absent under Washington law.",
            "input": {
                "state": "WA",
                "county": "Spokane",
                "event_date": "2024-04-14",
                "facts": "Caseworker entered home and seized minor based on non-emergency unhygienic conditions without obtaining judicial court order."
            },
            "reasoning_task": "19_search_seizure",
            "expected_behavior": {
                "jurisdiction": "WA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["RCW 13.34.050"],
                "epistemic_classification": ["FOURTH_AMENDMENT", "COURT_ORDER"]
            },
            "source": "Washington State Legislature RCW 13.34.050",
            "jurisdiction": "WA",
            "legal_date": "2024-04-14",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Evaluate warrantless seizure standard of urgent necessity under Illinois Juvenile Court Act.",
            "input": {
                "state": "IL",
                "county": "Cook",
                "event_date": "2023-10-24",
                "facts": "Caseworker accompanied by police forced entry into apartment without warrant to conduct home assessment based on hotline tip."
            },
            "reasoning_task": "19_search_seizure",
            "expected_behavior": {
                "jurisdiction": "IL",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["705 ILCS 405/2-10"],
                "epistemic_classification": ["FOURTH_AMENDMENT", "HOME_ENTRY"]
            },
            "source": "Illinois General Assembly 705 ILCS 405/2-10",
            "jurisdiction": "IL",
            "legal_date": "2023-10-24",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Assess statutory limitations on warrantless apprehension of children under Ohio Revised Code 2151.31.",
            "input": {
                "state": "OH",
                "county": "Montgomery",
                "event_date": "2024-03-19",
                "facts": "Law enforcement apprehended child from public park based on unsubstantiated truancy allegation without reasonable cause of immediate danger."
            },
            "reasoning_task": "19_search_seizure",
            "expected_behavior": {
                "jurisdiction": "OH",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["ORC § 2151.31"],
                "epistemic_classification": ["FOURTH_AMENDMENT", "APPREHENSION"]
            },
            "source": "Ohio Revised Code ORC § 2151.31",
            "jurisdiction": "OH",
            "legal_date": "2024-03-19",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Evaluate exigency requirements for social worker warrantless detention under California Welfare & Institutions Code 306.",
            "input": {
                "state": "CA",
                "county": "Alameda",
                "event_date": "2024-01-29",
                "facts": "Social worker seized infant from hospital without warrant despite hospital staff agreeing to hold infant until morning judicial hours."
            },
            "reasoning_task": "19_search_seizure",
            "expected_behavior": {
                "jurisdiction": "CA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Cal. Welf. & Inst. Code § 306"],
                "epistemic_classification": ["FOURTH_AMENDMENT", "EXIGENCY"]
            },
            "source": "California Welfare and Institutions Code § 306",
            "jurisdiction": "CA",
            "legal_date": "2024-01-29",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Analyze Fourth Amendment implications of peace officer temporary custody under California Section 305.",
            "input": {
                "state": "CA",
                "county": "San Francisco",
                "event_date": "2023-11-12",
                "facts": "Police officer detained youth on suspicion of emotional distress without showing physical injury or severe medical emergency."
            },
            "reasoning_task": "19_search_seizure",
            "expected_behavior": {
                "jurisdiction": "CA",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Cal. Welf. & Inst. Code § 305"],
                "epistemic_classification": ["FOURTH_AMENDMENT", "POLICE_SEIZURE"]
            },
            "source": "California Welfare and Institutions Code § 305",
            "jurisdiction": "CA",
            "legal_date": "2023-11-12",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Evaluate emergency removal without court order under Texas Family Code Section 262.104.",
            "input": {
                "state": "TX",
                "county": "Tarrant",
                "event_date": "2024-05-24",
                "facts": "DFPS investigator entered residence without consent and removed minor based on anonymous allegation of marijuana odor."
            },
            "reasoning_task": "19_search_seizure",
            "expected_behavior": {
                "jurisdiction": "TX",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Tex. Fam. Code § 262.104"],
                "epistemic_classification": ["FOURTH_AMENDMENT", "SEARCH_SEIZURE"]
            },
            "source": "Texas Family Code § 262.104",
            "jurisdiction": "TX",
            "legal_date": "2024-05-24",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Evaluate statutory limits on emergency removal without court order under New York Family Court Act Section 1024.",
            "input": {
                "state": "NY",
                "county": "Suffolk",
                "event_date": "2023-12-28",
                "facts": "CPS investigator removed child from daycare without court order or parental consent where no imminent danger existed."
            },
            "reasoning_task": "19_search_seizure",
            "expected_behavior": {
                "jurisdiction": "NY",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["N.Y. Fam. Ct. Act § 1024"],
                "epistemic_classification": ["FOURTH_AMENDMENT", "STATUTORY_LIMITS"]
            },
            "source": "New York Family Court Act § 1024",
            "jurisdiction": "NY",
            "legal_date": "2023-12-28",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Assess law enforcement protective custody requirements under Florida Statutes Section 39.401.",
            "input": {
                "state": "FL",
                "county": "Pinellas",
                "event_date": "2024-02-22",
                "facts": "Deputy took minor into custody without warrant following non-violent verbal disagreement between siblings."
            },
            "reasoning_task": "19_search_seizure",
            "expected_behavior": {
                "jurisdiction": "FL",
                "temporal_validation": True,
                "authority_tier": 4,
                "citation_required": True,
                "controlling_citations": ["Fla. Stat. § 39.401"],
                "epistemic_classification": ["FOURTH_AMENDMENT", "PROTECTIVE_CUSTODY"]
            },
            "source": "Florida Statutes § 39.401",
            "jurisdiction": "FL",
            "legal_date": "2024-02-22",
            "authority_level": "T4",
            "dataset_version": "0.3.0"
        },
        {
            "instruction": "Analyze Fourth Amendment protections against warrantless child seizure under federal constitutional standards.",
            "input": {
                "state": "US",
                "county": None,
                "event_date": "2024-01-08",
                "facts": "State child protection agency seized minor from private dwelling without judicial warrant, exigent circumstances, or parental consent."
            },
            "reasoning_task": "19_search_seizure",
            "expected_behavior": {
                "jurisdiction": "US",
                "temporal_validation": True,
                "authority_tier": 0,
                "citation_required": True,
                "controlling_citations": ["42 U.S.C. § 5106a"],
                "epistemic_classification": ["FOURTH_AMENDMENT", "CONSTITUTIONAL_SEIZURE"]
            },
            "source": "United States Code 42 U.S.C. § 5106a",
            "jurisdiction": "US",
            "legal_date": "2024-01-08",
            "authority_level": "T0",
            "dataset_version": "0.3.0"
        }
    ]

    PRIORITY_SEEDS_MAP = {
        "05_issue_spotting": _SEEDS_05_ISSUE_SPOTTING,
        "06_rule_extraction": _SEEDS_06_RULE_EXTRACTION,
        "13_parent_rights": _SEEDS_13_PARENT_RIGHTS,
        "17_due_process": _SEEDS_17_DUE_PROCESS,
        "19_search_seizure": _SEEDS_19_SEARCH_SEIZURE,
    }

    @classmethod
    def generate_seeds(cls, task_family: str, count: int = 10) -> List[Dict[str, Any]]:
        """Generates concrete, legally grounded, schema-validated seed training examples."""
        if count <= 0:
            return []

        # Check priority families first
        if task_family in cls.PRIORITY_SEEDS_MAP:
            base_pool = cls.PRIORITY_SEEDS_MAP[task_family]
            examples = []
            while len(examples) < count:
                for item in base_pool:
                    if len(examples) >= count:
                        break
                    # Validate against schema
                    DatasetSchema.validate(item)
                    examples.append(item)
            return examples

        # Fallback generator for other task families in the curriculum
        examples = []
        for idx in range(count):
            ex = {
                "instruction": f"Apply legal reasoning principles for curriculum task {task_family}.",
                "input": {
                    "state": "WA",
                    "county": "King",
                    "event_date": "2024-03-15",
                    "facts": f"Factual scenario {idx + 1} evaluating procedural rights under governing statutory frameworks."
                },
                "reasoning_task": task_family,
                "expected_behavior": {
                    "jurisdiction": "WA",
                    "temporal_validation": True,
                    "authority_tier": 4,
                    "citation_required": True,
                    "controlling_citations": ["RCW 13.34.065"],
                    "epistemic_classification": ["LAW", "ANALYSIS"]
                },
                "source": "Washington State Legislature RCW 13.34.065",
                "jurisdiction": "WA",
                "legal_date": "2024-03-15",
                "authority_level": "T4",
                "dataset_version": "0.3.0"
            }
            DatasetSchema.validate(ex)
            examples.append(ex)

        return examples

    @classmethod
    def write_seeds_to_disk(cls, task_family: str, count: int = 10, target_dir: Optional[Path] = None) -> Path:
        """Generates seed records and writes them to training/datasets/{task_family}/examples.jsonl."""
        seeds = cls.generate_seeds(task_family, count)
        if target_dir is None:
            # Default to repo root training/datasets/
            repo_root = Path(__file__).parent.parent.parent
            out_dir = repo_root / "training" / "datasets" / task_family
        else:
            out_dir = target_dir / task_family

        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "examples.jsonl"
        with open(out_file, "w", encoding="utf-8") as f:
            for item in seeds:
                f.write(json.dumps(item) + "\n")
        return out_file

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
