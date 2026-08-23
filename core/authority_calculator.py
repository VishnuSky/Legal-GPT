"""14-Level Legal Authority Hierarchy and Dynamic Multi-Factor Authority Calculator."""

from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class AuthorityTier(str, Enum):
    T0_CONSTITUTIONAL = "T0"            # U.S. & State Constitutions
    T1_BINDING_SCOTUS = "T1"            # Supreme Court of the United States
    T2_BINDING_FED_CIRCUIT = "T2"       # Binding Federal Circuit Court of Appeals
    T3_BINDING_STATE_APPELLATE = "T3"   # State Supreme Court & Binding State Appellate Courts
    T4_FEDERAL_STATUTE = "T4"           # United States Code
    T5_STATE_STATUTE = "T5"             # State Official Statutes (RCW, ILCS, ORC, WIC, etc.)
    T6_FEDERAL_REGULATION = "T6"        # Code of Federal Regulations (eCFR)
    T7_STATE_REGULATION = "T7"          # State Administrative Codes (WAC, OAC, CCR, etc.)
    T8_COURT_RULES = "T8"               # Federal & State Court Rules, Local Rules, Juvenile Rules
    T9_ADMIN_ORDERS = "T9"              # Formal Administrative Decisions & Agency Declaratory Orders
    T10_AGENCY_POLICY = "T10"           # Agency Manuals & Handbooks (DCYF, DCFS, ODJFS, CDSS, DFPS)
    T11_PERSUASIVE_CASELAW = "T11"      # Out-of-circuit / Out-of-state appellate precedent
    T12_SECONDARY_SOURCES = "T12"       # Restatements, Uniform Model Acts, Law Reviews
    T13_COMMENTARY = "T13"              # Practice Guides, Treatises, Legal Commentary


class AuthorityEvaluation(BaseModel):
    tier: AuthorityTier
    base_tier_weight: float
    court_level_weight: float
    jurisdiction_match_weight: float
    binding_status_weight: float
    temporal_validity_weight: float
    procedural_posture_weight: float
    subject_matter_weight: float
    citation_treatment_weight: float
    total_composite_weight: float
    is_binding: bool
    rationale: str


class DynamicAuthorityCalculator:
    """Calculates dynamic contextual authority score based on jurisdictional, temporal, procedural, and treatment factors."""

    BASE_WEIGHTS = {
        AuthorityTier.T0_CONSTITUTIONAL: 1.00,
        AuthorityTier.T1_BINDING_SCOTUS: 0.98,
        AuthorityTier.T2_BINDING_FED_CIRCUIT: 0.94,
        AuthorityTier.T3_BINDING_STATE_APPELLATE: 0.92,
        AuthorityTier.T4_FEDERAL_STATUTE: 0.90,
        AuthorityTier.T5_STATE_STATUTE: 0.88,
        AuthorityTier.T6_FEDERAL_REGULATION: 0.84,
        AuthorityTier.T7_STATE_REGULATION: 0.82,
        AuthorityTier.T8_COURT_RULES: 0.80,
        AuthorityTier.T9_ADMIN_ORDERS: 0.75,
        AuthorityTier.T10_AGENCY_POLICY: 0.70,
        AuthorityTier.T11_PERSUASIVE_CASELAW: 0.60,
        AuthorityTier.T12_SECONDARY_SOURCES: 0.45,
        AuthorityTier.T13_COMMENTARY: 0.30,
    }

    @classmethod
    def calculate_weight(
        cls,
        tier: AuthorityTier,
        authority_jurisdiction: str,
        target_jurisdiction: str,
        is_binding_in_forum: bool = True,
        is_temporally_valid: bool = True,
        procedural_posture_matches: bool = True,
        subject_matter_match_score: float = 1.0,
        treatment: str = "FOLLOWED"  # OVERRULED, ABROGATED, DISTINGUISHED, CRITICIZED, FOLLOWED, QUESTIONED
    ) -> AuthorityEvaluation:
        base_w = cls.BASE_WEIGHTS.get(tier, 0.50)

        # 1. Jurisdiction Match (0.0 to 1.0)
        if authority_jurisdiction == target_jurisdiction or authority_jurisdiction == "US":
            juris_match = 1.00
        elif target_jurisdiction.startswith(authority_jurisdiction):
            juris_match = 0.95
        else:
            juris_match = 0.20  # Foreign state or out-of-jurisdiction

        # 2. Binding Status (0.0 to 1.0)
        binding_w = 1.00 if is_binding_in_forum else 0.50

        # 3. Temporal Validity (0.0 to 1.0)
        temporal_w = 1.00 if is_temporally_valid else 0.10

        # 4. Procedural Posture Match (0.0 to 1.0)
        posture_w = 1.00 if procedural_posture_matches else 0.65

        # 5. Subject Matter Match (0.0 to 1.0)
        subject_w = max(0.0, min(1.0, subject_matter_match_score))

        # 6. Citation Treatment (-1.0 to +1.0)
        treatment_upper = treatment.upper()
        if treatment_upper == "OVERRULED" or treatment_upper == "ABROGATED" or treatment_upper == "SUPERSEDED_BY_STATUTE":
            treatment_w = -0.90
        elif treatment_upper == "DISTINGUISHED":
            treatment_w = 0.40
        elif treatment_upper == "QUESTIONED" or treatment_upper == "CRITICIZED":
            treatment_w = 0.50
        elif treatment_upper == "FOLLOWED":
            treatment_w = 1.00
        else:
            treatment_w = 0.80

        # Composite weighted formula
        if treatment_w < 0:
            composite = 0.05  # Negatively treated / overruled authority is virtually disqualified
        else:
            composite = (
                (base_w * 0.30)
                + (juris_match * 0.25)
                + (binding_w * 0.15)
                + (temporal_w * 0.10)
                + (posture_w * 0.05)
                + (subject_w * 0.10)
                + (treatment_w * 0.05)
            )

        composite = round(max(0.0, min(1.0, composite)), 4)
        is_binding_final = is_binding_in_forum and juris_match >= 0.90 and temporal_w == 1.0 and treatment_w > 0

        rationale = (
            f"Tier {tier.value} ({tier.name}) with base weight {base_w:.2f}. "
            f"Jurisdiction match: {juris_match:.2f}, Binding: {binding_w:.2f}, "
            f"Temporal validity: {temporal_w:.2f}, Treatment: {treatment} ({treatment_w:.2f}). "
            f"Composite Authority Score: {composite:.4f}."
        )

        return AuthorityEvaluation(
            tier=tier,
            base_tier_weight=base_w,
            court_level_weight=base_w,
            jurisdiction_match_weight=juris_match,
            binding_status_weight=binding_w,
            temporal_validity_weight=temporal_w,
            procedural_posture_weight=posture_w,
            subject_matter_weight=subject_w,
            citation_treatment_weight=treatment_w,
            total_composite_weight=composite,
            is_binding=is_binding_final,
            rationale=rationale
        )
