# Legal-GPT Training Datasets & Curriculum Seed Templates

## Overview

The JSONL files located in this directory (`training/datasets/`) serve strictly as **curriculum seed templates and structural prototypes**. They define and validate the input-output schemas, prompt topologies, and epistemic statement classification formats for Legal-GPT's Supervised Fine-Tuning (SFT) pipeline.

---

## Production Corpus Generation & Infrastructure

- **Seed Templates**: The examples checked into this public repository provide reference patterns and unit testing fixtures for CI/CD validation.
- **Full SFT Corpus Generation**: Generating the complete multi-turn fine-tuning dataset requires executing:
  ```bash
  python -m legal_gpt.training.dataset_builder --target all --output-dir /path/to/sft_corpus
  ```
- **Private GPU Environment**: Mass dataset generation, synthetic multi-turn expansion, and actual GPU-accelerated model fine-tuning must be executed within the private training environment (`legal-gpt-private`). This ensures no heavy intermediate model weights, checkpoint shards, or private compute caches pollute this public codebase.
- **Expected Production Scale**: **50,000+ training examples** distributed across all **23 task families** spanning the 4-stage curriculum (Foundational Epistemology, Core Reasoning, Vertical Substantive Domains, and Complex Intersections).

---

## 23 Task Families Architecture

| Stage | Task Families | Focus Area |
| :--- | :--- | :--- |
| **Stage 1: Foundation** | 01–04 | Jurisdiction Lock, Point-in-Time (`LAW_AT_DATE`), 14-Tier Authority Ranking, Citation Verification |
| **Stage 2: Reasoning** | 05–09 | Issue Spotting, Statutory Rule Extraction, Fact Application, Counterarguments, Uncertainty Quantification |
| **Stage 3: Verticals** | 10–16 | Constitutional Due Process, CPS Child Welfare, ICWA Tribal Law, Parental Rights, Human Rights, Drug Policy, Mental Health |
| **Stage 4: Intersections** | 17–23 | Procedural Due Process, Equal Protection, Search & Seizure, Family Integrity, Administrative Law, Civil Rights, Procedural Motion Remedies |

---

## Schema Traceability

All training instances adhere strictly to `training/schemas/dataset_schema.py`:
- `instruction`: Task objective and legal persona directive.
- `input`: Normalized jurisdiction code, optional county, ISO 8601 event date, and symbolic factual narrative.
- `reasoning_task`: One of the 23 recognized task family keys.
- `expected_behavior`: Controlling citations, authority tiers, and 12-category statement epistemological labels.
- `source`, `jurisdiction`, `legal_date`, `authority_level`, `dataset_version`: Complete provenance metadata.
