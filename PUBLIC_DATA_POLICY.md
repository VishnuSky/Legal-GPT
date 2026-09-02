# PUBLIC DATA & REPOSITORY SECURITY POLICY

> [!CAUTION]
> **THIS IS A PUBLIC REPOSITORY.**
> **PRIVATE CASE DATA, PERSONAL IDENTIFYING INFORMATION (PII), PROPRIETARY DATA, CREDENTIALS, EVIDENCE FILES, OR CONTENT FROM UNRELATED PROJECTS MUST NEVER BE COMMITTED OR PUSHED.**

---

## 1. Core Operating Principle

**Assume all external directories, files, databases, and projects are STRICTLY PRIVATE unless explicitly authorized as `PUBLIC-SAFE FOR LEGAL-GPT`.**

If you cannot verify that a document, dataset, example, citation, or prompt is intentionally and demonstrably public-safe, it must remain entirely outside this repository.

---

## 2. Public vs. Private Data Boundary

### Allowed in Legal-GPT (Public-Safe Core):
1. **Public-Domain Legal Information**: Constitutions, public statutes, administrative codes, published judicial opinions, official court rules.
2. **Public Government & Agency Policy**: Published agency policy manuals (e.g., DCYF, DCFS, ODJFS, CDSS, DFPS, OCFS).
3. **Public Government APIs & Metadata**: Documented public endpoints (GovInfo, CourtListener, Library of Congress).
4. **Original Source Code**: Code explicitly written for the open-source Legal-GPT architecture.
5. **Synthetic & Anonymized Benchmark Data**: Fully synthetic, fictionalized scenarios (e.g., `PERSON_A`, `CHILD_A`, `COUNTY_A`).
6. **Open-Source Documentation**: Architectural diagrams, educational guides, and standard developer documentation.

### Absolute Prohibitions (Never Permitted in this Repository):
- **Personal Identifying Information (PII)**: Real names in personal legal contexts, home addresses, phone numbers, personal emails, SSNs, financial/banking data, tax info, family records.
- **Private Legal & CPS Case Files**: Personal court filings, sealed dockets, guardian ad litem reports, CPS investigation logs, private correspondence.
- **Evidence Collections & Forensic Media**: Audio recordings, video footage, body-camera evidence, police reports obtained privately, OCR outputs, personal transcripts, timeline notes.
- **Credentials & Secrets**: API keys, tokens, SSH keys, passwords, certificates, OAuth secrets, database credentials, connection strings.
- **Private Infrastructure Metadata**: Hardcoded local machine filesystem paths (such as user profile paths, local drives, or home directories), internal IP addresses, local network domain names, or workstation identifiers.
- **Unrelated Project Materials**: Code, databases, indexes, or documentation from other workspaces or personal repositories (e.g., Evidence Manager, AI Swarms, VR/forensics, model training scripts).
- **Private AI Artifacts**: Transcripts of private conversations with ChatGPT, Claude, Gemini, or Antigravity containing confidential or personal context.

---

## 3. Project Firewalls & Interface Boundary

Legal-GPT operates as a modular, standalone legal intelligence core. Interoperability with external tools (such as case or evidence management systems) must always occur through **controlled, public-safe API interfaces**, never by importing or copying private project files or databases into this repository.

```
       🟢 PUBLIC REPOSITORY (Legal-GPT)
     ┌───────────────────────────────────┐
     │  - Statutory & Case Registries    │
     │  - Temporal & Procedure Engines   │
     │  - Proposition & Citation Verifier│
     │  - Synthetic Benchmarks           │
     └─────────────────┬─────────────────┘
                       │
             Public REST / MCP API
                       │
     ┌─────────────────▼─────────────────┐
     │  🔴 EXTERNAL / PRIVATE SYSTEMS    │
     │  (Evidence Manager, Private Dbs)  │
     └───────────────────────────────────┘
```

---

## 4. Synthetic Case Data Protocol

When writing test fixtures, CLI prompts, benchmark scenarios, or user-facing documentation:
- **Always use synthetic identifiers**: E.g., `PERSON_A`, `PARENT_1`, `CHILD_X`, `COUNTY_REF`, `STATE_WA`.
- **Never use real personal legal facts or private dispute details.**
- **Ground all legal rules in published statutory sections and cited appellate holdings.**

---

## 5. Secret & PII Scanning Gate

Prior to any commit or pull request, the automated privacy audit script must verify:
```bash
python scripts/privacy_audit.py
```
This scanner inspects staged files for:
- API key and token signatures.
- Local user profile path leaks and system directories.
- Private email addresses and telephone numbers.
- Uncommitted database files or raw media.

---

## 6. Failure Mode & Incident Protocol

If potentially sensitive, confidential, or personal information is discovered in working tree or historical commits:
1. **STOP immediately** — Do not push.
2. Flag: `POTENTIAL PRIVATE DATA DETECTED — HUMAN REVIEW REQUIRED`.
3. Invalidate any exposed credentials immediately at the provider level.
4. Notify repository maintainers to coordinate history hygiene if necessary.

---

## 7. Compliance

Every contributor and AI assistant operating in this codebase is bound by this policy without exception.
