"""Human Rights & International Norms Authority Tier Classifier."""

from enum import Enum
from typing import Dict, Any, List
from pydantic import BaseModel, Field


class HumanRightsAuthorityTier(str, Enum):
    BINDING_DOMESTIC_LAW = "BINDING_DOMESTIC_LAW"          # Tier 1: Statutes, Constitutions
    PERSUASIVE_DOMESTIC = "PERSUASIVE_DOMESTIC"              # Tier 2: Non-binding sister court rulings
    CONSTITUTIONAL_PRINCIPLE = "CONSTITUTIONAL_PRINCIPLE"    # Tier 3: Core constitutional doctrines
    ADMINISTRATIVE_REGULATION = "ADMINISTRATIVE_REGULATION"  # Tier 4: Promulgated agency rules
    RATIFIED_TREATY = "RATIFIED_TREATY"                      # Tier 5: Ratified treaties (Self-executing)
    INTERNATIONAL_DECLARATION = "INTERNATIONAL_DECLARATION"  # Tier 6: UDHR, CRC (Persuasive non-binding norms)
    SECONDARY_COMMENTARY = "SECONDARY_COMMENTARY"            # Tier 7: Law review articles, treatises
    POLICY_ARGUMENT = "POLICY_ARGUMENT"                      # Tier 8: Public advocacy, reform proposals


class AuthorityClassification(BaseModel):
    source_name: str
    tier: HumanRightsAuthorityTier
    is_legally_binding_in_us_court: bool
    epistemic_warning: str


class HumanRightsClassifier:
    """Enforces strict differentiation between binding domestic statutes and non-binding international norms."""

    @classmethod
    def classify(cls, source_name: str) -> AuthorityClassification:
        name_lower = source_name.lower()
        if any(w in name_lower for w in ["rcw", "ilcs", "r.c.", "u.s.c.", "usc", "statute", "constitution"]):
            return AuthorityClassification(
                source_name=source_name,
                tier=HumanRightsAuthorityTier.BINDING_DOMESTIC_LAW,
                is_legally_binding_in_us_court=True,
                epistemic_warning="Binding domestic authority. Directly enforceable in jurisdictional courts."
            )
        elif any(w in name_lower for w in ["declaration", "udhr", "un crc", "convention on the rights of the child", "geneva"]):
            return AuthorityClassification(
                source_name=source_name,
                tier=HumanRightsAuthorityTier.INTERNATIONAL_DECLARATION,
                is_legally_binding_in_us_court=False,
                epistemic_warning="Persuasive international norm/declaration. Non-binding in domestic state/federal proceedings unless incorporated by statute."
            )
        elif any(w in name_lower for w in ["treaty", "covenant", "iccppr"]):
            return AuthorityClassification(
                source_name=source_name,
                tier=HumanRightsAuthorityTier.RATIFIED_TREATY,
                is_legally_binding_in_us_court=False, # Depends on self-executing status (Medellin v. Texas)
                epistemic_warning="International treaty authority. Enforceability in domestic courts requires self-executing ratification or implementing federal statute."
            )
        else:
            return AuthorityClassification(
                source_name=source_name,
                tier=HumanRightsAuthorityTier.SECONDARY_COMMENTARY,
                is_legally_binding_in_us_court=False,
                epistemic_warning="Secondary commentary or policy proposal. Non-binding persuasive reference only."
            )
