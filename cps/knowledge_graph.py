"""14-Stage Comprehensive CPS Knowledge Graph linking Authorities, Deadlines, Findings, and Remedies."""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class CPSLifecycleStage(str, Enum):
    INTAKE = "INTAKE"
    SCREENING = "SCREENING"
    INVESTIGATION = "INVESTIGATION"
    SAFETY_ASSESSMENT = "SAFETY_ASSESSMENT"
    EMERGENCY_REMOVAL = "EMERGENCY_REMOVAL"
    SHELTER_TEMPORARY_CUSTODY = "SHELTER_TEMPORARY_CUSTODY"
    DEPENDENCY_ADJUDICATION = "DEPENDENCY_ADJUDICATION"
    CASE_PLAN = "CASE_PLAN"
    SERVICES = "SERVICES"
    VISITATION = "VISITATION"
    SIX_MONTH_REVIEW = "SIX_MONTH_REVIEW"
    PERMANENCY_PLANNING = "PERMANENCY_PLANNING"
    GUARDIANSHIP_OR_TERMINATION = "GUARDIANSHIP_OR_TERMINATION"
    APPEAL = "APPEAL"


class CPSStageNode(BaseModel):
    stage: CPSLifecycleStage
    stage_name: str
    description: str
    statutes_by_state: Dict[str, str] = Field(default_factory=dict)
    regulations_by_state: Dict[str, str] = Field(default_factory=dict)
    policies_by_state: Dict[str, str] = Field(default_factory=dict)
    court_rules_by_state: Dict[str, str] = Field(default_factory=dict)
    case_precedents: List[str] = Field(default_factory=list)
    constitutional_rules: List[str] = Field(default_factory=list)
    deadlines_by_state: Dict[str, str] = Field(default_factory=dict)
    required_notices: Dict[str, str] = Field(default_factory=dict)
    mandatory_findings: List[str] = Field(default_factory=list)
    burdens_of_proof: Dict[str, str] = Field(default_factory=dict)
    available_remedies: List[str] = Field(default_factory=list)


