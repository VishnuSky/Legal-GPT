# Legal-GPT ⚖️

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/VishnuSky/Legal-GPT)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version: v0.1.1](https://img.shields.io/badge/version-0.1.1-green.svg)](https://github.com/VishnuSky/Legal-GPT)

> **Compilation of Legal Datasets & Intelligence to provide Clients/Users with sound Legal Advice and links to Services in their areas, bridging Legal Services with the GPT Archive to safeguard members of Society and Increase the Effectiveness of Future Matters Resolved.**

**A Jurisdiction-Aware, Temporal, Citation-Verified Legal Intelligence Platform for Local AI & Child Welfare (CPS) Case Work.**

---

## 🏛️ Core Principles & Architecture
1. **Model = Reasoning, Database = Law**: Law is never trained statically into the base model weights. Instead, legal authority is retrieved, versioned, and verified from authoritative government sources.
2. **Strict Authority Hierarchy (Tiers 0–5)**:
   - **Tier 0**: Official statutory code, state/federal constitutions, official regulations, official court slip opinions.
   - **Tier 1**: CourtListener, Harvard Caselaw Access Project (CAP), GovInfo, Congress.gov, BIA/ICWA.
   - **Tier 2**: American Bar Association (ABA), State Bar Associations, Legal Aid.
   - **Tier 3**: Secondary legal treatises (Cornell LII, Justia, FindLaw).
   - **Tier 4**: Law firm articles & legal commentary.
   - **Tier 5**: Social forums & ungrounded LLMs (*strictly barred from serving as legal authority*).
3. **Temporal Law Engine**: Computes and retrieves the statute or policy version valid and in effect on the exact historical date of a case event (`law_effective_on(event_date)`).
4. **Jurisdiction Lock & Contamination Guard**: Prevents cross-jurisdiction legal errors (e.g. asserting Washington RCW in an Illinois matter).
5. **Zero-Hallucination Citation Verification**: Every citation candidate is resolved against canonical legal source registries before reaching the user.
6. **CPS / Child Welfare Launch Vertical**: Specialized deep domain models for **Federal (CAPTA, Title IV-E, ICWA, ASFA, FFPSA)**, **Washington (RCW 13.34, RCW 26.44, DCYF policies)**, **Illinois (705 ILCS 405, 325 ILCS 5, DCFS guides)**, and **Ohio (ORC Chapter 2151, ODJFS rules)**.

---

## 📁 Repository Layout

```
Legal-GPT/
├── configs/
│   ├── settings.yaml                 # Core configuration (LLMs, storage, CPS thresholds)
│   └── authority_tiers.yaml          # Authority scoring definitions (Tier 0 to 5)
├── legal_registry/                   # Machine-readable legal source registry v1.0
│   ├── schemas/                      # Pydantic models for sources, CPS, and courts
│   ├── federal/                      # GovInfo, US Code, CFR, Fed Register, CourtListener, BIA
│   ├── states/
│   │   ├── matrix.yaml               # Complete 50-State + DC + Territories matrix
│   │   ├── WA.yaml                   # Deep Washington source registry
│   │   ├── IL.yaml                   # Deep Illinois source registry
│   │   └── OH.yaml                   # Deep Ohio source registry
│   ├── cps/                          # Specialized child welfare statutory & policy registries
│   └── courts/                       # Federal & State Court hierarchy with CourtListener IDs
├── normalization/                    # Canonical Document, Chunk, and Citation models
├── core/                             # Authority, Jurisdiction Lock, Temporal, & Citation Verifier
├── cps/                              # 18-stage CPS lifecycle, Parent Rights, ICWA, & UCCJEA
├── storage/                          # SQLite metadata DB, Hybrid BM25/Vector store, Knowledge Graph
├── agents/                           # Intake classifier, Orchestrator, & 34-point Response Formatter
├── api/                              # FastAPI REST endpoints & Model Context Protocol (MCP) server
├── cli.py                            # Interactive CLI tool
└── tests/                            # Automated test suite
```

---

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/VishnuSky/Legal-GPT.git
cd Legal-GPT

# Create and activate a virtual environment (recommended)
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On macOS / Linux:
source .venv/bin/activate

# Install in editable mode
pip install -e .
```

### 2. Run Automated Verification Tests
```bash
pytest tests/ -v
```

### 3. Interactive CLI Queries
```bash
# Query statutory procedures, notice requirements, and hearing deadlines in Washington State
python cli.py query "What are the statutory notice requirements and hearing deadlines for emergency temporary custody under dependency procedure?" --state WA --county Skagit

# Query child welfare procedure with an event date for temporal law validation
python cli.py query "What statutory standards apply for administrative review and shelter care hearings?" --state IL --county Cook --event-date 2025-06-15

# Evaluate ICWA compliance, active efforts, and tribal notice requirements
python cli.py query "What are the required legal standards for ICWA inquiry, active efforts, and designated tribal notice?" --state WA

# Verify a legal citation against the canonical registry
python cli.py verify-citation "RCW 13.34.065"

# View Registry Summary across federal, state, tribal, and territorial domains
python cli.py registry-summary
```

### 4. Start Local REST API & MCP Server
```bash
uvicorn api.server:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation and interactive Swagger UI are available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## 📊 Current Capabilities & Roadmap

| Feature Area | Current Status (v0.1.1) | Upcoming Milestones |
|---|---|---|
| **50-State Legal Matrix** | Full metadata matrix for all 50 states + DC | Automated daily scrapers for all 50 state legislative portals |
| **CPS Deep Vertical** | WA, IL, OH + Federal statutory & policy coverage | Expansion to CA, TX, FL, NY, PA, MI |
| **Citation Verification** | Exact match against canonical registry & statutory patterns | Live CourtListener / GovInfo API verification fallback |
| **Temporal Law Engine** | `law_effective_on(date)` validity & repeal tracking | Full text historical diff viewer |
| **Parent Rights Engine** | Automated audit for notice, counsel, and reasonable efforts | State-specific pattern motion generator |
| **Inference Backends** | LM Studio, Ollama, OpenWebUI REST endpoints & MCP server | Fine-tuned LoRA models for structured legal reasoning |

---

## 🛡️ License & Disclaimer
This software is provided under the [MIT License](LICENSE).

> **IMPORTANT LEGAL DISCLAIMER**: This software is designed and provided for **legal research, educational, and document intelligence purposes only**. It does **not** constitute legal advice, does **not** create an attorney-client relationship, and must **never** be used as a substitute for competent advice from a licensed attorney admitted to practice in the relevant jurisdiction.
