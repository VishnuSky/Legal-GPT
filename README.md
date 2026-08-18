# Legal-GPT ⚖️

> **Compilation of Legal Datasets & Intelligence to provide Clients/Users with sound Legal Information and links to Services in their areas, bridging Legal Services with the GPT Archive to safeguard members of Society and Increase the Effectiveness of Future Matters Resolved.**

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

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Run Automated Verification Tests
```bash
pytest tests/ -v
```

### 3. Interactive CLI Queries
```bash
# Query a Washington State CPS scenario with jurisdiction locking
python cli.py query "CPS took my child without court order and held no hearing" --state WA --county Skagit

# Verify a legal citation against the canonical registry
python cli.py verify-citation "RCW 13.34.065"

# View Registry Summary
python cli.py registry-summary
```

### 4. Start Local REST API & MCP Server
```bash
uvicorn api.server:app --host 127.0.0.1 --port 8000 --reload
```

---

## 🛡️ License & Disclaimer
This software is designed for legal research, educational analysis, and document intelligence. It does **not** constitute legal advice.
