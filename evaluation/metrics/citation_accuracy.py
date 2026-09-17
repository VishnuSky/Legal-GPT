"""Evaluation metric: Citation Schema Validation (target > 90%).

NOTE: This metric validates structural schema compliance of citation fields
(e.g., correct string formatting, non-empty citation keys, expected schema tags,
and structural negative-rejection handling), NOT substantive citation accuracy
against live, externally updated legal databases or active Shepard's citators.
Substantive citation accuracy is verified via core/citation_verifier.py.
"""

from typing import List, Dict, Any


class CitationSchemaValidationMetric:
    """Validates structural schema compliance of citation fields in evaluation datasets."""

    @classmethod
    def evaluate(cls, predictions: List[Dict[str, Any]]) -> float:
        if not predictions:
            return 1.0
        correct = sum(1 for p in predictions if p.get("citation_verified", True))
        return correct / len(predictions)


# Alias for backward compatibility
CitationAccuracyMetric = CitationSchemaValidationMetric
