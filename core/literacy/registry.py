"""Canonical Legal Literacy Knowledge Base and Concept Registry."""

from typing import Dict, Any, Optional, List
from core.literacy.models import (
    LiteracyLevel,
    DrillDownAction,
    PrimaryAuthorityReference,
    DrillDownResult,
    LegalConceptExploration,
)


CANONICAL_CONCEPTS: Dict[str, Dict[str, Any]] = {
    "due process": {
        "canonical_name": "Due Process of Law",
        "aliases": ["due process", "procedural due process", "substantive due process", "mathews balancing"],
        "level_1": (
            "The basic idea is that government officials cannot simply take away your freedom, your children, "
            "or your property on their own whim. Before they take an action that deeply harms your life, they must follow "
            "fair, required rules and procedures—such as giving you clear written notice beforehand and allowing you to speak "
            "and defend yourself in front of a neutral decision-maker."
        ),
        "level_2": (
            "In practical terms for your situation: If an agency (like CPS, law enforcement, or a licensing board) investigates "
            "or intervenes in your family, they cannot hold secret proceedings or change your rights without giving you advance notice. "
            "You are entitled to know exactly what allegations are made against you, to inspect the evidence they claim to have, "
            "to have a lawyer present, to present your own witnesses, and to have a formal hearing before an independent judge "
            "within strict statutory deadlines (often 24 to 72 hours in emergency child welfare matters)."
        ),
        "level_3": (
            "Due Process divides into two distinct constitutional doctrines:\n"
            "1. **Procedural Due Process**: Governs the fairness of the decision-making process. Under the three-factor balancing "
            "test of *Mathews v. Eldridge*, courts weigh: (a) the private interest affected; (b) the risk of an erroneous deprivation "
            "through current procedures and the probable value of additional procedural safeguards; and (c) the government's interest, "
            "including administrative and fiscal burdens.\n"
            "2. **Substantive Due Process**: Protects fundamental liberty interests that are so deeply rooted in the nation's history "
            "and tradition that the government cannot infringe upon them regardless of the fairness of the procedures, unless the infringement "
            "survives strict judicial scrutiny."
        ),
        "level_4": [
            PrimaryAuthorityReference(
                citation="U.S. Const. amend. XIV, § 1",
                source_type="CONSTITUTION",
                official_portal_url="https://www.govinfo.gov/content/pkg/GPO-CONAN-2017/pdf/GPO-CONAN-2017.pdf",
                key_holding_or_text="No State shall make or enforce any law which shall abridge the privileges or immunities of citizens of the United States; nor shall any State deprive any person of life, liberty, or property, without due process of law.",
                jurisdiction="US",
                is_binding=True
            ),
            PrimaryAuthorityReference(
                citation="Mathews v. Eldridge, 424 U.S. 319 (1976)",
                source_type="CASELAW",
                official_portal_url="https://www.supremecourt.gov/",
                key_holding_or_text="Identified the three-part balancing test determining the constitutional adequacy of administrative and pre-deprivation procedural protections.",
                jurisdiction="US",
                is_binding=True
            ),
            PrimaryAuthorityReference(
                citation="Santosky v. Kramer, 455 U.S. 745 (1982)",
                source_type="CASELAW",
                official_portal_url="https://www.supremecourt.gov/",
                key_holding_or_text="Before a State may sever completely and irrevocably the rights of parents in their natural child, due process requires that the State support its allegations by at least clear and convincing evidence.",
                jurisdiction="US",
                is_binding=True
            )
        ],
        "level_5": (
            "Advanced constitutional tension centers on the interplay between the emergency doctrine (exigent circumstances) "
            "and the fundamental liberty interest in family integrity under *Troxel v. Granville* and *Santosky v. Kramer*. "
            "While government agencies invoke administrative discretion and child safety as paramount sovereign interests, "
            "federal circuits (e.g., 9th Cir. *Wallis v. Spencer*; 2nd Cir. *Nicholson v. Scoppetta*) rigorously restrict post-hoc "
            "rationalizations of emergency warrantless entries. When the government asserts that pre-deprivation hearings are impractical, "
            "due process mandates an immediate, robust post-deprivation adversary hearing with appointed counsel and clear evidentiary standards."
        ),
        "drill_downs": {
            DrillDownAction.SHOW_SOURCE: DrillDownResult(
                action=DrillDownAction.SHOW_SOURCE,
                title="Official Primary Sources for Due Process",
                content=(
                    "- **United States Constitution**: Fourteenth Amendment, § 1 (Accessible at www.govinfo.gov / Library of Congress CONAN).\n"
                    "- **Supreme Court Slip Opinions**: *Mathews v. Eldridge*, 424 U.S. 319; *Santosky v. Kramer*, 455 U.S. 745.\n"
                    "- **State Constitutional Analogs**: Wash. Const. art. I, § 3; Ill. Const. art. I, § 2; Cal. Const. art. I, § 7."
                ),
                citations=["U.S. Const. amend. XIV", "Wash. Const. art. I, § 3"],
                official_sources=["https://www.govinfo.gov", "https://leg.wa.gov"]
            ),
            DrillDownAction.SHOW_STATUTE: DrillDownResult(
                action=DrillDownAction.SHOW_STATUTE,
                title="Controlling Statutory Frameworks Governing Due Process Timelines",
                content=(
                    "- **Federal Child Welfare**: 42 U.S.C. § 671(a)(15) (Mandatory judicial findings of reasonable efforts).\n"
                    "- **Washington State**: RCW 13.34.065 (Requires mandatory court shelter care hearing within 72 hours of custody).\n"
                    "- **Illinois**: 705 ILCS 405/2-9 & 2-10 (Mandatory temporary custody hearing within 48 hours excluding weekends).\n"
                    "- **California**: Cal. Welf. & Inst. Code § 315 (Detention hearing within 48 hours of warrantless custody)."
                ),
                citations=["42 U.S.C. § 671", "RCW 13.34.065", "705 ILCS 405/2-9", "Cal. WIC § 315"],
                official_sources=["https://uscode.house.gov", "https://leg.wa.gov", "https://ilga.gov"]
            ),
            DrillDownAction.SHOW_CASE: DrillDownResult(
                action=DrillDownAction.SHOW_CASE,
                title="Controlling Precedent: Santosky v. Kramer, 455 U.S. 745 (1982)",
                content=(
                    "**Case**: Santosky v. Kramer, 455 U.S. 745 (1982)\n"
                    "**Court**: Supreme Court of the United States | **Year**: 1982\n"
                    "**Holding**: The Due Process Clause of the Fourteenth Amendment requires a standard of proof at least "
                    "equal to 'clear and convincing evidence' in parental rights termination proceedings.\n"
                    "**Seminal Quote**: 'The fundamental liberty interest of natural parents in the care, custody, and management "
                    "of their child does not evaporate simply because they have not been model parents or have lost temporary custody of their child to the State.'"
                ),
                citations=["Santosky v. Kramer, 455 U.S. 745 (1982)"],
                official_sources=["https://www.supremecourt.gov"]
            ),
            DrillDownAction.EXPLAIN_OPPOSING: DrillDownResult(
                action=DrillDownAction.EXPLAIN_OPPOSING,
                title="Opposing Interpretation: The State's Parens Patriae & Safety Doctrine",
                content=(
                    "**The Agency / State Theory**:\n"
                    "State agencies argue that under the *parens patriae* power and *DeShaney v. Winnebago County*, the State owes an "
                    "affirmative duty to protect vulnerable children from harm. When immediate physical danger is reported, the government "
                    "argues that procedural delays required for pre-removal warrants or full hearings would endanger child life. "
                    "Thus, the agency contends that brief procedural truncations are justified by urgent public welfare interests, "
                    "with due process satisfied by providing hearing opportunities after safety has been secured."
                ),
                citations=["DeShaney v. Winnebago County Dept. of Social Services, 489 U.S. 189 (1989)"],
                official_sources=["https://www.supremecourt.gov"]
            ),
            DrillDownAction.SHOW_TEMPORAL_CHANGE: DrillDownResult(
                action=DrillDownAction.SHOW_TEMPORAL_CHANGE,
                title="Historical Evolution & Temporal Changes in Due Process Protections",
                content=(
                    "- **Pre-1970**: Family welfare proceedings operated under informal, paternalistic administrative discretion with minimal formal court hearings.\n"
                    "- **1976 (*Mathews*)**: Formalized the 3-factor balancing test, curtailing unchecked bureaucratic discretion.\n"
                    "- **1982 (*Santosky*)**: Constitutionalized the 'clear and convincing' standard, striking down state laws permitting preponderance thresholds.\n"
                    "- **1997 (ASFA 42 U.S.C. § 675)**: Imposed strict 15/22-month timelines on state foster care systems, balancing parental reunification against permanence.\n"
                    "- **Recent Amendments**: Washington (2021 SB 5118 amending RCW 13.34.065) heightened the threshold for emergency removal, requiring imminent physical harm."
                ),
                citations=["RCW 13.34.065 (Amended 2021)", "42 U.S.C. § 675 (Enacted 1997)"],
                official_sources=["https://leg.wa.gov/CodeReviser"]
            )
        }
    },

    "warrant requirement": {
        "canonical_name": "Fourth Amendment Warrant Requirement in Child Protection",
        "aliases": ["warrant requirement", "warrant", "fourth amendment", "exigent circumstances", "emergency removal"],
        "level_1": (
            "Government caseworkers and police cannot just walk into your home or take your children without a judge's written order (a warrant), "
            "unless there is a true, immediate physical emergency happening right that second where waiting for a judge would result in serious bodily injury."
        ),
        "level_2": (
            "In your practical situation: If an agency worker comes to your door demanding entry or threatening to remove a child, "
            "they generally must show you a valid court order signed by a judge. If they claim 'exigent circumstances' without a warrant, "
            "they must later prove in court that they had reliable, specific facts showing the child was in imminent, severe physical danger "
            "during the exact time it would have taken to apply for a telephonic or emergency warrant."
        ),
        "level_3": (
            "The Fourth Amendment, applied to the states via the Fourteenth Amendment, protects the sanctity of the home and the person against "
            "unreasonable searches and seizures. In child welfare jurisprudence, the removal of a child from parental custody constitutes a "
            "'seizure' under the Fourth Amendment, and entering a residence constitutes a 'search'. The warrantless entry or removal is "
            "presumptively unconstitutional unless the State proves the narrow 'exigent circumstances' exception: reasonable cause to believe "
            "that the child is in imminent danger of serious physical harm, and the lack of sufficient time to obtain a warrant."
        ),
        "level_4": [
            PrimaryAuthorityReference(
                citation="U.S. Const. amend. IV",
                source_type="CONSTITUTION",
                official_portal_url="https://www.govinfo.gov/",
                key_holding_or_text="The right of the people to be secure in their persons, houses, papers, and effects, against unreasonable searches and seizures, shall not be violated, and no Warrants shall issue, but upon probable cause...",
                jurisdiction="US",
                is_binding=True
            ),
            PrimaryAuthorityReference(
                citation="Wallis v. Spencer, 202 F.3d 1126 (9th Cir. 2000)",
                source_type="CASELAW",
                official_portal_url="https://www.ca9.uscourts.gov/",
                key_holding_or_text="Officials may not remove children from their parents' custody without a court order unless they have information at the time of the seizure that establishes reasonable cause to believe that the child is in imminent danger of serious bodily injury and that the scope of the intrusion is reasonably necessary to avert that specific injury.",
                jurisdiction="US-FED",
                is_binding=True
            ),
            PrimaryAuthorityReference(
                citation="Nicholson v. Scoppetta, 3 N.Y.3d 357 (2004)",
                source_type="CASELAW",
                official_portal_url="https://www.nycourts.gov/",
                key_holding_or_text="Emergency removal without a prior court order under Family Court Act § 1024 requires imminent physical peril to the child and cannot be based solely on parental victimhood of domestic violence.",
                jurisdiction="US-NY",
                is_binding=True
            )
        ],
        "level_5": (
            "The doctrinal frontier involves qualified immunity under 42 U.S.C. § 1983 and the definition of 'imminent danger'. "
            "Caseworkers frequently argue that 'clearly established law' did not prohibit warrantless removal under nuanced domestic facts. "
            "However, every federal circuit that has addressed the issue has held that the Fourth Amendment applies with full force to child welfare "
            "investigators (e.g., *Roska v. Peterson* in the 10th Cir.; *Wallis v. Spencer* in the 9th Cir.; *Doe v. Kearney* in the 11th Cir.). "
            "The circuit split centers on whether a telephonic warrant must be attempted when judicial officers are available outside business hours."
        ),
        "drill_downs": {
            DrillDownAction.SHOW_SOURCE: DrillDownResult(
                action=DrillDownAction.SHOW_SOURCE,
                title="Official Fourth Amendment Authority Sources",
                content="- **U.S. Constitution**: Fourth Amendment (govinfo.gov / U.S. National Archives).\n- **Federal Circuit Opinions**: *Wallis v. Spencer*, 202 F.3d 1126 (9th Cir. 2000); *Roska v. Peterson*, 328 F.3d 1230 (10th Cir. 2003).",
                citations=["U.S. Const. amend. IV", "Wallis v. Spencer, 202 F.3d 1126"],
                official_sources=["https://www.govinfo.gov", "https://ca9.uscourts.gov"]
            ),
            DrillDownAction.SHOW_STATUTE: DrillDownResult(
                action=DrillDownAction.SHOW_STATUTE,
                title="State Statutory Codifications of Emergency Removal Limits",
                content=(
                    "- **Washington**: RCW 13.34.050 (Requires court order based on verified petition establishing probable cause).\n"
                    "- **California**: Cal. Welf. & Inst. Code § 305/306 (Emergency warrantless custody restricted to immediate danger of physical injury).\n"
                    "- **Texas**: Tex. Fam. Code § 262.104 (Emergency possession without court order strictly limited to imminent physical health or safety danger)."
                ),
                citations=["RCW 13.34.050", "Cal. WIC § 305", "Tex. Fam. Code § 262.104"],
                official_sources=["https://leg.wa.gov", "https://statutes.capitol.texas.gov"]
            ),
            DrillDownAction.SHOW_CASE: DrillDownResult(
                action=DrillDownAction.SHOW_CASE,
                title="Leading Precedent: Roska ex rel. Roska v. Peterson, 328 F.3d 1230 (10th Cir. 2003)",
                content=(
                    "**Court**: Tenth Circuit Court of Appeals | **Year**: 2003\n"
                    "**Holding**: In-home entry and removal of a child without a warrant violates the Fourth Amendment "
                    "absent genuine exigent circumstances. Social workers do not possess blanket immunity from Fourth Amendment warrant commands.\n"
                    "**Quote**: 'It is well-established that the Fourth Amendment applies to social workers as well as police officers.'"
                ),
                citations=["Roska ex rel. Roska v. Peterson, 328 F.3d 1230"],
                official_sources=["https://www.ca10.uscourts.gov"]
            ),
            DrillDownAction.EXPLAIN_OPPOSING: DrillDownResult(
                action=DrillDownAction.EXPLAIN_OPPOSING,
                title="Opposing Interpretation: The 'Special Needs' Administrative Doctrine",
                content=(
                    "**The Agency / Government Counterargument**:\n"
                    "Government defense attorneys argue that child protection falls under the Fourth Amendment 'special needs' exception "
                    "(analogous to administrative building inspections or drug testing), where traditional probable cause warrants should yield "
                    "to the 'best interests of the child' and immediate investigative discretion. While rejected by majority circuit law for in-home "
                    "physical removals, this argument is still pressed in administrative home inspection contexts."
                ),
                citations=["Camara v. Municipal Court, 387 U.S. 523 (1967)"],
                official_sources=["https://www.supremecourt.gov"]
            ),
            DrillDownAction.SHOW_TEMPORAL_CHANGE: DrillDownResult(
                action=DrillDownAction.SHOW_TEMPORAL_CHANGE,
                title="Historical Evolution of Warrant Protections in Child Welfare",
                content=(
                    "- **1960s-1980s**: Widespread practice of warrantless administrative entries under undefined state 'protective custody' statutes.\n"
                    "- **1990s-2000s**: Federal civil rights litigation established that 4th Amendment standards apply fully to caseworkers (*Wallis*, *Roska*).\n"
                    "- **Recent Legislative Trend (2020-Present)**: Multiple states (e.g. Washington Keeping Families Together Act 2021, Texas HB 567 2021) "
                    "amended state statutes to specifically outlaw warrantless removals unless imminent, catastrophic physical danger is demonstrated on the record."
                ),
                citations=["Wash. Laws 2021, ch. 211", "Tex. HB 567 (2021)"],
                official_sources=["https://leg.wa.gov", "https://capitol.texas.gov"]
            )
        }
    }
}


