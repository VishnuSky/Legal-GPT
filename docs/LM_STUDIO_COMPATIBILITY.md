# LM Studio & Local Runtime Compatibility Guide

**Version**: Alpha 0.3.2  
**Supported Runtimes**: LM Studio, llama.cpp, Ollama, vLLM  
**API Endpoints**: 9 Public Endpoints (`/api/v1/public/*`)  
**MCP Server**: JSON-RPC 2.0 (`api/mcp_server.py`) & Public HTTP/SSE (`api/mcp_public.py`)

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
Legal information only. Not legal advice. No attorney-client relationship.
<|im_end|>
<|im_start|>user
What is the mandatory shelter care hearing timeline in Washington state after an emergency removal?
<|im_end|>
<|im_start|>assistant
```

---

## 3. Two-Brain Architecture Integration with LM Studio

Legal-GPT connects with LM Studio in two bi-directional ways:

### Mode A: Legal-GPT Calls Local LM Studio
When running Legal-GPT orchestrators with a local neural engine:
1. Start LM Studio Local Inference Server on `http://localhost:1234/v1`.
2. Configure Legal-GPT environment:
   ```bash
   export LOCAL_LLM_URL="http://localhost:1234/v1"
   export LOCAL_LLM_MODEL="local-model"
   ```
3. Run queries through Legal-GPT CLI:
   ```bash
   python cli.py query "What are the shelter care hearing deadlines under RCW 13.34.065?" --state WA
   ```

### Mode B: LM Studio / Client Calls Legal-GPT Tools (MCP)
1. Configure Legal-GPT MCP server in client settings (`claude_desktop_config.json` or LM Studio tool configs):
   ```json
   {
     "mcpServers": {
       "legal-gpt": {
         "command": "python",
         "args": ["-m", "api.mcp_server"]
       }
     }
   }
   ```
2. Alternatively, connect via HTTP MCP endpoint:
   ```text
   http://localhost:8000/mcp/v1/tools
   ```
3. Available tools:
   - `lookup_public_law`: Retrieves verified statutory authority packages.
   - `explain_concept`: Progressive 5-level legal concept explanations.
   - `lookup_services`: Official legal aid and court self-help registry.
   - `get_deadlines`: Statutory date and court-day deadline calculator.

---

## 4. REST API Endpoint Mapping

When running Legal-GPT alongside LM Studio, the following 9 public endpoints are available on `http://localhost:8000/api/v1/public/` (or port 8001 if port 8000 is occupied):

| Endpoint | Method | Function |
|:---|:---|:---|
| `/resolve` | POST | Single-turn legal resolution with controlling statutory citations |
| `/resolve/stream` | POST | Streaming ndjson resolution across 6 reasoning stages |
| `/navigate` | POST | 16-section legal roadmap and procedural pathways |
| `/services` | GET | Official civil legal aid, court self-help, and public assistance |
| `/deadlines` | POST | Statutory date and court-day procedural deadline calculation |
| `/timeline` | POST | Chronological event sequencing and procedural defect audit |
| `/explain-document` | POST | Multi-tier legal document explanations (Plain, Practical, Legal) |
| `/question-builder` | POST | Tactical prioritized questions for attorneys, caseworkers, judges |
| `/explain-concept` | POST | 5-level progressive legal concept breakdown and drill-downs |

---

## 5. Verification Checklist
- [x] Model loads successfully in LM Studio
- [x] ChatML template formatting compliant
- [x] JSON structured citation extraction verified
- [x] Fast token generation (>40 tok/sec on modern GPUs)
- [x] Verification-gated authority retrieval (abstention on unknown law)
- [x] Zero private data leakage