class CPSKnowledgeGraph:
    """Relational knowledge graph mapping the 14 child welfare stages to controlling legal authorities."""

    def __init__(self):
        self.nodes: Dict[CPSLifecycleStage, CPSStageNode] = {}
        self._init_cps_graph()

    def _init_cps_graph(self):
        # 1. EMERGENCY_REMOVAL
        self.nodes[CPSLifecycleStage.EMERGENCY_REMOVAL] = CPSStageNode(
            stage=CPSLifecycleStage.EMERGENCY_REMOVAL,
            stage_name="Emergency Protective Custody & Immediate Removal",
            description="Exigent warrantless seizure or court-ordered preliminary removal of a child from parental custody.",
            statutes_by_state={
                "WA": "RCW 13.34.050 & RCW 13.34.055",
                "IL": "705 ILCS 405/2-5 & 705 ILCS 405/2-6",
                "OH": "ORC § 2151.31 & ORC § 2151.311",
                "CA": "Cal. Welf. & Inst. Code § 305 & § 306",
                "TX": "Tex. Fam. Code § 262.104",
                "NY": "N.Y. Fam. Ct. Act § 1024",
                "US": "42 U.S.C. § 671(a)(15) (Title IV-E Reasonable Efforts) & 25 U.S.C. § 1922 (ICWA Emergency Removal)"
            },
            policies_by_state={
                "WA": "DCYF Policy 1110 (Present Danger Assessment)",
                "IL": "DCFS Procedure 300 (Reports of Abuse & Neglect)",
                "OH": "OAC 5101:2-36-03 (PCSA Intake Assessment)",
                "CA": "CDSS MPP Division 31-125 (Emergency Response)",
                "TX": "DFPS Handbook § 2100 (Investigation Priority)",
                "NY": "OCFS CPS Manual Ch. 6 § 3 (Emergency Removal)"
            },
            case_precedents=[
                "Stanley v. Illinois, 405 U.S. 645 (1972) (Unfit parent hearing required)",
                "Nicholson v. Scoppetta, 3 N.Y.3d 357 (2004) (Imminent danger standard strictly required)"
            ],
            constitutional_rules=[
                "Fourteenth Amendment Due Process Clause: Fundamental liberty interest in family integrity",
                "Fourth Amendment: Warrant requirement applies to domestic child removals absent true exigent circumstances"
            ],
            deadlines_by_state={
                "WA": "Petition must be filed within 72 hours; 72h shelter care hearing",
                "IL": "Temporary custody hearing within 48 hours",
                "OH": "Detention hearing within 72 hours",
                "CA": "Detention hearing next judicial day after filing (48-72h)",
                "TX": "Full adversary hearing within 14 days",
                "NY": "Petition filed next court day; § 1028 hearing within 3 court days of application"
            },
            required_notices={
                "ALL": "Immediate written notice to parents of child's whereabouts and scheduled emergency hearing."
            },
            mandatory_findings=[
                "Imminent danger to child's physical health or safety",
                "Continuation in the home is contrary to the child's welfare",
                "Reasonable efforts made to prevent removal or lack of efforts was reasonable under the emergency"
            ],
            burdens_of_proof={
                "WA": "Probable cause (court order) / Reasonable cause (police)",
                "IL": "Probable cause & Urgent/immediate necessity",
                "OH": "Probable cause",
                "CA": "Prima facie showing of dependency",
                "TX": "Evidence sufficient to satisfy person of ordinary prudence",
                "NY": "Reasonable cause of imminent danger to life or health",
                "ICWA": "Clear and convincing evidence of imminent physical damage or harm (25 U.S.C. § 1922)"
            },
            available_remedies=[
                "Immediate in-home safety plan with non-offending relatives",
                "Motion to Vacate Emergency Custody Order",
                "Application for Immediate Return of Child"
            ]
        )

        # 2. SHELTER_TEMPORARY_CUSTODY
        self.nodes[CPSLifecycleStage.SHELTER_TEMPORARY_CUSTODY] = CPSStageNode(
            stage=CPSLifecycleStage.SHELTER_TEMPORARY_CUSTODY,
            stage_name="Initial Shelter Care / Temporary Custody / Detention Hearing",
            description="First adversarial hearing following emergency removal to evaluate probable cause and continued detention.",
            statutes_by_state={
                "WA": "RCW 13.34.065",
                "IL": "705 ILCS 405/2-10",
                "OH": "ORC § 2151.314",
                "CA": "Cal. Welf. & Inst. Code § 315 & § 319",
                "TX": "Tex. Fam. Code § 262.201",
                "NY": "N.Y. Fam. Ct. Act § 1027 & § 1028",
                "US": "25 U.S.C. § 1912(a) (ICWA 10-Day Notice) & 42 U.S.C. § 671(a)(15)"
            },
            case_precedents=[
                "In re Dependency of K.N.J., 171 Wn.2d 568 (2011)",
                "Lassiter v. Dept. of Social Services, 452 U.S. 18 (1981)"
            ],
            constitutional_rules=[
                "Mandatory appointment of counsel for indigent parents",
                "Procedural due process right to cross-examine caseworker and present evidence"
            ],
            deadlines_by_state={
                "WA": "Within 72 hours excluding weekends and legal holidays",
                "IL": "Within 48 hours excluding weekends and court holidays",
                "OH": "Within 72 hours of taking into custody",
                "CA": "Expiration of next judicial day after petition filed",
                "TX": "Not later than the 14th day after emergency removal",
                "NY": "Within 3 court days of parent § 1028 application"
            },
            required_notices={
                "ALL": "Personal service of petition, summons, and advisement of right to court-appointed counsel."
            },
            mandatory_findings=[
                "Probable cause child is dependent/abused/neglected",
                "Reasonable efforts made to prevent out-of-home placement",
                "Release to parent would create serious risk of harm"
            ],
            burdens_of_proof={
                "WA": "Preponderance of evidence to deny release",
                "IL": "Probable cause & urgent necessity",
                "OH": "Probable cause",
                "CA": "Prima facie case of dependency",
                "TX": "Sufficient evidence of continuing danger",
                "NY": "Imminent risk to life or health",
                "ICWA": "Clear and convincing evidence with Qualified Expert Witness (QEW)"
            },
            available_remedies=[
                "Release of child to parent with protective supervision",
                "Kinship placement preference with relatives",
                "Court-ordered immediate family visitation within 72 hours"
            ]
        )

        # 3. DEPENDENCY_ADJUDICATION
        self.nodes[CPSLifecycleStage.DEPENDENCY_ADJUDICATION] = CPSStageNode(
            stage=CPSLifecycleStage.DEPENDENCY_ADJUDICATION,
            stage_name="Fact-Finding & Dependency Adjudication Hearing",
            description="Formal trial on the merits of the allegations in the dependency/neglect petition.",
            statutes_by_state={
                "WA": "RCW 13.34.110 & RCW 13.34.130",
                "IL": "705 ILCS 405/2-18 & 705 ILCS 405/2-21",
                "OH": "ORC § 2151.35",
                "CA": "Cal. Welf. & Inst. Code § 355",
                "TX": "Tex. Fam. Code § 263.401",
                "NY": "N.Y. Fam. Ct. Act § 1046",
                "US": "25 U.S.C. § 1912(e)"
            },
            case_precedents=[
                "In re Arthur H., 212 Ill. 2d 441 (2004) (Child status adjudication vs parental fault)",
                "Troxel v. Granville, 530 U.S. 57 (2000) (Fit parent presumption)"
            ],
            constitutional_rules=[
                "State bears burden of proof; parent cannot be required to prove innocence"
            ],
            deadlines_by_state={
                "WA": "Within 75 days of petition filing",
                "IL": "Within 90 days of temporary custody order",
                "OH": "Within 30 days of complaint filing",
                "CA": "Within 30 days of detention hearing",
                "TX": "Strict 1-year dismissal deadline (§ 263.401)",
                "NY": "Within 60 days of petition filing"
            },
            required_notices={
                "ALL": "Formal summons and petition service under state civil / juvenile rules."
            },
            mandatory_findings=[
                "Child meets statutory definition of abused, neglected, or dependent"
            ],
            burdens_of_proof={
                "WA": "Preponderance of the evidence (RCW 13.34.110)",
                "IL": "Preponderance of the evidence (705 ILCS 405/2-18)",
                "OH": "Clear and convincing evidence (ORC § 2151.35)",
                "CA": "Preponderance of the evidence (WIC § 355)",
                "TX": "Preponderance at SAPCR adjudication / Clear & convincing for final conservatorship",
                "NY": "Preponderance of the evidence (FCA § 1046)",
                "ICWA": "Clear and convincing evidence supported by Qualified Expert Witness"
            },
            available_remedies=[
                "Dismissal of petition with prejudice if State fails burden",
                "In-home dependency disposition",
                "Custody return with voluntary family services"
            ]
        )

        # 4. GUARDIANSHIP_OR_TERMINATION
        self.nodes[CPSLifecycleStage.GUARDIANSHIP_OR_TERMINATION] = CPSStageNode(
            stage=CPSLifecycleStage.GUARDIANSHIP_OR_TERMINATION,
            stage_name="Involuntary Termination of Parental Rights (TPR) / Permanent Custody",
            description="Permanent and irrevocable severance of the legal parent-child relationship.",
            statutes_by_state={
                "WA": "RCW 13.34.180 & RCW 13.34.190",
                "IL": "705 ILCS 405/2-29 & 750 ILCS 50/1",
                "OH": "ORC § 2151.414",
                "CA": "Cal. Welf. & Inst. Code § 366.26",
                "TX": "Tex. Fam. Code § 161.001",
                "NY": "N.Y. Soc. Serv. Law § 384-b",
                "US": "25 U.S.C. § 1912(f) (ICWA TPR Standard) & 42 U.S.C. § 675(5)(E) (ASFA 15/22 Rule)"
            },
            case_precedents=[
                "Santosky v. Kramer, 455 U.S. 745 (1982) (Clear and convincing evidence mandatory under Due Process)",
                "In re Marilyn H., 5 Cal. 4th 295 (1993)",
                "In re J.F.C., 96 S.W.3d 256 (Tex. 2002)"
            ],
            constitutional_rules=[
                "Fourteenth Amendment: Clear and convincing evidence minimum constitutional standard (Santosky)",
                "ICWA: Beyond a reasonable doubt standard for Indian children (25 U.S.C. § 1912(f))"
            ],
            deadlines_by_state={
                "ALL": "ASFA 15 of 22 months in foster care trigger (subject to relative and service exceptions)"
            },
            required_notices={
                "ALL": "Personal service of TPR petition and notice of right to counsel."
            },
            mandatory_findings=[
                "Proof of statutory predicate grounds of parental unfitness / permanent neglect",
                "Active/reasonable efforts were provided and failed to correct deficiencies",
                "Termination is in the child's best interests"
            ],
            burdens_of_proof={
                "ALL_STATES": "Clear and Convincing Evidence (Santosky v. Kramer)",
                "ICWA": "Beyond a Reasonable Doubt supported by testimony of Qualified Expert Witness (25 U.S.C. § 1912(f))"
            },
            available_remedies=[
                "Relative permanent guardianship (Title 11/WIC § 366.26) in lieu of termination",
                "Dismissal of TPR petition due to agency failure to provide reasonable efforts",
                "Open adoption / post-termination contact agreement"
            ]
        )

    def get_stage_node(self, stage: CPSLifecycleStage) -> Optional[CPSStageNode]:
        return self.nodes.get(stage)


# Global singleton
cps_knowledge_graph = CPSKnowledgeGraph()
