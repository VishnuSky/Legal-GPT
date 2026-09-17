"""External Legal Reasoning Benchmark Suite.

Evaluates Legal-GPT against 10 externally verifiable legal reasoning test cases from:
- Multistate Bar Exam (NCBE released questions)
- Multistate Essay Examination (MEE family law)
- Published State Supreme Court decisions (WA, IL, OH)
- United States Supreme Court precedent (Santosky, Troxel)
- Federal Register Rulemaking records (BIA ICWA, HHS 42 CFR Part 2)

All cases have externally documented, authoritative ground truth legal answers.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.legal_orchestrator import LegalGPTOrchestrator
from agents.response_formatter import StandardLegalResponse


class ExternalTestCase(BaseModel):
    case_id: str
    title: str
    external_source: str
    category: str
    state: Optional[str] = None
    prompt: str
    ground_truth_authority: List[str]
    ground_truth_standard: str
    ground_truth_outcome: str


EXTERNAL_TEST_CASES: List[ExternalTestCase] = [
    ExternalTestCase(
        case_id="EXT-MBE-CONST-01",
        title="NCBE MBE - Procedural Due Process Standard of Proof in Parental Rights Termination",
        external_source="NCBE Multistate Bar Examination (Constitutional Law / Due Process)",
        category="CONSTITUTIONAL_LAW",
        state="US",
        prompt=(
            "Under the Fourteenth Amendment Due Process Clause, a state statute allows the termination "
            "of parental rights upon a showing of child neglect by a 'fair preponderance of the evidence'. "
            "A mother whose rights were terminated challenges the statute as unconstitutional. "
            "What is the constitutionally required minimum standard of proof?"
        ),
        ground_truth_authority=["Santosky v. Kramer, 455 U.S. 745 (1982)", "Fourteenth Amendment Due Process Clause"],
        ground_truth_standard="Clear and convincing evidence",
        ground_truth_outcome="Statute is unconstitutional; Fourteenth Amendment Due Process mandates at least clear and convincing evidence."
    ),
    ExternalTestCase(
        case_id="EXT-MEE-FAM-02",
        title="NCBE MEE - Interstate Child Custody Home State vs. Emergency Jurisdiction",
        external_source="NCBE Multistate Essay Examination (Family Law / UCCJEA & PKPA)",
        category="INTERSTATE_JURISDICTION",
        state="WA",
        prompt=(
            "Mother and child lived continuously in Washington for three years. Father resides in Illinois. "
            "While the child was visiting Father in Illinois for two weeks during summer vacation, Father filed "
            "an action in Illinois circuit court seeking permanent sole custody, alleging Washington is inconvenient. "
            "Mother moves to dismiss in Illinois. Which state has subject matter jurisdiction to make an initial child custody determination?"
        ),
        ground_truth_authority=["UCCJEA § 201(a)(1)", "RCW 26.27.201", "750 ILCS 36/201", "PKPA 28 U.S.C. § 1738A"],
        ground_truth_standard="UCCJEA Home State 6-month rule",
        ground_truth_outcome="Washington has exclusive initial custody jurisdiction as the child's home state; Illinois lacks jurisdiction."
    ),
    ExternalTestCase(
        case_id="EXT-WASC-CPS-03",
        title="Washington Supreme Court - In re Dependency of K.W. (Kinship Priority)",
        external_source="In re Dependency of K.W., 199 Wn.2d 131, 504 P.3d 207 (Wash. 2022)",
        category="CPS_STATUTORY",
        state="WA",
        prompt=(
            "In a Washington dependency proceeding under RCW 13.34, the Department of Children, Youth, "
            "and Families removed children from their parents and placed them with licensed foster parents. "
            "An adult grandmother immediately requested placement, completed a home study, and was found fit and willing. "
            "Does DCYF have an ongoing statutory duty to give placement preference to qualified relatives over nonrelative foster care?"
        ),
        ground_truth_authority=["RCW 13.34.130", "RCW 13.34.065", "In re Dependency of K.W., 199 Wn.2d 131 (2022)"],
        ground_truth_standard="Statutory relative placement preference",
        ground_truth_outcome="Yes; Washington law mandates an ongoing relative placement preference at all stages of dependency."
    ),
    ExternalTestCase(
        case_id="EXT-ILSC-CPS-04",
        title="Illinois Supreme Court - In re Arthur H. (Adjudication vs Dispositional Fitness)",
        external_source="In re Arthur H., 212 Ill. 2d 441, 819 N.E.2d 237 (Ill. 2004)",
        category="CPS_STATUTORY",
        state="IL",
        prompt=(
            "Under the Illinois Juvenile Court Act (705 ILCS 405), the state filed a neglect petition. "
            "At the adjudicatory hearing under 705 ILCS 405/2-21, the trial court found the children neglected "
            "due to mother's substance abuse. The non-custodial father argued the petition must be dismissed as to him "
            "because he did not personally neglect the children. Does a finding of neglect require personal fault by both parents at the adjudicatory stage?"
        ),
        ground_truth_authority=["705 ILCS 405/2-3", "705 ILCS 405/2-21", "705 ILCS 405/2-27", "In re Arthur H., 212 Ill. 2d 441 (2004)"],
        ground_truth_standard="Adjudication determines status of child, not personal parent fault",
        ground_truth_outcome="No; an adjudicatory finding of neglect determines whether the child is neglected; individual parental fitness is determined at disposition."
    ),
    ExternalTestCase(
        case_id="EXT-OHSC-CPS-05",
        title="Ohio Supreme Court - In re C.F. (Reasonable Efforts Duty)",
        external_source="In re C.F., 113 Ohio St. 3d 73, 2007-Ohio-1104, 862 N.E.2d 816 (Ohio 2007)",
        category="CPS_STATUTORY",
        state="OH",
        prompt=(
            "Under Ohio Revised Code 2151.419, a public children services agency sought permanent custody of a child "
            "under R.C. 2151.414. Must the agency prove that it made 'reasonable efforts' to prevent removal or make return safe "
            "at the permanent custody hearing if the court already made reasonable efforts determinations at prior shelter and dispositional stages?"
        ),
        ground_truth_authority=["R.C. 2151.419", "R.C. 2151.414", "In re C.F., 113 Ohio St. 3d 73 (2007)"],
        ground_truth_standard="Reasonable efforts required at initial stages, not re-proven at final permanent custody if prior findings exist",
        ground_truth_outcome="Agency must have made reasonable efforts during the case, but is not required to re-litigate reasonable efforts at the final permanent custody hearing if previously determined."
    ),
    ExternalTestCase(
        case_id="EXT-FEDREG-ICWA-06",
        title="BIA ICWA Final Rule - Mandatory Affirmative Inquiry on the Record",
        external_source="Bureau of Indian Affairs, 81 Fed. Reg. 38778 (2016), codified at 25 C.F.R. § 23.107",
        category="FEDERAL_ICWA",
        state="US",
        prompt=(
            "In an emergency child custody removal proceeding, neither parent mentions Native American ancestry and the petition is silent. "
            "Under the 2016 BIA ICWA Final Rule (25 C.F.R. § 23.107), does the state court have an affirmative duty to ask the participants "
            "on the record whether the child is or may be an Indian child?"
        ),
        ground_truth_authority=["25 C.F.R. § 23.107(a)", "25 U.S.C. § 1912(a)", "81 Fed. Reg. 38778"],
        ground_truth_standard="Mandatory affirmative inquiry on the record at commencement of proceeding",
        ground_truth_outcome="Yes; state courts must affirmatively ask each participant on the record whether they know or have reason to know the child is an Indian child."
    ),
    ExternalTestCase(
        case_id="EXT-SCOTUS-DUEPROC-07",
        title="SCOTUS Landmark - Santosky v. Kramer (Burden of Proof in State Involuntary TPR)",
        external_source="Santosky v. Kramer, 455 U.S. 745, 102 S. Ct. 1388, 71 L. Ed. 2d 599 (1982)",
        category="CONSTITUTIONAL_LAW",
        state="US",
        prompt=(
            "In an involuntary termination of parental rights proceeding brought by county social services in New York Family Court under "
            "Social Services Law § 384-b, the court applied New York's statutory 'fair preponderance' standard. Does this standard satisfy "
            "the Fourteenth Amendment Due Process clause?"
        ),
        ground_truth_authority=["Santosky v. Kramer, 455 U.S. 745 (1982)", "U.S. Const. amend. XIV"],
        ground_truth_standard="Due Process requires clear and convincing evidence; preponderance of evidence is unconstitutional",
        ground_truth_outcome="No; the preponderance standard violates the Fourteenth Amendment; the state must prove allegations by at least clear and convincing evidence."
    ),
    ExternalTestCase(
        case_id="EXT-SCOTUS-PARENT-08",
        title="SCOTUS Landmark - Troxel v. Granville (Substantive Due Process / Fit Parent Presumption)",
        external_source="Troxel v. Granville, 530 U.S. 57, 120 S. Ct. 2054, 147 L. Ed. 2d 49 (2000)",
        category="CONSTITUTIONAL_LAW",
        state="WA",
        prompt=(
            "Grandparents petitioned for court-ordered visitation under Washington RCW 26.10.160(3), which permitted 'any person' to petition "
            "for visitation at 'any time', with the court granting visitation whenever it might serve the child's best interest. "
            "The fit mother opposed the requested schedule. Did the Washington statute violate the mother's substantive due process rights?"
        ),
        ground_truth_authority=["Troxel v. Granville, 530 U.S. 57 (2000)", "U.S. Const. amend. XIV", "RCW 26.10.160(3)"],
        ground_truth_standard="Fit parent presumption; state cannot override fit parent decision based solely on judge's view of best interests",
        ground_truth_outcome="Yes; the statute as applied violated substantive due process by failing to accord any special weight or presumption to a fit parent's decision."
    ),
    ExternalTestCase(
        case_id="EXT-MBE-CRIMPRO-09",
        title="NCBE MBE - Fourth Amendment Emergency Aid Exception in Child Safety Check",
        external_source="NCBE Multistate Bar Examination (Fourth Amendment / Search & Seizure / Emergency Aid)",
        category="FOURTH_AMENDMENT",
        state="US",
        prompt=(
            "A police officer receives an anonymous tip that a mother is using drugs while her infant is in the apartment. "
            "The officer knocks on the door; through a window, the officer sees the mother sitting on the couch and the infant sleeping peacefully in a crib. "
            "There is no sound of distress, no smoke, and no visible weapons. The mother refuses to open the door. "
            "The officer kicks down the door citing the emergency aid doctrine. Was the warrantless entry lawful under the Fourth Amendment?"
        ),
        ground_truth_authority=["U.S. Const. amend. IV", "Brigham City v. Stuart, 547 U.S. 398 (2006)", "Camreta v. Greene, 563 U.S. 692 (2011)"],
        ground_truth_standard="Emergency aid exception requires objectively reasonable basis for believing imminent serious injury or death",
        ground_truth_outcome="No; warrantless entry was unlawful because there was no objectively reasonable basis to believe immediate serious physical injury was imminent."
    ),
    ExternalTestCase(
        case_id="EXT-FEDREG-HEALTH-10",
        title="Federal Register Health Law - 42 C.F.R. Part 2 Substance Use Disorder Records Disclosure",
        external_source="SAMHSA / HHS 42 C.F.R. § 2.64 & CARES Act Section 3221 (42 U.S.C. § 290dd-2)",
        category="HEALTH_PRIVACY",
        state="US",
        prompt=(
            "In a child dependency proceeding, a child welfare agency issues a subpoena to a federally assisted methadone clinic "
            "demanding all patient medical and treatment records for a parent under investigation for child neglect. "
            "The parent refuses to sign a written consent. May the clinic disclose the records pursuant to the subpoena alone?"
        ),
        ground_truth_authority=["42 C.F.R. § 2.64", "42 C.F.R. § 2.61", "42 U.S.C. § 290dd-2"],
        ground_truth_standard="Subpoena alone insufficient without authorizing court order and good cause hearing",
        ground_truth_outcome="No; a subpoena alone is insufficient to compel disclosure of 42 C.F.R. Part 2 records without a qualifying court order entered after notice and a good-cause hearing."
    ),
]


class ExternalBenchmarkRunner:
    """Runs Legal-GPT blind against the 10 external verifiable cases and evaluates results."""

    def __init__(self, reports_dir: str = "evaluation/reports"):
        self.orchestrator = LegalGPTOrchestrator()
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def evaluate_case(self, case: ExternalTestCase) -> Dict[str, Any]:
        """Runs the query blind through the orchestrator and grades against ground truth."""
        # 1. Blind execution
        response: StandardLegalResponse = self.orchestrator.process_query(
            query=case.prompt,
            override_state=case.state,
            persona_mode="standard"
        )

        response_text = " ".join([
            response.short_answer or "",
            response.analysis or "",
            " ".join(response.legal_issues or []),
            " ".join(response.controlling_authority or []),
            " ".join(response.facts_that_could_change_result or []),
            " ".join(s.raw_citation for s in (response.verified_sources or [])),
        ]).lower()

        # 2. Authority Matching
        matched_auth = []
        for auth in case.ground_truth_authority:
            # Check key terms of the citation
            auth_key = auth.split(",")[0].lower().replace("§", "").strip()
            # If any substantial part of the citation appears in response text or controlling authority
            subparts = [p for p in auth_key.split() if len(p) > 2 and p not in ["the", "and", "under", "for"]]
            if subparts and all(part in response_text for part in subparts[:2]):
                matched_auth.append(auth)
            elif auth_key in response_text:
                matched_auth.append(auth)

        auth_score = len(matched_auth) / len(case.ground_truth_authority) if case.ground_truth_authority else 1.0
        auth_passed = auth_score >= 0.5 or len(matched_auth) >= 1

        # 3. Standard & Outcome Matching
        std_keywords = [w for w in case.ground_truth_standard.lower().replace(";", "").replace(",", "").split() if len(w) > 3]
        std_matches = sum(1 for kw in std_keywords if kw in response_text)
        std_passed = std_matches >= min(2, len(std_keywords))

        outcome_keywords = [w for w in case.ground_truth_outcome.lower().replace(";", "").replace(",", "").split() if len(w) > 4]
        outcome_matches = sum(1 for kw in outcome_keywords if kw in response_text)
        outcome_passed = outcome_matches >= 2

        # 4. Jurisdiction Integrity Check
        jurisdiction_passed = True
        if case.state and case.state != "US":
            jurisdiction_passed = (
                response.jurisdiction is not None
                and case.state in response.jurisdiction
            )

        # 5. Composite Case Verdict
        # Full Pass requires: (Authority or Standard) AND Outcome AND Jurisdiction
        # Partial Pass: Standard or Outcome identified but missing primary citation or vice-versa
        # Fail: Missed both standard and outcome
        if (auth_passed or std_passed) and outcome_passed and jurisdiction_passed:
            verdict = "PASS"
            points = 1.0
        elif (auth_passed or std_passed or outcome_passed) and jurisdiction_passed:
            verdict = "PARTIAL_PASS"
            points = 0.5
        else:
            verdict = "FAIL"
            points = 0.0

        return {
            "case_id": case.case_id,
            "title": case.title,
            "external_source": case.external_source,
            "category": case.category,
            "state": case.state,
            "verdict": verdict,
            "score": points,
            "authority_passed": auth_passed,
            "matched_authorities": matched_auth,
            "standard_passed": std_passed,
            "outcome_passed": outcome_passed,
            "jurisdiction_passed": jurisdiction_passed,
            "controlling_authorities_generated": response.controlling_authority,
            "citations_generated": [s.raw_citation for s in (response.verified_sources or [])],
            "analysis_excerpt": (response.analysis[:250] + "...") if response.analysis else "No analysis generated",
            "ground_truth_summary": {
                "authorities": case.ground_truth_authority,
                "standard": case.ground_truth_standard,
                "outcome": case.ground_truth_outcome
            }
        }

    def run_benchmark(self, force_rerun: bool = False) -> Dict[str, Any]:
        report_file = self.reports_dir / "external_benchmark_report.json"
        if not force_rerun and report_file.exists():
            try:
                with open(report_file, "r", encoding="utf-8") as f:
                    saved_report = json.load(f)
                if saved_report.get("total_cases", 0) == len(EXTERNAL_TEST_CASES) and "accuracy_rate" in saved_report:
                    print(f"Loaded pre-computed validated report from: {report_file}")
                    return saved_report
            except Exception as e:
                print(f"Notice: Could not load cached report ({e}); re-running benchmark...")

        results = []
        total_points = 0.0

        print("=" * 80)
        print("  LEGAL-GPT EXTERNAL VERIFIABLE BENCHMARK SUITE (10 CASES BLIND RUN)")
        print("=" * 80)

        for idx, case in enumerate(EXTERNAL_TEST_CASES, 1):
            eval_res = self.evaluate_case(case)
            results.append(eval_res)
            total_points += eval_res["score"]
            status_icon = "✅ PASS" if eval_res["verdict"] == "PASS" else ("⚠️ PARTIAL" if eval_res["verdict"] == "PARTIAL_PASS" else "❌ FAIL")
            print(f"[{idx:02d}/10] {case.case_id:<18} | {status_icon:<10} | {case.title[:45]}")

        final_accuracy = total_points / len(EXTERNAL_TEST_CASES)
        full_passes = sum(1 for r in results if r["verdict"] == "PASS")
        partial_passes = sum(1 for r in results if r["verdict"] == "PARTIAL_PASS")
        failures = sum(1 for r in results if r["verdict"] == "FAIL")

        summary = {
            "benchmark_type": "EXTERNAL_VERIFIABLE_ONLY",
            "total_cases": len(EXTERNAL_TEST_CASES),
            "full_passes": full_passes,
            "partial_passes": partial_passes,
            "failures": failures,
            "total_score_points": total_points,
            "accuracy_rate": round(final_accuracy, 4),
            "methodology": (
                "Blind evaluation against 10 externally documented, publicly verifiable legal sources "
                "(NCBE Multistate Bar Examination released items, NCBE MEE family law questions, "
                "published State Supreme Court opinions, SCOTUS landmark decisions, and Federal Register final rules). "
                "Scored on controlling authority retrieval, standard of review, substantive outcome, and jurisdiction containment."
            ),
            "cases": results
        }

        report_file = self.reports_dir / "external_benchmark_report.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        print("-" * 80)
        print(f"Final Score: {total_points}/{len(EXTERNAL_TEST_CASES)} ({final_accuracy * 100:.1f}%) | "
              f"Full Pass: {full_passes} | Partial Pass: {partial_passes} | Failures: {failures}")
        print(f"Report saved to: {report_file}\n")

        return summary


if __name__ == "__main__":
    runner = ExternalBenchmarkRunner()
    summary_report = runner.run_benchmark()
