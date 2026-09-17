"""Model weights, GGUF adapters, and checkpoint registry."""

from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ModelArtifact(BaseModel):
    artifact_id: str
    artifact_type: str # gguf, adapter, merged, checkpoint
    path: str
    quantization: Optional[str] = None
    filesize_bytes: int = 0
    sha256: str = ""
    is_ready: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ModelRegistry:
    """Discovers and catalogs GGUF models, LoRA adapters, and checkpoints."""

    def __init__(self, models_root: Optional[str] = None):
        self.models_root = Path(models_root) if models_root else Path("models")
        self.artifacts: Dict[str, ModelArtifact] = {}
        self.scan()

    def scan(self):
        self.artifacts.clear()
        if not self.models_root.exists():
            return

        # Scan gguf directory
        gguf_dir = self.models_root / "gguf"
        if gguf_dir.exists():
            for f in gguf_dir.glob("*.gguf"):
                art = ModelArtifact(
                    artifact_id=f.stem,
                    artifact_type="gguf",
                    path=str(f),
                    quantization=f.stem.split("-")[-1] if "-" in f.stem else "Q4_K_M",
                    filesize_bytes=f.stat().st_size if f.exists() else 0,
                    is_ready=True
                )
                self.artifacts[art.artifact_id] = art

        # Scan adapters
        adapter_dir = self.models_root / "adapters"
        if adapter_dir.exists():
            for d in adapter_dir.iterdir():
                if d.is_dir():
                    art = ModelArtifact(
                        artifact_id=d.name,
                        artifact_type="adapter",
                        path=str(d),
                        is_ready=True
                    )
                    self.artifacts[art.artifact_id] = art

    def get_artifact(self, artifact_id: str) -> Optional[ModelArtifact]:
        return self.artifacts.get(artifact_id)

    def list_gguf_models(self) -> List[ModelArtifact]:
        return [a for a in self.artifacts.values() if a.artifact_type == "gguf"]


default_model_registry = ModelRegistry()
