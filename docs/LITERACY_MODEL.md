# Legal-GPT: Legal Literacy Model (v1.0 Architecture)

The Legal Literacy Model (`core/literacy/`) provides a multi-level legal education and progressive disclosure system. It translates complex statutory frameworks, constitutional doctrines, and court procedures into accessible explanations without stripping away critical legal nuance or fabricating legal authority.

---

## 1. Five Progressive Literacy Levels

The model structures every legal concept across five rigorous tiers:

1. **Level 1 — Plain English (Intuitive):**
   - High-clarity, everyday language explaining the core concept.
   - Avoids legal jargon while strictly avoiding false simplicity (e.g. never claims "the state can never enter your home").
2. **Level 2 — Practical Explanation (Situational Context):**
   - Explains what an individual actually observes or experiences in real life (e.g. notices received, paperwork served, courtroom hearing appearances).
3. **Level 3 — Legal Terminology & Doctrine:**
   - Formal legal doctrines, balancing tests, standards of review, and jurisdictional terminology.
4. **Level 4 — Primary Authority Grounding:**
   - Concrete, verified constitutional provisions, statutes, court rules, and judicial precedents.
   - Every reference includes verified citation string, source type, official government portal URL, and binding status.
5. **Level 5 — Advanced Legal Analysis:**
   - Competing judicial doctrines, federal circuit splits, historical evolutions, and statutory construction tensions.

---

## 2. Five On-Demand Drill-Down Actions

Every concept provides structured on-demand drill-downs:

- **`SHOW_SOURCE` ("Show me the source."):** Official government portal URLs and verified repository links.
- **`SHOW_STATUTE` ("Show me the statute."):** Controlling statutory provisions from official legislative codes.
- **`SHOW_CASE` ("Show me the case."):** Controlling appellate and Supreme Court slip opinions or official reporter citations.
- **`EXPLAIN_OPPOSING` ("Explain the opposing interpretation."):** Adversarial interpretations (e.g. agency *parens patriae* arguments vs. parent family-integrity arguments).
- **`SHOW_TEMPORAL_CHANGE` ("Show me what changed over time."):** Legislative amendment history, point-in-time evolutions, and statutory revisions.

---

## 3. Verification Claims and Limitations

In accordance with the project's Safety and Claims Audit (`docs/LEGAL_CLAIMS_AUDIT.md`), the Legal Literacy Engine operates under strict verification parameters:

1. **Verification-Gated, Not Infallible:**
   - Legal-GPT does not claim mathematical "zero hallucination."
   - The Literacy Model enforces an **abstention-first architecture**. If primary authority for a requested jurisdiction is absent from `legal_registry`, the engine returns `PARTIAL` or `ABSTAIN`, refusing to synthesize placeholder citations.
2. **Jurisdiction Isolation:**
   - Authority is segregated by jurisdiction. When a user requests an explanation under Washington law (`WA`), the engine will never present Illinois (`IL`) or California (`CA`) statutes as binding authority. Persuasive or foreign authorities are explicitly tagged as non-binding.
3. **Primary Authority URLs:**
   - Level 4 citations must link to verified official government sources (e.g., `govinfo.gov`, state legislature official portals, `supremecourt.gov`). Unofficial blogs or commercial summaries are prohibited as primary sources.
4. **No Judicial Determination / Non-Adjudicative:**
   - The engine provides educational legal literacy only. It never declares that a user's rights were violated or makes definitive predictions of case outcomes.
5. **Citator Treatment:**
   - Citator cross-references rely on the project's internal relational treatment graph, not proprietary commercial citator services.

---

## 4. Concept Packing Architecture & Pack A Inventory

Concepts are stored as structured YAML files in:
`legal_registry/literacy/concepts/{concept_id}.yaml`

Each concept YAML file defines:
- `id`: Unique identifier (e.g. `due_process`, `shelter_care_hearing`).
- `canonical_name`: Formal legal name.
- `aliases`: Recognized search terms and synonyms.
- `jurisdiction`: Primary jurisdiction (`US` or two-letter state code).
- `level_1_plain_english`: Plain English prose.
- `level_2_practical`: Real-world operational context.
- `level_3_terminology`: Doctrinal distinctions.
- `level_4_primary_authority`: List of structured authority records with official URLs.
- `level_5_advanced_analysis`: Doctrinal tensions and circuit splits.
- `drill_downs`: Pre-computed or verified drill-down responses.
- `retrieved_date`: ISO date when statutory text was verified.

