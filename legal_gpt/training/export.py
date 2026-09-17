"""Export utilities for LoRA merging, Hugging Face checkpoint packaging, and GGUF quantization."""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger("legal_gpt.training.export")


class ModelExporter:
    """Coordinates merging adapters and generating GGUF quantization manifests."""

    @classmethod
    def create_export_manifest(
        cls,
        model_name: str,
        base_model: str,
        adapter_path: str,
        output_dir: str,
        quantizations: Optional[list] = None
    ) -> Dict[str, Any]:
        quants = quantizations or ["Q4_K_M", "Q5_K_M", "Q8_0"]
        manifest = {
            "model_name": model_name,
            "base_model": base_model,
            "adapter_path": adapter_path,
            "output_dir": output_dir,
            "quantizations": quants,
            "target_artifacts": [f"{model_name}-{q}.gguf" for q in quants],
            "lm_studio_ready": True,
            "status": "CONFIGURED"
        }
        out_path = Path(output_dir) / "export_manifest.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        return manifest
