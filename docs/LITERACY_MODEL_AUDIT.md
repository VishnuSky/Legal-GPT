# Legal Literacy Model: Initial Audit & Inventory

**Date:** 2026-09-18  
**Branch:** `feat/literacy-model-v1`  
**Audit Scope:** `core/literacy/`, related tests, API routes, CLI commands, and statutory grounding in `legal_registry`.  

---

## 1. Module Inventory

### 1.1 `core/literacy/`
- **`__init__.py`** (661 B): Exports `LiteracyLevel`, `DrillDownAction`, `PrimaryAuthorityReference`, `DrillDownResult`, `LegalConceptExploration`, `LegalLiteracyEngine`, and `LiteracyRenderer`.
- **`models.py`** (2.88 KB): Defines Pydantic models and Enums.
  - `LiteracyLevel` (Levels 1 to 5).
  - `DrillDownAction` (5 actions: `SHOW_SOURCE`, `SHOW_STATUTE`, `SHOW_CASE`, `EXPLAIN_OPPOSING`, `SHOW_TEMPORAL_CHANGE`).
  - `PrimaryAuthorityReference` (citation, source_type, official_portal_url, key_holding_or_text, jurisdiction, is_binding).
  - `DrillDownResult` (action, title, content, citations, official_sources).
  - `LegalConceptExploration` (5 level fields + drill_downs map).
- **`registry.py`** (26.37 KB): Contains static `CANONICAL_CONCEPTS` dictionary and `LegalConceptRegistry`. Implements `_synthesize_concept` fallback for unlisted concepts.
- **`engine.py`** (4.07 KB): Implements `LegalLiteracyEngine.explain()` and `LegalLiteracyEngine.drill_down()`. Pass-through to `LegalConceptRegistry`. Fallback branches for dynamic drill-downs.
- **`renderer.py`** (4.68 KB): Formats explorations and drill-down results as Markdown.

### 1.2 Tests Mentioning Literacy
- **`tests/test_legal_literacy.py`** (172 lines):
  - `test_due_process_five_level_coverage_and_nuance`: Verifies 5 tiers for Due Process.
  - `test_five_on_demand_drill_down_actions`: Verifies 5 drill-down queries for Due Process.
  - `test_warrant_requirement_drill_downs_and_opposing_view`: Verifies Fourth Amendment concept.
  - `test_dynamic_concept_synthesis_for_unlisted_concept`: Tests `_synthesize_concept` on unlisted concepts (currently tests placeholder synthesis).
  - `test_renderer_level_selection_and_complete_view`: Tests markdown rendering.
  - `test_fastapi_literacy_endpoints`: Tests `/api/v1/literacy/explain` and `/api/v1/literacy/drill-down`.
- **`tests/test_cli_commands.py`**: Tests `legal-gpt explain-doc` (document explainer).
- **`tests/test_document_explainer.py`**: Validates document literacy levels (Plain English, Practical, Legal Terminology).

### 1.3 API Routes
- **`POST /api/v1/literacy/explain`**: Request body `LiteracyExplainRequest(concept, level, jurisdiction, situation)`. Returns exploration + rendered markdown.
- **`POST /api/v1/literacy/drill-down`**: Request body `LiteracyDrillDownRequest(concept, action, jurisdiction, situation)`. Returns drill-down result + rendered markdown.
- **`POST /api/v1/public/explain-document`**: Document explainer endpoint (analyzes legal pleadings and notices).
- *Gap Identified:* No first-class `POST /api/v1/public/explain-concept` endpoint exists yet in the public API group.

### 1.4 CLI Commands
- **`legal-gpt explain`** (lines 435–470 in `cli.py`): Accepts concept, optional level, jurisdiction, situation, and optional `--action` for drill-down.
- **`legal-gpt explain-doc`** (lines 577–610 in `cli.py`): Accepts `--type`, `--text`, `--state`, `--level`, `--json`.

---

## 2. Concept Registry Audit (`core/literacy/registry.py`)

| Concept Identifier | Canonical Name | Jurisdictions Claimed | Real Level 4 Citations? | Real Drill-Down Citations? | Status |
|:---|:---|:---|:---|:---|:---:|
| `due process` | Due Process of Law | US, WA, IL, CA | **Yes** (U.S. Const. amend. XIV, Mathews v. Eldridge, Santosky v. Kramer) | **Partial** (`EXPLAIN_OPPOSING` has empty citations `[]`) | **PARTIAL** |
| `warrant requirement` | Fourth Amendment Warrant Requirement in Child Protection | US, US-FED, US-NY, WA, CA, TX | **Yes** (U.S. Const. amend. IV, Wallis v. Spencer, Nicholson v. Scoppetta) | **Yes** (Camara, Roska, state statutes, Wash. Laws 2021) | **PARTIAL** |
| `_synthesize_concept` (Dynamic Fallback) | *Dynamic (Any unlisted)* | Any requested jurisdiction | **No** (Generic string placeholder e.g. `"Controlling {j_str} Authority"`) | **No** (Generic placeholder strings) | **UNSOURCED** |

### Detailed Concept Breakdown

