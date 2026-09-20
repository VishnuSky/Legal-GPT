# Legal-GPT Public Benefit Capability Audit
**Document Version:** 1.0.0  
**Repository:** `VishnuSky/Legal-GPT`  
**Date:** September 2026  
**Status:** Canonical System Architecture & Capability Audit  

---

## Executive Summary: The Public Infrastructure Thesis

Legal-GPT was conceived not merely as a conversational AI or legal chatbot, but as an **open-weight, verification-gated public legal intelligence infrastructure**. 

For an ordinary person—a parent whose child has been removed by child protective services, a tenant served with a notice to vacate, a consumer facing abusive debt collection, or a self-represented litigant navigating state court procedure—the legal system presents an asymmetric wall of complexity, procedural traps, confusing jargon, strict unyielding deadlines, and severe power imbalances. Most individuals cannot afford private legal representation, and legal aid programs are forced to turn away over 70% of eligible applicants due to catastrophic resource constraints.

In this context, the central inquiry of this audit is:
> **"What useful things can Legal-GPT provide to an ordinary person trying to understand, navigate, document, or respond to a legal problem?"**

This audit provides an exhaustive inventory of Legal-GPT's existing technical capabilities, systematically evaluates them against **39 distinct public user needs (A through AM)**, identifies structural resource gaps, models a dedicated **Public Legal Navigator** architectural layer, analyzes epistemic safety risks, and delivers a prioritized, actionable implementation roadmap.

---

## 1. Existing Capabilities Inventory

