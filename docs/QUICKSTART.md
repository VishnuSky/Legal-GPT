# Legal-GPT Quickstart Guide

Get Legal-GPT running standalone in under 2 minutes.

---

## 1. Installation

### Clone the Repository
```bash
git clone https://github.com/VishnuSky/Legal-GPT.git
cd Legal-GPT
```

### Install Dependencies
```bash
pip install -r requirements.txt
```
*(Requires Python 3.10 or higher)*

---

## 2. Start the Server (One Command)

### On Windows / PC1:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/start_legal_gpt.ps1
```
*(Automatically detects port availability and falls back to port 8001 if port 8000 is occupied by background services).*

### On Linux / macOS:
```bash
chmod +x scripts/start_legal_gpt.sh
./scripts/start_legal_gpt.sh
```

---

## 3. First Query (Shelter Care Hearing)

Run your first query against the progressive legal literacy endpoint:

```bash
curl -X POST http://localhost:8000/api/v1/public/explain-concept \
  -H "Content-Type: application/json" \
  -d '{
    "concept": "shelter_care_hearing",
    "jurisdiction": "WA",
    "level": 1
  }'
```

### Expected Output:
```json
{
  "concept": "Shelter Care Hearing (Initial Detention Hearing)",
  "jurisdiction": "WA",
  "disclaimer": "Legal information only. Not legal advice. Not a lawyer. Verify with qualified counsel.",
  "requested_level_text": "A shelter care hearing is the emergency court hearing that must take place immediately after child welfare workers take a child into state custody...",
  "available_levels": [1, 2, 3, 4, 5],
  "verification_status": "VERIFIED",
  "citations": [
    "RCW 13.34.065",
    "JuCR 2.4"
  ],
  "drill_down_actions": [
    "SHOW_SOURCE",
    "SHOW_STATUTE",
    "SHOW_CASE",
    "EXPLAIN_OPPOSING",
    "SHOW_TEMPORAL_CHANGE"
  ]
}
```

---

## 4. Interactive CLI Usage

Legal-GPT includes a comprehensive offline CLI:

```bash
# 1. Explain a legal concept (Levels 1 to 5)
python cli.py explain-concept --concept shelter_care_hearing --state WA --level 1

# 2. On-demand drill down (e.g. SHOW_STATUTE or SHOW_CASE)
python cli.py explain-concept --concept due_process --state WA --drill-down SHOW_STATUTE

# 3. Calculate procedural deadlines from primary statutes
python cli.py deadline --state WA --event emergency_removal --date 2026-09-17

# 4. Synthesize tactical questions for an attorney or caseworker
python cli.py questions --situation cps_removal --audience attorney --state WA

# 5. Explain a court document in Plain English
python cli.py explain-doc --type shelter_care_order --state WA --level 1

# 6. Audit a case timeline for procedural defects
python cli.py timeline --file events.json
```

---

## 5. LM Studio Integration

Legal-GPT integrates seamlessly with local models via LM Studio:

1. **Launch LM Studio:**
   - Download any open-weight GGUF model (e.g., Llama-3, Mistral, Qwen).
   - Start the Local Server in LM Studio on `http://localhost:1234/v1`.

2. **Configure Environment:**
   ```bash
   export LOCAL_LLM_URL="http://localhost:1234/v1"
   export LOCAL_LLM_MODEL="local-model"
   ```

3. **Run Query with Local Neural Reasoning:**
   ```bash
   python cli.py query "What are the shelter care hearing deadlines under Washington RCW 13.34.065?" --state WA
   ```

4. **Model Context Protocol (MCP) Setup:**
   Configure `api/mcp_server.py` in your LM Studio or Claude Desktop MCP config:
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
