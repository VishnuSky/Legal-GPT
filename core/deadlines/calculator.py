"""Deadline Calculator: Date arithmetic supporting court days, calendar days, and hours."""

from datetime import date, datetime, timedelta
from typing import Tuple, Optional


# Standard Federal & State Court Holidays (Month, Day)
STANDARD_COURT_HOLIDAYS = {
    (1, 1),   # New Year's Day
    (1, 19),  # MLK Day (approx mid-Jan)
    (2, 16),  # Presidents' Day (approx mid-Feb)
    (5, 25),  # Memorial Day (approx late May)
    (6, 19),  # Juneteenth
    (7, 4),   # Independence Day
    (9, 7),   # Labor Day (approx early Sept)
    (11, 11), # Veterans Day
    (11, 26), # Thanksgiving
    (12, 25), # Christmas Day
}


class DeadlineCalculator:
    """Computes statutory deadlines with court day and calendar day logic."""

    @staticmethod
    def parse_iso_date(date_str: str) -> Tuple[Optional[date], Optional[str]]:
        """Parses an ISO date string (YYYY-MM-DD), returning (date_obj, error_msg)."""
        if not date_str or not isinstance(date_str, str):
            return None, "Event date must be a non-empty string in YYYY-MM-DD format."
        try:
            # Handle timestamps by taking date portion if needed
            clean_date = date_str.split("T")[0].strip()
            parsed = datetime.strptime(clean_date, "%Y-%m-%d").date()
            return parsed, None
        except ValueError:
            return None, f"Invalid event_date '{date_str}'. Expected ISO 8601 format YYYY-MM-DD."

    @classmethod
    def is_court_day(cls, dt: date) -> bool:
        """Determines if a date is a court business day (Monday-Friday, non-holiday)."""
        # 5 is Saturday, 6 is Sunday
        if dt.weekday() in (5, 6):
            return False
        if (dt.month, dt.day) in STANDARD_COURT_HOLIDAYS:
            return False
        return True

    @classmethod
    def add_calendar_days(cls, start: date, days: int) -> date:
        """Adds calendar days."""
        return start + timedelta(days=days)

    @classmethod
    def add_court_days(cls, start: date, days: int) -> date:
        """Adds business / court days, skipping weekends and court holidays."""
        current = start
        added = 0
        while added < days:
            current += timedelta(days=1)
            if cls.is_court_day(current):
                added += 1
        return current

    @classmethod
    def compute_due_date(cls, start: date, amount: int, unit: str, mode: str) -> date:
        """General dispatcher computing due date based on unit and mode.
        
        Args:
            start: The triggering event date.
            amount: Number of units (e.g. 72, 30, 14).
            unit: 'hours', 'days', 'months'.
            mode: 'court_days' or 'calendar_days'.
        """
        if unit == "hours":
            # For 24 hours: 1 court day or 1 calendar day
            # For 72 hours: 3 court days (e.g. WA RCW 13.34.065 excludes weekends/holidays)
            days = max(1, amount // 24)
            if mode == "court_days":
                return cls.add_court_days(start, days)
            return cls.add_calendar_days(start, days)
        elif unit == "days":
            if mode == "court_days":
                return cls.add_court_days(start, amount)
            return cls.add_calendar_days(start, amount)
        elif unit == "months":
            # Approximation for months: 30 days per month
            approx_days = amount * 30
            return cls.add_calendar_days(start, approx_days)
        else:
            return cls.add_calendar_days(start, amount)
