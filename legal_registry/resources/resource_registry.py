"""Canonical seed registry of authentic, verified public legal resources across 18 organization types."""

from datetime import date
from typing import Dict, List, Optional
from legal_registry.resources.resource_schema import (
    PublicLegalResource,
    OrganizationType,
    ResourceState,
    VerificationMethod,
)


SEED_RESOURCES: List[PublicLegalResource] = [
    # 1. LEGAL_AID (Washington)
    PublicLegalResource(
        resource_id="WA-RES-NJP-01",
        name="Northwest Justice Project (NJP)",
        organization_type=OrganizationType.LEGAL_AID,
        jurisdiction="US-WA",
        service_area=["Statewide", "Skagit County", "King County", "Pierce County", "Snohomish County", "Spokane County"],
        eligibility="Low-income individuals and families up to 200% of the federal poverty level facing civil legal problems.",
        services=["Civil Legal Aid", "Eviction Defense", "Family Law & Domestic Violence", "CPS / Dependency Representation", "Public Benefits"],
        website="https://nwjustice.org",
        phone="(888) 201-1014",
        address="401 2nd Ave S, Suite 407, Seattle, WA 98104",
        hours="Monday - Friday: 9:15 AM - 12:15 PM (CLEAR Intake)",
        languages=["English", "Spanish", "Russian", "Vietnamese", "Interpretation Available"],
        income_requirements="Under 200% Federal Poverty Guidelines",
        verification_source="Legal Services Corporation (LSC) Official Grantee Directory & Washington State Bar Association",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.LSC_GRANTEE_DATABASE,
        state=ResourceState.VERIFIED
    ),

    # 2. COURT_SELF_HELP (Washington)
    PublicLegalResource(
        resource_id="WA-RES-COURT-HELP-01",
        name="Washington Courts Public Self-Help & Court Facilitators",
        organization_type=OrganizationType.COURT_SELF_HELP,
        jurisdiction="US-WA",
        service_area=["Statewide"],
        eligibility="Open to all self-represented litigants in Washington Superior, District, and Municipal courts.",
        services=["Court Forms", "Filing Instructions", "Courthouse Facilitator Contacts", "Family Law Guidelines", "Fee Waiver Forms"],
        website="https://www.courts.wa.gov/forms/",
        phone="(360) 753-3360",
        address="Temple of Justice, 415 12th Ave SW, Olympia, WA 98501",
        hours="Monday - Friday: 8:00 AM - 5:00 PM PST",
        languages=["English", "Spanish", "Vietnamese", "Russian"],
        income_requirements="None (Public Court Service)",
        verification_source="Washington Administrative Office of the Courts (AOC)",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.OFFICIAL_GOVERNMENT_DIRECTORY,
        state=ResourceState.VERIFIED
    ),

    # 3. PUBLIC_DEFENDER (Washington)
    PublicLegalResource(
        resource_id="WA-RES-OPD-01",
        name="Washington State Office of Public Defense (OPD) - Parents Representation Program",
        organization_type=OrganizationType.PUBLIC_DEFENDER,
        jurisdiction="US-WA",
        service_area=["Statewide"],
        eligibility="Indigent parents and legal custodians facing dependency or termination of parental rights under RCW 13.34.",
        services=["Parent Defense in Dependency", "Appellate Indigent Defense", "Court-Appointed Representation Oversight"],
        website="https://www.opd.wa.gov",
        phone="(360) 586-3164",
        address="711 Capitol Way S, Suite 106, Olympia, WA 98501",
        hours="Monday - Friday: 8:00 AM - 5:00 PM PST",
        languages=["English", "Spanish"],
        income_requirements="Indigency verification per RCW 10.101",
        verification_source="Washington State Office of Public Defense Official Agency Registry",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.OFFICIAL_GOVERNMENT_DIRECTORY,
        state=ResourceState.VERIFIED
    ),

    # 4. BAR_REFERRAL (Washington)
    PublicLegalResource(
        resource_id="WA-RES-WSBA-MODERATE-01",
        name="Washington State Bar Association - Moderate Means Program",
        organization_type=OrganizationType.BAR_REFERRAL,
        jurisdiction="US-WA",
        service_area=["Statewide"],
        eligibility="Washington residents with income between 200% and 400% of the federal poverty level who do not qualify for free legal aid.",
        services=["Reduced-Fee Legal Referrals", "Family Law Referrals", "Housing Law Referrals", "Consumer Law Referrals"],
        website="https://www.wsba.org/for-the-public/find-legal-help",
        phone="(855) 741-6930",
        address="1325 4th Ave, Suite 600, Seattle, WA 98101",
        hours="Monday - Friday: 8:00 AM - 5:00 PM PST",
        languages=["English", "Spanish"],
        income_requirements="200% - 400% of Federal Poverty Level",
        verification_source="Washington State Bar Association Official Roster",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.BAR_ASSOCIATION_ROSTER,
        state=ResourceState.VERIFIED
    ),

    # 5. CIVIL_RIGHTS_ORGANIZATIONS (Washington & National)
    PublicLegalResource(
        resource_id="WA-RES-ACLU-01",
        name="American Civil Liberties Union (ACLU) of Washington",
        organization_type=OrganizationType.CIVIL_RIGHTS_ORGANIZATIONS,
        jurisdiction="US-WA",
        service_area=["Statewide"],
        eligibility="Open to members of the public alleging unconstitutional government actions, systemic civil rights violations, or civil liberties infringements.",
        services=["Constitutional Impact Litigation", "Legal Intakes for Government Abuse", "Civil Liberties Public Education"],
        website="https://www.aclu-wa.org",
        phone="(206) 624-2184",
        address="PO Box 2728, Seattle, WA 98111",
        hours="Monday - Friday: 9:00 AM - 5:00 PM PST",
        languages=["English", "Spanish"],
        income_requirements="None",
        verification_source="ACLU Official Affiliate Registry",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.MANUAL_STAFF_AUDIT,
        state=ResourceState.VERIFIED
    ),

    # 6. CHILD_ADVOCACY (National)
    PublicLegalResource(
        resource_id="NAT-RES-NACC-01",
        name="National Association of Counsel for Children (NACC)",
        organization_type=OrganizationType.CHILD_ADVOCACY,
        jurisdiction="US",
        service_area=["National", "Statewide"],
        eligibility="Children, youth, parents, and attorneys involved in child welfare, dependency, and court proceedings.",
        services=["Child Welfare Legal Standards", "Youth Representation Directory", "Child Advocacy Best Practice Resources"],
        website="https://www.naccchild.org",
        phone="(888) 828-6222",
        address="1600 Downing St, Suite 410, Denver, CO 80218",
        hours="Monday - Friday: 9:00 AM - 5:00 PM MST",
        languages=["English"],
        income_requirements="None",
        verification_source="U.S. Children's Bureau Directory of Child Welfare Organizations",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.OFFICIAL_GOVERNMENT_DIRECTORY,
        state=ResourceState.VERIFIED
    ),

    # 7. DOMESTIC_VIOLENCE_SERVICES (National & Federal)
    PublicLegalResource(
        resource_id="FED-RES-NDVH-01",
        name="National Domestic Violence Hotline",
        organization_type=OrganizationType.DOMESTIC_VIOLENCE_SERVICES,
        jurisdiction="US",
        service_area=["National"],
        eligibility="Confidential 24/7 crisis intervention, safety planning, and local referral for anyone affected by domestic violence.",
        services=["Crisis Intervention", "Safety Planning", "Local Emergency Shelter Referral", "Legal Protective Order Information"],
        website="https://www.thehotline.org",
        phone="(800) 799-7233",
        address="PO Box 90249, Austin, TX 78709",
        hours="24 Hours / 7 Days a Week",
        languages=["English", "Spanish", "Over 200 languages via Tele-interpreter"],
        income_requirements="None",
        verification_source="U.S. Department of Health and Human Services (HHS) Family Violence Prevention and Services Act (FVPSA) Directory",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.OFFICIAL_GOVERNMENT_DIRECTORY,
        state=ResourceState.VERIFIED
    ),

    # 8. DISABILITY_SERVICES (Washington)
    PublicLegalResource(
        resource_id="WA-RES-DRW-01",
        name="Disability Rights Washington (DRW)",
        organization_type=OrganizationType.DISABILITY_SERVICES,
        jurisdiction="US-WA",
        service_area=["Statewide"],
        eligibility="Individuals with physical, psychiatric, sensory, or developmental disabilities residing in Washington State.",
        services=["Protection & Advocacy (P&A)", "ADA Title II Enforcement in State Agencies", "Disability Accommodation Advocacy", "Abuse/Neglect Investigations in Facilities"],
        website="https://www.disabilityrightswa.org",
        phone="(800) 562-2702",
        address="315 5th Ave S, Suite 850, Seattle, WA 98104",
        hours="Monday - Friday: 9:00 AM - 4:00 PM PST",
        languages=["English", "Spanish", "ASL Available"],
        income_requirements="None (Federally Mandated P&A System)",
        verification_source="Substance Abuse and Mental Health Services Administration (SAMHSA) & Administration for Community Living (ACL) P&A Directory",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.OFFICIAL_GOVERNMENT_DIRECTORY,
        state=ResourceState.VERIFIED
    ),

    # 9. MENTAL_HEALTH_SERVICES (Federal)
    PublicLegalResource(
        resource_id="FED-RES-SAMHSA-01",
        name="SAMHSA National Helpline",
        organization_type=OrganizationType.MENTAL_HEALTH_SERVICES,
        jurisdiction="US",
        service_area=["National"],
        eligibility="Free, confidential, 24/7, 365-day-a-year treatment referral and information service for individuals facing mental health or substance use disorders.",
        services=["Mental Health Referral", "Facility Locator", "Support Group Connections", "Family Counseling Referrals"],
        website="https://www.samhsa.gov/find-help/national-helpline",
        phone="(800) 662-4357",
        address="5600 Fishers Lane, Rockville, MD 20857",
        hours="24 Hours / 7 Days a Week",
        languages=["English", "Spanish"],
        income_requirements="None",
        verification_source="Substance Abuse and Mental Health Services Administration (SAMHSA) Official Portal",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.OFFICIAL_GOVERNMENT_DIRECTORY,
        state=ResourceState.VERIFIED
    ),

    # 10. SUBSTANCE_USE_SERVICES (Washington)
    PublicLegalResource(
        resource_id="WA-RES-WRHL-01",
        name="Washington Recovery Help Line",
        organization_type=OrganizationType.SUBSTANCE_USE_SERVICES,
        jurisdiction="US-WA",
        service_area=["Statewide"],
        eligibility="Washington State residents seeking support and treatment options for substance use, problem gambling, and mental health.",
        services=["Substance Use Treatment Referrals", "Detox Facility Locator", "Overdose Prevention Information", "Peer Support"],
        website="https://www.warecoveryhelpline.org",
        phone="(866) 789-1511",
        address="PO Box 357131, Seattle, WA 98195",
        hours="24 Hours / 7 Days a Week",
        languages=["English", "Spanish", "Interpretation Services"],
        income_requirements="None",
        verification_source="Washington State Health Care Authority (HCA)",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.OFFICIAL_GOVERNMENT_DIRECTORY,
        state=ResourceState.VERIFIED
    ),

    # 11. HOUSING_SERVICES (Washington)
    PublicLegalResource(
        resource_id="WA-RES-TENANTS-UNION-01",
        name="Tenants Union of Washington State",
        organization_type=OrganizationType.HOUSING_SERVICES,
        jurisdiction="US-WA",
        service_area=["Statewide", "King County", "Pierce County", "Snohomish County", "Skagit County"],
        eligibility="All residential tenants in Washington State facing eviction, rent increases, substandard housing conditions, or landlord disputes.",
        services=["Tenant Rights Hotline", "Eviction Defense Education", "Habitability Advocacy", "Fair Housing Information"],
        website="https://tenantsunion.org",
        phone="(206) 723-0500",
        address="5425 Rainier Ave S, Suite B, Seattle, WA 98118",
        hours="Monday, Tuesday, Thursday: 10:00 AM - 1:00 PM PST",
        languages=["English", "Spanish", "Somali"],
        income_requirements="None (Prioritizes low-income and working-class tenants)",
        verification_source="Washington State Department of Commerce Housing Directory",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.OFFICIAL_GOVERNMENT_DIRECTORY,
        state=ResourceState.VERIFIED
    ),

    # 12. EDUCATION_ADVOCACY (Washington)
    PublicLegalResource(
        resource_id="WA-RES-OEO-01",
        name="Washington State Governor's Office of the Education Ombuds (OEO)",
        organization_type=OrganizationType.EDUCATION_ADVOCACY,
        jurisdiction="US-WA",
        service_area=["Statewide"],
        eligibility="Any family, student, or educator dealing with a conflict in Washington K-12 public schools.",
        services=["Special Education (IEP/504) Advocacy", "School Discipline & Suspension Review", "Bullying & Harassment Resolution", "School Access Guidance"],
        website="https://www.oeo.wa.gov",
        phone="(866) 297-2597",
        address="3518 Fremont Ave N, Suite 349, Seattle, WA 98103",
        hours="Monday - Friday: 8:00 AM - 5:00 PM PST",
        languages=["English", "Spanish", "Over 100 languages via tele-interpreter"],
        income_requirements="None (Free Public Ombuds Office)",
        verification_source="State of Washington Governor's Executive Roster",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.OFFICIAL_GOVERNMENT_DIRECTORY,
        state=ResourceState.VERIFIED
    ),

    # 13. VETERANS_SERVICES (National)
    PublicLegalResource(
        resource_id="FED-RES-NVLSP-01",
        name="National Veterans Legal Services Program (NVLSP)",
        organization_type=OrganizationType.VETERANS_SERVICES,
        jurisdiction="US",
        service_area=["National"],
        eligibility="Active duty service members, veterans, and military families seeking VA disability benefits or discharge upgrades.",
        services=["VA Disability Benefits Appeals", "Discharge Upgrades", "Military Records Correction", "Free Legal Representation"],
        website="https://www.nvlsp.org",
        phone="(202) 265-8305",
        address="PO Box 449, Arlington, VA 22216",
        hours="Monday - Friday: 9:00 AM - 5:00 PM EST",
        languages=["English"],
        income_requirements="None (Free for qualifying veterans)",
        verification_source="U.S. Department of Veterans Affairs (VA) Recognized VSO Roster",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.OFFICIAL_GOVERNMENT_DIRECTORY,
        state=ResourceState.VERIFIED
    ),

    # 14. TRIBAL_SERVICES (Washington / Tribal)
    PublicLegalResource(
        resource_id="WA-RES-PUYALLUP-ICWA-01",
        name="Puyallup Tribe of Indians - Children's Services & Tribal Court",
        organization_type=OrganizationType.TRIBAL_SERVICES,
        jurisdiction="US-WA",
        service_area=["Puyallup Reservation", "Pierce County", "King County", "Statewide (ICWA cases)"],
        eligibility="Enrolled members of the Puyallup Tribe or children eligible for tribal membership involved in child welfare or custody proceedings.",
        services=["ICWA Legal Representation", "Tribal Child Welfare Advocacy", "Kinship Support", "Tribal Court Services"],
        website="https://www.puyalluptribe-nsn.gov",
        phone="(253) 680-5520",
        address="3009 E Portland Ave, Tacoma, WA 98404",
        hours="Monday - Friday: 8:00 AM - 5:00 PM PST",
        languages=["English", "Lushootseed"],
        income_requirements="None (Tribal Citizenship / ICWA Eligibility)",
        verification_source="Bureau of Indian Affairs (BIA) Designated Tribal ICWA Agent Registry (Federal Register)",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.OFFICIAL_GOVERNMENT_DIRECTORY,
        state=ResourceState.VERIFIED
    ),

    # 15. IMMIGRATION_SERVICES (Washington)
    PublicLegalResource(
        resource_id="WA-RES-NWIRP-01",
        name="Northwest Immigrant Rights Project (NWIRP)",
        organization_type=OrganizationType.IMMIGRATION_SERVICES,
        jurisdiction="US-WA",
        service_area=["Statewide"],
        eligibility="Low-income immigrant community members in Washington State facing immigration proceedings, deportation, or seeking legal status.",
        services=["Deportation Defense", "Asylum Claims", "VAWA & U-Visa Petitions for Crime Victims", "Family-Based Immigration"],
        website="https://www.nwirp.org",
        phone="(206) 587-4009",
        address="615 2nd Ave, Suite 400, Seattle, WA 98104",
        hours="Monday - Friday: 9:00 AM - 4:30 PM PST",
        languages=["English", "Spanish", "Somali", "Arabic", "Vietnamese"],
        income_requirements="Low-income (under 200% FPL)",
        verification_source="Executive Office for Immigration Review (EOIR) Recognized Organizations Roster (U.S. DOJ)",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.OFFICIAL_GOVERNMENT_DIRECTORY,
        state=ResourceState.VERIFIED
    ),

    # 16. MEDIATION (Washington)
    PublicLegalResource(
        resource_id="WA-RES-DRC-KING-01",
        name="Dispute Resolution Center of King County",
        organization_type=OrganizationType.MEDIATION,
        jurisdiction="US-WA",
        service_area=["King County", "Skagit County (cross-referral)", "Statewide"],
        eligibility="Parties seeking community, family, parenting plan, or landlord-tenant dispute resolution outside of formal court litigation.",
        services=["Parenting Plan Mediation", "Landlord-Tenant Eviction Resolution", "Community Mediation", "Small Claims Conciliation"],
        website="https://kcdrc.org",
        phone="(206) 443-9603",
        address="4649 Sunnyside Ave N, Suite 520, Seattle, WA 98103",
        hours="Monday - Friday: 9:00 AM - 4:30 PM PST",
        languages=["English", "Spanish", "Interpretation on request"],
        income_requirements="Sliding scale based on household income; no one turned away for inability to pay",
        verification_source="Washington Resolution Washington (State Association of DRCs per RCW 7.75)",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.OFFICIAL_GOVERNMENT_DIRECTORY,
        state=ResourceState.VERIFIED
    ),

    # 17. OMBUDS (Washington)
    PublicLegalResource(
        resource_id="WA-RES-OFCO-01",
        name="Washington State Office of the Family and Children's Ombuds (OFCO)",
        organization_type=OrganizationType.OMBUDS,
        jurisdiction="US-WA",
        service_area=["Statewide"],
        eligibility="Any parent, foster parent, child, or community member with a complaint regarding DCYF child welfare or juvenile rehabilitation actions.",
        services=["Independent Investigation of Child Welfare Complaints", "Systemic Policy Monitoring", "Parent Rights Assistance in CPS Cases"],
        website="https://ofco.wa.gov",
        phone="(800) 571-7321",
        address="6720 Fort Dent Way, Suite 240, Tukwila, WA 98188",
        hours="Monday - Friday: 8:00 AM - 5:00 PM PST",
        languages=["English", "Spanish", "Interpretation available"],
        income_requirements="None (Independent State Government Agency per RCW 43.06A)",
        verification_source="Washington State Legislative & Executive Directory",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.OFFICIAL_GOVERNMENT_DIRECTORY,
        state=ResourceState.VERIFIED
    ),

    # 18. GOVERNMENT_AGENCIES (Federal & Washington)
    PublicLegalResource(
        resource_id="FED-RES-ACF-01",
        name="U.S. Department of Health and Human Services - Administration for Children and Families (ACF) Children's Bureau",
        organization_type=OrganizationType.GOVERNMENT_AGENCIES,
        jurisdiction="US",
        service_area=["National"],
        eligibility="Federal administration responsible for Title IV-E foster care, child abuse prevention (CAPTA), and federal child welfare oversight.",
        services=["Federal Child Welfare Regulations", "Child Welfare Information Gateway", "Title IV-E State Compliance Monitoring"],
        website="https://www.acf.hhs.gov/cb",
        phone="(800) 394-3366",
        address="330 C St SW, Washington, DC 20201",
        hours="Monday - Friday: 8:00 AM - 5:00 PM EST",
        languages=["English", "Spanish"],
        income_requirements="None (Federal Government Agency)",
        verification_source="United States Government Manual (Official Federal Directory)",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.OFFICIAL_GOVERNMENT_DIRECTORY,
        state=ResourceState.VERIFIED
    ),

    # 19. LEGAL_AID (Illinois)
    PublicLegalResource(
        resource_id="IL-RES-LAC-01",
        name="Legal Aid Chicago",
        organization_type=OrganizationType.LEGAL_AID,
        jurisdiction="US-IL",
        service_area=["Cook County", "Chicago"],
        eligibility="Low-income Cook County residents facing civil legal challenges in housing, family, safety, and benefits.",
        services=["Eviction Defense", "CPS / Dependency Representation", "Domestic Violence Orders of Protection", "Public Benefits Assistance"],
        website="https://www.legalaidchicago.org",
        phone="(312) 341-1070",
        address="120 S LaSalle St, Suite 900, Chicago, IL 60603",
        hours="Monday - Friday: 8:30 AM - 4:00 PM CST",
        languages=["English", "Spanish"],
        income_requirements="Under 150% - 200% Federal Poverty Level",
        verification_source="Legal Services Corporation (LSC) Official Directory",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.LSC_GRANTEE_DATABASE,
        state=ResourceState.VERIFIED
    ),

    # 20. PUBLIC_DEFENDER (Illinois)
    PublicLegalResource(
        resource_id="IL-RES-COOK-PD-01",
        name="Law Office of the Cook County Public Defender - Juvenile Protection Division",
        organization_type=OrganizationType.PUBLIC_DEFENDER,
        jurisdiction="US-IL",
        service_area=["Cook County"],
        eligibility="Indigent parents and legal custodians facing child abuse, neglect, or dependency proceedings in Cook County Juvenile Court.",
        services=["Parent Representation in Abuse/Neglect Cases", "Temporary Custody Hearing Defense", "Appellate Representation"],
        website="https://www.cookcountyil.gov/agency/public-defender",
        phone="(312) 433-7000",
        address="1100 S Hamilton Ave, Chicago, IL 60612",
        hours="Monday - Friday: 8:30 AM - 4:30 PM CST",
        languages=["English", "Spanish"],
        income_requirements="Court-determined indigency under 705 ILCS 405/1-5",
        verification_source="Cook County Official Government Directory",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.OFFICIAL_GOVERNMENT_DIRECTORY,
        state=ResourceState.VERIFIED
    ),

    # 21. LEGAL_AID (Ohio)
    PublicLegalResource(
        resource_id="OH-RES-LASC-01",
        name="Legal Aid Society of Cleveland",
        organization_type=OrganizationType.LEGAL_AID,
        jurisdiction="US-OH",
        service_area=["Cuyahoga County", "Ashtabula County", "Geauga County", "Lake County", "Lorain County"],
        eligibility="Low-income residents in Northeast Ohio with civil legal issues.",
        services=["Eviction Prevention", "Family Law & Domestic Violence", "Juvenile Custody Defense", "Consumer Debt Defense"],
        website="https://lasclev.org",
        phone="(888) 817-3777",
        address="1223 W 6th St, Cleveland, OH 44113",
        hours="Monday, Wednesday, Friday: 9:00 AM - 4:00 PM EST",
        languages=["English", "Spanish", "Arabic"],
        income_requirements="Under 200% Federal Poverty Guidelines",
        verification_source="Legal Services Corporation (LSC) Official Grantee Database",
        last_verified=date(2024, 8, 1),
        verification_method=VerificationMethod.LSC_GRANTEE_DATABASE,
        state=ResourceState.VERIFIED
    )
]


