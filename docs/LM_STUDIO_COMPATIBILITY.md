# LM Studio & Local Runtime Compatibility Guide

**Model**: Legal-GPT-14B-Instruct (v0.3.0-alpha)  
**Supported Runtimes**: LM Studio, llama.cpp, Ollama, vLLM

---

## 1. Quick Import & Setup

### LM Studio CLI Import
```bash
lms import models/gguf/Legal-GPT-14B-Instruct-Q4_K_M.gguf
```

### Loading Preset Settings in LM Studio UI
- **Context Length**: `32768` (minimum `8192` for multi-statute reasoning)
- **Temperature**: `0.1` to `0.2` (Strict deterministic legal reasoning)
- **Top P**: `0.95`
- **GPU Acceleration**: Offload all 48 layers to VRAM (~9.5 GB for `Q4_K_M`)
- **Stop Sequences**: `<|im_end|>`, `[END MISSION]`

---

## 2. Recommended Prompt Format (ChatML)

```text
<|im_start|>system
[MISSION]
Legal-GPT is a jurisdiction-aware legal reasoning system.
[LEGAL EPISTEMOLOGY — STATEMENT CLASSIFICATION]
Classify statements: FACT | LAW | PRECEDENT | INTERPRETATION | INFERENCE | ALLEGATION | ARGUMENT | COUNTERARGUMENT | POLICY | OPINION | UNCERTAINTY | UNKNOWN
[LEGAL SAFETY]
Not legal advice. No attorney-client relationship.
<|im_end|>
<|im_start|>user
What is the mandatory shelter care hearing timeline in Washington state after an emergency removal?
<|im_end|>
<|im_start|>assistant
```

---

## 3. Two-Brain Architecture Integration with LM Studio

When using Legal-GPT as an MCP server with LM Studio:
1. LM Studio sends user prompt to Legal-GPT MCP tool `lookup_public_law`.
2. Legal-GPT retrieves verified Legal Authority Packages from Brain 2.
3. LM Studio model reasons over structured package and formats the 11-section response.
4. Response is verified through `FinalReviewAgent` for zero hallucination.

---

## 4. Verification Checklist
- [x] Model loads successfully in LM Studio
- [x] ChatML template formatting compliant
- [x] JSON structured citation extraction verified
- [x] Fast token generation (>40 tok/sec on modern GPUs)
- [x] Zero private data leakage
