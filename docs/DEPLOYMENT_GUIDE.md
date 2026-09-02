# Legal-GPT: Deployment & Local AI Integration Guide

This guide explains how to deploy **Legal-GPT v1.0.0** locally and integrate it with **LM Studio**, **OpenWebUI**, **Docker**, and **Model Context Protocol (MCP)** clients.

---

## ⚡ Quickstart: Local Installation

### 1. Prerequisites
- Python 3.10+ (Recommended: Python 3.11 or 3.12)
- Git

### 2. Clone & Install
```bash
git clone https://github.com/VishnuSky/Legal-GPT.git
cd Legal-GPT
pip install -e .
```

### 3. Run Verification Suite
```bash
pytest -v
python cli.py benchmark --category all
```

---

## 🔌 1. Model Context Protocol (MCP) Integration (LM Studio & Claude Desktop)

Legal-GPT includes a built-in MCP server (`api/mcp_server.py`) communicating over standard I/O.

### Configuration for Claude Desktop / LM Studio
Add the following snippet to your `mcp_config.json` or `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "legal-gpt": {
      "command": "python",
      "args": ["-m", "cli", "mcp"],
      "cwd": "/path/to/Legal-GPT"
    }
  }
}
```

### Starting the MCP Server via CLI
```bash
python cli.py mcp
```

---

## 🌐 2. OpenWebUI Custom Pipeline Integration

Legal-GPT provides a drop-in custom pipeline in [`api/openwebui_pipeline.py`](api/openwebui_pipeline.py).

### How to Install in OpenWebUI
1. Open your **OpenWebUI Admin Panel** $\to$ **Functions / Pipelines**.
2. Click **Add Function / Pipeline** $\to$ **Import from File**.
3. Select `api/openwebui_pipeline.py` or paste its contents.
4. Configure valves:
   - `default_state`: Default state (e.g. `WA`, `IL`, `OH`, `CA`, `TX`, `NY`).
   - `default_persona_mode`: `standard`, `self_represented`, `investigator`, `attorney`, or `court`.
5. Save and enable. The model will appear in your OpenWebUI model dropdown.

---

## 🚀 3. Local REST API Server

To run the standalone FastAPI REST server:

```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Interactive API Documentation
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Core API Endpoints
- `POST /api/v1/query`: Multi-factor legal research query.
- `GET /api/v1/citator`: Shepard's/KeyCite-style subsequent treatment lookups.
- `GET /api/v1/law-at-date`: Point-in-time statutory revisions and textual diffs.
- `POST /api/v1/cps/evidence/evaluate`: Fact vs Allegation matrix and evidentiary gap audit.
- `POST /api/v1/cps/motions/generate`: State-specific court motion generation.
- `POST /api/v1/cps/audit/due-process`: 7-pillar due process and parent rights audit.
- `GET /api/v1/benchmark`: Automated 50-scenario benchmark suite execution.

---

## 🐳 4. Docker Deployment

A clean Docker container can be built and run using:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -e .
EXPOSE 8000
CMD ["python", "cli.py", "serve", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t legal-gpt .
docker run -p 8000:8000 legal-gpt
```

---

## 🛡️ 5. Security & Privacy Audit Gate

Before making contributions or deploying publicly, always verify data isolation:
```bash
python scripts/privacy_audit.py
python scripts/deep_security_audit.py
```
