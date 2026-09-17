"""Canonical procedural pathway definitions for CPS, Administrative, Criminal, and Civil tracks."""

from typing import Dict, List
from core.procedure.models import LegalTrack, StageDefinition


ALL_STAGES: List[StageDefinition] = [
    # ==========================================
    # 1. CPS / CHILD WELFARE DEPENDENCY TRACK
    # ==========================================
    StageDefinition(
        stage_id="CPS_INVESTIGATION",
        track=LegalTrack.CPS_DEPENDENCY,
        stage_name="CPS Investigation / Family Assessment",
        order=1,
        description="Child welfare agency investigates report of alleged child abuse or neglect, conducts home assessment, or interviews family members.",
        governing_authority=[
            "CAPTA 42 U.S.C. § 5106a",
            "RCW 26.44.030 / RCW 26.44.050 (WA)",
            "325 ILCS 5/7.4 (IL)",
            "ORC § 2151.421 (OH)"
        ],
        possible_next_stages=["CPS_REMOVAL", "DEPENDENCY_PETITION", "CASE_CLOSURE_UNFOUNDED"],
        statutory_deadlines=[
            "Agency must complete initial investigation within 30 to 60 days of intake report",
            "Emergency referral response required within 24 hours (or immediate 2 hours for imminent danger)"
        ],
        notice_requirements=[
            "Caseworker must inform parent of allegations and purpose of interview upon initial contact",
            "Written notice of investigation rights and pamphlet"
        ],
        hearing_opportunities=[
            "No formal court hearing at this initial stage unless agency files an ex parte motion or search order"
        ],
        decision_makers=["CPS Caseworker", "Child Welfare Investigative Supervisor", "Law Enforcement Liaison"],
        review_mechanisms=[
            "Request administrative supervisory review of investigative conduct",
            "File complaint with state Office of the Family and Children's Ombuds (OFCO / DCFS Ombudsman)"
        ],
        critical_documents_to_locate=[
            "Initial intake intake summary / screening narrative",
            "Written Notice of Investigation Rights provided by caseworker",
            "Medical, school, or police incident reports referenced by worker"
        ],
        questions_to_ask=[
            "What specific allegations or safety threats were reported?",
            "Is this an alternative response / family assessment or a formal child abuse investigation?",
            "Are you requesting voluntary cooperation or do you have a court order / warrant?"
        ],
        required_factual_predicates=["Report made to child abuse hotline", "Caseworker contact with family"],
        unknown_facts_to_investigate=[
            "Did the caseworker obtain a judicial warrant or court order to enter the home?",
            "Has the agency classified the matter as an emergency or non-emergency?"
        ]
    ),

    StageDefinition(
        stage_id="CPS_REMOVAL",
        track=LegalTrack.CPS_DEPENDENCY,
        stage_name="Emergency Removal / Protective Custody",
        order=2,
        description="Child is taken into state protective custody by law enforcement or child welfare worker without prior contested court hearing.",
        governing_authority=[
            "U.S. Const. amend. IV & XIV (Due Process & Warrant Requirement; Doe v. Heck)",
            "RCW 13.34.050 / RCW 26.44.050 (WA)",
            "705 ILCS 405/2-8 & 405/2-9 (IL)",
            "Fla. Stat. § 39.401 (FL)",
            "Tex. Fam. Code § 262.104 (TX)"
        ],
        possible_next_stages=["SHELTER_HEARING", "VOLUNTARY_RETURN"],
        statutory_deadlines=[
            "Strict Post-Removal Hearing Clocks:",
            "WA: Shelter hearing within 72 hours (excluding weekends and court holidays) per RCW 13.34.065",
            "IL: Temporary custody hearing within 48 hours (excluding weekends and court holidays) per 705 ILCS 405/2-9",
            "FL: Shelter hearing within 24 hours of removal per Fla. Stat. § 39.402",
            "TX: Full adversary hearing within 14 days per Tex. Fam. Code § 262.201"
        ],
        notice_requirements=[
            "Immediate written notice of removal given to parents including grounds and time/location of shelter hearing",
            "Notice of parent's right to court-appointed counsel and right to phone contact"
        ],
        hearing_opportunities=[
            "Immediate emergency shelter / preliminary detention hearing before a juvenile court judge or commissioner"
        ],
        decision_makers=["Law Enforcement Officer", "Child Protective Specialist", "Ex Parte Judicial Officer"],
        review_mechanisms=[
            "Emergency Motion for Immediate Return / Release of Child",
            "Demand for formal judicial hearing within statutory hour clock",
            "Affidavit for Rehearing under state court rules (e.g. WA JuCR 2.4)"
        ],
        critical_documents_to_locate=[
            "Written Notice of Removal / Temporary Custody Receipt",
            "Law enforcement police report or emergency intake declaration",
            "Affidavit of Exigent Circumstances or ex parte removal order (if signed by judge)"
        ],
        questions_to_ask=[
            "What judge signed the removal order, or was this a warrantless removal?",
            "What is the exact date, time, and courtroom for the emergency shelter care hearing?",
            "Have you notified the public defender or court clerk to appoint my attorney?"
        ],
        required_factual_predicates=["Child physically removed from parental custody", "Child placed in foster care or shelter"],
        unknown_facts_to_investigate=[
            "Did genuine exigent circumstances (imminent physical bodily peril) exist at the moment of entry?",
            "Were capable adult relatives / grandparents offered immediate kinship placement?"
        ]
    ),

    StageDefinition(
        stage_id="SHELTER_HEARING",
        track=LegalTrack.CPS_DEPENDENCY,
        stage_name="Shelter Care Hearing / Temporary Custody Hearing",
        order=3,
        description="First contested court appearance following emergency removal where judge evaluates initial detention and temporary placement.",
        governing_authority=[
            "RCW 13.34.065 (WA)",
            "705 ILCS 405/2-9 (IL)",
            "Fla. Stat. § 39.402 (FL)",
            "ORC § 2151.314 (OH)"
        ],
        possible_next_stages=["DEPENDENCY_PETITION", "PRE_TRIAL_CONFERENCE", "RETURN_HOME_WITH_SUPERVISION"],
        statutory_deadlines=[
            "Hearing held within 24 - 72 hours of removal (state-specific)",
            "30-day relative placement notice deadline under 42 U.S.C. § 671(a)(29)"
        ],
        notice_requirements=[
            "Formal written summons and copy of dependency petition served on parents before or at hearing",
            "Oral advisement of constitutional and statutory rights by presiding judge"
        ],
        hearing_opportunities=[
            "Contested preliminary hearing: parent has right to testify, cross-examine caseworker, and present relative caregivers"
        ],
        decision_makers=["Superior Court Judge", "Juvenile Court Commissioner", "Family Court Referee"],
        review_mechanisms=[
            "Motion for Rehearing within 72 hours upon parent affidavit of changed circumstances (e.g. JuCR 2.4)",
            "Interlocutory revision of commissioner's ruling before presiding Superior Court judge"
        ],
        critical_documents_to_locate=[
            "Dependency Petition / Initial Complaint",
            "Caseworker's Sworn Declaration / Affidavit in Support of Shelter Care",
            "Shelter Care Hearing Order / Temporary Custody Minute Order"
        ],
        questions_to_ask=[
            "Has an attorney been appointed to represent me today?",
            "What specific safety risks did the agency claim justify out-of-home placement rather than an in-home safety plan?",
            "When is the next court date and what is my visitation schedule?"
        ],
        required_factual_predicates=["Child in state custody", "First court appearance scheduled or held"],
        unknown_facts_to_investigate=[
            "Did the judge establish a minimum visitation schedule on the court record?",
            "Were reasonable efforts made to prevent the need for removal?"
        ]
    ),

    StageDefinition(
        stage_id="DEPENDENCY_PETITION",
        track=LegalTrack.CPS_DEPENDENCY,
        stage_name="Dependency Petition & Initial Plea / Settlement Conference",
        order=4,
        description="Formal petition filed by state agency detailing statutory grounds of abuse, neglect, or abandonment.",
        governing_authority=[
            "RCW 13.34.040 / RCW 13.34.070 (WA)",
            "705 ILCS 405/2-13 (IL)",
            "ORC § 2151.27 (OH)"
        ],
        possible_next_stages=["ADJUDICATION", "AGREED_ORDER_OF_DEPENDENCY"],
        statutory_deadlines=[
            "Fact-finding hearing (adjudication) must typically occur within 60 to 90 days of petition filing"
        ],
        notice_requirements=[
            "Personal service of petition and summons at least 5 to 14 days before fact-finding",
            "Notice by certified mail or publication if parent location is unknown despite diligent search"
        ],
        hearing_opportunities=[
            "Pretrial status conference, plea entry, mediation, or settlement conference"
        ],
        decision_makers=["Juvenile Court Judge", "Assistant Attorney General (AAG) / County State's Attorney"],
        review_mechanisms=[
            "Motion to Dismiss Petition for failure to state a statutory claim under court rules (Rule 12(b)(6) equivalent)",
            "Motion for Bill of Particulars / More Definite Statement"
        ],
        critical_documents_to_locate=[
            "Formal Dependency Petition with statutory citations",
            "Affidavit of Service of Summons",
            "Pretrial Order setting Fact-Finding / Adjudication trial date"
        ],
        questions_to_ask=[
            "Which exact statutory definitions under state law does the petition allege?",
            "What is the deadline for my attorney to file formal discovery requests?",
            "Is there an agreed safety plan or mediation option that avoids an adjudication finding?"
        ],
        required_factual_predicates=["Formal petition filed with clerk of juvenile court"],
        unknown_facts_to_investigate=[
            "Were all named parents and legal custodians formally served with summons?",
            "Has the child's Indian heritage / ICWA eligibility been formally inquired on the record?"
        ]
    ),

    StageDefinition(
        stage_id="ADJUDICATION",
        track=LegalTrack.CPS_DEPENDENCY,
        stage_name="Adjudication Hearing / Fact-Finding Trial",
        order=5,
        description="Contested trial where the State bears the burden of proving that the child meets the statutory definition of dependent or abused.",
        governing_authority=[
            "RCW 13.34.110 (WA)",
            "705 ILCS 405/2-18 / 2-21 (IL)",
            "ORC § 2151.35 (OH)",
            "Santosky v. Kramer, 455 U.S. 745 (1982)"
        ],
        possible_next_stages=["DISPOSITION", "DISMISSAL_OF_PETITION"],
        statutory_deadlines=[
            "Must be completed within 75 days of petition filing (WA RCW 13.34.070) or 90 days (IL 705 ILCS 405/2-14)"
        ],
        notice_requirements=[
            "Formal written notice of trial date issued to all parties and counsel of record"
        ],
        hearing_opportunities=[
            "Full evidentiary bench trial: live witness testimony, direct examination, cross-examination, and exhibits"
        ],
        decision_makers=["Juvenile Court Trial Judge"],
        review_mechanisms=[
            "Motion for Directed Finding / Involuntary Dismissal at close of State's case",
            "Direct appeal or petition for discretionary appellate review following final disposition"
        ],
        critical_documents_to_locate=[
            "Exhibit list and witness disclosures from Department / State",
            "Written Findings of Fact and Conclusions of Law (Order of Adjudication)",
            "Court reporter trial transcript"
        ],
        questions_to_ask=[
            "What standard of proof applies (preponderance of evidence vs clear and convincing evidence)?",
            "What witnesses will the Department call against me?",
            "What affirmative evidence or witnesses will we introduce to rebut their claims?"
        ],
        required_factual_predicates=["Adjudication trial scheduled or underway"],
        unknown_facts_to_investigate=[
            "Did the court make specific written factual findings on each statutory allegation?",
            "Was the hearsay exception for child statements properly tested under statutory reliability rules?"
        ]
    ),

    StageDefinition(
        stage_id="DISPOSITION",
        track=LegalTrack.CPS_DEPENDENCY,
        stage_name="Dispositional Hearing & Court-Ordered Service Plan",
        order=6,
        description="Court determines child placement (in-home vs foster/kinship care) and enters mandatory remedial service orders for parents and agency.",
        governing_authority=[
            "RCW 13.34.130 (WA)",
            "705 ILCS 405/2-22 / 2-23 (IL)",
            "Title IV-E 42 U.S.C. § 671(a)(15) (Reasonable Efforts)"
        ],
        possible_next_stages=["VISITATION", "REUNIFICATION_REVIEW", "PERMANENCY_PLANNING"],
        statutory_deadlines=[
            "Disposition hearing held immediately after adjudication or within 14 to 30 days of fact-finding finding"
        ],
        notice_requirements=[
            "Department must submit proposed individual service plan to parents and counsel 10 to 14 days prior to hearing"
        ],
        hearing_opportunities=[
            "Dispositional hearing where parent can challenge proposed remedial services and request specific providers"
        ],
        decision_makers=["Juvenile Court Judge", "Caseworker", "CASA / Guardian ad Litem"],
        review_mechanisms=[
            "Motion to Amend Service Plan / Object to Overbroad or Inappropriate Services",
            "Direct appeal of final dispositional order"
        ],
        critical_documents_to_locate=[
            "Department's Court Report and Proposed Service Plan",
            "Court's Disposition Order",
            "Individualized Family Service Plan (IFSP / ISP)"
        ],
        questions_to_ask=[
            "Are the ordered services tailored to the specific adjudicatory findings, or are they boilerplate?",
            "Who pays for the ordered evaluations or classes?",
            "What specific benchmark must be met for my child to return home?"
        ],
        required_factual_predicates=["Child found dependent at adjudication", "Dispositional order entered"],
        unknown_facts_to_investigate=[
            "Did the court order active or reasonable efforts tailored to parent's language and disability needs?",
            "Is the child placed in the least restrictive setting with relatives?"
        ]
    ),

    StageDefinition(
        stage_id="VISITATION",
        track=LegalTrack.CPS_DEPENDENCY,
        stage_name="Family Time & Visitation Plan Review",
        order=7,
        description="Court and agency structure parental visitation; visits must be frequent and consistent with reunification goals.",
        governing_authority=[
            "RCW 13.34.136(2)(b)(ii) (WA)",
            "705 ILCS 405/2-10(2) (IL)",
            "Due Process Family Integrity Liberty Interest (Troxel)"
        ],
        possible_next_stages=["UNSUPERVISED_VISITATION", "TRIAL_RETURN_HOME", "REUNIFICATION_REVIEW"],
        statutory_deadlines=[
            "First visit must generally occur within 72 hours of removal",
            "Visitation plan reviewed at every 30-day or 90-day court review"
        ],
        notice_requirements=[
            "Written schedule of visitation times, supervision level, and transportation details provided to parent"
        ],
        hearing_opportunities=[
            "Motion to increase visitation frequency or transition from supervised to unsupervised visits"
        ],
        decision_makers=["Juvenile Court Judge", "Visitation Supervisor", "Caseworker"],
        review_mechanisms=[
            "Motion for Expanded Family Time / Motion to Remove Supervision",
            "Administrative grievance regarding cancelled visits or supervisor bias"
        ],
        critical_documents_to_locate=[
            "Written Family Time / Visitation Schedule",
            "Visitation supervisor observation notes and logs",
            "Transportation assistance vouchers"
        ],
        questions_to_ask=[
            "What specific criteria must I satisfy to move from supervised to unsupervised visitation?",
            "Why was my visitation suspended or restricted, and did the court order that restriction?",
            "Can a trusted relative supervise my visits instead of a paid agency contractor?"
        ],
        required_factual_predicates=["Child in out-of-home placement", "Parent granted visitation rights"],
        unknown_facts_to_investigate=[
            "Is the agency unlawfully conditioning visitation on service compliance contrary to state law?",
            "Are visit notes objective and delivered in discovery?"
        ]
    ),

    StageDefinition(
        stage_id="REUNIFICATION",
        track=LegalTrack.CPS_DEPENDENCY,
        stage_name="Permanency Planning & Periodic Review Hearings",
        order=8,
        description="Periodic review hearings evaluating parent compliance, agency reasonable efforts, and progress toward return home.",
        governing_authority=[
            "Title IV-E 42 U.S.C. § 675(5)(C) (ASFA 12-Month Permanency Mandate)",
            "RCW 13.34.138 / RCW 13.34.145 (WA)",
            "705 ILCS 405/2-28 (IL)"
        ],
        possible_next_stages=["DISMISSAL_AND_FULL_RETURN", "GUARDIANSHIP", "TERMINATION"],
        statutory_deadlines=[
            "Review hearings every 6 months",
            "Permanency planning hearing must occur no later than 12 months after removal",
            "ASFA 15/22 rule: Agency must file termination if child in foster care 15 of last 22 months unless exception applies"
        ],
        notice_requirements=[
            "Written notice of review hearing and Department status report served 14 days before hearing"
        ],
        hearing_opportunities=[
            "Contested permanency hearing: court evaluates whether child can safely return home immediately"
        ],
        decision_makers=["Juvenile Court Judge"],
        review_mechanisms=[
            "Motion for Finding of Lack of Reasonable Efforts by Department",
            "Motion for Trial Return Home (e.g. WA RCW 13.34.138)"
        ],
        critical_documents_to_locate=[
            "Department's 6-Month Court Review Report",
            "Provider service completion certificates, clean urinalysis logs, therapy letters",
            "CASA / Guardian ad Litem recommendation report"
        ],
        questions_to_ask=[
            "Did the court enter a formal finding that the Department made reasonable / active efforts?",
            "Does a compelling reason exception apply to prevent filing a termination petition under ASFA?",
            "When can the child be placed on an in-home trial return?"
        ],
        required_factual_predicates=["Child has been in foster care for 6+ months", "Review hearing scheduled"],
        unknown_facts_to_investigate=[
            "Has the agency provided the remedial services ordered in the disposition plan?",
            "Has an approved relative stepped forward for permanent legal guardianship?"
        ]
    ),

    StageDefinition(
        stage_id="TERMINATION",
        track=LegalTrack.CPS_DEPENDENCY,
        stage_name="Termination of Parental Rights (TPR) Proceedings",
        order=9,
        description="State petitions to permanently and irrevocably sever all legal rights and responsibilities of the biological/legal parents.",
        governing_authority=[
            "Santosky v. Kramer, 455 U.S. 745 (1982) (Clear and convincing evidence requirement)",
            "RCW 13.34.180 / RCW 13.34.190 (WA)",
            "705 ILCS 405/2-29 (IL)",
            "ICWA 25 U.S.C. § 1912(f) (Beyond a reasonable doubt for Indian children)"
        ],
        possible_next_stages=["APPEAL", "ADOPTION_PLACEMENT", "REINSTATEMENT_OF_PARENTAL_RIGHTS"],
        statutory_deadlines=[
            "Contested trial held within statutory timeline (e.g. 60 to 90 days after TPR petition)",
            "Notice of Appeal must be filed within 30 days of entry of final TPR order"
        ],
        notice_requirements=[
            "Personal service of TPR petition and summons giving at least 30 days advance notice of trial"
        ],
        hearing_opportunities=[
            "Full contested trial: State must prove all statutory elements by clear and convincing evidence"
        ],
        decision_makers=["Juvenile Court Trial Judge"],
        review_mechanisms=[
            "Direct Appeal to State Court of Appeals as a matter of right",
            "Motion for Relief from Judgment (e.g. CR 60 / 735 ILCS 5/2-1401)"
        ],
        critical_documents_to_locate=[
            "Petition for Termination of Parental Rights",
            "Final Order Terminating Parental Rights",
            "Written Findings of Fact and Conclusions of Law"
        ],
        questions_to_ask=[
            "Did the State prove that all ordered services were offered and that parent is currently unfit?",
            "If ICWA applies, did qualified expert witnesses testify that continued custody causes serious emotional/physical damage beyond a reasonable doubt?",
            "What is the exact deadline to file the Notice of Appeal?"
        ],
        required_factual_predicates=["Termination petition filed", "TPR trial scheduled or order entered"],
        unknown_facts_to_investigate=[
            "Did the parent preserve objections on the record during the trial?",
            "Was an indigent appellate public defender designated in the final order?"
        ]
    ),

    StageDefinition(
        stage_id="CPS_APPEAL",
        track=LegalTrack.CPS_DEPENDENCY,
        stage_name="Appellate Review of Juvenile Court Order",
        order=10,
        description="Direct appeal to the State Court of Appeals challenging an order of disposition, dependency, or termination of parental rights.",
        governing_authority=[
            "M.L.B. v. S.L.J., 519 U.S. 102 (1996) (Right to transcript for indigent parents)",
            "State Rules of Appellate Procedure (e.g. WA RAP 5.2, IL S. Ct. R. 303/606)"
        ],
        possible_next_stages=["APPELLATE_DECISION", "PETITION_FOR_SUPREME_COURT_REVIEW", "REMAND_FOR_NEW_TRIAL"],
        statutory_deadlines=[
            "Strict 30-day jurisdictional deadline to file Notice of Appeal after entry of final order",
            "Designation of verbatim report of proceedings within 30 to 45 days of notice of appeal"
        ],
        notice_requirements=[
            "Notice of Appeal filed with superior court clerk and served on all parties and appellate clerk"
        ],
        hearing_opportunities=[
            "Oral argument before a three-judge appellate panel (if granted)"
        ],
        decision_makers=["State Court of Appeals Panel (3 Judges)"],
        review_mechanisms=[
            "Motion for Stay of Juvenile Court Order Pending Appeal",
            "Motion for Reconsideration before the Court of Appeals",
            "Petition for Discretionary Review to State Supreme Court"
        ],
        critical_documents_to_locate=[
            "Notice of Appeal with file stamp",
            "Verbatim Report of Proceedings (Trial Transcript)",
            "Appellant Opening Brief, Respondent Brief, and Reply Brief"
        ],
        questions_to_ask=[
            "Has the Notice of Appeal been timely filed with the court clerk?",
            "Did the trial court enter an order of indigency authorizing public expense for trial transcripts?",
            "Is the appeal proceeding on an expedited timeline for child dependency matters?"
        ],
        required_factual_predicates=["Final appealable order entered by juvenile court judge"],
        unknown_facts_to_investigate=[
            "Did the parent retain trial counsel or was an appellate public defender assigned?",
            "Are there preserved legal errors (due process, statutory element failure, hearsay admissions)?"
        ]
    ),

    # ==========================================
    # 2. ADMINISTRATIVE PROCEDURE ACT TRACK
    # ==========================================
    StageDefinition(
        stage_id="ADMIN_INVESTIGATION",
        track=LegalTrack.ADMINISTRATIVE,
        stage_name="Administrative Inquiry / Agency Investigation",
        order=1,
        description="Administrative agency conducts regulatory audit, licensing inspection, or inquiry into alleged regulatory violation.",
        governing_authority=[
            "Administrative Procedure Act (APA), 5 U.S.C. § 551 et seq. (Federal)",
            "State Administrative Procedure Acts (e.g. RCW 34.05, 5 ILCS 100, ORC Chapter 119)"
        ],
        possible_next_stages=["ADMIN_NOTICE", "INFORMAL_RESOLUTION", "INVESTIGATION_CLOSED"],
        statutory_deadlines=["Agency internal processing standards (typically 30-90 days)"],
        notice_requirements=["Subpoena duces tecum or formal notice of inquiry"],
        hearing_opportunities=["Informal interview or conference with regulatory investigators"],
        decision_makers=["Agency Investigator", "Regulatory Enforcement Division Director"],
        review_mechanisms=["Motion to Quash Administrative Subpoena in Court"],
        critical_documents_to_locate=["Administrative Subpoena / Records Request", "Notice of Regulatory Inspection"],
        questions_to_ask=["Is participation in this interview mandatory or voluntary?", "What specific statutory regulation is alleged to be violated?"],
        required_factual_predicates=["Agency investigating business, license, or individual"],
        unknown_facts_to_investigate=["Does the agency have statutory authority to compel documents without a warrant?"]
    ),

    StageDefinition(
        stage_id="ADMIN_NOTICE",
        track=LegalTrack.ADMINISTRATIVE,
        stage_name="Notice of Proposed Adverse Action / Indicated Finding",
        order=2,
        description="Agency serves formal written notice proposing to revoke license, assess civil penalty, or enter founded finding on central registry.",
        governing_authority=[
            "Due Process Clause (Mullane v. Central Hanover Bank)",
            "State APAs (e.g. RCW 34.05.413, 5 ILCS 100/10-25)"
        ],
        possible_next_stages=["ADMIN_HEARING", "DEFAULT_FINAL_ORDER"],
        statutory_deadlines=[
            "Strict Deadline to Request Hearing: typically 20 to 30 days from date of receipt of notice"
        ],
        notice_requirements=["Certified mail or personal delivery containing detailed allegations and instructions on requesting a hearing"],
        hearing_opportunities=["Opportunity to request formal contested administrative hearing before an Administrative Law Judge (ALJ)"],
        decision_makers=["Agency Section Chief", "Regulatory Enforcement Counsel"],
        review_mechanisms=["Filing timely Written Request for Administrative Hearing / Appeal"],
        critical_documents_to_locate=["Formal Notice of Proposed Action", "Hearing Request Form / Instructions", "Proof of delivery / certified mail receipt"],
        questions_to_ask=["What is the exact calendar deadline to submit my written request for a hearing?", "Where and to whom must the hearing request be delivered?"],
        required_factual_predicates=["Formal notice served by agency proposing penalty or license suspension"],
        unknown_facts_to_investigate=["Was the notice delivered to the correct address of record?", "Does requesting a hearing trigger an automatic stay of the penalty?"]
    ),

    StageDefinition(
        stage_id="ADMIN_HEARING",
        track=LegalTrack.ADMINISTRATIVE,
        stage_name="Contested Evidentiary Administrative Hearing",
        order=3,
        description="Full evidentiary trial conducted before an independent Administrative Law Judge (ALJ) or hearing officer under the APA.",
        governing_authority=[
            "State Office of Administrative Hearings (OAH) procedural rules",
            "APA Evidentiary Standards (e.g. RCW 34.05.446, 5 ILCS 100/10-40)"
        ],
        possible_next_stages=["ADMIN_DECISION", "POST_HEARING_BRIEFS"],
        statutory_deadlines=["Hearing held within 30 to 90 days of request; discovery cutoff 14 days prior to hearing"],
        notice_requirements=["Notice of Hearing specifying date, time, virtual/in-person location, and presiding ALJ"],
        hearing_opportunities=["Live witness examination, admission of business records, cross-examination, opening/closing statements"],
        decision_makers=["Administrative Law Judge (ALJ)", "Hearing Officer"],
        review_mechanisms=["Interlocutory motion to disqualify hearing officer for bias", "Motion in limine to exclude evidence"],
        critical_documents_to_locate=["Notice of Hearing", "Agency Hearing Exhibit Packet", "Witness List"],
        questions_to_ask=["Do formal rules of evidence apply, or is reliable hearsay admissible under the APA?", "Can I subpoena third-party witnesses to testify?"],
        required_factual_predicates=["Hearing request accepted and docketed before administrative tribunal"],
        unknown_facts_to_investigate=["Has the agency complied with all pre-hearing disclosure requirements?"]
    ),

    StageDefinition(
        stage_id="ADMIN_DECISION",
        track=LegalTrack.ADMINISTRATIVE,
        stage_name="Initial / Final Administrative Order",
        order=4,
        description="Presiding ALJ issues written findings of fact, conclusions of law, and proposed or final administrative order.",
        governing_authority=[
            "State APAs (e.g. RCW 34.05.461, 5 ILCS 100/10-50)"
        ],
        possible_next_stages=["ADMIN_APPEAL", "JUDICIAL_REVIEW"],
        statutory_deadlines=[
            "ALJ typically issues decision within 30 to 90 days after hearing record closes",
            "Deadline to file administrative appeal: 14 to 30 days after entry of order"
        ],
        notice_requirements=["Written order mailed to all parties and representatives with notice of appeal rights"],
        hearing_opportunities=["Post-decision motion for reconsideration or petition for administrative review"],
        decision_makers=["Administrative Law Judge", "Agency Director / Review Officer"],
        review_mechanisms=["Petition for Administrative Review before Agency Director or Appeals Board"],
        critical_documents_to_locate=["Written Initial or Final Order of the ALJ", "Notice of Administrative Appeal Rights"],
        questions_to_ask=["Is this an 'Initial Order' requiring agency review or a 'Final Order'?", "What is the exact deadline to file a petition for review?"],
        required_factual_predicates=["ALJ issued written ruling following administrative hearing"],
        unknown_facts_to_investigate=["Did the ALJ rule in favor of or against the respondent on each specific violation?"]
    ),

    StageDefinition(
        stage_id="ADMIN_APPEAL",
        track=LegalTrack.ADMINISTRATIVE,
        stage_name="Internal Agency Administrative Appeal",
        order=5,
        description="Review of the ALJ's initial order by the Agency Director, Commissioner, or Administrative Review Board.",
        governing_authority=[
            "State APAs (e.g. RCW 34.05.464, 5 ILCS 100/10-60)"
        ],
        possible_next_stages=["JUDICIAL_REVIEW", "FINAL_AGENCY_ORDER"],
        statutory_deadlines=["Petition for review must be filed within 20 to 30 days of initial order"],
        notice_requirements=["Filing petition with agency executive office and serving opposing agency counsel"],
        hearing_opportunities=["Review typically conducted on the written administrative record and briefs; oral argument discretionary"],
        decision_makers=["Agency Director", "Appeals Review Board"],
        review_mechanisms=["Exhaustion of administrative remedies requirement prior to court review"],
        critical_documents_to_locate=["Petition for Administrative Review", "Agency Final Order / Decision"],
        questions_to_ask=["Has the requirement to exhaust all administrative remedies been satisfied?"],
        required_factual_predicates=["Timely internal appeal filed following initial order"],
        unknown_facts_to_investigate=["Did the Agency Director adopt, modify, or reject the ALJ's findings of fact?"]
    ),

    StageDefinition(
        stage_id="JUDICIAL_REVIEW",
        track=LegalTrack.ADMINISTRATIVE,
        stage_name="Judicial Review in Superior / Circuit Court",
        order=6,
        description="Party appeals final agency order to the judicial branch by filing a Petition for Judicial Review under the APA.",
        governing_authority=[
            "State APAs (e.g. RCW 34.05.570, 735 ILCS 5/Art. III)",
            "Arbitrary and Capricious / Error of Law Standards"
        ],
        possible_next_stages=["APPELLATE_COURT_APPEAL", "REMAND_TO_AGENCY", "AFFIRMANCE_OR_REVERSAL"],
        statutory_deadlines=[
            "Strict 30-Day Jurisdictional Window: Petition must be filed within 30 days of service of final agency order"
        ],
        notice_requirements=["Summons and Petition served on the Agency, Attorney General, and all parties of record"],
        hearing_opportunities=["Oral argument before Superior/Circuit Court judge based on the administrative record"],
        decision_makers=["Superior / Circuit Court Judge"],
        review_mechanisms=["Appeal to State Court of Appeals", "Motion for Stay of Agency Action pending judicial review"],
        critical_documents_to_locate=["Petition for Judicial Review", "Certified Agency Record", "Opening Brief"],
        questions_to_ask=["Can we obtain an emergency judicial stay to prevent the agency order from taking effect during the appeal?", "Was the petition filed within the strict 30-day window?"],
        required_factual_predicates=["Final agency order entered and administrative remedies exhausted"],
        unknown_facts_to_investigate=["Did the agency transmit the complete certified administrative record to the court clerk?"]
    ),

    # ==========================================
    # 3. CRIMINAL PROSECUTION TRACK
    # ==========================================
    StageDefinition(
        stage_id="CRIMINAL_INVESTIGATION",
        track=LegalTrack.CRIMINAL,
        stage_name="Criminal Investigation & Police Inquiry",
        order=1,
        description="Law enforcement investigates alleged criminal offense, executes search warrants, or seeks interviews.",
        governing_authority=["U.S. Const. amend. IV & V", "Miranda v. Arizona, 384 U.S. 436 (1966)"],
        possible_next_stages=["CITATION_OR_ARREST", "CHARGING", "DECLINATION_TO_PROSECUTE"],
        statutory_deadlines=["Statute of limitations for specific crime"],
        notice_requirements=["Search warrant execution inventory"],
        hearing_opportunities=["None at investigative stage"],
        decision_makers=["Police Detective", "Prosecutor"],
        review_mechanisms=["Motion to Suppress Evidence (post-charging)"],
        critical_documents_to_locate=["Search Warrant & Return", "Miranda Advisement Form", "Police Incident Report"],
        questions_to_ask=["Am I free to leave or am I under arrest?", "I assert my 5th Amendment right to remain silent and request an attorney."],
        required_factual_predicates=["Police contact regarding alleged criminal violation"],
        unknown_facts_to_investigate=["Were any statements elicited in custody without Miranda warnings?"]
    ),

    StageDefinition(
        stage_id="CITATION_OR_ARREST",
        track=LegalTrack.CRIMINAL,
        stage_name="Custodial Arrest / Criminal Citation",
        order=2,
        description="Defendant taken into physical custody or issued a criminal citation / summons to appear in court.",
        governing_authority=["County of Riverside v. McLaughlin, 500 U.S. 44 (1991) (48-Hour Probable Cause Rule)", "State Criminal Rules"],
        possible_next_stages=["CHARGING", "ARRAIGNMENT", "RELEASE_ON_OWN_RECOGNIZANCE"],
        statutory_deadlines=["Judicial probable cause determination within 48 hours of warrantless arrest"],
        notice_requirements=["Citation citation ticket or booking sheet detailing charges"],
        hearing_opportunities=["Initial preliminary appearance / bail hearing"],
        decision_makers=["Arresting Officer", "Magistrate / Duty Judge"],
        review_mechanisms=["Emergency Bail Review Motion / Petition for Writ of Habeas Corpus"],
        critical_documents_to_locate=["Citation / Summons to Appear", "Booking Sheet", "Probable Cause Affidavit"],
        questions_to_ask=["When will I see a judge for bail?", "Has a public defender been assigned?"],
        required_factual_predicates=["Defendant arrested or cited with a crime"],
        unknown_facts_to_investigate=["Was probable cause found by a judicial officer within 48 hours?"]
    ),

    StageDefinition(
        stage_id="CHARGING",
        track=LegalTrack.CRIMINAL,
        stage_name="Filing of Formal Criminal Charges",
        order=3,
        description="Prosecutor files Information, Complaint, or Grand Jury Indictment formally charging defendant with specific crimes.",
        governing_authority=["U.S. Const. amend. VI (Notice of Charges)", "State Rules of Criminal Procedure (e.g. CrR 2.1)"],
        possible_next_stages=["ARRAIGNMENT", "MOTION_TO_DISMISS"],
        statutory_deadlines=["Speedy filing limits under local court rules (typically 72 hours from arrest if in custody)"],
        notice_requirements=["Service of formal Information or Indictment"],
        hearing_opportunities=["Grand Jury proceeding (prosecution only) or Preliminary Hearing for felony bind-over"],
        decision_makers=["Elected Prosecutor / State's Attorney", "Grand Jury"],
        review_mechanisms=["Motion to Dismiss for lack of probable cause / defective charging document"],
        critical_documents_to_locate=["Criminal Information / Indictment", "Affidavit of Probable Cause"],
        questions_to_ask=["What are the exact statutory code sections and felony/misdemeanor classes charged?"],
        required_factual_predicates=["Prosecutor filed formal charging instrument"],
        unknown_facts_to_investigate=["Did the prosecutor file charges within the in-custody time limit?"]
    ),

    StageDefinition(
        stage_id="ARRAIGNMENT",
        track=LegalTrack.CRIMINAL,
        stage_name="Arraignment & Conditions of Release (Bail)",
        order=4,
        description="Defendant appears in court, advised of rights, enters plea (Not Guilty), and judge sets bail and release conditions.",
        governing_authority=["U.S. Const. amend. VIII (Excessive Bail Clause)", "CrR 3.1 / CrR 3.2"],
        possible_next_stages=["PRETRIAL_CONFERENCES", "DISCOVERY"],
        statutory_deadlines=[
            "Speedy Trial Clock starts: 60 days if in custody, 90 days if out of custody (e.g. WA CrR 3.3)"
        ],
        notice_requirements=["Reading of charges in open court unless waived by defense counsel"],
        hearing_opportunities=["Bail argument, release conditions, entry of plea"],
        decision_makers=["Presiding Judge / Magistrate"],
        review_mechanisms=["Motion to Modify Conditions of Release / Reduce Bail"],
        critical_documents_to_locate=["Arraignment Minute Order", "Conditions of Release / Bail Bond Receipt", "Scheduling Order"],
        questions_to_ask=["What are my conditions of release (e.g. travel restrictions, no-contact orders)?", "When is the next omnibus / pretrial hearing?"],
        required_factual_predicates=["Arraignment held or scheduled"],
        unknown_facts_to_investigate=["Was the speedy trial clock properly calculated and preserved?"]
    ),

    StageDefinition(
        stage_id="PRETRIAL",
        track=LegalTrack.CRIMINAL,
        stage_name="Pretrial Motions, Discovery, and Omnibus",
        order=5,
        description="Exchange of mandatory discovery (police reports, bodycam), suppression motions (warrant/confession), and plea negotiations.",
        governing_authority=["Brady v. Maryland, 373 U.S. 83 (1963)", "CrR 4.7 (Discovery) & CrR 3.5 / 3.6 (Suppression)"],
        possible_next_stages=["TRIAL", "PLEA_AGREEMENT", "DISMISSAL"],
        statutory_deadlines=["Pretrial motion cutoff date set by court scheduling order"],
        notice_requirements=["Formal written motions and responses with notice of hearing date"],
        hearing_opportunities=["CrR 3.5 confession hearing, CrR 3.6 suppression hearing, omnibus hearing"],
        decision_makers=["Criminal Trial Judge"],
        review_mechanisms=["Interlocutory petition for discretionary review of suppression denial"],
        critical_documents_to_locate=["State's Discovery Disclosures", "Police Bodycam Footage", "Defense Motion to Suppress"],
        questions_to_ask=["Has the prosecutor provided all Brady exculpatory evidence?", "Can we challenge the legality of the search or confession?"],
        required_factual_predicates=["Plea of not guilty entered, matter set for trial"],
        unknown_facts_to_investigate=["Are there unproduced bodycam recordings or witness interview statements?"]
    ),

    StageDefinition(
        stage_id="TRIAL",
        track=LegalTrack.CRIMINAL,
        stage_name="Criminal Jury / Bench Trial",
        order=6,
        description="Constitutional trial where State must prove every element beyond a reasonable doubt to a unanimous jury.",
        governing_authority=["U.S. Const. amend. VI (Confrontation Clause & Jury Trial)", "In re Winship, 397 U.S. 358 (1970)"],
        possible_next_stages=["ACQUITTAL_DISMISSAL", "SENTENCING"],
        statutory_deadlines=["Trial must commence prior to expiration of constitutional/statutory speedy trial clock"],
        notice_requirements=["Trial readiness call / docket call"],
        hearing_opportunities=["Full contested jury trial: opening statements, witness cross-examination, jury instructions"],
        decision_makers=["Jury (12 members for felony) or Bench Trial Judge"],
        review_mechanisms=["Motion for Judgment of Acquittal under Rule 29 / CrR 7.4"],
        critical_documents_to_locate=["Jury Instructions", "Verdict Forms", "Court Reporter Record"],
        questions_to_ask=["Will this be a jury trial or a bench trial?", "What lesser included offenses are submitted to the jury?"],
        required_factual_predicates=["Trial commenced"],
        unknown_facts_to_investigate=["Did the jury render a verdict or is there a mistrial/hung jury?"]
    ),

    StageDefinition(
        stage_id="SENTENCING",
        track=LegalTrack.CRIMINAL,
        stage_name="Sentencing Hearing",
        order=7,
        description="Following conviction, court holds sentencing hearing to review presentence report, criminal history, and impose sentence.",
        governing_authority=["Sentencing Reform Act (SRA) / Statutory Sentencing Guidelines", "U.S. Const. amend. VIII"],
        possible_next_stages=["CRIMINAL_APPEAL"],
        statutory_deadlines=["Sentencing typically occurs within 30 to 45 days of verdict"],
        notice_requirements=["Service of State and Defense Sentencing Memoranda"],
        hearing_opportunities=["Right of Allocution (defendant speaks to judge), victim impact statements, witness testimony"],
        decision_makers=["Sentencing Judge"],
        review_mechanisms=["Motion to Correct Sentence / Motion for New Trial"],
        critical_documents_to_locate=["Judgment and Sentence Order", "Presentence Investigation Report (PSI)", "Felony Judgment & Sentence"],
        questions_to_ask=["What is the standard sentencing range based on my offender score?", "Is an exceptional sentence or diversionary alternative available?"],
        required_factual_predicates=["Verdict of guilty entered"],
        unknown_facts_to_investigate=["Was the criminal history score accurately calculated without unconstitutional prior convictions?"]
    ),

    StageDefinition(
        stage_id="CRIMINAL_APPEAL",
        track=LegalTrack.CRIMINAL,
        stage_name="Direct Criminal Appeal",
        order=8,
        description="Direct appeal to the State Court of Appeals challenging trial errors, unconstitutional evidence, or sentencing errors.",
        governing_authority=["Douglas v. California, 372 U.S. 353 (1963) (Right to Appointed Appellate Counsel)", "Rules of Appellate Procedure"],
        possible_next_stages=["APPELLATE_DECISION", "PETITION_FOR_REVIEW_SUPREME_COURT", "PERSONAL_RESTRAINT_PETITION"],
        statutory_deadlines=["Notice of Appeal must be filed within 30 days of Judgment and Sentence"],
        notice_requirements=["Filing Notice of Appeal with trial court clerk and appellate court"],
        hearing_opportunities=["Appellate panel oral argument"],
        decision_makers=["Court of Appeals Panel (3 Judges)"],
        review_mechanisms=["Motion for Appeal Bond / Stay of Sentence", "Personal Restraint Petition / Post-Conviction Relief"],
        critical_documents_to_locate=["Notice of Appeal", "Verbatim Report of Proceedings", "Appellate Briefs"],
        questions_to_ask=["Has an appellate public defender been appointed?", "What trial errors were preserved by trial counsel's objections?"],
        required_factual_predicates=["Judgment and Sentence entered"],
        unknown_facts_to_investigate=["Did trial counsel file the Notice of Appeal before the 30-day deadline expired?"]
    ),

    # ==========================================
    # 4. CIVIL LITIGATION TRACK
    # ==========================================
    StageDefinition(
        stage_id="CIVIL_COMPLAINT",
        track=LegalTrack.CIVIL_LITIGATION,
        stage_name="Filing of Civil Complaint / Petition",
        order=1,
        description="Plaintiff files formal complaint alleging causes of action, damages, and prayer for relief in court.",
        governing_authority=["Fed. R. Civ. P. 3 / State Civil Rules (CR 3)", "Notice Pleading Standards (Twombly / Iqbal)"],
        possible_next_stages=["SERVICE_OF_PROCESS"],
        statutory_deadlines=["Filing must occur before expiration of applicable statute of limitations"],
        notice_requirements=["Filing with court clerk and obtaining stamped summons"],
        hearing_opportunities=["None at initial filing stage"],
        decision_makers=["Court Clerk / Plaintiff's Attorney"],
        review_mechanisms=["Voluntary dismissal without prejudice (Rule 41)"],
        critical_documents_to_locate=["Summons and Verified Complaint", "Civil Case Cover Sheet"],
        questions_to_ask=["What causes of action are asserted?", "Which court has subject matter and personal jurisdiction?"],
        required_factual_predicates=["Complaint drafted or filed"],
        unknown_facts_to_investigate=["Has the applicable statute of limitations expired?"]
    ),

    StageDefinition(
        stage_id="SERVICE_OF_PROCESS",
        track=LegalTrack.CIVIL_LITIGATION,
        stage_name="Service of Process",
        order=2,
        description="Plaintiff delivers formal summons and complaint to defendant in compliance with personal service rules.",
        governing_authority=["Fed. R. Civ. P. 4 / State CR 4", "Due Process (Mullane v. Central Hanover Bank)"],
        possible_next_stages=["ANSWER_OR_MOTION_TO_DISMISS", "MOTION_FOR_DEFAULT_JUDGMENT"],
        statutory_deadlines=["Service must be completed within 90 days of filing complaint (FRCP 4(m))"],
        notice_requirements=["Personal service by non-party adult or authorized process server"],
        hearing_opportunities=["Special appearance to contest personal jurisdiction / service"],
        decision_makers=["Process Server / Judicial Officer"],
        review_mechanisms=["Motion to Quash Service of Process (Rule 12(b)(5))"],
        critical_documents_to_locate=["Affidavit / Declaration of Service of Process", "Summons"],
        questions_to_ask=["Was service executed personally or by substitute service at residence?", "What is the exact date service was perfected?"],
        required_factual_predicates=["Summons and complaint issued for service"],
        unknown_facts_to_investigate=["Was service executed properly on a qualified individual of suitable age and discretion?"]
    ),

    StageDefinition(
        stage_id="ANSWER_OR_MOTION",
        track=LegalTrack.CIVIL_LITIGATION,
        stage_name="Responsive Pleading (Answer or Rule 12 Motion)",
        order=3,
        description="Defendant files formal Answer with affirmative defenses or files a pre-answer Motion to Dismiss.",
        governing_authority=["Fed. R. Civ. P. 12 / State CR 12"],
        possible_next_stages=["CIVIL_DISCOVERY", "HEARING_ON_MOTION_TO_DISMISS"],
        statutory_deadlines=[
            "Strict Response Clock:",
            "21 days after service of summons (Federal FRCP 12(a)(1))",
            "20 days in Washington State (CR 12(a))",
            "30 days in Illinois (735 ILCS 5/2-602)"
        ],
        notice_requirements=["Service of Answer or Motion on plaintiff counsel of record"],
        hearing_opportunities=["Contested hearing on Motion to Dismiss (Rule 12(b)(6))"],
        decision_makers=["Civil Motions Judge"],
        review_mechanisms=["Motion for Default Judgment (if defendant fails to answer within deadline)"],
        critical_documents_to_locate=["Defendant's Answer and Affirmative Defenses", "Motion to Dismiss & Memorandum of Law"],
        questions_to_ask=["What is the exact deadline to answer before plaintiff can file for default?", "What affirmative defenses (e.g. statute of limitations, waiver, failure to mitigate) must be pleaded?"],
        required_factual_predicates=["Defendant served with summons and complaint"],
        unknown_facts_to_investigate=["Has the plaintiff moved for entry of default?"]
    ),

    StageDefinition(
        stage_id="CIVIL_DISCOVERY",
        track=LegalTrack.CIVIL_LITIGATION,
        stage_name="Discovery & Document Disclosures",
        order=4,
        description="Formal exchange of evidence through interrogatories, requests for production of documents, admissions, and depositions.",
        governing_authority=["Fed. R. Civ. P. 26 - 37 / State CR 26 - 37"],
        possible_next_stages=["SUMMARY_JUDGMENT_MOTIONS", "SETTLEMENT_MEDIATION"],
        statutory_deadlines=[
            "Responses to written discovery due within 30 days of service",
            "Discovery cutoff set by court scheduling order (typically 60-90 days before trial)"
        ],
        notice_requirements=["Certificate of Service for all discovery requests and responses"],
        hearing_opportunities=["Hearing on Motion to Compel Discovery or Motion for Protective Order"],
        decision_makers=["Civil Trial Judge / Discovery Magistrate"],
        review_mechanisms=["Motion to Compel Discovery under Rule 37", "Motion for Sanctions"],
        critical_documents_to_locate=["Interrogatories and Answers", "Requests for Production and Document Responses", "Deposition Transcripts"],
        questions_to_ask=["What is the court's discovery cutoff deadline?", "What documents has the opposing party refused to produce?"],
        required_factual_predicates=["Pleadings closed, discovery phase underway"],
        unknown_facts_to_investigate=["Have all relevant communications, emails, and financial records been preserved under litigation hold?"]
    ),

    StageDefinition(
        stage_id="SUMMARY_JUDGMENT",
        track=LegalTrack.CIVIL_LITIGATION,
        stage_name="Summary Judgment & Dispositive Motions",
        order=5,
        description="Party moves for judgment as a matter of law, asserting there is no genuine dispute as to any material fact.",
        governing_authority=["Fed. R. Civ. P. 56 / State CR 56 (Celotex / Anderson standards)"],
        possible_next_stages=["CIVIL_TRIAL", "ENTRY_OF_JUDGMENT_DISMISSAL", "MEDIATION"],
        statutory_deadlines=["Motion must typically be filed at least 28 to 30 days prior to hearing (WA CR 56 requires 28 days notice)"],
        notice_requirements=["Filing motion, legal brief, and supporting affidavits with strict advance notice to opposing counsel"],
        hearing_opportunities=["Oral argument on summary judgment before trial judge"],
        decision_makers=["Civil Motions / Trial Judge"],
        review_mechanisms=["Motion for Reconsideration within 10 to 14 days", "Direct appeal if order terminates all claims"],
        critical_documents_to_locate=["Motion for Summary Judgment", "Opposition Brief and Affidavits", "Court's Summary Judgment Order"],
        questions_to_ask=["What specific material facts are genuinely disputed requiring a jury trial?", "Did the moving party meet its initial burden of proof?"],
        required_factual_predicates=["Discovery complete, summary judgment motion filed"],
        unknown_facts_to_investigate=["Are there competing declarations or expert reports establishing a triable issue of fact?"]
    ),

    StageDefinition(
        stage_id="CIVIL_TRIAL",
        track=LegalTrack.CIVIL_LITIGATION,
        stage_name="Civil Jury / Bench Trial",
        order=6,
        description="Formal trial of disputed facts before a jury or bench judge under the preponderance of the evidence standard.",
        governing_authority=["Fed. R. Civ. P. 38 - 53 / State CR 38 - 53", "Rules of Evidence"],
        possible_next_stages=["ENTRY_OF_CIVIL_JUDGMENT"],
        statutory_deadlines=["Pretrial order, motions in limine, and exhibit marking deadlines set by court order"],
        notice_requirements=["Notice of Trial Setting"],
        hearing_opportunities=["Opening statements, witness direct/cross, admission of exhibits, closing arguments"],
        decision_makers=["Jury or Superior Court Judge"],
        review_mechanisms=["Motion for Judgment as a Matter of Law (Rule 50)", "Motion for Mistrial"],
        critical_documents_to_locate=["Joint Pretrial Statement", "Jury Verdict Form", "Minute Entries"],
        questions_to_ask=["What standard of proof governs each cause of action?", "What are the proposed jury instructions?"],
        required_factual_predicates=["Matter called for trial"],
        unknown_facts_to_investigate=["Did the jury reach a verdict or deadlock?"]
    ),

    StageDefinition(
        stage_id="CIVIL_JUDGMENT",
        track=LegalTrack.CIVIL_LITIGATION,
        stage_name="Entry of Final Judgment & Post-Trial Motions",
        order=7,
        description="Court enters formal written judgment awarding damages, injunctive relief, or dismissing claims.",
        governing_authority=["Fed. R. Civ. P. 54 / 58 / 59 / State CR 54 / 59"],
        possible_next_stages=["CIVIL_APPEAL", "JUDGMENT_ENFORCEMENT_COLLECTION"],
        statutory_deadlines=[
            "Motion for New Trial / Motion to Alter Judgment: must be filed within 28 days of judgment (FRCP 59(b)) or 10 days (WA CR 59)",
            "Cost Bill / Attorney Fee Motion within 10 to 14 days"
        ],
        notice_requirements=["Service of Notice of Entry of Judgment"],
        hearing_opportunities=["Hearing on post-trial motions or fee petitions"],
        decision_makers=["Trial Judge"],
        review_mechanisms=["Motion for New Trial (Rule 59)", "Motion for Relief from Judgment (Rule 60)"],
        critical_documents_to_locate=["Final Judgment Order", "Cost Bill / Fee Award Order", "Notice of Entry of Judgment"],
        questions_to_ask=["When was the final judgment formally entered on the court docket?", "What is the exact deadline to file post-trial motions?"],
        required_factual_predicates=["Final judgment signed and docketed by clerk"],
        unknown_facts_to_investigate=["Does the judgment dispose of all claims against all parties, making it final and appealable?"]
    ),

    StageDefinition(
        stage_id="CIVIL_APPEAL",
        track=LegalTrack.CIVIL_LITIGATION,
        stage_name="Civil Appellate Review",
        order=8,
        description="Party appeals final judgment to the State Court of Appeals or Federal Circuit Court of Appeals.",
        governing_authority=["Fed. R. App. P. 3 & 4 / State Rules of Appellate Procedure (RAP 5.2)"],
        possible_next_stages=["APPELLATE_OPINION", "SUPREME_COURT_PETITION"],
        statutory_deadlines=[
            "Strict 30-Day Jurisdictional Deadline: Notice of Appeal must be filed within 30 days of entry of judgment or order disposing of timely Rule 59 motion"
        ],
        notice_requirements=["Filing Notice of Appeal with trial court clerk and serving all counsel"],
        hearing_opportunities=["Appellate panel oral argument"],
        decision_makers=["Appellate Court Panel (3 Judges)"],
        review_mechanisms=["Supersedeas Bond / Motion for Stay of Enforcement Pending Appeal"],
        critical_documents_to_locate=["Notice of Appeal with filing stamp", "Trial Court Record", "Opening Brief"],
        questions_to_ask=["Has a supersedeas bond been posted to stay collection on the monetary judgment?", "Was the appeal notice filed within the 30-day jurisdictional limit?"],
        required_factual_predicates=["Final judgment entered, appeal filed"],
        unknown_facts_to_investigate=["Were all appellate legal issues properly preserved by trial objections?"]
    )
]


class PathwayRegistry:
    """Indexed lookup for procedural stages and pathway graphs."""

    _STAGES_BY_ID: Dict[str, StageDefinition] = {s.stage_id: s for s in ALL_STAGES}

    @classmethod
    def get_all_stages(cls) -> List[StageDefinition]:
        return list(cls._STAGES_BY_ID.values())

    @classmethod
    def get_by_id(cls, stage_id: str) -> StageDefinition | None:
        return cls._STAGES_BY_ID.get(stage_id)

    @classmethod
    def get_by_track(cls, track: LegalTrack) -> List[StageDefinition]:
        stages = [s for s in cls._STAGES_BY_ID.values() if s.track == track]
        stages.sort(key=lambda x: x.order)
        return stages
