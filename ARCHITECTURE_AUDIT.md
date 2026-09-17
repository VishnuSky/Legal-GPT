# Legal-GPT Architecture Audit (v1.0 → Alpha 0.3.0)

**Date**: 2026-09-16  
**Auditor**: Legal-GPT Core Architecture Team  
**Scope**: Full repository architecture, module interfaces, data flows, integration points, and model training expansion pathways.

---

## 1. Executive Summary

Legal-GPT v1.0 is an operational, jurisdiction-aware, citation-verified legal intelligence and RAG platform. The system operates on a 14-tier dynamic authority hierarchy (T0–T13), point-in-time statutory resolution (`LAW_AT_DATE`), a Shepherd's-style relational citator, an anti-contamination jurisdiction lock, and an adversarial due process reviewer.

The platform is now advancing to **Alpha 0.3.0**, implementing a **Two-Brain Architecture**:
- **Brain 1 (Model Reasoning / GGUF / LoRA)**: Learns legal epistemology, issue spotting, argument synthesis, and epistemological statement classification across 12 distinct categories.
- **Brain 2 (Legal Authority Engine / Database)**: Authoritative repository of statutory, regulatory, and judicial primary sources, ensuring statutes are not hard-baked into weight parameters.

---

## 2. Module Inventory & Interface Matrix

| Module | Primary Interface / Class | Functionality | Status & Integration Points |
| :--- | :--- | :--- | :--- |
| **`core/`** | `JurisdictionLock`, `PointInTimeEngine`, `AuthorityHierarchy`, `ClaimsMatrixEngine` | Enforces geographic bounds, temporal validity, 14-tier authority ranking, and substantive claims evaluation. | Extended with `LegalTruthObject` and `core/conflicts/` engine. |
| **`cps/`** | `CPSLifecycleEngine`, `ParentRightsAuditor`, `EvidenceMatrix`, `PleadingGenerator` | End-to-end child welfare workflow across 8+ jurisdictions (Federal, WA, IL, OH, CA, TX, NY, Tribal). | Extended into 19 discrete lifecycle curricula. |
| **`legal_registry/`** | `LegalRegistryLoader`, `default_registry` | 50-state statutory matrices, court registries, and jurisdictional rules. | Integrated with Brain 1 authority selector. |
| **`services/`** | `ServiceRegistry`, `default_service_registry` | Official public civil legal aid, self-help, and institutional service directory. | Bridges user needs to official public institutional resources. |
| **`normalization/`** | `StatuteChunker`, `PolicyChunker`, `RegulationChunker`, `LegalDocument` | Canonical document modeling, hash computation, and structural legal chunking. | Feeds SFT dataset builder and evaluation harness. |
| **`ingestion/`** | `GovInfoConnector`, `CourtListenerConnector`, `WashingtonLegConnector`, `IllinoisLegConnector`, `OhioLegConnector` | Official public API and portal crawlers with SHA-256 caching and rate limiting. | Supplies primary source grounded texts. |
| **`agents/`** | `LegalOrchestrator`, `DueProcessAuditor` | Multi-agent coordination and adversarial review. | Extended into formal 11-agent hierarchy with Final Review guardrail. |
| **`api/`** | `FastAPI` application, `LegalMCPHandler` | REST API endpoints (`/api/v1/public/resolve`, `/api/v1/public/services`) and Model Context Protocol server. | Interfaces with OpenWebUI, LM Studio, and Scout Bot. |
| **`benchmarks/`** | `LegalBenchmarkEvaluator`, 50 synthetic scenarios | Multi-category accuracy, jurisdiction lock, and temporal precision testing. | Preserved and integrated into CI security gates. |

---

## 3. Epistemological & Training Integration Analysis

### 3.1 Two-Brain Division of Labor
```
                        ┌──────────────────────────────────────────────┐
                        │              USER INQUIRY / SCOUT            │
                        └──────────────────────┬───────────────────────┘
                                               │
                                               ▼
                        ┌──────────────────────────────────────────────┐
                        │          BRAIN 1: LEGAL-GPT MODEL            │
                        │ (GGUF / LoRA: Epistemology, Reasoning, Plan) │
                        └──────────────────────┬───────────────────────┘
                                               │ "Query Intent & Needs"
                                               ▼
                        ┌──────────────────────────────────────────────┐
                        │        BRAIN 2: LEGAL AUTHORITY ENGINE       │
                        │ (RAG, Registry, Temporal, Citator, Database) │
                        └──────────────────────┬───────────────────────┘
                                               │ Structured Legal Package
                                               ▼
                        ┌──────────────────────────────────────────────┐
                        │          BRAIN 1: LEGAL-GPT MODEL            │
                        │ (Applies rules, drafts argument, cites auth) │
                        └──────────────────────┬───────────────────────┘
                                               │ Proposed Response
                                               ▼
                        ┌──────────────────────────────────────────────┐
                        │     PROPOSITION & CITATION VERIFIER GATE     │
                        │ (Zero hallucination & jurisdiction lock)     │
                        └──────────────────────┬───────────────────────┘
                                               │ Verified Response
                                               ▼
                                         FINAL ANSWER
```

