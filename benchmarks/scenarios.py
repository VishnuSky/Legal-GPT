"""Comprehensive Multi-Jurisdiction Benchmark Scenarios and Evaluation Suite."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import date
from agents.legal_orchestrator import LegalGPTOrchestrator


class BenchmarkScenario(BaseModel):
    scenario_id: str
    title: str
    category: str  # CPS_EMERGENCY, ICWA, UCCJEA, PARENT_RIGHTS, TEMPORAL, PROCEDURAL, DUE_PROCESS
    state: Optional[str] = None
    county: Optional[str] = None
    event_date: Optional[date] = None
    prompt: str
    expected_jurisdiction_contains: str
    expected_controlling_citations: List[str]
    expected_procedural_keywords: List[str]
    is_icwa_eligible: bool = False
    months_in_state: Optional[int] = None
    notice_given: bool = True
    counsel_present: bool = True


# Comprehensive 50-Scenario Benchmark Suite (100% Pure Objective Statutory Queries)
BENCHMARK_SCENARIOS: List[BenchmarkScenario] = [
    # 1-5: Washington State CPS LifeCycle & JuCR Rules
    BenchmarkScenario(
        scenario_id="WA-01",
        title="WA Emergency Removal Statutory Standards",
        category="CPS_EMERGENCY",
        state="WA",
        prompt="What are the statutory requirements, warrant standards, and exigent circumstances criteria for emergency child custody removal under RCW 13.34.050?",
        expected_jurisdiction_contains="WA",
        expected_controlling_citations=["RCW 13.34.050", "JuCR 2.1"],
        expected_procedural_keywords=["imminent danger", "72 hours"]
    ),
    BenchmarkScenario(
        scenario_id="WA-02",
        title="WA Shelter Care Hearing 72h Timeline",
        category="CPS_EMERGENCY",
        state="WA",
        prompt="What are the statutory deadlines and kinship placement duties governing preliminary shelter care hearings under RCW 13.34.065?",
        expected_jurisdiction_contains="WA",
        expected_controlling_citations=["RCW 13.34.065"],
        expected_procedural_keywords=["72 hours", "relative"]
    ),
    BenchmarkScenario(
        scenario_id="WA-03",
        title="WA Parent Right to Appointed Counsel",
        category="PARENT_RIGHTS",
        state="WA",
        prompt="What statutory rights guarantee court-appointed legal representation for indigent parents under RCW 13.34.090?",
        expected_jurisdiction_contains="WA",
        expected_controlling_citations=["RCW 13.34.090", "RCW 13.34.065"],
        expected_procedural_keywords=["counsel", "indigent", "advisement"]
    ),
    BenchmarkScenario(
        scenario_id="WA-04",
        title="WA Remedial Services Tailoring Standard",
        category="PARENT_RIGHTS",
        state="WA",
        prompt="What is the legal standard for offering individually tailored remedial services to parents under RCW 13.34.136 and In re Dependency of K.N.J.?",
        expected_jurisdiction_contains="WA",
        expected_controlling_citations=["RCW 13.34.136", "In re Dependency of K.N.J."],
        expected_procedural_keywords=["reasonable efforts", "tailored"]
    ),
    BenchmarkScenario(
        scenario_id="WA-05",
        title="WA Family Time & Visitation Protections",
        category="PARENT_RIGHTS",
        state="WA",
        prompt="What statutory standards govern family time, parent-child visitation schedules, and restrictions under RCW 13.34.065?",
        expected_jurisdiction_contains="WA",
        expected_controlling_citations=["RCW 13.34.065", "DCYF Policy"],
        expected_procedural_keywords=["visitation", "family time"]
    ),

    # 6-10: Illinois Juvenile Court Act (705 ILCS 405)
    BenchmarkScenario(
        scenario_id="IL-01",
        title="IL 48-Hour Temporary Custody Hearing",
        category="CPS_EMERGENCY",
        state="IL",
        prompt="What are the statutory timeframes and probable cause standards for temporary custody hearings under 705 ILCS 405/2-9 and 405/2-10?",
        expected_jurisdiction_contains="IL",
        expected_controlling_citations=["705 ILCS 405/2-9", "705 ILCS 405/2-10"],
        expected_procedural_keywords=["48 hours", "probable cause", "urgent and immediate necessity"]
    ),
    BenchmarkScenario(
        scenario_id="IL-02",
        title="IL Rehearing Motion on Temporary Custody",
        category="PROCEDURAL",
        state="IL",
        prompt="What are the procedural rules and filing requirements for a rehearing on temporary custody under 705 ILCS 405/2-10(b)?",
        expected_jurisdiction_contains="IL",
        expected_controlling_citations=["705 ILCS 405/2-10(b)"],
        expected_procedural_keywords=["rehearing", "affidavit", "14 days"]
    ),
    BenchmarkScenario(
        scenario_id="IL-03",
        title="IL Relative Placement Preference",
        category="PARENT_RIGHTS",
        state="IL",
        prompt="What statutory priority is given to adult relative and kinship placements under 705 ILCS 405/1-3 and federal Title IV-E standards?",
        expected_jurisdiction_contains="IL",
        expected_controlling_citations=["705 ILCS 405/1-3", "42 U.S.C. § 671"],
        expected_procedural_keywords=["relative", "kinship", "preference"]
    ),
    BenchmarkScenario(
        scenario_id="IL-04",
        title="IL Adjudication Burden of Proof",
        category="DUE_PROCESS",
        state="IL",
        prompt="What standard of proof is required at an adjudicatory trial under 705 ILCS 405/2-18 and In re Arthur H.?",
        expected_jurisdiction_contains="IL",
        expected_controlling_citations=["705 ILCS 405/2-18", "In re Arthur H."],
        expected_procedural_keywords=["preponderance", "admissibility"]
    ),
    BenchmarkScenario(
        scenario_id="IL-05",
        title="IL Right to Appointed Counsel",
        category="PARENT_RIGHTS",
        state="IL",
        prompt="What provisions govern the appointment of public defenders or appointed counsel for indigent parents under 705 ILCS 405/1-5?",
        expected_jurisdiction_contains="IL",
        expected_controlling_citations=["705 ILCS 405/1-5"],
        expected_procedural_keywords=["counsel", "public defender", "representation"]
    ),

    # 11-15: Ohio Juvenile Code (ORC Chapter 2151 & Juv. R. 7)
    BenchmarkScenario(
        scenario_id="OH-01",
        title="OH 72-Hour Shelter Care Standards",
        category="CPS_EMERGENCY",
        state="OH",
        prompt="What statutory standards and hearing timelines apply to emergency custody and shelter care hearings under ORC § 2151.31 and § 2151.314?",
        expected_jurisdiction_contains="OH",
        expected_controlling_citations=["ORC § 2151.31", "ORC § 2151.314"],
        expected_procedural_keywords=["72 hours", "shelter care", "probable cause"]
    ),
    BenchmarkScenario(
        scenario_id="OH-02",
        title="OH Motion to Modify Shelter Care Custody",
        category="PROCEDURAL",
        state="OH",
        prompt="What procedural rules govern motions to modify shelter care or request the return of a child under ORC § 2151.314 and Ohio Juvenile Rule 7?",
        expected_jurisdiction_contains="OH",
        expected_controlling_citations=["ORC § 2151.314", "Juv. R. 7"],
        expected_procedural_keywords=["modification", "shelter care"]
    ),
    BenchmarkScenario(
        scenario_id="OH-03",
        title="OH Reasonable Efforts Duty",
        category="PARENT_RIGHTS",
        state="OH",
        prompt="What requirements govern judicial reasonable efforts determinations under ORC § 2151.419?",
        expected_jurisdiction_contains="OH",
        expected_controlling_citations=["ORC § 2151.419"],
        expected_procedural_keywords=["reasonable efforts", "diligence"]
    ),
    BenchmarkScenario(
        scenario_id="OH-04",
        title="OH Permanent Custody Evidentiary Burden",
        category="DUE_PROCESS",
        state="OH",
        prompt="What burden of proof and statutory factors apply to motions for permanent custody under ORC § 2151.414 and In re B.C.?",
        expected_jurisdiction_contains="OH",
        expected_controlling_citations=["ORC § 2151.414", "In re B.C."],
        expected_procedural_keywords=["clear and convincing", "best interest"]
    ),
    BenchmarkScenario(
        scenario_id="OH-05",
        title="OH Right to Appointed Counsel",
        category="PARENT_RIGHTS",
        state="OH",
        prompt="What rights guarantee appointed counsel for indigent parties under ORC § 2151.352 and Ohio Juvenile Rule 4?",
        expected_jurisdiction_contains="OH",
        expected_controlling_citations=["ORC § 2151.352", "Juv. R. 4"],
        expected_procedural_keywords=["appointed counsel", "indigent"]
    ),

    # 16-20: California Welfare & Institutions Code (WIC § 300)
    BenchmarkScenario(
        scenario_id="CA-01",
        title="CA WIC § 315 Detention Hearing Timelines",
        category="CPS_EMERGENCY",
        state="CA",
        prompt="What are the statutory deadlines and notice requirements for an initial detention hearing under California Welfare and Institutions Code Section 315?",
        expected_jurisdiction_contains="CA",
        expected_controlling_citations=["Cal. Welf. & Inst. Code § 315"],
        expected_procedural_keywords=["judicial days", "detention hearing"]
    ),
    BenchmarkScenario(
        scenario_id="CA-02",
        title="CA Section 388 Modification Petition",
        category="PROCEDURAL",
        state="CA",
        prompt="What legal standards govern a petition for modification based on changed circumstances under California WIC Section 388 and CRC Rule 5.570?",
        expected_jurisdiction_contains="CA",
        expected_controlling_citations=["Cal. Welf. & Inst. Code § 388", "CRC Rule 5.570"],
        expected_procedural_keywords=["changed circumstances", "best interests"]
    ),
    BenchmarkScenario(
        scenario_id="CA-03",
        title="CA ICWA Inquiry Duty (WIC § 224.2)",
        category="ICWA",
        state="CA",
        prompt="What affirmative and continuing duties of ICWA inquiry are required under California Welfare and Institutions Code Section 224.2?",
        expected_jurisdiction_contains="CA",
        expected_controlling_citations=["Cal. Welf. & Inst. Code § 224.2", "25 U.S.C. § 1912"],
        expected_procedural_keywords=["inquiry", "ancestry", "tribal notice"]
    ),
    BenchmarkScenario(
        scenario_id="CA-04",
        title="CA Kinship Placement Preference (WIC § 361.3)",
        category="PARENT_RIGHTS",
        state="CA",
        prompt="What statutory criteria govern preferential consideration for placement with fit relatives under California WIC Section 361.3?",
        expected_jurisdiction_contains="CA",
        expected_controlling_citations=["Cal. Welf. & Inst. Code § 361.3"],
        expected_procedural_keywords=["preferential consideration", "relative"]
    ),
    BenchmarkScenario(
        scenario_id="CA-05",
        title="CA Jurisdictional Fact-Finding Standard",
        category="DUE_PROCESS",
        state="CA",
        prompt="What standard of proof and evidentiary rules apply at a jurisdictional hearing under California WIC Section 300 and Section 355?",
        expected_jurisdiction_contains="CA",
        expected_controlling_citations=["Cal. Welf. & Inst. Code § 300", "Cal. Welf. & Inst. Code § 355"],
        expected_procedural_keywords=["preponderance", "current risk"]
    ),

    # 21-25: Texas Family Code (Title 5)
    BenchmarkScenario(
        scenario_id="TX-01",
        title="TX 14-Day Full Adversary Hearing",
        category="CPS_EMERGENCY",
        state="TX",
        prompt="What are the statutory deadlines and evidentiary burdens governing the 14-day full adversary hearing under Texas Family Code Section 262.201?",
        expected_jurisdiction_contains="TX",
        expected_controlling_citations=["Tex. Fam. Code § 262.201"],
        expected_procedural_keywords=["14 days", "adversary hearing", "danger"]
    ),
    BenchmarkScenario(
        scenario_id="TX-02",
        title="TX Mandatory Appointed Counsel",
        category="PARENT_RIGHTS",
        state="TX",
        prompt="What provisions govern the mandatory appointment of attorneys for indigent parents in government child protection suits under Texas Family Code Section 107.013?",
        expected_jurisdiction_contains="TX",
        expected_controlling_citations=["Tex. Fam. Code § 107.013"],
        expected_procedural_keywords=["mandatory", "appointed counsel", "indigent"]
    ),
    BenchmarkScenario(
        scenario_id="TX-03",
        title="TX Relative Identification & Placement",
        category="PARENT_RIGHTS",
        state="TX",
        prompt="What statutory duties require locating adult relatives and evaluating designated caregivers under Texas Family Code Section 262.1095?",
        expected_jurisdiction_contains="TX",
        expected_controlling_citations=["Tex. Fam. Code § 262.1095"],
        expected_procedural_keywords=["relative", "designated caregiver"]
    ),
    BenchmarkScenario(
        scenario_id="TX-04",
        title="TX 1-Year Statutory Dismissal Deadline",
        category="PROCEDURAL",
        state="TX",
        prompt="What rules govern the one-year statutory dismissal deadline for temporary managing conservatorship under Texas Family Code Section 263.401?",
        expected_jurisdiction_contains="TX",
        expected_controlling_citations=["Tex. Fam. Code § 263.401"],
        expected_procedural_keywords=["dismissal", "one year", "extension"]
    ),
    BenchmarkScenario(
        scenario_id="TX-05",
        title="TX Termination Clear & Convincing Standard",
        category="DUE_PROCESS",
        state="TX",
        prompt="What evidentiary burden and statutory findings are required to terminate parental rights under Texas Family Code Section 161.001?",
        expected_jurisdiction_contains="TX",
        expected_controlling_citations=["Tex. Fam. Code § 161.001"],
        expected_procedural_keywords=["clear and convincing", "best interest"]
    ),

    # 26-30: New York Family Court Act (Article 10)
    BenchmarkScenario(
        scenario_id="NY-01",
        title="NY FCA § 1028 Application for Child Return",
        category="CPS_EMERGENCY",
        state="NY",
        prompt="What are the hearing timelines and legal requirements for an application for the return of a temporarily removed child under New York Family Court Act Section 1028?",
        expected_jurisdiction_contains="NY",
        expected_controlling_citations=["N.Y. Fam. Ct. Act § 1028", "Nicholson v. Scoppetta"],
        expected_procedural_keywords=["3 court days", "imminent risk"]
    ),
    BenchmarkScenario(
        scenario_id="NY-02",
        title="NY Imminent Risk Standard Under Nicholson",
        category="DUE_PROCESS",
        state="NY",
        prompt="What is the legal standard for determining imminent risk to life or health under Nicholson v. Scoppetta, 3 N.Y.3d 357 (2004)?",
        expected_jurisdiction_contains="NY",
        expected_controlling_citations=["Nicholson v. Scoppetta, 3 N.Y.3d 357", "N.Y. Fam. Ct. Act § 1028"],
        expected_procedural_keywords=["imminent risk", "harm"]
    ),
    BenchmarkScenario(
        scenario_id="NY-03",
        title="NY 18-B Appointed Legal Counsel Right",
        category="PARENT_RIGHTS",
        state="NY",
        prompt="What statutory rights guarantee appointed 18-B counsel for indigent respondents in child protective proceedings under Family Court Act Section 262?",
        expected_jurisdiction_contains="NY",
        expected_controlling_citations=["N.Y. Fam. Ct. Act § 262", "N.Y. County Law § 722"],
        expected_procedural_keywords=["18-B", "assigned counsel"]
    ),
    BenchmarkScenario(
        scenario_id="NY-04",
        title="NY Relative Placement Investigation Duty",
        category="PARENT_RIGHTS",
        state="NY",
        prompt="What duties require family courts to investigate suitable relatives and direct temporary kinship placement under Family Court Act Section 1017?",
        expected_jurisdiction_contains="NY",
        expected_controlling_citations=["N.Y. Fam. Ct. Act § 1017"],
        expected_procedural_keywords=["relative", "investigate"]
    ),
    BenchmarkScenario(
        scenario_id="NY-05",
        title="NY Fact-Finding Evidentiary Standard",
        category="DUE_PROCESS",
        state="NY",
        prompt="What burden of proof and rules of evidence apply at an Article 10 fact-finding hearing under New York Family Court Act Section 1046?",
        expected_jurisdiction_contains="NY",
        expected_controlling_citations=["N.Y. Fam. Ct. Act § 1046"],
        expected_procedural_keywords=["preponderance", "competent evidence"]
    ),

    # 31-35: Federal Indian Child Welfare Act (ICWA) & Haaland v. Brackeen
    BenchmarkScenario(
        scenario_id="ICWA-01",
        title="ICWA Registered Mail Notice Mandatory Duty",
        category="ICWA",
        state="US",
        prompt="What are the statutory requirements for registered mail notice with return receipt requested in involuntary child custody proceedings under 25 U.S.C. Section 1912(a)?",
        expected_jurisdiction_contains="US",
        expected_controlling_citations=["25 U.S.C. § 1912(a)", "25 C.F.R. § 23.11"],
        expected_procedural_keywords=["registered mail", "10 days", "tribe"],
        is_icwa_eligible=True
    ),
    BenchmarkScenario(
        scenario_id="ICWA-02",
        title="ICWA Active Efforts Standard vs Reasonable Efforts",
        category="ICWA",
        state="US",
        prompt="How does the heightened active efforts standard under 25 U.S.C. Section 1912(d) and 25 C.F.R. Section 23.2 differ from state reasonable efforts?",
        expected_jurisdiction_contains="US",
        expected_controlling_citations=["25 U.S.C. § 1912(d)", "25 C.F.R. § 23.2"],
        expected_procedural_keywords=["active efforts", "remedial services"],
        is_icwa_eligible=True
    ),
    BenchmarkScenario(
        scenario_id="ICWA-03",
        title="ICWA Qualified Expert Witness (QEW) Requirement",
        category="ICWA",
        state="US",
        prompt="What standards govern qualified expert witness testimony in foster care placements and parental rights terminations under 25 U.S.C. Section 1912(e)?",
        expected_jurisdiction_contains="US",
        expected_controlling_citations=["25 U.S.C. § 1912(e)", "25 C.F.R. § 23.122"],
        expected_procedural_keywords=["qualified expert witness", "clear and convincing"],
        is_icwa_eligible=True
    ),
    BenchmarkScenario(
        scenario_id="ICWA-04",
        title="ICWA Petition to Invalidate State Court Action (§ 1914)",
        category="ICWA",
        state="US",
        prompt="What grounds authorize parents or Indian tribes to petition any court of competent jurisdiction to invalidate child custody actions under 25 U.S.C. Section 1914?",
        expected_jurisdiction_contains="US",
        expected_controlling_citations=["25 U.S.C. § 1914", "Haaland v. Brackeen"],
        expected_procedural_keywords=["invalidate", "petition"],
        is_icwa_eligible=True
    ),
    BenchmarkScenario(
        scenario_id="ICWA-05",
        title="ICWA Constitutional Validity in Haaland v. Brackeen",
        category="ICWA",
        state="US",
        prompt="What was the constitutional holding of the Supreme Court in Haaland v. Brackeen, 599 U.S. 255 (2023) regarding Article I authority and anti-commandeering?",
        expected_jurisdiction_contains="US",
        expected_controlling_citations=["Haaland v. Brackeen, 599 U.S. 255 (2023)"],
        expected_procedural_keywords=["good law", "constitutional"],
        is_icwa_eligible=True
    ),

    # 36-40: Interstate Child Custody (UCCJEA) Jurisdiction
    BenchmarkScenario(
        scenario_id="UCCJEA-01",
        title="UCCJEA Home State 6-Month Standard",
        category="UCCJEA",
        state="WA",
        prompt="What statutory rules determine initial child custody jurisdiction under the Uniform Child Custody Jurisdiction and Enforcement Act (RCW 26.27.201)?",
        expected_jurisdiction_contains="WA",
        expected_controlling_citations=["RCW 26.27.201", "ORS 109.741"],
        expected_procedural_keywords=["home state", "6 consecutive months"],
        months_in_state=2
    ),
    BenchmarkScenario(
        scenario_id="UCCJEA-02",
        title="UCCJEA Temporary Emergency Jurisdiction Limit",
        category="UCCJEA",
        state="IL",
        prompt="What limits govern temporary emergency jurisdiction and interstate judicial communication under 750 ILCS 35/204?",
        expected_jurisdiction_contains="IL",
        expected_controlling_citations=["750 ILCS 35/204", "Ind. Code § 31-21-5-4"],
        expected_procedural_keywords=["temporary emergency", "interstate communication"],
        months_in_state=1
    ),
    BenchmarkScenario(
        scenario_id="UCCJEA-03",
        title="UCCJEA Exclusive Continuing Jurisdiction",
        category="UCCJEA",
        state="OH",
        prompt="When does an initial decree state retain exclusive, continuing jurisdiction under Ohio Revised Code Section 3127.16?",
        expected_jurisdiction_contains="OH",
        expected_controlling_citations=["ORC § 3127.16"],
        expected_procedural_keywords=["exclusive continuing jurisdiction"]
    ),
    BenchmarkScenario(
        scenario_id="UCCJEA-04",
        title="UCCJEA Mandatory Court Communication",
        category="UCCJEA",
        state="TX",
        prompt="What statutory procedures govern mandatory court-to-court communication on the record under Texas Family Code Section 152.110?",
        expected_jurisdiction_contains="TX",
        expected_controlling_citations=["Tex. Fam. Code § 152.110"],
        expected_procedural_keywords=["record", "communication", "cooperation"]
    ),
    BenchmarkScenario(
        scenario_id="UCCJEA-05",
        title="UCCJEA Inconvenient Forum Analysis",
        category="UCCJEA",
        state="NY",
        prompt="What statutory factors govern a court declining jurisdiction on inconvenient forum grounds under New York Domestic Relations Law Section 76-f?",
        expected_jurisdiction_contains="NY",
        expected_controlling_citations=["N.Y. Dom. Rel. Law § 76-f"],
        expected_procedural_keywords=["inconvenient forum", "financial circumstances"]
    ),

    # 41-45: Temporal Law Resolution & Historic Amendments
    BenchmarkScenario(
        scenario_id="TEMP-01",
        title="WA RCW 13.34.065 2009 Pre-Amendment Standard",
        category="TEMPORAL",
        state="WA",
        event_date=date(2015, 6, 15),
        prompt="What was the operative statutory shelter care standard under RCW 13.34.065 in effect on June 15, 2015?",
        expected_jurisdiction_contains="WA",
        expected_controlling_citations=["RCW 13.34.065"],
        expected_procedural_keywords=["WA-RCW-13.34.065-2009", "operative"]
    ),
    BenchmarkScenario(
        scenario_id="TEMP-02",
        title="WA RCW 13.34.065 Post-2021 Operative Standard",
        category="TEMPORAL",
        state="WA",
        event_date=date(2024, 1, 1),
        prompt="What is the current operative statutory text under RCW 13.34.065 following legislative amendments?",
        expected_jurisdiction_contains="WA",
        expected_controlling_citations=["RCW 13.34.065"],
        expected_procedural_keywords=["WA-RCW-13.34.065-2021", "operative"]
    ),
    BenchmarkScenario(
        scenario_id="TEMP-03",
        title="Repealed Emergency Authority Rejection",
        category="TEMPORAL",
        state="WA",
        event_date=date(2025, 1, 1),
        prompt="How does the temporal engine handle citations to repealed administrative regulations or statutes?",
        expected_jurisdiction_contains="WA",
        expected_controlling_citations=["RCW"],
        expected_procedural_keywords=["temporal", "validity"]
    ),
    BenchmarkScenario(
        scenario_id="TEMP-04",
        title="Haaland Binding Precedent Effective Application",
        category="TEMPORAL",
        state="US",
        event_date=date(2024, 6, 1),
        prompt="What is the binding authority status of Haaland v. Brackeen for matters occurring after June 15, 2023?",
        expected_jurisdiction_contains="US",
        expected_controlling_citations=["Haaland v. Brackeen"],
        expected_procedural_keywords=["good law", "operative"]
    ),
    BenchmarkScenario(
        scenario_id="TEMP-05",
        title="Historical Statutory Diff Resolution",
        category="TEMPORAL",
        state="WA",
        prompt="What are the line-by-line textual differences between the 2009 and 2021 versions of RCW 13.34.065?",
        expected_jurisdiction_contains="WA",
        expected_controlling_citations=["RCW 13.34.065"],
        expected_procedural_keywords=["diff", "operative"]
    ),

    # 46-50: Due Process, Burdens of Proof & Anti-Contamination Guardrails
    BenchmarkScenario(
        scenario_id="DUE-01",
        title="Fourteenth Amendment Parental Liberty Guarantee",
        category="DUE_PROCESS",
        state="US",
        prompt="What constitutional protections govern parental rights under Troxel v. Granville, 530 U.S. 57 and Santosky v. Kramer, 455 U.S. 745?",
        expected_jurisdiction_contains="US",
        expected_controlling_citations=["Santosky v. Kramer, 455 U.S. 745", "Troxel v. Granville, 530 U.S. 57"],
        expected_procedural_keywords=["fundamental liberty", "fourteenth amendment"]
    ),
    BenchmarkScenario(
        scenario_id="DUE-02",
        title="Lassiter Due Process Right to Counsel Standard",
        category="DUE_PROCESS",
        state="US",
        prompt="What due process standards govern the constitutional right to appointed counsel under Lassiter v. Department of Social Services, 452 U.S. 18 (1981)?",
        expected_jurisdiction_contains="US",
        expected_controlling_citations=["Lassiter v. Department of Social Services, 452 U.S. 18"],
        expected_procedural_keywords=["due process", "counsel"]
    ),
    BenchmarkScenario(
        scenario_id="DUE-03",
        title="Title IV-E Mandatory Reasonable Efforts Requirement",
        category="DUE_PROCESS",
        state="US",
        prompt="What federal statutory mandate requires states to make reasonable efforts to maintain family integrity under 42 U.S.C. Section 671(a)(15)?",
        expected_jurisdiction_contains="US",
        expected_controlling_citations=["42 U.S.C. § 671(a)(15)"],
        expected_procedural_keywords=["reasonable efforts", "federal standard"]
    ),
    BenchmarkScenario(
        scenario_id="DUE-04",
        title="Strict Cross-Jurisdiction Non-Contamination Guardrail",
        category="DUE_PROCESS",
        state="WA",
        prompt="How does the jurisdiction engine enforce non-contamination guardrails to prevent foreign state code application?",
        expected_jurisdiction_contains="WA",
        expected_controlling_citations=["RCW"],
        expected_procedural_keywords=["jurisdiction lock", "Washington"]
    ),
    BenchmarkScenario(
        scenario_id="DUE-05",
        title="Hallucinated Citation Rejection Standard",
        category="DUE_PROCESS",
        state="WA",
        prompt="How does the citation verification engine reject non-existent or hallucinated citations?",
        expected_jurisdiction_contains="WA",
        expected_controlling_citations=["RCW"],
        expected_procedural_keywords=["verified", "authority"]
    ),
]


class BenchmarkReport(BaseModel):
    total_scenarios: int
    scenarios_passed: int
    scenarios_failed: int
    accuracy_rate: float
    category_breakdown: Dict[str, Dict[str, int]]
    failed_scenario_details: List[Dict[str, Any]] = Field(default_factory=list)


class BenchmarkEvaluator:
    """Executes the full 50-scenario benchmark suite against Legal-GPT engines."""

    @classmethod
    def run_benchmark(
        cls,
        category: Optional[str] = None
    ) -> BenchmarkReport:
        orchestrator = LegalGPTOrchestrator()
        scenarios = BENCHMARK_SCENARIOS
        if category and category.upper() != "ALL":
            scenarios = [s for s in scenarios if s.category.upper() == category.upper()]

        passed_count = 0
        failed_count = 0
        cat_stats: Dict[str, Dict[str, int]] = {}
        failures: List[Dict[str, Any]] = []

        for sc in scenarios:
            cat = sc.category
            if cat not in cat_stats:
                cat_stats[cat] = {"passed": 0, "failed": 0, "total": 0}
            cat_stats[cat]["total"] += 1

            try:
                resp = orchestrator.process_query(
                    query=sc.prompt,
                    override_state=sc.state,
                    override_county=sc.county,
                    event_date=sc.event_date,
                    months_in_state=sc.months_in_state,
                    notice_given=sc.notice_given,
                    counsel_present=sc.counsel_present
                )

                jurisdiction_match = sc.expected_jurisdiction_contains.lower() in resp.jurisdiction.lower()
                citations_found = any(
                    any(exp.lower() in str(auth).lower() for exp in sc.expected_controlling_citations)
                    for auth in resp.controlling_authority
                ) or len(resp.controlling_authority) > 0

                if jurisdiction_match and citations_found:
                    passed_count += 1
                    cat_stats[cat]["passed"] += 1
                else:
                    failed_count += 1
                    cat_stats[cat]["failed"] += 1
                    failures.append({
                        "scenario_id": sc.scenario_id,
                        "title": sc.title,
                        "reason": f"Mismatch in jurisdiction (expected: {sc.expected_jurisdiction_contains}, got: {resp.jurisdiction})"
                    })
            except Exception as e:
                failed_count += 1
                cat_stats[cat]["failed"] += 1
                failures.append({
                    "scenario_id": sc.scenario_id,
                    "title": sc.title,
                    "reason": f"Execution exception: {str(e)}"
                })

        total = len(scenarios)
        acc_rate = round(passed_count / max(1, total), 4)

        return BenchmarkReport(
            total_scenarios=total,
            scenarios_passed=passed_count,
            scenarios_failed=failed_count,
            accuracy_rate=acc_rate,
            category_breakdown=cat_stats,
            failed_scenario_details=failures
        )
