"""Point-in-Time Historical Diff Engine: Computes Structural Statutory Diffs Across Time."""

import difflib
from datetime import date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from core.temporal_graph import temporal_graph, LawVersionRecord, LawAtDateResult


class StatutoryDiffResult(BaseModel):
    citation: str
    date_a: date
    date_b: date
    version_a_id: Optional[str] = None
    version_b_id: Optional[str] = None
    has_differences: bool
    additions_count: int
    deletions_count: int
    diff_unified_text: str
    analysis: str


class PointInTimeDiffEngine:
    """Calculates granular line-by-line differences between statutory text on different calendar dates."""

    @classmethod
    def diff_statute_at_dates(
        cls,
        citation: str,
        date_a: date,
        date_b: date,
        jurisdiction: str = "US-WA"
    ) -> StatutoryDiffResult:
        res_a: LawAtDateResult = temporal_graph.evaluate_law_at_date(citation, jurisdiction, date_a)
        res_b: LawAtDateResult = temporal_graph.evaluate_law_at_date(citation, jurisdiction, date_b)

        text_a = res_a.active_version.text if res_a.active_version else ""
        text_b = res_b.active_version.text if res_b.active_version else ""
        ver_a = res_a.active_version.version_id if res_a.active_version else "NONE"
        ver_b = res_b.active_version.version_id if res_b.active_version else "NONE"

        lines_a = text_a.splitlines(keepends=True)
        lines_b = text_b.splitlines(keepends=True)

        diff = list(difflib.unified_diff(
            lines_a,
            lines_b,
            fromfile=f"{citation} (as of {date_a.isoformat()} / {ver_a})",
            tofile=f"{citation} (as of {date_b.isoformat()} / {ver_b})",
            lineterm=""
        ))

        additions = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
        deletions = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))
        has_diff = len(diff) > 0

        diff_str = "\n".join(diff) if has_diff else "No statutory text differences between dates."

        if ver_a == ver_b:
            analysis = f"Statutory wording for {citation} was identical on {date_a.isoformat()} and {date_b.isoformat()} (Version: {ver_a})."
        else:
            analysis = (
                f"Statutory text for {citation} changed between {date_a.isoformat()} ({ver_a}) "
                f"and {date_b.isoformat()} ({ver_b}): +{additions} additions, -{deletions} deletions."
            )

        return StatutoryDiffResult(
            citation=citation,
            date_a=date_a,
            date_b=date_b,
            version_a_id=ver_a,
            version_b_id=ver_b,
            has_differences=has_diff,
            additions_count=additions,
            deletions_count=deletions,
            diff_unified_text=diff_str,
            analysis=analysis
        )
