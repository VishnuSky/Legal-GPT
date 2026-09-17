# Source Submission Schema

This document specifies the exact technical schema for community submissions to Legal-GPT. All submissions must conform to this schema to be admitted into the `PROPOSED` quarantine review pool.

---

## 1. JSON Schema Definition

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "LegalGPTCommunityContribution",
  "type": "object",
  "required": [
    "contribution_id",
    "contribution_type",
    "source",
    "submitter",
    "date",
    "jurisdiction",
    "authority_type",
    "provenance",
    "license",
    "verification_state"
  ],
  "properties": {
    "contribution_id": {
      "type": "string",
      "pattern": "^CONTRIB-[A-F0-9]{8,12}$",
      "description": "Unique identifier for the contribution."
    },
    "contribution_type": {
      "type": "string",
      "enum": [
        "LEGAL_SOURCE",
        "SOURCE_METADATA",
        "JURISDICTION",
        "CASE",
        "STATUTE",
        "REGULATION",
        "COURT_RULE",
        "AGENCY_POLICY",
        "RESOURCE",
        "DATASET",
        "TEST_CASE",
        "BENCHMARK",
        "BUG_REPORT",
        "DOCUMENTATION",
        "TRANSLATION",
        "LEGAL_LITERACY_MATERIAL"
      ],
      "description": "Category of legal or technical contribution."
    },
    "source": {
      "type": "string",
      "minLength": 3,
      "description": "The legal citation, official title, or identifier."
    },
    "submitter": {
      "type": "string",
      "minLength": 2,
      "description": "Identity, GitHub handle, or organization of submitter."
    },
    "date": {
      "type": "string",
      "format": "date",
      "description": "Submission date in ISO format YYYY-MM-DD."
    },
    "jurisdiction": {
      "type": "string",
      "pattern": "^(US|US-[A-Z]{2}|US-TRIBAL-[A-Z0-9_-]+|INTERNATIONAL)$",
      "description": "Standardized jurisdiction identifier."
    },
    "authority_type": {
      "type": "string",
      "enum": [
        "T0_CONSTITUTIONAL",
        "T1_BINDING_SCOTUS",
        "T2_BINDING_FED_CIRCUIT",
        "T3_BINDING_STATE_APPELLATE",
        "T4_FEDERAL_STATUTE",
        "T5_STATE_STATUTE",
        "T6_FEDERAL_REGULATION",
        "T7_STATE_REGULATION",
        "T8_COURT_RULES",
        "T9_ADMIN_ORDERS",
        "T10_AGENCY_POLICY",
        "T11_PERSUASIVE_CASELAW",
        "T12_SECONDARY_SOURCES",
        "RESOURCE_AID",
        "TECHNICAL_DATASET",
        "BENCHMARK_SPEC"
      ],
      "description": "Authority hierarchy level."
    },
    "effective_date": {
      "type": ["string", "null"],
      "format": "date",
      "description": "Date when this law, amendment, or policy became legally effective."
    },
    "provenance": {
      "type": "object",
      "required": ["origin_url", "publisher", "verification_method"],
      "properties": {
        "origin_url": {
          "type": "string",
          "format": "uri",
          "description": "Official government or court repository URL."
        },
        "publisher": {
          "type": "string",
          "description": "Official entity publishing the source (e.g. WA State Legislature)."
        },
        "verification_method": {
          "type": "string",
          "description": "How the source was authenticated (e.g. Official Government Portal Scraping, Certified Slip Opinion)."
        },
        "content_hash": {
          "type": "string",
          "description": "SHA-256 hash of the submitted source content for cryptographic tamper-proofing."
        }
      }
    },
    "license": {
      "type": "string",
      "enum": [
        "CC0-1.0",
        "Public Domain",
        "Apache-2.0",
        "MIT",
        "ODbL-1.0"
      ],
      "description": "Permissive license under which contribution is released."
    },
    "verification_state": {
      "type": "string",
      "enum": [
        "PROPOSED",
        "UNDER_REVIEW",
        "VERIFIED",
        "REJECTED",
        "SUPERSEDED",
        "ARCHIVED"
      ],
      "default": "PROPOSED",
      "description": "Lifecycle state of the submission."
    },
    "payload": {
      "type": "object",
      "description": "The substantive payload (statutory text, test assertions, benchmark YAML, etc.)."
    }
  }
}
```

---

## 2. Concrete Submission Example: Statute

```json
{
  "contribution_id": "CONTRIB-A9F21804",
  "contribution_type": "STATUTE",
  "source": "RCW 13.34.065",
  "submitter": "AdvocateWA-01",
  "date": "2026-09-17",
  "jurisdiction": "US-WA",
  "authority_type": "T5_STATE_STATUTE",
  "effective_date": "2021-07-01",
  "provenance": {
    "origin_url": "https://leg.wa.gov/CodeReviser/Pages/RCW13.34.065.aspx",
    "publisher": "Washington State Statute Law Committee",
    "verification_method": "Official Legislative Portal Text Ingestion",
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  },
  "license": "CC0-1.0",
  "verification_state": "PROPOSED",
  "payload": {
    "title": "Shelter care — Hearing — Recommendation as to further custody — Release",
    "key_statutory_rule": "The juvenile court must conduct a shelter care hearing within seventy-two hours, excluding Saturdays, Sundays, and legal holidays, or the child must be released.",
    "subsections": [
      {
        "number": "1",
        "text": "When a child is taken custody, the court shall hold a shelter care hearing within seventy-two hours, excluding Saturdays, Sundays, and legal holidays."
      }
    ]
  }
}
```

---

## 3. Concrete Submission Example: Public Legal Resource

```json
{
  "contribution_id": "CONTRIB-C104B8E2",
  "contribution_type": "RESOURCE",
  "source": "Northwest Justice Project (CLEAR Hotline)",
  "submitter": "public-defender-alliance",
  "date": "2026-09-17",
  "jurisdiction": "US-WA",
  "authority_type": "RESOURCE_AID",
  "effective_date": null,
  "provenance": {
    "origin_url": "https://nwjustice.org/get-legal-help",
    "publisher": "Northwest Justice Project",
    "verification_method": "Direct verification with organizational portal and directory",
    "content_hash": "a54f128c701bc994..."
  },
  "license": "CC0-1.0",
  "verification_state": "PROPOSED",
  "payload": {
    "name": "Northwest Justice Project",
    "organization_type": "LEGAL_AID",
    "service_area": "Washington Statewide",
    "eligibility": "Low-income individuals and families at or below 200% federal poverty guideline.",
    "phone": "1-888-201-1014",
    "website": "https://nwjustice.org",
    "services": ["Civil legal aid", "Family law representation", "Housing defense", "CPS dependency advocacy"]
  }
}
```
