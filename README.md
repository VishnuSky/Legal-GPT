# Legal-GPT ⚖️

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-100%25%20passing-brightgreen.svg)](https://github.com/VishnuSky/Legal-GPT)
[![Benchmark](https://img.shields.io/badge/benchmark-50%2F50%20(100%25)-brightgreen.svg)](https://github.com/VishnuSky/Legal-GPT)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version: v1.0.0](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/VishnuSky/Legal-GPT)
[![MCP Server](https://img.shields.io/badge/MCP-JSON--RPC%202.0-blueviolet.svg)](https://github.com/VishnuSky/Legal-GPT)

> **Compilation of Legal Datasets & Intelligence to provide Clients/Users with sound Legal Advice and links to Services in their areas, bridging Legal Services with the GPT Archive to safeguard members of Society and Increase the Effectiveness of Future Matters Resolved.**

**A Jurisdiction-Aware, Temporal, Citation-Verified Legal Intelligence Platform for Local AI & Child Welfare (CPS) Case Work.**

---

## 🏛️ Core Principles & Architecture
1. **Model = Reasoning, Database = Law**: Law is never trained statically into base model weights. Instead, legal authority is dynamically retrieved, versioned, and verified from authoritative government sources.
2. **14-Level Dynamic Authority Hierarchy (T0–T13)**:
   - **T0–T5**: Federal Constitution, U.S. Code Statutes (ICWA, Title IV-E), C.F.R., SCOTUS Precedents (*Haaland*, *Santosky*, *Troxel*), Federal Circuit & District Opinions.
   - **T6–T11**: State Constitutions, Primary State Codes (RCW, ILCS, ORC, WIC, Tex. Fam. Code, FCA), Administrative Codes, State Supreme Court & Appellate Precedents, Court Rules (JuCR, Juv. R., CRC).
   - **T12–T13**: Agency Policy Manuals (DCYF, DCFS, ODJFS, CDSS, DFPS, OCFS) & Secondary Treatises.
3. **Point-in-Time Law Engine (`LAW_AT_DATE`)**: Computes the exact operative statutory text in effect on any historical date, complete with line-by-line legislative text diffs.
4. **Relational Citator Engine**: Shepard's / KeyCite-style subsequent treatment tracking (`GOOD_LAW`, `CAUTION`, `NEGATIVE`, `NEUTRAL`).
5. **Jurisdiction Lock & Anti-Contamination Guard**: Prevents cross-jurisdiction legal errors (e.g. citing Washington RCW in an Illinois proceeding).
6. **Multi-Stage Proposition Verifier**: Enforces zero-hallucination verification with explicit abstention state machine (`SUPPORTED`, `CONTRADICTED`, `OUTDATED_AUTHORITY`, `JURISDICTION_MISMATCH`, etc.).
7. **Adversarial Reviewer & 4 Persona Modes**: Simulates opposing counsel challenges and renders outputs for *Self-Represented Parents*, *Investigators*, *Attorneys*, or *Judicial Reviewers*.
8. **CPS / Child Welfare Launch Vertical**: Full 14-stage life-cycle modeling across Federal, WA, IL, OH, CA, TX, NY, and Tribal jurisdictions.

---

## 📁 Repository Layout

```
Legal-GPT/
├── configs/                          # Core configuration & authority tiers
├── legal_registry/                   # Machine-readable legal source registry v1.0
│   ├── federal/                      # GovInfo, US Code, CFR, CourtListener, BIA/ICWA
│   ├── states/                       # 50-State + DC + Territories matrix (deep WA, IL, OH, CA, TX, NY)
│   ├── cps/                          # Specialized child welfare statutory & policy registries
│   └── courts/                       # Federal & State Court hierarchy
├── core/                             # Authority, Temporal, Citation Verifier, Local LLM & Procedure Engines
├── cps/                              # Evidence Matrix, Bridge, Pleading Generator & Due Process Auditor
├── knowledge_graph/                  # Relational Citator Graph & Point-in-Time Diff Engine
├── normalization/                    # Canonical Document, Chunk, and Citation schemas
├── storage/                          # SQLite metadata DB, Hybrid BM25/Vector store
├── agents/                           # Legal Orchestrator, Adversarial Reviewer, Persona Renderers
├── api/                              # FastAPI REST endpoints, OpenWebUI Pipeline & MCP Server
├── benchmarks/                       # 50-Scenario Multi-Jurisdiction Benchmark Suite
├── docs/                             # Architecture & Deployment Guides
├── scripts/                          # Privacy, security & data isolation audit scanners
├── cli.py                            # Interactive CLI tool
└── tests/                            # Comprehensive 100+ automated test suite
```

---

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/VishnuSky/Legal-GPT.git
cd Legal-GPT

# Install in editable mode
pip install -e .
```

### 2. Run Verification Tests & 50-Scenario Benchmark
```bash
pytest -v
python cli.py benchmark --category all
```

---

## 💻 Interactive CLI Tool

```bash
# 1. Query a legal inquiry with jurisdiction locking and citation verification
python cli.py query "What are the statutory notice requirements for emergency temporary custody?" --state WA

# 2. Query child welfare procedure with temporal event date
python cli.py query "What statutory standards apply for shelter care?" --state IL --event-date 2024-01-01

# 3. Inspect subsequent treatment and citing precedents (Citator)
python cli.py citator "Haaland v. Brackeen"
python cli.py citator "RCW 13.34.065"

# 4. Resolve Point-in-Time statutory text and line-by-line diffs
python cli.py law-at-date "RCW 13.34.065" --date 2015-01-01 --diff-with 2024-01-01

# 5. Generate formal state-specific court motions and pleadings
python cli.py generate-motion --state WA --motion shelter_rehearing
python cli.py generate-motion --state NY --motion section_1028

# 6. Audit 7-pillar constitutional and statutory due process health
python cli.py due-process-audit --state WA --no-notice --no-counsel --icwa

# 7. Evaluate evidentiary matrix (Fact vs Allegation vs Documented Exhibit)
python cli.py evaluate-evidence --jurisdiction US-WA

# 8. Start Model Context Protocol (MCP) JSON-RPC stdio server
python cli.py mcp

# 9. Start FastAPI REST Server
python cli.py serve --host 127.0.0.1 --port 8000
```

---

## 🔌 Local AI & Tool Integration

- **Model Context Protocol (MCP)**: Native integration for LM Studio, Claude Desktop, and local AI nodes (`api/mcp_server.py`).
- **OpenWebUI Pipeline**: Drop-in custom pipeline for OpenWebUI chat interfaces (`api/openwebui_pipeline.py`).
- **Local Inference Support**: Connects to LM Studio, Ollama, vLLM, and llama.cpp via OpenAI-compatible endpoints with deterministic offline fallback (`core/local_llm.py`).

For full setup instructions, see the [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) and [System Architecture](docs/ARCHITECTURE.md).

---

## 🛡️ Public Repository Security & Data Isolation Policy

Legal-GPT is a strictly isolated public repository. No private case files, personal identifying information (PII), proprietary datasets, credentials, evidence files, or data from other projects are ever permitted in this codebase.

- **Master Policy**: [`PUBLIC_DATA_POLICY.md`](PUBLIC_DATA_POLICY.md)
- **Security Policy**: [`SECURITY.md`](SECURITY.md)
- **Privacy Audit Scanners**: `scripts/privacy_audit.py` & `scripts/deep_security_audit.py`

---

## 📄 License
MIT License. Copyright (c) 2026 VishnuSky / Legal-GPT Contributors.
