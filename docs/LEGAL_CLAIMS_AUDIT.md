# Legal-GPT Public Legal Claims & Safety Audit

**Date:** 2026-09-18  
**Branch:** `feat/literacy-model-v1`  
**Purpose:** Formal audit and classification of public documentation claims regarding accuracy, verification, architecture, and safety.  

---

## 1. Classification Methodology

Each public claim is evaluated and assigned one of five audit classifications:
- **`IMPLEMENTATION-SUPPORTED`**: The claim is directly enforced and verified by deterministic code paths in the repository.
- **`PARTIALLY-SUPPORTED`**: The core mechanism exists, but the public claim oversimplifies edge cases or lacks qualifications.
- **`BENCHMARK-LIMITED`**: The claim holds true only within the boundaries of the specific 50-scenario test suite, not as a universal guarantee.
- **`OVERSTATED`**: The claim exceeds technical reality (e.g. mathematical impossibility of hallucinations or proprietary system parity).
- **`UNVERIFIED`**: The claim lacks empirical telemetry or programmatic enforcement in the codebase.

---

## 2. Claim Inventory & Classification

| # | Public Claim Statement | Document Source | Audit Classification | Analysis & Required Correction |
|:---|:---|:---|:---:|:---|
| 1 | *"navigate complex legal systems with zero hallucination"* | `README.md` (Line 10) | **OVERSTATED** | Neural LLMs cannot mathematically guarantee zero hallucination. The architecture is **verification-gated** and **abstention-first**, rejecting or flagging citations that do not match `legal_registry`. Language must be corrected from *"zero hallucination"* to *"verification-gated, citation-verified where supported"*. |
| 2 | *"ZERO-HALLUCINATION VERIFICATION FIREWALL"* | Multiple docs / reports | **OVERSTATED** | While the symbolic engine filters and rejects unverified citations, calling it an impenetrable "zero-hallucination firewall" creates false reliance for self-represented litigants. Replace with *"Authority Verification & Quarantine Gate"*. |
| 3 | *"Real-time Shepard's-style Citator"* | `README.md` (Line 44) | **OVERSTATED** | Legal-GPT implements an internal relational precedent treatment graph (`knowledge_graph/relational_graph.py`). It does not possess access to LexisNexis's proprietary Shepard's® service. Must be corrected to *"citator-style authority treatment graph"*. |
| 4 | *"9.5 / 10 (95%+) accuracy"* | `README.md` (Line 264) | **BENCHMARK-LIMITED** | This score reflects the 50-scenario adversarial benchmark suite in `evaluation/`, not universal accuracy across all U.S. legal domains. Documentation must state the exact benchmark population (50 synthetic adversarial cases) and test conditions. |
| 5 | *"100% zero hallucination on citations"* | `README.md` (Line 266) | **BENCHMARK-LIMITED** | 100% of citations in the included benchmark matched registry keys. In freeform generation without verification gating, the underlying model can still hallucinate. Must state: *"100% citation verification pass rate across the 50 included benchmark scenarios."* |
| 6 | *"Substantive law is never statically baked into base model weights"* / *"Model = Reasoning / Database = Law"* | `ARCHITECTURE.md` & `README.md` | **PARTIALLY-SUPPORTED** | Open-weight foundation models (e.g. Qwen, Llama) inherently memorize legal tokens and doctrines during pretraining. What the architecture enforces is that the system prompt and runtime tools **ground conclusions strictly in retrieved registry texts**, refusing to treat model weight memory as authoritative. Must clarify: *"Substantive authoritative legal text is retrieved dynamically from verified repositories; the neural model serves solely as a language and reasoning engine, not as an unverified source of law."* |
| 7 | *"The Public Legal Toolbox (28 Capabilities)"* | `README.md` (Line 55) | **OVERSTATED** | The section header claims 28 capabilities, but the actual numbered list itemizes 30 distinct modules (running from 1 to 30). The heading and text must be updated to 30 to match reality. |
| 8 | *"14-Jurisdiction CPS Statutory Coverage Table"* | `README.md` (Line 92) | **IMPLEMENTATION-SUPPORTED** | Verified in `legal_registry/cps/` for WA, IL, OH, CA, TX, NY, FL, PA, GA, NC, MI, NJ, VA, and Federal/ICWA. Supported by `tests/test_expanded_cps_states.py`. |
| 9 | *"8 Public API Endpoints with Example Curl Commands"* | `README.md` (Line 115) | **IMPLEMENTATION-SUPPORTED** | All 8 public endpoints (`/resolve`, `/services`, `/research-plan`, `/deadlines`, `/timeline`, `/explain-document`, `/question-builder`, `/mcp`) exist in `api/server.py` and are tested by test suites. |
| 10 | *"Test Suite Pass Rate: 100% (266 / 266 tests)"* | `README.md` (Line 265) | **PARTIALLY-SUPPORTED** | Stale metric. As of Alpha 0.3.2, the full test suite contains 275 passing tests (275/275). Documentation should reflect current test counts. |
| 11 | *"Cryptographic provenance: SHA-256 makes storage immutable"* | `PROVENANCE_MODEL.md` | **PARTIALLY-SUPPORTED** | SHA-256 hashes provide cryptographic integrity verification and tamper detection. SHA-256 alone does not make a filesystem or database immutable without write-once physical media or distributed consensus. Correct phrasing to *"cryptographically verifiable tamper-evident artifact tracking"*. |
| 12 | *"Numeric authority tiers (T0-T8) establish universal bindingness"* | `core/citator/` docs | **PARTIALLY-SUPPORTED** | Numeric authority tiers are internal ranking heuristics for search and prompt construction. They are metadata, not formal judicial declarations of bindingness across all procedural postures. |

---

## 3. Required Language & Framing Rules

To maintain absolute public safety and transparency:

1. **Zero Hallucination Claims:**  
   Never state or imply that Legal-GPT has solved hallucination mathematically. Always use:
   - *"verification-gated"*
   - *"citation-verified where supported"*
   - *"abstention-first architecture"*
   - *"authority-grounded"*
   - *"tested against the included benchmark suite"*

2. **Benchmark Reporting:**  
   Always qualify accuracy metrics by defining the evaluation set: *"Scored 9.5/10 across the 50-scenario adversarial benchmark suite under controlled evaluation conditions."*

3. **Citator Terminology:**  
   Avoid referencing proprietary commercial services. Use *"citator-style authority treatment graph"* or *"subsequent history relational graph"*.

4. **Two-Brain Representation:**  
   Accurately describe that while base LLMs possess latent training weights, Legal-GPT's symbolic engine acts as a strict verification layer that rejects ungrounded claims.

5. **Literacy Module Inheritance:**  
   The Legal Literacy Model (`core/literacy/`) must strictly inherit these verification constraints. Level 4 citations must be classified as `VERIFIED`, `UNVERIFIED`, or `ABSTAIN`, and never dynamically synthesize placeholder citations.