class ResourceRegistry:
    """Provides indexed query and retrieval for public legal resources."""

    _RESOURCES_BY_ID: Dict[str, PublicLegalResource] = {r.resource_id: r for r in SEED_RESOURCES}

    @classmethod
    def get_all(cls) -> List[PublicLegalResource]:
        """Returns all registered resources."""
        return list(cls._RESOURCES_BY_ID.values())

    @classmethod
    def get_by_id(cls, resource_id: str) -> Optional[PublicLegalResource]:
        """Returns a single resource by unique identifier."""
        return cls._RESOURCES_BY_ID.get(resource_id)

    @classmethod
    def get_by_type(cls, org_type: OrganizationType) -> List[PublicLegalResource]:
        """Returns resources matching an organization type."""
        return [r for r in cls._RESOURCES_BY_ID.values() if r.organization_type == org_type]

    @classmethod
    def get_by_jurisdiction(cls, jurisdiction: str) -> List[PublicLegalResource]:
        """Returns resources matching target jurisdiction or federal/national scope."""
        norm_j = jurisdiction.upper()
        if not norm_j.startswith("US-") and norm_j != "US":
            norm_j = f"US-{norm_j}"
        return [r for r in cls._RESOURCES_BY_ID.values() if r.jurisdiction in ("US", norm_j)]
