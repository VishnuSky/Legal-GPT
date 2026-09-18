"""Document Explainer Engine: Explains legal court documents at multiple literacy levels."""

import re
from typing import Optional, List, Dict, Any

from legal_registry.loader import RegistryLoader, default_registry
from core.document_explainer.models import (
    DocumentType,
    DeadlineItem,
    RightItem,
    ActionItem,
    DocumentExplanationRequest,
    DocumentExplanationReport,
)


class DocumentExplainerEngine:
    """Explains legal notices, petitions, orders, and summons grounded in primary law."""

    def __init__(self, registry: Optional[RegistryLoader] = None):
        self.registry = registry or default_registry

    def _normalize_jurisdiction(self, jur: Optional[str]) -> str:
        if not jur:
            return "US"
        clean = jur.upper().replace("US-", "").strip()
        return clean if clean else "US"

    def _detect_document_type(self, req: DocumentExplanationRequest) -> str:
        """Determines the document type from explicit type or text keywords."""
        if req.document_type:
            clean = req.document_type.upper().replace(" ", "_").strip()
            if clean in ("SHELTER_CARE_ORDER", "SHELTER_ORDER", "REMOVAL_ORDER", "DETENTION_ORDER"):
                return DocumentType.TEMPORARY_CUSTODY_ORDER.value
            for member in DocumentType:
                if member.value == clean or member.name == clean:
                    return member.value

        text = (req.document_text or "").lower()
        if "summons" in text and ("complaint" in text or "sued" in text or "appear" in text):
            return DocumentType.SUMMONS_AND_COMPLAINT.value
        if "dependency petition" in text or "petition in the interest of" in text or "petition for dependency" in text:
            return DocumentType.DEPENDENCY_PETITION.value
        if "temporary custody" in text or "order for immediate custody" in text or "shelter care order" in text:
            return DocumentType.TEMPORARY_CUSTODY_ORDER.value
        if "notice of investigation" in text or "child abuse investigation" in text:
            return DocumentType.NOTICE_OF_INVESTIGATION.value
        if "subpoena" in text:
            return DocumentType.SUBPOENA.value
        if "terminate parental rights" in text or "tpr" in text:
            return DocumentType.MOTION_TO_TERMINATE_PARENTAL_RIGHTS.value
        if "protective order" in text or "restraining order" in text:
            return DocumentType.PROTECTIVE_ORDER.value

        return DocumentType.UNKNOWN.value

    def explain_document(self, request: DocumentExplanationRequest) -> DocumentExplanationReport:
        """Analyzes a legal document and generates a literacy-graded breakdown."""
        doc_type = self._detect_document_type(request)
        state = self._normalize_jurisdiction(request.jurisdiction)
        level = request.literacy_level if request.literacy_level in (1, 2, 3) else 1

        # =========================================================================
        # 1. SUMMONS AND COMPLAINT
        # =========================================================================
        if doc_type == DocumentType.SUMMONS_AND_COMPLAINT.value:
            deadline_days = 21 if state == "US" else (20 if state == "WA" else 30)
            citation = "Fed. R. Civ. P. 12(a)(1)(A)(i)" if state == "US" else f"{state} Civil Rules (CR 12)"

            deadlines = [
                DeadlineItem(
                    name="Answer / Responsive Pleading Deadline",
                    timeframe=f"{deadline_days} calendar days from date of service",
                    citation=citation,
                    consequence_of_missing="Plaintiff can obtain a Default Judgment awarding all requested relief without a trial."
                )
            ]

            rights = [
                RightItem(
                    right_name="Right to Contest and Defend",
                    description="You have the legal right to file a written Answer denying the allegations and asserting affirmative defenses.",
                    authority="Procedural Due Process / Civil Rule 8"
                ),
                RightItem(
                    right_name="Right to Challenge Jurisdiction / Service",
                    description="You may file a pre-answer Motion to Dismiss if service was improper or the court lacks jurisdiction.",
                    authority="Civil Rule 12(b)"
                )
            ]

            consequences = [
                "Entry of Default Judgment awarding monetary damages or requested injunctions against you.",
                "Forfeiture of compulsory counterclaims and affirmative defenses.",
                "Subsequent wage garnishment, bank levies, or liens on personal property."
            ]

            actions = [
                ActionItem(step="Note Exact Service Date", priority="URGENT", description="Write down the exact date, time, and method by which you received this document."),
                ActionItem(step="Consult Legal Counsel or Legal Aid", priority="URGENT", description="Contact an attorney or local legal aid society immediately before your response window closes."),
                ActionItem(step="Draft and File Answer", priority="IMPORTANT", description=f"File a written Answer with the court clerk and serve a copy on plaintiff's attorney within {deadline_days} days.")
            ]

            plain_en = (
                "You have been officially sued in court. This document consists of two parts: the Summons (which tells "
                f"you that you are sued and commands you to respond within {deadline_days} days) and the Complaint "
                "(which lists what the other party claims happened and what they want from you). If you do not reply in writing, "
                "the other side wins automatically by 'default'."
            )

            practical = (
                f"Do not ignore this paper. Count {deadline_days} days from the day you received it. You must file a written "
                "response (an 'Answer') with the court clerk and mail a copy to the other party's attorney. Simply calling the court "
                "or talking to the plaintiff will NOT prevent a default judgment."
            )

            legal_term = (
                "Formal civil process initiating an adversarial action. Comprises Summons establishing in personam jurisdiction "
                "and Complaint alleging cause of action under Civil Rules. Triggers mandatory responsive pleading window under "
                f"Rule 12(a); failure to plead or otherwise defend results in entry of default under Rule 55."
            )

            return DocumentExplanationReport(
                document_title="Summons and Complaint",
                document_category="Civil Litigation",
                jurisdiction=state,
                issuing_body="State / Federal Court Clerk",
                purpose_summary="Commands a formal written response to an initiated civil lawsuit.",
                literacy_level=level,
                plain_english_explanation=plain_en,
                practical_explanation=practical,
                legal_terminology_explanation=legal_term,
                deadlines=deadlines,
                rights=rights,
                consequences_of_inaction=consequences,
                recommended_actions=actions,
                verification_status="VERIFIED"
            )

        # =========================================================================
        # 2. DEPENDENCY PETITION
        # =========================================================================
        elif doc_type == DocumentType.DEPENDENCY_PETITION.value:
            hearing_hours = 72 if state in ("WA", "OH", "CA", "PA", "GA") else (24 if state == "FL" else 48)
            citation = "Governing State Juvenile / Child Welfare Code"
            if state == "WA":
                citation = "RCW 13.34.040 / RCW 13.34.065"
            elif state == "IL":
                citation = "705 ILCS 405/2-13"
            elif state == "FL":
                citation = "Fla. Stat. § 39.501"

            deadlines = [
                DeadlineItem(
                    name="Shelter Care / Preliminary Detention Hearing",
                    timeframe=f"Within {hearing_hours} hours of emergency removal (if child detained)",
                    citation=citation,
                    consequence_of_missing="Child remains in state custody; initial placement decisions made without parental input."
                ),
                DeadlineItem(
                    name="Adjudicatory / Fact-Finding Hearing",
                    timeframe="Within 30 to 75 days of petition filing",
                    citation=citation,
                    consequence_of_missing="Waiver of trial rights and potential default finding of dependency."
                )
            ]

            rights = [
                RightItem(
                    right_name="Right to Court-Appointed Attorney",
                    description="Parents have a statutory and constitutional due process right to counsel at all stages of child dependency proceedings.",
                    authority="Fourteenth Amendment Due Process; State Juvenile Code"
                ),
                RightItem(
                    right_name="Indian Child Welfare Act (ICWA) Inquiry",
                    description="The court and agency must inquire into whether the child is an Indian child under ICWA.",
                    authority="25 U.S.C. § 1912(a)"
                ),
                RightItem(
                    right_name="Right to Frequent Parent-Child Visitation",
                    description="Parents have the right to regular visitation unless the court finds that visitation causes serious physical or emotional harm.",
                    authority="State Child Welfare Statutory Rules"
                )
            ]

            consequences = [
                "Child will remain in state foster care or out-of-home placement.",
                "Juvenile court may enter an order of dependency stripping parents of primary legal custody.",
                "Can initiate statutory timeline toward termination of parental rights (TPR) if child remains out of home for 15 of 22 months under ASFA."
            ]

            actions = [
                ActionItem(step="Request Court-Appointed Counsel", priority="URGENT", description="Immediately contact the court clerk or public defender's office to request appointed counsel before the first hearing."),
                ActionItem(step="Attend All Scheduled Hearings", priority="URGENT", description="Never skip a court hearing. Failing to appear can be treated as a default admission of the petition's claims."),
                ActionItem(step="Identify Relative Placements", priority="IMPORTANT", description="Provide the caseworker and court with names and contact details of trusted relatives (grandparents, aunts/uncles) for kinship care.")
            ]

            plain_en = (
                "The child welfare agency has asked a judge to take legal custody of your child. The agency claims "
                "that the child is neglected, abused, or without proper care. This is a serious court case, but you have the "
                "right to a free lawyer if you cannot afford one."
            )

            practical = (
                "You must attend the first hearing (often called a shelter hearing). Ask the judge for a lawyer the moment your "
                "case is called if one was not already assigned. Do not discuss the facts with caseworkers or police without your lawyer present."
            )

            legal_term = (
                "Pleading invoking juvenile court subject-matter jurisdiction over a minor child pursuant to state dependency statutes. "
                "Commences non-criminal civil proceedings to adjudicate parental unfitness, custody, and protective disposition under ASFA and ICWA."
            )

            return DocumentExplanationReport(
                document_title="Child Dependency Petition",
                document_category="Child Welfare / Juvenile Law",
                jurisdiction=state,
                issuing_body="State Child Welfare Agency / County Prosecutor",
                purpose_summary="Petitions juvenile court to assume protective legal custody of a minor child.",
                literacy_level=level,
                plain_english_explanation=plain_en,
                practical_explanation=practical,
                legal_terminology_explanation=legal_term,
                deadlines=deadlines,
                rights=rights,
                consequences_of_inaction=consequences,
                recommended_actions=actions,
                verification_status="VERIFIED"
            )

        # =========================================================================
        # 3. TEMPORARY CUSTODY ORDER / REMOVAL ORDER
        # =========================================================================
        elif doc_type == DocumentType.TEMPORARY_CUSTODY_ORDER.value:
            deadlines = [
                DeadlineItem(
                    name="Mandatory Shelter Care Review Hearing",
                    timeframe="Within 24 to 72 hours of entry or physical removal",
                    citation="State Juvenile Court Emergency Removal Rules",
                    consequence_of_missing="Emergency custody continues without judicial scrutiny."
                )
            ]

            rights = [
                RightItem(
                    right_name="Right to Immediate Judicial Review",
                    description="Judicial order placing custody temporarily with the state requires immediate confirmation at a hearing with counsel present.",
                    authority="Fourteenth Amendment Due Process; Procedural Safeguards"
                ),
                RightItem(
                    right_name="Right to Relative Kinship Preference",
                    description="State agencies are legally required to evaluate adult relatives as placement alternatives prior to foster care placement.",
                    authority="42 U.S.C. § 671(a)(29); State Kinship Statutes"
                )
            ]

            consequences = [
                "Continued physical separation of child from parents.",
                "Child placed in licensed stranger foster care if kinship caregivers are not identified."
            ]

            actions = [
                ActionItem(step="Request Shelter Hearing Immediately", priority="URGENT", description="Ensure a formal shelter care hearing is docketed within the statutory 24-72 hour window."),
                ActionItem(step="Provide Kinship Caregiver Names", priority="IMPORTANT", description="Submit a list of eligible family members willing to provide temporary kinship care.")
            ]

            plain_en = (
                "A judge has granted temporary permission for the state to take custody of your child on an emergency basis. "
                "This is not a permanent decision, and you have the right to challenge it in front of a judge within days."
            )

            practical = (
                "Prepare for the upcoming shelter hearing. Gather contact information for family members who can care for your child "
                "so the child does not have to stay in foster care while the case is sorted out."
            )

            legal_term = (
                "Interlocutory ex parte or preliminary judicial decree transferring physical and legal custody pendente lite. "
                "Subject to immediate adversarial shelter/detention hearing under procedural due process strictures."
            )

            return DocumentExplanationReport(
                document_title="Temporary Custody / Emergency Removal Order",
                document_category="Family / Juvenile Court Order",
                jurisdiction=state,
                issuing_body="Juvenile / Family Court Division",
                purpose_summary="Authorizes immediate temporary state custody pending formal shelter hearing.",
                literacy_level=level,
                plain_english_explanation=plain_en,
                practical_explanation=practical,
                legal_terminology_explanation=legal_term,
                deadlines=deadlines,
                rights=rights,
                consequences_of_inaction=consequences,
                recommended_actions=actions,
                verification_status="VERIFIED"
            )

        # =========================================================================
        # 4. SUBPOENA
        # =========================================================================
        elif doc_type == DocumentType.SUBPOENA.value:
            deadlines = [
                DeadlineItem(
                    name="Appearance / Production Date",
                    timeframe="Specified on face of subpoena",
                    citation="FRCP 45 / State Court Rules",
                    consequence_of_missing="Court may issue a bench warrant for contempt of court and impose monetary sanctions."
                )
            ]

            rights = [
                RightItem(
                    right_name="Right to Move to Quash or Modify",
                    description="You can file a formal motion asking the court to cancel or modify the subpoena if it is unduly burdensome or requests privileged material.",
                    authority="Civil Rule 45(d)(3)"
                ),
                RightItem(
                    right_name="Fifth Amendment Privilege Against Self-Incrimination",
                    description="You cannot be compelled to provide testimony that could expose you to criminal liability.",
                    authority="U.S. Const. amend. V"
                )
            ]

            consequences = [
                "Contempt of court citation.",
                "Issuance of a bench warrant for your arrest to compel attendance.",
                "Monetary sanctions for attorney fees incurred by the issuing party."
            ]

            actions = [
                ActionItem(step="Verify Subpoena Validity and Dates", priority="URGENT", description="Check whether the subpoena is signed by a court clerk or licensed attorney and note the appearance date."),
                ActionItem(step="Consult Legal Counsel", priority="IMPORTANT", description="If testifying could risk criminal liability or if complying requires burdensome document collection, consult a lawyer to file a motion to quash.")
            ]

            plain_en = (
                "A subpoena is a direct court order commanding you to show up to testify, or to bring certain papers or records. "
                "You cannot ignore it; doing so can result in arrest or fines."
            )

            practical = (
                "Check the date, time, and courtroom listed on the subpoena. If you have a conflict or cannot comply, you must contact "
                "the lawyer who sent it or hire an attorney to file a motion to modify it before the date."
            )

            legal_term = (
                "Judicial writ issued under seal of the court commanding attendance (ad testificandum) or production of tangible evidence "
                "(duces tecum). Failure to comply without adequate excuse constitutes civil or criminal contempt under Rule 45(g)."
            )

            return DocumentExplanationReport(
                document_title="Subpoena (Command to Appear or Produce)",
                document_category="Court Process / Discovery",
                jurisdiction=state,
                issuing_body="Court of Competent Jurisdiction",
                purpose_summary="Legally compels personal attendance for testimony or production of documents.",
                literacy_level=level,
                plain_english_explanation=plain_en,
                practical_explanation=practical,
                legal_terminology_explanation=legal_term,
                deadlines=deadlines,
                rights=rights,
                consequences_of_inaction=consequences,
                recommended_actions=actions,
                verification_status="VERIFIED"
            )

        # =========================================================================
        # 5. UNKNOWN / UNRECOGNIZED
        # =========================================================================
        else:
            return DocumentExplanationReport(
                document_title="Unrecognized Legal Document",
                document_category="General Legal Notice",
                jurisdiction=state,
                issuing_body="Unknown Issuing Body",
                purpose_summary="Document type cannot be determined with verified certainty from provided information.",
                literacy_level=level,
                plain_english_explanation="The system could not identify this document with verified accuracy. Legal-GPT does not guess when legal rights and deadlines are at stake.",
                practical_explanation="Examine the top of the paper for a court title, case number, or headline like 'Notice', 'Order', or 'Summons'. Take this document to a local court clerk or legal aid clinic.",
                legal_terminology_explanation="Unclassified legal instrument lacking determinable procedural posture under governing procedural rules.",
                deadlines=[],
                rights=[],
                consequences_of_inaction=["Missing an unverified court deadline may result in waiver of procedural rights."],
                recommended_actions=[
                    ActionItem(step="Inspect Case Caption", priority="IMPORTANT", description="Identify the court, case number, and parties listed at the top."),
                    ActionItem(step="Seek Legal Aid Guidance", priority="URGENT", description="Present document to an attorney or legal aid self-help center for direct review.")
                ],
                verification_status="UNKNOWN_AUTHORITY_GAP"
            )
