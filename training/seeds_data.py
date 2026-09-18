"""Comprehensive Seed Data for all 15 Legal-GPT Training Task Families."""

# 02_temporal_law (10 examples)
SEEDS_02_TEMPORAL_LAW = [
    {
        "instruction": "Analyze temporal applicability of statutory shelter care deadlines following emergency custody.",
        "input": {"state": "WA", "county": "King", "event_date": "2024-03-01", "facts": "Child removed on Friday afternoon. Shelter hearing held on Thursday afternoon."},
        "reasoning_task": "02_temporal_law",
        "expected_behavior": {"jurisdiction": "WA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["RCW 13.34.065"], "epistemic_classification": ["LAW", "ANALYSIS"]},
        "source": "Washington State Legislature RCW 13.34.065", "jurisdiction": "WA", "legal_date": "2024-03-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate temporal compliance with mandatory 30-day statutory adjudicatory hearing clock.",
        "input": {"state": "IL", "county": "Cook", "event_date": "2024-04-10", "facts": "Dependency petition filed April 10. Trial scheduled for June 20 without waiver or good cause continuance."},
        "reasoning_task": "02_temporal_law",
        "expected_behavior": {"jurisdiction": "IL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["705 ILCS 405/2-14"], "epistemic_classification": ["LAW", "ANALYSIS"]},
        "source": "Illinois General Assembly 705 ILCS 405/2-14", "jurisdiction": "IL", "legal_date": "2024-04-10", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess whether shelter care hearing met Ohio 72-hour temporal deadline excluding weekend.",
        "input": {"state": "OH", "county": "Franklin", "event_date": "2024-01-12", "facts": "Child taken into emergency custody on Friday morning; detention hearing convened the following Wednesday."},
        "reasoning_task": "02_temporal_law",
        "expected_behavior": {"jurisdiction": "OH", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["ORC § 2151.314"], "epistemic_classification": ["LAW", "ANALYSIS"]},
        "source": "Ohio Revised Code ORC § 2151.314", "jurisdiction": "OH", "legal_date": "2024-01-12", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Compute operative detention hearing time limit under California juvenile court law.",
        "input": {"state": "CA", "county": "Los Angeles", "event_date": "2024-02-15", "facts": "Child taken into custody on Thursday; detention hearing scheduled for Tuesday afternoon."},
        "reasoning_task": "02_temporal_law",
        "expected_behavior": {"jurisdiction": "CA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Cal. Welf. & Inst. Code § 315"], "epistemic_classification": ["LAW", "ANALYSIS"]},
        "source": "California Welfare & Institutions Code § 315", "jurisdiction": "CA", "legal_date": "2024-02-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Determine whether full adversary hearing occurred within Texas 14-day statutory window.",
        "input": {"state": "TX", "county": "Harris", "event_date": "2024-03-05", "facts": "Emergency custody order entered March 5; adversary hearing docketed for March 28."},
        "reasoning_task": "02_temporal_law",
        "expected_behavior": {"jurisdiction": "TX", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Tex. Fam. Code § 262.201"], "epistemic_classification": ["LAW", "ANALYSIS"]},
        "source": "Texas Family Code § 262.201", "jurisdiction": "TX", "legal_date": "2024-03-05", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate Florida strict 24-hour statutory shelter hearing requirement.",
        "input": {"state": "FL", "county": "Miami-Dade", "event_date": "2024-05-02", "facts": "Child removed by investigator Thursday 10:00 AM; shelter hearing held Saturday 11:00 AM."},
        "reasoning_task": "02_temporal_law",
        "expected_behavior": {"jurisdiction": "FL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Fla. Stat. § 39.402"], "epistemic_classification": ["LAW", "ANALYSIS"]},
        "source": "Florida Statutes § 39.402", "jurisdiction": "FL", "legal_date": "2024-05-02", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Audit Pennsylvania 72-hour informal hearing rule from emergency custody taking.",
        "input": {"state": "PA", "county": "Philadelphia", "event_date": "2024-06-03", "facts": "Police took child into protective custody Monday 3:00 PM; informal hearing held Friday 10:00 AM."},
        "reasoning_task": "02_temporal_law",
        "expected_behavior": {"jurisdiction": "PA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["42 Pa. C.S. § 6332"], "epistemic_classification": ["LAW", "ANALYSIS"]},
        "source": "Pennsylvania Consolidated Statutes 42 Pa. C.S. § 6332", "jurisdiction": "PA", "legal_date": "2024-06-03", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Calculate Georgia 72-hour preliminary protective hearing over holiday period.",
        "input": {"state": "GA", "county": "Fulton", "event_date": "2024-07-02", "facts": "Child removed Tuesday afternoon; July 4th court holiday intervened; hearing held the following Monday."},
        "reasoning_task": "02_temporal_law",
        "expected_behavior": {"jurisdiction": "GA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["O.C.G.A. § 15-11-145"], "epistemic_classification": ["LAW", "ANALYSIS"]},
        "source": "Official Code of Georgia Annotated O.C.G.A. § 15-11-145", "jurisdiction": "GA", "legal_date": "2024-07-02", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Review North Carolina 7-day nonsecure custody review deadline.",
        "input": {"state": "NC", "county": "Wake", "event_date": "2024-08-01", "facts": "Nonsecure custody order issued August 1; initial review hearing scheduled for August 15."},
        "reasoning_task": "02_temporal_law",
        "expected_behavior": {"jurisdiction": "NC", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["N.C.G.S. § 7B-506"], "epistemic_classification": ["LAW", "ANALYSIS"]},
        "source": "North Carolina General Statutes N.C.G.S. § 7B-506", "jurisdiction": "NC", "legal_date": "2024-08-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Check Michigan 24-hour preliminary hearing deadline following protective placement.",
        "input": {"state": "MI", "county": "Wayne", "event_date": "2024-09-04", "facts": "Child placed in temporary shelter Wednesday 2:00 PM; preliminary hearing held Friday 4:00 PM."},
        "reasoning_task": "02_temporal_law",
        "expected_behavior": {"jurisdiction": "MI", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["MCL 712A.13a"], "epistemic_classification": ["LAW", "ANALYSIS"]},
        "source": "Michigan Compiled Laws MCL 712A.13a", "jurisdiction": "MI", "legal_date": "2024-09-04", "authority_level": "T4", "dataset_version": "0.3.0"
    },
]

# 03_authority_ranking (10 examples)
SEEDS_03_AUTHORITY_RANKING = [
    {
        "instruction": "Rank controlling authority between federal Title IV-E mandates and conflicting state practice.",
        "input": {"state": "US", "event_date": "2024-01-15", "facts": "State agency policy allows 90 days before completing initial written service plan; Title IV-E federal standard requires timely plan."},
        "reasoning_task": "03_authority_ranking",
        "expected_behavior": {"jurisdiction": "US", "temporal_validation": True, "authority_tier": 1, "citation_required": True, "controlling_citations": ["42 U.S.C. § 671"], "epistemic_classification": ["LAW", "HIERARCHY"]},
        "source": "United States Code 42 U.S.C. § 671", "jurisdiction": "US", "legal_date": "2024-01-15", "authority_level": "T1", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Determine whether federal ICWA standard of active efforts outranks state reasonable efforts statute.",
        "input": {"state": "US", "event_date": "2024-02-10", "facts": "In an Indian child custody proceeding, agency provided standard state referrals rather than active remedial efforts."},
        "reasoning_task": "03_authority_ranking",
        "expected_behavior": {"jurisdiction": "US", "temporal_validation": True, "authority_tier": 1, "citation_required": True, "controlling_citations": ["25 U.S.C. § 1912"], "epistemic_classification": ["LAW", "HIERARCHY"]},
        "source": "United States Code 25 U.S.C. § 1912", "jurisdiction": "US", "legal_date": "2024-02-10", "authority_level": "T1", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Rank Washington state statute over internal DCYF field operations manual policy.",
        "input": {"state": "WA", "county": "Pierce", "event_date": "2024-03-01", "facts": "Caseworker manual suggested relative search could occur after 30 days; primary RCW mandates relative notification at shelter care."},
        "reasoning_task": "03_authority_ranking",
        "expected_behavior": {"jurisdiction": "WA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["RCW 13.34.065"], "epistemic_classification": ["LAW", "HIERARCHY"]},
        "source": "Washington State Legislature RCW 13.34.065", "jurisdiction": "WA", "legal_date": "2024-03-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Establish supremacy of statutory proof standards over informal caseworker risk assessments in California.",
        "input": {"state": "CA", "county": "Orange", "event_date": "2024-03-20", "facts": "Agency structured decision-making tool rated family high risk; petition lacked legally admissible proof under WIC § 355."},
        "reasoning_task": "03_authority_ranking",
        "expected_behavior": {"jurisdiction": "CA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Cal. Welf. & Inst. Code § 355"], "epistemic_classification": ["LAW", "HIERARCHY"]},
        "source": "California Welfare & Institutions Code § 355", "jurisdiction": "CA", "legal_date": "2024-03-20", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Rank Illinois Juvenile Court Act statutory commands over DCFS administrative directives.",
        "input": {"state": "IL", "county": "DuPage", "event_date": "2024-04-05", "facts": "DCFS internal memo purported to delay court filing; Juvenile Court Act mandates immediate petition filing upon custody."},
        "reasoning_task": "03_authority_ranking",
        "expected_behavior": {"jurisdiction": "IL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["705 ILCS 405/2-10"], "epistemic_classification": ["LAW", "HIERARCHY"]},
        "source": "Illinois General Assembly 705 ILCS 405/2-10", "jurisdiction": "IL", "legal_date": "2024-04-05", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate statutory authority hierarchy between Family Court Act and local DSS practice in New York.",
        "input": {"state": "NY", "county": "New York", "event_date": "2024-05-15", "facts": "Local caseworker argued 1028 application was untimely under local practice; Family Court Act § 1028 grants absolute 3-day right."},
        "reasoning_task": "03_authority_ranking",
        "expected_behavior": {"jurisdiction": "NY", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["N.Y. Fam. Ct. Act § 1028"], "epistemic_classification": ["LAW", "HIERARCHY"]},
        "source": "New York Family Court Act § 1028", "jurisdiction": "NY", "legal_date": "2024-05-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Rank Florida statutory hearing deadline above judicial scheduling convenience.",
        "input": {"state": "FL", "county": "Orange", "event_date": "2024-06-01", "facts": "Court calendar congested; judge sought to defer shelter hearing to 72 hours despite Florida 24-hour statutory command."},
        "reasoning_task": "03_authority_ranking",
        "expected_behavior": {"jurisdiction": "FL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Fla. Stat. § 39.402"], "epistemic_classification": ["LAW", "HIERARCHY"]},
        "source": "Florida Statutes § 39.402", "jurisdiction": "FL", "legal_date": "2024-06-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Determine authority hierarchy between Ohio Revised Code and ODJFS county policy manual.",
        "input": {"state": "OH", "county": "Hamilton", "event_date": "2024-06-18", "facts": "County manual omitted mandatory reasonable efforts findings; ORC § 2151.419 mandates explicit judicial determination."},
        "reasoning_task": "03_authority_ranking",
        "expected_behavior": {"jurisdiction": "OH", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["ORC § 2151.419"], "epistemic_classification": ["LAW", "HIERARCHY"]},
        "source": "Ohio Revised Code ORC § 2151.419", "jurisdiction": "OH", "legal_date": "2024-06-18", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Rank Pennsylvania statutory right to counsel at all proceedings above local court rules.",
        "input": {"state": "PA", "county": "Allegheny", "event_date": "2024-07-10", "facts": "Local practice conducted informal shelter hearings without defense counsel present; 42 Pa. C.S. § 6337 mandates counsel at all stages."},
        "reasoning_task": "03_authority_ranking",
        "expected_behavior": {"jurisdiction": "PA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["42 Pa. C.S. § 6337"], "epistemic_classification": ["LAW", "HIERARCHY"]},
        "source": "Pennsylvania Consolidated Statutes 42 Pa. C.S. § 6337", "jurisdiction": "PA", "legal_date": "2024-07-10", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Determine supremacy of Texas Family Code dismissal deadline over trial court docket backlog.",
        "input": {"state": "TX", "county": "Dallas", "event_date": "2024-08-01", "facts": "One-year dismissal deadline reached; trial court purported to extend deadline indefinitely due to heavy caseload."},
        "reasoning_task": "03_authority_ranking",
        "expected_behavior": {"jurisdiction": "TX", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Tex. Fam. Code § 263.401"], "epistemic_classification": ["LAW", "HIERARCHY"]},
        "source": "Texas Family Code § 263.401", "jurisdiction": "TX", "legal_date": "2024-08-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
]

# 04_citation_verification (10 examples)
SEEDS_04_CITATION_VERIFICATION = [
    {
        "instruction": "Verify exact statutory citation for warrantless emergency removal in Washington.",
        "input": {"state": "WA", "county": "King", "event_date": "2024-01-20", "facts": "Law enforcement officer took custody of minor without judicial warrant on basis of alleged imminent harm."},
        "reasoning_task": "04_citation_verification",
        "expected_behavior": {"jurisdiction": "WA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["RCW 13.34.055"], "epistemic_classification": ["CITATION", "VERIFICATION"]},
        "source": "Washington State Legislature RCW 13.34.055", "jurisdiction": "WA", "legal_date": "2024-01-20", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Verify controlling pinpoint citation for temporary custody hearing notice in Illinois.",
        "input": {"state": "IL", "county": "Cook", "event_date": "2024-02-12", "facts": "Parent received no formal summons or notice prior to shelter custody hearing."},
        "reasoning_task": "04_citation_verification",
        "expected_behavior": {"jurisdiction": "IL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["705 ILCS 405/2-9"], "epistemic_classification": ["CITATION", "VERIFICATION"]},
        "source": "Illinois General Assembly 705 ILCS 405/2-9", "jurisdiction": "IL", "legal_date": "2024-02-12", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Verify Florida statutory citation governing emergency removal criteria.",
        "input": {"state": "FL", "county": "Broward", "event_date": "2024-03-05", "facts": "Investigator took child into custody claiming probable cause of child abuse."},
        "reasoning_task": "04_citation_verification",
        "expected_behavior": {"jurisdiction": "FL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Fla. Stat. § 39.401"], "epistemic_classification": ["CITATION", "VERIFICATION"]},
        "source": "Florida Statutes § 39.401", "jurisdiction": "FL", "legal_date": "2024-03-05", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Verify pinpoint statutory reference for reasonable efforts judicial determination in Ohio.",
        "input": {"state": "OH", "county": "Cuyahoga", "event_date": "2024-04-01", "facts": "Juvenile court magistrate entered shelter order without determining whether agency made reasonable efforts."},
        "reasoning_task": "04_citation_verification",
        "expected_behavior": {"jurisdiction": "OH", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["ORC § 2151.419"], "epistemic_classification": ["CITATION", "VERIFICATION"]},
        "source": "Ohio Revised Code ORC § 2151.419", "jurisdiction": "OH", "legal_date": "2024-04-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Verify California Welfare and Institutions Code citation for mandatory appointment of parent counsel.",
        "input": {"state": "CA", "county": "Santa Clara", "event_date": "2024-04-25", "facts": "Indigent mother appeared unrepresented at initial detention hearing; court failed to appoint public defender."},
        "reasoning_task": "04_citation_verification",
        "expected_behavior": {"jurisdiction": "CA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Cal. Welf. & Inst. Code § 317"], "epistemic_classification": ["CITATION", "VERIFICATION"]},
        "source": "California Welfare & Institutions Code § 317", "jurisdiction": "CA", "legal_date": "2024-04-25", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Verify Texas Family Code citation for emergency warrantless possession of a child.",
        "input": {"state": "TX", "county": "Bexar", "event_date": "2024-05-10", "facts": "Caseworker removed child without obtaining prior court order under Chapter 262."},
        "reasoning_task": "04_citation_verification",
        "expected_behavior": {"jurisdiction": "TX", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Tex. Fam. Code § 262.104"], "epistemic_classification": ["CITATION", "VERIFICATION"]},
        "source": "Texas Family Code § 262.104", "jurisdiction": "TX", "legal_date": "2024-05-10", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Verify Pennsylvania citation for indigent parent's right to legal counsel at informal hearing.",
        "input": {"state": "PA", "county": "Lancaster", "event_date": "2024-06-01", "facts": "Parent requested appointed counsel at 72-hour informal hearing; court proceeded with detention without counsel."},
        "reasoning_task": "04_citation_verification",
        "expected_behavior": {"jurisdiction": "PA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["42 Pa. C.S. § 6337"], "epistemic_classification": ["CITATION", "VERIFICATION"]},
        "source": "Pennsylvania Consolidated Statutes 42 Pa. C.S. § 6337", "jurisdiction": "PA", "legal_date": "2024-06-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Verify Georgia statutory section guaranteeing appointed counsel for indigent parents in dependency.",
        "input": {"state": "GA", "county": "DeKalb", "event_date": "2024-06-20", "facts": "Indigent father requested attorney representation at preliminary protective hearing."},
        "reasoning_task": "04_citation_verification",
        "expected_behavior": {"jurisdiction": "GA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["O.C.G.A. § 15-11-103"], "epistemic_classification": ["CITATION", "VERIFICATION"]},
        "source": "Official Code of Georgia Annotated O.C.G.A. § 15-11-103", "jurisdiction": "GA", "legal_date": "2024-06-20", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Verify North Carolina General Statutes citation for parent right to counsel in child welfare.",
        "input": {"state": "NC", "county": "Mecklenburg", "event_date": "2024-07-15", "facts": "Respondent parent appeared without lawyer at nonsecure custody hearing."},
        "reasoning_task": "04_citation_verification",
        "expected_behavior": {"jurisdiction": "NC", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["N.C.G.S. § 7B-602"], "epistemic_classification": ["CITATION", "VERIFICATION"]},
        "source": "North Carolina General Statutes N.C.G.S. § 7B-602", "jurisdiction": "NC", "legal_date": "2024-07-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Verify Michigan compiled laws citation for right to attorney at every stage of child protection.",
        "input": {"state": "MI", "county": "Oakland", "event_date": "2024-08-10", "facts": "Referee conducted preliminary hearing without advising parents of right to court-appointed lawyer."},
        "reasoning_task": "04_citation_verification",
        "expected_behavior": {"jurisdiction": "MI", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["MCL 712A.17c"], "epistemic_classification": ["CITATION", "VERIFICATION"]},
        "source": "Michigan Compiled Laws MCL 712A.17c", "jurisdiction": "MI", "legal_date": "2024-08-10", "authority_level": "T4", "dataset_version": "0.3.0"
    },
]

# 07_fact_application (10 examples)
SEEDS_07_FACT_APPLICATION = [
    {
        "instruction": "Apply statutory emergency removal standard to fact pattern involving clutter vs imminent danger.",
        "input": {"state": "WA", "county": "Snohomish", "event_date": "2024-02-15", "facts": "Caseworker observed unwashed dishes and cluttered floor; children were uninjured, nourished, and happy. Caseworker removed children."},
        "reasoning_task": "07_fact_application",
        "expected_behavior": {"jurisdiction": "WA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["RCW 13.34.050"], "epistemic_classification": ["FACTS", "APPLICATION"]},
        "source": "Washington State Legislature RCW 13.34.050", "jurisdiction": "WA", "legal_date": "2024-02-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Apply urgent necessity standard to temporary housing loss without physical hazard.",
        "input": {"state": "IL", "county": "Cook", "event_date": "2024-03-01", "facts": "Family faced eviction notice; mother had identified temporary shelter with maternal aunt; agency petitioned for out-of-home foster care."},
        "reasoning_task": "07_fact_application",
        "expected_behavior": {"jurisdiction": "IL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["705 ILCS 405/2-10"], "epistemic_classification": ["FACTS", "APPLICATION"]},
        "source": "Illinois General Assembly 705 ILCS 405/2-10", "jurisdiction": "IL", "legal_date": "2024-03-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Apply Ohio reasonable grounds standard where able relative is present at apprehension.",
        "input": {"state": "OH", "county": "Cuyahoga", "event_date": "2024-03-20", "facts": "Single mother taken to hospital for migraine; grandmother was in home caring for children; police transported children to county shelter."},
        "reasoning_task": "07_fact_application",
        "expected_behavior": {"jurisdiction": "OH", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["ORC § 2151.31"], "epistemic_classification": ["FACTS", "APPLICATION"]},
        "source": "Ohio Revised Code ORC § 2151.31", "jurisdiction": "OH", "legal_date": "2024-03-20", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Apply California substantial risk standard where alleged incident was isolated and resolved.",
        "input": {"state": "CA", "county": "San Diego", "event_date": "2024-04-10", "facts": "Parents had verbal dispute two months prior while child was absent; no physical domestic violence occurred; agency filed Section 300 petition."},
        "reasoning_task": "07_fact_application",
        "expected_behavior": {"jurisdiction": "CA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Cal. Welf. & Inst. Code § 300"], "epistemic_classification": ["FACTS", "APPLICATION"]},
        "source": "California Welfare & Institutions Code § 300", "jurisdiction": "CA", "legal_date": "2024-04-10", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Apply Florida emergency removal criteria to unverified telephone referral.",
        "input": {"state": "FL", "county": "Hillsborough", "event_date": "2024-05-01", "facts": "Anonymous caller claimed mother was shouting; investigator visited, found child sleeping peacefully with ample food and utilities functioning."},
        "reasoning_task": "07_fact_application",
        "expected_behavior": {"jurisdiction": "FL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Fla. Stat. § 39.401"], "epistemic_classification": ["FACTS", "APPLICATION"]},
        "source": "Florida Statutes § 39.401", "jurisdiction": "FL", "legal_date": "2024-05-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Apply Texas immediate danger standard where utility cutoff can be remedied with community funds.",
        "input": {"state": "TX", "county": "Travis", "event_date": "2024-05-22", "facts": "Electric bill was overdue for 3 days during mild weather; church offered payment guarantee; caseworker removed child without court order."},
        "reasoning_task": "07_fact_application",
        "expected_behavior": {"jurisdiction": "TX", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Tex. Fam. Code § 262.104"], "epistemic_classification": ["FACTS", "APPLICATION"]},
        "source": "Texas Family Code § 262.104", "jurisdiction": "TX", "legal_date": "2024-05-22", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Apply Pennsylvania clear necessity test where parent has valid medical prescription.",
        "input": {"state": "PA", "county": "Bucks", "event_date": "2024-06-15", "facts": "Mother tested positive for prescribed ADHD medication; caseworker alleged illicit substance abuse without verifying physician records."},
        "reasoning_task": "07_fact_application",
        "expected_behavior": {"jurisdiction": "PA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["42 Pa. C.S. § 6324"], "epistemic_classification": ["FACTS", "APPLICATION"]},
        "source": "Pennsylvania Consolidated Statutes 42 Pa. C.S. § 6324", "jurisdiction": "PA", "legal_date": "2024-06-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Apply Georgia protective custody statute where responsible adult relative is available.",
        "input": {"state": "GA", "county": "Cobb", "event_date": "2024-07-08", "facts": "Father was arrested on unpaid traffic citations; adult aunt residing in same apartment complex was present to care for child."},
        "reasoning_task": "07_fact_application",
        "expected_behavior": {"jurisdiction": "GA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["O.C.G.A. § 15-11-133"], "epistemic_classification": ["FACTS", "APPLICATION"]},
        "source": "Official Code of Georgia Annotated O.C.G.A. § 15-11-133", "jurisdiction": "GA", "legal_date": "2024-07-08", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Apply North Carolina temporary custody statute to school attendance referral.",
        "input": {"state": "NC", "county": "Durham", "event_date": "2024-08-05", "facts": "Child had 10 unexcused absences due to lack of school bus route; caseworker removed child alleging educational neglect."},
        "reasoning_task": "07_fact_application",
        "expected_behavior": {"jurisdiction": "NC", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["N.C.G.S. § 7B-500"], "epistemic_classification": ["FACTS", "APPLICATION"]},
        "source": "North Carolina General Statutes N.C.G.S. § 7B-500", "jurisdiction": "NC", "legal_date": "2024-08-05", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Apply Michigan emergency removal standard where family has arranged safe alternative heating.",
        "input": {"state": "MI", "county": "Macomb", "event_date": "2024-09-12", "facts": "Home furnace failed; parent immediately relocated children to grandmother's warm residence while repair technician was scheduled."},
        "reasoning_task": "07_fact_application",
        "expected_behavior": {"jurisdiction": "MI", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["MCL 712A.13a"], "epistemic_classification": ["FACTS", "APPLICATION"]},
        "source": "Michigan Compiled Laws MCL 712A.13a", "jurisdiction": "MI", "legal_date": "2024-09-12", "authority_level": "T4", "dataset_version": "0.3.0"
    },
]

# 08_counterargument (10 examples)
SEEDS_08_COUNTERARGUMENT = [
    {
        "instruction": "Formulate defense counterargument against agency claim of imminent physical danger.",
        "input": {"state": "WA", "county": "King", "event_date": "2024-01-18", "facts": "Agency argues children must remain in foster care due to dirty home. Defense proves no physical injury, healthy medical records, and willing kinship placement."},
        "reasoning_task": "08_counterargument",
        "expected_behavior": {"jurisdiction": "WA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["RCW 13.34.050"], "epistemic_classification": ["COUNTERARGUMENT", "ANALYSIS"]},
        "source": "Washington State Legislature RCW 13.34.050", "jurisdiction": "WA", "legal_date": "2024-01-18", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Rebut state claim of urgent necessity based on economic housing hardship in Illinois.",
        "input": {"state": "IL", "county": "Cook", "event_date": "2024-02-14", "facts": "State argues homelessness per se constitutes neglect. Defense counterargues poverty is not a statutory ground and agency failed to offer housing assistance."},
        "reasoning_task": "08_counterargument",
        "expected_behavior": {"jurisdiction": "IL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["705 ILCS 405/2-10"], "epistemic_classification": ["COUNTERARGUMENT", "ANALYSIS"]},
        "source": "Illinois General Assembly 705 ILCS 405/2-10", "jurisdiction": "IL", "legal_date": "2024-02-14", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Challenge agency assertion that reasonable efforts were bypassed due to emergency in Ohio.",
        "input": {"state": "OH", "county": "Cuyahoga", "event_date": "2024-03-02", "facts": "Agency claims sudden emergency excused remedial services; defense demonstrates agency had two weeks notice of family utility issue."},
        "reasoning_task": "08_counterargument",
        "expected_behavior": {"jurisdiction": "OH", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["ORC § 2151.419"], "epistemic_classification": ["COUNTERARGUMENT", "ANALYSIS"]},
        "source": "Ohio Revised Code ORC § 2151.419", "jurisdiction": "OH", "legal_date": "2024-03-02", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Counter agency reliance on uncorroborated hearsay at California jurisdictional hearing.",
        "input": {"state": "CA", "county": "Los Angeles", "event_date": "2024-03-25", "facts": "County relies exclusively on anonymous hotline tip; defense objects that jurisdictional finding under WIC § 355 requires legally admissible proof."},
        "reasoning_task": "08_counterargument",
        "expected_behavior": {"jurisdiction": "CA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Cal. Welf. & Inst. Code § 355"], "epistemic_classification": ["COUNTERARGUMENT", "ANALYSIS"]},
        "source": "California Welfare & Institutions Code § 355", "jurisdiction": "CA", "legal_date": "2024-03-25", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Formulate respondent parent counterargument against continued foster placement at Texas adversary hearing.",
        "input": {"state": "TX", "county": "Bexar", "event_date": "2024-04-12", "facts": "State seeks continued temporary managing conservatorship; defense proves mother completed parenting classes and maternal grandmother home is fully approved."},
        "reasoning_task": "08_counterargument",
        "expected_behavior": {"jurisdiction": "TX", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Tex. Fam. Code § 262.201"], "epistemic_classification": ["COUNTERARGUMENT", "ANALYSIS"]},
        "source": "Texas Family Code § 262.201", "jurisdiction": "TX", "legal_date": "2024-04-12", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Rebut Florida Department of Children and Families request for ongoing shelter detention.",
        "input": {"state": "FL", "county": "Miami-Dade", "event_date": "2024-05-05", "facts": "DCF argues shelter detention necessary; defense shows safety plan with paternal aunt resolves all alleged risks in home."},
        "reasoning_task": "08_counterargument",
        "expected_behavior": {"jurisdiction": "FL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Fla. Stat. § 39.402"], "epistemic_classification": ["COUNTERARGUMENT", "ANALYSIS"]},
        "source": "Florida Statutes § 39.402", "jurisdiction": "FL", "legal_date": "2024-05-05", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Formulate counterargument against dependency finding where able kinship caregiver is ready in Pennsylvania.",
        "input": {"state": "PA", "county": "Philadelphia", "event_date": "2024-05-28", "facts": "CYS claims child is without proper parental care; defense demonstrates grandmother has cared for child with parent's consent and filed kinship petition."},
        "reasoning_task": "08_counterargument",
        "expected_behavior": {"jurisdiction": "PA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["42 Pa. C.S. § 6332"], "epistemic_classification": ["COUNTERARGUMENT", "ANALYSIS"]},
        "source": "Pennsylvania Consolidated Statutes 42 Pa. C.S. § 6332", "jurisdiction": "PA", "legal_date": "2024-05-28", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Rebut agency emergency custody request where parent voluntarily entered treatment in Georgia.",
        "input": {"state": "GA", "county": "Gwinnett", "event_date": "2024-06-14", "facts": "DFCS seeks protective custody after mother enrolled in detox; defense shows children were left with licensed relative guardian under power of attorney."},
        "reasoning_task": "08_counterargument",
        "expected_behavior": {"jurisdiction": "GA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["O.C.G.A. § 15-11-145"], "epistemic_classification": ["COUNTERARGUMENT", "ANALYSIS"]},
        "source": "Official Code of Georgia Annotated O.C.G.A. § 15-11-145", "jurisdiction": "GA", "legal_date": "2024-06-14", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Counter North Carolina DSS motion for nonsecure custody based on missed medical checkup.",
        "input": {"state": "NC", "county": "Forsyth", "event_date": "2024-07-01", "facts": "DSS claims missed dental appointment constitutes medical neglect; defense proves appointment was rescheduled due to parent work shift."},
        "reasoning_task": "08_counterargument",
        "expected_behavior": {"jurisdiction": "NC", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["N.C.G.S. § 7B-506"], "epistemic_classification": ["COUNTERARGUMENT", "ANALYSIS"]},
        "source": "North Carolina General Statutes N.C.G.S. § 7B-506", "jurisdiction": "NC", "legal_date": "2024-07-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Rebut Michigan foster care petition where relative placement preference was ignored.",
        "input": {"state": "MI", "county": "Genesee", "event_date": "2024-08-01", "facts": "Agency placed child with stranger foster family; defense shows two fit adult maternal aunts immediately requested kinship placement."},
        "reasoning_task": "08_counterargument",
        "expected_behavior": {"jurisdiction": "MI", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["MCL 712A.13a"], "epistemic_classification": ["COUNTERARGUMENT", "ANALYSIS"]},
        "source": "Michigan Compiled Laws MCL 712A.13a", "jurisdiction": "MI", "legal_date": "2024-08-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
]

# 09_uncertainty (10 examples)
SEEDS_09_UNCERTAINTY = [
    {
        "instruction": "Identify critical missing facts regarding exact hour of child removal under Washington law.",
        "input": {"state": "WA", "county": "King", "event_date": "2024-01-10", "facts": "Notice states child was removed on January 10 but omits timestamp. Defense cannot verify whether 72-hour shelter clock has expired."},
        "reasoning_task": "09_uncertainty",
        "expected_behavior": {"jurisdiction": "WA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["RCW 13.34.065"], "epistemic_classification": ["UNCERTAINTY", "GAPS"]},
        "source": "Washington State Legislature RCW 13.34.065", "jurisdiction": "WA", "legal_date": "2024-01-10", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Identify procedural uncertainty regarding proof of service in Illinois dependency proceeding.",
        "input": {"state": "IL", "county": "Cook", "event_date": "2024-02-05", "facts": "Court docket contains petition but summons return is missing or unexecuted. Record is silent on personal service."},
        "reasoning_task": "09_uncertainty",
        "expected_behavior": {"jurisdiction": "IL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["705 ILCS 405/2-9"], "epistemic_classification": ["UNCERTAINTY", "GAPS"]},
        "source": "Illinois General Assembly 705 ILCS 405/2-9", "jurisdiction": "IL", "legal_date": "2024-02-05", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Identify threshold uncertainty regarding Indian Child Welfare Act tribal eligibility.",
        "input": {"state": "OH", "county": "Cuyahoga", "event_date": "2024-02-28", "facts": "Intake report states grandmother believes family has Cherokee heritage; court record lacks formal inquiry or tribal notice."},
        "reasoning_task": "09_uncertainty",
        "expected_behavior": {"jurisdiction": "OH", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["ORC § 2151.314"], "epistemic_classification": ["UNCERTAINTY", "GAPS"]},
        "source": "Ohio Revised Code ORC § 2151.314", "jurisdiction": "OH", "legal_date": "2024-02-28", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Highlight missing factual documentation regarding relative home assessment in California.",
        "input": {"state": "CA", "county": "Los Angeles", "event_date": "2024-03-15", "facts": "Social worker noted aunt expressed interest in placement, but file contains no background clearance or inspection report."},
        "reasoning_task": "09_uncertainty",
        "expected_behavior": {"jurisdiction": "CA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Cal. Welf. & Inst. Code § 315"], "epistemic_classification": ["UNCERTAINTY", "GAPS"]},
        "source": "California Welfare & Institutions Code § 315", "jurisdiction": "CA", "legal_date": "2024-03-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Spot evidentiary gap where Texas emergency removal affidavit is absent from court file.",
        "input": {"state": "TX", "county": "Harris", "event_date": "2024-04-02", "facts": "Temporary custody order issued ex parte but supporting sworn affidavit required by Chapter 262 was never served or attached."},
        "reasoning_task": "09_uncertainty",
        "expected_behavior": {"jurisdiction": "TX", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Tex. Fam. Code § 262.101"], "epistemic_classification": ["UNCERTAINTY", "GAPS"]},
        "source": "Texas Family Code § 262.101", "jurisdiction": "TX", "legal_date": "2024-04-02", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Identify unverified claims in Florida emergency shelter care petition.",
        "input": {"state": "FL", "county": "Miami-Dade", "event_date": "2024-04-20", "facts": "Shelter petition cites confidential informant but provides no dates, specific acts, or personal observations by investigator."},
        "reasoning_task": "09_uncertainty",
        "expected_behavior": {"jurisdiction": "FL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Fla. Stat. § 39.402"], "epistemic_classification": ["UNCERTAINTY", "GAPS"]},
        "source": "Florida Statutes § 39.402", "jurisdiction": "FL", "legal_date": "2024-04-20", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Recognize lack of laboratory verification in Pennsylvania substance allegations.",
        "input": {"state": "PA", "county": "Montgomery", "event_date": "2024-05-12", "facts": "Caseworker noted parent appeared fatigued and presumed drug intoxication; no urinalysis or toxicology report was conducted."},
        "reasoning_task": "09_uncertainty",
        "expected_behavior": {"jurisdiction": "PA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["42 Pa. C.S. § 6332"], "epistemic_classification": ["UNCERTAINTY", "GAPS"]},
        "source": "Pennsylvania Consolidated Statutes 42 Pa. C.S. § 6332", "jurisdiction": "PA", "legal_date": "2024-05-12", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Identify factual uncertainty regarding diligent search for paternal relatives in Georgia.",
        "input": {"state": "GA", "county": "Chatham", "event_date": "2024-06-05", "facts": "Agency file notes father is unknown; mother provided father's full name and city of residence at intake, but no inquiry letter was mailed."},
        "reasoning_task": "09_uncertainty",
        "expected_behavior": {"jurisdiction": "GA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["O.C.G.A. § 15-11-145"], "epistemic_classification": ["UNCERTAINTY", "GAPS"]},
        "source": "Official Code of Georgia Annotated O.C.G.A. § 15-11-145", "jurisdiction": "GA", "legal_date": "2024-06-05", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Highlight vague allegations in North Carolina nonsecure custody petition.",
        "input": {"state": "NC", "county": "Guilford", "event_date": "2024-06-25", "facts": "Petition alleges general injurious environment without describing any specific incident, injury, or impairment to the minor."},
        "reasoning_task": "09_uncertainty",
        "expected_behavior": {"jurisdiction": "NC", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["N.C.G.S. § 7B-500"], "epistemic_classification": ["UNCERTAINTY", "GAPS"]},
        "source": "North Carolina General Statutes N.C.G.S. § 7B-500", "jurisdiction": "NC", "legal_date": "2024-06-25", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Flag absence of written reasonable efforts finding in Michigan preliminary hearing order.",
        "input": {"state": "MI", "county": "Washtenaw", "event_date": "2024-07-18", "facts": "Preliminary hearing concluded with pre-printed checkbox order lacking explicit factual findings on reasonable efforts."},
        "reasoning_task": "09_uncertainty",
        "expected_behavior": {"jurisdiction": "MI", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["MCL 712A.13a"], "epistemic_classification": ["UNCERTAINTY", "GAPS"]},
        "source": "Michigan Compiled Laws MCL 712A.13a", "jurisdiction": "MI", "legal_date": "2024-07-18", "authority_level": "T4", "dataset_version": "0.3.0"
    },
]

# 14_human_rights (10 examples)
SEEDS_14_HUMAN_RIGHTS = [
    {
        "instruction": "Analyze international human rights standards protecting family integrity against arbitrary state separation.",
        "input": {"state": "US", "event_date": "2024-01-15", "facts": "State welfare agency removed child based solely on parent's low income and substandard housing without providing social assistance."},
        "reasoning_task": "14_human_rights",
        "expected_behavior": {"jurisdiction": "US", "temporal_validation": True, "authority_tier": 1, "citation_required": True, "controlling_citations": ["42 U.S.C. § 671"], "epistemic_classification": ["HUMAN_RIGHTS", "PRINCIPLES"]},
        "source": "United States Code 42 U.S.C. § 671", "jurisdiction": "US", "legal_date": "2024-01-15", "authority_level": "T1", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Examine human rights protections for indigenous child cultural heritage and identity.",
        "input": {"state": "US", "event_date": "2024-02-10", "facts": "State agency placed Native American child in non-indigenous foster home without notifying tribe or evaluating tribal kinship options."},
        "reasoning_task": "14_human_rights",
        "expected_behavior": {"jurisdiction": "US", "temporal_validation": True, "authority_tier": 1, "citation_required": True, "controlling_citations": ["25 U.S.C. § 1912"], "epistemic_classification": ["HUMAN_RIGHTS", "INDIGENOUS"]},
        "source": "United States Code 25 U.S.C. § 1912", "jurisdiction": "US", "legal_date": "2024-02-10", "authority_level": "T1", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate child's right to placement in the least restrictive family environment in Washington.",
        "input": {"state": "WA", "county": "King", "event_date": "2024-03-01", "facts": "Agency placed 4-year-old child in group facility rather than with willing adult maternal grandmother."},
        "reasoning_task": "14_human_rights",
        "expected_behavior": {"jurisdiction": "WA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["RCW 13.34.060"], "epistemic_classification": ["HUMAN_RIGHTS", "CHILD_RIGHTS"]},
        "source": "Washington State Legislature RCW 13.34.060", "jurisdiction": "WA", "legal_date": "2024-03-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess human right to fair hearing and effective legal assistance in Illinois child custody proceeding.",
        "input": {"state": "IL", "county": "Cook", "event_date": "2024-03-22", "facts": "Indigent non-English speaking mother had temporary custody revoked without certified interpreter or appointed counsel."},
        "reasoning_task": "14_human_rights",
        "expected_behavior": {"jurisdiction": "IL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["705 ILCS 405/2-10"], "epistemic_classification": ["HUMAN_RIGHTS", "DUE_PROCESS"]},
        "source": "Illinois General Assembly 705 ILCS 405/2-10", "jurisdiction": "IL", "legal_date": "2024-03-22", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Examine human rights principles regarding state non-interference in family privacy in California.",
        "input": {"state": "CA", "county": "San Francisco", "event_date": "2024-04-12", "facts": "Investigator demanded unrestricted access to family home without warrant or evidence of child maltreatment."},
        "reasoning_task": "14_human_rights",
        "expected_behavior": {"jurisdiction": "CA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Cal. Welf. & Inst. Code § 300"], "epistemic_classification": ["HUMAN_RIGHTS", "PRIVACY"]},
        "source": "California Welfare & Institutions Code § 300", "jurisdiction": "CA", "legal_date": "2024-04-12", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze right to prompt judicial remedy following state seizure of a child in New York.",
        "input": {"state": "NY", "county": "Bronx", "event_date": "2024-05-02", "facts": "Child removed without court order; parent filed application for immediate return under Section 1028; court delayed hearing for two weeks."},
        "reasoning_task": "14_human_rights",
        "expected_behavior": {"jurisdiction": "NY", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["N.Y. Fam. Ct. Act § 1028"], "epistemic_classification": ["HUMAN_RIGHTS", "REMEDY"]},
        "source": "New York Family Court Act § 1028", "jurisdiction": "NY", "legal_date": "2024-05-02", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Review human rights standards protecting children from institutionalization in Pennsylvania.",
        "input": {"state": "PA", "county": "Philadelphia", "event_date": "2024-05-20", "facts": "CYS placed infant in congregate care facility instead of exploring fit kinship foster care."},
        "reasoning_task": "14_human_rights",
        "expected_behavior": {"jurisdiction": "PA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["42 Pa. C.S. § 6351"], "epistemic_classification": ["HUMAN_RIGHTS", "KINSHIP"]},
        "source": "Pennsylvania Consolidated Statutes 42 Pa. C.S. § 6351", "jurisdiction": "PA", "legal_date": "2024-05-20", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze universal principle of preserving child's familial identity under Ohio law.",
        "input": {"state": "OH", "county": "Cuyahoga", "event_date": "2024-06-10", "facts": "Agency failed to maintain family connections or explore kinship placement prior to filing for permanent custody."},
        "reasoning_task": "14_human_rights",
        "expected_behavior": {"jurisdiction": "OH", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["ORC § 2151.419"], "epistemic_classification": ["HUMAN_RIGHTS", "FAMILY_UNITY"]},
        "source": "Ohio Revised Code ORC § 2151.419", "jurisdiction": "OH", "legal_date": "2024-06-10", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Examine human rights implications of prolonged adversary hearing delays in Texas.",
        "input": {"state": "TX", "county": "Dallas", "event_date": "2024-07-01", "facts": "Child remained separated from parents for 45 days before trial court convened an initial evidentiary hearing."},
        "reasoning_task": "14_human_rights",
        "expected_behavior": {"jurisdiction": "TX", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Tex. Fam. Code § 262.201"], "epistemic_classification": ["HUMAN_RIGHTS", "SPEEDY_TRIAL"]},
        "source": "Texas Family Code § 262.201", "jurisdiction": "TX", "legal_date": "2024-07-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess human rights guarantees of regular parent-child contact during state custody in Florida.",
        "input": {"state": "FL", "county": "Duval", "event_date": "2024-07-25", "facts": "Agency restricted parent visitation to once per month without demonstrating any physical risk to the child."},
        "reasoning_task": "14_human_rights",
        "expected_behavior": {"jurisdiction": "FL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Fla. Stat. § 39.402"], "epistemic_classification": ["HUMAN_RIGHTS", "VISITATION"]},
        "source": "Florida Statutes § 39.402", "jurisdiction": "FL", "legal_date": "2024-07-25", "authority_level": "T4", "dataset_version": "0.3.0"
    },
]

# 15_drug_policy (10 examples)
SEEDS_15_DRUG_POLICY = [
    {
        "instruction": "Analyze statutory nexus requirement between parental substance use and imminent danger in Washington.",
        "input": {"state": "WA", "county": "King", "event_date": "2024-01-25", "facts": "Mother tested positive for cannabis; child was well-cared for, healthy, and developmentally on track. Caseworker removed child."},
        "reasoning_task": "15_drug_policy",
        "expected_behavior": {"jurisdiction": "WA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["RCW 13.34.050"], "epistemic_classification": ["DRUG_POLICY", "NEXUS"]},
        "source": "Washington State Legislature RCW 13.34.050", "jurisdiction": "WA", "legal_date": "2024-01-25", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate whether lawful medical cannabis use can constitute statutory neglect under Illinois law.",
        "input": {"state": "IL", "county": "Cook", "event_date": "2024-02-18", "facts": "Parent holds valid state medical cannabis card for chronic pain; caseworker filed petition alleging neglect based solely on positive test."},
        "reasoning_task": "15_drug_policy",
        "expected_behavior": {"jurisdiction": "IL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["705 ILCS 405/2-3"], "epistemic_classification": ["DRUG_POLICY", "MEDICAL"]},
        "source": "Illinois General Assembly 705 ILCS 405/2-3", "jurisdiction": "IL", "legal_date": "2024-02-18", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess Ohio reasonable grounds standard where sober caregiver is present during parental relapse.",
        "input": {"state": "OH", "county": "Cuyahoga", "event_date": "2024-03-08", "facts": "Father had substance relapse but had entrusted child to sober maternal grandmother who was providing full-time care."},
        "reasoning_task": "15_drug_policy",
        "expected_behavior": {"jurisdiction": "OH", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["ORC § 2151.31"], "epistemic_classification": ["DRUG_POLICY", "SAFETY_PLAN"]},
        "source": "Ohio Revised Code ORC § 2151.31", "jurisdiction": "OH", "legal_date": "2024-03-08", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Determine whether enrollment in voluntary substance treatment mitigates risk in California.",
        "input": {"state": "CA", "county": "Alameda", "event_date": "2024-03-29", "facts": "Mother voluntarily admitted herself to outpatient substance recovery program; agency filed petition alleging current substantial risk."},
        "reasoning_task": "15_drug_policy",
        "expected_behavior": {"jurisdiction": "CA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Cal. Welf. & Inst. Code § 300"], "epistemic_classification": ["DRUG_POLICY", "RECOVERY"]},
        "source": "California Welfare & Institutions Code § 300", "jurisdiction": "CA", "legal_date": "2024-03-29", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze refusal of non-court-ordered drug screen under Texas emergency removal framework.",
        "input": {"state": "TX", "county": "Harris", "event_date": "2024-04-15", "facts": "Caseworker demanded parent submit to instant swab without court order; parent refused; caseworker removed child for non-compliance."},
        "reasoning_task": "15_drug_policy",
        "expected_behavior": {"jurisdiction": "TX", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Tex. Fam. Code § 262.104"], "epistemic_classification": ["DRUG_POLICY", "FOURTH_AMENDMENT"]},
        "source": "Texas Family Code § 262.104", "jurisdiction": "TX", "legal_date": "2024-04-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate Florida newborn toxicology screening without evidence of parental impairment.",
        "input": {"state": "FL", "county": "Orange", "event_date": "2024-05-10", "facts": "Newborn tested positive for prescribed buprenorphine under physician care; hospital worker called child protection hotline."},
        "reasoning_task": "15_drug_policy",
        "expected_behavior": {"jurisdiction": "FL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Fla. Stat. § 39.401"], "epistemic_classification": ["DRUG_POLICY", "PRESCRIPTION"]},
        "source": "Florida Statutes § 39.401", "jurisdiction": "FL", "legal_date": "2024-05-10", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess clear necessity standard for drug exposure in Pennsylvania child dependency.",
        "input": {"state": "PA", "county": "Allegheny", "event_date": "2024-05-30", "facts": "Parent admitted to past substance history; current home is clean, food present, and parent actively attends supportive counseling."},
        "reasoning_task": "15_drug_policy",
        "expected_behavior": {"jurisdiction": "PA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["42 Pa. C.S. § 6324"], "epistemic_classification": ["DRUG_POLICY", "NECESSITY"]},
        "source": "Pennsylvania Consolidated Statutes 42 Pa. C.S. § 6324", "jurisdiction": "PA", "legal_date": "2024-05-30", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate Georgia safety plan utilization in substance allegations.",
        "input": {"state": "GA", "county": "Fulton", "event_date": "2024-06-18", "facts": "Agency investigated substance allegation; parent agreed to daily supervision by fit maternal aunt; caseworker nonetheless removed child."},
        "reasoning_task": "15_drug_policy",
        "expected_behavior": {"jurisdiction": "GA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["O.C.G.A. § 15-11-133"], "epistemic_classification": ["DRUG_POLICY", "SAFETY_PLAN"]},
        "source": "Official Code of Georgia Annotated O.C.G.A. § 15-11-133", "jurisdiction": "GA", "legal_date": "2024-06-18", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze North Carolina imminent harm requirement where substance use occurs outside child presence.",
        "input": {"state": "NC", "county": "Wake", "event_date": "2024-07-08", "facts": "Parent consumed alcohol on weekend while child was visiting grandparents; caseworker initiated temporary custody proceeding."},
        "reasoning_task": "15_drug_policy",
        "expected_behavior": {"jurisdiction": "NC", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["N.C.G.S. § 7B-500"], "epistemic_classification": ["DRUG_POLICY", "HARM_STANDARD"]},
        "source": "North Carolina General Statutes N.C.G.S. § 7B-500", "jurisdiction": "NC", "legal_date": "2024-07-08", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Determine whether Michigan reasonable efforts mandate requires outpatient addiction referral prior to removal.",
        "input": {"state": "MI", "county": "Wayne", "event_date": "2024-08-05", "facts": "Agency removed child upon positive marijuana screen without providing referrals to community outpatient services or relative safety plan."},
        "reasoning_task": "15_drug_policy",
        "expected_behavior": {"jurisdiction": "MI", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["MCL 712A.13a"], "epistemic_classification": ["DRUG_POLICY", "REASONABLE_EFFORTS"]},
        "source": "Michigan Compiled Laws MCL 712A.13a", "jurisdiction": "MI", "legal_date": "2024-08-05", "authority_level": "T4", "dataset_version": "0.3.0"
    },
]

# 16_mental_health (10 examples)
SEEDS_16_MENTAL_HEALTH = [
    {
        "instruction": "Apply Americans with Disabilities Act reasonable accommodation rules to Washington CPS case plan.",
        "input": {"state": "WA", "county": "King", "event_date": "2024-01-22", "facts": "Mother with major depressive disorder requested virtual or in-home visits due to anxiety; agency terminated services for missed office appointments."},
        "reasoning_task": "16_mental_health",
        "expected_behavior": {"jurisdiction": "WA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["RCW 13.34.136"], "epistemic_classification": ["MENTAL_HEALTH", "ADA"]},
        "source": "Washington State Legislature RCW 13.34.136", "jurisdiction": "WA", "legal_date": "2024-01-22", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze whether mental health diagnosis alone can sustain neglect finding under Illinois law.",
        "input": {"state": "IL", "county": "Cook", "event_date": "2024-02-15", "facts": "Father diagnosed with bipolar disorder is actively medicated and stable; caseworker filed petition citing diagnosis without alleging parental failure."},
        "reasoning_task": "16_mental_health",
        "expected_behavior": {"jurisdiction": "IL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["705 ILCS 405/2-3"], "epistemic_classification": ["MENTAL_HEALTH", "NEXUS"]},
        "source": "Illinois General Assembly 705 ILCS 405/2-3", "jurisdiction": "IL", "legal_date": "2024-02-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate Ohio reasonable efforts duty to provide tailored mental health accommodations.",
        "input": {"state": "OH", "county": "Cuyahoga", "event_date": "2024-03-05", "facts": "Parent with autism spectrum disorder struggled with group therapy; requested individual counseling; agency refused accommodation."},
        "reasoning_task": "16_mental_health",
        "expected_behavior": {"jurisdiction": "OH", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["ORC § 2151.419"], "epistemic_classification": ["MENTAL_HEALTH", "ACCOMMODATION"]},
        "source": "Ohio Revised Code ORC § 2151.419", "jurisdiction": "OH", "legal_date": "2024-03-05", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess California case plan obligations for parents with psychological conditions.",
        "input": {"state": "CA", "county": "Los Angeles", "event_date": "2024-03-22", "facts": "Mother hospitalized for brief postpartum depression; infant placed in foster care; agency offered generic parenting classes rather than specialized treatment."},
        "reasoning_task": "16_mental_health",
        "expected_behavior": {"jurisdiction": "CA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Cal. Welf. & Inst. Code § 361.5"], "epistemic_classification": ["MENTAL_HEALTH", "CASE_PLAN"]},
        "source": "California Welfare & Institutions Code § 361.5", "jurisdiction": "CA", "legal_date": "2024-03-22", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze emergency removal following voluntary psychiatric hospitalization in Texas.",
        "input": {"state": "TX", "county": "Travis", "event_date": "2024-04-10", "facts": "Mother voluntarily checked into hospital for medication adjustment after leaving child with competent adult grandmother; CPS removed child from grandmother."},
        "reasoning_task": "16_mental_health",
        "expected_behavior": {"jurisdiction": "TX", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Tex. Fam. Code § 262.104"], "epistemic_classification": ["MENTAL_HEALTH", "HOSPITALIZATION"]},
        "source": "Texas Family Code § 262.104", "jurisdiction": "TX", "legal_date": "2024-04-10", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate Florida supportive in-home services alternative to removal for parent with anxiety.",
        "input": {"state": "FL", "county": "Miami-Dade", "event_date": "2024-05-01", "facts": "Parent experiences panic attacks; child is safe and attended by father; department seeks shelter custody instead of in-home protective supervision."},
        "reasoning_task": "16_mental_health",
        "expected_behavior": {"jurisdiction": "FL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Fla. Stat. § 39.402"], "epistemic_classification": ["MENTAL_HEALTH", "SUPPORTIVE_SERVICES"]},
        "source": "Florida Statutes § 39.402", "jurisdiction": "FL", "legal_date": "2024-05-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess Pennsylvania legal representation duties for parent facing mental health challenges.",
        "input": {"state": "PA", "county": "Philadelphia", "event_date": "2024-05-20", "facts": "Parent struggled to understand proceedings due to cognitive disability; counsel failed to request guardian ad litem or supportive accommodation."},
        "reasoning_task": "16_mental_health",
        "expected_behavior": {"jurisdiction": "PA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["42 Pa. C.S. § 6337"], "epistemic_classification": ["MENTAL_HEALTH", "COMPETENCY"]},
        "source": "Pennsylvania Consolidated Statutes 42 Pa. C.S. § 6337", "jurisdiction": "PA", "legal_date": "2024-05-20", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Review Georgia requirement for tailored mental health services prior to termination proceedings.",
        "input": {"state": "GA", "county": "Fulton", "event_date": "2024-06-12", "facts": "DFCS moved for termination alleging non-compliance with case plan after failing to provide accessible transportation for mental health appointments."},
        "reasoning_task": "16_mental_health",
        "expected_behavior": {"jurisdiction": "GA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["O.C.G.A. § 15-11-202"], "epistemic_classification": ["MENTAL_HEALTH", "TPR_BARRIER"]},
        "source": "Official Code of Georgia Annotated O.C.G.A. § 15-11-202", "jurisdiction": "GA", "legal_date": "2024-06-12", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze North Carolina relative placement support where parent manages mental health condition.",
        "input": {"state": "NC", "county": "Mecklenburg", "event_date": "2024-07-02", "facts": "Mother managing bipolar disorder agreed to relative kinship placement; agency moved to place child in licensed stranger foster care."},
        "reasoning_task": "16_mental_health",
        "expected_behavior": {"jurisdiction": "NC", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["N.C.G.S. § 7B-505"], "epistemic_classification": ["MENTAL_HEALTH", "KINSHIP"]},
        "source": "North Carolina General Statutes N.C.G.S. § 7B-505", "jurisdiction": "NC", "legal_date": "2024-07-02", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate Michigan case service plan transit accommodations for psychological services.",
        "input": {"state": "MI", "county": "Wayne", "event_date": "2024-07-28", "facts": "Parent assigned to clinic 25 miles away without vehicle or public transit; agency reported parent uncooperative for missing sessions."},
        "reasoning_task": "16_mental_health",
        "expected_behavior": {"jurisdiction": "MI", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["MCL 712A.18f"], "epistemic_classification": ["MENTAL_HEALTH", "TRANSPORTATION"]},
        "source": "Michigan Compiled Laws MCL 712A.18f", "jurisdiction": "MI", "legal_date": "2024-07-28", "authority_level": "T4", "dataset_version": "0.3.0"
    },
]

# 17_due_process (15 additional examples to expand existing 10 to 25)
SEEDS_17_DUE_PROCESS_EXPANSION = [
    {
        "instruction": "Evaluate due process violations in Florida 24-hour shelter hearing held without notice to parent.",
        "input": {"state": "FL", "county": "Miami-Dade", "event_date": "2024-01-15", "facts": "Agency removed child; held 24-hour shelter hearing without serving parent or providing phone notice."},
        "reasoning_task": "17_due_process",
        "expected_behavior": {"jurisdiction": "FL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Fla. Stat. § 39.402"], "epistemic_classification": ["DUE_PROCESS", "NOTICE"]},
        "source": "Florida Statutes § 39.402", "jurisdiction": "FL", "legal_date": "2024-01-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Audit Pennsylvania 72-hour informal hearing rule as fundamental due process safeguard.",
        "input": {"state": "PA", "county": "Philadelphia", "event_date": "2024-02-01", "facts": "Child detained for 6 days before informal hearing occurred; parent moves for immediate return."},
        "reasoning_task": "17_due_process",
        "expected_behavior": {"jurisdiction": "PA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["42 Pa. C.S. § 6332"], "epistemic_classification": ["DUE_PROCESS", "HEARING_DEADLINE"]},
        "source": "Pennsylvania Consolidated Statutes 42 Pa. C.S. § 6332", "jurisdiction": "PA", "legal_date": "2024-02-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Examine due process deprivation where Georgia court conducts hearing without appointed counsel for indigent parent.",
        "input": {"state": "GA", "county": "Fulton", "event_date": "2024-02-20", "facts": "Indigent mother appeared without lawyer; court refused to appoint counsel and entered preliminary detention order."},
        "reasoning_task": "17_due_process",
        "expected_behavior": {"jurisdiction": "GA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["O.C.G.A. § 15-11-103"], "epistemic_classification": ["DUE_PROCESS", "COUNSEL"]},
        "source": "Official Code of Georgia Annotated O.C.G.A. § 15-11-103", "jurisdiction": "GA", "legal_date": "2024-02-20", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze due process implications of extending North Carolina nonsecure custody without findings.",
        "input": {"state": "NC", "county": "Wake", "event_date": "2024-03-10", "facts": "Court continued nonsecure custody order without entering findings that reasonable efforts were made to prevent removal."},
        "reasoning_task": "17_due_process",
        "expected_behavior": {"jurisdiction": "NC", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["N.C.G.S. § 7B-506"], "epistemic_classification": ["DUE_PROCESS", "FINDINGS"]},
        "source": "North Carolina General Statutes N.C.G.S. § 7B-506", "jurisdiction": "NC", "legal_date": "2024-03-10", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess Michigan preliminary hearing rules regarding opportunity to cross-examine caseworker.",
        "input": {"state": "MI", "county": "Wayne", "event_date": "2024-03-25", "facts": "Referee denied defense counsel opportunity to cross-examine caseworker regarding necessity of removal."},
        "reasoning_task": "17_due_process",
        "expected_behavior": {"jurisdiction": "MI", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["MCL 712A.13a"], "epistemic_classification": ["DUE_PROCESS", "CROSS_EXAMINATION"]},
        "source": "Michigan Compiled Laws MCL 712A.13a", "jurisdiction": "MI", "legal_date": "2024-03-25", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate Virginia 72-hour preliminary removal hearing rule under Fourteenth Amendment due process.",
        "input": {"state": "VA", "county": "Fairfax", "event_date": "2024-04-10", "facts": "Emergency removal order entered; court failed to schedule preliminary hearing within mandatory 72-hour window."},
        "reasoning_task": "17_due_process",
        "expected_behavior": {"jurisdiction": "VA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Va. Code § 16.1-252"], "epistemic_classification": ["DUE_PROCESS", "HEARING_DEADLINE"]},
        "source": "Code of Virginia Va. Code § 16.1-252", "jurisdiction": "VA", "legal_date": "2024-04-10", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Audit New Jersey emergent removal summary court review standard.",
        "input": {"state": "NJ", "county": "Essex", "event_date": "2024-04-28", "facts": "Division took emergent custody on Friday; failed to file complaint or seek summary court review on next court day."},
        "reasoning_task": "17_due_process",
        "expected_behavior": {"jurisdiction": "NJ", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["N.J.S.A. 9:6-8.30"], "epistemic_classification": ["DUE_PROCESS", "SUMMARY_REVIEW"]},
        "source": "New Jersey Statutes N.J.S.A. 9:6-8.30", "jurisdiction": "NJ", "legal_date": "2024-04-28", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze due process consequence of failing to convene Texas 14-day full adversary hearing.",
        "input": {"state": "TX", "county": "Harris", "event_date": "2024-05-15", "facts": "Full adversary hearing postponed past 14 days without agreement or statutory extension; parent seeks dismissal."},
        "reasoning_task": "17_due_process",
        "expected_behavior": {"jurisdiction": "TX", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Tex. Fam. Code § 262.201"], "epistemic_classification": ["DUE_PROCESS", "DISMISSAL"]},
        "source": "Texas Family Code § 262.201", "jurisdiction": "TX", "legal_date": "2024-05-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Examine notice defects in California initial detention hearing.",
        "input": {"state": "CA", "county": "Los Angeles", "event_date": "2024-05-30", "facts": "Agency had mother's actual address but sent notice by regular mail day before hearing; hearing held in absentia."},
        "reasoning_task": "17_due_process",
        "expected_behavior": {"jurisdiction": "CA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Cal. Welf. & Inst. Code § 315"], "epistemic_classification": ["DUE_PROCESS", "NOTICE_DEFECT"]},
        "source": "California Welfare & Institutions Code § 315", "jurisdiction": "CA", "legal_date": "2024-05-30", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Review due process right to apply for return of child under New York Family Court Act Section 1028.",
        "input": {"state": "NY", "county": "Kings", "event_date": "2024-06-15", "facts": "Parent filed motion under Section 1028 for return of child; court refused to hold hearing within 3 court business days."},
        "reasoning_task": "17_due_process",
        "expected_behavior": {"jurisdiction": "NY", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["N.Y. Fam. Ct. Act § 1028"], "epistemic_classification": ["DUE_PROCESS", "SECTION_1028"]},
        "source": "New York Family Court Act § 1028", "jurisdiction": "NY", "legal_date": "2024-06-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate federal procedural due process protections for parents in foster care review proceedings.",
        "input": {"state": "US", "event_date": "2024-06-30", "facts": "Child kept in foster care for 18 months without judicial permanency hearing or written case plan."},
        "reasoning_task": "17_due_process",
        "expected_behavior": {"jurisdiction": "US", "temporal_validation": True, "authority_tier": 1, "citation_required": True, "controlling_citations": ["42 U.S.C. § 671"], "epistemic_classification": ["DUE_PROCESS", "FEDERAL_FLOOR"]},
        "source": "United States Code 42 U.S.C. § 671", "jurisdiction": "US", "legal_date": "2024-06-30", "authority_level": "T1", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze parent's statutory right to call and examine witnesses under Washington juvenile code.",
        "input": {"state": "WA", "county": "Spokane", "event_date": "2024-07-10", "facts": "Court prohibited defense counsel from calling family doctor to rebut neglect claims at fact-finding hearing."},
        "reasoning_task": "17_due_process",
        "expected_behavior": {"jurisdiction": "WA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["RCW 13.34.090"], "epistemic_classification": ["DUE_PROCESS", "WITNESS_RIGHTS"]},
        "source": "Washington State Legislature RCW 13.34.090", "jurisdiction": "WA", "legal_date": "2024-07-10", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate requirement for specific written findings on emergency custody in Illinois.",
        "input": {"state": "IL", "county": "Kane", "event_date": "2024-07-22", "facts": "Judge signed blank pre-printed form ordering custody without stating facts showing urgent necessity."},
        "reasoning_task": "17_due_process",
        "expected_behavior": {"jurisdiction": "IL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["705 ILCS 405/2-10"], "epistemic_classification": ["DUE_PROCESS", "WRITTEN_FINDINGS"]},
        "source": "Illinois General Assembly 705 ILCS 405/2-10", "jurisdiction": "IL", "legal_date": "2024-07-22", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Audit clear and convincing evidentiary standard in Ohio permanent custody termination.",
        "input": {"state": "OH", "county": "Franklin", "event_date": "2024-08-05", "facts": "Trial court granted permanent custody applying preponderance of evidence standard rather than clear and convincing proof."},
        "reasoning_task": "17_due_process",
        "expected_behavior": {"jurisdiction": "OH", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["ORC § 2151.414"], "epistemic_classification": ["DUE_PROCESS", "BURDEN_OF_PROOF"]},
        "source": "Ohio Revised Code ORC § 2151.414", "jurisdiction": "OH", "legal_date": "2024-08-05", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate conflict of interest in joint legal representation of parents under Pennsylvania law.",
        "input": {"state": "PA", "county": "Berks", "event_date": "2024-08-20", "facts": "Court appointed single public defender to represent both parents where father had alleged domestic violence history."},
        "reasoning_task": "17_due_process",
        "expected_behavior": {"jurisdiction": "PA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["42 Pa. C.S. § 6337"], "epistemic_classification": ["DUE_PROCESS", "CONFLICT_OF_INTEREST"]},
        "source": "Pennsylvania Consolidated Statutes 42 Pa. C.S. § 6337", "jurisdiction": "PA", "legal_date": "2024-08-20", "authority_level": "T4", "dataset_version": "0.3.0"
    },
]

# 18_equal_protection (10 examples)
SEEDS_18_EQUAL_PROTECTION = [
    {
        "instruction": "Analyze Equal Protection and Title VI violations where court denies certified language interpreter.",
        "input": {"state": "US", "event_date": "2024-01-20", "facts": "Spanish-speaking mother was not provided certified court interpreter; child placed in stranger foster care."},
        "reasoning_task": "18_equal_protection",
        "expected_behavior": {"jurisdiction": "US", "temporal_validation": True, "authority_tier": 1, "citation_required": True, "controlling_citations": ["42 U.S.C. § 671"], "epistemic_classification": ["EQUAL_PROTECTION", "LANGUAGE_ACCESS"]},
        "source": "United States Code 42 U.S.C. § 671", "jurisdiction": "US", "legal_date": "2024-01-20", "authority_level": "T1", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate equal protection challenge to treating poverty as neglect under Washington law.",
        "input": {"state": "WA", "county": "King", "event_date": "2024-02-12", "facts": "Agency removed children from homeless mother solely due to lack of stable lease, while wealthier parents receive voluntary support."},
        "reasoning_task": "18_equal_protection",
        "expected_behavior": {"jurisdiction": "WA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["RCW 13.34.030"], "epistemic_classification": ["EQUAL_PROTECTION", "POVERTY_DISCRIMINATION"]},
        "source": "Washington State Legislature RCW 13.34.030", "jurisdiction": "WA", "legal_date": "2024-02-12", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess equal protection disparity between foster care stipends for relative vs licensed stranger caregivers in Illinois.",
        "input": {"state": "IL", "county": "Cook", "event_date": "2024-03-05", "facts": "Maternal grandmother providing kinship care denied financial foster care stipends provided to licensed non-relatives."},
        "reasoning_task": "18_equal_protection",
        "expected_behavior": {"jurisdiction": "IL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["705 ILCS 405/2-10"], "epistemic_classification": ["EQUAL_PROTECTION", "KINSHIP_STIPEND"]},
        "source": "Illinois General Assembly 705 ILCS 405/2-10", "jurisdiction": "IL", "legal_date": "2024-03-05", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate differential service provision between rural and urban county agencies in Ohio.",
        "input": {"state": "OH", "county": "Athens", "event_date": "2024-03-25", "facts": "Rural county provided no substance treatment programs within 50 miles, resulting in higher termination rates than urban counties."},
        "reasoning_task": "18_equal_protection",
        "expected_behavior": {"jurisdiction": "OH", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["ORC § 2151.419"], "epistemic_classification": ["EQUAL_PROTECTION", "GEOGRAPHIC_DISPARITY"]},
        "source": "Ohio Revised Code ORC § 2151.419", "jurisdiction": "OH", "legal_date": "2024-03-25", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze language access rights under Equal Protection in California juvenile dependency proceedings.",
        "input": {"state": "CA", "county": "Fresno", "event_date": "2024-04-15", "facts": "Indigenous Mixteco-speaking mother was provided Spanish interpreter; mother could not understand proceedings."},
        "reasoning_task": "18_equal_protection",
        "expected_behavior": {"jurisdiction": "CA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Cal. Welf. & Inst. Code § 315"], "epistemic_classification": ["EQUAL_PROTECTION", "INDIGENOUS_LANGUAGE"]},
        "source": "California Welfare & Institutions Code § 315", "jurisdiction": "CA", "legal_date": "2024-04-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Examine racial and socioeconomic profiling in Texas warrantless emergency removals.",
        "input": {"state": "TX", "county": "Harris", "event_date": "2024-05-02", "facts": "Investigator removed child without warrant citing neighborhood crime statistics rather than individual parental unfitness."},
        "reasoning_task": "18_equal_protection",
        "expected_behavior": {"jurisdiction": "TX", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Tex. Fam. Code § 262.104"], "epistemic_classification": ["EQUAL_PROTECTION", "PROFILING"]},
        "source": "Texas Family Code § 262.104", "jurisdiction": "TX", "legal_date": "2024-05-02", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze immigration status discrimination in Florida child custody determinations.",
        "input": {"state": "FL", "county": "Miami-Dade", "event_date": "2024-05-25", "facts": "Judge cited mother's undocumented immigration status as grounds to deny return of child and order foster placement."},
        "reasoning_task": "18_equal_protection",
        "expected_behavior": {"jurisdiction": "FL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Fla. Stat. § 39.402"], "epistemic_classification": ["EQUAL_PROTECTION", "IMMIGRATION"]},
        "source": "Florida Statutes § 39.402", "jurisdiction": "FL", "legal_date": "2024-05-25", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess discriminatory exclusion of relative placement based on minor non-violent record in Pennsylvania.",
        "input": {"state": "PA", "county": "Philadelphia", "event_date": "2024-06-12", "facts": "Grandmother disqualified as kinship foster provider due to 15-year-old misdemeanor disorderly conduct conviction."},
        "reasoning_task": "18_equal_protection",
        "expected_behavior": {"jurisdiction": "PA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["42 Pa. C.S. § 6332"], "epistemic_classification": ["EQUAL_PROTECTION", "KINSHIP_BARRIER"]},
        "source": "Pennsylvania Consolidated Statutes 42 Pa. C.S. § 6332", "jurisdiction": "PA", "legal_date": "2024-06-12", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate Indian Child Welfare Act equal protection challenge and tribal classification in federal law.",
        "input": {"state": "US", "event_date": "2024-07-01", "facts": "Challengers argue ICWA placement preferences constitute race discrimination; federal precedent upholds political classification."},
        "reasoning_task": "18_equal_protection",
        "expected_behavior": {"jurisdiction": "US", "temporal_validation": True, "authority_tier": 1, "citation_required": True, "controlling_citations": ["25 U.S.C. § 1915"], "epistemic_classification": ["EQUAL_PROTECTION", "TRIBAL_POLITICAL"]},
        "source": "United States Code 25 U.S.C. § 1915", "jurisdiction": "US", "legal_date": "2024-07-01", "authority_level": "T1", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze equal protection violation where housing instability is treated as neglect in North Carolina.",
        "input": {"state": "NC", "county": "Mecklenburg", "event_date": "2024-07-20", "facts": "Low-income father living in extended-stay motel had children removed solely due to lack of permanent residential lease."},
        "reasoning_task": "18_equal_protection",
        "expected_behavior": {"jurisdiction": "NC", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["N.C.G.S. § 7B-500"], "epistemic_classification": ["EQUAL_PROTECTION", "HOUSING_DISCRIMINATION"]},
        "source": "North Carolina General Statutes N.C.G.S. § 7B-500", "jurisdiction": "NC", "legal_date": "2024-07-20", "authority_level": "T4", "dataset_version": "0.3.0"
    },
]

# 20_family_integrity (10 examples)
SEEDS_20_FAMILY_INTEGRITY = [
    {
        "instruction": "Analyze constitutional right to family integrity and parental liberty under Washington law.",
        "input": {"state": "WA", "county": "King", "event_date": "2024-01-18", "facts": "Welfare agency removed child without showing imminent physical harm; parent asserts fundamental liberty interest in custody."},
        "reasoning_task": "20_family_integrity",
        "expected_behavior": {"jurisdiction": "WA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["RCW 13.34.050"], "epistemic_classification": ["FAMILY_INTEGRITY", "CONSTITUTIONAL"]},
        "source": "Washington State Legislature RCW 13.34.050", "jurisdiction": "WA", "legal_date": "2024-01-18", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate duty to maintain family integrity through in-home protective services in Illinois.",
        "input": {"state": "IL", "county": "Cook", "event_date": "2024-02-10", "facts": "Agency sought out-of-home placement; defense establishes in-home homemaker assistance would safely preserve family unit."},
        "reasoning_task": "20_family_integrity",
        "expected_behavior": {"jurisdiction": "IL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["705 ILCS 405/2-10"], "epistemic_classification": ["FAMILY_INTEGRITY", "IN_HOME_SERVICES"]},
        "source": "Illinois General Assembly 705 ILCS 405/2-10", "jurisdiction": "IL", "legal_date": "2024-02-10", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess preservation of family integrity through relative kinship placement in Ohio.",
        "input": {"state": "OH", "county": "Cuyahoga", "event_date": "2024-03-01", "facts": "Grandparents willing to provide immediate custody; agency placed child with stranger foster family; parents assert kinship preference."},
        "reasoning_task": "20_family_integrity",
        "expected_behavior": {"jurisdiction": "OH", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["ORC § 2151.314"], "epistemic_classification": ["FAMILY_INTEGRITY", "KINSHIP_PRIORITY"]},
        "source": "Ohio Revised Code ORC § 2151.314", "jurisdiction": "OH", "legal_date": "2024-03-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate statutory presumption favoring family reunification in California dependency.",
        "input": {"state": "CA", "county": "Los Angeles", "event_date": "2024-03-20", "facts": "Court bypassed reunification services without clear statutory grounds; parents move for full statutory reunification period."},
        "reasoning_task": "20_family_integrity",
        "expected_behavior": {"jurisdiction": "CA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Cal. Welf. & Inst. Code § 361.5"], "epistemic_classification": ["FAMILY_INTEGRITY", "REUNIFICATION"]},
        "source": "California Welfare & Institutions Code § 361.5", "jurisdiction": "CA", "legal_date": "2024-03-20", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze emergency standard required to overcome presumption of family integrity in Texas.",
        "input": {"state": "TX", "county": "Harris", "event_date": "2024-04-05", "facts": "Warrantless removal executed on non-emergency grounds; defense argues state failed to demonstrate immediate physical danger."},
        "reasoning_task": "20_family_integrity",
        "expected_behavior": {"jurisdiction": "TX", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Tex. Fam. Code § 262.104"], "epistemic_classification": ["FAMILY_INTEGRITY", "BURDEN_OF_PROOF"]},
        "source": "Texas Family Code § 262.104", "jurisdiction": "TX", "legal_date": "2024-04-05", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Examine statutory mechanism for immediate return of child to preserve family unity in New York.",
        "input": {"state": "NY", "county": "New York", "event_date": "2024-04-28", "facts": "Parent files 1028 application asserting continued separation inflicts trauma on child and allegations can be managed at home."},
        "reasoning_task": "20_family_integrity",
        "expected_behavior": {"jurisdiction": "NY", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["N.Y. Fam. Ct. Act § 1028"], "epistemic_classification": ["FAMILY_INTEGRITY", "RETURN_APPLICATION"]},
        "source": "New York Family Court Act § 1028", "jurisdiction": "NY", "legal_date": "2024-04-28", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Review Florida mandate to preserve parent-child bond through regular visitation.",
        "input": {"state": "FL", "county": "Miami-Dade", "event_date": "2024-05-15", "facts": "Agency suspended parent visits to coerce participation in extra-statutory services; parent moves for immediate visitation order."},
        "reasoning_task": "20_family_integrity",
        "expected_behavior": {"jurisdiction": "FL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Fla. Stat. § 39.402"], "epistemic_classification": ["FAMILY_INTEGRITY", "VISITATION_RIGHTS"]},
        "source": "Florida Statutes § 39.402", "jurisdiction": "FL", "legal_date": "2024-05-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess Pennsylvania Juvenile Act purpose to preserve the unity of the family.",
        "input": {"state": "PA", "county": "Philadelphia", "event_date": "2024-06-02", "facts": "Court placed child in group home; Juvenile Act mandates preserving family unity and exploring kinship care alternatives."},
        "reasoning_task": "20_family_integrity",
        "expected_behavior": {"jurisdiction": "PA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["42 Pa. C.S. § 6351"], "epistemic_classification": ["FAMILY_INTEGRITY", "STATUTORY_PURPOSE"]},
        "source": "Pennsylvania Consolidated Statutes 42 Pa. C.S. § 6351", "jurisdiction": "PA", "legal_date": "2024-06-02", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate heightened federal standard requiring active efforts to prevent breakup of Indian family.",
        "input": {"state": "US", "event_date": "2024-06-25", "facts": "Agency provided superficial referrals; ICWA § 1912(d) mandates affirmative, culturally relevant active efforts to maintain family integrity."},
        "reasoning_task": "20_family_integrity",
        "expected_behavior": {"jurisdiction": "US", "temporal_validation": True, "authority_tier": 1, "citation_required": True, "controlling_citations": ["25 U.S.C. § 1912"], "epistemic_classification": ["FAMILY_INTEGRITY", "ACTIVE_EFFORTS"]},
        "source": "United States Code 25 U.S.C. § 1912", "jurisdiction": "US", "legal_date": "2024-06-25", "authority_level": "T1", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze Georgia statutory priority for kinship placement to safeguard extended family ties.",
        "input": {"state": "GA", "county": "Fulton", "event_date": "2024-07-15", "facts": "DFCS refused to assess paternal grandmother; Georgia code directs court to evaluate relatives to preserve family integrity."},
        "reasoning_task": "20_family_integrity",
        "expected_behavior": {"jurisdiction": "GA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["O.C.G.A. § 15-11-145"], "epistemic_classification": ["FAMILY_INTEGRITY", "KINSHIP_EVALUATION"]},
        "source": "Official Code of Georgia Annotated O.C.G.A. § 15-11-145", "jurisdiction": "GA", "legal_date": "2024-07-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
]

# 21_administrative_law (10 examples)
SEEDS_21_ADMINISTRATIVE_LAW = [
    {
        "instruction": "Analyze due process hearing rights to challenge founded child abuse finding on Washington central registry.",
        "input": {"state": "WA", "county": "King", "event_date": "2024-01-28", "facts": "DCYF issued founded finding of negligent treatment without formal court adjudication; parent requested administrative hearing."},
        "reasoning_task": "21_administrative_law",
        "expected_behavior": {"jurisdiction": "WA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["RCW 26.44.100"], "epistemic_classification": ["ADMINISTRATIVE", "CENTRAL_REGISTRY"]},
        "source": "Washington State Legislature RCW 26.44.100", "jurisdiction": "WA", "legal_date": "2024-01-28", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate administrative appeal and expungement procedures under Illinois Abused and Neglected Child Reporting Act.",
        "input": {"state": "IL", "county": "Cook", "event_date": "2024-02-22", "facts": "DCFS entered indicated report against certified daycare worker; worker timely filed notice of administrative appeal."},
        "reasoning_task": "21_administrative_law",
        "expected_behavior": {"jurisdiction": "IL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["325 ILCS 5/7.16"], "epistemic_classification": ["ADMINISTRATIVE", "EXPUNGEMENT"]},
        "source": "Illinois General Assembly 325 ILCS 5/7.16", "jurisdiction": "IL", "legal_date": "2024-02-22", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze federal Child Abuse Prevention and Treatment Act (CAPTA) administrative hearing mandates.",
        "input": {"state": "US", "event_date": "2024-03-12", "facts": "State child protection system provided no administrative mechanism for accused parents to challenge substantiated maltreatment findings."},
        "reasoning_task": "21_administrative_law",
        "expected_behavior": {"jurisdiction": "US", "temporal_validation": True, "authority_tier": 1, "citation_required": True, "controlling_citations": ["42 U.S.C. § 5106a"], "epistemic_classification": ["ADMINISTRATIVE", "CAPTA_MANDATE"]},
        "source": "United States Code 42 U.S.C. § 5106a", "jurisdiction": "US", "legal_date": "2024-03-12", "authority_level": "T1", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess Ohio administrative review procedures for contested central registry investigations.",
        "input": {"state": "OH", "county": "Cuyahoga", "event_date": "2024-04-02", "facts": "Parent received notification of substantiated finding; requested administrative review by public children services agency director."},
        "reasoning_task": "21_administrative_law",
        "expected_behavior": {"jurisdiction": "OH", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["ORC § 2151.421"], "epistemic_classification": ["ADMINISTRATIVE", "REGISTRY_REVIEW"]},
        "source": "Ohio Revised Code ORC § 2151.421", "jurisdiction": "OH", "legal_date": "2024-04-02", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate exhaustion of administrative remedies before challenging California social services decisions.",
        "input": {"state": "CA", "county": "Orange", "event_date": "2024-04-20", "facts": "Foster parent filed state court lawsuit challenging county service denial prior to completing county grievance procedure."},
        "reasoning_task": "21_administrative_law",
        "expected_behavior": {"jurisdiction": "CA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Cal. Welf. & Inst. Code § 300"], "epistemic_classification": ["ADMINISTRATIVE", "EXHAUSTION"]},
        "source": "California Welfare & Institutions Code § 300", "jurisdiction": "CA", "legal_date": "2024-04-20", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze Texas administrative review of child abuse investigative dispositions under Family Code.",
        "input": {"state": "TX", "county": "Travis", "event_date": "2024-05-08", "facts": "DFPS investigator issued 'reason to believe' finding; alleged perpetrator filed request for administrative review of findings (ARIF)."},
        "reasoning_task": "21_administrative_law",
        "expected_behavior": {"jurisdiction": "TX", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Tex. Fam. Code § 262.109"], "epistemic_classification": ["ADMINISTRATIVE", "ARIF"]},
        "source": "Texas Family Code § 262.109", "jurisdiction": "TX", "legal_date": "2024-05-08", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess Florida administrative hearing rights to amend or expunge child maltreatment record.",
        "input": {"state": "FL", "county": "Leon", "event_date": "2024-05-28", "facts": "Teacher received verified report of neglect; petitioned Florida Division of Administrative Hearings (DOAH) for expungement."},
        "reasoning_task": "21_administrative_law",
        "expected_behavior": {"jurisdiction": "FL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Fla. Stat. § 39.01"], "epistemic_classification": ["ADMINISTRATIVE", "DOAH_EXPUNGEMENT"]},
        "source": "Florida Statutes § 39.01", "jurisdiction": "FL", "legal_date": "2024-05-28", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Review Pennsylvania ChildLine administrative registry appeal and expungement standards.",
        "input": {"state": "PA", "county": "Dauphin", "event_date": "2024-06-15", "facts": "Individual named as perpetrator in indicated report filed timely appeal with Department of Human Services Bureau of Hearings and Appeals."},
        "reasoning_task": "21_administrative_law",
        "expected_behavior": {"jurisdiction": "PA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["23 Pa. C.S. § 6315"], "epistemic_classification": ["ADMINISTRATIVE", "CHILDLINE_APPEAL"]},
        "source": "Pennsylvania Consolidated Statutes 23 Pa. C.S. § 6315", "jurisdiction": "PA", "legal_date": "2024-06-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate North Carolina county DSS compliance with administrative policy and statutory mandates.",
        "input": {"state": "NC", "county": "Wake", "event_date": "2024-07-05", "facts": "County DSS failed to follow state administrative division guidelines governing screening and intake of dependency petitions."},
        "reasoning_task": "21_administrative_law",
        "expected_behavior": {"jurisdiction": "NC", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["N.C.G.S. § 7B-405"], "epistemic_classification": ["ADMINISTRATIVE", "INTAKE_RULES"]},
        "source": "North Carolina General Statutes N.C.G.S. § 7B-405", "jurisdiction": "NC", "legal_date": "2024-07-05", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze Michigan administrative review of child protective services investigation findings.",
        "input": {"state": "MI", "county": "Wayne", "event_date": "2024-07-22", "facts": "MDHHS placed individual on central registry; individual requested administrative hearing before Michigan Office of Administrative Hearings and Rules."},
        "reasoning_task": "21_administrative_law",
        "expected_behavior": {"jurisdiction": "MI", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["MCL 712A.14"], "epistemic_classification": ["ADMINISTRATIVE", "REGISTRY_HEARING"]},
        "source": "Michigan Compiled Laws MCL 712A.14", "jurisdiction": "MI", "legal_date": "2024-07-22", "authority_level": "T4", "dataset_version": "0.3.0"
    },
]

# 22_civil_rights (10 examples)
SEEDS_22_CIVIL_RIGHTS = [
    {
        "instruction": "Analyze Section 1983 Fourth Amendment liability for warrantless child removal absent exigent circumstances in Washington.",
        "input": {"state": "WA", "county": "King", "event_date": "2024-01-20", "facts": "Caseworker and police entered home without warrant, consent, or imminent danger, and seized two minor children."},
        "reasoning_task": "22_civil_rights",
        "expected_behavior": {"jurisdiction": "WA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["RCW 13.34.050"], "epistemic_classification": ["CIVIL_RIGHTS", "SECTION_1983"]},
        "source": "Washington State Legislature RCW 13.34.050", "jurisdiction": "WA", "legal_date": "2024-01-20", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate Fourth Amendment coercion and unlawful search during Illinois CPS home visit.",
        "input": {"state": "IL", "county": "Cook", "event_date": "2024-02-14", "facts": "Caseworker threatened immediate arrest unless parent permitted warrantless search of bedrooms and medicine cabinets."},
        "reasoning_task": "22_civil_rights",
        "expected_behavior": {"jurisdiction": "IL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["705 ILCS 405/2-6"], "epistemic_classification": ["CIVIL_RIGHTS", "FOURTH_AMENDMENT"]},
        "source": "Illinois General Assembly 705 ILCS 405/2-6", "jurisdiction": "IL", "legal_date": "2024-02-14", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess Title VI Civil Rights violation where agency fails to provide certified interpreter in California.",
        "input": {"state": "CA", "county": "Fresno", "event_date": "2024-03-01", "facts": "Agency conducted all interviews and evaluations in English despite knowing parent spoke only indigenous language."},
        "reasoning_task": "22_civil_rights",
        "expected_behavior": {"jurisdiction": "CA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Cal. Welf. & Inst. Code § 315"], "epistemic_classification": ["CIVIL_RIGHTS", "TITLE_VI"]},
        "source": "California Welfare & Institutions Code § 315", "jurisdiction": "CA", "legal_date": "2024-03-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Examine Fourteenth Amendment substantive due process claim for deliberate fabrication of evidence in Texas removal.",
        "input": {"state": "TX", "county": "Harris", "event_date": "2024-03-22", "facts": "Caseworker knowingly altered parent interview statements in sworn affidavit to fabricate basis for emergency order."},
        "reasoning_task": "22_civil_rights",
        "expected_behavior": {"jurisdiction": "TX", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Tex. Fam. Code § 262.101"], "epistemic_classification": ["CIVIL_RIGHTS", "FABRICATION_OF_EVIDENCE"]},
        "source": "Texas Family Code § 262.101", "jurisdiction": "TX", "legal_date": "2024-03-22", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate First Amendment retaliation claim where agency removes child after parent files civil complaint in Ohio.",
        "input": {"state": "OH", "county": "Cuyahoga", "event_date": "2024-04-10", "facts": "Parent filed formal grievance against caseworker; caseworker immediately initiated emergency protective custody proceeding."},
        "reasoning_task": "22_civil_rights",
        "expected_behavior": {"jurisdiction": "OH", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["ORC § 2151.31"], "epistemic_classification": ["CIVIL_RIGHTS", "RETALIATION"]},
        "source": "Ohio Revised Code ORC § 2151.31", "jurisdiction": "OH", "legal_date": "2024-04-10", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze Americans with Disabilities Act Title II claim against Florida Department of Children and Families.",
        "input": {"state": "FL", "county": "Miami-Dade", "event_date": "2024-05-02", "facts": "Deaf parent was denied ASL certified interpreter during required dependency hearings and case planning meetings."},
        "reasoning_task": "22_civil_rights",
        "expected_behavior": {"jurisdiction": "FL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Fla. Stat. § 39.402"], "epistemic_classification": ["CIVIL_RIGHTS", "ADA_TITLE_II"]},
        "source": "Florida Statutes § 39.402", "jurisdiction": "FL", "legal_date": "2024-05-02", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess Fourth Amendment unlawful seizure claim for seizing child from public school in Pennsylvania.",
        "input": {"state": "PA", "county": "Philadelphia", "event_date": "2024-05-25", "facts": "CYS caseworker removed child from elementary school without parental consent, warrant, or exigent emergency danger."},
        "reasoning_task": "22_civil_rights",
        "expected_behavior": {"jurisdiction": "PA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["42 Pa. C.S. § 6324"], "epistemic_classification": ["CIVIL_RIGHTS", "SCHOOL_SEIZURE"]},
        "source": "Pennsylvania Consolidated Statutes 42 Pa. C.S. § 6324", "jurisdiction": "PA", "legal_date": "2024-05-25", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate Section 1983 claim for prolonged detention without judicial hearing in Georgia.",
        "input": {"state": "GA", "county": "Fulton", "event_date": "2024-06-15", "facts": "DFCS kept child in temporary foster custody for 10 days without filing petition or bringing matter before juvenile judge."},
        "reasoning_task": "22_civil_rights",
        "expected_behavior": {"jurisdiction": "GA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["O.C.G.A. § 15-11-133"], "epistemic_classification": ["CIVIL_RIGHTS", "PROLONGED_DETENTION"]},
        "source": "Official Code of Georgia Annotated O.C.G.A. § 15-11-133", "jurisdiction": "GA", "legal_date": "2024-06-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze civil rights enforcement under federal Title IV-E statutory scheme.",
        "input": {"state": "US", "event_date": "2024-07-01", "facts": "State systematically failed to provide statutory procedural safeguards and periodic judicial reviews to foster children."},
        "reasoning_task": "22_civil_rights",
        "expected_behavior": {"jurisdiction": "US", "temporal_validation": True, "authority_tier": 1, "citation_required": True, "controlling_citations": ["42 U.S.C. § 671"], "epistemic_classification": ["CIVIL_RIGHTS", "FEDERAL_STATUTORY"]},
        "source": "United States Code 42 U.S.C. § 671", "jurisdiction": "US", "legal_date": "2024-07-01", "authority_level": "T1", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Examine First Amendment Free Exercise rights regarding religious healthcare choices in Michigan.",
        "input": {"state": "MI", "county": "Kent", "event_date": "2024-07-20", "facts": "Agency removed child alleging neglect after parents sought second medical opinion consistent with faith community beliefs."},
        "reasoning_task": "22_civil_rights",
        "expected_behavior": {"jurisdiction": "MI", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["MCL 712A.13a"], "epistemic_classification": ["CIVIL_RIGHTS", "FREE_EXERCISE"]},
        "source": "Michigan Compiled Laws MCL 712A.13a", "jurisdiction": "MI", "legal_date": "2024-07-20", "authority_level": "T4", "dataset_version": "0.3.0"
    },
]

# 23_procedural_rights (10 examples)
SEEDS_23_PROCEDURAL_RIGHTS = [
    {
        "instruction": "Analyze parent's statutory right to formal discovery and access to case file in Washington.",
        "input": {"state": "WA", "county": "King", "event_date": "2024-01-15", "facts": "Agency refused to provide caseworker notes, medical evaluation reports, and witness contact information prior to fact-finding trial."},
        "reasoning_task": "23_procedural_rights",
        "expected_behavior": {"jurisdiction": "WA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["RCW 13.34.090"], "epistemic_classification": ["PROCEDURAL", "DISCOVERY"]},
        "source": "Washington State Legislature RCW 13.34.090", "jurisdiction": "WA", "legal_date": "2024-01-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate respondent parent's procedural right to confront adverse witnesses and evidence in Illinois.",
        "input": {"state": "IL", "county": "Cook", "event_date": "2024-02-10", "facts": "Judge accepted written summary report without requiring caseworker or doctor to testify or undergo cross-examination."},
        "reasoning_task": "23_procedural_rights",
        "expected_behavior": {"jurisdiction": "IL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["705 ILCS 405/2-18"], "epistemic_classification": ["PROCEDURAL", "CROSS_EXAMINATION"]},
        "source": "Illinois General Assembly 705 ILCS 405/2-18", "jurisdiction": "IL", "legal_date": "2024-02-10", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess right to compulsory process and subpoena power for respondent parents in Ohio.",
        "input": {"state": "OH", "county": "Cuyahoga", "event_date": "2024-03-01", "facts": "Clerk of court refused to issue subpoenas for parent's treating physician and family therapist to testify at hearing."},
        "reasoning_task": "23_procedural_rights",
        "expected_behavior": {"jurisdiction": "OH", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["ORC § 2151.35"], "epistemic_classification": ["PROCEDURAL", "SUBPOENA"]},
        "source": "Ohio Revised Code ORC § 2151.35", "jurisdiction": "OH", "legal_date": "2024-03-01", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Determine right to formal evidentiary trial on allegations in California Section 300 petition.",
        "input": {"state": "CA", "county": "Los Angeles", "event_date": "2024-03-22", "facts": "Court ordered child into foster placement at initial hearing without scheduling contested jurisdictional fact-finding hearing."},
        "reasoning_task": "23_procedural_rights",
        "expected_behavior": {"jurisdiction": "CA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Cal. Welf. & Inst. Code § 355"], "epistemic_classification": ["PROCEDURAL", "CONTESTED_TRIAL"]},
        "source": "California Welfare & Institutions Code § 355", "jurisdiction": "CA", "legal_date": "2024-03-22", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Review statutory right to complete court reporter record for appeal in Texas child welfare.",
        "input": {"state": "TX", "county": "Bexar", "event_date": "2024-04-12", "facts": "Judge conducted full adversary hearing off the record without court reporter; parent requested transcript for appeal."},
        "reasoning_task": "23_procedural_rights",
        "expected_behavior": {"jurisdiction": "TX", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Tex. Fam. Code § 262.201"], "epistemic_classification": ["PROCEDURAL", "RECORD_FOR_APPEAL"]},
        "source": "Texas Family Code § 262.201", "jurisdiction": "TX", "legal_date": "2024-04-12", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze personal service and petition delivery deadlines in Florida dependency arraignment.",
        "input": {"state": "FL", "county": "Orange", "event_date": "2024-05-05", "facts": "Petition served on parent in courtroom hallway 10 minutes prior to formal arraignment and plea entry."},
        "reasoning_task": "23_procedural_rights",
        "expected_behavior": {"jurisdiction": "FL", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["Fla. Stat. § 39.501"], "epistemic_classification": ["PROCEDURAL", "TIMELY_SERVICE"]},
        "source": "Florida Statutes § 39.501", "jurisdiction": "FL", "legal_date": "2024-05-05", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate right to bifurcated adjudication and dispositional hearings in Pennsylvania.",
        "input": {"state": "PA", "county": "Philadelphia", "event_date": "2024-05-25", "facts": "Court entered disposition terminating custody immediately upon finding dependency without separate dispositional hearing."},
        "reasoning_task": "23_procedural_rights",
        "expected_behavior": {"jurisdiction": "PA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["42 Pa. C.S. § 6335"], "epistemic_classification": ["PROCEDURAL", "BIFURCATION"]},
        "source": "Pennsylvania Consolidated Statutes 42 Pa. C.S. § 6335", "jurisdiction": "PA", "legal_date": "2024-05-25", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Assess right to file motion to dismiss for insufficient petition allegations in Georgia.",
        "input": {"state": "GA", "county": "Fulton", "event_date": "2024-06-15", "facts": "Dependency petition failed to state date, place, or specific conduct of neglect; parent filed pre-trial motion to dismiss."},
        "reasoning_task": "23_procedural_rights",
        "expected_behavior": {"jurisdiction": "GA", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["O.C.G.A. § 15-11-181"], "epistemic_classification": ["PROCEDURAL", "MOTION_TO_DISMISS"]},
        "source": "Official Code of Georgia Annotated O.C.G.A. § 15-11-181", "jurisdiction": "GA", "legal_date": "2024-06-15", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Evaluate mandatory written notice contents for nonsecure custody hearing in North Carolina.",
        "input": {"state": "NC", "county": "Wake", "event_date": "2024-07-02", "facts": "Notice mailed to parent omitted time of hearing, court location, and information on right to appointed counsel."},
        "reasoning_task": "23_procedural_rights",
        "expected_behavior": {"jurisdiction": "NC", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["N.C.G.S. § 7B-506"], "epistemic_classification": ["PROCEDURAL", "NOTICE_CONTENTS"]},
        "source": "North Carolina General Statutes N.C.G.S. § 7B-506", "jurisdiction": "NC", "legal_date": "2024-07-02", "authority_level": "T4", "dataset_version": "0.3.0"
    },
    {
        "instruction": "Analyze right to emergency interlocutory appeal of wrongful removal order in Michigan.",
        "input": {"state": "MI", "county": "Wayne", "event_date": "2024-07-25", "facts": "Court ordered child into foster placement; parent filed emergency application for leave to appeal with Court of Appeals."},
        "reasoning_task": "23_procedural_rights",
        "expected_behavior": {"jurisdiction": "MI", "temporal_validation": True, "authority_tier": 4, "citation_required": True, "controlling_citations": ["MCR 3.965"], "epistemic_classification": ["PROCEDURAL", "INTERLOCUTORY_APPEAL"]},
        "source": "Michigan Court Rules MCR 3.965", "jurisdiction": "MI", "legal_date": "2024-07-25", "authority_level": "T4", "dataset_version": "0.3.0"
    },
]
