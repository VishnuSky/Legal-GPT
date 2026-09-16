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
