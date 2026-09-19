# Public Law Scout & Grok Bot Integration Specification

This document defines how **Public Law Scout** (the official Grok bot on xAI) integrates with Legal-GPT as an external, verified legal intelligence source.

---

## Architectural Overview

Public Law Scout is an AI legal scout designed to assist ordinary people in crisis. To prevent legal hallucination and ensure strict procedural accuracy, Scout relies on Legal-GPT's deterministic primary legal registry, citation verification firewall, and progressive legal literacy models.

```text
┌─────────────────────────┐                     ┌───────────────────────────────────┐
│  PUBLIC LAW SCOUT       │                     │         LEGAL-GPT ENGINE          │
│  (xAI Grok Bot Engine)  │                     │   (Deterministic Primary Truth)   │
│                         │                     │                                   │
│  • User Intent Parsing  ├─[ Tool Call/MCP ]──►│  • Controlling Statutory Lookup   │
│  • Natural Conversation │◄──[ Verified JSON ]─┤  • 5-Level Progressive Literacy   │
│  • Empathetic Delivery  │                     │  • Civil Aid & Services Registry  │
│  • Non-Adjudication     │                     │  • Procedural Deadline Engine     │
└─────────────────────────┘                     └───────────────────────────────────┘
```

---

## Integration Pathways

### Option A: Remote Model Context Protocol (MCP) Server (Recommended for Live Hosting)

When Legal-GPT is hosted on a publicly accessible HTTPS endpoint (e.g., `https://api.legal-gpt.org`), xAI's native MCP integration allows Grok to directly discover and invoke tools over HTTP.

#### 1. xAI Bot MCP Configuration JSON
Add this configuration block to the Grok bot's external MCP tools registry:

```json
{
  "mcpServers": {
    "legal-gpt": {
      "url": "https://api.legal-gpt.org/mcp/v1/tools",
      "transport": "http",
      "headers": {
        "Accept": "application/json"
      }
    }
  }
}
```

#### 2. Endpoints Exposed
- `GET  /mcp/v1/tools`: Returns the standard MCP JSON schema for all 4 tools.
- `POST /mcp/v1/tools/call`: Executes the tool and returns verified results with mandatory disclaimers and verification status (`VERIFIED`, `PARTIAL`, or `ABSTAIN`).

---

### Option B: System Prompt Function Calling / OpenAPI Specs (Recommended for Contest Deadline)

If Legal-GPT is operating in a local or hybrid staging environment prior to full public domain certification, Grok's system prompt can be configured with embedded OpenAPI function definitions. Grok outputs structured JSON tool calls that can be dispatched to Legal-GPT's REST API.

#### 1. Embedded Tool Calling Schema for Grok System Prompt
```json
[
  {
    "name": "lookup_public_law",
    "description": "Lookup controlling statutory sections, caselaw, and procedural rights for a specific jurisdiction. Use when the user asks about specific statutes, hearing rules, or legal standards.",
    "parameters": {
      "type": "object",
      "properties": {
        "question": {"type": "string", "description": "Legal question or situation"},
        "jurisdiction": {"type": "string", "description": "2-letter state code (e.g. WA, IL, OH) or US for federal"}
      },
      "required": ["question", "jurisdiction"]
    }
  },
  {
    "name": "explain_concept",
    "description": "Explain a complex legal concept across progressive literacy levels (1: Plain English, 2: Practical, 3: Terminology, 4: Primary Authority, 5: Advanced Analysis).",
    "parameters": {
      "type": "object",
      "properties": {
        "concept": {"type": "string", "description": "Concept key (e.g. shelter_care_hearing, due_process, notice, active_efforts)"},
        "jurisdiction": {"type": "string", "description": "State code or US"},
        "level": {"type": "integer", "description": "Literacy level 1 to 5", "default": 1}
      },
      "required": ["concept", "jurisdiction"]
    }
  },
  {
    "name": "lookup_services",
    "description": "Find verified civil legal aid, public defense, or court self-help resources in the user's county or state.",
    "parameters": {
      "type": "object",
      "properties": {
        "jurisdiction": {"type": "string", "description": "2-letter state code"},
        "service_type": {"type": "string", "enum": ["LEGAL_AID", "COURT_SELF_HELP", "BAR_REFERRAL", "TRIBAL_ICWA", "PUBLIC_CONTACT"]},
        "county": {"type": "string", "description": "County or judicial district"}
      },
      "required": ["jurisdiction"]
    }
  },
  {
    "name": "get_deadlines",
    "description": "Calculate procedural deadlines and hearing time limits from primary statutes.",
    "parameters": {
      "type": "object",
      "properties": {
        "event_type": {"type": "string", "description": "Triggering event e.g. emergency_removal"},
        "event_date": {"type": "string", "description": "Date of event (YYYY-MM-DD)"},
        "jurisdiction": {"type": "string", "description": "2-letter state code"}
      },
      "required": ["event_type", "event_date", "jurisdiction"]
    }
  }
]
```

#### 2. REST API Dispatch Mapping
| Grok Tool Call | Dispatched Legal-GPT Endpoint |
|:---|:---|
| `lookup_public_law` | `POST /api/v1/public/resolve` or `POST /mcp/v1/tools/call` |
| `explain_concept` | `POST /api/v1/public/explain-concept` or `POST /mcp/v1/tools/call` |
| `lookup_services` | `GET  /api/v1/public/services` or `POST /mcp/v1/tools/call` |
| `get_deadlines` | `POST /api/v1/public/deadlines` or `POST /mcp/v1/tools/call` |

---

### Option C: Web-Search Grounded with Primary Source Constraints (Current Baseline)

In the current live Public Law Scout on Grok, tool calling is grounded in xAI's real-time web search.

#### How It Works:
1. Grok receives the user's situation and extracts the governing jurisdiction.
2. Grok queries public web sources matching the exact statutory registers tracked by Legal-GPT (e.g. Washington Legislature `app.leg.wa.gov`, Illinois General Assembly `ilga.gov`, Ohio Revised Code `codes.ohio.gov`).
3. Grok answers using Legal-GPT's structural formatting rules.

#### Strengths & Limitations:
- **Strengths:** Zero infrastructure cost; operates immediately without private servers or API keys.
- **Limitations:** While typically accurate, results are *not deterministically verified by Legal-GPT's citation engine*. Grok may occasionally summarize web articles rather than citing the operative statutory text, and cannot execute point-in-time temporal diffs.

---

## Recommended Deployment Path

- **For Immediate Contest Submission (Now):** Deploy **Option B** using the system prompt addition defined in [`docs/SCOUT_SYSTEM_PROMPT.md`](SCOUT_SYSTEM_PROMPT.md). This immediately imbues Scout with Legal-GPT's epistemic discipline, non-adjudication posture, and 5-level explanation format.
- **For Production Launch:** Deploy **Option A (MCP)** on a hardened containerized cloud node (e.g. Cloud Run, AWS ECS, or Fly.io) pointing xAI's MCP tools configuration directly to `/mcp/v1/tools`.
