# Contributing Data, Law, and Resources to Legal-GPT

Thank you for contributing to **Legal-GPT**, an open, public-benefit legal intelligence platform.

Legal-GPT is designed to provide ordinary individuals, advocates, researchers, and legal professionals with accurate, jurisdiction-locked, and verifiable legal information. Because individuals rely on this platform during critical moments—such as child welfare investigations, eviction proceedings, or administrative hearings—**accuracy and epistemic integrity are our highest priorities**.

---

## 1. The Core Authority Isolation Rule

> [!IMPORTANT]
> **Community submissions NEVER automatically become authoritative legal sources.**
> 
> All contributed data, statutes, cases, policies, datasets, and benchmark scenarios enter an **unverified quarantine layer** with state `PROPOSED`. They are **strictly isolated from the authoritative legal registry and citator graph** until they pass our formal multi-stage verification pipeline.

---

## 2. Supported Contribution Types

We welcome 16 distinct categories of contributions:

1. **`LEGAL_SOURCE`**: New primary legal sources (e.g. official legislative code portals, slip opinion feeds).
2. **`SOURCE_METADATA`**: Structured metadata for existing sources (e.g. publication dates, update frequencies).
3. **`JURISDICTION`**: Definitions and boundaries for counties, municipal courts, tribal nations, or judicial districts.
4. **`CASE`**: Binding or persuasive appellate court opinions, citations, and procedural holdings.
5. **`STATUTE`**: Codified legislative acts, section numbers, effective dates, and statutory text.
6. **`REGULATION`**: Administrative codes, agency rules (e.g. WAC, ILCS, CCR, eCFR).
7. **`COURT_RULE`**: Local, state, or federal procedural court rules (e.g. Juvenile Court Rules, Local Superior Court Rules).
8. **`AGENCY_POLICY`**: Publicly available administrative policy manuals, practice guides, or operational bulletins.
9. **`RESOURCE`**: Verified civil legal aid organizations, public defenders, self-help clinics, or ombuds offices.
10. **`DATASET`**: Curriculum seed templates, synthetic evaluation datasets, or domain classification corpora.
11. **`TEST_CASE`**: Regression test fixtures verifying statutory deadlines or jurisdictional constraints.
12. **`BENCHMARK`**: Real-world legal scenarios for measuring precision, hallucination avoidance, and citation accuracy.
13. **`BUG_REPORT`**: Notifications of misapplied law, broken source links, or out-of-date statutory versions.
14. **`DOCUMENTATION`**: Architectural guides, legal literacy explainers, or developer documentation.
15. **`TRANSLATION`**: High-fidelity, verified translations of legal explanations and plain-English resources.
16. **`LEGAL_LITERACY_MATERIAL`**: Multi-level conceptual explanations breaking down complex legal doctrine into plain English.

---

## 3. Mandatory Contribution Fields

Every contribution—regardless of type—must include the 9 mandatory metadata fields:

| Field | Description | Example |
| :--- | :--- | :--- |
| `source` | The primary legal citation, official document title, or source identifier. | `"RCW 13.34.065"` or `"Santosky v. Kramer, 455 U.S. 745"` |
| `submitter` | Contributor identity or pseudonymous handle and affiliation. | `"JaneDoe (Legal Aid of WA)"` or `"advocate-402"` |
| `date` | Submission timestamp in ISO format (`YYYY-MM-DD`). | `"2026-09-17"` |
| `jurisdiction` | Standardized jurisdiction code. | `"US-WA"`, `"US-IL"`, `"US-TRIBAL-NAVAJO"`, `"US"` |
| `authority_type` | Hierarchical authority classification. | `"T0_CONSTITUTIONAL"`, `"T5_STATE_STATUTE"`, `"RESOURCE"` |
| `effective_date` | Enactment, effective range, or version date (if applicable). | `"2021-07-01"` |
| `provenance` | Complete origin trace, official URL, or repository link. | `"https://leg.wa.gov/CodeReviser/Pages/RCW13.34.065.aspx"` |
| `license` | Permissive open-data license. | `"CC0-1.0"` (Public Domain Law), `"Apache-2.0"`, `"MIT"` |
| `verification_state` | Initial state must always be `PROPOSED`. | `"PROPOSED"` |

---

## 4. Licensing Requirements

- **Primary Law (Constitutions, Statutes, Judicial Opinions, Regulations)**: Must be licensed as **CC0 1.0 Universal / Public Domain**. Primary edicts of government cannot be copyrighted.
- **Agency Policies & Public Guides**: Must be public government records free of commercial distribution restrictions.
- **Datasets, Benchmarks, and Code**: Must be licensed under **Apache 2.0** or **MIT**.

---

## 5. Privacy & Data Safety Rules

> [!CAUTION]
> **NO PRIVATE CASE EVIDENCE, DOCKET CONFIDENTIALITY BREACHES, OR PII ALLOWED.**
> 
> - Never submit private, non-public court pleadings, confidential child welfare case records, sealed filings, or personal identifying information (names of children, SSNs, addresses, phone numbers of litigants).
> - All factual examples submitted for benchmarks or literacy materials must be completely anonymized, synthesized, or derived from published appellate opinions.
> - Any submission containing private data will be immediately rejected and permanently purged.

---

## 6. How to Submit

1. Review [SOURCE_SUBMISSION_SCHEMA.md](SOURCE_SUBMISSION_SCHEMA.md) for field requirements.
2. Structure your submission in JSON format.
3. Submit a Pull Request or use the `core/contributions` programmatic workflow API.
4. Track review progress via [VERIFICATION_WORKFLOW.md](VERIFICATION_WORKFLOW.md) and [PROVENANCE_MODEL.md](PROVENANCE_MODEL.md).
