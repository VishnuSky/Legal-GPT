# Legal-GPT Deployment Guide

This guide describes how to deploy Legal-GPT standalone and configure it as an external tool source for xAI / Grok Public Law Scout.

---

## 1. Local Deployment (Python Direct)

### Prerequisites
- Python 3.10+
- `pip install -r requirements.txt`

### Start Command
- **Windows / PC1:**
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts/start_legal_gpt.ps1
  ```
  *(Automatically detects port availability and falls back to port 8001 if port 8000 is occupied by background services).*

- **Linux / macOS:**
  ```bash
  chmod +x scripts/start_legal_gpt.sh
  ./scripts/start_legal_gpt.sh
  ```

- **Direct Uvicorn:**
  ```bash
  python -m uvicorn api.server:app --host 0.0.0.0 --port 8000
  ```

---

## 2. Docker & Docker Compose Deployment

### Build and Run with Docker
```bash
docker build -t legal-gpt:latest .
docker run -d -p 8000:8000 --name legal-gpt legal-gpt:latest
```

### Run with Docker Compose
```bash
docker compose up -d
```

### Live Law Updates via Volume Mount
The `docker-compose.yml` mounts `./legal_registry` into `/app/legal_registry:ro`. When new statutory amendments, court rules, or concept packs are added locally, the container reads them immediately without needing an image rebuild.

---

## 3. Cloud Deployment (Cloud-Agnostic)

Legal-GPT is a stateless, containerized microservice that can be deployed onto any container hosting service.

### Container Specifications:
- **Base Image:** `python:3.11-slim`
- **Memory:** Minimum 512 MB, recommended 1 GB+
- **CPU:** 1 vCPU
- **Internal Port:** `8000`
- **Health Check Endpoint:** `GET /health` (returns HTTP 200)

### Cloud Provider Examples:
- **Google Cloud Run:**
  ```bash
  gcloud run deploy legal-gpt \
    --image gcr.io/[PROJECT-ID]/legal-gpt:latest \
    --platform managed \
    --port 8000 \
    --allow-unauthenticated
  ```
- **AWS App Runner / ECS:**
  Configure service using `Dockerfile`, port 8000, health check path `/health`.
- **Fly.io:**
  ```bash
  fly launch
  fly deploy
  ```

---

## 4. Registering with xAI / Grok for MCP

Once Legal-GPT has a public HTTPS domain (e.g. `https://api.legal-gpt.org`):

### What URL to Give xAI:
Provide the MCP tool discovery endpoint:
```text
https://api.legal-gpt.org/mcp/v1/tools
```

### Tools Registered:
1. `lookup_public_law`: Primary statutory research with controlling citations.
2. `explain_concept`: Progressive 5-level legal literacy breakdown.
3. `lookup_services`: Official legal aid and court self-help locator.
4. `get_deadlines`: Statutory date and court-day procedural deadline calculator.

### MCP JSON-RPC Registration Payload:
```json
{
  "mcpServers": {
    "legal-gpt": {
      "url": "https://api.legal-gpt.org/mcp/v1/tools",
      "transport": "http",
      "headers": {
        "Content-Type": "application/json"
      }
    }
  }
}
```

---

## 5. Security, Firewall & CORS Requirements

To allow xAI and public clients to safely call Legal-GPT:

1. **HTTPS / TLS 1.3:**
   xAI requires HTTPS for remote MCP servers. Always terminate TLS at your reverse proxy (e.g. Cloudflare, Caddy, AWS ALB, or GCP Cloud Load Balancing).

2. **CORS Configuration:**
   For browser or WebUI clients calling the API directly, ensure FastAPI CORS middleware permits the originating origin:
   - Allow Methods: `GET, POST, OPTIONS`
   - Allow Headers: `Content-Type, Authorization, Accept`

3. **Firewall & Ingress:**
   - Ingress port: 443 (HTTPS) $\rightarrow$ forwards to container port 8000.
   - Outbound: No outbound internet access is strictly required for Brain 2 statutory lookups (all law is verified locally in `legal_registry`). If LM Studio is used, outbound access to `LOCAL_LLM_URL` is needed.
