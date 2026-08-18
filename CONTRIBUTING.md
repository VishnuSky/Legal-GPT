# Contributing to Legal-GPT ⚖️

Thank you for your interest in contributing to **Legal-GPT**!

## Core Architecture Principles to Respect
1. **Model = Reasoning, Database = Law**: Never train or bake mutable statutes or regulations directly into base LLM weights or system prompts. Legal authority lives in the machine-readable database/registry; the model provides reasoning and synthesis.
2. **Authority Hierarchy (Tiers 0–5)**:
   - **Tier 0**: Official government sources (Statutes, Constitutions, Regulations, Court slip opinions).
   - **Tier 1**: Curated open-access databases (CourtListener, Harvard CAP, GovInfo, Congress.gov, BIA).
   - **Tier 2**: Institutional & Bar Associations & Legal Aid.
   - **Tier 3**: Secondary legal indexes (Cornell LII, Justia, FindLaw).
   - **Tier 4**: Law firm articles & blogs.
   - **Tier 5**: Forums & ungrounded LLMs (*Strictly barred from serving as legal authority*).
3. **Temporal Validity**: Always account for effective dates, enacted dates, and repeal dates.
4. **Zero-Hallucination Citations**: Never allow the model to present fabricated citations. Every citation must resolve against the canonical registry.

## Development Setup

```bash
# 1. Clone repository
git clone https://github.com/VishnuSky/Legal-GPT.git
cd Legal-GPT

# 2. Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# 3. Install in editable mode with development dependencies
pip install -e ".[dev]"

# 4. Run tests
pytest tests/ -v
```

## Adding a New State or Legal Source
1. Define the source entry in `legal_registry/states/<STATE>.yaml` or `legal_registry/cps/<state>_cps.yaml`.
2. Ensure the entry adheres to `legal_registry/schemas/registry_entry.py` or `cps_source_entry.py`.
3. Add corresponding unit tests in `tests/`.
