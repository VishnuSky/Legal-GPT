#!/usr/bin/env bash
#
# Starts the Legal-GPT API Server on Linux / macOS.
# Verifies Python >= 3.10, installs requirements if missing,
# displays all 9 public API endpoints and LM Studio URL, and starts uvicorn.

set -e

PORT=${PORT:-8000}
HOST=${HOST:-0.0.0.0}

echo "=================================================="
echo "⚖️  LEGAL-GPT SYSTEM STARTUP (LINUX / MACOS)"
echo "=================================================="

# 1. Determine Python executable
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo "[-] Error: Python is not installed or not in PATH."
    exit 1
fi

# 2. Check Python version (>= 3.10)
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || { [ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]; }; then
    echo "[-] Error: Python 3.10 or higher is required. Found Python $PYTHON_VERSION"
    exit 1
fi
echo "[✓] Python version verified: Python $PYTHON_VERSION"

# 3. Check and install dependencies
echo "[*] Checking Python dependencies..."
DEPS_OK=$($PYTHON_CMD -c "
try:
    import pydantic, pyyaml, fastapi, uvicorn, httpx, rich, typer, dateutil, networkx, jinja2
    print('OK')
except ImportError:
    print('MISSING')
")

if [ "$DEPS_OK" != "OK" ]; then
    echo "[*] Installing missing dependencies from requirements.txt..."
    $PYTHON_CMD -m pip install -r requirements.txt
    echo "[✓] Dependencies successfully installed."
else
    echo "[✓] All dependencies verified."
fi

# 4. Display 9 Public API Endpoints
echo ""
echo "🌐 Legal-GPT Public REST API Endpoints (Port $PORT):"
echo "  1. Resolution:         POST http://localhost:$PORT/api/v1/public/resolve"
echo "  2. Streaming:          POST http://localhost:$PORT/api/v1/public/resolve/stream"
echo "  3. Navigator:          POST http://localhost:$PORT/api/v1/public/navigate"
echo "  4. Services:           GET  http://localhost:$PORT/api/v1/public/services"
echo "  5. Deadlines:          POST http://localhost:$PORT/api/v1/public/deadlines"
echo "  6. Timeline:           POST http://localhost:$PORT/api/v1/public/timeline"
echo "  7. Document Explainer: POST http://localhost:$PORT/api/v1/public/explain-document"
echo "  8. Question Builder:   POST http://localhost:$PORT/api/v1/public/question-builder"
echo "  9. Legal Literacy:     POST http://localhost:$PORT/api/v1/public/explain-concept"

echo ""
echo "🤖 LM Studio Integration:"
echo "  • LM Studio Server URL: http://localhost:1234/v1"
echo "  • Native MCP Stdio:      python -m api.mcp_server"
echo "  • Public MCP HTTP:       http://localhost:$PORT/mcp/v1/tools"

echo ""
echo "🚀 Launching uvicorn server on http://$HOST:$PORT..."
echo "Press CTRL+C to stop the server."
echo ""

exec $PYTHON_CMD -m uvicorn api.server:app --host "$HOST" --port "$PORT"
