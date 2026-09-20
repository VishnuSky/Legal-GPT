# Legal-GPT: Tribal Authority & Grok/Local Orchestration Audit

**Audit Date**: September 19, 2026  
**Starting Commit**: `1351a76` (`feat(tribal): Indigenous law, treaty rights, historical accountability, Pack C (#11)`)  
**Base**: `origin/main`  
**Branch**: `feat/tribal-orchestration-audit`  
**Working Tree Status**: Clean  

---

## 1. Executive Summary & Architectural Conflict Assessment

This audit evaluates the current state of **Tribal Law / ICWA authority records** and **Grok + Local-Model inference and orchestration** across the Legal-GPT repository.

### Key Audit Finding & Architectural Conflict Assessment
- **Architectural Conflict Status**: **NO MAJOR CONFLICT DETECTED**.
- **Assessment**: The existing Legal-GPT Two-Brain architecture (`legal_registry/` for deterministic primary law; `core/` for procedural reasoning, jurisdiction locking, and verification; `agents/` for multi-stage safety review) is fundamentally sound, modular, and extensible.
- **Identified Gaps**:
  1. **Tribal Authority / Jurisdiction Gaps**: While extensive federal foundational records (sovereignty, treaties, federal ICWA, boarding school records) and general tribal directory metadata exist, `core/jurisdiction.py` lacks cross-contamination detection between Tribal nations, or between state law and tribal law. `core/citation_verifier.py` lacks formal recognition of Tribal statutory codes (`N.N.C.`, `PTC`, `C.N.C.A.`) and treaty Statutes at Large citations (`Stat.`), nor does it distinguish between Federal ICWA, State ICWA overlays (e.g. WACWA, CAL-ICWA), and sovereign Tribal Court jurisdiction.
  2. **Provider Orchestration Gaps**: Grok integration currently exists as an inbound tool consumer via public MCP endpoints (`api/mcp_public.py`). Local model inference exists via `core/local_llm.py` and `legal_gpt/model/inference.py`. However, there is no unified, typed handoff contract supporting outbound role-based routing, provider failover, retry handling, remote provider disablement, or post-generation verification gating.

---

## 2. Inventory of Existing Components

### 2.1 Tribal / ICWA Inventory