### Concept Pack A (Foundational Family & Constitutional Law):
1. `due_process.yaml`: Fourteenth Amendment Procedural and Substantive Due Process (*Mathews v. Eldridge*, *Santosky v. Kramer*, RCW 13.34.065).
2. `notice.yaml`: Procedural Due Process Notice Command (*Mullane*, *Armstrong v. Manzo*, WA JuCR 2.1).
3. `opportunity_to_be_heard.yaml`: Adversarial Hearing Rights (*Mathews*, *Stanley v. Illinois*, RCW 13.34.090).
4. `right_to_counsel_dependency.yaml`: Indigent Parent Defense in Custody Proceedings (*Lassiter*, *In re Dependency of Grove*, RCW 13.34.090).
5. `emergency_removal.yaml`: Fourth Amendment Warrant Requirement & Exigent Circumstances (*Wallis v. Spencer*, RCW 13.34.050).
6. `shelter_care_hearing.yaml`: 72-Hour Initial Custody Hearing Strict Deadlines (RCW 13.34.065, 705 ILCS 405/2-9).
7. `probable_cause_vs_preponderance.yaml`: Evidentiary Burdens of Proof (*Santosky*, RCW 13.34.050, RCW 13.34.130).
8. `icwa_inquiry.yaml`: Indian Child Welfare Act Mandatory Inquiry Standard (25 U.S.C. § 1912, 25 C.F.R. § 23.107, RCW 13.38.050).
9. `active_efforts.yaml`: ICWA Active Efforts vs. State Reasonable Efforts (25 U.S.C. § 1912(d), *Haaland v. Brackeen*, RCW 13.38.040).
10. `reasonable_efforts.yaml`: Title IV-E Mandatory Remedial Services (42 U.S.C. § 671(a)(15), RCW 13.34.136).
11. `permanency_planning.yaml`: 12-Month Permanency Review & ASFA 15/22 Clock (42 U.S.C. § 675(5)(C), RCW 13.34.145).
12. `appeal_or_revision_dependency.yaml`: Motion for Revision & Interlocutory Appeal (Wash. Const. art. IV, § 23, RCW 2.24.050, RAP 2.2).

---

## 5. Public Interfaces & Truth Engine Integration

### Truth Engine Wiring:
- **`CitationVerifier`**: Every Level 4 authority row is passed through canonical regex and official registry validation. Any tampered or unrecognized citation is downgraded to `UNVERIFIED`, preventing concepts from falsely claiming `VERIFIED` status.
- **`temporal_graph`**: The `SHOW_TEMPORAL_CHANGE` action verifies point-in-time statutory versions (e.g. Washington 2021 SB 5118 amending RCW 13.34.065). If temporal history or enactment dates are missing/unverified, the engine explicitly abstains.
- **`ExplanationTraceEngine`**: Emits auditable 10-field explanation traces and powers 8 interrogative queries (`WHY`, `SOURCE`, `WHEN`, `WHERE`, `WHAT_IF`, `WHAT_CHANGED`, `WHAT_DISAGREES`, `WHAT_IS_MISSING`) grounded in primary authority.

### Public API:
- `POST /api/v1/public/explain-concept`: Exposes verified concept breakdowns across levels 1–5, complete with drill-down execution and verification status reporting.

### Command Line Interface:
- `legal-gpt explain-concept --concept <id> [--state <ST>] [--level <1-5>] [--drill-down <ACTION>] [--json]`

---

## 6. Public Law Scout Bridge

Public Law Scout acts as the conversational interface for the Legal Literacy Model:
- Scout formats Level 1 and Level 2 explanations for public users.
- Scout links directly to official portal URLs provided in Level 4.
- Scout **never invents or synthesizes Level 4 citations**. If Level 4 authority is unverified or marked `ABSTAIN`, Scout transparently states that verified primary authority is not currently packed for that jurisdiction.

---

## 7. Current Gaps & Roadmap

- **Concept Breadth:** Pack A covers 12 foundational CPS, family, and due-process concepts. Future packs (Pack B, Pack C) will cover housing, consumer debt, disability rights, and immigration.
- **Opposing Interpretations:** While Pack A provides verified opposing legal theories grounded in caselaw, non-packed concepts currently abstain rather than speculating.
- **Temporal Depth:** Point-in-time historical versions are currently grounded in major statutory enactments (e.g. ASFA 1997, Keeping Families Together Act 2021). Detailed section-by-section historical diffs remain an ongoing expansion milestone.
