"""Database Seed Script: Pre-populates SQLite and Vector Index with authoritative core statutes across Anchor States & Federal Law."""

from datetime import date
from storage.db import LegalDatabase
from storage.vector_store import SimpleHybridStore
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import StatuteChunker


def build_seed_documents() -> list[LegalDocument]:
    docs = []

    # 1. WA RCW 13.34.050 (Emergency Removal)
    wa_rcw_13_34_050 = LegalDocument(
        document_id="WA-RCW-13.34.050",
        source_id="WA_RCW",
        jurisdiction="US-WA",
        level="state",
        document_type="statute",
        title="Court order to take child into custody",
        citation="RCW 13.34.050",
        full_text=(
            "The court may enter an order directing a law enforcement officer, probation counselor, or child protective services "
            "caseworker to take a child into custody if: (1) A petition is filed with the court alleging that the child is dependent; "
            "(2) The court finds probable cause to believe that: (a) The child is dependent; and (b) The child's health, safety, and welfare "
            "will be seriously endangered if not taken into custody. The petition must contain a statement of the facts supporting the request."
        ),
        temporal=TemporalMetadata(effective_date=date(2021, 7, 1), is_current=True),
        authority=AuthorityScore(tier="TIER_0", weight=1.0, official_source=True, provider_name="Washington State Legislature"),
        source_url="https://app.leg.wa.gov/rcw/default.aspx?cite=13.34.050",
        cps_topics=["emergency_removal", "dependency_petition", "probable_cause"]
    )
    wa_rcw_13_34_050.chunks = StatuteChunker.chunk_statute(
        wa_rcw_13_34_050.document_id,
        "RCW 13.34.050: Court order to take child into custody",
        wa_rcw_13_34_050.full_text
    )
    wa_rcw_13_34_050.compute_hash()
    docs.append(wa_rcw_13_34_050)

    # 2. WA RCW 13.34.065 (Shelter Care Hearing - 72 Hours)
    wa_rcw_13_34_065 = LegalDocument(
        document_id="WA-RCW-13.34.065",
        source_id="WA_RCW",
        jurisdiction="US-WA",
        level="state",
        document_type="statute",
        title="Shelter care — Hearing — Recommendation as to further custody — Release",
        citation="RCW 13.34.065",
        full_text=(
            "(1)(a) When a child is taken custody, the court shall hold a shelter care hearing within seventy-two hours, excluding Saturdays, Sundays, "
            "and legal holidays. The primary purpose of the shelter care hearing is to determine whether the child can be immediately and safely returned "
            "home while the adjudication of the dependency is pending. (b) If a parent or guardian is not given notice of the shelter care hearing, the "
            "parent may file an affidavit establishing that fact and the court shall hold a rehearing within seventy-two hours."
        ),
        temporal=TemporalMetadata(effective_date=date(2021, 7, 1), is_current=True),
        authority=AuthorityScore(tier="TIER_0", weight=1.0, official_source=True, provider_name="Washington State Legislature"),
        source_url="https://app.leg.wa.gov/rcw/default.aspx?cite=13.34.065",
        cps_topics=["shelter_care_hearing", "72_hour_notice", "release"]
    )
    wa_rcw_13_34_065.chunks = StatuteChunker.chunk_statute(
        wa_rcw_13_34_065.document_id,
        "RCW 13.34.065: Shelter care hearing",
        wa_rcw_13_34_065.full_text
    )
    wa_rcw_13_34_065.compute_hash()
    docs.append(wa_rcw_13_34_065)

    # 3. IL 705 ILCS 405/2-10 (Illinois Temporary Custody Hearing - 48 Hours)
    il_705_ilcs_405_2_10 = LegalDocument(
        document_id="IL-ILCS-705-405-2-10",
        source_id="IL_ILCS",
        jurisdiction="US-IL",
        level="state",
        document_type="statute",
        title="Temporary custody hearing",
        citation="705 ILCS 405/2-10",
        full_text=(
            "At the appearance of the minor before the court at the temporary custody hearing, which shall be held within 48 hours after the minor "
            "is taken into temporary custody, excluding Saturdays, Sundays, and court designated holidays: (1) The court shall examine the minor, "
            "his parents, guardian, or other persons having physical custody. (2) If the court finds probable cause to believe that the minor is "
            "abused, neglected or dependent, and that there is urgent and immediate necessity for temporary custody, the court may enter an order."
        ),
        temporal=TemporalMetadata(effective_date=date(2022, 1, 1), is_current=True),
        authority=AuthorityScore(tier="TIER_0", weight=1.0, official_source=True, provider_name="Illinois General Assembly"),
        source_url="https://www.ilga.gov/legislation/ilcs/ilcs4.asp?DocName=070504050HArt.+II",
        cps_topics=["temporary_custody", "48_hour_hearing", "urgent_necessity"]
    )
    il_705_ilcs_405_2_10.chunks = StatuteChunker.chunk_statute(
        il_705_ilcs_405_2_10.document_id,
        "705 ILCS 405/2-10: Temporary custody hearing",
        il_705_ilcs_405_2_10.full_text
    )
    il_705_ilcs_405_2_10.compute_hash()
    docs.append(il_705_ilcs_405_2_10)

    # 4. OH ORC § 2151.314 (Ohio Shelter Care Hearing - 72 Hours)
    oh_orc_2151_314 = LegalDocument(
        document_id="OH-ORC-2151.314",
        source_id="OH_ORC",
        jurisdiction="US-OH",
        level="state",
        document_type="statute",
        title="Detention hearing; shelter care hearing",
        citation="ORC § 2151.314",
        full_text=(
            "When a child is taken into custody, the court shall hold a detention or shelter care hearing not later than seventy-two hours "
            "after the child is placed in shelter care or detention. The court shall determine whether there is probable cause to believe that "
            "the child is an abused, neglected, or dependent child and whether detention or shelter care is required."
        ),
        temporal=TemporalMetadata(effective_date=date(2025, 9, 30), is_current=True),
        authority=AuthorityScore(tier="TIER_0", weight=1.0, official_source=True, provider_name="Ohio General Assembly"),
        source_url="https://codes.ohio.gov/ohio-revised-code/section-2151.314",
        cps_topics=["shelter_care_hearing", "72_hour_hearing", "probable_cause"]
    )
    oh_orc_2151_314.chunks = StatuteChunker.chunk_statute(
        oh_orc_2151_314.document_id,
        "ORC § 2151.314: Detention / Shelter care hearing",
        oh_orc_2151_314.full_text
    )
    oh_orc_2151_314.compute_hash()
    docs.append(oh_orc_2151_314)

    # 5. CA WIC § 315 (California Detention Hearing - 48-72 Hours)
    ca_wic_315 = LegalDocument(
        document_id="CA-WIC-315",
        source_id="CA_CODES",
        jurisdiction="US-CA",
        level="state",
        document_type="statute",
        title="Detention hearing; setting; time limits",
        citation="Cal. Welf. & Inst. Code § 315",
        full_text=(
            "If a child has been taken into custody, the juvenile court shall hold a hearing (detention hearing) to determine whether the "
            "child shall be further detained. This hearing shall be set as soon as possible, but in no event later than the expiration of the "
            "next judicial day after a petition to declare the child a dependent has been filed. If the hearing is not commenced within that "
            "time, the child shall be released from custody."
        ),
        temporal=TemporalMetadata(effective_date=date(2020, 1, 1), is_current=True),
        authority=AuthorityScore(tier="TIER_0", weight=1.0, official_source=True, provider_name="California State Legislature"),
        source_url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=WIC&sectionNum=315",
        cps_topics=["detention_hearing", "time_limits", "release_mandate"]
    )
    ca_wic_315.chunks = StatuteChunker.chunk_statute(
        ca_wic_315.document_id,
        "Cal. Welf. & Inst. Code § 315: Detention hearing",
        ca_wic_315.full_text
    )
    ca_wic_315.compute_hash()
    docs.append(ca_wic_315)

    # 6. TX Family Code § 262.201 (Texas Full Adversary Hearing - 14 Days)
    tx_fam_262_201 = LegalDocument(
        document_id="TX-FAM-262-201",
        source_id="TX_FAMILY_CODE",
        jurisdiction="US-TX",
        level="state",
        document_type="statute",
        title="Full Adversary Hearing; Findings",
        citation="Tex. Fam. Code § 262.201",
        full_text=(
            "(a) Unless the child has already been returned to the parent, managing conservator, possessory conservator, guardian, caretaker, "
            "or custodian entitled to possession and the temporary order has been dissolved, a full adversary hearing shall be held not later than "
            "the 14th day after the date the child was taken into possession by the governmental entity. (g) In a suit filed under Section 262.101 "
            "or 262.105, at the conclusion of the full adversary hearing, the court shall order the return of the child unless the court finds "
            "sufficient evidence that continuing possession is necessary to prevent danger to physical health or safety."
        ),
        temporal=TemporalMetadata(effective_date=date(2021, 9, 1), is_current=True),
        authority=AuthorityScore(tier="TIER_0", weight=1.0, official_source=True, provider_name="Texas Legislature Online"),
        source_url="https://statutes.capitol.texas.gov/Docs/FA/htm/FA.262.htm#262.201",
        cps_topics=["full_adversary_hearing", "14_day_hearing", "return_mandate"]
    )
    tx_fam_262_201.chunks = StatuteChunker.chunk_statute(
        tx_fam_262_201.document_id,
        "Tex. Fam. Code § 262.201: Full Adversary Hearing",
        tx_fam_262_201.full_text
    )
    tx_fam_262_201.compute_hash()
    docs.append(tx_fam_262_201)

    # 7. NY Family Court Act § 1028 (New York Application to Return Child - 3 Court Days)
    ny_fca_1028 = LegalDocument(
        document_id="NY-FCA-1028",
        source_id="NY_FCA",
        jurisdiction="US-NY",
        level="state",
        document_type="statute",
        title="Application to return child temporarily removed",
        citation="N.Y. Fam. Ct. Act § 1028",
        full_text=(
            "(a) Upon the application of the parent or other person legally responsible for the care of a child who has been temporarily removed "
            "under this part, the court shall hold a hearing to determine whether the child should be returned. The hearing shall be held within "
            "three court days of the application and shall not be adjourned for more than three court days, except by consent of the parties. "
            "The court shall grant the application and return the child unless it finds that the return presents an imminent risk to the child's life or health."
        ),
        temporal=TemporalMetadata(effective_date=date(2020, 1, 1), is_current=True),
        authority=AuthorityScore(tier="TIER_0", weight=1.0, official_source=True, provider_name="New York State Senate"),
        source_url="https://www.nysenate.gov/legislation/laws/FCT/1028",
        cps_topics=["parent_application_return", "3_day_hearing", "imminent_risk_standard"]
    )
    ny_fca_1028.chunks = StatuteChunker.chunk_statute(
        ny_fca_1028.document_id,
        "N.Y. Fam. Ct. Act § 1028: Application to Return Child",
        ny_fca_1028.full_text
    )
    ny_fca_1028.compute_hash()
    docs.append(ny_fca_1028)

    # 8. Federal ICWA 25 U.S.C. § 1912 (Pending Court Proceedings)
    fed_icwa_1912 = LegalDocument(
        document_id="FED-USC-25-1912",
        source_id="FED_USCODE",
        jurisdiction="US",
        level="federal",
        document_type="statute",
        title="Pending court proceedings; notice; active efforts; standard of proof",
        citation="25 U.S.C. § 1912",
        full_text=(
            "(a) Notice: In any involuntary proceeding in a State court, where the court knows or has reason to know that an Indian child "
            "is involved, the party seeking foster care placement or termination of parental rights shall notify the parent or Indian custodian "
            "and the Indian child's tribe, by registered mail with return receipt requested. (d) Active efforts: Any party seeking foster care "
            "placement or termination of parental rights shall satisfy the court that active efforts have been made to provide remedial services "
            "and rehabilitative programs designed to prevent the breakup of the Indian family. (e) Foster care standard: Clear and convincing evidence "
            "including testimony of qualified expert witnesses. (f) Termination standard: Beyond a reasonable doubt."
        ),
        temporal=TemporalMetadata(effective_date=date(1978, 11, 8), is_current=True),
        authority=AuthorityScore(tier="TIER_0", weight=1.0, official_source=True, provider_name="United States Congress"),
        source_url="https://uscode.house.gov/view.xhtml?req=(title:25%20section:1912)",
        cps_topics=["icwa", "active_efforts", "tribal_notice", "qualified_expert_witness"]
    )
    fed_icwa_1912.chunks = StatuteChunker.chunk_statute(
        fed_icwa_1912.document_id,
        "25 U.S.C. § 1912: ICWA Pending Court Proceedings",
        fed_icwa_1912.full_text
    )
    fed_icwa_1912.compute_hash()
    docs.append(fed_icwa_1912)

    # 9. Federal Social Security Act Title IV-E 42 U.S.C. § 671 (Reasonable Efforts)
    fed_title_iv_e_671 = LegalDocument(
        document_id="FED-USC-42-671",
        source_id="FED_USCODE",
        jurisdiction="US",
        level="federal",
        document_type="statute",
        title="State plan for foster care and adoption assistance; reasonable efforts",
        citation="42 U.S.C. § 671",
        full_text=(
            "(a)(15) In order for a State to be eligible for payments under this part, it shall have a plan approved by the Secretary which "
            "provides that: (A) in each case, reasonable efforts shall be made to prevent or eliminate the need for removing the child from the child's home; "
            "and (B) to make it possible for a child to safely return home. (C) If continuation of reasonable efforts is determined to be inconsistent "
            "with the permanency plan for the child, reasonable efforts shall be made to place the child in a timely manner in accordance with the permanency plan."
        ),
        temporal=TemporalMetadata(effective_date=date(1980, 6, 17), is_current=True),
        authority=AuthorityScore(tier="TIER_0", weight=1.0, official_source=True, provider_name="United States Congress"),
        source_url="https://uscode.house.gov/view.xhtml?req=(title:42%20section:671)",
        cps_topics=["title_iv_e", "reasonable_efforts", "foster_care_plan", "permanency"]
    )
    fed_title_iv_e_671.chunks = StatuteChunker.chunk_statute(
        fed_title_iv_e_671.document_id,
        "42 U.S.C. § 671: Title IV-E Reasonable Efforts",
        fed_title_iv_e_671.full_text
    )
    fed_title_iv_e_671.compute_hash()
    docs.append(fed_title_iv_e_671)

    return docs


def seed_database(db_path: str = "legal_gpt.db") -> int:
    db = LegalDatabase(db_path=db_path)
    docs = build_seed_documents()
    for doc in docs:
        db.insert_document(doc)
    return len(docs)


if __name__ == "__main__":
    count = seed_database()
    print(f"Successfully seeded {count} foundational statutes into legal_gpt.db across WA, IL, OH, CA, TX, NY, and Federal law.")