Below is an inventory of every substantive subsystem, engine, agent, and module currently implemented in the Legal-GPT codebase.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 LEGAL-GPT PLATFORM MATRIX                                   │
├───────────────────────────────┬───────────────────────────────┬─────────────────────────────┤
│      KNOWLEDGE & REGISTRY     │     REASONING & CITATOR       │    CPS & PROCEDURAL ENGINES │
│ - 50-State Statutory Matrix   │ - 14-Tier Dynamic Authority   │ - 18-Stage Lifecycle Engine │
│ - Federal & Tribal Sources    │ - Shepard's-Style Citator     │ - Due Process Auditor       │
│ - Live State Crawlers         │ - LAW_AT_DATE Temporal Graph  │ - Evidence Matrix (Suffic.) │
│ - Civil Services Directory    │ - 5-Way Conflict Detector     │ - Procedural Motion Guides  │
│ - Hybrid BM25 / Vector Store  │ - NLI Proposition Verifier    │ - Court Pleading Generator  │
├───────────────────────────────┼───────────────────────────────┼─────────────────────────────┤
│         SAFETY & GATES        │     PERSONAS & INTERFACES     │     STANDARDS & METRICS     │
│ - Strict Jurisdiction Lock    │ - Self-Represented Mode       │ - 50-Scenario Benchmark     │
│ - Anti-Contamination Firewall │ - Investigator Evidence Mode  │ - 10 External Ground-Truth  │
│ - Final Review 5-Check Gate   │ - Formal Attorney Memo Mode   │ - 23 SFT Task Family Seeds  │
│ - Explicit Abstention Trigger │ - Court Bench Record Mode     │ - Automated Privacy Audits  │
│ - Public Data Isolation Wall  │ - FastAPI & MCP Streaming     │ - GGUF 4-bit Quant Export   │
└───────────────────────────────┴───────────────────────────────┴─────────────────────────────┘
```

---

### Capability Inventory Table

| ID | Capability Name | Module & File | Class / Function | Entry Point (API / CLI) | Input | Output | Dependencies | Tests | Maturity | Known Limitations |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **C01** | **Jurisdiction Locking & Boundary Enforcement** | `core/jurisdiction.py` | `JurisdictionEngine.validate_jurisdiction_lock()` | CLI: `--state`, API: `LegalQueryRequest.state` | State code, query text, county | Normalized jurisdiction, lock status, contamination warning | `legal_registry.loader` | `tests/test_jurisdiction_lock.py` | **IMPLEMENTED** | Relies on 2-letter state codes or registry mappings; cannot infer sub-tribal jurisdictional compacts automatically without explicit tribal flag. |
| **C02** | **14-Tier Dynamic Authority Hierarchy** | `core/authority.py`, `core/authority_calculator.py` | `AuthorityHierarchyCalculator.calculate_authority_score()` | CLI: `query`, API: `POST /api/v1/query` | Document metadata, court level, publication type, enactment date | `AuthorityScore` (Tier T0–T13, decimal weight 0.0–1.0) | None (pure logic) | `tests/test_advanced_architecture.py` | **IMPLEMENTED** | State court rule ranking relative to local administrative guidance is hardcoded; requires periodic validation against state-specific civil rule hierarchy. |
| **C03** | **Point-in-Time Law Resolution (LAW_AT_DATE)** | `core/temporal.py`, `core/temporal_graph.py` | `TemporalGraph.evaluate_law_at_date()` | CLI: `law-at-date`, API: `GET /api/v1/temporal/{cite}` | Citation string, jurisdiction, calendar date | `TemporalStatusResult` (valid_on_date, superseded, operative_version) | `storage.vector_store` | `tests/test_temporal.py` | **IMPLEMENTED** | Complete legislative historical version trees currently populated primarily for Washington RCW/WAC and Federal Title IV-E/ICWA; other states hold current law with sunset metadata. |
| **C04** | **Line-by-Line Statutory Diff Engine** | `knowledge_graph/point_in_time_diff.py` | `PointInTimeDiffEngine.diff_statute_at_dates()` | CLI: `law-at-date --diff-with` | Citation, date_a, date_b | `StatutoryDiffReport` (unified text diff, additions, deletions) | `core.temporal_graph` | `tests/test_temporal.py` | **IMPLEMENTED** | Requires multiple archived statutory snapshots in local storage; fallback generates notice when historical snapshot is unavailable. |
| **C05** | **Relational Citator & Shepard's Signals** | `knowledge_graph/relational_graph.py` | `CitatorGraph.evaluate_citator_status()` | CLI: `citator`, API: `GET /api/v1/citator/{cite}` | Citation or case name (e.g. *Haaland v. Brackeen*) | `CitatorReport` (overall_signal: GOOD_LAW, CAUTION, OVERRULED, citing_references) | SQLite / in-memory graph | `tests/test_phase3_citator.py` | **IMPLEMENTED** | Seed graph covers landmark CPS and constitutional precedent (*Santosky*, *Troxel*, *Stanley*, *Brackeen*); coverage of routine intermediate state appeals court decisions requires expanded caselaw ingestion. |
| **C06** | **Anti-Hallucination Citation Verifier** | `core/citation_verifier.py` | `CitationVerifier.verify_citation()` | CLI: `verify-citation`, MCP: `verify_citation` | Citation string | `CitationVerificationResult` (verified: bool, authority_tier, publisher_name) | `legal_registry.loader` | `tests/test_citation_verifier.py` | **IMPLEMENTED** | Strictly validates known structural formats and registered statutory sections; does not check physical volume/page numbers of unpublished state slip opinions. |
| **C07** | **Multi-Stage Proposition Verifier** | `core/proposition_verifier.py` | `PropositionVerifier.verify_response_propositions()` | Internal orchestrator step | Draft model response, verified source chunks | `PropositionVerificationReport` (grounded_ratio, ungrounded_claims, epistemic_tags) | None (NLI/regex logic) | `tests/test_curricula_and_truth.py` | **IMPLEMENTED** | Uses deterministic proposition splitting; complex multi-clause compound legal sentences occasionally require clause decomposition. |
| **C08** | **5-Way Legal Conflict Detection Engine** | `core/conflicts/` | `StatutoryConflictDetector`, `TemporalConflictDetector`, etc. | Internal orchestrator step | Controlling authorities, factual dates, jurisdiction | List of identified conflicts (Federal preemption, inter-statute, temporal sunset) | `legal_registry` | `tests/test_conflicts_engine.py` | **IMPLEMENTED** | Handles statutory, temporal, jurisdiction, precedent, and authority conflicts; municipal ordinance conflicts are currently scaffolded. |
| **C09** | **Final Review Agent & Proposition Validator** | `agents/final_review_agent.py` | `FinalReviewAgent.review_response()` | Internal orchestrator step | `StandardLegalResponse` | `FinalReviewResult` (passed, failures, warnings, jurisdiction_confirmed, citation_coverage) | `core.citation_verifier` | `tests/test_final_review_agent.py` | **IMPLEMENTED** | Replaces heuristic regex with 5 structured checks; triggers automated abstention and uncertainty when critical checks fail. |
| **C10** | **Adversarial Reviewer & Counterarguments** | `agents/adversarial_reviewer.py` | `AdversarialReviewer.generate_counterarguments()` | CLI: `query`, API: `POST /api/v1/query` | Draft analysis, jurisdiction, factual assertions | List of `AdversarialCounterargument` (opposing_argument, legal_theory, rebuttal_strategy) | Core engines | `tests/test_orchestrator.py` | **IMPLEMENTED** | Provides realistic agency and prosecutor counter-theories for child welfare and civil procedure; criminal defense counterarguments remain scaffolded. |
| **C11** | **4-Persona Rendering System** | `agents/human_review_modes.py` | `PersonaRenderer` | CLI: `--mode`, API: `mode` | Standard response object, persona flag | Rendered markdown tailored for: Self-Represented, Investigator, Attorney, Court | Response formatter | `tests/test_orchestrator.py` | **IMPLEMENTED** | Self-represented mode strips legalese and adds checklists; court mode produces judicial bench memos with audit blocks. |
| **C12** | **18-Stage CPS Lifecycle Engine** | `cps/lifecycle.py` | `CPSLifecycleEngine` | API: `POST /api/v1/due_process/audit`, CLI | Stage enum (e.g. `SHELTER_CARE_HEARING`), state | `CPSStageRequirements` (deadlines, notice requirements, counsel rights, standards of proof) | `legal_registry` | `tests/test_cps_lifecycle.py` | **IMPLEMENTED** | Covers all 18 lifecycle stages from initial allegation to appeal for WA, IL, OH, CA, TX, NY, and Federal/ICWA. |
| **C13** | **Evidentiary Sufficiency & Proof Gap Engine** | `cps/evidence_matrix.py` | `EvidenceMatrixEngine.evaluate_evidence_items()` | CLI: `evaluate-evidence`, API: `POST /api/v1/evidence/evaluate` | List of `CaseEvidenceItem` (type, description, source, element) | `EvidentiaryMatrixEvaluation` (sufficiency_rating, evidentiary_gaps, rebuttal_strategy) | None (Pydantic models) | `tests/test_claims_matrix.py` | **IMPLEMENTED** | Rigorously categorizes UNVERIFIED_ALLEGATION vs. DOCUMENTED_EXHIBIT; requires manual or structured API submission of evidence items. |
| **C14** | **Due Process Multi-Pillar Auditor** | `cps/due_process_audit.py` | `DueProcessAuditor.audit_case()` | CLI: `due-process-audit`, API: `POST /api/v1/due_process/audit` | State, stage, notice, counsel, services, visitation, ICWA status | `DueProcessAuditReport` (compliance matrix, violations identified, recommended remedies) | `cps.lifecycle`, `cps.parent_rights` | `tests/test_phase4_cps_deep_dives.py` | **IMPLEMENTED** | Evaluates 8 constitutional pillars; maps exact statutory remedies (e.g. immediate return motion, rehearing affidavit). |
| **C15** | **Procedural Motion & Court Rule Guide Engine** | `core/procedural_engine.py` | `ProceduralEngine.get_guides_for_jurisdiction()` | Internal engine, API: `POST /api/v1/public/resolve` | Jurisdiction, matter, factual context | List of `ProceduralMotionGuide` (statutory deadline, prerequisites, service rules, exhibits) | None (Pydantic models) | `tests/test_phase4_cps_deep_dives.py` | **IMPLEMENTED** | Implemented for 7 critical motions across WA, IL, NY, CA, TX, OH, ICWA; expansion needed for housing eviction and debt defense procedures. |
| **C16** | **State Court Pleading & Form Generator** | `cps/pleading_generator.py` | `PleadingGenerator.generate_pleading()` | CLI: `generate-motion`, API: `POST /api/v1/pleadings/draft` | `PleadingDraftRequest` (state, motion_type, county, facts) | `PleadingDraftResponse` (court caption, formal body markdown, certificate of service) | None | `tests/test_phase4_cps_deep_dives.py` | **IMPLEMENTED** | Generates standardized, rule-compliant motion templates; does not electronically file or integrate with court e-filing systems (ECF/Odyssey). |
| **C17** | **Official Civil Services & Legal Aid Registry** | `services/registry.py`, `services/models.py` | `ServiceRegistry.query_services()` | API: `GET /api/v1/public/services`, `POST /api/v1/public/resolve` | State, county, matter, service_type | List of `PublicServiceRecord` (name, address, intake_url, phone, hours, eligibility) | Seed YAMLs (`seeds/*.yaml`) | `tests/test_services_registry.py` | **IMPLEMENTED** | Seeded with verified official providers for WA, IL, OH, and Federal; needs continuous expansion across remaining 47 states and territories. |
| **C18** | **Public Scout Bridge & Resolution Engine** | `api/server.py` | `resolve_public_query()` | API: `POST /api/v1/public/resolve` | `PublicResolveRequest` (question, jurisdiction, county, date, matter) | `PublicResolveResponse` (jurisdiction_lock, controlling_sources, procedures, service_hits, abstention) | Orchestrator, ServiceRegistry | `tests/test_public_api.py` | **IMPLEMENTED** | Provides unified public endpoint marrying legal analysis with official service directory routing and procedural forms. |
| **C19** | **Streaming MCP & REST Reasoning Protocols** | `api/mcp_server.py`, `api/server.py` | `LegalMCPHandler.execute_tool_stream()` | API: `POST /api/v1/public/resolve/stream`, MCP stdio | Tool arguments (`lookup_public_law`, `lookup_services`) | 6-stage chronological stream (`ndjson` chunks terminating in `complete` or `error`) | FastAPI StreamingResponse | `tests/test_mcp_streaming.py` | **IMPLEMENTED** | Exposes full reasoning lifecycle to external UI clients; error chunks safely surface invalid jurisdictions without 500 crashes. |
| **C20** | **Live Multi-State Legislative Crawlers** | `ingestion/state_crawlers/` | `WashingtonCrawler`, `CaliforniaCrawler`, `TexasCrawler`, `NewYorkCrawler`, `FloridaCrawler` | CLI: `ingest --state`, API: `POST /api/v1/ingest/sync` | Target state code, live web connection | Normalized `LegalDocument` objects, cached raw HTML/JSON | `ingestion.base`, `requests`, `BeautifulSoup` | `tests/test_live_state_crawlers.py` | **IMPLEMENTED** | Crawlers fetch live statutes with local disk caching and offline fixture fallbacks; legislative site HTML redesigns require parser maintenance. |
| **C21** | **Automated Privacy & Secret Firewall Audits** | `scripts/privacy_audit.py`, `scripts/deep_security_audit.py` | Audit scripts | CLI: `python scripts/privacy_audit.py` | Working tree files, Git history, index metadata | Binary PASS/FAIL report verifying zero PII, zero tokens, zero local paths, zero tracked databases | Regex, Git subprocess | `tests/test_privacy_policy.py` | **IMPLEMENTED** | Enforces complete isolation between local development environments and public repository commits. |
| **C22** | **External Ground-Truth Benchmark Suite** | `evaluation/external_benchmark.py` | `run_external_benchmark()` | CLI execution | 10 external verifiable legal questions (bar exams, published appellate cases) | Precision, recall, citation accuracy, abstention correctness | Full reasoning stack | `tests/test_advanced_architecture.py` | **IMPLEMENTED** | Prevents self-evaluation bias by benchmarking against independently verifiable external legal records. |
| **C23** | **23 Task Family SFT Dataset Builder** | `legal_gpt/training/dataset_builder.py`, `training/schemas/dataset_schema.py` | `DatasetBuilder.generate_seeds()` | CLI / Training scripts | Task family name, count | List of validated `LegalTrainingExample` records | `training.schemas` | `tests/test_dataset_builder.py` | **IMPLEMENTED** | Priority seed datasets generated for 5 core families (50 examples); remaining 18 families utilize validated fallback schema generators. |
| **C24** | **GGUF 4-Bit Model Export Pipeline** | `training/export/gguf_pipeline.py` | `GGUFExportPipeline.export_to_gguf()` | CLI / Python script | Model path, quantization type (`Q4_K_M`, `Q8_0`) | Export manifest, quantized binary metadata | PyTorch, `llama.cpp` tools | `tests/test_model_ecosystem.py` | **SCAFFOLDED** | Scaffolds packaging, conversion, and quantization commands; execution requires local GPU training weights and `llama.cpp` binaries. |

---

## 2. Public User Needs Mapping & Gap Analysis

To determine how effectively Legal-GPT serves the public, each of the **39 specific public user needs (A through AM)** has been evaluated against the existing codebase.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PUBLIC USER NEEDS COVERAGE (A–AM)                     │
├────────────────────────────────┬────────────────────────────────────────────┤
│  FULLY IMPLEMENTED (EXISTS)    │ 16 Needs: B, C, D, E, H, I, J, K, M, N,    │
│                                │           Q, S, U, AJ, AK, AL, AM          │
├────────────────────────────────┼────────────────────────────────────────────┤
│  PARTIALLY IMPLEMENTED (PART.) │ 14 Needs: A, F, G, L, O, P, R, T, V, W,    │
│                                │           AA, AB, AF, AI                   │
├────────────────────────────────┼────────────────────────────────────────────┤
│  MISSING / UNIMPLEMENTED       │  9 Needs: X, Y, Z, AC, AD, AE, AG, AH      │
└────────────────────────────────┴────────────────────────────────────────────┘
```

---

### Detailed Needs Matrix

#### Category 1: Understanding the Legal Problem & Governing Authority

| Code | Public Need Description | Status | Current Codebase Implementation | Required Implementation for Full Public Utility |
|:---|:---|:---:|:---|:---|
| **A** | **Understand a legal problem** | **PARTIAL** | `agents/legal_orchestrator.py` identifies legal issues and generates plain-English explanations via `PersonaRenderer.render_self_represented()`. | Implement an interactive, conversational intake diagnostic that asks clarifying questions when facts are underspecified before generating analysis. |
| **B** | **Identify jurisdiction** | **EXISTS** | `core/jurisdiction.py` parses state, county, and tribal designations; locks jurisdiction; rejects contamination across state boundaries. | Expose a geographic reverse-geocoding lookup (Zip Code $\to$ County $\to$ Judicial District $\to$ Governing State Court). |
| **C** | **Identify applicable law** | **EXISTS** | `core/authority.py` and `SimpleHybridStore` retrieve controlling statutes, administrative codes, and binding precedents. | Expand statutory coverage beyond child welfare, civil rights, and constitutional law to include consumer debt, habitability, and family custody. |
| **D** | **Determine relevant dates** | **EXISTS** | `core/temporal.py` and `core/temporal_graph.py` (`LAW_AT_DATE`) evaluate statutory validity at specific calendar event dates. | Add automated date extraction from user narratives to automatically establish the point-in-time timeline without requiring explicit flag input. |
| **E** | **Find authoritative sources** | **EXISTS** | `core/citation_verifier.py` and `legal_registry` match citations against official government publishers (e.g. OLRC, Leg.wa.gov, ILGA, GPO). | Add direct canonical hyperlinks to official government legislative pages in all rendered outputs. |
| **F** | **Understand terminology** | **PARTIAL** | `PersonaRenderer.render_self_represented()` rephrases complex legal standards into plain terms (e.g. "urgent and immediate necessity" $\to$ "serious immediate danger"). | Add a dedicated `LegalGlossaryEngine` providing expandable definitions of procedural terms (e.g. "pro se", "rehearing", "clear and convincing", "interlocutory"). |

---

#### Category 2: Procedural Posture, Timelines, & Deadlines

| Code | Public Need Description | Status | Current Codebase Implementation | Required Implementation for Full Public Utility |
|:---|:---|:---:|:---|:---|
| **G** | **Identify procedural posture** | **PARTIAL** | `cps/lifecycle.py` maps 18 discrete procedural stages and identifies the current case stage based on facts. | Generalize procedural posture classification beyond CPS to general civil litigation (pre-filing, summons served, answer due, discovery, summary judgment, trial, appeal). |
| **H** | **Identify deadlines** | **EXISTS** | `cps/lifecycle.py` and `core/procedural_engine.py` define strict statutory deadlines (e.g. 72-hour shelter care, 48-hour emergency removal, 14-day adversary hearing, 24-hour Florida shelter rule). | Add an interactive "Deadline Calculator" that takes the event timestamp and computes exact calendar deadlines excluding weekends and legal holidays. |
| **I** | **Identify required notices** | **EXISTS** | `cps/due_process_audit.py` and `cps/parent_rights.py` check whether formal personal summons, 72-hour notice, or registered tribal mail was properly served. | Generate a printable "Notice Defect Checklist" that self-represented litigants can file with the court clerk to contest defective service. |
| **J** | **Identify hearings** | **EXISTS** | `core/procedural_engine.py` identifies mandatory court hearings associated with procedural stages (e.g. 72-hour shelter hearing, 90-day adjudication, 12-month permanency). | Provide a "Hearing Roadmap" explaining who will be in the courtroom, what the judge will decide, and what evidence is admissible. |
| **K** | **Identify available motions** | **EXISTS** | `core/procedural_engine.py` details available motions (e.g. Affidavit for Rehearing, § 1028 Return Application, Section 388 Modification) with filing prerequisites. | Expand procedural motion catalog to general civil motions (Motion to Quash Defective Service, Motion for Extension of Time, Motion for Continuance). |
| **L** | **Identify appeal/review mechanisms** | **PARTIAL** | `cps/lifecycle.py` Stage 18 includes appellate review; `procedural_engine` includes rehearing affidavits. | Add dedicated appellate guidance explaining Notice of Appeal filing deadlines (typically 30 days), stays pending appeal, and standard of review. |

---

#### Category 3: Rights, Violations, & Due Process

| Code | Public Need Description | Status | Current Codebase Implementation | Required Implementation for Full Public Utility |
|:---|:---|:---:|:---|:---|
| **M** | **Identify potential rights** | **EXISTS** | `cps/parent_rights.py` and `cps/due_process_audit.py` audit statutory right to counsel, visitation, relative placement preference, and active efforts. | Broaden rights discovery to tenant rights (warranty of habitability, anti-retaliation), debtor rights (FDCPA), and disability accommodations (ADA Title II). |
| **N** | **Identify potential violations** | **EXISTS** | `DueProcessAuditor` flags specific statutory and constitutional due process violations (e.g. lack of notice, denial of counsel, failure of reasonable efforts). | Provide clear actionable remedy cards for each violation detected (e.g. "Violated: RCW 13.34.065 $\to$ Remedy: File Form WPF JU 02.0200 within 72 hours"). |
| **O** | **Identify missing facts** | **PARTIAL** | `StandardLegalResponse.facts_that_could_change_result` lists factual ambiguities flagged during reasoning. | Convert missing facts into a guided question prompt that actively asks the user to fill in critical missing variables. |
| **P** | **Organize evidence** | **PARTIAL** | `cps/evidence_matrix.py` accepts structured evidence items and evaluates their sufficiency against statutory proof standards. | Build an end-user "Evidence Binder" tool allowing users to log, tag, and categorize documents (text messages, photos, lease agreements, receipts) into court-admissible exhibit lists. |
| **Q** | **Distinguish fact/allegation/opinion** | **EXISTS** | `cps/evidence_matrix.py` categorizes items into `UNVERIFIED_ALLEGATION`, `DISPUTED_FACT`, `ESTABLISHED_FACT`, and `DOCUMENTED_EXHIBIT`. | Create a visual "Evidentiary Weight Meter" showing litigants which of the agency's claims are uncorroborated hearsay versus documented facts. |

---

#### Category 4: Timelines, Case History, & Research

| Code | Public Need Description | Status | Current Codebase Implementation | Required Implementation for Full Public Utility |
|:---|:---|:---:|:---|:---|
| **R** | **Build a timeline** | **PARTIAL** | `core/temporal_graph.py` tracks versions across dates; `audit/ledger.py` logs chronological events. | Build a visual chronological case timeline generator that plots incident date, notice date, removal date, hearing date, and filing deadlines. |
| **S** | **Compare versions of law** | **EXISTS** | `knowledge_graph/point_in_time_diff.py` computes unified text diffs between statutes at two dates. | Add plain-English legislative impact summaries explaining how the statutory amendment changed the citizen's legal rights. |
| **T** | **Find related cases** | **PARTIAL** | `SimpleHybridStore` performs hybrid BM25 retrieval over appellate decisions; `citator_graph` tracks citing references. | Add natural-language semantic precedent matching to find "cases with facts like mine" in the user's judicial district. |
| **U** | **Find subsequent treatment** | **EXISTS** | `knowledge_graph/relational_graph.py` evaluates whether precedent remains good law or has been overruled, distinguished, or questioned. | Display clear visual Shepards/KeyCite-style badges (Green Check, Yellow Caution, Red Stop) in plain language. |

---

#### Category 5: Social Infrastructure, Legal Aid, & Institutional Navigation

| Code | Public Need Description | Status | Current Codebase Implementation | Required Implementation for Full Public Utility |
|:---|:---|:---:|:---|:---|
| **V** | **Find government services** | **PARTIAL** | `services/registry.py` indexes official ombudsman offices, family advocacy offices, and public agency contacts for WA, IL, OH. | Expand seed directory to cover municipal services, child support enforcement agencies, and housing authorities across all 50 states. |
| **W** | **Find legal aid** | **PARTIAL** | `services/registry.py` queries LSC-funded legal aid programs (e.g. Northwest Justice Project, Legal Aid Chicago, Legal Aid Society of Cleveland). | Integrate direct income-eligibility screener (e.g. 125% or 200% of Federal Poverty Guidelines) and online intake web links. |
| **X** | **Find advocacy organizations** | **MISSING** | `ServiceType` includes `PUBLIC_CONTACT` and `BAR_REFERRAL`, but non-governmental grassroots advocacy groups are not yet cataloged. | Create an index of verified non-profit family defense, civil liberties, and tenant union advocacy organizations. |
| **Y** | **Find public defenders** | **MISSING** | `cps/parent_rights.py` asserts right to counsel, but specific County Public Defender / Office of Public Defense contact details are not in `ServiceRegistry`. | Add `ServiceType.PUBLIC_DEFENDER` to `services/models.py` with county-by-county indigent defense office directories. |
| **Z** | **Find disability/mental-health resources** | **MISSING** | `CivilMatterType.DISABILITY` is defined in schema, but seed files currently focus on family CPS and civil legal aid. | Populate seed directories with state Protection & Advocacy (P&A) agencies, ADA legal centers, and community mental health crisis resources. |
| **AA** | **Find child/family services** | **PARTIAL** | `seeds/wa_services.yaml`, `il_services.yaml`, `oh_services.yaml` include kinship navigators and family support networks. | Expand to all 50 states; catalog subsidized daycare, parenting education, and family preservation resources. |
| **AB** | **Understand administrative processes** | **PARTIAL** | `cps/lifecycle.py` outlines investigation, safety planning, and voluntary services administrative phases. | Document formal administrative appeal processes (e.g. challenging a "founded" or "substantiated" CPS finding on the state central child abuse registry). |

---

#### Category 6: Practical Preparation & Document Assistance

| Code | Public Need Description | Status | Current Codebase Implementation | Required Implementation for Full Public Utility |
|:---|:---|:---:|:---|:---|
| **AC** | **Prepare questions for an attorney** | **MISSING** | `PersonaRenderer.render_self_represented()` lists general verification items, but no dedicated attorney consultation preparation module exists. | Create an automated "Attorney Consultation Brief Generator" that formats a 1-page case summary with specific targeted questions to ask an attorney. |
| **AD** | **Prepare questions for a caseworker** | **MISSING** | Not specifically implemented. | Build a "Caseworker Meeting Script & Question Checklist" (e.g. asking for specific service referrals in writing, requesting visit schedules, clarifying safety plan requirements). |
| **AE** | **Prepare questions for a court hearing** | **MISSING** | `PersonaRenderer.render_self_represented()` includes what to ask the judge (e.g. requesting appointed counsel), but no cross-examination questions. | Generate a "Pro Se Court Hearing Guide" with suggested questions for cross-examining the caseworker on missing evidence. |
| **AF** | **Prepare document checklists** | **PARTIAL** | `PersonaRenderer.render_self_represented()` Section 4 and `ProceduralMotionGuide.required_exhibits_and_forms` list required documents. | Provide downloadable, customized document gathering checklists (e.g. proof of income, clean drug screen results, lease agreements, character reference letters). |
| **AG** | **Generate research plans** | **MISSING** | Internal orchestrator executes research, but does not output a step-by-step self-help research roadmap for the citizen. | Implement a "Legal Research Action Plan" module detailing: which statutes to read, what court rules apply, and which court forms to request from the clerk. |
| **AH** | **Explain legal documents** | **MISSING** | Ingestion pipeline parses statutes/cases, but the system has no dedicated endpoint to ingest a user's notice, petition, or order and explain it clause-by-clause. | Build a "Document Explainer" tool that accepts text from a summons, protective custody order, or petition and produces a plain-English clause breakdown. |

---

#### Category 7: Epistemic Integrity & Safety Guards

| Code | Public Need Description | Status | Current Codebase Implementation | Required Implementation for Full Public Utility |
|:---|:---|:---:|:---|:---|
| **AI** | **Compare competing interpretations** | **PARTIAL** | `agents/adversarial_reviewer.py` generates opposing theories and counterarguments. | Provide side-by-side comparative views of agency argument versus defense counterargument. |
| **AJ** | **Identify uncertainty** | **EXISTS** | `agents/legal_orchestrator.py` and `FinalReviewAgent` force `confidence_level = "Uncertain"` and mandate explicit warnings when evidence or law is ambiguous. | Maintain existing safety gating; add visual confidence indicators in the user interface. |
| **AK** | **Detect missing authority** | **EXISTS** | `agents/legal_orchestrator.py` triggers `abstention_state = "ABSTAIN"` when no controlling authority can be verified for the target jurisdiction. | Maintain zero-tolerance hallucination policy; refuse to generate legal conclusions without verified authority. |
| **AL** | **Detect jurisdiction contamination** | **EXISTS** | `core/jurisdiction.py` (`JurisdictionLockEngine`) actively blocks out-of-state statutes from contaminating answers. | Maintain strict state-level isolation firewalls. |
| **AM** | **Detect outdated law** | **EXISTS** | `core/temporal_graph.py` checks effective dates and flags repealed, amended, or sunsetted statutes as `superseded = True`. | Maintain point-in-time temporal verification across all citation resolution paths. |

---

## 3. Resource Gap Analysis: Core Intelligence vs. Public Navigation

There is a fundamental difference between **legal intelligence** (what Legal-GPT's core reasoning engine does) and **public legal navigation** (what an ordinary person actually needs).

```
┌──────────────────────────────────────────────┐       ┌──────────────────────────────────────────────┐
│        LEGAL-GPT CORE (BACKEND)              │       │     PUBLIC USER EXPERIENCE (NEED)            │
│ - Raw statutory citations (RCW 13.34.065)    │  VS.  │ - "When do I get to see my child?"           │
│ - 14-Tier authority decimal scores (0.92)    │       │ - "Can the caseworker enter without warrant?"│
│ - Shepard's signals (GOOD_LAW)               │       │ - "What do I say to the judge tomorrow?"     │
│ - JSON RPC 2.0 / MCP protocols               │       │ - "Where is the nearest legal aid office?"   │
│ - Pleading markdown templates                │       │ - "Help me organize my drug test records"    │
└──────────────────────────────────────────────┘       └──────────────────────────────────────────────┘
```

### Key Gaps Identified:

1. **The Ingestion vs. Interaction Gap:**
   Legal-GPT excels at taking a legal query and producing a multi-stage citation-verified answer. However, an ordinary person in crisis rarely knows how to frame a legally precise query. They present emotional, unstructured, incomplete narratives ("CPS took my baby from daycare yesterday and won't tell me where she is"). The system needs an **Intake & Triage Layer** that guides the user to supply critical parameters (state, date of removal, whether court papers were signed, whether police were present) before executing legal analysis.

2. **The Procedural Motion vs. E-Filing Gap:**
   `PleadingGenerator` generates valid court pleading drafts, but a self-represented litigant does not know what to do with markdown text. They need step-by-step filing instructions: "Print 3 copies, go to Room 204 at 8:30 AM, pay the filing fee or ask for a fee waiver (GR 34), hand one copy to the clerk, and have someone over 18 serve the agency."

3. **The Services Directory Depth Gap:**
   `ServiceRegistry` has high architectural fidelity with SHA-256 integrity hashing and Pydantic schemas, but its seed data currently covers only WA, IL, OH, and Federal. For national public utility, it must expand to all 50 states, covering legal aid, public defender offices, court facilitator help desks, and emergency community services.

4. **The User Document Understanding Gap:**
   Ordinary citizens receive dense court orders, notice of hearings, and caseworker service plans. Legal-GPT currently has no mechanism for a user to paste text from an order and ask: "What does this mean for me right now?"

---

## 4. Public-Service Layer: The "Public Legal Navigator"

To bridge the gap between backend legal intelligence and the needs of ordinary people, Legal-GPT should expose a dedicated, citizen-facing module: **The Public Legal Navigator**.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 PUBLIC LEGAL NAVIGATOR                                      │
├───────────────────────────────┬───────────────────────────────┬─────────────────────────────┤
│        1. TRIAGE & INTAKE     │       2. RIGHTS & REMEDIES    │    3. PROCEDURAL ROADMAP    │
│ - Crisis Question Diagnostic  │ - Fundamental Rights Checker  │ - Step-by-Step Action Plan  │
│ - Jurisdiction Auto-Resolver  │ - Due Process Violation Audit │ - Court Appearance Script   │
│ - Key Date & Timeline Builder │ - Defect & Defense Discovery  │ - Form & Filing Checklist   │
├───────────────────────────────┼───────────────────────────────┼─────────────────────────────┤
│     4. EVIDENCE ORGANIZER     │     5. DOCUMENT TRANSLATOR    │    6. DIRECTORY & ROUTING   │
│ - Exhibit Categorization      │ - Court Order Explainer       │ - Verified Legal Aid Search │
│ - Fact vs. Allegation Matrix  │ - Plain-English Clause Diff   │ - Public Defender Locator   │
│ - Rebuttal Evidence Checklist │ - Jargon & Terminology Decoder│ - Court Facilitator Helpdesk│
└───────────────────────────────┴───────────────────────────────┴─────────────────────────────┘
```

### The 12 Sub-Modules of the Public Legal Navigator:

1. **Legal Research Module (`navigator/research.py`):**  
   Translates everyday language into targeted statutory and caselaw inquiries, returning plain-language summaries with clickable official links.
2. **Rights Discovery Module (`navigator/rights.py`):**  
   Evaluates user circumstances to identify fundamental rights (e.g. right to silence with investigators, right to court-appointed counsel, right to regular family visitation).
3. **Procedure Discovery Module (`navigator/procedure.py`):**  
   Identifies exact procedural options, available motions, mandatory deadlines, and formal filing prerequisites based on the case's current stage.
4. **Evidence Organization Module (`navigator/evidence.py`):**  
   Provides an interactive workspace where litigants can input case facts, categorize exhibits, separate agency allegations from proven facts, and identify missing proof.
5. **Timeline Construction Module (`navigator/timeline.py`):**  
   Builds an authoritative chronological timeline of events, automatically calculating statutory deadlines and highlighting procedural delays or statutory violations.
6. **Document Understanding Module (`navigator/document_explainer.py`):**  
   Allows users to paste excerpts from notices, safety plans, or court orders to receive line-by-line plain-English explanations and immediate action items.
7. **Service Discovery Module (`navigator/services.py`):**  
   Connects users directly with official government ombudsman offices, family advocacy programs, and local social services.
8. **Legal-Aid Discovery Module (`navigator/legal_aid.py`):**  
   Filters LSC and non-profit legal aid providers by user county and matter type, providing verified telephone numbers and intake links.
9. **Court Navigation Module (`navigator/court.py`):**  
   Provides courthouse directories, self-help facilitator hours, fee waiver instructions, and decorum/hearing appearance guidelines.
10. **Agency Navigation Module (`navigator/agency.py`):**  
    Explains how administrative child welfare agencies function, parents' rights during investigations, and how to contest administrative findings.
11. **Appeal Navigation Module (`navigator/appeals.py`):**  
    Explains post-order review mechanisms, including motions for reconsideration, statutory rehearing affidavits, and notices of appeal.
12. **Research Planning Module (`navigator/planning.py`):**  
    Synthesizes the entire matter into a prioritized, printable "Self-Advocacy Action Plan" with document checklists, attorney questions, and key deadlines.

---

## 5. Epistemic Safety & Risk Mitigation

Public legal assistance involves high stakes: loss of child custody, homelessness, or financial ruin. Below is an audit of potential system failure modes and recommended safeguards.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 SAFETY & INTEGRITY GATES                                    │
├───────────────────────────────┬───────────────────────────────┬─────────────────────────────┤
│         FAILURE MODE          │             RISK              │     ENFORCED SAFEGUARD      │
├───────────────────────────────┼───────────────────────────────┼─────────────────────────────┤
│ Fabricating Law               │ Citations to nonexistent code │ CitationVerifier + T0 Gate  │
│ Fabricating Services          │ Fake phone numbers or URLs    │ SHA-256 Registry Integrity  │
│ Fabricating Deadlines         │ Missing court appearances     │ Statutory Deadline Engine   │
│ Jurisdiction Contamination    │ Applying CA law to TX case    │ Hard Jurisdiction Lock      │
│ Outdated Law Confusion        │ Applying repealed statutes    │ LAW_AT_DATE Temporal Graph  │
│ Allegations Treated as Facts  │ Biased or unfair analysis     │ Evidence Sufficiency Matrix │
│ Overstating Certainty         │ False confidence to litigant  │ NLI Safety Gate + Abstain   │
│ Implied Representation        │ Unauthorized practice of law  │ Mandatory Educational Notice│
└───────────────────────────────┴───────────────────────────────┴─────────────────────────────┘
```

### Detailed Safeguards:

1. **Fabricating Law / Phantom Citations:**
   - *Risk:* Hallucinating a nonexistent statutory subsection or phantom case precedent.
   - *Safeguard:* The `CitationVerifier` rejects any citation not verified against the machine-readable registry or ingested caselaw database. `FinalReviewAgent` Check 1 blocks any holding statement lacking a verified citation.

2. **Fabricating Public Services or Hotlines:**
   - *Risk:* Providing a disconnected phone number, commercial referral mill, or scam website to a vulnerable litigant.
   - *Safeguard:* All service records in `ServiceRegistry` must originate from human-curated YAML files with `is_official: True` and SHA-256 cryptographic payload hashing. The LLM is prohibited from inventing service contacts.

3. **Fabricating or Miscalculating Deadlines:**
   - *Risk:* Misinforming a parent that they have 30 days to respond when state law requires action within 72 hours, resulting in default judgment.
   - *Safeguard:* Deadlines are derived deterministically from `core/procedural_engine.py` and `cps/lifecycle.py` rules, never free-generated by the LLM without statutory backing.

4. **Jurisdiction Contamination:**
   - *Risk:* Recommending an Illinois 48-hour temporary custody motion to a parent in Washington whose rights are governed by RCW 13.34.065.
   - *Safeguard:* The `JurisdictionEngine` enforces strict jurisdiction locking. Cross-jurisdiction references trigger automated rejection unless explicitly compared in an interstate UCCJEA context.

5. **Confusing Historical and Operative Law:**
   - *Risk:* Citing a pre-2021 statute that did not require reasonable efforts before removal.
   - *Safeguard:* The `TemporalGraph` evaluates statutory text at the specific `LAW_AT_DATE`. If an amendment has superseded the text, the system flags the statute as superseded.

6. **Treating Unverified Allegations as Established Facts:**
   - *Risk:* The AI accepts a caseworker's unproven allegation ("Mother is unfit") as fact and advises the parent that they cannot win.
   - *Safeguard:* The `EvidenceMatrixEngine` classifies assertions into `UNVERIFIED_ALLEGATION` vs. `DOCUMENTED_EXHIBIT`. `FinalReviewAgent` Check 3 specifically forbids presenting allegations as established facts or law.

7. **Overstating Certainty & Failure to Abstain:**
   - *Risk:* Providing a definitive outcome prediction in a highly discretionary custody determination.
   - *Safeguard:* `FinalReviewAgent` Check 2 enforces epistemic uncertainty markers. When governing law is missing or ambiguous, `LegalGPTOrchestrator` sets `confidence_level = "Uncertain"` and triggers explicit abstention (`abstention_state: "ABSTAIN"`).

8. **Implying Representation (Unauthorized Practice of Law):**
   - *Risk:* A user believes Legal-GPT is their legal attorney and fails to request court-appointed counsel.
   - *Safeguard:* Every response across CLI, REST, and MCP includes an unavoidable, prominent educational disclaimer:  
     > *"⚠️ IMPORTANT NOTICE: Legal-GPT is an automated legal intelligence research tool for educational and informational purposes only. It is not an attorney, cannot provide formal legal advice, and does not create an attorney-client relationship. You should immediately request your court-appointed attorney at your very first hearing."*

---

## 6. Testing, Verification, & Quality Assurance Requirements

To guarantee reliability as a public resource, Legal-GPT enforces a rigorous multi-layered testing regimen:

1. **Unit & Regression Testing (173 Tests Currently Passing):**
   - All engines (`jurisdiction`, `authority`, `temporal`, `citator`, `procedural`, `evidence`, `pleadings`) are covered by automated unit tests in `tests/`.
2. **Dual-Benchmark Evaluation:**
   - **Internal 50-Scenario Benchmark (`benchmarks/scenarios.py`):** Multi-jurisdictional battery evaluating CPS emergency removal, ICWA compliance, UCCJEA interstate jurisdiction, parental rights, and temporal diffs.
   - **External 10-Case Verifiable Benchmark (`evaluation/external_benchmark.py`):** Real-world legal hypos derived from external bar exam questions, published state appellate decisions, and federal administrative rulemaking, scored for citation accuracy and hallucination rate.
3. **Automated Privacy & Secret Audits:**
   - `python scripts/privacy_audit.py` scans working tree files for unauthorized personal identifiers or confidential data.
   - `python scripts/deep_security_audit.py` scans entire Git commit histories, branch refs, and `.gitignore` compliance to prevent credentials, private tokens, or SQLite databases from entering the repository.

---

## 7. Prioritized Public Benefit Implementation Roadmap

Below is the phased, prioritized roadmap to elevate Legal-GPT into a comprehensive, public-facing legal navigation system.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 IMPLEMENTATION ROADMAP                                      │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 1: Immediate Enhancements (Weeks 1–2)                                                 │
│ • CLI Public Service & Navigator Commands (`legal-gpt services`, `legal-gpt navigate`)      │
│ • Expansion of Civil Services Registry to top 10 populated states                           │
│ • Interactive Statutory Deadline Calculator                                                 │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 2: Practical Litigant Tooling (Weeks 3–4)                                             │
│ • Attorney Consultation Brief & Caseworker Meeting Question Generators                      │
│ • Pro Se Document Checklist & Hearing Appearance Preparation Guides                         │
│ • Court Order & Legal Document Explainer Tool (`explain_document`)                          │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 3: Evidentiary & Timeline Interactive Layer (Weeks 5–6)                               │
│ • Interactive Case Timeline Builder with statutory milestone visualization                  │
│ • Self-Advocate Evidence Binder & Exhibit Indexing Interface                                │
│ • Expanded Civil Motions (Eviction defense, Debt dispute, Civil rights)                     │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 4: Full Multi-State Service Directory (Weeks 7–8)                                     │
│ • Complete 50-state LSC legal aid and public defender directory                             │
│ • Automated Legal Aid Income & Eligibility Screening Engine                                 │
│ • Integration with Court Facilitator and Self-Help Center directories                       │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 5: Open-Weight Public Deployment (Weeks 9–10)                                         │
│ • Full SFT multi-stage training across all 23 task families (50,000+ examples)              │
│ • Release of quantized GGUF models (`Q4_K_M`, `Q8_0`) for local, private execution          │
│ • Web & Mobile responsive Public Legal Navigator frontend client                            │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Conclusion

Legal-GPT possesses a rare, exceptionally strong foundational core: strict jurisdiction locking, a 14-tier dynamic authority hierarchy, point-in-time statutory resolution, Shepard's-style citation verification, and an 18-stage child welfare lifecycle engine.

By wrapping these verified backend reasoning capabilities in the **Public Legal Navigator** layer—translating dense statutes into plain-language deadlines, checklists, evidence matrices, and official legal aid connections—Legal-GPT can realize its mission as a transformative public infrastructure project for ordinary citizens navigating the legal system.
