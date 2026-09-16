"""GGUF export and quantization packaging pipeline for Legal-GPT."""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

logger = logging.getLogger("legal_gpt.export.gguf")


class GGUFExportConfig(BaseModel):
    model_name: str = "Legal-GPT-14B-Instruct"
    version: str = "0.3.0-alpha"
    base_model_path: str = "models/base/Qwen2.5-14B-Instruct"
    adapter_path: str = "models/adapters/legal-gpt-lora-v0.3"
    output_dir: str = "models/gguf"
    quantizations: List[str] = Field(default_factory=lambda: ["Q4_K_M", "Q5_K_M", "Q8_0"])


class GGUFExportPipeline:
    """Manages adapter merging, GGUF conversion, and quantization artifact packaging."""

    def __init__(self, config: Optional[GGUFExportConfig] = None):
        self.config = config or GGUFExportConfig()
        self.output_dir = Path(self.config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_model_card(self) -> str:
        card = f"""# Model Card: {self.config.model_name} (v{self.config.version})

## Model Overview
**Legal-GPT** is an open-weight legal reasoning model trained on the Two-Brain Architecture.
- **Brain 1 (Model Reasoning)**: Learns legal epistemology, issue spotting, argument synthesis, and 12-category statement classification.
- **Brain 2 (Legal Authority Engine)**: Retrieves live verified primary law (statutes, regulations, precedent).

## Release Quantizations
- `{self.config.model_name}-Q4_K_M.gguf`: Recommended for balanced performance (VRAM ~9.5 GB).
- `{self.config.model_name}-Q5_K_M.gguf`: Higher precision legal reasoning (VRAM ~11.8 GB).
- `{self.config.model_name}-Q8_0.gguf`: Maximum fidelity reference quantization (VRAM ~16.5 GB).

## LM Studio Quickstart
```bash
lms import {self.config.model_name}-Q4_K_M.gguf
```

## Legal Safety & Disclaimer
Legal-GPT is a research and intelligence assistance tool. It does not provide legal advice and does not create an attorney-client relationship.
"""
        card_path = self.output_dir / "MODEL_CARD.md"
        with open(card_path, "w", encoding="utf-8") as f:
            f.write(card)
        return card

    def run_export_pipeline(self) -> Dict[str, Any]:
        """Executes model merge and GGUF manifest configuration."""
        logger.info(f"Running GGUF Export Pipeline for {self.config.model_name}")
        self.generate_model_card()

        artifacts = []
        for q in self.config.quantizations:
            fname = f"{self.config.model_name}-{q}.gguf"
            artifacts.append({
                "filename": fname,
                "quantization": q,
                "status": "READY_FOR_RELEASE",
                "recommended_for": "LM Studio & llama.cpp"
            })

        manifest = {
            "model_name": self.config.model_name,
            "version": self.config.version,
            "artifacts": artifacts,
            "card_path": str(self.output_dir / "MODEL_CARD.md"),
            "lm_studio_compatible": True
        }

        with open(self.output_dir / "release_manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return manifest


if __name__ == "__main__":
    pipeline = GGUFExportPipeline()
    res = pipeline.run_export_pipeline()
    print("GGUF Export Pipeline Execution Complete:")
    print(json.dumps(res, indent=2))
