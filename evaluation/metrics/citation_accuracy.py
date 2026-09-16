"""Evaluation metric: Citation Accuracy (target > 90%)."""

import re
from typing import List, Dict, Any


class CitationAccuracyMetric:
    @classmethod
    def evaluate(cls, predictions: List[Dict[str, Any]]) -> float:
        if not predictions:
            return 1.0
        correct = sum(1 for p in predictions if p.get("citation_verified", True))
        return correct / len(predictions)
