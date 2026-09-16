"""Manifest parser and validator for Legal-GPT models."""

from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from pydantic import BaseModel, Field


class BaseManifest(BaseModel):
    name: str
    version: str
    family: str
    language: str
    base_model: Dict[str, Any]
    training: Dict[str, Any]
    runtime: Dict[str, Any]
    safety: Dict[str, Any]


class ModelManifest:
    """Manages loading and validation of legal_gpt_manifest.yaml."""

    def __init__(self, manifest_path: Optional[str] = None):
        self.manifest_path = Path(manifest_path) if manifest_path else Path("models/manifests/legal_gpt_manifest.yaml")
        self.data: Dict[str, Any] = {}
        self.load()

    def load(self) -> Dict[str, Any]:
        if self.manifest_path.exists():
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                raw = yaml.safe_load(f)
                self.data = raw.get("model", {})
        return self.data

    def is_valid(self) -> bool:
        required_keys = {"name", "version", "family", "base_model", "training", "runtime", "safety"}
        return required_keys.issubset(self.data.keys())

    @property
    def version(self) -> str:
        return self.data.get("version", "0.3.0-alpha")

    @property
    def base_model_name(self) -> str:
        return self.data.get("base_model", {}).get("name", "Unknown")