### 3.2 Key Architectural Opportunities & Solutions
1. **Separation of Legal Reasoning from Authority**: Avoids parameter decay by keeping statutes in databases and reasoning structures in model weights.
2. **Statement Classification Epistemology**: Classifies outputs into 12 explicit categories (`FACT`, `LAW`, `PRECEDENT`, `INTERPRETATION`, `INFERENCE`, `ALLEGATION`, `ARGUMENT`, `COUNTERARGUMENT`, `POLICY`, `OPINION`, `UNCERTAINTY`, `UNKNOWN`).
3. **Structured Conflict Surfacing**: Prevents silent legal conflict resolution by generating explicit Supremacy, Preemption, Temporal, and Jurisdiction conflict records.
4. **Local Runtime Portability**: Provides out-of-the-box support for LM Studio, llama.cpp, Ollama, and vLLM via standardized GGUF exports and MCP tool bridges.

---

## 4. Public Safety & Data Isolation Verification
- All code, datasets, and prompts comply strictly with `PUBLIC_DATA_POLICY.md` and `SECURITY.md`.
- No private case files, credentials, local user paths, or audio recordings exist in the repository.
- Deep security audits run continuously with zero violations.

---

## 5. Known Gaps, Incomplete Implementations, and Blockers

While all 140 unit and integration tests are currently passing against symbolic mocks and synthetic fixtures, a rigorous architectural inspection reveals several key implementation gaps, ingestion boundaries, and pending tasks required for a production v1.0 / Alpha 0.3.1 rollout:

### 5.1 Incomplete Implementations & Simulated Pipelines
1. **SFT Training Loop Simulation (`training/train_sft.py`)**:
   - The current `SFTTrainingPipeline.run_training_simulation()` validates curriculum stages, hyperparameter configurations, and schema compliance without executing real multi-GPU PyTorch backward passes.
   - *Status*: Working simulation and schema verification. Real distributed LoRA training runs on private GPU infrastructure (`legal-gpt-private`) to prevent heavy weight caches and checkpoints from entering this public repository.
2. **GGUF Export Pipeline Packaging (`training/export/gguf_pipeline.py`)**:
   - Generates release manifests, quant specifications (`Q4_K_M`, `Q5_K_M`, `Q8_0`), and model cards.
   - The actual `llama-quantize` C++ binary invocation must be executed in an environment with compiled llama.cpp tooling installed.
3. **Local Inference Client Fallback (`legal_gpt/model/inference.py`)**:
   - If an LM Studio or Ollama endpoint is unreachable at `http://localhost:1234/v1`, the client gracefully falls back to deterministic structured mock completions for offline testing.
4. **Final Review Agent Coverage (`agents/final_review_agent.py`)**:
   - Epistemic safety check currently performs heuristic string and regex matching for required disclaimers rather than an end-to-end NLI (Natural Language Inference) contradiction model.

### 5.2 Ingestion & Crawler Limitations
1. **State Crawler Coverage**:
   - Live scrapers with caching and parsing are implemented for **Washington** (`ingestion/state_crawlers/washington.py`), **Illinois** (`ingestion/state_crawlers/illinois.py`), and **Ohio** (`ingestion/state_crawlers/ohio.py`).
   - The remaining 47 states currently rely on curated seed statutes in `legal_registry/` rather than dynamic live web crawlers.
2. **Third-Party API Rate Limits & Keys**:
   - `CourtListenerConnector` and `GovInfoConnector` require valid API keys in `.env` for production volume synchronization; both operate in offline fixture fallback mode when keys are absent.
   - The Washington crawler rate-limits requests to $\ge 1.0\text{s}$ per section, meaning a full 1,000-statute crawl takes approximately 18 minutes.

### 5.3 Dataset Population & Size Limitations
1. **Evaluation Datasets (`evaluation/datasets/*.jsonl`)**:
   - The 7 benchmark evaluation datasets contain **16 curated seed records** (2–3 high-value benchmark pairs per domain) designed for schema validation, regression CI, and fast test execution.
   - Expanding each dataset to 500+ real-world anonymized scenarios is planned for Alpha 0.3.1.
2. **Training Datasets (`training/datasets/`)**:
   - Task families 01–23 contain synthetic JSONL template samples. Full-scale SFT requires compiling 50,000+ synthetic multi-turn dialogues across the 4 curriculum stages prior to the final fine-tuning run.

### 5.4 Architecture Inconsistencies & Unresolved Integration Points
1. **MCP Streaming vs. Synchronous RPC**:
   - `FastAPI` supports async streaming responses for token generation, but the current `LegalMCPHandler` (`api/mcp_server.py`) returns complete tool-call payloads synchronously. Streaming MCP protocol support is pending.
2. **In-Memory Citator Graph Scale**:
   - The Shepherd's-style relational citator (`core/citator.py`) operates in-memory and in SQLite for testing. Scaling to 10M+ national judicial citation edges requires a dedicated PostgreSQL graph or Neo4j backend in Brain 2.
3. **External Scout Bot Webhook Bridge**:
   - The public bridge API contract (`POST /api/v1/public/resolve`, `GET /api/v1/public/services`) and MCP tools (`lookup_public_law`, `lookup_services`) are operational in `api/public_api.py`. However, the live external Grok bot webhook dispatcher runs outside the public repository.

### 5.5 Action Items & Roadmap for Alpha 0.3.1
- [ ] Implement live scrapers for CA, TX, NY, and FL legislative portals.
- [ ] Expand the 7 evaluation datasets from 16 seed records to 500+ curated scenarios per domain.
- [ ] Add streaming tool response support to `api/mcp_server.py`.
- [ ] Transition citator relational graph to persistent vector + relational backend for multi-million citation lookups.
- [ ] Finalize the external Grok Scout Bot webhook integration using the documented `/api/v1/public/resolve` schema.

