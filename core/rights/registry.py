"""Registry of canonical legal rights, authorities, required facts, exceptions, and counterarguments."""

from datetime import date
from typing import Dict, List
from core.rights.models import LegalBasis, RightCategory, RightDefinition


CANONICAL_RIGHTS: List[RightDefinition] = [
    # 1. CONSTITUTIONAL RIGHTS / LIBERTY INTERESTS / PARENTAL RIGHTS
    RightDefinition(
        right_id="const_parental_liberty_troxel",
        right_name="Fundamental Liberty Interest in Care, Custody, and Control of Children",
        category=RightCategory.PARENTAL_RIGHTS,
        legal_basis=LegalBasis.CONSTITUTIONAL,
        authority_tier="TIER_0",
        authority="U.S. Const. amend. XIV, § 1 (Due Process Clause); Troxel v. Granville, 530 U.S. 57 (2000)",
        citation="530 U.S. 57",
        jurisdiction="US",
        procedural_context=["INVESTIGATION", "EMERGENCY_REMOVAL", "SHELTER_HEARING", "ADJUDICATION", "TERMINATION"],
        required_facts=[
            "Parent-child legal or biological relationship exists",
            "State interference or proposed limitation on parent's custodial authority"
        ],
        known_exceptions=[
            "Emergency imminent harm or severe physical danger to child",
            "Judicial finding of parental unfitness under clear and convincing evidence standard"
        ],
        counterarguments=[
            "State's parens patriae duty to protect child welfare supersedes parental presumption",
            "Parent voluntarily relinquished temporary physical custody"
        ],
        core_holding="The Due Process Clause of the Fourteenth Amendment protects the fundamental right of parents to make decisions concerning the care, custody, and control of their children."
    ),

    # 2. DUE PROCESS PROTECTIONS / STANDARD OF PROOF
    RightDefinition(
        right_id="const_due_process_santosky",
        right_name="Heightened Standard of Proof in Termination of Parental Rights",
        category=RightCategory.DUE_PROCESS_PROTECTIONS,
        legal_basis=LegalBasis.CONSTITUTIONAL,
        authority_tier="TIER_0",
        authority="U.S. Const. amend. XIV, § 1; Santosky v. Kramer, 455 U.S. 745 (1982)",
        citation="455 U.S. 745",
        jurisdiction="US",
        procedural_context=["TERMINATION", "PERMANENCY_HEARING"],
        required_facts=[
            "State agency petitions for permanent termination of parental rights",
            "Evidentiary hearing before a judicial fact-finder"
        ],
        known_exceptions=[
            "Voluntary statutory surrender or consent to adoption"
        ],
        counterarguments=[
            "Preponderance of evidence applied only to temporary interim detention, not permanent termination",
            "Parental rights were not permanently severed, only physical placement transferred"
        ],
        core_holding="Before a State may sever completely and irrevocably the rights of parents in their natural child, due process requires that the State support its allegations by at least clear and convincing evidence."
    ),

    # 3. SEARCH & SEIZURE PROTECTIONS / PRIVACY RIGHTS
    RightDefinition(
        right_id="const_fourth_amendment_home_entry",
        right_name="Protection Against Warrantless Entry and Unreasonable Seizure in the Home",
        category=RightCategory.SEARCH_SEIZURE_PROTECTIONS,
        legal_basis=LegalBasis.CONSTITUTIONAL,
        authority_tier="TIER_0",
        authority="U.S. Const. amend. IV; Doe v. Heck, 327 F.3d 492 (7th Cir. 2003); Camara v. Municipal Court, 387 U.S. 523 (1967)",
        citation="327 F.3d 492",
        jurisdiction="US",
        procedural_context=["INVESTIGATION", "EMERGENCY_REMOVAL"],
        required_facts=[
            "Government official (caseworker or law enforcement) entered private residence without consent",
            "Child or person seized or physical residence inspected"
        ],
        known_exceptions=[
            "Valid judicial warrant or court order authorizing entry",
            "True exigent circumstances: reasonable cause to believe child faces imminent, serious physical bodily injury before a warrant can be secured",
            "Voluntary, uncoerced consent given by authorized adult occupant"
        ],
        counterarguments=[
            "Caseworker acted under administrative welfare check exception without coercive search intent",
            "Occupant consented to entry or opened door voluntarily",
            "Qualified immunity protects officer where emergency exigency was reasonably debatable"
        ],
        conflicting_procedures=["State statutory provisions authorizing summary casework entry upon unverified reports"],
        core_holding="Child welfare workers and police cannot enter a private home or seize a child without a warrant, court order, parental consent, or immediate exigent circumstances of imminent bodily harm."
    ),

    # 4. NOTICE RIGHTS / PROCEDURAL DUE PROCESS
    RightDefinition(
        right_id="const_notice_mullane",
        right_name="Procedural Due Process Right to Timely and Meaningful Notice of Allegations",
        category=RightCategory.NOTICE_RIGHTS,
        legal_basis=LegalBasis.CONSTITUTIONAL,
        authority_tier="TIER_0",
        authority="U.S. Const. amend. XIV, § 1; Mullane v. Central Hanover Bank & Trust Co., 339 U.S. 306 (1950)",
        citation="339 U.S. 306",
        jurisdiction="US",
        procedural_context=["INVESTIGATION", "EMERGENCY_REMOVAL", "SHELTER_HEARING", "ADJUDICATION"],
        required_facts=[
            "State initiated formal legal proceedings or deprivation of custody",
            "Parent or affected party entitled to service of process"
        ],
        known_exceptions=[
            "Emergency ex parte removal where pre-deprivation notice is impossible due to imminent peril (must be followed by prompt post-deprivation notice)"
        ],
        counterarguments=[
            "Constructive or verbal notice was conveyed at the scene",
            "Notice was mailed to last known address in good faith compliance",
            "Parent waived formal service by voluntarily appearing at hearing"
        ],
        core_holding="An elementary and fundamental requirement of due process in any proceeding which is to be accorded finality is notice reasonably calculated, under all circumstances, to apprise interested parties of the pendency of the action."
    ),

    # 5. HEARING RIGHTS / DUE PROCESS PROTECTIONS
    RightDefinition(
        right_id="const_hearing_mathews",
        right_name="Right to Meaningful Opportunity to be Heard Before an Impartial Decisionmaker",
        category=RightCategory.HEARING_RIGHTS,
        legal_basis=LegalBasis.CONSTITUTIONAL,
        authority_tier="TIER_0",
        authority="U.S. Const. amend. XIV; Mathews v. Eldridge, 424 U.S. 319 (1976)",
        citation="424 U.S. 319",
        jurisdiction="US",
        procedural_context=["SHELTER_HEARING", "ADJUDICATION", "DISPOSITION", "ADMINISTRATIVE_HEARING"],
        required_facts=[
            "State deprivation of protected liberty or property interest",
            "Adjudicative or administrative forum"
        ],
        known_exceptions=[
            "Temporary emergency restraint prior to full evidentiary hearing",
            "Procedural waiver"
        ],
        counterarguments=[
            "Three-factor Mathews balancing justifies expedited proceedings given paramount state interest in child protection",
            "Evidentiary rules relaxed at emergency preliminary detention stage"
        ],
        core_holding="Due process requires the opportunity to be heard at a meaningful time and in a meaningful manner, balancing private interest, risk of erroneous deprivation, and government burden."
    ),

    # 6. COUNSEL RIGHTS / DUE PROCESS
    RightDefinition(
        right_id="const_counsel_lassiter",
        right_name="Due Process Right to Appointed Counsel in Parental Severance",
        category=RightCategory.COUNSEL_RIGHTS,
        legal_basis=LegalBasis.CONSTITUTIONAL,
        authority_tier="TIER_0",
        authority="U.S. Const. amend. XIV; Lassiter v. Department of Social Services, 452 U.S. 18 (1981)",
        citation="452 U.S. 18",
        jurisdiction="US",
        procedural_context=["TERMINATION", "ADJUDICATION"],
        required_facts=[
            "Indigent parent facing termination of parental rights",
            "Complex legal or evidentiary allegations where presence of counsel is essential to fairness"
        ],
        known_exceptions=[
            "Non-indigent parents with ability to retain private counsel",
            "Simple proceedings without risk of criminal prosecution or expert testimony where court finds counsel not constitutionally required (federal baseline)"
        ],
        counterarguments=[
            "Federal constitutional baseline leaves appointment to case-by-case discretion (though state statutes routinely mandate appointment)",
            "Parent waived right to counsel knowingly and voluntarily"
        ],
        core_holding="The Constitution does not mandate appointed counsel for indigent parents in every termination proceeding, but requires appointment when fundamental fairness demands it under the Mathews factors."
    ),

    # 7. STATUTORY COUNSEL RIGHTS (WASHINGTON STATE)
    RightDefinition(
        right_id="stat_wa_counsel_rcw_13_34_090",
        right_name="Mandatory Right to Appointed Counsel for Indigent Parents in Dependency",
        category=RightCategory.COUNSEL_RIGHTS,
        legal_basis=LegalBasis.STATUTORY,
        authority_tier="TIER_0",
        authority="Washington Revised Code RCW 13.34.090(2)",
        citation="RCW 13.34.090",
        jurisdiction="US-WA",
        effective_date_start=date(1977, 1, 1),
        procedural_context=["EMERGENCY_REMOVAL", "SHELTER_HEARING", "ADJUDICATION", "TERMINATION"],
        required_facts=[
            "Parent is a party to a dependency or termination proceeding in Washington State",
            "Parent qualifies as indigent or unable to afford legal counsel"
        ],
        known_exceptions=[
            "Parent affirmatively and knowingly waives right to counsel on the record",
            "Parent has financial resources exceeding statutory indigency threshold"
        ],
        counterarguments=[
            "Parent failed to submit financial eligibility documentation or application",
            "Counsel was appointed at initial appearance and prior investigative interview did not constitute a critical court stage"
        ],
        core_holding="At all stages of a dependency proceeding in Washington, parents have the absolute statutory right to be represented by counsel, and indigent parents must have counsel appointed immediately by the court."
    ),

    # 8. STATUTORY SHELTER HEARING DEADLINE (WASHINGTON STATE)
    RightDefinition(
        right_id="stat_wa_shelter_72h_rcw_13_34_065",
        right_name="Strict 72-Hour Judicial Shelter Hearing Deadline Following Removal",
        category=RightCategory.PROCEDURAL_RIGHTS,
        legal_basis=LegalBasis.STATUTORY,
        authority_tier="TIER_0",
        authority="Washington Revised Code RCW 13.34.065(1)",
        citation="RCW 13.34.065",
        jurisdiction="US-WA",
        effective_date_start=date(1979, 1, 1),
        procedural_context=["EMERGENCY_REMOVAL", "SHELTER_HEARING"],
        required_facts=[
            "Child placed in custody of DCYF or law enforcement protective custody in Washington State",
            "Ex parte removal without prior full contested hearing"
        ],
        known_exceptions=[
            "Exclusion of Saturdays, Sundays, and legal court holidays from the 72-hour calculation",
            "Formal continuance requested by parent or child's counsel"
        ],
        counterarguments=[
            "72 hours have not elapsed when excluding court weekend/holiday hours",
            "Continuance granted for good cause upon motion of defense"
        ],
        core_holding="The court must hold a shelter care hearing within seventy-two hours, excluding Saturdays, Sundays, and holidays, after a child is taken into custody."
    ),

    # 9. STATUTORY COUNSEL & NOTICE (ILLINOIS)
    RightDefinition(
        right_id="stat_il_counsel_notice_705_ilcs_405",
        right_name="Statutory Rights to Notice, Counsel, and Explanation of Proceedings",
        category=RightCategory.STATUTORY_RIGHTS,
        legal_basis=LegalBasis.STATUTORY,
        authority_tier="TIER_0",
        authority="Illinois Compiled Statutes 705 ILCS 405/1-5; 705 ILCS 405/2-9",
        citation="705 ILCS 405/1-5",
        jurisdiction="US-IL",
        effective_date_start=date(1987, 1, 1),
        procedural_context=["EMERGENCY_REMOVAL", "SHELTER_HEARING", "ADJUDICATION"],
        required_facts=[
            "Juvenile court proceeding commenced under Article II of Illinois Juvenile Court Act",
            "Party is a parent, guardian, or legal custodian"
        ],
        known_exceptions=[
            "Explicit waiver on the court record",
            "Financial disqualification from appointed indigent defense"
        ],
        counterarguments=[
            "Public Defender was formally assigned at earliest call of the court call sheet",
            "Service by publication attempted following diligent search"
        ],
        core_holding="Parents and legal guardians have the statutory right to be present, to be heard, to present evidence material to the proceedings, to cross-examine witnesses, and to be represented by counsel in all proceedings under the Illinois Juvenile Court Act."
    ),

    # 10. STATUTORY SHELTER HEARING DEADLINE (ILLINOIS)
    RightDefinition(
        right_id="stat_il_temporary_custody_48h_705_ilcs_405_2_9",
        right_name="Strict 48-Hour Temporary Custody Hearing Mandate",
        category=RightCategory.PROCEDURAL_RIGHTS,
        legal_basis=LegalBasis.STATUTORY,
        authority_tier="TIER_0",
        authority="Illinois Compiled Statutes 705 ILCS 405/2-9(1)",
        citation="705 ILCS 405/2-9",
        jurisdiction="US-IL",
        effective_date_start=date(1987, 1, 1),
        procedural_context=["EMERGENCY_REMOVAL", "SHELTER_HEARING"],
        required_facts=[
            "Minor taken into temporary protective custody in Illinois",
            "Detention by DCFS or law enforcement"
        ],
        known_exceptions=[
            "Exclusion of Saturdays, Sundays, and legal court holidays",
            "Continuance on motion of parent or custodian"
        ],
        counterarguments=[
            "48 hours does not include intervening court holiday",
            "Minor was brought before judicial officer within statutory clock"
        ],
        core_holding="Unless sooner released, a minor taken into temporary custody must be brought before a judicial officer within 48 hours, exclusive of Saturdays, Sundays, and court-designated holidays, for a temporary custody hearing."
    ),

    # 11. DISABILITY RIGHTS / REASONABLE ACCOMMODATION
    RightDefinition(
        right_id="civ_ada_title_ii_child_welfare",
        right_name="Right to Non-Discrimination and Reasonable Accommodation in State Services",
        category=RightCategory.DISABILITY_RIGHTS,
        legal_basis=LegalBasis.STATUTORY,
        authority_tier="TIER_0",
        authority="Americans with Disabilities Act Title II, 42 U.S.C. § 12132; 28 C.F.R. § 35.130; DOJ/HHS Joint Guidance (2015)",
        citation="42 U.S.C. § 12132",
        jurisdiction="US",
        effective_date_start=date(1992, 1, 26),
        procedural_context=["INVESTIGATION", "REASONABLE_EFFORTS", "SERVICE_PLAN", "TERMINATION"],
        required_facts=[
            "Parent or child qualifies as an individual with a recognized physical, mental, or intellectual disability",
            "Public state agency (e.g. child welfare department) provides services, programs, or activities"
        ],
        known_exceptions=[
            "Requested accommodation would impose fundamental alteration to the nature of the program or undue financial/administrative burden",
            "Individual poses a direct threat to the health or safety of others that cannot be mitigated"
        ],
        counterarguments=[
            "Parent never disclosed disability or requested tailored accommodation",
            "Agency provided standardized services sufficient for general public",
            "ADA cannot be used as an absolute defense against termination where child's safety is at immediate risk"
        ],
        core_holding="No qualified individual with a disability shall, by reason of such disability, be excluded from participation in or be denied the benefits of the services, programs, or activities of a public entity, or be subjected to discrimination."
    ),

    # 12. FAMILY-ASSOCIATION INTERESTS / KINSHIP PLACEMENT PREFERENCE
    RightDefinition(
        right_id="stat_title_iv_e_kinship_preference",
        right_name="Kinship Placement Notification and Preference Requirement",
        category=RightCategory.FAMILY_ASSOCIATION_INTERESTS,
        legal_basis=LegalBasis.STATUTORY,
        authority_tier="TIER_0",
        authority="Social Security Act Title IV-E, 42 U.S.C. § 671(a)(19), (a)(29)",
        citation="42 U.S.C. § 671",
        jurisdiction="US",
        effective_date_start=date(2008, 10, 7),
        procedural_context=["EMERGENCY_REMOVAL", "PLACEMENT", "DISPOSITION"],
        required_facts=[
            "Child removed from parental home into state foster care",
            "Adult relatives or grandparents available and identifiable"
        ],
        known_exceptions=[
            "Relative fails criminal history background check or child abuse central registry clearance",
            "Placement with relative contrary to child's verified best interest or medical safety"
        ],
        counterarguments=[
            "Agency exercised diligent search but no suitable relative came forward within 30 days",
            "Relative home environment found unsafe upon walk-through inspection"
        ],
        core_holding="State child welfare agencies receiving Title IV-E funding must exercise due diligence to identify and provide notice to all adult grandparents and other adult relatives within 30 days of removal, and give preference to an adult relative over a non-related caregiver."
    ),

    # 13. CHILD RIGHTS / TRIBAL SOVEREIGNTY / ICWA ACTIVE EFFORTS
    RightDefinition(
        right_id="stat_icwa_active_efforts_25_usc_1912",
        right_name="Mandatory Active Efforts and Heightened Evidentiary Standards for Indian Children",
        category=RightCategory.CHILD_RIGHTS,
        legal_basis=LegalBasis.STATUTORY,
        authority_tier="TIER_0",
        authority="Indian Child Welfare Act, 25 U.S.C. § 1912(d), (e), (f); 25 C.F.R. § 23.120",
        citation="25 U.S.C. § 1912",
        jurisdiction="US",
        effective_date_start=date(1978, 11, 8),
        procedural_context=["INVESTIGATION", "EMERGENCY_REMOVAL", "SHELTER_HEARING", "ADJUDICATION", "TERMINATION"],
        required_facts=[
            "Child is an unmarried person under 18 who is either a member of an Indian tribe or eligible for membership and the biological child of a member",
            "Child custody proceeding in state court"
        ],
        known_exceptions=[
            "Emergency removal permitted only to prevent imminent physical damage or harm, and must terminate immediately when emergency ends or child is transferred to tribal jurisdiction"
        ],
        counterarguments=[
            "Child is not an Indian Child as verified by formal tribal response",
            "Proceeding is an intra-family divorce custody dispute exempt from ICWA"
        ],
        core_holding="Any party seeking foster care placement or termination of parental rights must satisfy the court that active efforts have been made to provide remedial services and rehabilitative programs designed to prevent the breakup of the Indian family and that these efforts have proved unsuccessful."
    ),

    # 14. CIVIL RIGHTS / DISCRIMINATION
    RightDefinition(
        right_id="civ_title_vi_non_discrimination",
        right_name="Title VI Protection Against Race and National Origin Discrimination",
        category=RightCategory.CIVIL_RIGHTS,
        legal_basis=LegalBasis.STATUTORY,
        authority_tier="TIER_0",
        authority="Civil Rights Act of 1964 Title VI, 42 U.S.C. § 2000d",
        citation="42 U.S.C. § 2000d",
        jurisdiction="US",
        effective_date_start=date(1964, 7, 2),
        procedural_context=["INVESTIGATION", "SERVICE_PLAN", "REASONABLE_EFFORTS"],
        required_facts=[
            "Recipient program receives federal financial assistance",
            "Disparate intentional discrimination or language barrier denial of services"
        ],
        known_exceptions=[
            "Legitimate non-discriminatory statutory child safety determination"
        ],
        counterarguments=[
            "Action based solely on objective child endangerment facts, not racial or ethnic animus",
            "Title VI requires showing of intentional discrimination for compensatory damages"
        ],
        core_holding="No person in the United States shall, on the ground of race, color, or national origin, be excluded from participation in, be denied the benefits of, or be subjected to discrimination under any program or activity receiving Federal financial assistance."
    ),

    # 15. ADMINISTRATIVE RIGHTS / REGISTRY EXPUNGEMENT
    RightDefinition(
        right_id="admin_capta_central_registry_appeal",
        right_name="Right to Administrative Due Process and Appeal of Child Abuse Central Registry Finding",
        category=RightCategory.ADMINISTRATIVE_RIGHTS,
        legal_basis=LegalBasis.ADMINISTRATIVE,
        authority_tier="TIER_0",
        authority="Child Abuse Prevention and Treatment Act (CAPTA), 42 U.S.C. § 5106a(b)(2)(B)(viii); State Administrative Procedure Acts",
        citation="42 U.S.C. § 5106a",
        jurisdiction="US",
        effective_date_start=date(1996, 10, 3),
        procedural_context=["ADMINISTRATIVE_HEARING", "INVESTIGATION"],
        required_facts=[
            "State agency issued an 'indicated' or 'founded' administrative finding of child abuse or neglect",
            "Individual's name placed on state central abuse registry"
        ],
        known_exceptions=[
            "Collateral estoppel or res judicata where juvenile court has entered an identical judicial finding after full contested hearing"
        ],
        counterarguments=[
            "Individual failed to file administrative hearing request within mandatory statutory deadline (e.g. 30 or 60 days from notice)",
            "Administrative finding supported by credible evidence"
        ],
        core_holding="States must provide individuals against whom an indicated finding of abuse or neglect is made an opportunity to appeal and seek expungement or amendment of the central registry record through administrative due process."
    ),

    # 16. RELIGIOUS RIGHTS / MEDICAL TREATMENT DISPUTES
    RightDefinition(
        right_id="const_religious_freedom_treatment",
        right_name="Religious Freedom and Parental Decision-Making Protections",
        category=RightCategory.RELIGIOUS_RIGHTS,
        legal_basis=LegalBasis.CONSTITUTIONAL,
        authority_tier="TIER_0",
        authority="U.S. Const. amend. I (Free Exercise Clause); Wisconsin v. Yoder, 406 U.S. 205 (1972); Prince v. Massachusetts, 321 U.S. 158 (1944)",
        citation="406 U.S. 205",
        jurisdiction="US",
        procedural_context=["INVESTIGATION", "MEDICAL_DECISIONS"],
        required_facts=[
            "Sincere religious belief or practice governing family life or medical care",
            "State agency coercion or mandate infringing upon religious observance"
        ],
        known_exceptions=[
            "Prince exception: Parents may not make martyrs of their children; state may compel life-saving or limb-preserving emergency medical care",
            "Preventing severe, irreversible physical impairment or death"
        ],
        counterarguments=[
            "Child's immediate medical necessity overrides parental religious objection under Prince doctrine",
            "State neutral law of general applicability"
        ],
        core_holding="Parental religious freedom is subject to limitation where the child's life, physical health, or safety is directly and gravely endangered."
    ),

    # 17. APPEAL RIGHTS / ACCESS TO TRANSCRIPTS
    RightDefinition(
        right_id="const_appeal_transcript_mlb",
        right_name="Right to Indigent Appellate Record and Appeal of Parental Rights Severance",
        category=RightCategory.APPEAL_RIGHTS,
        legal_basis=LegalBasis.CONSTITUTIONAL,
        authority_tier="TIER_0",
        authority="M.L.B. v. S.L.J., 519 U.S. 102 (1996); U.S. Const. amend. XIV",
        citation="519 U.S. 102",
        jurisdiction="US",
        procedural_context=["APPEAL"],
        required_facts=[
            "Indigent parent seeks appellate review of trial court order terminating parental rights",
            "State law conditioned appeal upon payment of record preparation fees or trial transcript costs"
        ],
        known_exceptions=[
            "Non-indigent litigants capable of paying filing fees",
            "Frivolous appeals lacking any arguable legal basis under Anders procedures"
        ],
        counterarguments=[
            "Order appealed is an interlocutory dependency review order, not a final termination decree",
            "Notice of appeal was untimely filed past jurisdictional deadline"
        ],
        core_holding="Just as in criminal cases, a State may not block an indigent parent's appeal from the permanent termination of parental rights based on inability to pay record preparation and transcript fees."
    ),

    # 18. EQUAL PROTECTION CONCERNS
    RightDefinition(
        right_id="const_equal_protection_disparities",
        right_name="Equal Protection Protection Against Selective Enforcement and Bias",
        category=RightCategory.EQUAL_PROTECTION_CONCERNS,
        legal_basis=LegalBasis.CONSTITUTIONAL,
        authority_tier="TIER_0",
        authority="U.S. Const. amend. XIV, § 1 (Equal Protection Clause); Village of Arlington Heights v. Metropolitan Housing Dev. Corp., 429 U.S. 252 (1977)",
        citation="429 U.S. 252",
        jurisdiction="US",
        procedural_context=["INVESTIGATION", "EMERGENCY_REMOVAL"],
        required_facts=[
            "Differential treatment compared to similarly situated families",
            "Protected class membership or fundamental right burden"
        ],
        known_exceptions=[
            "Differential treatment justified by compelling state interest in child protection and narrowly tailored means",
            "Individualized safety risk assessment rather than class-based classification"
        ],
        counterarguments=[
            "Statistical racial or socioeconomic disparity alone does not establish discriminatory intent required under Arlington Heights",
            "Caseworker acted upon specific, substantiated danger indicators rather than discriminatory motive"
        ],
        core_holding="The Equal Protection Clause prohibits state child welfare authorities from invidious discrimination based on race, national origin, or protected traits, requiring proof of discriminatory intent."
    ),

    # 19. PROPERTY INTERESTS / BENEFITS DUE PROCESS
    RightDefinition(
        right_id="const_property_benefits_goldberg",
        right_name="Procedural Due Process Protection for Statutory Entitlement Benefits",
        category=RightCategory.PROPERTY_INTERESTS,
        legal_basis=LegalBasis.CONSTITUTIONAL,
        authority_tier="TIER_0",
        authority="Goldberg v. Kelly, 397 U.S. 254 (1970); U.S. Const. amend. XIV",
        citation="397 U.S. 254",
        jurisdiction="US",
        procedural_context=["ADMINISTRATIVE_HEARING", "SERVICE_PLAN"],
        required_facts=[
            "Termination or reduction of statutory public assistance, foster care maintenance payments, or child welfare subsidies",
            "Recipient had established statutory entitlement"
        ],
        known_exceptions=[
            "Statewide across-the-board legislative statutory rate reductions or program expirations",
            "Automatic adjustments due to verifiable changes in household earned income"
        ],
        counterarguments=[
            "Adequate post-deprivation administrative remedy satisfies due process",
            "Benefit program was discretionary rather than an entitlement"
        ],
        core_holding="Under the Due Process Clause, recipients of statutory public assistance are entitled to an evidentiary hearing before the termination of benefits."
    ),

    # 20. PRIVACY RIGHTS / INFORMATIONAL PRIVACY
    RightDefinition(
        right_id="priv_medical_records_hipaa_state",
        right_name="Right to Confidentiality of Medical and Mental Health Records",
        category=RightCategory.PRIVACY_RIGHTS,
        legal_basis=LegalBasis.STATUTORY,
        authority_tier="TIER_0",
        authority="45 C.F.R. § 164.512; Jaffee v. Redmond, 518 U.S. 1 (1996); State Psychotherapist-Patient Privilege",
        citation="45 C.F.R. § 164.512",
        jurisdiction="US",
        procedural_context=["INVESTIGATION", "DISCOVERY", "ADJUDICATION"],
        required_facts=[
            "Child welfare agency seeks confidential psychotherapeutic, mental health, or substance abuse treatment records",
            "Records created during confidential healthcare consultation"
        ],
        known_exceptions=[
            "Mandatory child abuse reporting disclosures",
            "Specific judicial court order or subpoena issued following in camera review",
            "Valid written patient authorization"
        ],
        counterarguments=[
            "Parent placed mental health at issue by claiming fitness to care for special-needs child",
            "Statutory mandatory reporter exception overrides healthcare privacy"
        ],
        core_holding="Confidential communications between a patient and a licensed psychotherapist are protected from compelled disclosure unless a recognized statutory exception or valid judicial authorization applies."
    ),

    # 21. FLORIDA STATUTORY EMERGENCY REMOVAL & SHELTER HEARING
    RightDefinition(
        right_id="stat_fl_shelter_24h_stat_39_402",
        right_name="Florida 24-Hour Judicial Shelter Hearing Deadline",
        category=RightCategory.PROCEDURAL_RIGHTS,
        legal_basis=LegalBasis.STATUTORY,
        authority_tier="TIER_0",
        authority="Florida Statutes § 39.402(1)",
        citation="Fla. Stat. § 39.402",
        jurisdiction="US-FL",
        effective_date_start=date(1998, 10, 1),
        procedural_context=["EMERGENCY_REMOVAL", "SHELTER_HEARING"],
        required_facts=[
            "Child taken into custody by DCF or law enforcement in Florida",
            "Placement in emergency shelter care"
        ],
        known_exceptions=[
            "No weekend or holiday exclusion: Florida statute strictly requires hearing within 24 hours of removal"
        ],
        counterarguments=[
            "Child was not taken into state custody (e.g. voluntary relative safety plan)",
            "Hearing held within exact 24-hour hour-to-hour timestamp"
        ],
        core_holding="Under Florida law, a child taken into custody shall not be held in a shelter longer than 24 hours without a judicial shelter hearing before the court."
    ),

    # 22. OHIO STATUTORY COUNSEL AND NOTICE
    RightDefinition(
        right_id="stat_oh_counsel_notice_orc_2151_352",
        right_name="Ohio Statutory Right to Counsel for Indigent Parties in Juvenile Court",
        category=RightCategory.COUNSEL_RIGHTS,
        legal_basis=LegalBasis.STATUTORY,
        authority_tier="TIER_0",
        authority="Ohio Revised Code ORC § 2151.352; Juv.R. 4",
        citation="ORC § 2151.352",
        jurisdiction="US-OH",
        effective_date_start=date(1969, 11, 19),
        procedural_context=["EMERGENCY_REMOVAL", "SHELTER_HEARING", "ADJUDICATION"],
        required_facts=[
            "Child or parent is a party to juvenile court proceeding in Ohio",
            "Party qualifies as indigent"
        ],
        known_exceptions=[
            "Knowing and voluntary waiver by adult parent"
        ],
        counterarguments=[
            "Party has not established indigency on record",
            "Counsel provided at shelter hearing"
        ],
        core_holding="A child or parent is entitled to representation by legal counsel at all stages of proceedings under ORC Chapter 2151, and if indigent, counsel must be appointed."
    ),

    # 23. CONSTITUTIONAL RIGHTS / SUBSTANTIVE DUE PROCESS
    RightDefinition(
        right_id="const_fourteenth_substantive_due_process",
        right_name="Fourteenth Amendment Substantive Due Process Family Integrity Protection",
        category=RightCategory.CONSTITUTIONAL_RIGHTS,
        legal_basis=LegalBasis.CONSTITUTIONAL,
        authority_tier="TIER_0",
        authority="U.S. Const. amend. XIV, § 1; Meyer v. Nebraska, 262 U.S. 390 (1923); Pierce v. Society of Sisters, 268 U.S. 510 (1925)",
        citation="262 U.S. 390",
        jurisdiction="US",
        procedural_context=["INVESTIGATION", "EMERGENCY_REMOVAL", "SHELTER_HEARING", "ADJUDICATION", "TERMINATION"],
        required_facts=[
            "State action intruding upon core private family decision-making or parent-child relationship",
            "Absence of compelling state interest narrowly tailored"
        ],
        known_exceptions=[
            "Imminent child physical peril or substantiated grave abuse",
            "Neutral compulsory child safety laws"
        ],
        counterarguments=[
            "State acting strictly under compelling child protective mandate",
            "De minimis interference"
        ],
        core_holding="The Fourteenth Amendment protects the fundamental substantive due process right of individuals to establish a home and bring up children free from arbitrary state interference."
    ),

    # 24. LIBERTY INTERESTS / STIGMA-PLUS DOCTRINE
    RightDefinition(
        right_id="const_liberty_interest_stigma_plus",
        right_name="Liberty Interest in Reputation Combined with Tangible Legal Status Loss (Stigma-Plus)",
        category=RightCategory.LIBERTY_INTERESTS,
        legal_basis=LegalBasis.CONSTITUTIONAL,
        authority_tier="TIER_0",
        authority="Paul v. Davis, 424 U.S. 693 (1976); Valmonte v. Bane, 18 F.3d 992 (2d Cir. 1994); U.S. Const. amend. XIV",
        citation="424 U.S. 693",
        jurisdiction="US",
        procedural_context=["ADMINISTRATIVE_HEARING", "INVESTIGATION", "CENTRAL_REGISTRY"],
        required_facts=[
            "Government action imposes severe reputational stigma (e.g. child abuse central registry listing)",
            "Coupled with tangible loss or alteration of legal right, employment eligibility, or custodial status (the 'plus' factor)"
        ],
        known_exceptions=[
            "Defamation without any alteration of legal status or statutory benefit",
            "Registry listings post-conviction in criminal court"
        ],
        counterarguments=[
            "Registry listing is purely administrative record without automatic disqualification",
            "Adequate post-deprivation administrative hearing available"
        ],
        core_holding="Under the stigma-plus doctrine, reputational harm from state child abuse labeling combined with statutory exclusion from employment or custody constitutes a deprivation of a protected Fourteenth Amendment liberty interest."
    )
]


class RightsRegistry:
    """Provides indexed access to canonical rights."""
    
    @classmethod
    def get_all(cls) -> List[RightDefinition]:
        return list(CANONICAL_RIGHTS)

    @classmethod
    def get_by_id(cls, right_id: str) -> RightDefinition | None:
        for r in CANONICAL_RIGHTS:
            if r.right_id == right_id:
                return r
        return None

    @classmethod
    def get_by_category(cls, category: RightCategory) -> List[RightDefinition]:
        return [r for r in CANONICAL_RIGHTS if r.category == category]

    @classmethod
    def get_by_jurisdiction(cls, jurisdiction: str) -> List[RightDefinition]:
        norm_j = jurisdiction.upper()
        if not norm_j.startswith("US-") and norm_j != "US":
            norm_j = f"US-{norm_j}"
        return [r for r in CANONICAL_RIGHTS if r.jurisdiction in ("US", norm_j)]
