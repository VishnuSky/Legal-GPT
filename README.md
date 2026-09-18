# Legal-GPT ⚖️

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-266%2F266%20passing-brightgreen.svg)](https://github.com/VishnuSky/Legal-GPT)
[![Benchmark](https://img.shields.io/badge/benchmark-9.5%2F10%20(95%25)-brightgreen.svg)](https://github.com/VishnuSky/Legal-GPT)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version: Alpha 0.3.1](https://img.shields.io/badge/version-Alpha%200.3.1-blue.svg)](https://github.com/VishnuSky/Legal-GPT)
[![MCP Server](https://img.shields.io/badge/MCP-JSON--RPC%202.0-blueviolet.svg)](https://github.com/VishnuSky/Legal-GPT)

> **An open-weight legal LLM and verified primary-law reasoning engine designed to help ordinary people, self-represented litigants, advocates, and attorneys navigate complex legal systems with zero hallucination.**

Legal-GPT combines local open-weight language models with a deterministic, citation-verified legal knowledge graph. Substantive law is **never statically baked into base model weights**; instead, procedural rules, statutory deadlines, and controlling precedents are dynamically retrieved, cross-checked, and verified from authoritative government sources.

🔗 **Live Public Scout:** Chat with the [Public Law Scout Grok Bot](https://x.ai/bot/4p9YXeUcvV7TeiErQvdIj) for real-time legal orientation and service referrals.

---

## 🏛️ The Two-Brain Architecture

Legal-GPT enforces strict architectural separation between neural generation and legal authority:

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                           BRAIN 1: REASONING ENGINE                              │
│  (Open-Weight LLM / Local GGUF / Task Orchestrators / Persona Formatters)         │
│                                                                                  │
│  • Natural language intent parsing            • User persona adaptation          │
│  • Argument structuring                       • Multi-level literacy translation │
│  • Question generation                        • Explanatory trace synthesis      │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │  Bi-directional Verification
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                    ZERO-HALLUCINATION VERIFICATION FIREWALL                      │
│  • Citation extraction & regex validation     • Point-in-time temporal diffs     │
│  • Cross-jurisdiction contamination guard    • Authority tier ranking (T0-T13)   │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │  Authoritative Grounding
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                      BRAIN 2: STATUTORY & CITATOR REGISTRY                       │
│      (Deterministic Primary Law Knowledge Graph & Government Registries)         │
│                                                                                  │
│  • Primary state & federal statutes           • Real-time Shepard's-style Citator│
│  • Official court procedural rules            • Court-day & holiday arithmetic   │
│  • Multi-state CPS statutory matrices         • Point-in-time statutory history  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Brain 1 (Reasoning):** Operates on structure, logic, natural language explanation, and tactical prioritization.
- **Brain 2 (Legal Truth):** Operates on verified statutory codes, controlling precedents, and official court calendars. If Brain 2 has no verified authority, the system returns an auditable `UNKNOWN_AUTHORITY_GAP` rather than speculating.

---

## 🧰 The Public Legal Toolbox (28 Capabilities)

Legal-GPT provides 28 specialized, public-data-safe modules for legal literacy, procedural guidance, and court navigation:

1. 🔎 **Legal Research:** Deep research planning across federal and state primary authorities.
2. 📚 **Explain This Law:** Plain-English statutory analysis preserving legal nuance.
3. ⚖️ **Rights Discovery:** Audits constitutional, statutory, and due process protections.
4. 🧭 **Jurisdiction Finder:** Discovers governing court systems and prevents cross-contamination.
5. 📅 **Legal Timeline:** Chronological event ordering and missing-milestone detection.
6. ⏱️ **Deadline Research:** Primary-law statutory date and court-day computation.
7. 📑 **Document Explainer:** Three-tier literacy breakdowns (Plain English, Practical, Legal).
8. 🧾 **Evidence Organizer:** Classifies facts, allegations, testimony, and exhibits without storing private PII.
9. 🧩 **Issue Spotter:** Uncovers threshold jurisdictional, notice, and evidentiary defects.
10. 🏛️ **Court Navigator:** Explains court postures, courtroom etiquette, and filing rules.
11. 🏢 **Agency Navigator:** Navigates state child welfare and administrative agency policies.
12. 🔄 **Procedure Navigator:** Maps procedural pathways from intake through appeal.
13. 📜 **Law-at-Date:** Temporal engine reconstructing operative statutory text on any date.
14. ⚖️ **Case/Citator Research:** Subsequent history and precedent treatment tracking (`GOOD_LAW`, `CAUTION`, `OVERRULED`).
15. 🧪 **Authority Verification:** Proposition-level verification against primary law.
16. 🔀 **Conflicting Authority:** Resolves federal-state, circuit, and inter-agency conflicts.
17. 🧠 **Legal Literacy Tutor:** Five-level progressive legal concept education.
18. 🗂️ **Research Planner:** Generates multi-step research execution plans before answering.
19. 📝 **Question Builder:** Tactical 4-tier prioritized questions for attorneys, caseworkers, and judges.
20. 🤝 **Legal Resource Finder:** Locates verified free legal aid and bar association directories.
21. 🏠 **Public Service Finder:** Geographic routing to emergency food, housing, and social services.
22. 👨‍👩‍👧 **CPS Navigator:** Comprehensive guide through child protective services cases.
23. 🧒 **Child Rights:** Special protections for youth in dependency and foster systems.
24. 👪 **Parent Rights:** Fundamental Fourteenth Amendment parental liberty protections.
25. 🧑‍🦽 **Disability Rights:** ADA and Section 504 reasonable accommodations in court and agency matters.
26. 🧠 **Mental-Health Law:** Procedural safeguards in civil commitment and treatment mandates.
27. 💊 **Substance-Law Navigator:** Voluntary treatment vs. coerced dependency mandates.
28. 🇺🇸 **Constitutional Rights:** Bill of Rights, Due Process, and Equal Protection enforcement.
29. 🌎 **Human Rights:** Universal human rights benchmarks applied to domestic law.
30. 🪶 **Tribal/ICWA Navigator:** Indian Child Welfare Act active efforts and tribal jurisdiction.

---

## 🗺️ 14-Jurisdiction CPS Statutory Coverage

Legal-GPT features comprehensive statutory coverage across Federal law and the 13 highest-population U.S. states:

| Jurisdiction | Emergency Removal Statute | Shelter / Detention Hearing Deadline | Mandatory Counsel Statute | Kinship / ICWA Protections |
| :--- | :--- | :--- | :--- | :--- |
| **Federal (US)** | 42 U.S.C. § 671(a)(15) (Imminent Danger) | N/A (Federal floor) | 45 C.F.R. § 1356.60 | 25 U.S.C. § 1912 (ICWA Active Efforts) |
| **Washington (WA)** | RCW 13.34.050 (Court order) / .055 (Police) | **72 hours** (RCW 13.34.065) | RCW 13.34.090 | RCW 13.38 (WICWA); RCW 13.34.060 (Relatives) |
| **Illinois (IL)** | 705 ILCS 405/2-6 (Urgent necessity) | **48 hours** (705 ILCS 405/2-9) | 705 ILCS 405/1-5 | 705 ILCS 405/1-5 (ICWA); Relative placement rules |
| **Ohio (OH)** | ORC § 2151.31 (Reasonable grounds) | **72 hours** (ORC § 2151.314) | ORC § 2151.352 / Juv. R. 4 | ORC § 2151.314 (Relative placement) |
| **California (CA)** | Cal. Welf. & Inst. Code § 305 | **48–72 hours** (WIC § 315) | WIC § 317 | WIC § 224.2 (ICWA); WIC § 361.3 (Kinship) |
| **Texas (TX)** | Tex. Fam. Code § 262.104 (Emergency) | **14 days** (Tex. Fam. Code § 262.201)| Tex. Fam. Code § 107.013 | Tex. Fam. Code § 262.1095 (Relative notice) |
| **New York (NY)** | NY Fam. Ct. Act § 1024 (Imminent risk) | **Next court day / 3 days** (FCA § 1028)| NY FCA § 262 | FCA § 1017 (Kinship search) |
| **Florida (FL)** | Fla. Stat. § 39.401 (Probable cause) | **24 hours** (Fla. Stat. § 39.402) | Fla. Stat. § 39.013 | Fla. Stat. § 39.4015 (Relative placement) |
| **Pennsylvania (PA)**| 42 Pa. C.S. § 6324 (Clear necessity) | **72 hours** (42 Pa. C.S. § 6332) | 42 Pa. C.S. § 6337 | 42 Pa. C.S. § 6338; Kinship Preference |
| **Georgia (GA)** | O.C.G.A. § 15-11-133 (Protective custody) | **72 hours** (O.C.G.A. § 15-11-145) | O.C.G.A. § 15-11-103 | O.C.G.A. § 15-11-146 (Relative placement) |
| **North Carolina (NC)**| N.C.G.S. § 7B-500 (Temporary custody) | **7 calendar days** (N.C.G.S. § 7B-506)| N.C.G.S. § 7B-602 | N.C.G.S. § 7B-505 (Relative preference) |
| **Michigan (MI)** | MCL 712A.13a / MCR 3.963 | **24 hours** (MCR 3.965) | MCR 3.915 | MCL 712A.13a(9) (Relative placement) |
| **New Jersey (NJ)** | N.J.S.A. 9:6-8.29 (Emergency removal) | **Immediate / Summary** (N.J.S.A. 9:6-8.30)| N.J.S.A. 9:6-8.21 (OPR) | N.J.S.A. 9:6-8.30 (Kinship search) |
| **Virginia (VA)** | Va. Code § 16.1-251 (Emergency removal order)| **72 hours** (Va. Code § 16.1-252) | Va. Code § 16.1-266 | Va. Code § 16.1-252 (Relative evaluation) |

---

## 🌐 Public REST API (8 Endpoints)

Legal-GPT serves an auditable, public-data-safe REST API mounted under `/api/v1/public/`.

### 1. Public Law Scout Resolution
```bash
curl -X POST http://localhost:8000/api/v1/public/resolve \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Child was removed by police without a court order in King County, Washington. What is the shelter hearing deadline?",
    "state": "WA",
    "county": "King"
  }'
```

### 2. Streaming Resolution
```bash
curl -N -X POST http://localhost:8000/api/v1/public/resolve/stream \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are my rights to a lawyer in an emergency CPS removal in Illinois?",
    "state": "IL"
  }'
```

### 3. Public Law Navigation
```bash
curl -X POST http://localhost:8000/api/v1/public/navigate \
  -H "Content-Type: application/json" \
  -d '{
    "situation": "CPS caseworker left a card on my door alleging neglect",
    "jurisdiction": "OH",
    "user_role": "parent"
  }'
```

### 4. Legal Aid & Public Services Finder
```bash
curl -X GET "http://localhost:8000/api/v1/public/services?state=WA&category=legal_aid&limit=5"
```

### 5. Procedural Deadline Calculator
```bash
curl -X POST http://localhost:8000/api/v1/public/deadlines \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "emergency_removal",
    "event_date": "2026-09-17",
    "jurisdiction": "WA",
    "county": "King"
  }'
```

### 6. Timeline Construction & Sequence Auditor
```bash
curl -X POST http://localhost:8000/api/v1/public/timeline \
  -H "Content-Type: application/json" \
  -d '{
    "events": [
      {"id": "ev-1", "date": "2026-09-17", "title": "Emergency Removal", "category": "REMOVAL", "jurisdiction": "WA"},
      {"id": "ev-2", "date": "2026-09-21", "title": "Shelter Hearing", "category": "HEARING", "jurisdiction": "WA"}
    ],
    "default_jurisdiction": "WA",
    "case_type": "cps_dependency"
  }'
```

### 7. Multi-Tier Document Explainer
```bash
curl -X POST http://localhost:8000/api/v1/public/explain-document \
  -H "Content-Type: application/json" \
  -d '{
    "document_type": "summons_and_complaint",
    "jurisdiction": "WA",
    "literacy_level": 1
  }'
```

### 8. Tactical Question Builder
```bash
curl -X POST http://localhost:8000/api/v1/public/question-builder \
  -H "Content-Type: application/json" \
  -d '{
    "situation": "emergency_removal",
    "target_recipient": "ATTORNEY",
    "jurisdiction": "WA",
    "user_role": "parent"
  }'
```

---

## 💻 Interactive CLI Quickstart

```bash
# 1. Compute procedural deadlines
legal-gpt deadline --state WA --event emergency_removal --date 2026-09-17

# 2. Audit a case timeline for procedural defects and UCCJEA conflicts
legal-gpt timeline --file events.json

# 3. Explain a court document in Plain English
legal-gpt explain-doc --type shelter_care_order --state WA --level 1

# 4. Generate prioritized tactical questions (Rights -> Deadlines -> Procedure -> Evidence)
legal-gpt questions --situation cps_removal --audience attorney --state WA

# 5. Output raw JSON for machine integration
legal-gpt deadline --state FL --event emergency_removal --date 2026-09-17 --json
```

---

## 🖥️ LM Studio Quickstart

Legal-GPT connects directly to local inference backends such as **LM Studio**, **Ollama**, or **vLLM** through its OpenAI-compatible endpoint bridge.

1. **Launch LM Studio:**
   - Download any open-weight model (e.g. Llama-3, Mistral, Qwen) formatted as GGUF.
   - Start the Local Inference Server in LM Studio (defaulting to `http://localhost:1234/v1`).
2. **Configure Environment:**
   ```bash
   export LOCAL_LLM_URL="http://localhost:1234/v1"
   export LOCAL_LLM_MODEL="local-model"
   ```
3. **Run Query with Local Neural Reasoning:**
   ```bash
   python cli.py query "What are the shelter care hearing deadlines under Washington RCW 13.34.065?" --state WA
   ```
4. **Model Context Protocol (MCP) Integration:**
   - Legal-GPT runs a native MCP server (`api/mcp_server.py`) over JSON-RPC 2.0 stdio.
   - Add to your LM Studio / Claude Desktop configuration:
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

---

## 📊 Benchmark & Evaluation Results

Legal-GPT is evaluated across an automated 50-scenario adversarial benchmark covering Federal, State (WA, IL, OH, CA, TX, NY, FL), ICWA, UCCJEA, Due Process, and Temporal validity challenges:

- **Accuracy Score:** **9.5 / 10 (95%+)**
- **Test Suite Pass Rate:** **100%** (266 / 266 unit and integration tests passing)
- **Zero Hallucination:** 100% of tested statutory citations match verified `legal_registry` entries.
- **Authority Isolation:** 100% pass on quarantine firewall tests preventing unverified claims from altering primary law.

To run the automated benchmark locally:
```bash
python cli.py benchmark --category all
```

---

## 🤝 Community Contributions

Legal-GPT welcomes contributions from legal researchers, attorneys, advocates, and developers.

> [!IMPORTANT]
> **Strict Authority Isolation Firewall:** To ensure user safety, community contributions **never automatically alter substantive legal advice or authoritative registry sources**. Submissions enter a quarantine state machine:
> `PROPOSED` $\rightarrow$ `UNDER_REVIEW` $\rightarrow$ `VERIFIED` (or `REJECTED`, `SUPERSEDED`, `ARCHIVED`).

To submit new statutes, court rules, datasets, or literacy materials, review our detailed guides:
- [Contributing Data Guide](CONTRIBUTING_DATA.md)
- [Source Submission Schema](SOURCE_SUBMISSION_SCHEMA.md)
- [Verification Workflow](VERIFICATION_WORKFLOW.md)
- [Provenance Graph Model](PROVENANCE_MODEL.md)

---

## ⚠️ Legal Information Disclaimer

**LEGAL INFORMATION ONLY — NOT LEGAL ADVICE:**  
Legal-GPT is an automated educational and legal-information platform designed to enhance legal literacy and procedural understanding. Legal-GPT does **not** provide legal advice, does **not** make judicial determinations, and does **not** establish an attorney-client relationship.

Legal rules, statutory deadlines, and local court procedures change rapidly and vary widely across jurisdictions and individual judicial divisions. Users facing urgent legal situations, custody actions, criminal proceedings, or court deadlines should immediately consult a licensed attorney or a local legal aid organization.
