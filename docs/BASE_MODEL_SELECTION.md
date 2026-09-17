# Base Model Selection & Architecture Specification

## 1. Selected Base Model

**`Qwen/Qwen2.5-14B-Instruct`**

- **Developer**: Alibaba Cloud / Qwen Team
- **Parameter Count**: 14.7 Billion
- **Architecture**: `Qwen2ForCausalLM` (Transformer decoder with Grouped Query Attention)
- **Native Context Window**: 128k tokens (Fine-tuning target: 8,192 – 32,768 tokens)
- **License**: **Apache 2.0** (Fully permissive for commercial use, fine-tuning, and open-weight distribution)

---

## 2. Selection Rationale & Evaluation Criteria

### A. License & Commercial Redistribution
- **Apache 2.0 Compliance**: Unlike models with restrictive commercial clauses (e.g., Llama 3.1's 700M monthly active user threshold or Gemma's specific commercial terms), Qwen 2.5 is released under a clean, unrestricted Apache 2.0 license.
- **Open-Weight Derivative Distribution**: Allows the Legal-GPT project to release merged model weights and GGUF quantization files publicly without legal licensing constraints.

### B. Two-Brain Reasoning Alignment
- **Reasoning Density**: Legal analysis requires nuanced, multi-step statutory interpretation, issue identification, and epistemic statement classification. At 14.7B parameters, Qwen 2.5 demonstrates significantly higher deductive reasoning and instruction-following fidelity than 7B/8B models, while remaining orders of magnitude faster and more cost-effective to fine-tune than 70B+ models.
- **Dynamic Authority Offloading**: Because Legal-GPT utilizes a **Two-Brain Architecture**, the base model does not need to memorize millions of statutory sections in its weights. Instead, 14B parameters provide optimal capacity for mastering:
  1. 12-category legal statement epistemology
  2. Issue spotting and statutory element extraction
  3. IRAC / CRAC argument structuring
  4. Uncertainty quantification and explicit abstention triggers

### C. GGUF Quantization & Local Hardware Accessibility
The 14B parameter footprint provides ideal memory efficiency for local and edge execution across standard consumer hardware:

| Quantization Type | Memory Footprint (VRAM / RAM) | Target Hardware | Recommended Runtime |
| :--- | :--- | :--- | :--- |
| **Q4_K_M** | **~9.5 GB** | Single 12 GB GPU (RTX 3060 / 4060 / 4070) or Apple Silicon (16 GB Unified) | LM Studio, llama.cpp, Ollama |
| **Q5_K_M** | **~11.8 GB** | 16 GB GPU (RTX 4080 / T4 / V100) or Apple Silicon (18+ GB Unified) | LM Studio, vLLM |
| **Q8_0** | **~16.5 GB** | 24 GB GPU (RTX 3090 / 4090 / A10G) or High-Memory Mac (32+ GB) | llama.cpp, Local High-Precision Server |

### D. LoRA / QLoRA Training Compatibility
- **Target Modules**: `["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]`
- **Recommended Hyperparameters**:
  - **Rank ($r$)**: 64
  - **Alpha ($\alpha$)**: 128
  - **Dropout**: 0.05
  - **Learning Rate**: $2 \times 10^{-4}$ (Cosine schedule with warmup)
  - **Precision**: 4-bit NF4 with double quantization (QLoRA) or bfloat16 LoRA
- **Tooling Support**: Fully supported out-of-the-box in HuggingFace PEFT, TRL, vLLM, and standard fine-tuning frameworks.

---

## 3. Candidate Model Comparison Matrix

| Candidate Model | Parameter Size | License | Multi-Step Reasoning | Structured JSON / Tool Calling | Quantized VRAM (Q4) | Selection Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Qwen2.5-14B-Instruct** | **14.7B** | **Apache 2.0** | **Exceptional** | **Exceptional** | **~9.5 GB** | **SELECTED (Primary)** |
| *Llama-3.1-8B-Instruct* | 8.0B | Custom Community | Moderate | Good | ~5.8 GB | Strong fallback for <8GB devices; lower complex statutory reasoning depth. |
| *Mistral-NeMo-12B* | 12.2B | Apache 2.0 | Good | Moderate | ~8.2 GB | Good license, but weaker JSON schema and tool-call reliability in legal workflows. |
| *DeepSeek-R1-Distill-Qwen-14B* | 14.7B | MIT | Exceptional | Variable | ~9.5 GB | Excellent for pure chain-of-thought, but over-generates verbose thinking tokens that complicate strict JSON MCP tools. |
| *Gemma-2-9B / 27B* | 9.2B / 27.2B | Gemma Terms | Good | Moderate | ~6.5 GB / ~18 GB | Sliding window attention adds complexity in certain llama.cpp GGUF quantizations; 27B exceeds standard 16GB GPUs. |

---

## 4. Manifest Lock & Configuration Verification

The base model is locked in the model manifest (`models/manifests/legal_gpt_manifest.yaml`):

```yaml
model:
  name: Legal-GPT
  version: 0.3.0-alpha
  family: legal-instruct
  language: en-US
  base_model:
    name: "Qwen/Qwen2.5-14B-Instruct"
    architecture: "Qwen2ForCausalLM"
    parameters: "14.7B"
    context_length: 32768
    license: "Apache-2.0"
```

And initialized in the SFT training pipeline config (`training/train_sft.py`):
```python
class TrainingConfig(BaseModel):
    base_model_name: str = "Qwen/Qwen2.5-14B-Instruct"
    lora_r: int = 64
    lora_alpha: int = 128
    lora_dropout: float = 0.05
    target_modules: list = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    learning_rate: float = 2e-4
    max_seq_length: int = 8192
    output_dir: str = "models/checkpoints/legal-gpt-14b-alpha"
    use_qlora_4bit: bool = True
```