#### 1. `due process` (Due Process of Law)
- **Status:** **PARTIAL**
- **Level 4 Citations:**
  - `U.S. Const. amend. XIV, § 1` | URL: `https://www.govinfo.gov/content/pkg/GPO-CONAN-2017/pdf/GPO-CONAN-2017.pdf` (REAL)
  - `Mathews v. Eldridge, 424 U.S. 319 (1976)` | URL: `https://www.supremecourt.gov/` (REAL, but court homepage rather than direct slip opinion or official reporter)
  - `Santosky v. Kramer, 455 U.S. 745 (1982)` | URL: `https://www.supremecourt.gov/` (REAL, court homepage)
- **Drill-Down Citations:**
  - `SHOW_SOURCE`: `U.S. Const. amend. XIV`, `Wash. Const. art. I, § 3` (URLs: `https://www.govinfo.gov`, `https://leg.wa.gov`) — REAL.
  - `SHOW_STATUTE`: `42 U.S.C. § 671`, `RCW 13.34.065`, `705 ILCS 405/2-9`, `Cal. WIC § 315` — REAL statutes, but mixes multiple state statutes in a single output without jurisdiction filtering.
  - `SHOW_CASE`: `Santosky v. Kramer, 455 U.S. 745 (1982)` — REAL.
  - `EXPLAIN_OPPOSING`: Citations `[]`, official sources `[]` — **UNSOURCED / EMPTY CITATIONS**.
  - `SHOW_TEMPORAL_CHANGE`: `RCW 13.34.065 (Amended 2021)`, `42 U.S.C. § 675 (Enacted 1997)` — REAL.
- **Deficiencies:**
  - Opposing interpretation lacks cited authority.
  - Bundles WA, IL, and CA statutes together even when a specific jurisdiction like WA is queried.

#### 2. `warrant requirement` (Fourth Amendment Warrant Requirement in Child Protection)
- **Status:** **PARTIAL**
- **Level 4 Citations:**
  - `U.S. Const. amend. IV` | URL: `https://www.govinfo.gov/` (REAL)
  - `Wallis v. Spencer, 202 F.3d 1126 (9th Cir. 2000)` | URL: `https://www.ca9.uscourts.gov/` (REAL)
  - `Nicholson v. Scoppetta, 3 N.Y.3d 357 (2004)` | URL: `https://www.nycourts.gov/` (REAL)
- **Drill-Down Citations:**
  - `SHOW_SOURCE`: `U.S. Const. amend. IV`, `Wallis v. Spencer, 202 F.3d 1126` — REAL.
  - `SHOW_STATUTE`: `RCW 13.34.050`, `Cal. WIC § 305`, `Tex. Fam. Code § 262.104` — REAL, but combines multiple states into a single text block.
  - `SHOW_CASE`: `Roska ex rel. Roska v. Peterson, 328 F.3d 1230 (10th Cir. 2003)` — REAL.
  - `EXPLAIN_OPPOSING`: `Camara v. Municipal Court, 387 U.S. 523 (1967)` — REAL.
  - `SHOW_TEMPORAL_CHANGE`: `Wash. Laws 2021, ch. 211`, `Tex. HB 567 (2021)` — REAL.
- **Deficiencies:**
  - Cross-jurisdiction contamination: A query for WA returns NY caselaw (`Nicholson v. Scoppetta`) and TX/CA statutes without separating federal binding precedent from foreign persuasive state authority.

#### 3. Dynamic Synthesis (`_synthesize_concept`)
- **Status:** **UNSOURCED**
- **Level 4 Citations:**
  - Generic string interpolation: `f"Controlling {j_str} Statutory & Constitutional Provisions regarding {c_title}"`
  - Fake URL: `"https://www.govinfo.gov / Official State Legislative Code"`
- **Drill-Down Citations:**
  - Placeholder arrays: `["Controlling {j_str} Authority"]`, `["Opposing Legal Theories"]`, `["Historical Enactments"]`.
- **Deficiencies:**
  - Directly violates the **Zero-Guessing Principle** and **Two-Brain Architecture**. If an unlisted or unverified concept is queried, the engine must return `ABSTAIN` or `PARTIAL`, never synthesize placeholder citations as if they were authoritative law.

---

## 3. Immediate Action Plan for Days 1–5

1. **Contract Hardening (Days 1–2):**
   - Extend `PrimaryAuthorityReference` with required fields: `verification_status` (`VERIFIED`, `UNVERIFIED`, `ABSTAIN`), `effective_date`, `pinpoint`.
   - Extend `LegalConceptExploration` with `verification_status`, `abstention_reason`, `related_concepts`, and mandatory UPL disclaimer.
   - Eliminate placeholder synthesis in `_synthesize_concept` — enforce strict abstention when no verified authority exists.
   - Enforce jurisdiction isolation: WA queries must strictly return WA and controlling Federal authority; foreign state authorities must either be excluded or explicitly labeled non-binding/persuasive.
2. **Concept Pack A Delivery (Days 3–5):**
   - Implement YAML-backed concept repository in `legal_registry/literacy/concepts/{concept_id}.yaml` for the 12 core CPS/due-process concepts.
   - Ground all 12 concepts in verified primary authority from existing `legal_registry` and official government portals.
