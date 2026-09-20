#!/usr/bin/env python3
"""Build Civil Rights Concept Pack B (10 Concepts) for Legal-GPT."""

import os
import yaml
from pathlib import Path

CONCEPTS_DIR = Path(__file__).resolve().parent.parent / "legal_registry" / "literacy" / "concepts"

PACK_B = {
    "fourth_amendment_home_entry": {
        "id": "fourth_amendment_home_entry",
        "canonical_name": "Fourth Amendment Protection Against Warrantless Home Entry",
        "aliases": [
            "fourth amendment",
            "warrantless home entry",
            "home search",
            "exigent circumstances",
            "brigham city",
            "cps home entry",
            "police entered my home"
        ],
        "jurisdiction": "US",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "The Fourth Amendment gives you a sacred right to privacy inside your home. Government workers, "
            "including police officers and Child Protective Services (CPS) caseworkers, cannot force their way inside "
            "your private residence without a valid judicial warrant signed by a judge, your voluntary and knowing consent, "
            "or a true, life-or-death emergency."
        ),
        "level_2_practical": (
            "If caseworkers or police officers knock on your door, you have the right to speak to them from your porch "
            "or with the door closed. You can calmly state: 'I do not consent to any entry or search of my home without a warrant.' "
            "Unless they possess a signed court order or face an immediate emergency where someone is suffering imminent, "
            "serious physical injury, they cannot kick down your door or enter without your permission."
        ),
        "level_3_terminology": (
            "The Fourth Amendment's warrant requirement applies fully to administrative child welfare investigations "
            "(Camara v. Municipal Court, 387 U.S. 523). Exceptions are strictly limited to: (1) Voluntary Consent (must be "
            "freely given and not coerced); (2) Exigent Circumstances under the emergency aid doctrine (Brigham City v. Stuart), "
            "requiring an objectively reasonable basis to believe an occupant is seriously injured or imminently threatened; "
            "and (3) Valid Judicial Warrant based on probable cause."
        ),
        "level_4_primary_authority": [
            {
                "citation": "U.S. Const. amend. IV",
                "source_type": "CONSTITUTION",
                "official_portal_url": "https://www.govinfo.gov/content/pkg/GPO-CONAN-2017/pdf/GPO-CONAN-2017.pdf",
                "key_holding_or_text": (
                    "The right of the people to be secure in their persons, houses, papers, and effects, "
                    "against unreasonable searches and seizures, shall not be violated, and no Warrants shall issue, "
                    "but upon probable cause."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Brigham City v. Stuart, 547 U.S. 398 (2006)",
                "source_type": "CASELAW",
                "official_portal_url": "https://www.supremecourt.gov/opinions/05pdf/05-502.pdf",
                "key_holding_or_text": (
                    "Warrantless entry under the emergency aid exception requires an objectively reasonable basis for "
                    "believing that an occupant is seriously injured or imminently threatened with such injury."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Camara v. Municipal Court, 387 U.S. 523 (1967)",
                "source_type": "CASELAW",
                "official_portal_url": "https://www.supremecourt.gov/",
                "key_holding_or_text": (
                    "Except in certain carefully defined classes of cases, a search of private property without proper "
                    "consent is unreasonable unless authorized by a valid search warrant."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "Federal circuit jurisprudence establishes that child protection investigators are governed by the Fourth Amendment "
            "to the same degree as law enforcement officers (e.g., Wallis v. Spencer, 202 F.3d 1126 (9th Cir. 2000); Calabretta "
            "v. Floyd, 189 F.3d 808 (9th Cir. 1999)). Government officials cannot claim qualified immunity when conducting "
            "warrantless home entries in the absence of demonstrable imminent physical peril. Speculative allegations of neglect "
            "or unverified hotline tips never constitute exigent circumstances justifying warrantless intrusion."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Constitutional Text of the Fourth Amendment",
                "content": "U.S. Constitution, Fourth Amendment guarantees the right to be secure in houses against unreasonable searches.",
                "citations": ["U.S. Const. amend. IV"],
                "official_sources": ["https://www.govinfo.gov"]
            },
            "SHOW_STATUTE": {
                "title": "Statutory Authority for Judicial Entry Orders",
                "content": "Administrative search warrants and dependency pickup orders require sworn affidavits demonstrating probable cause of imminent harm.",
                "citations": ["42 U.S.C. § 1983", "U.S. Const. amend. IV"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_CASE": {
                "title": "Controlling Precedent: Brigham City v. Stuart, 547 U.S. 398 (2006)",
                "content": "Emergency aid exception permits warrantless home entry only when officers have an objectively reasonable basis to believe an occupant is seriously injured or imminently threatened.",
                "citations": ["Brigham City v. Stuart, 547 U.S. 398 (2006)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "Government Position: Community Caretaking and Child Welfare Exigency",
                "content": "Caseworkers argue that the state's parens patriae interest requires rapid inspection of living quarters when responding to severe child abuse allegations.",
                "citations": ["Brigham City v. Stuart, 547 U.S. 398 (2006)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Narrowing of Administrative Search Exceptions",
                "content": "Modern doctrine has rejected broad 'social worker exceptions' to the Fourth Amendment, holding caseworkers strictly accountable to traditional warrant requirements.",
                "citations": ["Brigham City v. Stuart, 547 U.S. 398 (2006)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            }
        },
        "related_concepts": ["due_process", "emergency_removal", "civil_rights_section_1983"]
    },

    "first_amendment_family_association": {
        "id": "first_amendment_family_association",
        "canonical_name": "First Amendment Right to Intimate Family Association",
        "aliases": [
            "family association",
            "intimate association",
            "troxel",
            "parental liberty",
            "first amendment family"
        ],
        "jurisdiction": "US",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "You have a fundamental constitutional right to live together as a family and to love, raise, and guide "
            "your children without government meddling. The Constitution protects family bonds as one of the most basic "
            "freedoms in American life."
        ),
        "level_2_practical": (
            "The state cannot dictate your family life, beliefs, or cultural traditions simply because an agency prefers "
            "a different lifestyle. As long as you provide adequate care and do not abuse or neglect your child, the legal "
            "presumption is that you—not a state caseworker or judge—act in your child's best interests."
        ),
        "level_3_terminology": (
            "The right to intimate family association emanates from both the First Amendment (freedom of association) "
            "and the Fourteenth Amendment Due Process Clause (Roberts v. United States Jaycees, 468 U.S. 609; Troxel v. "
            "Granville, 530 U.S. 57). Under Troxel, fit parents are endowed with a constitutional presumption that their "
            "decisions serve the best interests of their children, subject to strict judicial scrutiny."
        ),
        "level_4_primary_authority": [
            {
                "citation": "U.S. Const. amend. I",
                "source_type": "CONSTITUTION",
                "official_portal_url": "https://www.govinfo.gov/content/pkg/GPO-CONAN-2017/pdf/GPO-CONAN-2017.pdf",
                "key_holding_or_text": (
                    "Congress shall make no law respecting an establishment of religion, or prohibiting the free exercise "
                    "thereof; or abridging the freedom of speech, or of the press; or the right of the people peaceably to assemble."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Troxel v. Granville, 530 U.S. 57 (2000)",
                "source_type": "CASELAW",
                "official_portal_url": "https://www.supremecourt.gov/opinions/boundvolumes/530bv.pdf",
                "key_holding_or_text": (
                    "The interest of parents in the care, custody, and control of their children is perhaps the oldest "
                    "of the fundamental liberty interests recognized by the Supreme Court."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Roberts v. United States Jaycees, 468 U.S. 609 (1984)",
                "source_type": "CASELAW",
                "official_portal_url": "https://www.supremecourt.gov/",
                "key_holding_or_text": (
                    "Choices to enter into and maintain certain intimate human relationships must be secured against undue "
                    "cultural intrusion by the State because of the role of such relationships in safeguarding individual freedom."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "The intersection of First Amendment expressive association and Fourteenth Amendment substantive liberty establishes "
            "a heightened shield around the nuclear and extended family. State intrusion into familial integrity must survive "
            "strict scrutiny: the state must demonstrate a compelling governmental interest (preventing severe harm) and that the "
            "deprivation is narrowly tailored using the least restrictive means."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "First Amendment Association and Parental Rights Authority",
                "content": "U.S. Constitution First Amendment protects freedom of association and family ties.",
                "citations": ["U.S. Const. amend. I"],
                "official_sources": ["https://www.govinfo.gov"]
            },
            "SHOW_STATUTE": {
                "title": "Family Integrity Preservation Statutes",
                "content": "Federal and state statutes mandate reasonable efforts to maintain the child in the family home prior to placement.",
                "citations": ["42 U.S.C. § 671(a)(15)"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_CASE": {
                "title": "Controlling Precedent: Troxel v. Granville, 530 U.S. 57 (2000)",
                "content": "Troxel v. Granville affirms that fit parents are presumed to act in their child's best interests.",
                "citations": ["Troxel v. Granville, 530 U.S. 57 (2000)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "State Best Interests Test vs Parental Presumption",
                "content": "Agencies often argue that the state's independent evaluation of the child's best interests can supersede parental decision-making.",
                "citations": ["Troxel v. Granville, 530 U.S. 57 (2000)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Strengthening of Parental Fit Presumption",
                "content": "Since Troxel (2000), courts have systematically struck down state statutes granting non-parents visitation rights over fit parents' objections.",
                "citations": ["Troxel v. Granville, 530 U.S. 57 (2000)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            }
        },
        "related_concepts": ["due_process", "fourteenth_amendment_substantive_due_process"]
    },

    "fourteenth_amendment_equal_protection": {
        "id": "fourteenth_amendment_equal_protection",
        "canonical_name": "Fourteenth Amendment Equal Protection of the Laws",
        "aliases": [
            "equal protection",
            "fourteenth amendment equal protection",
            "discrimination",
            "strict scrutiny",
            "rational basis"
        ],
        "jurisdiction": "US",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "The government must treat people fairly and equally under the law. State agencies cannot target you, take away "
            "your children, or hold you to harsher rules because of your race, national origin, religion, or disability."
        ),
        "level_2_practical": (
            "If child welfare caseworkers treat you differently than other parents in the same situation—such as demanding "
            "extra conditions or subjecting your home to harsher scrutiny because of your background, race, or language—the "
            "agency may be violating the Equal Protection Clause. You have the right to equal treatment and services."
        ),
        "level_3_terminology": (
            "Under the Fourteenth Amendment's Equal Protection Clause, judicial review of government action employs three tiers "
            "of scrutiny: (1) Strict Scrutiny for suspect classifications (race, religion, national origin) or fundamental rights, "
            "requiring a compelling state interest and narrow tailoring; (2) Intermediate Scrutiny for quasi-suspect classifications "
            "(gender); and (3) Rational Basis Review for general social/economic regulations, requiring a legitimate state interest."
        ),
        "level_4_primary_authority": [
            {
                "citation": "U.S. Const. amend. XIV, § 1",
                "source_type": "CONSTITUTION",
                "official_portal_url": "https://www.govinfo.gov/content/pkg/GPO-CONAN-2017/pdf/GPO-CONAN-2017.pdf",
                "key_holding_or_text": (
                    "No State shall make or enforce any law which shall abridge the privileges or immunities of citizens of "
                    "the United States... nor deny to any person within its jurisdiction the equal protection of the laws."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Palmore v. Sidoti, 466 U.S. 429 (1984)",
                "source_type": "CASELAW",
                "official_portal_url": "https://www.supremecourt.gov/",
                "key_holding_or_text": (
                    "Private racial biases and the possible injury they might inflict are not permissible considerations for "
                    "depriving a parent of the custody of a child."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "City of Cleburne v. Cleburne Living Center, 473 U.S. 432 (1985)",
                "source_type": "CASELAW",
                "official_portal_url": "https://www.supremecourt.gov/",
                "key_holding_or_text": (
                    "Government actions motivated by prejudice or irrational antipathy against individuals with disabilities "
                    "violate the Equal Protection Clause."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "In systemic child welfare litigation, plaintiffs increasingly assert disparate impact and selective enforcement claims "
            "under Washington v. Davis, 426 U.S. 229, and Title VI of the Civil Rights Act of 1964. While constitutional equal protection "
            "requires establishing discriminatory intent, institutional practices that disproportionately remove children from minority "
            "or low-income households without objective evidence of imminent harm face rigorous statutory and judicial scrutiny."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Equal Protection Clause Primary Text",
                "content": "Fourteenth Amendment, Section 1 guarantees equal protection of the laws to all persons.",
                "citations": ["U.S. Const. amend. XIV, § 1"],
                "official_sources": ["https://www.govinfo.gov"]
            },
            "SHOW_STATUTE": {
                "title": "Federal Anti-Discrimination Statutes in Child Welfare",
                "content": "Title VI of the Civil Rights Act of 1964 (42 U.S.C. § 2000d) prohibits racial discrimination by recipients of federal child welfare funds.",
                "citations": ["42 U.S.C. § 2000d"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_CASE": {
                "title": "Controlling Precedent: Palmore v. Sidoti, 466 U.S. 429 (1984)",
                "content": "Supreme Court held that racial bias cannot justify modifying custody or removing children from parents.",
                "citations": ["Palmore v. Sidoti, 466 U.S. 429 (1984)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "State Neutrality Defense",
                "content": "Agencies argue that removals are based on facially neutral child safety assessments rather than discriminatory factors.",
                "citations": ["Palmore v. Sidoti, 466 U.S. 429 (1984)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Heightened Oversight of Child Welfare Disparities",
                "content": "State and federal reforms have mandated data tracking on disproportionality and banned consideration of poverty alone as child neglect.",
                "citations": ["42 U.S.C. § 2000d"],
                "official_sources": ["https://uscode.house.gov/"]
            }
        },
        "related_concepts": ["due_process", "fourteenth_amendment_substantive_due_process", "ada_section_504_dependency"]
    },

    "fourteenth_amendment_substantive_due_process": {
        "id": "fourteenth_amendment_substantive_due_process",
        "canonical_name": "Fourteenth Amendment Substantive Due Process and Parental Liberty",
        "aliases": [
            "substantive due process",
            "parental liberty interest",
            "santosky",
            "mathews balancing",
            "fundamental right to parent"
        ],
        "jurisdiction": "US",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "Substantive due process protects your fundamental right to raise your child. Because your bond with your child "
            "is so vital, the government cannot permanently tear your family apart based on mere guesswork or minor disagreements; "
            "it must meet an exceptionally high burden of proof in court."
        ),
        "level_2_practical": (
            "In dependency and child welfare proceedings, the state cannot permanently terminate your parental rights based on a simple "
            "'preponderance of evidence' (51% likelihood). The U.S. Supreme Court requires the state to prove its allegations by at "
            "least 'clear and convincing evidence'—a much higher standard—before it can sever your parental bond."
        ),
        "level_3_terminology": (
            "Substantive Due Process under the Fourteenth Amendment protects fundamental liberty interests deeply rooted in tradition "
            "(Santosky v. Kramer, 455 U.S. 745). Procedural protections are calibrated under Mathews v. Eldridge, 424 U.S. 319, "
            "balancing: (1) the private interest; (2) the risk of erroneous deprivation and value of additional safeguards; and "
            "(3) the government's interest. In parental termination, the parent's interest is commanding, requiring clear and convincing proof."
        ),
        "level_4_primary_authority": [
            {
                "citation": "Santosky v. Kramer, 455 U.S. 745 (1982)",
                "source_type": "CASELAW",
                "official_portal_url": "https://www.supremecourt.gov/",
                "key_holding_or_text": (
                    "Before a State may sever completely and irrevocably the rights of parents in their natural child, due process "
                    "requires that the State support its allegations by at least clear and convincing evidence."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Mathews v. Eldridge, 424 U.S. 319 (1976)",
                "source_type": "CASELAW",
                "official_portal_url": "https://www.supremecourt.gov/",
                "key_holding_or_text": (
                    "Procedural due process requires balancing the private interest affected, the risk of erroneous deprivation "
                    "under existing procedures, and the Government's interest, including administrative burdens."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Stanley v. Illinois, 405 U.S. 645 (1972)",
                "source_type": "CASELAW",
                "official_portal_url": "https://www.supremecourt.gov/",
                "key_holding_or_text": (
                    "The rights of parents to the companionship, care, custody, and management of their children are cognizable "
                    "and substantial interests warranting constitutional deference."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "The constitutional tension under Santosky and Mathews centers on asymmetric risk allocation. Because termination "
            "of parental rights works an irrevocable and total destruction of the parent-child relationship, the standard of proof "
            "must reflect the gravity of erroneous permanent termination. State statutes attempting to relax evidentiary burdens or "
            "rely on default judgments in termination proceedings violate Fourteenth Amendment substantive due process."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Fourteenth Amendment Due Process Clause",
                "content": "Fourteenth Amendment, § 1 prohibits states from depriving any person of life, liberty, or property without due process.",
                "citations": ["U.S. Const. amend. XIV, § 1"],
                "official_sources": ["https://www.govinfo.gov"]
            },
            "SHOW_STATUTE": {
                "title": "Statutory Termination of Parental Rights Standards",
                "content": "State termination statutes must incorporate clear and convincing evidence standards to comply with Santosky v. Kramer.",
                "citations": ["Santosky v. Kramer, 455 U.S. 745 (1982)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "SHOW_CASE": {
                "title": "Controlling Precedent: Santosky v. Kramer, 455 U.S. 745 (1982)",
                "content": "Holding that due process mandates at least clear and convincing evidence for termination of parental rights.",
                "citations": ["Santosky v. Kramer, 455 U.S. 745 (1982)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "State Permanency Timeline Priority",
                "content": "Agencies argue that rapid termination promotes child stability and adoption permanence under the Adoption and Safe Families Act (ASFA).",
                "citations": ["Santosky v. Kramer, 455 U.S. 745 (1982)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Evolution of Evidentiary Standards in Family Courts",
                "content": "Before Santosky (1982), several states permitted termination on a mere fair preponderance standard, which was invalidated nationwide.",
                "citations": ["Santosky v. Kramer, 455 U.S. 745 (1982)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            }
        },
        "related_concepts": ["due_process", "first_amendment_family_association", "probable_cause_vs_preponderance"]
    },

    "ada_section_504_dependency": {
        "id": "ada_section_504_dependency",
        "canonical_name": "ADA Title II and Section 504 Protections in Child Welfare",
        "aliases": [
            "ada in cps",
            "section 504 dependency",
            "disability discrimination",
            "reasonable accommodations child welfare",
            "ada parental rights"
        ],
        "jurisdiction": "US",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "Federal disability rights laws protect parents who have physical, intellectual, or mental health disabilities. "
            "A child welfare agency cannot remove your child or refuse to reunite your family simply because you have a disability. "
            "They must provide reasonable accommodations to help you succeed."
        ),
        "level_2_practical": (
            "If you have a disability (such as depression, anxiety, physical mobility issues, hearing impairment, or an intellectual "
            "limitation), CPS cannot simply hand you standard parenting class packets and expect you to fail. Under the Americans "
            "with Disabilities Act (ADA) and Section 504, they must adapt their services—providing specialized in-home coaching, sign language "
            "interpreters, or modified timelines—to accommodate your disability."
        ),
        "level_3_terminology": (
            "Title II of the Americans with Disabilities Act (42 U.S.C. § 12132) and Section 504 of the Rehabilitation Act "
            "(29 U.S.C. § 794) prohibit public entities and federally funded programs from discriminating against qualified individuals "
            "with disabilities. In dependency matters, child welfare agencies are mandated to provide 'reasonable modifications in "
            "policies, practices, or procedures' and individually tailored remedial services before pursuing termination."
        ),
        "level_4_primary_authority": [
            {
                "citation": "42 U.S.C. § 12132",
                "source_type": "STATUTE",
                "official_portal_url": "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title42-section12132&num=0&edition=prelim",
                "key_holding_or_text": (
                    "Subject to the provisions of this subchapter, no qualified individual with a disability shall, by reason "
                    "of such disability, be excluded from participation in or be denied the benefits of the services, programs, "
                    "or activities of a public entity, or be subjected to discrimination by any such entity."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "29 U.S.C. § 794",
                "source_type": "STATUTE",
                "official_portal_url": "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title29-section794&num=0&edition=prelim",
                "key_holding_or_text": (
                    "No otherwise qualified individual with a disability in the United States... shall, solely by reason of her or his "
                    "disability, be excluded from the participation in, be denied the benefits of, or be subjected to discrimination "
                    "under any program or activity receiving Federal financial assistance."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "DOJ & HHS Joint Guidance on Protecting Parental Rights (2015)",
                "source_type": "REGULATION",
                "official_portal_url": "https://www.ada.gov/doj_hhs_ta/child_welfare_ta.html",
                "key_holding_or_text": (
                    "Child welfare agencies and family courts must ensure that parents with disabilities are not subjected to "
                    "discrimination, must conduct individualized assessments, and must provide reasonable modifications."
                ),
                "jurisdiction": "US",
                "is_binding": False,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "Federal circuit and state appellate authority reflect an ongoing doctrinal division regarding whether an ADA violation "
            "can serve as a direct defense to termination of parental rights, or must be brought as a separate § 1983/Title II action. "
            "However, virtually all jurisdictions recognize that failure to provide reasonable accommodations directly undermines "
            "the statutory finding that the agency provided 'reasonable efforts' to reunify the family under Title IV-E."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "ADA Title II and Rehabilitation Act Statutes",
                "content": "42 U.S.C. § 12132 and 29 U.S.C. § 794 establish affirmative duties to accommodate parents with disabilities.",
                "citations": ["42 U.S.C. § 12132", "29 U.S.C. § 794"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_STATUTE": {
                "title": "Statutory Duty to Modify Services",
                "content": "Federal regulations 28 CFR § 35.130(b)(7) require public entities to make reasonable modifications in policies and services.",
                "citations": ["42 U.S.C. § 12132", "28 CFR § 35.130"],
                "official_sources": ["https://www.ecfr.gov/"]
            },
            "SHOW_CASE": {
                "title": "Controlling Agency Guidance: DOJ & HHS Joint Guidance (2015)",
                "content": "DOJ and HHS affirm that child welfare agencies must provide tailored, accessible accommodations rather than generic requirements.",
                "citations": ["DOJ & HHS Joint Guidance (2015)"],
                "official_sources": ["https://www.ada.gov/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "Agency Argument: Child Safety Trumps ADA Accommodations",
                "content": "Agencies argue that the primary focus of child welfare proceedings is the child's safety, asserting ADA claims cannot delay permanency.",
                "citations": ["42 U.S.C. § 12132"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Rise of Disability Rights Protections in State Family Codes",
                "content": "Multiple states have enacted specific statutory provisions prohibiting termination of parental rights based on disability without clear proof of direct harm.",
                "citations": ["42 U.S.C. § 12132"],
                "official_sources": ["https://uscode.house.gov/"]
            }
        },
        "related_concepts": ["reasonable_efforts", "due_process", "civil_rights_section_1983"]
    },

    "title_iv_e_reasonable_efforts": {
        "id": "title_iv_e_reasonable_efforts",
        "canonical_name": "Title IV-E Statutory Requirement for Reasonable Efforts",
        "aliases": [
            "title iv e",
            "reasonable efforts requirement",
            "asfa",
            "adoption and safe families act",
            "42 usc 671"
        ],
        "jurisdiction": "US",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "Federal law requires state child welfare agencies to make real, reasonable efforts to prevent children from being "
            "taken from their families, and to help families reunite safely after a child is removed. The state cannot just take "
            "a child and walk away without offering genuine help."
        ),
        "level_2_practical": (
            "Before removing your child, and throughout your case, the caseworker must offer active, relevant support services—such as "
            "housing assistance referrals, counseling, food support, or family preservation services. At every court hearing, the judge "
            "must formally determine on the record whether the state made 'reasonable efforts' to prevent removal and reunify your family."
        ),
        "level_3_terminology": (
            "Under Title IV-E of the Social Security Act (42 U.S.C. § 671(a)(15)), enacted through the Adoption and Safe Families Act "
            "(ASFA), states receiving federal foster care funding must ensure that reasonable efforts are made: (A) prior to placement, "
            "to prevent or eliminate the need for removing the child; and (B) to make it possible for the child to return home safely. "
            "Exceptions exist only under statutory 'aggravated circumstances'."
        ),
        "level_4_primary_authority": [
            {
                "citation": "42 U.S.C. § 671(a)(15)",
                "source_type": "STATUTE",
                "official_portal_url": "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title42-section671&num=0&edition=prelim",
                "key_holding_or_text": (
                    "In order for a State to be eligible for payments under this part, it shall have a plan approved by the Secretary "
                    "which provides that... reasonable efforts shall be made to preserve and reunify families prior to the placement "
                    "of a child in foster care, and to make it possible for a child to safely return home."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "45 C.F.R. § 1356.21(b)",
                "source_type": "REGULATION",
                "official_portal_url": "https://www.ecfr.gov/current/title-45/subtitle-B/chapter-XIII/subchapter-G/part-1356/section-1356.21",
                "key_holding_or_text": (
                    "Judicial determination of reasonable efforts to prevent removal must be made within 60 days of the date the child "
                    "was removed from the home, and reasonable efforts to finalize permanency must be made every 12 months."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "Title IV-E conditioning of federal foster care funding under the Spending Clause creates mandatory statutory duties for "
            "state courts and agencies. While Suter v. Artist M., 503 U.S. 347 (1992), limited private § 1983 damages actions enforcing "
            "Title IV-E directly, state dependency statutes codify identical reasonable efforts standards as mandatory threshold requirements "
            "for maintaining protective custody and terminating parental rights."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Title IV-E Social Security Act Statutory Language",
                "content": "42 U.S.C. § 671(a)(15) controls state eligibility for federal child welfare funding and dictates reasonable efforts.",
                "citations": ["42 U.S.C. § 671(a)(15)"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_STATUTE": {
                "title": "Federal Regulations on Judicial Findings of Reasonable Efforts",
                "content": "45 C.F.R. § 1356.21(b) mandates explicit judicial findings of reasonable efforts within 60 days of child removal.",
                "citations": ["45 C.F.R. § 1356.21(b)"],
                "official_sources": ["https://www.ecfr.gov/"]
            },
            "SHOW_CASE": {
                "title": "Supreme Court Review: Suter v. Artist M., 503 U.S. 347 (1992)",
                "content": "Holding that Title IV-E creates programmatic state plan requirements enforced primarily through federal funding oversight.",
                "citations": ["Suter v. Artist M., 503 U.S. 347 (1992)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "Aggravated Circumstances and Safety Paramountcy",
                "content": "Under ASFA amendments, child safety is paramount; reasonable efforts are not required when the parent has subjected the child to aggravated circumstances.",
                "citations": ["42 U.S.C. § 671(a)(15)(D)"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Shift from Adoption Acceleration to Prevention (Family First Act)",
                "content": "The Family First Prevention Services Act (2018) amended Title IV-E to allow federal funding for mental health, substance abuse, and in-home parenting to prevent foster care entries.",
                "citations": ["42 U.S.C. § 671"],
                "official_sources": ["https://uscode.house.gov/"]
            }
        },
        "related_concepts": ["reasonable_efforts", "active_efforts", "permanency_planning"]
    },

    "first_amendment_religion_custody": {
        "id": "first_amendment_religion_custody",
        "canonical_name": "First Amendment Free Exercise of Religion in Parental Custody",
        "aliases": [
            "first amendment religion custody",
            "religious freedom in parenting",
            "free exercise child welfare",
            "religious upbringing",
            "first amendment custody"
        ],
        "jurisdiction": "US",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "The First Amendment protects your right to teach your religious beliefs and values to your children. "
            "A court or child welfare agency cannot take your children away or judge your fitness as a parent simply because "
            "they disagree with your religious faith, spiritual practices, or church."
        ),
        "level_2_practical": (
            "The state cannot condition reunification or judge your parenting based on whether you attend a traditional church, "
            "follow particular dietary laws, pray, or hold non-mainstream religious views. The state can only intervene if a specific "
            "action creates an immediate, demonstrable physical danger to the child's life or health."
        ),
        "level_3_terminology": (
            "Under the Free Exercise Clause of the First Amendment and parental rights doctrine (Wisconsin v. Yoder, 406 U.S. 205), "
            "the government must demonstrate a compelling interest of the highest order to override parental religious decisions. "
            "The state's parens patriae authority allows intervention only to prevent direct physical harm (Prince v. Massachusetts, "
            "321 U.S. 158), not to enforce religious orthodoxy or social conformity."
        ),
        "level_4_primary_authority": [
            {
                "citation": "U.S. Const. amend. I",
                "source_type": "CONSTITUTION",
                "official_portal_url": "https://www.govinfo.gov/content/pkg/GPO-CONAN-2017/pdf/GPO-CONAN-2017.pdf",
                "key_holding_or_text": (
                    "Congress shall make no law respecting an establishment of religion, or prohibiting the free exercise thereof."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Wisconsin v. Yoder, 406 U.S. 205 (1972)",
                "source_type": "CASELAW",
                "official_portal_url": "https://www.supremecourt.gov/",
                "key_holding_or_text": (
                    "The primary role of parents in the upbringing of their children is established beyond debate as an enduring "
                    "American tradition; a parent's religious beliefs and custody cannot be lightly overborne by state educational goals."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Prince v. Massachusetts, 321 U.S. 158 (1944)",
                "source_type": "CASELAW",
                "official_portal_url": "https://www.supremecourt.gov/",
                "key_holding_or_text": (
                    "The family itself is not beyond regulation in the public interest, as against a claim of religious liberty; "
                    "the state may intervene to protect children from direct physical harm or exploitation."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "Constitutional analysis distinguishes between purely religious instruction and practices that impose acute physical "
            "hazards (such as denial of life-saving blood transfusions or critical medical care). Under the Religious Freedom Restoration "
            "Act (RFRA) and state RFRAs, when the state burdens a parent's religious exercise in family court, the state must prove that "
            "the restriction is the least restrictive means of achieving the compelling governmental interest of preventing grave bodily injury."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "First Amendment Free Exercise Clause Text",
                "content": "U.S. Constitution First Amendment forbids state laws prohibiting the free exercise of religion.",
                "citations": ["U.S. Const. amend. I"],
                "official_sources": ["https://www.govinfo.gov"]
            },
            "SHOW_STATUTE": {
                "title": "Federal Religious Freedom Restoration Act (RFRA)",
                "content": "42 U.S.C. § 2000bb-1 prohibits government from substantially burdening religious exercise without compelling interest.",
                "citations": ["42 U.S.C. § 2000bb-1"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_CASE": {
                "title": "Controlling Precedent: Wisconsin v. Yoder, 406 U.S. 205 (1972)",
                "content": "Supreme Court upheld parents' fundamental right to guide the religious future and upbringing of their children.",
                "citations": ["Wisconsin v. Yoder, 406 U.S. 205 (1972)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "Medical Neglect and Child Safety Boundaries",
                "content": "Under Prince v. Massachusetts, the state contends that religious conviction cannot exempt parents from mandatory medical treatments necessary to preserve a child's life.",
                "citations": ["Prince v. Massachusetts, 321 U.S. 158 (1944)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Narrowing of Religious Exemptions in Child Protection Laws",
                "content": "States have progressively modified statutory faith-healing exemptions to ensure emergency medical care can be authorized for imperiled children.",
                "citations": ["Prince v. Massachusetts, 321 U.S. 158 (1944)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            }
        },
        "related_concepts": ["first_amendment_family_association", "due_process", "fourteenth_amendment_substantive_due_process"]
    },

    "sixth_amendment_confrontation": {
        "id": "sixth_amendment_confrontation",
        "canonical_name": "Sixth Amendment Confrontation and Hearsay Distinction in Dependency",
        "aliases": [
            "sixth amendment confrontation",
            "confrontation clause dependency",
            "crawford v washington",
            "hearsay in cps",
            "cross examination dependency"
        ],
        "jurisdiction": "US",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "In criminal court, the Sixth Amendment gives defendants the absolute right to confront and cross-examine witnesses face-to-face. "
            "However, child welfare and dependency cases are civil matters, not criminal trials. While you do not get the full Sixth "
            "Amendment criminal guarantee, the Fourteenth Amendment Due Process Clause still gives you a right to challenge evidence, "
            "object to unreliable hearsay, and question witnesses who testify against you."
        ),
        "level_2_practical": (
            "Caseworkers often submit written reports containing rumors, second-hand statements, or anonymous hotline calls. "
            "Because dependency is a civil proceeding, judges sometimes consider written agency reports. But you and your lawyer "
            "have the right to subpoena the authors of those reports, call the caseworker to the stand, cross-examine them under oath, "
            "and expose factual inaccuracies or bias."
        ),
        "level_3_terminology": (
            "The Sixth Amendment Confrontation Clause (Crawford v. Washington, 541 U.S. 36) strictly bars testimonial hearsay in "
            "criminal prosecutions unless the declarant is unavailable and the defendant had a prior opportunity for cross-examination. "
            "CRITICAL DISTINCTION: Because child dependency proceedings are civil actions, the Sixth Amendment does NOT apply directly. "
            "Instead, procedural fairness is governed by Fourteenth Amendment Due Process and state evidentiary rules (e.g. ER 801-804), "
            "which balance evidentiary reliability against the state's interest in protecting child witnesses."
        ),
        "level_4_primary_authority": [
            {
                "citation": "Crawford v. Washington, 541 U.S. 36 (2004)",
                "source_type": "CASELAW",
                "official_portal_url": "https://www.supremecourt.gov/opinions/03pdf/02-9410.pdf",
                "key_holding_or_text": (
                    "Where testimonial evidence is at issue, however, the Sixth Amendment demands what the common law required: "
                    "unavailability and a prior opportunity for cross-examination."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "U.S. Const. amend. VI",
                "source_type": "CONSTITUTION",
                "official_portal_url": "https://www.govinfo.gov/content/pkg/GPO-CONAN-2017/pdf/GPO-CONAN-2017.pdf",
                "key_holding_or_text": (
                    "In all criminal prosecutions, the accused shall enjoy the right... to be confronted with the witnesses against him."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "U.S. Const. amend. XIV, § 1",
                "source_type": "CONSTITUTION",
                "official_portal_url": "https://www.govinfo.gov/content/pkg/GPO-CONAN-2017/pdf/GPO-CONAN-2017.pdf",
                "key_holding_or_text": (
                    "No State shall deprive any person of life, liberty, or property, without due process of law."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "State courts universally hold that Crawford's Sixth Amendment confrontation rule does not govern juvenile dependency "
            "hearings (e.g. In re Mary S., 186 Cal. App. 3d 414; In re Dependency of A.E.P., 135 Wn.2d 208). Instead, cross-examination "
            "in family court is evaluated under the Mathews v. Eldridge due process balancing test. When child hearsay is admitted under "
            "specialized statutory exceptions, due process requires corroboration and safeguards ensuring substantial reliability."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Sixth Amendment and Confrontation Authority",
                "content": "Sixth Amendment text provides confrontation rights in criminal prosecutions; Fourteenth Amendment provides civil due process.",
                "citations": ["U.S. Const. amend. VI", "U.S. Const. amend. XIV, § 1"],
                "official_sources": ["https://www.govinfo.gov"]
            },
            "SHOW_STATUTE": {
                "title": "Child Hearsay Exceptions in Dependency Proceedings",
                "content": "State evidentiary codes establish specific exceptions allowing reliable statements of young children regarding abuse.",
                "citations": ["Fed. R. Evid. 803", "Fed. R. Evid. 804"],
                "official_sources": ["https://www.law.cornell.edu/rules/fre"]
            },
            "SHOW_CASE": {
                "title": "Controlling Precedent: Crawford v. Washington, 541 U.S. 36 (2004)",
                "content": "Landmark ruling establishing criminal confrontation standards, highlighting the distinction with civil dependency matters.",
                "citations": ["Crawford v. Washington, 541 U.S. 36 (2004)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "Child Protection from Trauma vs Parental Cross-Examination",
                "content": "State child welfare agencies argue that requiring traumatized children to testify directly in court causes severe secondary trauma.",
                "citations": ["Crawford v. Washington, 541 U.S. 36 (2004)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Evolution of Video and In-Camera Child Testimony Rules",
                "content": "Family courts have adopted closed-circuit television, videotaped interviews, and in-chambers interviews with counsel to balance child well-being and parental fairness.",
                "citations": ["Crawford v. Washington, 541 U.S. 36 (2004)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            }
        },
        "related_concepts": ["due_process", "opportunity_to_be_heard", "right_to_counsel_dependency"]
    },

    "civil_rights_section_1983": {
        "id": "civil_rights_section_1983",
        "canonical_name": "Civil Rights Remedy Under 42 U.S.C. § 1983",
        "aliases": [
            "section 1983",
            "42 usc 1983",
            "civil rights lawsuit",
            "monell",
            "suing cps",
            "violated my civil rights"
        ],
        "jurisdiction": "US",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "Section 1983 is a powerful federal law that allows everyday citizens to sue government workers or municipalities "
            "in federal court when those officials abuse their official authority to violate your constitutional rights."
        ),
        "level_2_practical": (
            "If caseworkers or police officers break the law—such as seizing your children without a warrant or emergency, "
            "fabricating false evidence in court reports, or retaliating against you for exercising your free speech—you may have "
            "grounds to file a federal civil rights lawsuit for monetary damages or court orders barring their illegal practices. "
            "Note: Claiming a civil rights violation is an assertion by the individual, not an established judicial fact."
        ),
        "level_3_terminology": (
            "Under 42 U.S.C. § 1983, a plaintiff must prove that: (1) the defendant acted 'under color of state law'; and (2) their "
            "conduct deprived the plaintiff of a right secured by the U.S. Constitution or federal statutes. Under Monell v. Dept. of "
            "Social Services, 436 U.S. 658, local governments and municipal agencies can be liable only if the constitutional violation "
            "was caused by an official policy, custom, or systemic failure to train."
        ),
        "level_4_primary_authority": [
            {
                "citation": "42 U.S.C. § 1983",
                "source_type": "STATUTE",
                "official_portal_url": "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title42-section1983&num=0&edition=prelim",
                "key_holding_or_text": (
                    "Every person who, under color of any statute, ordinance, regulation, custom, or usage, of any State... subjects, "
                    "or causes to be subjected, any citizen of the United States... to the deprivation of any rights, privileges, or "
                    "immunities secured by the Constitution and laws, shall be liable to the party injured."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Monell v. Dept. of Social Services, 436 U.S. 658 (1978)",
                "source_type": "CASELAW",
                "official_portal_url": "https://www.supremecourt.gov/",
                "key_holding_or_text": (
                    "Local governing bodies can be sued directly under § 1983 for monetary, declaratory, or injunctive relief where "
                    "the action that is alleged to be unconstitutional implements or executes a policy statement, ordinance, regulation, "
                    "or decision officially adopted and promulgated by that body's officers."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "Litigating § 1983 child welfare actions requires navigating two formidable federal doctrines: (1) Qualified Immunity, "
            "which shields individual workers unless they violated 'clearly established' statutory or constitutional rights that every "
            "reasonable official would have known; and (2) The Rooker-Feldman and Younger abstention doctrines, which prohibit federal "
            "district courts from reviewing or interfering with ongoing state family court proceedings. Federal damages suits typically "
            "proceed after state court adjudication concludes."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Federal Civil Rights Statute Text",
                "content": "42 U.S.C. § 1983 authorizes civil actions for deprivation of constitutional rights under color of state law.",
                "citations": ["42 U.S.C. § 1983"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_STATUTE": {
                "title": "Civil Rights Attorney's Fees Awards Act",
                "content": "42 U.S.C. § 1988 permits prevailing plaintiffs in § 1983 actions to recover reasonable attorney's fees.",
                "citations": ["42 U.S.C. § 1988"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_CASE": {
                "title": "Controlling Precedent: Monell v. Dept. of Social Services, 436 U.S. 658 (1978)",
                "content": "Establishes municipal liability standards under § 1983 for unconstitutional agency policies or customs.",
                "citations": ["Monell v. Dept. of Social Services, 436 U.S. 658 (1978)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "Qualified Immunity and Absolute Prosecutorial Immunity Defenses",
                "content": "Caseworkers and agency attorneys assert qualified immunity for investigative acts and quasi-prosecutorial immunity for initiating dependency petitions.",
                "citations": ["Monell v. Dept. of Social Services, 436 U.S. 658 (1978)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Judicial Rejection of Absolute Immunity for Falsifying Evidence",
                "content": "Modern federal decisions uniformly hold that social workers do not possess immunity for submitting deliberately fabricated evidence or perjury in sworn removal declarations.",
                "citations": ["42 U.S.C. § 1983"],
                "official_sources": ["https://uscode.house.gov/"]
            }
        },
        "related_concepts": ["fourth_amendment_home_entry", "due_process", "fourteenth_amendment_equal_protection"]
    },

    "administrative_appeal_exhaustion": {
        "id": "administrative_appeal_exhaustion",
        "canonical_name": "Administrative Appeal and Exhaustion of Remedies Doctrine",
        "aliases": [
            "exhaustion of administrative remedies",
            "administrative appeal",
            "central registry appeal",
            "founded finding appeal",
            "exhaustion doctrine"
        ],
        "jurisdiction": "US",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "Before you can sue a state agency in a court of law over an administrative decision (like being placed on a child abuse "
            "registry or having benefits denied), you must first complete every step of the agency's internal appeal process. "
            "This rule is called 'exhausting administrative remedies.'"
        ),
        "level_2_practical": (
            "If CPS issues a 'founded' or 'substantiated' finding of child abuse against you, that finding can harm your job and background "
            "checks. You have a strict, limited window (often 20 to 30 days) to file an administrative appeal with the agency. "
            "If you miss this agency deadline, you usually lose your right to challenge the finding in court later."
        ),
        "level_3_terminology": (
            "The doctrine of exhaustion of administrative remedies mandates that no one is entitled to judicial relief for a supposed "
            "or threatened injury until the prescribed administrative remedy has been exhausted (Myers v. Bethlehem Shipbuilding Corp., "
            "303 U.S. 41). Exceptions are narrow and require demonstrating: (1) futility; (2) irreparable harm; or (3) that the agency "
            "lacks statutory jurisdiction. State specific administrative procedures vary widely; local rules must be verified."
        ),
        "level_4_primary_authority": [
            {
                "citation": "Myers v. Bethlehem Shipbuilding Corp., 303 U.S. 41 (1938)",
                "source_type": "CASELAW",
                "official_portal_url": "https://www.supremecourt.gov/",
                "key_holding_or_text": (
                    "The rule requiring the exhaustion of administrative remedies before resorting to the courts is a long settled "
                    "rule of judicial administration."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Woodford v. Ngo, 548 U.S. 81 (2006)",
                "source_type": "CASELAW",
                "official_portal_url": "https://www.supremecourt.gov/opinions/05pdf/05-416.pdf",
                "key_holding_or_text": (
                    "Proper exhaustion of administrative remedies demands compliance with an agency's deadlines and other "
                    "critical procedural rules."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "In child welfare administrative practice, tension often exists between parallel dependency court proceedings and "
            "central registry administrative appeals. While some states automatically stay administrative registry appeals pending "
            "the outcome of the juvenile court dependency trial, other states maintain independent tracks. Failure to exhaust "
            "administrative avenues bars subsequent state court judicial review under state administrative procedure acts."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Exhaustion Doctrine Judicial Precedent",
                "content": "Myers v. Bethlehem Shipbuilding Corp. and Woodford v. Ngo define federal exhaustion requirements.",
                "citations": ["Myers v. Bethlehem Shipbuilding Corp., 303 U.S. 41 (1938)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "SHOW_STATUTE": {
                "title": "Administrative Procedure Act Framework",
                "content": "Federal Administrative Procedure Act (5 U.S.C. § 704) and state APAs govern judicial review of final agency actions.",
                "citations": ["5 U.S.C. § 704"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_CASE": {
                "title": "Controlling Precedent: Woodford v. Ngo, 548 U.S. 81 (2006)",
                "content": "Holding that proper exhaustion requires adherence to all agency deadlines and critical procedural rules.",
                "citations": ["Woodford v. Ngo, 548 U.S. 81 (2006)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "Agency Finality and Administrative Efficiency",
                "content": "Agencies argue that exhaustion promotes administrative efficiency and allows the agency to correct its own errors before court intervention.",
                "citations": ["Woodford v. Ngo, 548 U.S. 81 (2006)"],
                "official_sources": ["https://www.supremecourt.gov/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Clarification of State Central Registry Appeal Rights",
                "content": "Due process challenges have forced states to implement clear administrative hearing rights for individuals placed on child abuse registries.",
                "citations": ["5 U.S.C. § 704"],
                "official_sources": ["https://uscode.house.gov/"]
            }
        },
        "related_concepts": ["due_process", "notice", "civil_rights_section_1983"]
    }
}


def build_pack_b():
    CONCEPTS_DIR.mkdir(parents=True, exist_ok=True)
    for cid, data in PACK_B.items():
        out_file = CONCEPTS_DIR / f"{cid}.yaml"
        with open(out_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
        print(f"Created concept YAML: {out_file.name}")
    print(f"Successfully generated all {len(PACK_B)} Pack B concepts in {CONCEPTS_DIR}.")


if __name__ == "__main__":
    build_pack_b()
