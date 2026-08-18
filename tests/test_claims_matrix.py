"""Tests for Claims Matrix & Evidence Classification."""

from datetime import date
from cps.claims_matrix import ClaimsMatrix, CaseItem, LegalClaimRecord


def test_claims_matrix_workflow():
    matrix = ClaimsMatrix()

    # Add evidence exhibit item
    item1 = CaseItem(
        item_id="DOC_001",
        item_type="DOCUMENTED_EXHIBIT",
        description="CPS Initial Intake and Removal Notice dated 2026-04-12",
        source_document="CPS Report #47",
        date_occurred=date(2026, 4, 12),
        party="CPS Investigator",
        corroborated=True
    )
    matrix.add_item(item1)

    # Add legal claim
    claim = LegalClaimRecord(
        claim_id="CLM_001",
        claim_name="Failure to provide 72-hour shelter care hearing notice",
        associated_items=[item1],
        controlling_authority=["RCW 13.34.065"],
        counterarguments=["Agency claims emergency circumstances justified delay"],
        status="SUPPORTED",
        required_next_steps=["File motion for immediate release or expedited hearing"]
    )
    matrix.add_claim(claim)

    summary = matrix.get_summary_table()
    assert len(summary) == 1
    assert summary[0]["claim_id"] == "CLM_001"
    assert summary[0]["status"] == "SUPPORTED"
    assert summary[0]["evidence_count"] == 1
