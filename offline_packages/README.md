# Legal-GPT Offline Data Packages

The Legal-GPT Offline Data Package enables parents, self-represented litigants, child welfare advocates, and legal aid attorneys to access verified statutory child welfare timelines, primary constitutional and statutory authorities, procedural rights checklists, and legal literacy concept explanations completely offline on any device.

---

## 1. Package Contents

Each package is bundled as a clean, machine-readable JSON file:

- **Full Package (`legal_gpt_offline_{date}.json`)**:
  - All 50 U.S. states + DC + U.S. Territories + Washington Tribal overlay.
  - Complete 22 Legal Literacy Concepts (Pack A & Pack B) spanning 5 literacy levels.
  - Crisis checklists for immediate emergency protective custody / removal defense.
  - Verified statewide legal aid directory and contact portals.
  - Plain-English legal disclaimer and staleness metadata.

- **State-Specific Packages (`states/{STATE}_offline.json`)**:
  - Individual jurisdiction profile with emergency removal timelines, shelter hearing hours, counsel appointment citations, and TPR statutory thresholds.
  - Full concept literacy corpus and state-specific legal aid resources.

---

## 2. Downloading Packages via API

Legal-GPT serves packages directly from the local or hosted API:

### View Available Manifest
```bash
curl -s http://localhost:8000/api/v1/offline/manifest | jq .
```

### Download State Package (e.g., Washington)
```bash
curl -o WA_offline.json http://localhost:8000/api/v1/offline/download/WA
```

### Download Full National Package
```bash
curl -o legal_gpt_offline_full.json http://localhost:8000/api/v1/offline/download/all
```

---

## 3. CLI `--offline` Flag Usage

The Legal-GPT command line interface supports zero-network local execution using the `--offline` flag:

```bash
# Explain Shelter Care Hearing in Washington at Level 1 (Plain English)
python cli.py explain-concept --concept shelter_care_hearing --state WA --level 1 --offline

# Explain Fourth Amendment Home Entry at Level 4 (Primary Authority)
python cli.py explain-concept --concept fourth_amendment_home_entry --state WA --level 4 --offline

# Perform an On-Demand Drill-Down for Case Law Offline
python cli.py explain-concept --concept due_process --state WA --drill-down SHOW_CASE --offline

# Output Machine-Readable JSON
python cli.py explain-concept --concept emergency_removal --state WA --json --offline
```

---

## 4. Staleness Policy (Quarterly Refresh)

Statutes and court rules undergo legislative and judicial revisions. Legal-GPT enforces an automated **90-day staleness warning**:

- Packages older than 90 calendar days automatically display a prominent staleness alert upon execution:
  ```text
  WARNING: STALENESS NOTICE
  This offline package was generated [YYYY-MM-DD].
  Verify current law at [official_legislature_portal].
  ```
- Packages should be regenerated quarterly by running:
  ```bash
  python scripts/build_offline_package.py
  ```

---

## 5. SHA-256 Integrity Verification

All generated offline packages are hashed at build time. To verify package integrity prior to loading in sensitive environments:

```bash
# Verify checksums on Linux/macOS
sha256sum -c checksums.sha256

# Verify checksum on Windows (PowerShell)
Get-FileHash -Algorithm SHA256 legal_gpt_offline_latest.json
```

---

## 6. Public Domain Status & Licensing

- **Underlying Statutory Text**: The text of U.S. federal statutes, constitutional provisions, federal court opinions, and state statutes is in the public domain and not subject to copyright protection (17 U.S.C. § 101; *Georgia v. Public.Resource.Org, Inc.*, 140 S. Ct. 1498 (2020)).
- **Legal-GPT Analysis and Metadata**: Conceptual plain-English explanations, structured multi-level summaries, verification tagging, and JSON schemas authored by Legal-GPT are licensed under the **Apache License 2.0**.

---

## 7. What Offline Packages Do NOT Include

To guarantee strict privacy and security, offline packages **never** contain:
- Private case files or confidential docket entries
- Personally Identifiable Information (PII) of parents, children, or case participants
- Proprietary or paywalled database extracts
- Evidence Manager records or local drive artifacts

---

## 8. Permitted Use & Attribution

Users and developers **CAN**:
- Download for personal legal preparation: **YES**
- Share offline files with family, friends, or advocates: **YES**
- Print materials and bring them to court hearings: **YES**
- Integrate packages into free/open-source legal aid applications: **YES (with attribution)**
- Claim the package output as formal legal advice: **NO**

### Mandatory Attribution Line
> "Legal information from Legal-GPT (https://github.com/VishnuSky/Legal-GPT) based on public domain U.S. and state statutory text. Not legal advice."