| Category | File Path | Status | Verification Tier | Scope / Description |
|---|---|---|---|---|
| **Sources Registry** | `legal_registry/tribal/tribal_sources.yaml` | Implemented | TIER_0 (Official) | Defines BIA Designated ICWA Agents, Navajo Nation Children's Code (9 N.N.C.), Puyallup Tribal Law Title 7 (PTC), Cherokee Nation Code Title 10 (C.N.C.A.). |
| **Sovereignty Doctrine** | `legal_registry/tribal/sovereignty/doctrine.yaml` | Implemented | TIER_1 (Precedent) | Inherent pre-constitutional sovereignty, Marshall Trilogy (*Worcester*, *Cherokee Nation*, *Johnson v. M'Intosh*), *McGirt v. Oklahoma*. |
| **Plenary Power** | `legal_registry/tribal/sovereignty/plenary_power.yaml` | Implemented | TIER_1 (Precedent) | *Lone Wolf*, *Kagama*, *Lara*, trust doctrine, international law context (UNDRIP Arts. 3, 19). |
| **State Jurisdiction** | `legal_registry/tribal/sovereignty/state_jurisdiction.yaml` | Implemented | TIER_0 / TIER_1 | Public Law 83-280 (18 U.S.C. § 1162, 28 U.S.C. § 1360), *Williams v. Lee*, *Bryan v. Itasca County*, *Castro-Huerta*. |
| **Treaty Overview** | `legal_registry/tribal/treaties/overview.yaml` | Implemented | TIER_0 (Constitutional) | U.S. Const. art. VI cl. 2, 25 U.S.C. § 71, Indian Canons of Construction (*Mille Lacs*, *Blackfeet*, *Jones v. Meehan*). |
| **Treaties - Pacific NW** | `legal_registry/tribal/treaties/pacific_northwest.yaml` | Implemented | TIER_0 / TIER_1 | Treaty of Medicine Creek (10 Stat. 1132), Treaty of Point Elliott (12 Stat. 927), Boldt Decision (*U.S. v. Washington*), culverts case. |
| **Treaties - Plains** | `legal_registry/tribal/treaties/great_plains.yaml` | Implemented | TIER_0 / TIER_1 | Fort Laramie Treaties (1851 11 Stat. 749, 1868 15 Stat. 635), Black Hills taking (*Sioux Nation*). |
| **Treaties - Southeast** | `legal_registry/tribal/treaties/southeast.yaml` | Implemented | TIER_0 / TIER_1 | Treaty of New Echota (7 Stat. 478), Indian Removal Act (4 Stat. 411), *McGirt*. |
| **Treaties - Southwest** | `legal_registry/tribal/treaties/southwest.yaml` | Implemented | TIER_0 / TIER_1 | Treaty of Guadalupe Hidalgo (9 Stat. 922), Navajo Treaty of 1868 (15 Stat. 667), *Winters* water doctrine. |
| **ICWA History** | `legal_registry/tribal/icwa/history.yaml` | Implemented | TIER_0 / TIER_1 | Pub. L. 95-608 (25 U.S.C. §§ 1901-1963), Congressional findings (25-35% removal), *Holyfield*. |
| **ICWA Challenge** | `legal_registry/tribal/icwa/constitutional_challenge.yaml` | Implemented | TIER_1 (Precedent) | *Haaland v. Brackeen* (599 U.S. 255, 2023), Article I plenary authority, 10th Amendment anti-commandeering rejection. |
| **ICWA Standards** | `legal_registry/tribal/icwa/active_efforts_standard.yaml` | Implemented | TIER_0 / TIER_1 | 25 U.S.C. § 1912(d), 25 C.F.R. § 23.2, heightened standard vs Title IV-E reasonable efforts. |
| **ICWA Jurisdiction** | `legal_registry/tribal/icwa/tribal_court_jurisdiction.yaml` | Implemented | TIER_0 (Statutory) | 25 U.S.C. § 1911(a) exclusive, § 1911(b) transfer, § 1911(c) intervention, § 1911(d) full faith & credit. |
| **Boarding Schools** | `legal_registry/tribal/history/boarding_schools.yaml` | Implemented | Official Investigative | DOI May 2022 Federal Indian Boarding School Report, Indian Civilization Act 1819 (3 Stat. 516), 25 U.S.C. § 282. |
| **Timeline** | `legal_registry/tribal/history/legal_timeline.yaml` | Implemented | Verified Chronology | 21 milestone legal events from 1823 (*Johnson v. M'Intosh*) to 2023 (*Haaland v. Brackeen*). |
| **Nations Directory** | `legal_registry/tribal/nations/*.yaml` (6 files) | Implemented | Directory / Metadata | Overview (574 federally recognized tribes), Pacific NW, Southwest, Plains, Southeast, Great Lakes. |
| **International Bridge**| `legal_registry/international/indigenous/*.yaml` (3 files)| Implemented | International Norms | UNDRIP (non-binding domestic), ILO 169 (unratified), ICCPR Art. 27 (non-self-executing). |
| **Literacy Pack C** | `legal_registry/literacy/concepts/*.yaml` (10 files) | Implemented | 5-Level Progressive | 10 concepts covering sovereignty, ICWA active efforts, QEW, jurisdiction, blood quantum, discovery, land trust, voting. |
| **State CPS Overlay** | `legal_registry/cps/wa_tribal_cps.yaml` | Implemented | TIER_0 (State/Tribal) | 25 U.S.C. Chapter 21 & RCW 13.38 (WICWA), emergency removal, notice, standard of proof. |
| **ICWA Engine** | `cps/icwa_engine.py` | Implemented | Logic Engine | Evaluates ICWA inquiry compliance, mandatory notice (25 U.S.C. § 1912(a)), active efforts, QEW standards. |
| **Tribal Registry Tests** | `tests/test_tribal_registry.py` | Implemented | Automated Tests | 10 tests verifying sovereignty, Boldt citation, ICWA history, UNDRIP status, timeline, DOI report, Pack C. |

### 2.2 Provider Abstraction, Inference & Orchestration Inventory

| Component | Path | Status | Capabilities & Current Limitations |
|---|---|---|---|
| **Local LLM Client** | `core/local_llm.py` | Implemented | Supports OpenAI-compatible endpoints (`/v1`), model discovery, prompt formatting, timeout. Lacks retry policies, failover, provider typing. |
| **Model Runtime Client** | `legal_gpt/model/inference.py` | Implemented | Basic `LegalModelClient`, `InferenceRequest`, `InferenceResponse` with deterministic fallback. Lacks remote provider routing. |
| **Grok / Public MCP** | `api/mcp_public.py` | Implemented | Public HTTP/SSE MCP server with `lookup_public_law`, `explain_concept`, `lookup_services`, `get_deadlines`. Gated by verification. |
| **Grok Documentation** | `docs/GROK_INTEGRATION.md`, `docs/SCOUT_SYSTEM_PROMPT.md` | Implemented | Complete specification for Public Law Scout integration with tool definitions and prompt guards. |
| **Master Orchestrator** | `agents/legal_orchestrator.py` | Implemented | Multi-stage pipeline: intake -> jurisdiction lock -> substantive logic -> adversarial review -> citation verification -> persona rendering -> final safety gate. |
| **Audit Ledger** | `audit/ledger.py` | Implemented | SHA-256 session logging of queries, authorities, chunks, outputs, and counterarguments. |
| **Orchestrator Tests** | `tests/test_orchestrator.py` | Implemented | 5 tests validating due process flags, ICWA active efforts trigger, adversarial counterarguments, citation verification. |

---

## 3. Phase 1: Comprehensive Tribal Authority Audit

Every existing tribal legal record is audited below against primary source standards:

### 3.1 Sources & Statutory Codes

1. **BIA Designated Tribal ICWA Agents (Federal Register Notice)**
   - **Jurisdiction / Entity**: Federal / Executive Agency (`BIA`, U.S. Dept. of the Interior)
   - **Official URL**: `https://www.bia.gov/bia/ois/dhs/icwa`
   - **Source Type**: Administrative Directory / Federal Register Notice
   - **Authority Scope**: Annual designated agents for service of process under 25 U.S.C. § 1912(a).
   - **Verification Status**: `VERIFIED`
   - **Known Limitations**: Updated annually; addresses must be verified directly with BIA/tribal clerks for pending filings.

2. **Navajo Nation Code — Title 9: Domestic Relations & Children**
   - **Jurisdiction / Entity**: Sovereign Nation (`Navajo Nation`) / Navajo Nation Council
   - **Official URL**: `https://www.nnols.org/navajo-nation-code/`
   - **Citation Format**: `9 N.N.C. § {section}`
   - **Source Type**: Tribal Sovereign Statute
   - **Authority Scope**: Exclusive domestic relations and child welfare law within Navajo Nation territorial jurisdiction.
   - **Verification Status**: `VERIFIED` (Official Office of Legislative Services)
   - **Known Limitations**: Requires access to official Diné legal portals; does not govern other tribal nations.

3. **Puyallup Tribal Law — Title 7: Children's Code**
   - **Jurisdiction / Entity**: Sovereign Nation (`Puyallup Tribe of Indians`) / Puyallup Tribal Council
   - **Official URL**: `https://www.codepublishing.com/WA/PuyallupTribe/`
   - **Citation Format**: `PTC 7.{section}`
   - **Source Type**: Tribal Sovereign Statute
   - **Authority Scope**: Child protection and dependency within the Puyallup Reservation (Washington).
   - **Verification Status**: `VERIFIED`
   - **Known Limitations**: Governs only Puyallup tribal members and reservation boundaries; distinct from state WACWA.

4. **Cherokee Nation Code Annotated — Title 10: Children**
   - **Jurisdiction / Entity**: Sovereign Nation (`Cherokee Nation`) / Cherokee Nation Tribal Council
   - **Official URL**: `https://attorneygeneral.cherokee.org/laws-and-code/`
   - **Citation Format**: `10 C.N.C.A. § {section}`
   - **Source Type**: Tribal Sovereign Statute
   - **Authority Scope**: Child welfare and parental rights within the Cherokee Nation reservation.
   - **Verification Status**: `VERIFIED`
   - **Known Limitations**: Applicable exclusively to Cherokee Nation jurisdiction; non-transferable to other nations.

### 3.2 Federal ICWA vs. State Overlays vs. Tribal Law

| Authority Layer | Governing Law | Jurisdictional Scope | Binding Level in State Court |
|---|---|---|---|
| **Federal ICWA** | 25 U.S.C. §§ 1901–1963; 25 C.F.R. Part 23 | All Indian child custody proceedings in all 50 states | **Mandatory Federal Floor** (Art. VI Supremacy Clause; *Haaland v. Brackeen*) |
| **State ICWA (e.g. WACWA)** | RCW Chapter 13.38 | Proceedings in Washington State Superior Courts | **Binding State Law** (Provides heightened protections exceeding federal minimums) |
| **Tribal Sovereign Code** | E.g., 9 N.N.C.; PTC Title 7; 10 C.N.C.A. | Tribal Court proceedings within tribal territory/jurisdiction | **Exclusive or Concurrent Sovereign Authority** (Full Faith & Credit under 25 U.S.C. § 1911(d)) |
| **Tribal Court Procedure** | Local Tribal Court Rules & Codes | Tribal Court administration | **Binding strictly within Tribal Court**; never silently substituted for state rules |

### 3.3 Identification of Missing or Inaccessible Sources
- **Tribal Court Procedural Rules**: Not uniformly indexed. Most tribes maintain independent, non-public or separate court clerk rules.
- **Tribal Citizenship & Enrollment Ordinances**: Must NOT be inferred or simulated; exclusively controlled by each sovereign Nation.
- **50-State ICWA Overlay Gaps**: States other than WA, MN, CA, OK, and NM lack codified state-level ICWA statutes and rely solely on federal ICWA.

---

## 4. Phase 3: Provider Orchestration Audit

| Feature Requirement | Current Implementation Status | Assessment & Gap Analysis |
|---|---|---|
| **Provider Abstraction** | `PARTIAL` | `core/local_llm.py` and `legal_gpt/model/inference.py` exist but lack a polymorphic `BaseProvider` class. |
| **Role-Based Routing** | `SCAFFOLDED` | Agent roles exist (`IntakeClassifier`, `AdversarialReviewer`, `FinalReviewAgent`), but dispatching to different models/providers is hardcoded. |
| **Structured Input/Output Contracts** | `PARTIAL` | `InferenceRequest` exists in `legal_gpt/model/inference.py`, but lacks a typed safe handoff object with verified source boundaries. |
| **Timeouts and Retries** | `PARTIAL` | Fixed timeout (120s in `local_llm.py`), but no exponential backoff or retry logic. |
| **Failover Behavior** | `PARTIAL` | Soft fallback to deterministic text exists, but no provider-to-provider failover (e.g. Grok -> Local -> Deterministic). |
| **Model/Provider Identification** | `IMPLEMENTED` | Server info and model name tracked in response metadata. |
| **Verification After Generation** | `IMPLEMENTED` | `FinalReviewAgent` and `CitationVerifier` run post-generation verification. |
| **Audit Logging** | `IMPLEMENTED` | `audit/ledger.py` records cryptographic hash of queries and outputs. |
| **Local-Only Operation** | `IMPLEMENTED` | Local LLM defaults to `localhost:1234/v1` and operates zero-network. |
| **Remote-Provider Disablement** | `PARTIAL` | Needs explicit flag (`ALLOW_REMOTE_PROVIDERS=false` / `LOCAL_ONLY=true`). |
| **Configuration Validation** | `SCAFFOLDED` | Needs unified configuration schema validating API keys, endpoints, and timeouts. |

---

## 5. Planned Work for Phases 2–6

1. **Phase 2 (Jurisdiction & Contamination Safeguards)**:
   - Enhance `core/jurisdiction.py` to identify Tribal Nation codes (`TRIBAL-NAVAJO`, `TRIBAL-PUYALLUP`, `TRIBAL-CHEROKEE`, etc.) and prohibit silent state-law substitution or cross-nation contamination.
   - Enhance `core/citation_verifier.py` to recognize and verify Tribal Codes (`N.N.C.`, `PTC`, `C.N.C.A.`), Treaty Statutes at Large (`Stat.`), and distinguish `FEDERAL` ICWA from state overlays and sovereign tribal codes.
   - Add targeted pytest suite in `tests/test_tribal_jurisdiction_safeguards.py`.

2. **Phase 4 & 3 (Safe Handoff Contract & Unified Provider Orchestration)**:
   - Create `core/orchestration/handoff.py`: Typed Pydantic contract (`SafeHandoffContract`, `VerifiedSourceReference`, `HandoffOutputSchema`).
   - Create `core/orchestration/provider.py`: Unified `BaseProvider`, `GrokProvider`, `LocalLLMProvider`, `FallbackDeterministicProvider`, `ProviderRouter` supporting timeouts, retries, failover, and strict verification gating.

3. **Phase 5 (Failure & Adversarial Tests)**:
   - Create `tests/test_provider_orchestration_failures.py`: Adversarial tests covering Grok unavailable, local unavailable, malformed responses, prompt injections, fabricated citations, conflicting authority, and abstention on missing tribal sources.

4. **Phase 6 (Documentation & Release Gates)**:
   - Generate `docs/TRIBAL_ORCHESTRATION_RELEASE_GATES.md`.
