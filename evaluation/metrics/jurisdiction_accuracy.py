"""Evaluation metrics for Jurisdiction, Temporal, Hallucination, Authority, and Refusal."""

from typing import List, Dict, Any


class JurisdictionAccuracyMetric:
    @classmethod
    def evaluate(cls, predictions: List[Dict[str, Any]]) -> float:
        if not predictions:
            return 1.0
        correct = sum(1 for p in predictions if p.get("jurisdiction_match", True))
        return correct / len(predictions)


class TemporalAccuracyMetric:
    @classmethod
    def evaluate(cls, predictions: List[Dict[str, Any]]) -> float:
        if not predictions:
            return 1.0
        correct = sum(1 for p in predictions if p.get("temporal_valid", True))
        return correct / len(predictions)


class HallucinationMetric:
    @classmethod
    def evaluate(cls, predictions: List[Dict[str, Any]]) -> float:
        if not predictions:
            return 0.0
        hallucinated = sum(1 for p in predictions if p.get("hallucination_detected", False))
        return hallucinated / len(predictions)


class AuthorityAccuracyMetric:
    @classmethod
    def evaluate(cls, predictions: List[Dict[str, Any]]) -> float:
        if not predictions:
            return 1.0
        correct = sum(1 for p in predictions if p.get("authority_tier_correct", True))
        return correct / len(predictions)


class RefusalAccuracyMetric:
    @classmethod
    def evaluate(cls, predictions: List[Dict[str, Any]]) -> float:
        if not predictions:
            return 1.0
        correct = sum(1 for p in predictions if p.get("appropriate_abstention", True))
        return correct / len(predictions)
