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
        if manifest_path:
            self.manifest_path = Path(manifest_path)
        else:
            local_path = Path("models/manifests/legal_gpt_manifest.yaml")
            if local_path.exists():
                self.manifest_path = local_path
            else:
                self.manifest_path = Path(__file__).resolve().parent.parent.parent / "models" / "manifests" / "legal_gpt_manifest.yaml"
        self.data: Dict[str, Any] = {}
        self.load()

    def load(self) -> Dict[str, Any]:
        if self.manifest_path.exists():
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                raw = yaml.safe_load(f)
                self.data = raw.get("model", {})
        return self.data

    def is_valid(self) -> bool:
        """Validates that required manifest fields exist and basic model identity is set.
        
        Accepts 'TBD' for base_model specification during alpha stage.
        """
        required_keys = {"name", "version", "family", "base_model", "training", "runtime", "safety"}
        if not required_keys.issubset(self.data.keys()):
            return False

        if not self.data.get("name") or not self.data.get("version"):
            return False

        if not isinstance(self.data.get("base_model"), dict):
            return False

        return True

    def is_production_ready(self) -> bool:
        """Requires all base_model fields to be fully specified with non-TBD values."""
        if not self.is_valid():
            return False

        base_model = self.data.get("base_model", {})
        for field in ("name", "architecture", "parameters", "context_length"):
            val = base_model.get(field)
            if val is None or str(val).strip().upper() in ("", "TBD", "UNKNOWN"):
                return False

        return True

    @property
    def version(self) -> str:
        return self.data.get("version", "0.3.0-alpha")

    @property
    def base_model_name(self) -> str:
        return self.data.get("base_model", {}).get("name", "Unknown")

