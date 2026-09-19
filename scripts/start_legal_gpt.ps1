<#
.SYNOPSIS
    Starts the Legal-GPT API Server on Windows / PC1.
.DESCRIPTION
    Verifies Python >= 3.10, installs requirements if missing,
    detects port availability (fallback to 8001 if 8000 occupied),
    displays all 9 public API endpoints and LM Studio URL, and starts uvicorn.
#>

param(
    [int]$Port = 8000,
    [string]$HostAddress = "0.0.0.0"
)

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "⚖️  LEGAL-GPT SYSTEM STARTUP (WINDOWS / PC1)" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Check Python version (>= 3.10)
try {
    $pythonVersionOutput = & python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>&1
    $versionParts = $pythonVersionOutput.Trim().Split(".")
    $major = [int]$versionParts[0]
    $minor = [int]$versionParts[1]
    
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
        Write-Error "Python 3.10 or higher is required. Found Python $pythonVersionOutput"
        exit 1
    }
    Write-Host "[✓] Python version verified: Python $pythonVersionOutput" -ForegroundColor Green
} catch {
    Write-Error "Python is not installed or not found in PATH."
    exit 1
}

# 2. Check and install dependencies
Write-Host "[*] Checking Python dependencies..." -ForegroundColor Yellow
$depsInstalled = & python -c "
try:
    import pydantic, pyyaml, fastapi, uvicorn, httpx, rich, typer, dateutil, networkx, jinja2
    print('OK')
except ImportError as e:
    print('MISSING')
" 2>&1

if ($depsInstalled.Trim() -ne "OK") {
    Write-Host "[*] Installing missing dependencies from requirements.txt..." -ForegroundColor Yellow
    & pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install required Python packages."
        exit 1
    }
    Write-Host "[✓] Dependencies successfully installed." -ForegroundColor Green
} else {
    Write-Host "[✓] All dependencies verified." -ForegroundColor Green
}

# 3. Port availability check (fallback if 8000 is occupied, e.g. by Incredibuild/system services)
$portTest = & python -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind(('127.0.0.1', $Port))
    s.close()
    print('FREE')
except Exception:
    print('OCCUPIED')
" 2>&1

if ($portTest.Trim() -eq "OCCUPIED") {
    $fallbackPort = 8001
    Write-Host "[!] Port $Port is currently in use or restricted. Falling back to port $fallbackPort." -ForegroundColor Yellow
    $Port = $fallbackPort
}

# 4. Display 9 Public API Endpoints
Write-Host ""
Write-Host "🌐 Legal-GPT Public REST API Endpoints (Port $Port):" -ForegroundColor Cyan
Write-Host "  1. Resolution:         POST http://localhost:$Port/api/v1/public/resolve" -ForegroundColor Gray
Write-Host "  2. Streaming:          POST http://localhost:$Port/api/v1/public/resolve/stream" -ForegroundColor Gray
Write-Host "  3. Navigator:          POST http://localhost:$Port/api/v1/public/navigate" -ForegroundColor Gray
Write-Host "  4. Services:           GET  http://localhost:$Port/api/v1/public/services" -ForegroundColor Gray
Write-Host "  5. Deadlines:          POST http://localhost:$Port/api/v1/public/deadlines" -ForegroundColor Gray
Write-Host "  6. Timeline:           POST http://localhost:$Port/api/v1/public/timeline" -ForegroundColor Gray
Write-Host "  7. Document Explainer: POST http://localhost:$Port/api/v1/public/explain-document" -ForegroundColor Gray
Write-Host "  8. Question Builder:   POST http://localhost:$Port/api/v1/public/question-builder" -ForegroundColor Gray
Write-Host "  9. Legal Literacy:     POST http://localhost:$Port/api/v1/public/explain-concept" -ForegroundColor Gray

Write-Host ""
Write-Host "🤖 LM Studio Integration:" -ForegroundColor Cyan
Write-Host "  • LM Studio Server URL: http://localhost:1234/v1" -ForegroundColor Gray
Write-Host "  • Native MCP Stdio:      python -m api.mcp_server" -ForegroundColor Gray
Write-Host "  • Public MCP HTTP:       http://localhost:$Port/mcp/v1/tools" -ForegroundColor Gray

Write-Host ""
Write-Host "🚀 Launching uvicorn server on http://$HostAddress`:$Port..." -ForegroundColor Green
Write-Host "Press CTRL+C to stop the server." -ForegroundColor Yellow
Write-Host ""

& python -m uvicorn api.server:app --host $HostAddress --port $Port
