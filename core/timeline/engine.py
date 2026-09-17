"""Timeline Construction Engine: Chronological sequencing, procedural validation, and gap detection."""

from datetime import datetime, date
from typing import List, Optional, Tuple, Dict, Any

from legal_registry.loader import RegistryLoader, default_registry
from core.timeline.models import (
    TimelineEvent,
    TimelineRequest,
    TimelineReport,
    ProceduralIssue,
    EventCategory,
    SequenceFlag,
)
from core.deadlines.calculator import DeadlineCalculator


class TimelineEngine:
    """Constructs auditable legal timelines and evaluates procedural sequence validity."""

    def __init__(self, registry: Optional[RegistryLoader] = None):
        self.registry = registry or default_registry

    def _parse_event_datetime(self, date_str: str) -> datetime:
        """Parses ISO date/datetime string into datetime object for chronological sorting."""
        clean = date_str.strip()
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"):
            try:
                return datetime.strptime(clean, fmt)
            except ValueError:
                continue
        # Fallback if just date
        try:
            return datetime.combine(datetime.strptime(clean[:10], "%Y-%m-%d").date(), datetime.min.time())
        except Exception:
            return datetime.min

    def construct_timeline(self, request: TimelineRequest) -> TimelineReport:
        """Takes a set of raw events, chronologically orders them, and validates procedural rules."""
        if not request.events:
            return TimelineReport(
                total_events=0,
                chronological_events=[],
                detected_issues=[],
                jurisdictions_involved=[],
                has_jurisdiction_shift=False,
                procedural_compliance_score=1.0,
                summary="Empty event sequence provided."
            )

        # 1. Chronological Sorting
        sorted_events: List[TimelineEvent] = sorted(
            request.events,
            key=lambda e: self._parse_event_datetime(e.date)
        )

        detected_issues: List[ProceduralIssue] = []

        # 2. Jurisdiction Shift Analysis (UCCJEA / PKPA)
        jurisdictions = set()
        for ev in sorted_events:
            j = ev.jurisdiction or request.default_jurisdiction or "US"
            j_clean = j.upper().replace("US-", "").strip()
            if j_clean:
                jurisdictions.add(j_clean)

        has_jurisdiction_shift = len(jurisdictions) > 1
        if has_jurisdiction_shift:
            states_str = ", ".join(sorted(jurisdictions))
            detected_issues.append(ProceduralIssue(
                issue_type="JURISDICTION_SHIFT",
                severity="WARNING",
                description=(
                    f"Timeline spans multiple jurisdictions ({states_str}). Potential UCCJEA (Uniform Child "
                    f"Custody Jurisdiction and Enforcement Act) jurisdictional conflict. Under UCCJEA § 201, "
                    f"a court must possess 'home state' jurisdiction (child resided with parent for 6 consecutive months) "
                    f"before entering non-emergency custody orders."
                ),
                affected_events=[e.id for e in sorted_events],
                governing_authority="UCCJEA § 201; Parental Kidnapping Prevention Act (PKPA), 28 U.S.C. § 1738A"
            ))
            for ev in sorted_events:
                if SequenceFlag.JURISDICTION_SHIFT.value not in ev.flags:
                    ev.flags.append(SequenceFlag.JURISDICTION_SHIFT.value)

        # 3. Case-Type Specific Procedural Auditing (CPS Dependency Focus)
        if request.case_type == "cps_dependency":
            self._audit_cps_sequence(sorted_events, detected_issues, request.default_jurisdiction)

        # 4. Calculate Procedural Compliance Score
        critical_count = sum(1 for i in detected_issues if i.severity == "CRITICAL")
        warning_count = sum(1 for i in detected_issues if i.severity == "WARNING")
        penalty = (critical_count * 0.30) + (warning_count * 0.10)
        compliance_score = max(0.0, round(1.0 - penalty, 2))

        # 5. Build Summary
        summary = (
            f"Analyzed {len(sorted_events)} procedural events across {len(jurisdictions)} jurisdiction(s). "
            f"Detected {len(detected_issues)} procedural issue(s) with compliance score {compliance_score * 100:.0f}%."
        )

        return TimelineReport(
            total_events=len(sorted_events),
            chronological_events=sorted_events,
            detected_issues=detected_issues,
            jurisdictions_involved=sorted(list(jurisdictions)),
            has_jurisdiction_shift=has_jurisdiction_shift,
            procedural_compliance_score=compliance_score,
            summary=summary
        )

    def _audit_cps_sequence(
        self,
        events: List[TimelineEvent],
        issues: List[ProceduralIssue],
        default_jurisdiction: Optional[str]
    ) -> None:
        """Audits child welfare procedural milestones: removal -> shelter hearing -> petition -> adjudication -> disposition."""
        removal_indices = []
        shelter_indices = []
        petition_indices = []
        adjudication_indices = []
        disposition_indices = []

        for idx, ev in enumerate(events):
            cat = ev.category.upper()
            title_lower = ev.title.lower()

            if cat == EventCategory.REMOVAL.value or "removal" in title_lower or "protective custody" in title_lower:
                removal_indices.append(idx)
            elif "shelter" in title_lower or "detention" in title_lower or "preliminary hearing" in title_lower:
                shelter_indices.append(idx)
            elif cat == EventCategory.PETITION.value or "petition" in title_lower:
                petition_indices.append(idx)
            elif "adjudicat" in title_lower or "fact-finding" in title_lower or "jurisdictional hearing" in title_lower:
                adjudication_indices.append(idx)
            elif cat == EventCategory.DISPOSITION.value or "disposition" in title_lower:
                disposition_indices.append(idx)

        # Check 1: Removal without Shelter Hearing
        for r_idx in removal_indices:
            r_event = events[r_idx]
            subsequent_shelters = [s_idx for s_idx in shelter_indices if s_idx > r_idx]

            if not subsequent_shelters:
                r_event.flags.append(SequenceFlag.MISSING_REQUIRED_EVENT.value)
                issues.append(ProceduralIssue(
                    issue_type="MISSING_SHELTER_HEARING",
                    severity="CRITICAL",
                    description=(
                        f"Event '{r_event.title}' on {r_event.date} records a child removal, but no judicial "
                        f"shelter care / detention hearing appears subsequently on the timeline. Under state law "
                        f"and the Fourteenth Amendment Due Process clause, a judicial detention hearing is mandatory "
                        f"promptly following state removal of a child."
                    ),
                    affected_events=[r_event.id],
                    governing_authority="Fourteenth Amendment Due Process Clause; State Juvenile Court Act"
                ))
            else:
                # Check timing between removal and shelter hearing
                first_shelter_idx = subsequent_shelters[0]
                s_event = events[first_shelter_idx]
                r_dt = self._parse_event_datetime(r_event.date).date()
                s_dt = self._parse_event_datetime(s_event.date).date()
                days_diff = (s_dt - r_dt).days

                # Identify state
                state = (r_event.jurisdiction or default_jurisdiction or "US").upper().replace("US-", "").strip()
                max_calendar_days = 3 if state == "WA" else (1 if state == "FL" else 4)

                if days_diff > max_calendar_days:
                    s_event.flags.append(SequenceFlag.DEADLINE_EXCEEDED.value)
                    issues.append(ProceduralIssue(
                        issue_type="SHELTER_HEARING_DELAYED",
                        severity="WARNING",
                        description=(
                            f"Shelter hearing on {s_event.date} occurred {days_diff} days after removal on {r_event.date}, "
                            f"potentially exceeding statutory deadline limits ({max_calendar_days} days in {state})."
                        ),
                        affected_events=[r_event.id, s_event.id],
                        governing_authority=f"{state} Child Welfare Statutory Hearing Deadlines"
                    ))

        # Check 2: Out of Sequence Adjudication before Petition
        for adj_idx in adjudication_indices:
            adj_event = events[adj_idx]
            prior_petitions = [p_idx for p_idx in petition_indices if p_idx < adj_idx]

            if not prior_petitions and not petition_indices:
                adj_event.flags.append(SequenceFlag.OUT_OF_SEQUENCE.value)
                issues.append(ProceduralIssue(
                    issue_type="OUT_OF_SEQUENCE_ADJUDICATION",
                    severity="CRITICAL",
                    description=(
                        f"Adjudicatory / fact-finding hearing '{adj_event.title}' on {adj_event.date} appears "
                        f"without any prior formal dependency petition being filed. Court lacks subject matter jurisdiction "
                        f"to enter a dependency adjudication without a valid petition."
                    ),
                    affected_events=[adj_event.id],
                    governing_authority="Statutory Pleading and Notice Requirements; In re Gault, 387 U.S. 1 (1967)"
                ))

        # Check 3: Disposition before Adjudication
        for disp_idx in disposition_indices:
            disp_event = events[disp_idx]
            prior_adj = [a_idx for a_idx in adjudication_indices if a_idx < disp_idx]
            if not prior_adj and adjudication_indices:
                disp_event.flags.append(SequenceFlag.OUT_OF_SEQUENCE.value)
                issues.append(ProceduralIssue(
                    issue_type="OUT_OF_SEQUENCE_DISPOSITION",
                    severity="CRITICAL",
                    description=(
                        f"Dispositional hearing '{disp_event.title}' on {disp_event.date} occurred prior to fact-finding adjudication. "
                        f"Disposition can only be entered after parental unfitness or child dependency is formally adjudicated."
                    ),
                    affected_events=[disp_event.id],
                    governing_authority="Juvenile Court Rules - Bifurcated Adjudication/Disposition Structure"
                ))
