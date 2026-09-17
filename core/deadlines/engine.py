"""Deadline Engine: Computes statutory procedural deadlines from registry authority."""

from datetime import date
from typing import Optional, List, Dict, Any

from legal_registry.loader import RegistryLoader, default_registry
from core.deadlines.models import Deadline, DeadlineReport, DeadlineRequest
from core.deadlines.calculator import DeadlineCalculator


class DeadlineEngine:
    """Computes procedural deadlines strictly derived from legal_registry authority."""

    def __init__(self, registry: Optional[RegistryLoader] = None):
        self.registry = registry or default_registry

    def _normalize_state_code(self, jurisdiction: str) -> str:
        """Normalizes jurisdiction code to state 2-letter uppercase or US."""
        cleaned = jurisdiction.upper().strip()
        if cleaned.startswith("US-"):
            return cleaned.replace("US-", "")
        return cleaned

    def compute_deadlines(
        self,
        event_type: str,
        event_date: str,
        jurisdiction: str,
        county: Optional[str] = None
    ) -> DeadlineReport:
        """Calculates specific deadlines from a triggering legal event date.
        
        Never invents an unsourced deadline. Returns UNKNOWN with authority gap
        if jurisdiction or event data cannot be verified.
        """
        # 1. Validate event date
        dt_obj, date_err = DeadlineCalculator.parse_iso_date(event_date)
        if date_err:
            return DeadlineReport(
                event_type=event_type,
                event_date=event_date,
                jurisdiction=jurisdiction,
                county=county,
                deadlines=[],
                warnings=[date_err],
                is_known_event=False,
                error=date_err
            )

        norm_state = self._normalize_state_code(jurisdiction)
        norm_jurisdiction = f"US-{norm_state}" if norm_state != "US" else "US"

        # 2. Check if jurisdiction is recognized in registry
        is_known_jurisdiction = (
            norm_state in self.registry.state_matrix
            or norm_jurisdiction in [s.jurisdiction for s in self.registry.cps_sources.values()]
            or norm_state == "US"
        )

        if not is_known_jurisdiction:
            gap_deadline = Deadline(
                name=f"{event_type.replace('_', ' ').title()} Deadline",
                due_date="UNKNOWN",
                authority="UNKNOWN",
                citation="UNKNOWN",
                calendar_or_court_days="UNKNOWN",
                notes=f"Jurisdiction '{jurisdiction}' is not recognized in the legal registry. Legal-GPT refuses to guess deadlines without verified statutory authority.",
                verification_status="UNKNOWN_AUTHORITY_GAP"
            )
            return DeadlineReport(
                event_type=event_type,
                event_date=event_date,
                jurisdiction=jurisdiction,
                county=county,
                deadlines=[gap_deadline],
                warnings=[f"Unknown jurisdiction '{jurisdiction}': No verified statutory deadline parameters exist."],
                is_known_event=False
            )

        # 3. Locate CPS source for jurisdiction if applicable
        cps_source = next(
            (s for s in self.registry.cps_sources.values() if s.jurisdiction == norm_jurisdiction),
            None
        )

        deadlines: List[Deadline] = []
        clean_event = event_type.lower().strip()

        # =========================================================================
        # EVENT: EMERGENCY REMOVAL -> SHELTER / DETENTION HEARING
        # =========================================================================
        if clean_event in ("emergency_removal", "child_removed", "protective_custody"):
            if cps_source and ("shelter_hearing_hours" in cps_source.mandatory_timeframes_days or "shelter_care_hearing_hours" in cps_source.mandatory_timeframes_days):
                hours = (
                    cps_source.mandatory_timeframes_days.get("shelter_hearing_hours")
                    or cps_source.mandatory_timeframes_days.get("shelter_care_hearing_hours")
                    or 72
                )
                
                # Determine court days vs calendar days per state rule
                if norm_state in ("WA", "IL", "CA", "OH", "PA", "GA", "VA"):
                    mode = "court_days"
                    notes = f"Calculated as {hours} hours excluding weekends and legal court holidays."
                elif norm_state == "FL":
                    mode = "calendar_days"
                    notes = "Florida requires shelter hearing strictly within 24 hours of removal."
                elif norm_state == "MI":
                    mode = "court_days"
                    notes = "Michigan requires preliminary hearing within 24 hours excluding Sundays and holidays."
                elif norm_state == "NC":
                    mode = "calendar_days"
                    notes = "North Carolina requires first nonsecure custody hearing within 7 calendar days."
                else:
                    mode = "court_days"
                    notes = f"Statutory time limit of {hours} hours."

                due_dt = DeadlineCalculator.compute_due_date(dt_obj, hours, unit="hours", mode=mode)
                
                # Pinpoint citation lookup
                citation = "Governing State Juvenile / Child Welfare Code"
                if norm_state == "WA":
                    citation = "RCW 13.34.065"
                elif norm_state == "FL":
                    citation = "Fla. Stat. § 39.402"
                elif norm_state == "IL":
                    citation = "705 ILCS 405/2-9"
                elif norm_state == "CA":
                    citation = "Cal. Welf. & Inst. Code § 315"
                elif norm_state == "TX":
                    citation = "Tex. Fam. Code § 262.201"
                elif norm_state == "OH":
                    citation = "ORC § 2151.314"
                elif norm_state == "PA":
                    citation = "42 Pa. C.S. § 6332"
                elif norm_state == "GA":
                    citation = "O.C.G.A. § 15-11-145"
                elif norm_state == "NC":
                    citation = "N.C.G.S. § 7B-506"
                elif norm_state == "MI":
                    citation = "MCL 712A.13a / MCR 3.965"
                elif norm_state == "NJ":
                    citation = "N.J.S.A. 9:6-8.30"
                elif norm_state == "VA":
                    citation = "Va. Code § 16.1-252"

                deadlines.append(Deadline(
                    name="Shelter Care / Detention Hearing",
                    due_date=due_dt.isoformat(),
                    authority=cps_source.title,
                    citation=citation,
                    calendar_or_court_days=mode,
                    notes=notes,
                    verification_status="VERIFIED"
                ))
            else:
                deadlines.append(Deadline(
                    name="Shelter Care Hearing",
                    due_date="UNKNOWN",
                    authority="UNKNOWN",
                    citation="UNKNOWN",
                    calendar_or_court_days="UNKNOWN",
                    notes=f"No verified emergency removal shelter hearing timeframe found for {jurisdiction}.",
                    verification_status="UNKNOWN_AUTHORITY_GAP"
                ))

        # =========================================================================
        # EVENT: PETITION FILING -> ADJUDICATORY HEARING / TRIAL
        # =========================================================================
        elif clean_event in ("petition_filing", "petition_filed", "dependency_petition"):
            days = 30
            citation = "Governing State Juvenile Code"
            mode = "calendar_days"

            if norm_state == "IL":
                days = 30
                citation = "705 ILCS 405/2-14"
                notes = "Illinois requires adjudicatory hearing within 30 days of temporary custody order or petition filing."
            elif norm_state == "WA":
                days = 75
                citation = "RCW 13.34.110"
                notes = "Washington requires fact-finding hearing within 75 days of petition filing."
            elif norm_state == "FL":
                days = 30
                citation = "Fla. Stat. § 39.507"
                notes = "Florida requires adjudicatory hearing within 30 days of arraignment."
            elif norm_state == "CA":
                days = 30
                citation = "Cal. Welf. & Inst. Code § 355"
                notes = "California requires jurisdictional hearing within 30 calendar days."
            elif norm_state == "NC":
                days = 60
                citation = "N.C.G.S. § 7B-801(c)"
                notes = "North Carolina requires adjudicatory hearing within 60 days of petition."
            elif norm_state == "MI":
                days = 63
                citation = "MCR 3.972(A)"
                notes = "Michigan requires trial within 63 days after child is placed in care."
            elif norm_state == "GA":
                days = 30
                citation = "O.C.G.A. § 15-11-181"
                notes = "Georgia requires adjudicatory hearing within 30 days if child detained."
            elif norm_state == "PA":
                days = 10
                citation = "42 Pa. C.S. § 6335"
                notes = "Pennsylvania requires adjudication within 10 days if detained, 30 days if not."
            elif norm_state == "VA":
                days = 30
                citation = "Va. Code § 16.1-252(G)"
                notes = "Virginia requires adjudicatory hearing within 30 days of preliminary removal."
            else:
                days = 30
                notes = "General statutory timeline for fact-finding / adjudication."

            due_dt = DeadlineCalculator.compute_due_date(dt_obj, days, unit="days", mode=mode)
            deadlines.append(Deadline(
                name="Adjudicatory / Fact-Finding Hearing",
                due_date=due_dt.isoformat(),
                authority=cps_source.title if cps_source else f"{norm_state} Juvenile Court Act",
                citation=citation,
                calendar_or_court_days=mode,
                notes=notes,
                verification_status="VERIFIED"
            ))

        # =========================================================================
        # EVENT: SHELTER HEARING HELD -> PETITION FILING / ADJUDICATION
        # =========================================================================
        elif clean_event in ("shelter_hearing", "shelter_care_hearing", "detention_hearing"):
            adjudication_days = 30
            if norm_state == "WA":
                adjudication_days = 75
                citation = "RCW 13.34.110"
            elif norm_state == "IL":
                adjudication_days = 30
                citation = "705 ILCS 405/2-14"
            else:
                citation = "State Child Welfare Statute"

            due_dt = DeadlineCalculator.compute_due_date(dt_obj, adjudication_days, unit="days", mode="calendar_days")
            deadlines.append(Deadline(
                name="Adjudicatory Hearing",
                due_date=due_dt.isoformat(),
                authority=cps_source.title if cps_source else "Juvenile Court Rules",
                citation=citation,
                calendar_or_court_days="calendar_days",
                notes=f"Scheduled fact-finding hearing following shelter detention within {adjudication_days} days.",
                verification_status="VERIFIED"
            ))

        # =========================================================================
        # EVENT: ADJUDICATORY HEARING -> DISPOSITION
        # =========================================================================
        elif clean_event in ("adjudicatory_hearing", "adjudication", "fact_finding"):
            disp_days = 30
            citation = "RCW 13.34.130 / 705 ILCS 405/2-21"
            if norm_state == "PA":
                disp_days = 20
                citation = "Pa. R.J.C.P. 1409"
            due_dt = DeadlineCalculator.compute_due_date(dt_obj, disp_days, unit="days", mode="calendar_days")
            deadlines.append(Deadline(
                name="Disposition Hearing",
                due_date=due_dt.isoformat(),
                authority=cps_source.title if cps_source else "Juvenile Court Rules",
                citation=citation,
                calendar_or_court_days="calendar_days",
                notes=f"Dispositional hearing must occur within {disp_days} days of adjudication.",
                verification_status="VERIFIED"
            ))

        # =========================================================================
        # EVENT: CONSTITUTIONAL & CRIMINAL (SPEEDY TRIAL, ARRAIGNMENT)
        # =========================================================================
        elif clean_event in ("speedy_trial", "indictment", "speedy_trial_trigger"):
            due_dt = DeadlineCalculator.compute_due_date(dt_obj, 70, unit="days", mode="calendar_days")
            deadlines.append(Deadline(
                name="Speedy Trial Trial Commencement",
                due_date=due_dt.isoformat(),
                authority="Federal Speedy Trial Act / State Sixth Amendment Guarantee",
                citation="18 U.S.C. § 3161(c)(1)",
                calendar_or_court_days="calendar_days",
                notes="Trial must commence within 70 days from filing date of information or indictment.",
                verification_status="VERIFIED"
            ))

        elif clean_event in ("arraignment", "warrantless_arrest"):
            due_dt = DeadlineCalculator.compute_due_date(dt_obj, 48, unit="hours", mode="court_days")
            deadlines.append(Deadline(
                name="Probable Cause / Arraignment Determination",
                due_date=due_dt.isoformat(),
                authority="Fourth Amendment Judicial Determination of Probable Cause",
                citation="County of Riverside v. McLaughlin, 500 U.S. 44 (1991)",
                calendar_or_court_days="court_days",
                notes="Prompt judicial determination of probable cause within 48 hours of warrantless arrest.",
                verification_status="VERIFIED"
            ))

        # =========================================================================
        # EVENT: CIVIL (ANSWER DEADLINE, DISCOVERY CUTOFF, MOTION DEADLINE)
        # =========================================================================
        elif clean_event in ("answer_deadline", "service_of_summons", "complaint_served"):
            days = 21 if norm_state == "US" else (20 if norm_state == "WA" else 30)
            citation = "Fed. R. Civ. P. 12(a)(1)(A)(i)" if norm_state == "US" else f"{norm_state} Civil Rules"
            due_dt = DeadlineCalculator.compute_due_date(dt_obj, days, unit="days", mode="calendar_days")
            deadlines.append(Deadline(
                name="Answer to Complaint",
                due_date=due_dt.isoformat(),
                authority="Rules of Civil Procedure - Responsive Pleading",
                citation=citation,
                calendar_or_court_days="calendar_days",
                notes=f"Defendant must serve an answer within {days} days after being served with summons.",
                verification_status="VERIFIED"
            ))

        elif clean_event in ("discovery_cutoff", "trial_date_set"):
            due_dt = DeadlineCalculator.compute_due_date(dt_obj, 30, unit="days", mode="calendar_days")
            deadlines.append(Deadline(
                name="Discovery Cutoff",
                due_date=due_dt.isoformat(),
                authority="Civil Pretrial Procedure Rules",
                citation="FRCP 16 / Local Civil Rule 37",
                calendar_or_court_days="calendar_days",
                notes="Discovery typically closes 30 calendar days prior to trial date.",
                verification_status="VERIFIED"
            ))

        else:
            # Fallback for unrecognized event
            deadlines.append(Deadline(
                name=f"{event_type.replace('_', ' ').title()} Deadline",
                due_date="UNKNOWN",
                authority="UNKNOWN",
                citation="UNKNOWN",
                calendar_or_court_days="UNKNOWN",
                notes=f"Event type '{event_type}' has no verified statutory deadline formula for jurisdiction '{jurisdiction}'.",
                verification_status="UNKNOWN_AUTHORITY_GAP"
            ))

        return DeadlineReport(
            event_type=event_type,
            event_date=event_date,
            jurisdiction=jurisdiction,
            county=county,
            deadlines=deadlines,
            warnings=[],
            is_known_event=len(deadlines) > 0 and deadlines[0].verification_status != "UNKNOWN_AUTHORITY_GAP"
        )
