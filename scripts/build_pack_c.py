#!/usr/bin/env python3
"""Build Indigenous Rights Literacy Concept Pack C (10 Concepts) for Legal-GPT."""

import yaml
from pathlib import Path

CONCEPTS_DIR = Path(__file__).resolve().parent.parent / "legal_registry" / "literacy" / "concepts"

PACK_C = {
    "tribal_sovereignty": {
        "id": "tribal_sovereignty",
        "canonical_name": "Inherent Tribal Sovereignty",
        "aliases": [
            "tribal sovereignty",
            "inherent sovereignty",
            "tribal nation",
            "domestic dependent nations",
            "worcester v georgia"
        ],
        "jurisdiction": "FED",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "Tribal nations are separate governments that existed long before the United States was formed. "
            "Because their authority comes from their own existence as nations—not from a gift by the U.S. government—they "
            "retain the power to govern their own people, lands, and internal affairs, unless Congress has clearly taken that power away."
        ),
        "level_2_practical": (
            "If you or your family are members of a federally recognized tribe, you are citizens of two governments: your tribal nation "
            "and the United States. State police, child welfare caseworkers, and state court judges generally cannot enforce state laws "
            "against you on reservation land or make decisions about your internal tribal relationships without specific federal statutory authorization."
        ),
        "level_3_terminology": (
            "Inherent tribal sovereignty is a foundational doctrine of federal Indian law established in the Marshall Trilogy (Johnson v. M'Intosh; "
            "Cherokee Nation v. Georgia; Worcester v. Georgia). Under Worcester, tribes are 'distinct, independent political communities'. "
            "Tribal sovereignty is inherent rather than delegated, meaning tribes retain all powers of self-governance not expressly divested "
            "by treaty or federal statute, or implicitly lost by virtue of their domestic dependent status (United States v. Wheeler, 435 U.S. 313)."
        ),
        "level_4_primary_authority": [
            {
                "citation": "Worcester v. Georgia, 31 U.S. 515 (1832)",
                "source_type": "CASELAW",
                "official_portal_url": "https://supreme.justia.com/cases/federal/us/31/515/",
                "key_holding_or_text": (
                    "The Indian nations had always been considered as distinct, independent political communities, retaining their original "
                    "natural rights, as the undisputed possessors of the soil, from time immemorial... The Cherokee nation, then, is a distinct "
                    "community occupying its own territory in which the laws of Georgia can have no force."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Santa Clara Pueblo v. Martinez, 436 U.S. 49 (1978)",
                "source_type": "CASELAW",
                "official_portal_url": "https://supreme.justia.com/cases/federal/us/436/49/",
                "key_holding_or_text": (
                    "Indian tribes are distinct, independent political communities, retaining their original natural rights in matters of "
                    "local self-government; tribes possess the common-law immunity from suit traditionally enjoyed by sovereign powers."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "U.S. Const. art. I, § 8, cl. 3",
                "source_type": "CONSTITUTION",
                "official_portal_url": "https://www.govinfo.gov/content/pkg/GPO-CONAN-2017/pdf/GPO-CONAN-2017.pdf",
                "key_holding_or_text": (
                    "Congress shall have Power... To regulate Commerce with foreign Nations, and among the several States, and with the Indian Tribes."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "Domestic U.S. law vs. International Norms:\n"
            "- Domestic Law: U.S. jurisprudence classifies tribes as 'domestic dependent nations' subject to Congress's plenary power "
            "(Lone Wolf v. Hitchcock), meaning Congress may unilaterally diminish or redefine tribal authority.\n"
            "- UNDRIP (International Norm — non-binding in U.S. domestic proceedings): Article 3 affirms that Indigenous peoples have the "
            "unqualified right to self-determination, and Article 19 requires States to obtain free, prior and informed consent (FPIC) before "
            "adopting legislative measures affecting them.\n"
            "- Alignment & Divergence: While domestic law recognizes inherent self-governance and judicial immunity, it diverges from UNDRIP "
            "by asserting unilateral federal plenary supremacy without requiring tribal consent.\n"
            "- Competing Positions: The Federal Government maintains that historical constitutional doctrine grants Congress plenary control "
            "over Indian affairs. Tribal nations contend that their pre-constitutional sovereignty and international principles of "
            "self-determination preclude unilateral federal extinguishment of sovereign rights."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Primary Sources for Inherent Tribal Sovereignty",
                "content": "U.S. Constitution, Article I, § 8, cl. 3 (Commerce Clause) and Worcester v. Georgia (31 U.S. 515).",
                "citations": ["U.S. Const. art. I, § 8, cl. 3", "Worcester v. Georgia, 31 U.S. 515 (1832)"],
                "official_sources": ["https://www.govinfo.gov", "https://supreme.justia.com/cases/federal/us/31/515/"]
            },
            "SHOW_STATUTE": {
                "title": "Federal Statutes Affirming Tribal Self-Determination",
                "content": "Indian Self-Determination and Education Assistance Act of 1975 (25 U.S.C. § 5301 et seq.) authorizing tribal administration of federal programs.",
                "citations": ["25 U.S.C. § 5301"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_CASE": {
                "title": "Controlling Precedent: Worcester v. Georgia, 31 U.S. 515 (1832)",
                "content": "Holding that tribal nations are independent political communities free from state jurisdictional control.",
                "citations": ["Worcester v. Georgia, 31 U.S. 515 (1832)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/31/515/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "State Encroachment vs Tribal Exclusive Sovereignty",
                "content": "States argue that statehood and general police powers permit concurrent jurisdiction over non-members or fee lands within reservations.",
                "citations": ["Oklahoma v. Castro-Huerta, 597 U.S. 629 (2022)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/597/629/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Evolution from Termination to Self-Determination Policy",
                "content": "In 1970, President Nixon formally repudiated the 1950s termination policy, ushering in the modern federal policy of tribal self-determination.",
                "citations": ["25 U.S.C. § 5301"],
                "official_sources": ["https://uscode.house.gov/"]
            }
        },
        "related_concepts": ["treaty_rights", "indian_country_jurisdiction", "doctrine_of_discovery_repudiation"]
    },

    "treaty_rights": {
        "id": "treaty_rights",
        "canonical_name": "Indian Treaty Rights and the Supremacy Clause",
        "aliases": [
            "treaty rights",
            "indian treaties",
            "canons of construction",
            "supremacy clause treaties",
            "boldt decision"
        ],
        "jurisdiction": "FED",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "Treaties between Indian tribes and the United States are formal international contracts between sovereign nations. "
            "Under the U.S. Constitution, treaties are the 'supreme Law of the Land'. When tribes signed treaties ceding land, "
            "they did not receive rights from the United States; instead, they reserved and kept their own preexisting rights "
            "to hunt, fish, gather, and govern themselves."
        ),
        "level_2_practical": (
            "If your tribe holds treaty rights (such as fishing rights in the Pacific Northwest or hunting rights in the Great Plains), "
            "those rights protect you from state licensing requirements, season limits, or state interference in traditional areas. "
            "State game wardens or agencies cannot override valid federal treaty guarantees."
        ),
        "level_3_terminology": (
            "Under the Supremacy Clause (U.S. Const. art. VI, cl. 2), treaties occupy the highest tier of domestic legal authority. "
            "The reserved rights doctrine (United States v. Winans, 198 U.S. 371) establishes that treaties are not a grant of rights "
            "to the Indians, but a grant of rights from them, with a reservation of those not granted. Treaty interpretation is governed "
            "by the Indian canons of construction: treaties must be construed as the Indians understood them, with ambiguities resolved "
            "in favor of the tribe (Minnesota v. Mille Lacs Band, 526 U.S. 172)."
        ),
        "level_4_primary_authority": [
            {
                "citation": "U.S. Const. art. VI, cl. 2",
                "source_type": "CONSTITUTION",
                "official_portal_url": "https://www.govinfo.gov/content/pkg/GPO-CONAN-2017/pdf/GPO-CONAN-2017.pdf",
                "key_holding_or_text": (
                    "This Constitution, and the Laws of the United States... and all Treaties made, or which shall be made, under the "
                    "Authority of the United States, shall be the supreme Law of the Land; and the Judges in every State shall be bound thereby."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Minnesota v. Mille Lacs Band of Chippewa Indians, 526 U.S. 172 (1999)",
                "source_type": "CASELAW",
                "official_portal_url": "https://supreme.justia.com/cases/federal/us/526/172/",
                "key_holding_or_text": (
                    "Congress may abrogate Indian treaty rights, but it must clearly express its intent to do so... Treaty rights are not "
                    "impliedly extinguished upon state admission into the Union."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "United States v. Winans, 198 U.S. 371 (1905)",
                "source_type": "CASELAW",
                "official_portal_url": "https://supreme.justia.com/cases/federal/us/198/371/",
                "key_holding_or_text": (
                    "The treaty was not a grant of rights to the Indians, but a grant of rights from them — a reservation of those not granted."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "Domestic U.S. law vs. International Norms:\n"
            "- Domestic Law: Under the 'last-in-time' rule and the plenary power doctrine (Lone Wolf v. Hitchcock), Congress possesses the "
            "domestic legal authority to abrogate Indian treaties via subsequent statute, provided congressional intent is clear.\n"
            "- UNDRIP (International Norm — non-binding in U.S. domestic proceedings): Article 37 affirms that Indigenous peoples have the "
            "right to the recognition, observance, and enforcement of treaties concluded with States, and that States shall honor and respect "
            "such treaties without unilateral abrogation.\n"
            "- Alignment & Divergence: U.S. law strictly enforces treaty rights against state governments, but diverges from international norms "
            "by allowing the federal legislature to unilaterally extinguish treaty obligations without tribal consent or bilateral negotiation.\n"
            "- Competing Positions: The Federal Government asserts that plenary power over treaties is an essential incident of national sovereignty. "
            "Tribal nations argue that treaties are permanent international pacts whose unilateral abrogation violates fundamental principles "
            "of international law and the federal trust duty."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Constitutional Supremacy of Treaties",
                "content": "U.S. Constitution, Article VI, Clause 2 mandates that all treaties are the supreme law of the land.",
                "citations": ["U.S. Const. art. VI, cl. 2"],
                "official_sources": ["https://www.govinfo.gov"]
            },
            "SHOW_STATUTE": {
                "title": "Continuation of Existing Treaties",
                "content": "25 U.S.C. § 71 ended future treaty-making in 1871 while expressly preserving the validity and force of all preexisting treaties.",
                "citations": ["25 U.S.C. § 71"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_CASE": {
                "title": "Controlling Precedent: Minnesota v. Mille Lacs Band, 526 U.S. 172 (1999)",
                "content": "Affirming that treaty rights survive statehood and require explicit, clear congressional abrogation.",
                "citations": ["Minnesota v. Mille Lacs Band of Chippewa Indians, 526 U.S. 172 (1999)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/526/172/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "State Equal Footing Doctrine Arguments",
                "content": "States historically argued that the equal footing doctrine terminated off-reservation treaty rights upon statehood, an argument rejected in Mille Lacs Band.",
                "citations": ["Minnesota v. Mille Lacs Band of Chippewa Indians, 526 U.S. 172 (1999)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/526/172/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Judicial Enforcement of Usufructuary Rights",
                "content": "From the Boldt Decision (1974) to Mille Lacs Band (1999) and Herrera v. Wyoming (2019), federal courts have consistently reaffirmed hunting and fishing treaty covenants.",
                "citations": ["Herrera v. Wyoming, 139 S. Ct. 1686 (2019)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/587/17-532/"]
            }
        },
        "related_concepts": ["tribal_sovereignty", "indian_country_jurisdiction", "land_rights_and_trust_responsibility"]
    },

    "indian_country_jurisdiction": {
        "id": "indian_country_jurisdiction",
        "canonical_name": "Indian Country Criminal and Civil Jurisdiction",
        "aliases": [
            "indian country",
            "18 usc 1151",
            "major crimes act",
            "mcgirt",
            "tribal jurisdiction"
        ],
        "jurisdiction": "FED",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "The law defines 'Indian Country' as all land inside an Indian reservation, dependent Indian communities, and individual "
            "Indian allotments. Inside Indian Country, special rules determine whether the tribal court, federal court, or state court has "
            "the authority to handle crimes, lawsuits, and family disputes."
        ),
        "level_2_practical": (
            "If an incident occurs on reservation land, jurisdiction depends on whether the parties are Indian or non-Indian, and whether "
            "the crime is a major felony. Under the landmark McGirt v. Oklahoma ruling, if a reservation was never disestablished by Congress, "
            "it remains Indian Country even if non-Indians live there or state officials believed otherwise for decades."
        ),
        "level_3_terminology": (
            "Indian Country is defined by federal statute under 18 U.S.C. § 1151 as: (a) all land within the limits of any Indian reservation; "
            "(b) all dependent Indian communities; and (c) all Indian allotments. Criminal jurisdiction is allocated under the Major Crimes Act "
            "(18 U.S.C. § 1153, exclusive federal jurisdiction over enumerated felonies by Indians), the General Crimes Act (18 U.S.C. § 1152), "
            "and inherent tribal jurisdiction. Civil regulatory and adjudicatory jurisdiction is governed by the Montana v. United States "
            "(450 U.S. 544) framework."
        ),
        "level_4_primary_authority": [
            {
                "citation": "18 U.S.C. § 1151",
                "source_type": "STATUTE",
                "official_portal_url": "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title18-section1151&num=0&edition=prelim",
                "key_holding_or_text": (
                    "Except as otherwise provided... the term 'Indian country'... means (a) all land within the limits of any Indian reservation "
                    "under the jurisdiction of the United States Government... (b) all dependent Indian communities... and (c) all Indian allotments."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "McGirt v. Oklahoma, 591 U.S. 894 (2020)",
                "source_type": "CASELAW",
                "official_portal_url": "https://supreme.justia.com/cases/federal/us/591/894/",
                "key_holding_or_text": (
                    "Only Congress can divest a reservation of its land and diminish its boundaries. Once a reservation is established, "
                    "it remains Indian country until Congress explicitly says otherwise."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Montana v. United States, 450 U.S. 544 (1981)",
                "source_type": "CASELAW",
                "official_portal_url": "https://supreme.justia.com/cases/federal/us/450/544/",
                "key_holding_or_text": (
                    "The inherent sovereign powers of an Indian tribe do not extend to the activities of nonmembers of the tribe, "
                    "except where nonmembers enter consensual relationships with the tribe or its members, or where conduct threatens "
                    "the political integrity, economic security, or health or welfare of the tribe."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "Domestic U.S. law vs. International Norms:\n"
            "- Domestic Law: Under Oliphant v. Suquamish Indian Tribe (435 U.S. 191), the Supreme Court ruled that tribes lost inherent "
            "criminal jurisdiction over non-Indians. Congress has partially restored jurisdiction over non-Indian domestic abusers via the "
            "Violence Against Women Act (VAWA, 25 U.S.C. § 1304), but broad criminal jurisdiction over non-Indians remains federally restricted.\n"
            "- UNDRIP (International Norm — non-binding in U.S. domestic proceedings): Article 34 affirms that Indigenous peoples have the right "
            "to promote, develop and maintain their institutional structures and their distinctive juridical customs and legal systems.\n"
            "- Alignment & Divergence: U.S. law acknowledges full civil and criminal authority over tribal members, but divides jurisdiction "
            "based on the race/political status of the parties, creating jurisdictional gaps that diverge from international territorial models.\n"
            "- Competing Positions: State prosecutors argue that state jurisdiction over non-Indians is necessary for public safety. Tribal "
            "governments contend that full territorial jurisdiction over all persons within reservation borders is essential to eliminate law "
            "enforcement voids."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Statutory Definition of Indian Country",
                "content": "18 U.S.C. § 1151 establishes the comprehensive three-part definition of Indian Country for federal and tribal jurisdiction.",
                "citations": ["18 U.S.C. § 1151"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_STATUTE": {
                "title": "Major Crimes Act Authority",
                "content": "18 U.S.C. § 1153 confers federal jurisdiction over felony offenses committed by Indians in Indian Country.",
                "citations": ["18 U.S.C. § 1153"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_CASE": {
                "title": "Controlling Precedent: McGirt v. Oklahoma, 591 U.S. 894 (2020)",
                "content": "Reaffirms that statutory reservation boundaries persist regardless of state historical practice absent explicit congressional disestablishment.",
                "citations": ["McGirt v. Oklahoma, 591 U.S. 894 (2020)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/591/894/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "State Concurrent Jurisdiction Claim",
                "content": "In Oklahoma v. Castro-Huerta (2022), the Supreme Court held that states have concurrent jurisdiction over crimes committed by non-Indians against Indians in Indian Country.",
                "citations": ["Oklahoma v. Castro-Huerta, 597 U.S. 629 (2022)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/597/629/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "VAWA Reauthorizations Restoring Tribal Criminal Authority",
                "content": "Congress enacted special tribal criminal jurisdiction in the 2013 and 2022 reauthorizations of the Violence Against Women Act (25 U.S.C. § 1304).",
                "citations": ["25 U.S.C. § 1304"],
                "official_sources": ["https://uscode.house.gov/"]
            }
        },
        "related_concepts": ["tribal_sovereignty", "treaty_rights", "tribal_court_jurisdiction_icwa"]
    },

    "icwa_active_efforts": {
        "id": "icwa_active_efforts",
        "canonical_name": "ICWA Active Efforts Requirement vs ASFA Reasonable Efforts",
        "aliases": [
            "icwa active efforts",
            "active efforts",
            "25 usc 1912 d",
            "25 cfr 23 2",
            "active efforts standard"
        ],
        "jurisdiction": "FED",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "When child welfare agencies deal with a Native child, the law requires them to do much more than simply give parents "
            "a list of phone numbers. They must provide 'active efforts'—actively helping parents access housing, treatment, transportation, "
            "and cultural support—to keep the family together before any child can be placed in foster care or parental rights terminated."
        ),
        "level_2_practical": (
            "In court, the caseworker cannot merely state: 'I gave the mother referrals, but she failed to call.' Under ICWA, active efforts "
            "means the caseworker must take the parent to the appointment, arrange culturally appropriate tribal healing programs, involve "
            "extended family, and consult the child's tribe. The state must prove by clear and convincing evidence that active efforts were "
            "provided and failed."
        ),
        "level_3_terminology": (
            "Under 25 U.S.C. § 1912(d), any party seeking foster care placement or termination of parental rights to an Indian child must "
            "demonstrate that 'active efforts have been made to provide remedial services and rehabilitative programs designed to prevent the "
            "breakup of the Indian family and that these efforts have proved unsuccessful.' The Bureau of Indian Affairs (25 C.F.R. § 23.2) "
            "defines active efforts as affirmative, active, thorough, and timely efforts tailored to the specific circumstances of the Indian family."
        ),
        "level_4_primary_authority": [
            {
                "citation": "25 U.S.C. § 1912(d)",
                "source_type": "STATUTE",
                "official_portal_url": "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title25-section1912&num=0&edition=prelim",
                "key_holding_or_text": (
                    "Any party seeking to effect a foster care placement of, or termination of parental rights to, an Indian child under State law "
                    "shall satisfy the court that active efforts have been made to provide remedial services and rehabilitative programs designed to "
                    "prevent the breakup of the Indian family and that these efforts have proved unsuccessful."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "25 C.F.R. § 23.2",
                "source_type": "REGULATION",
                "official_portal_url": "https://www.ecfr.gov/current/title-25/chapter-I/subchapter-D/part-23/subpart-A/section-23.2",
                "key_holding_or_text": (
                    "Active efforts means affirmative, active, thorough, and timely efforts intended primarily to maintain or reunite an Indian "
                    "child with his or her family... Active efforts must involve assisting the parent or parents or Indian custodian through the steps "
                    "of a case plan and with accessing or developing the resources necessary to satisfy the case plan."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Haaland v. Brackeen, 599 U.S. 255 (2023)",
                "source_type": "CASELAW",
                "official_portal_url": "https://supreme.justia.com/cases/federal/us/599/255/",
                "key_holding_or_text": (
                    "Upholding the constitutionality of ICWA, including the statutory requirements governing state court child custody proceedings."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "Domestic U.S. law vs. International Norms:\n"
            "- Domestic Law: ICWA § 1912(d) imposes an affirmative duty substantially higher than the 'reasonable efforts' standard under the "
            "Adoption and Safe Families Act (ASFA, 42 U.S.C. § 671). However, some state courts have attempted to create non-statutory exceptions "
            "(such as the discredited 'existing Indian family doctrine' or futility exceptions).\n"
            "- UNDRIP (International Norm — non-binding in U.S. domestic proceedings): Article 7 guarantees collective freedom from forced assimilation, "
            "and Article 10 prohibits forced relocation of Indigenous persons from their families and lands.\n"
            "- Alignment & Divergence: ICWA aligns closely with international human rights standards on family preservation and cultural integrity, "
            "serving as the gold standard of domestic child welfare law.\n"
            "- Competing Positions: State agencies sometimes argue that emergency safety risks or parental non-compliance excuse rigorous active "
            "efforts. Tribal nations and parents argue that federal law permits no exceptions: active efforts must be documented on the record "
            "before any non-emergency removal or termination can be sustained."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Statutory Text of 25 U.S.C. § 1912(d)",
                "content": "Federal statute governing mandatory active efforts in Indian child custody proceedings.",
                "citations": ["25 U.S.C. § 1912(d)"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_STATUTE": {
                "title": "BIA Regulations on Active Efforts",
                "content": "25 C.F.R. § 23.2 provides 11 non-exhaustive examples of active efforts required of child welfare agencies.",
                "citations": ["25 C.F.R. § 23.2"],
                "official_sources": ["https://www.ecfr.gov/"]
            },
            "SHOW_CASE": {
                "title": "Controlling Precedent: Haaland v. Brackeen, 599 U.S. 255 (2023)",
                "content": "Supreme Court held that ICWA's statutory requirements are constitutional exercises of congressional Article I power.",
                "citations": ["Haaland v. Brackeen, 599 U.S. 255 (2023)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/599/255/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "ASFA Timeline Conflicts",
                "content": "Agencies argue that ASFA's 15/22 month termination timeline conflicts with extensive active efforts, but federal regulations make clear ICWA controls.",
                "citations": ["42 U.S.C. § 675(5)(E)", "25 C.F.R. § 23.106"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Codification of BIA Regulations into Binding Rules (2016)",
                "content": "In 2016, the Department of the Interior promulgated binding federal regulations (25 C.F.R. Part 23) replacing advisory guidelines to ensure uniform national enforcement.",
                "citations": ["81 Fed. Reg. 38778 (June 14, 2016)"],
                "official_sources": ["https://www.federalregister.gov/"]
            }
        },
        "related_concepts": ["icwa_qualified_expert_witness", "tribal_court_jurisdiction_icwa", "reasonable_efforts"]
    },

    "icwa_qualified_expert_witness": {
        "id": "icwa_qualified_expert_witness",
        "canonical_name": "Qualified Expert Witness (QEW) Requirement under ICWA",
        "aliases": [
            "qualified expert witness",
            "qew icwa",
            "25 usc 1912 e",
            "25 usc 1912 f",
            "25 cfr 23 122"
        ],
        "jurisdiction": "FED",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "Before a judge can place a Native child into foster care or permanently sever parental ties, the law requires testimony "
            "from a Qualified Expert Witness who truly understands tribal child-rearing customs. A standard social worker is not enough; "
            "the expert must explain whether the child faces serious physical or emotional harm within their specific cultural community."
        ),
        "level_2_practical": (
            "In state court, CPS cannot rely solely on its own caseworkers or standard psychologists to justify removal of an Indian child. "
            "The state must produce a QEW—often designated by the child's tribe—who testifies under oath regarding tribal cultural standards. "
            "If the state fails to produce a qualified QEW, any foster care order or termination is legally invalid under federal law."
        ),
        "level_3_terminology": (
            "Under 25 U.S.C. §§ 1912(e) and 1912(f), foster care placement requires clear and convincing evidence, and termination of parental "
            "rights requires evidence beyond a reasonable doubt, 'including testimony of qualified expert witnesses, that the continued custody "
            "of the child by the parent or Indian custodian is likely to result in serious emotional or physical damage to the child.' Under "
            "25 C.F.R. § 23.122, the QEW must possess expertise in the prevailing social and cultural standards of the child's tribe."
        ),
        "level_4_primary_authority": [
            {
                "citation": "25 U.S.C. § 1912(e)",
                "source_type": "STATUTE",
                "official_portal_url": "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title25-section1912&num=0&edition=prelim",
                "key_holding_or_text": (
                    "No foster care placement may be ordered in such proceeding in the absence of a determination, supported by clear and convincing "
                    "evidence, including testimony of qualified expert witnesses, that the continued custody of the child by the parent or Indian custodian "
                    "is likely to result in serious emotional or physical damage to the child."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "25 U.S.C. § 1912(f)",
                "source_type": "STATUTE",
                "official_portal_url": "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title25-section1912&num=0&edition=prelim",
                "key_holding_or_text": (
                    "No termination of parental rights may be ordered... in the absence of a determination, supported by evidence beyond a reasonable doubt, "
                    "including testimony of qualified expert witnesses, that the continued custody of the child... is likely to result in serious emotional or physical damage."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "25 C.F.R. § 23.122",
                "source_type": "REGULATION",
                "official_portal_url": "https://www.ecfr.gov/current/title-25/chapter-I/subchapter-D/part-23/subpart-C/section-23.122",
                "key_holding_or_text": (
                    "The qualified expert witness must be qualified to testify regarding whether the child's continued custody is likely to result in serious "
                    "emotional or physical damage. The social worker regularly assigned to the Indian child may not serve as a qualified expert witness."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "Domestic U.S. law vs. International Norms:\n"
            "- Domestic Law: Federal regulations explicitly prohibit assigned state caseworkers from serving as their own QEWs (25 C.F.R. § 23.122(c)) "
            "to prevent self-serving, culturally biased assessments. However, some state trial courts still improperly attempt to qualify generic "
            "child psychologists who lack specific knowledge of tribal family structures.\n"
            "- UNDRIP (International Norm — non-binding in U.S. domestic proceedings): Article 14 affirms the right of Indigenous families to establish "
            "and control their educational and child care systems in a manner appropriate to their cultural methods of teaching and learning.\n"
            "- Alignment & Divergence: The QEW requirement is an explicit domestic safeguard against cultural bias, aligning with international protections "
            "against ethnocentric state deprivations of family integrity.\n"
            "- Competing Positions: State agencies often argue that certified mental health professionals should qualify regardless of tribal familiarity. "
            "Tribal nations argue that without specific immersion in the child's tribal customs, outside experts cannot distinguish cultural child-rearing "
            "practices from psychological neglect."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Statutory QEW Requirements",
                "content": "25 U.S.C. §§ 1912(e) and 1912(f) mandate QEW testimony for foster care and parental termination.",
                "citations": ["25 U.S.C. § 1912(e)", "25 U.S.C. § 1912(f)"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_STATUTE": {
                "title": "Federal Regulations on QEW Disqualification of State Social Workers",
                "content": "25 C.F.R. § 23.122(c) explicitly bars regularly assigned state social workers from testifying as the QEW.",
                "citations": ["25 C.F.R. § 23.122"],
                "official_sources": ["https://www.ecfr.gov/"]
            },
            "SHOW_CASE": {
                "title": "State Appellate Precedent Disqualifying Generic Experts",
                "content": "Appellate courts routinely reverse terminations where the purported QEW lacked knowledge of tribal child-rearing customs.",
                "citations": ["In re Dependency of J.M.W., 438 P.3d 170 (Wash. Ct. App. 2019)"],
                "official_sources": ["https://scholar.google.com/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "State Shortage of Tribal Experts Claim",
                "content": "State agencies argue that a scarcity of tribal QEWs delays permanency, whereas tribes emphasize that agencies must coordinate with tribal governments early in proceedings.",
                "citations": ["25 C.F.R. § 23.122"],
                "official_sources": ["https://www.ecfr.gov/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Transition from State Discretion to Uniform Federal Standards",
                "content": "Before the 2016 BIA regulations, state courts varied widely in qualifying non-Native professionals; the 2016 rules created strict national cultural qualifications.",
                "citations": ["25 C.F.R. § 23.122"],
                "official_sources": ["https://www.ecfr.gov/"]
            }
        },
        "related_concepts": ["icwa_active_efforts", "tribal_court_jurisdiction_icwa", "due_process"]
    },

    "tribal_court_jurisdiction_icwa": {
        "id": "tribal_court_jurisdiction_icwa",
        "canonical_name": "Tribal Court Jurisdiction and Case Transfer under ICWA",
        "aliases": [
            "tribal court jurisdiction icwa",
            "25 usc 1911",
            "icwa transfer",
            "holyfield",
            "tribal court transfer"
        ],
        "jurisdiction": "FED",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "When a Native child is involved in a court proceeding, tribal courts have special authority to hear the case. "
            "If the child lives on the reservation, the tribal court has exclusive power. If the child lives off the reservation, "
            "parents or the tribe have the legal right to ask the state judge to transfer the entire case into tribal court."
        ),
        "level_2_practical": (
            "If your child welfare case starts in a state county court, you or your tribe can file a formal motion to transfer the case "
            "to your tribal nation's court. The state court must transfer the case unless either parent objects or the judge finds specific, "
            "lawful 'good cause' not to transfer. The state judge cannot refuse transfer just because they believe the state court has more money or services."
        ),
        "level_3_terminology": (
            "Under 25 U.S.C. § 1911, ICWA establishes a dual jurisdictional framework: (a) Exclusive Jurisdiction (§ 1911(a)) over Indian children "
            "residing or domiciled within the reservation (Mississippi Band of Choctaw Indians v. Holyfield); and (b) Concurrent Presumptive Transfer "
            "Jurisdiction (§ 1911(b)) for off-reservation children. Under § 1911(b), transfer to tribal court is mandatory upon petition of a parent, "
            "custodian, or tribe, absent objection by either parent or good cause to the contrary. Good cause is strictly defined under 25 C.F.R. § 23.118."
        ),
        "level_4_primary_authority": [
            {
                "citation": "25 U.S.C. § 1911",
                "source_type": "STATUTE",
                "official_portal_url": "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title25-section1911&num=0&edition=prelim",
                "key_holding_or_text": (
                    "An Indian tribe shall have jurisdiction exclusive as to any State over any child custody proceeding involving an Indian "
                    "child who resides or is domiciled within the reservation... In any State court proceeding... the court, in the absence of "
                    "good cause to the contrary, shall transfer such proceeding to the jurisdiction of the tribe."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Mississippi Band of Choctaw Indians v. Holyfield, 490 U.S. 30 (1989)",
                "source_type": "CASELAW",
                "official_portal_url": "https://supreme.justia.com/cases/federal/us/490/30/",
                "key_holding_or_text": (
                    "Tribal jurisdiction under ICWA cannot be defeated by individual parents giving birth off-reservation; federal domicile "
                    "principles control, and the tribe's interest in its children is independent of the parents' preferences."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "25 C.F.R. § 23.118",
                "source_type": "REGULATION",
                "official_portal_url": "https://www.ecfr.gov/current/title-25/chapter-I/subchapter-D/part-23/subpart-C/section-23.118",
                "key_holding_or_text": (
                    "In determining whether good cause exists, the court may not consider whether the proceeding is at an advanced stage if the "
                    "parent or tribe did not receive prompt notice; whether transfer may affect placement; or the perceived adequacy of tribal court services."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "Domestic U.S. law vs. International Norms:\n"
            "- Domestic Law: ICWA § 1911(b) recognizes the presumptive authority of tribal judiciaries, but grants individual parents absolute "
            "veto power over transfer to tribal court, creating complex tensions between individual parental autonomy and collective tribal sovereignty.\n"
            "- UNDRIP (International Norm — non-binding in U.S. domestic proceedings): Article 5 affirms the right of Indigenous peoples to maintain "
            "and strengthen their distinct political, legal, economic, social and cultural institutions, while retaining their right to participate fully "
            "in the political life of the State.\n"
            "- Alignment & Divergence: The transfer mechanism operationalizes tribal self-determination within domestic family law, though parental "
            "veto provisions diverge from pure sovereign territorial jurisdiction.\n"
            "- Competing Positions: Foster parents and state agencies sometimes resist transfer by citing bond attachments or litigation delay. "
            "Tribal nations argue that Holyfield establishes that tribes possess an independent sovereign interest in the welfare of their child citizens "
            "that transcends state court forum preference."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Statutory Jurisdiction Framework",
                "content": "25 U.S.C. § 1911 governs exclusive reservation jurisdiction and presumptive transfer to tribal courts.",
                "citations": ["25 U.S.C. § 1911"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_STATUTE": {
                "title": "BIA Good Cause Regulations",
                "content": "25 C.F.R. § 23.118 lists impermissible factors that state courts may not use to deny transfer to tribal court.",
                "citations": ["25 C.F.R. § 23.118"],
                "official_sources": ["https://www.ecfr.gov/"]
            },
            "SHOW_CASE": {
                "title": "Controlling Precedent: Mississippi Band of Choctaw Indians v. Holyfield, 490 U.S. 30 (1989)",
                "content": "Landmark ruling defining tribal domicile and upholding exclusive tribal jurisdiction under § 1911(a).",
                "citations": ["Mississippi Band of Choctaw Indians v. Holyfield, 490 U.S. 30 (1989)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/490/30/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "Parental Veto Mechanics",
                "content": "Under 25 U.S.C. § 1911(b), an objection by either biological parent terminates the transfer request and keeps the case in state court.",
                "citations": ["25 U.S.C. § 1911(b)"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Elimination of Socioeconomic Comparisons in Transfer Reviews",
                "content": "Historical state court practice of denying transfer based on perceived inadequacy of tribal courts was expressly outlawed by the 2016 BIA regulations.",
                "citations": ["25 C.F.R. § 23.118"],
                "official_sources": ["https://www.ecfr.gov/"]
            }
        },
        "related_concepts": ["icwa_active_efforts", "tribal_sovereignty", "indian_country_jurisdiction"]
    },

    "blood_quantum_vs_citizenship": {
        "id": "blood_quantum_vs_citizenship",
        "canonical_name": "Blood Quantum vs Tribal Citizenship and Political Classification",
        "aliases": [
            "blood quantum",
            "tribal citizenship",
            "santa clara pueblo",
            "tribal enrollment",
            "political classification morton v mancari"
        ],
        "jurisdiction": "FED",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "Tribal citizenship is a political status, not a racial category. Just as the United States or France decides who its "
            "citizens are, each tribal nation has the absolute sovereign right to set its own membership criteria. Under U.S. Supreme "
            "Court precedent, being Native American in federal law is a political relationship between a citizen and their sovereign tribe."
        ),
        "level_2_practical": (
            "If a court or caseworker claims that child welfare laws or tribal rights are based on 'racial discrimination,' that claim is legally "
            "incorrect under federal law. In Morton v. Mancari and Haaland v. Brackeen, the Supreme Court confirmed that tribal rights apply "
            "because of citizenship in a self-governing political nation. Legal-GPT never defines who is or is not a tribal member; that authority "
            "belongs exclusively to each tribal nation."
        ),
        "level_3_terminology": (
            "The distinction between racial classification and political status is grounded in Morton v. Mancari (417 U.S. 535), which held "
            "that federal preferences for tribal members are political rather than racial, subject to rational basis review. In Santa Clara Pueblo "
            "v. Martinez (436 U.S. 49), the Supreme Court affirmed that a tribe's right to define its own membership for tribal purposes has "
            "long been recognized as central to its existence as an independent political community. Federal definitions (such as 25 U.S.C. § 1603 "
            "or 25 U.S.C. § 1903(4)) defer to tribal citizenship determinations."
        ),
        "level_4_primary_authority": [
            {
                "citation": "Santa Clara Pueblo v. Martinez, 436 U.S. 49 (1978)",
                "source_type": "CASELAW",
                "official_portal_url": "https://supreme.justia.com/cases/federal/us/436/49/",
                "key_holding_or_text": (
                    "A tribe's right to define its own membership for tribal purposes has long been recognized as central to its existence "
                    "as an independent political community... Given the often vast gulf between tribal traditions and those with which "
                    "federal courts are familiar, questions of tribal membership must remain with tribal authorities."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Morton v. Mancari, 417 U.S. 535 (1974)",
                "source_type": "CASELAW",
                "official_portal_url": "https://supreme.justia.com/cases/federal/us/417/535/",
                "key_holding_or_text": (
                    "Literally every piece of legislation dealing with Indian tribes... single out for special treatment a constituency of "
                    "tribal Indians. If these laws, derived from historical relationships and treaties, were deemed invidious racial classifications, "
                    "an entire Title of the United States Code would be effectively erased... The preference is political, not racial."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Haaland v. Brackeen, 599 U.S. 255 (2023)",
                "source_type": "CASELAW",
                "official_portal_url": "https://supreme.justia.com/cases/federal/us/599/255/",
                "key_holding_or_text": (
                    "Reaffirmed that Congress's power to legislate with respect to Indian tribes is broad and deeply rooted in constitutional text and history."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "Domestic U.S. law vs. International Norms:\n"
            "- Domestic Law: While federal courts treat tribal enrollment as a political status, federal statutes and administrative regulations "
            "historically imposed external 'blood quantum' standards (e.g. 1/4 degree Indian blood) for federal service eligibility (25 U.S.C. § 1603), "
            "originating from 19th-century allotment rolls.\n"
            "- UNDRIP (International Norm — non-binding in U.S. domestic proceedings): Article 33 affirms that Indigenous peoples have the right "
            "to determine their own identity or membership in accordance with their customs and traditions, free from external state-imposed criteria.\n"
            "- Alignment & Divergence: Santa Clara Pueblo aligns with UNDRIP by upholding tribal sovereignty over citizenship, but historical federal "
            "reliance on blood quantum fractions in statutory schemes creates ongoing tensions with traditional lineage systems.\n"
            "- Competing Positions: Opponents of tribal programs argue that blood quantum elements in tribal constitutions or federal criteria "
            "function as racial proxies. Tribal nations maintain that lineage-based criteria are standard citizenship mechanisms utilized by sovereign "
            "nations worldwide (jus sanguinis) and that tribal citizenship is exclusively a political bond."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Primary Authority on Tribal Membership",
                "content": "Santa Clara Pueblo v. Martinez (436 U.S. 49) establishes exclusive tribal authority over membership.",
                "citations": ["Santa Clara Pueblo v. Martinez, 436 U.S. 49 (1978)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/436/49/"]
            },
            "SHOW_STATUTE": {
                "title": "ICWA Definition of Indian Child",
                "content": "25 U.S.C. § 1903(4) defines Indian child based on tribal membership or eligibility for membership combined with a biological parent's membership.",
                "citations": ["25 U.S.C. § 1903(4)"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_CASE": {
                "title": "Controlling Precedent: Morton v. Mancari, 417 U.S. 535 (1974)",
                "content": "Holding that Indian legal status is political rather than racial, surviving equal protection scrutiny under rational basis review.",
                "citations": ["Morton v. Mancari, 417 U.S. 535 (1974)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/417/535/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "Equal Protection Challenges to ICWA Preferences",
                "content": "Challengers in Brackeen argued that ICWA's third placement preference (other Indian families) constitutes racial classification; the Supreme Court dismissed the claim for lack of standing.",
                "citations": ["Haaland v. Brackeen, 599 U.S. 255 (2023)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/599/255/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Tribal Transition from Federal Blood Quantum to Lineal Descent",
                "content": "Many tribal nations have amended their constitutions to replace BIA-mandated blood quantum requirements with lineal descent from historical base rolls.",
                "citations": ["Santa Clara Pueblo v. Martinez, 436 U.S. 49 (1978)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/436/49/"]
            }
        },
        "related_concepts": ["tribal_sovereignty", "icwa_active_efforts", "due_process"]
    },

    "doctrine_of_discovery_repudiation": {
        "id": "doctrine_of_discovery_repudiation",
        "canonical_name": "Doctrine of Discovery and Contemporary Legal Analysis",
        "aliases": [
            "doctrine of discovery",
            "johnson v mintosh",
            "discovery doctrine repudiation",
            "aboriginal title",
            "marshall trilogy"
        ],
        "jurisdiction": "FED",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "The 'Doctrine of Discovery' was a legal rule created in the 1800s that claimed European nations automatically gained ownership "
            "of land simply by arriving and 'discovering' it, reducing the Indigenous people who already lived there to mere occupants. "
            "While this rule remains part of historical American property law in court, international human rights organizations have condemned it "
            "as unjust and called for it to be rejected."
        ),
        "level_2_practical": (
            "If property disputes involve ancestral tribal lands or unceded territory, courts still look back to the 1823 Supreme Court decision "
            "Johnson v. M'Intosh. The case held that tribal land cannot be sold to anyone except the federal government. Understanding this "
            "doctrine helps explain why the federal government, rather than the tribe, holds formal legal title to many reservation lands today."
        ),
        "level_3_terminology": (
            "In Johnson v. M'Intosh, 21 U.S. 543 (1823), Chief Justice John Marshall incorporated the international colonial Doctrine of Discovery "
            "into U.S. common law, holding that European discovery gave the discovering sovereign ultimate fee title to the land, subject only to "
            "the Indian right of occupancy ('aboriginal title'). The sovereign held the exclusive power to extinguish this right of occupancy either "
            "by purchase or conquest. In Tee-Hit-Ton Indians v. United States, 348 U.S. 272 (1955), the Court reaffirmed that unrecognized aboriginal "
            "title is not property protected by the Fifth Amendment Takings Clause."
        ),
        "level_4_primary_authority": [
            {
                "citation": "Johnson v. M'Intosh, 21 U.S. 543 (1823)",
                "source_type": "CASELAW",
                "official_portal_url": "https://supreme.justia.com/cases/federal/us/21/543/",
                "key_holding_or_text": (
                    "Discovery gave title to the government by whose subjects, or by whose authority, it was made, against all other European governments, "
                    "which title might be consummated by possession... The Indian inhabitants are to be considered merely as occupants, to be protected, "
                    "indeed, while in peace, in the possession of their lands, but to be deemed incapable of transferring the absolute title to others."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Tee-Hit-Ton Indians v. United States, 348 U.S. 272 (1955)",
                "source_type": "CASELAW",
                "official_portal_url": "https://supreme.justia.com/cases/federal/us/348/272/",
                "key_holding_or_text": (
                    "It is well settled that in all the States of the Union the tribes who inhabited the lands of the State held them by a title "
                    "dependent on the will of the sovereign; the taking by the United States of unrecognized Indian title is not a compensable taking."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "City of Sherrill v. Oneida Indian Nation of New York, 544 U.S. 197 (2005)",
                "source_type": "CASELAW",
                "official_portal_url": "https://supreme.justia.com/cases/federal/us/544/197/",
                "key_holding_or_text": (
                    "Referenced the Doctrine of Discovery as the historical premise under which European fee title was established."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "Domestic U.S. law vs. International Norms:\n"
            "- Domestic Law: Johnson v. M'Intosh remains controlling property precedent in U.S. courts, anchoring federal fee ownership of trust lands "
            "and the absolute power of Congress to extinguish unratified aboriginal title.\n"
            "- UNDRIP & International Human Rights (Non-binding international norm): The United Nations Permanent Forum on Indigenous Issues and the "
            "UN Special Rapporteur on the Rights of Indigenous Peoples have formally condemned the Doctrine of Discovery as racist, scientifically "
            "false, legally invalid, and morally condemnable, calling for its explicit repudiation by all member states. On March 30, 2023, the Vatican "
            "issued a formal joint statement repudiating the 15th-century Papal Bulls (e.g. Inter Caetera) associated with the doctrine.\n"
            "- Alignment & Divergence: Total divergence exists between domestic legal doctrine—where Johnson v. M'Intosh remains technically binding "
            "property law—and international human rights instruments, which repudiate discovery-based title as incompatible with fundamental human rights.\n"
            "- Competing Positions: The Federal Government and state title holders maintain that stability of land titles across the continent relies on "
            "the chain of title tracing to sovereign federal patents. Indigenous scholars and tribal advocates argue that the doctrine is fundamentally "
            "illegitimate and that domestic law should recognize inherent Indigenous ownership."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Primary Case Law: Johnson v. M'Intosh (1823)",
                "content": "Full opinion by Chief Justice Marshall establishing discovery doctrine in American property law.",
                "citations": ["Johnson v. M'Intosh, 21 U.S. 543 (1823)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/21/543/"]
            },
            "SHOW_STATUTE": {
                "title": "Nonintercourse Act (25 U.S.C. § 177)",
                "content": "Federal statute codifying the rule that no purchase or cession of lands from an Indian nation is valid without federal approval.",
                "citations": ["25 U.S.C. § 177"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_CASE": {
                "title": "Fifth Amendment Takings Exclusion: Tee-Hit-Ton Indians (1955)",
                "content": "Holding that taking of unrecognized aboriginal title does not require Fifth Amendment just compensation.",
                "citations": ["Tee-Hit-Ton Indians v. United States, 348 U.S. 272 (1955)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/348/272/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "Land Title Stability Defense",
                "content": "Real property law relies on undisputed sovereign chain of title; courts express reluctance to disrupt centuries of settled property transactions.",
                "citations": ["City of Sherrill v. Oneida Indian Nation of New York, 544 U.S. 197 (2005)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/544/197/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Vatican Repudiation and Modern International Consensus",
                "content": "On March 30, 2023, the Holy See officially repudiated the concept of discovery doctrine, stating papal bulls did not adequately reflect the equal dignity and rights of indigenous peoples.",
                "citations": ["Joint Statement of the Dicasteries for Culture and for Promoting Integral Human Development (March 30, 2023)"],
                "official_sources": ["https://www.vatican.va/"]
            }
        },
        "related_concepts": ["tribal_sovereignty", "land_rights_and_trust_responsibility", "treaty_rights"]
    },

    "land_rights_and_trust_responsibility": {
        "id": "land_rights_and_trust_responsibility",
        "canonical_name": "Federal Trust Responsibility and Tribal Land Rights",
        "aliases": [
            "federal trust responsibility",
            "trust responsibility",
            "cobell v salazar",
            "indian trust lands",
            "25 usc 162a"
        ],
        "jurisdiction": "FED",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "Because the United States took millions of acres of land through treaties and statutes, the federal government owes a strict, "
            "sacred legal duty to protect Indian tribes, their lands, their resources, and their funds. This duty is called the 'federal trust responsibility.'"
        ),
        "level_2_practical": (
            "Reservation land is often held in 'trust status' by the United States for the benefit of the tribe or individual tribal members. "
            "This means county tax assessors cannot tax or foreclose on trust land, and state governments cannot regulate it. However, it also means "
            "the Bureau of Indian Affairs (BIA) must approve leases, sales, and resource development on the land."
        ),
        "level_3_terminology": (
            "The federal trust responsibility is a legally enforceable fiduciary obligation established in Seminole Nation v. United States, "
            "316 U.S. 286 (1942), holding the government to the most exacting fiduciary standards. Under 25 U.S.C. § 162a, Congress codified "
            "specific trust accounting responsibilities. In Cobell v. Salazar (settled 2009 for $3.4 billion), the federal courts held that the "
            "Department of the Interior breached its fiduciary duties by mismanaging Individual Indian Money (IIM) accounts for over a century."
        ),
        "level_4_primary_authority": [
            {
                "citation": "Seminole Nation v. United States, 316 U.S. 286 (1942)",
                "source_type": "CASELAW",
                "official_portal_url": "https://supreme.justia.com/cases/federal/us/316/286/",
                "key_holding_or_text": (
                    "In carrying out its treaty obligations with the Indian tribes, the Government is something more than a mere contracting party. "
                    "Under a humane and self imposed policy which has found expression in many acts of Congress and numerous decisions of this Court, "
                    "it has charged itself with moral obligations of the highest responsibility and trust... judged by the most exacting fiduciary standards."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "25 U.S.C. § 162a",
                "source_type": "STATUTE",
                "official_portal_url": "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title25-section162a&num=0&edition=prelim",
                "key_holding_or_text": (
                    "The Secretary's proper discharge of the trust responsibilities of the United States shall include... providing adequate systems "
                    "for accounting for and reporting trust balances... and auditing and reconciling of these accounts."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Cobell v. Salazar, 573 F.3d 808 (D.C. Cir. 2009)",
                "source_type": "CASELAW",
                "official_portal_url": "https://scholar.google.com/",
                "key_holding_or_text": (
                    "Affirmed systemic federal breach of fiduciary duties regarding individual Indian trust accounts, leading to a landmark $3.4 billion settlement."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "Domestic U.S. law vs. International Norms:\n"
            "- Domestic Law: While Seminole Nation and Cobell enforce strict trust accounting when specific statutes establish fiduciary duties, "
            "the Supreme Court in United States v. Jicarilla Apache Nation (564 U.S. 162) and Arizona v. Navajo Nation (599 U.S. 555, 2023) held that "
            "the trust responsibility does not create broad common-law fiduciary duties unless tied to specific statutory text.\n"
            "- UNDRIP (International Norm — non-binding in U.S. domestic proceedings): Article 26 guarantees that Indigenous peoples have the right "
            "to own, use, develop and control the lands, territories and resources that they possess by reason of traditional ownership.\n"
            "- Alignment & Divergence: The domestic trust model provides crucial protection against state taxation and alienation, but gives the federal "
            "government paternalistic control over land management, diverging from UNDRIP's model of full self-determined indigenous ownership.\n"
            "- Competing Positions: The Federal Government contends that its trust duties are defined solely by explicit statutory mandates. Tribal nations "
            "argue that the trust responsibility represents an enduring, moral and legal covenant arising from the cession of millions of acres of land."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Fiduciary Standard Authority: Seminole Nation (1942)",
                "content": "Supreme Court held that the government is held to the most exacting fiduciary standards in managing Indian affairs.",
                "citations": ["Seminole Nation v. United States, 316 U.S. 286 (1942)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/316/286/"]
            },
            "SHOW_STATUTE": {
                "title": "American Indian Trust Fund Management Reform Act of 1994",
                "content": "25 U.S.C. § 4001 et seq. codifies detailed federal accounting and auditing duties for tribal trust funds.",
                "citations": ["25 U.S.C. § 4001"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_CASE": {
                "title": "Cobell v. Salazar Trust Litigation",
                "content": "Historical class action led by Elouise Cobell challenging federal accounting failures, resulting in the Claims Resolution Act of 2010.",
                "citations": ["Claims Resolution Act of 2010, Pub. L. 111-291, 124 Stat. 3064"],
                "official_sources": ["https://www.govinfo.gov/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "Narrow Statutory Construction of Trust Duties",
                "content": "In Arizona v. Navajo Nation (2023), the Court held 5-4 that the 1868 Navajo treaty did not require the federal government to secure water rights for the tribe.",
                "citations": ["Arizona v. Navajo Nation, 599 U.S. 555 (2023)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/599/21-1484/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Land Buy-Back Program for Tribal Nations",
                "content": "The Cobell settlement funded a $1.9 billion federal program that purchased highly fractionated trust allotments and consolidated them into tribal ownership.",
                "citations": ["DOI Land Buy-Back Program Report (2022)"],
                "official_sources": ["https://www.doi.gov/"]
            }
        },
        "related_concepts": ["doctrine_of_discovery_repudiation", "treaty_rights", "tribal_sovereignty"]
    },

    "native_voting_rights": {
        "id": "native_voting_rights",
        "canonical_name": "Native American Voting Rights and Ballot Access",
        "aliases": [
            "native voting rights",
            "voting rights act native",
            "indian voting rights",
            "vra section 2",
            "arizona v inter tribal council"
        ],
        "jurisdiction": "FED",
        "retrieved_date": "2026-09-19",
        "level_1_plain_english": (
            "Even though Native Americans were granted U.S. citizenship in 1924, many states denied them the right to vote for decades. "
            "Today, federal laws like the Voting Rights Act protect Native voters from discriminatory state rules, such as refusing to accept "
            "tribal IDs, failing to provide ballots in Native languages, or placing ballot boxes hundreds of miles away from reservations."
        ),
        "level_2_practical": (
            "If you live on a rural reservation without traditional street addresses, state election officials cannot reject your voter "
            "registration simply because you use a P.O. Box or tribal ID. Federal courts have repeatedly struck down state voting laws that "
            "impose unequal obstacles on reservation voters, requiring states to provide accessible drop boxes and language assistance."
        ),
        "level_3_terminology": (
            "Native American voting rights litigation primarily arises under the Fourteenth and Fifteenth Amendments, Section 2 of the Voting "
            "Rights Act of 1965 (52 U.S.C. § 10301, prohibiting practices that result in a denial or abridgment of the right to vote on account "
            "of race or language minority status), and Section 203 (52 U.S.C. § 10503, mandatory bilingual ballots and language assistance). In "
            "Arizona v. Inter Tribal Council of Arizona, 570 U.S. 1 (2013), the Supreme Court held that the National Voter Registration Act (NVRA) "
            "preempts state laws requiring extra proof of citizenship beyond the federal voter registration form."
        ),
        "level_4_primary_authority": [
            {
                "citation": "52 U.S.C. § 10301 (Voting Rights Act § 2)",
                "source_type": "STATUTE",
                "official_portal_url": "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title52-section10301&num=0&edition=prelim",
                "key_holding_or_text": (
                    "No voting qualification or prerequisite to voting or standard, practice, or procedure shall be imposed or applied by any "
                    "State or political subdivision in a manner which results in a denial or abridgement of the right of any citizen of the "
                    "United States to vote on account of race or color, or in contravention of the guarantees set forth in section 10303(f)(2)."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "Arizona v. Inter Tribal Council of Arizona, Inc., 570 U.S. 1 (2013)",
                "source_type": "CASELAW",
                "official_portal_url": "https://supreme.justia.com/cases/federal/us/570/1/",
                "key_holding_or_text": (
                    "The National Voter Registration Act's requirement that States 'accept and use' the Federal Form preempts Arizona's law "
                    "requiring state-prescribed documentary evidence of citizenship."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            },
            {
                "citation": "52 U.S.C. § 10503 (Voting Rights Act § 203)",
                "source_type": "STATUTE",
                "official_portal_url": "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title52-section10503&num=0&edition=prelim",
                "key_holding_or_text": (
                    "Mandates bilingual election materials and oral language assistance in jurisdictions meeting statutory population thresholds for American Indian language groups."
                ),
                "jurisdiction": "US",
                "is_binding": True,
                "verification_status": "VERIFIED"
            }
        ],
        "level_5_advanced_analysis": (
            "Domestic U.S. law vs. International Norms:\n"
            "- Domestic Law: While the Voting Rights Act provides robust statutory tools to combat vote dilution and geographical barriers, "
            "the Supreme Court's decisions in Shelby County v. Holder (570 U.S. 529, invalidating VRA preclearance) and Brnovich v. Democratic "
            "National Committee (594 U.S. 647, 2021, heightening Section 2 burden of proof for ballot collection rules) have constrained federal remedies.\n"
            "- UNDRIP (International Norm — non-binding in U.S. domestic proceedings): Article 5 and Article 18 affirm the right of Indigenous peoples "
            "to participate fully in all levels of decision-making in matters that affect their rights, through representatives chosen by themselves.\n"
            "- Alignment & Divergence: Federal protections secure formal de jure voting equality, but geographic isolation, mail delivery limitations, "
            "and strict state photo ID requirements continue to produce de facto disparities in reservation turnout.\n"
            "- Competing Positions: State election officials argue that uniform voting rules, in-person precinct voting, and ballot collection restrictions "
            "deter voter fraud and promote administrative efficiency. Tribal advocates and civil rights organizations argue that applying rigid municipal "
            "voting rules to vast rural reservations without residential mail delivery severely suppresses Indigenous turnout."
        ),
        "drill_downs": {
            "SHOW_SOURCE": {
                "title": "Voting Rights Act Statutory Provisions",
                "content": "52 U.S.C. §§ 10301 and 10503 protect minority voters and mandate bilingual assistance for Native language groups.",
                "citations": ["52 U.S.C. § 10301", "52 U.S.C. § 10503"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_STATUTE": {
                "title": "National Voter Registration Act",
                "content": "52 U.S.C. § 20508 regulates federal voter registration forms, preventing states from adding unauthorized barriers.",
                "citations": ["52 U.S.C. § 20508"],
                "official_sources": ["https://uscode.house.gov/"]
            },
            "SHOW_CASE": {
                "title": "Controlling Precedent: Arizona v. Inter Tribal Council of Arizona (2013)",
                "content": "Holding that federal voter registration forms preempt restrictive state documentary proof requirements under the Elections Clause.",
                "citations": ["Arizona v. Inter Tribal Council of Arizona, Inc., 570 U.S. 1 (2013)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/570/1/"]
            },
            "EXPLAIN_OPPOSING": {
                "title": "State Election Integrity Arguments in Brnovich",
                "content": "In Brnovich v. DNC (2021), Arizona successfully defended out-of-precinct ballot rejection and third-party ballot collection bans under Section 2 review.",
                "citations": ["Brnovich v. Democratic National Committee, 594 U.S. 647 (2021)"],
                "official_sources": ["https://supreme.justia.com/cases/federal/us/594/19-1257/"]
            },
            "SHOW_TEMPORAL_CHANGE": {
                "title": "Historical Disenfranchisement to Modern Legal Protections",
                "content": "Although the Indian Citizenship Act was passed in 1924, states like Arizona and New Mexico excluded Native voters until state supreme court decisions in 1948 (Harrison v. Laveen, 196 P.2d 456).",
                "citations": ["Harrison v. Laveen, 196 P.2d 456 (Ariz. 1948)"],
                "official_sources": ["https://scholar.google.com/"]
            }
        },
        "related_concepts": ["blood_quantum_vs_citizenship", "tribal_sovereignty", "due_process"]
    }
}


def build_pack_c():
    CONCEPTS_DIR.mkdir(parents=True, exist_ok=True)
    for cid, data in PACK_C.items():
        out_file = CONCEPTS_DIR / f"{cid}.yaml"
        with open(out_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
        print(f"Created concept YAML: {out_file.name}")
    print(f"Successfully generated all {len(PACK_C)} Pack C concepts in {CONCEPTS_DIR}.")


if __name__ == "__main__":
    build_pack_c()
