"""Multi-State Motion and Court Pleading Template Generator."""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class PleadingDraftRequest(BaseModel):
    state: str = Field(..., description="2-letter state code e.g. WA, IL, OH, CA, TX, NY or ICWA")
    motion_type: str = Field("shelter_rehearing", description="Motion type: shelter_rehearing, return_child, section_1028, icwa_intervention, section_388")
    county: str = Field("District 1", description="County or Judicial District")
    court_name: Optional[str] = None
    case_number: str = Field("[CAUSE_NO_REDACTED]", description="Court Docket / Cause Number")
    parent_name: str = Field("[RESPONDENT_PARENT]", description="Parent identifier placeholder")
    child_name: str = Field("[CHILD_INITIALS]", description="Child identifier placeholder")
    caseworker_agency: Optional[str] = None
    factual_basis: str = Field("Statutory notice and evidentiary threshold grounds under governing juvenile court rules.", description="Summary of facts")
    proposed_relative_placement: Optional[str] = "[PROPOSED_KINSHIP_PLACEMENT]"


class PleadingDraftResponse(BaseModel):
    title: str
    jurisdiction: str
    governing_rule_and_statute: str
    caption: str
    body_markdown: str
    certificate_of_service: str


class PleadingGenerator:
    """Generates formal, state-specific child welfare court motion drafts."""

    @classmethod
    def generate_pleading(cls, req: PleadingDraftRequest) -> PleadingDraftResponse:
        st = req.state.upper().strip()
        m_type = req.motion_type.lower().strip()

        if st == "WA" or "shelter_rehearing" in m_type:
            return cls._generate_wa_shelter_rehearing(req)
        elif st == "IL":
            return cls._generate_il_temporary_custody_rehearing(req)
        elif st == "OH":
            return cls._generate_oh_shelter_modification(req)
        elif st == "CA":
            return cls._generate_ca_section_388_petition(req)
        elif st == "TX":
            return cls._generate_tx_adversary_motion(req)
        elif st == "NY" or "1028" in m_type:
            return cls._generate_ny_1028_application(req)
        elif st == "ICWA" or "icwa" in m_type:
            return cls._generate_icwa_intervention(req)
        else:
            return cls._generate_wa_shelter_rehearing(req)

    @classmethod
    def _generate_wa_shelter_rehearing(cls, req: PleadingDraftRequest) -> PleadingDraftResponse:
        title = "MOTION AND AFFIDAVIT FOR REHEARING OF SHELTER CARE ORDER & IMMEDIATE RELEASE"
        governing = "JuCR 2.4 & RCW 13.34.065"
        court = req.court_name or f"SUPERIOR COURT OF WASHINGTON FOR {req.county.upper()} (JUVENILE DIVISION)"

        caption = (
            f"IN THE {court}\n"
            f"In re the Dependency of:\t\tCause No.: {req.case_number}\n"
            f"{req.child_name}, D.O.B. [REDACTED],\t\tMOTION AND AFFIDAVIT FOR REHEARING\n"
            f"A Person Under 18 Years of Age.\t\tOF SHELTER CARE ORDER (RCW 13.34.065)"
        )

        body = (
            f"# {title}\n\n"
            f"**TO**: The Clerk of the Court, DCYF Assistant Attorney General, and Attorney for the Child / CASA.\n\n"
            f"## I. RELIEF REQUESTED\n"
            f"COMES NOW {req.parent_name}, by and through counsel of record, and respectfully moves this Court pursuant to "
            f"**RCW 13.34.065(1)(b)** and **JuCR 2.4** for an immediate order scheduling a Rehearing on the Shelter Care Order "
            f"within seventy-two (72) hours, and releasing the child {req.child_name} to parental custody with an agreed in-home safety plan, "
            f"or in the alternative, placing the child with an approved relative ({req.proposed_relative_placement}).\n\n"
            f"## II. STATEMENT OF FACTS\n"
            f"1. On or about [DATE], the Department of Children, Youth, and Families (DCYF) took physical custody of the child.\n"
            f"2. {req.factual_basis}\n"
            f"3. A viable relative placement ({req.proposed_relative_placement}) is willing, able, and available to provide care.\n\n"
            f"## III. LEGAL ARGUMENT & AUTHORITIES\n"
            f"1. **Mandatory Rehearing Right**: Under **RCW 13.34.065(1)(b)**, if a parent did not have actual notice of the shelter care hearing, "
            f"or presents evidence of changed circumstances, the court *shall* hold a rehearing within 72 hours of filing the affidavit.\n"
            f"2. **Strict Removal Standards**: Under **In re Dependency of K.N.J., 171 Wn.2d 568 (2011)** and **Troxel v. Granville, 530 U.S. 57 (2000)**, "
            f"parents possess a fundamental Fourteenth Amendment liberty interest in the care and custody of their children. "
            f"Continued out-of-home shelter care requires proof by a preponderance of the evidence that reasonable efforts cannot prevent removal.\n\n"
            f"## IV. PRAYER FOR RELIEF\n"
            f"WHEREFORE, Respondent Parent requests that this Court:\n"
            f"1. Schedule an expedited Rehearing within 72 hours of filing;\n"
            f"2. Vacate the temporary out-of-home placement and return the child to the parent; and\n"
            f"3. Grant such other relief as is just and equitable."
        )

        cert = (
            f"CERTIFICATE OF SERVICE\n"
            f"I certify under penalty of perjury under the laws of the State of Washington that on this date, "
            f"I served a copy of this Motion upon the DCYF AAG and Child's Attorney via electronic filing and delivery."
        )

        return PleadingDraftResponse(
            title=title,
            jurisdiction=f"US-WA ({req.county})",
            governing_rule_and_statute=governing,
            caption=caption,
            body_markdown=body,
            certificate_of_service=cert
        )

    @classmethod
    def _generate_ny_1028_application(cls, req: PleadingDraftRequest) -> PleadingDraftResponse:
        title = "APPLICATION FOR RETURN OF CHILD TEMPORARILY REMOVED (FCA § 1028)"
        governing = "N.Y. Fam. Ct. Act § 1028 & 22 NYCRR Part 205"
        court = req.court_name or f"FAMILY COURT OF THE STATE OF NEW YORK: {req.county.upper()}"

        caption = (
            f"{court}\n"
            f"In the Matter of\t\t\tDocket No.: {req.case_number}\n"
            f"{req.child_name},\t\t\tSECTION 1028 APPLICATION FOR\n"
            f"A Child under 18 Years Alleged to be Neglected.\tRETURN OF TEMPORARILY REMOVED CHILD"
        )

        body = (
            f"# {title}\n\n"
            f"## I. APPLICATION\n"
            f"Respondent Parent {req.parent_name} hereby makes application pursuant to **N.Y. Family Court Act § 1028** for the immediate return of "
            f"the child {req.child_name}, temporarily removed from parental custody by the local Department of Social Services.\n\n"
            f"## II. STATUTORY MANDATE FOR EXPEDITED HEARING\n"
            f"Pursuant to **FCA § 1028**, the Family Court **MUST hold a hearing within three (3) court days** of this application, and "
            f"cannot adjourn the hearing except upon consent or for good cause shown.\n\n"
            f"## III. LEGAL STANDARD\n"
            f"Under the landmark decision of the Court of Appeals in **Nicholson v. Scoppetta, 3 N.Y.3d 357 (2004)**, the Court *shall* grant "
            f"the application and return the child unless the agency proves by a preponderance of the evidence that return presents an "
            f"**imminent risk to the child's life or health** that cannot be mitigated by reasonable remedial efforts or services.\n\n"
            f"## IV. FACTUAL SUPPORT\n"
            f"{req.factual_basis}"
        )

        cert = (
            f"I hereby certify that on this date, a copy of this § 1028 Application was served on the County Attorney / ACS "
            f"and the Attorney for the Child."
        )

        return PleadingDraftResponse(
            title=title,
            jurisdiction=f"US-NY ({req.county})",
            governing_rule_and_statute=governing,
            caption=caption,
            body_markdown=body,
            certificate_of_service=cert
        )

    @classmethod
    def _generate_il_temporary_custody_rehearing(cls, req: PleadingDraftRequest) -> PleadingDraftResponse:
        title = "MOTION FOR REHEARING ON TEMPORARY CUSTODY (705 ILCS 405/2-10)"
        governing = "705 ILCS 405/2-10(b) & Ill. S. Ct. Rule Part F"
        court = req.court_name or f"IN THE CIRCUIT COURT OF {req.county.upper()}, ILLINOIS (CHILD PROTECTION DIVISION)"

        caption = f"{court}\nIn the Interest of {req.child_name}\tCause No.: {req.case_number}\nMOTION FOR REHEARING"
        body = (
            f"# {title}\n\n"
            f"Respondent Parent {req.parent_name} moves under **705 ILCS 405/2-10(b)** for a rehearing on temporary custody within 14 days, "
            f"establishing lack of personal service and presenting verified proof that urgent necessity no longer exists."
        )
        cert = "Certificate of service on State's Attorney and Public Guardian."

        return PleadingDraftResponse(
            title=title,
            jurisdiction=f"US-IL ({req.county})",
            governing_rule_and_statute=governing,
            caption=caption,
            body_markdown=body,
            certificate_of_service=cert
        )

    @classmethod
    def _generate_ca_section_388_petition(cls, req: PleadingDraftRequest) -> PleadingDraftResponse:
        title = "PETITION FOR MODIFICATION / CHANGE OF CIRCUMSTANCES (WIC § 388)"
        governing = "Cal. Welf. & Inst. Code § 388 & CRC Rule 5.570"
        court = req.court_name or f"SUPERIOR COURT OF CALIFORNIA, {req.county.upper()} (JUVENILE DIVISION)"
        caption = f"{court}\nIn re {req.child_name}, a Person Coming Under the Juvenile Court Law\tCase No.: {req.case_number}"
        body = (
            f"# {title}\n\n"
            f"Parent petitions pursuant to **WIC § 388** establishing changed circumstances and demonstrating that modification "
            f"of prior detention or placement order is in the child's best interest (**In re Marilyn H., 5 Cal. 4th 295**)."
        )
        cert = "Proof of service on County Counsel and Minor's Counsel."
        return PleadingDraftResponse(
            title=title,
            jurisdiction=f"US-CA ({req.county})",
            governing_rule_and_statute=governing,
            caption=caption,
            body_markdown=body,
            certificate_of_service=cert
        )

    @classmethod
    def _generate_tx_adversary_motion(cls, req: PleadingDraftRequest) -> PleadingDraftResponse:
        title = "MOTION TO CONTEST ADVERSARY HEARING & DEMAND FOR IMMEDIATE RETURN"
        governing = "Tex. Fam. Code § 262.201"
        court = req.court_name or f"IN THE DISTRICT COURT OF {req.county.upper()}, TEXAS"
        caption = f"{court}\nIN THE INTEREST OF {req.child_name}, A CHILD\tCAUSE NO.: {req.case_number}"
        body = (
            f"# {title}\n\n"
            f"Parent contests the 14-day Full Adversary Hearing under **Tex. Fam. Code § 262.201** and demands immediate return "
            f"of the child on grounds that DFPS cannot satisfy the burden of continuing danger."
        )
        cert = "Certificate of service on DFPS Attorney."
        return PleadingDraftResponse(
            title=title,
            jurisdiction=f"US-TX ({req.county})",
            governing_rule_and_statute=governing,
            caption=caption,
            body_markdown=body,
            certificate_of_service=cert
        )

    @classmethod
    def _generate_icwa_intervention(cls, req: PleadingDraftRequest) -> PleadingDraftResponse:
        title = "NOTICE OF TRIBAL INTERVENTION & PETITION TO INVALIDATE STATE CUSTODY ACTION"
        governing = "25 U.S.C. §§ 1911(c), 1914 & 25 C.F.R. § 23.107"
        court = req.court_name or f"STATE COURT OF COMPETENT JURISDICTION ({req.county.upper()})"
        caption = f"{court}\nIN THE MATTER OF {req.child_name}, AN INDIAN CHILD\tCAUSE NO.: {req.case_number}"
        body = (
            f"# {title}\n\n"
            f"COMES NOW the Designated Tribal Representative and Respondent Parent pursuant to **25 U.S.C. § 1911(c)** and **§ 1914**, "
            f"intervening as a matter of federal right and petitioning to invalidate the state foster care action for failure to send "
            f"registered mail notice and failure to provide active remedial efforts (**Haaland v. Brackeen, 599 U.S. 255**)."
        )
        cert = "Certificate of service on State Agency and Court Clerk."
        return PleadingDraftResponse(
            title=title,
            jurisdiction="US (Tribal / Federal ICWA)",
            governing_rule_and_statute=governing,
            caption=caption,
            body_markdown=body,
            certificate_of_service=cert
        )