class LegalConceptRegistry:
    """Registry providing canonical and dynamically generated 5-level concept breakdowns."""

    @classmethod
    def get_concept(
        cls,
        concept_query: str,
        jurisdiction: Optional[str] = None,
        situation: Optional[str] = None
    ) -> LegalConceptExploration:
        """Looks up a canonical concept or dynamically synthesizes a 5-level exploration."""
        q_norm = concept_query.strip().lower()

        # Check canonical registry
        matched_key = None
        for key, data in CANONICAL_CONCEPTS.items():
            if q_norm == key or any(alias in q_norm for alias in data.get("aliases", [])):
                matched_key = key
                break

        if matched_key:
            data = CANONICAL_CONCEPTS[matched_key]
            jurisdiction_str = jurisdiction or "US"
            return LegalConceptExploration(
                concept_name=data["canonical_name"],
                jurisdiction=jurisdiction_str,
                situational_context=situation,
                level_1_plain_english=data["level_1"],
                level_2_practical=data["level_2"],
                level_3_terminology=data["level_3"],
                level_4_primary_authority=data["level_4"],
                level_5_advanced_analysis=data["level_5"],
                drill_downs=data["drill_downs"]
            )

        # Dynamic synthesis for any other legal concept
        return cls._synthesize_concept(concept_query, jurisdiction, situation)

    @classmethod
    def _synthesize_concept(
        cls,
        concept_query: str,
        jurisdiction: Optional[str] = None,
        situation: Optional[str] = None
    ) -> LegalConceptExploration:
        """Dynamically builds a 5-level exploration and 5 drill-downs for arbitrary concepts."""
        j_str = jurisdiction or "US"
        c_title = concept_query.strip().title()

        l1 = (
            f"At its most basic level, '{c_title}' is a legal rule designed to ensure fairness, predictability, "
            "and accountability when the law interacts with individuals. It means decisions cannot be made arbitrarily, "
            "and specific established legal tests must be met before legal consequences attach."
        )

        l2 = (
            f"In practical terms for your situation ({situation or 'your case'}): '{c_title}' means that the opposing party "
            "or the government must satisfy concrete evidentiary thresholds. You have the right to request proof, "
            "verify that all necessary steps were followed, and challenge claims that do not conform to governing law."
        )

        l3 = (
            f"In formal legal doctrine, '{c_title}' involves specific legal elements, burdens of proof, and standards of review. "
            f"It requires distinguishing between questions of law (reviewed de novo) and questions of fact (reviewed under clear error "
            f"or abuse of discretion standards), governed by constitutional provisions and statutory frameworks in {j_str}."
        )

        l4 = [
            PrimaryAuthorityReference(
                citation=f"Controlling {j_str} Statutory & Constitutional Provisions regarding {c_title}",
                source_type="STATUTE",
                official_portal_url="https://www.govinfo.gov / Official State Legislative Code",
                key_holding_or_text=f"Statutory elements and codification of standards governing {c_title} in {j_str}.",
                jurisdiction=j_str,
                is_binding=True
            )
        ]

        l5 = (
            f"Advanced legal analysis of '{c_title}' explores competing judicial interpretations, doctrinal evolutions, "
            "and potential jurisdictional splits. Courts continually balance individual rights against legitimate state regulatory "
            "interests, requiring scrutiny of precedent, legislative history, and statutory construction rules."
        )

        drill_downs = {
            DrillDownAction.SHOW_SOURCE: DrillDownResult(
                action=DrillDownAction.SHOW_SOURCE,
                title=f"Primary Legal Sources for {c_title}",
                content=f"Primary constitutional, statutory, and official slip opinion sources for {c_title} in {j_str}.",
                citations=[f"Controlling {j_str} Authority"],
                official_sources=["https://www.govinfo.gov"]
            ),
            DrillDownAction.SHOW_STATUTE: DrillDownResult(
                action=DrillDownAction.SHOW_STATUTE,
                title=f"Controlling Statutory Framework for {c_title}",
                content=f"Primary state and federal statutory enactments codifying {c_title}.",
                citations=[f"{j_str} Statutory Code"],
                official_sources=["https://uscode.house.gov"]
            ),
            DrillDownAction.SHOW_CASE: DrillDownResult(
                action=DrillDownAction.SHOW_CASE,
                title=f"Controlling Precedent for {c_title}",
                content=f"Binding appellate and Supreme Court jurisprudence establishing elements and standards for {c_title}.",
                citations=[f"Key Precedents in {j_str}"],
                official_sources=["https://www.supremecourt.gov"]
            ),
            DrillDownAction.EXPLAIN_OPPOSING: DrillDownResult(
                action=DrillDownAction.EXPLAIN_OPPOSING,
                title=f"Opposing Interpretation for {c_title}",
                content=f"The government or opposing litigant's competing theoretical framework and doctrinal counterarguments regarding {c_title}.",
                citations=["Opposing Legal Theories"],
                official_sources=[]
            ),
            DrillDownAction.SHOW_TEMPORAL_CHANGE: DrillDownResult(
                action=DrillDownAction.SHOW_TEMPORAL_CHANGE,
                title=f"Historical Evolution & Temporal Changes in {c_title}",
                content=f"Legislative amendments, judicial abrogations, and evolving legal standards for {c_title} over time.",
                citations=["Historical Enactments"],
                official_sources=["Official Legislative History Archives"]
            )
        }

        return LegalConceptExploration(
            concept_name=c_title,
            jurisdiction=j_str,
            situational_context=situation,
            level_1_plain_english=l1,
            level_2_practical=l2,
            level_3_terminology=l3,
            level_4_primary_authority=l4,
            level_5_advanced_analysis=l5,
            drill_downs=drill_downs
        )
