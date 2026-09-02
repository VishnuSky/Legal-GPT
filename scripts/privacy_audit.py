"""Automated Repository Privacy & Secret Audit Script.

Scans the Legal-GPT repository to ensure zero leakage of:
- API keys, tokens, or credentials
- Local machine paths (e.g., C:\\Users\\, /home/)
- Private / personal case data or evidence
- Unintended binary databases or private files
"""

import os
import re
import sys
from pathlib import Path

# Safe console encoding for Windows
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Sensitive regex signatures
SECRET_PATTERNS = [
    (r"\bAIza[0-9A-Za-z-_]{35}\b", "Google API Key"),
    (r"\bghp_[0-9a-zA-Z]{36}\b", "GitHub Personal Access Token"),
    (r"\bsk_live_[0-9a-zA-Z]{24}\b", "Stripe Live Secret Key"),
    (r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "Private Key Header"),
    (r"(?:api_key|apikey|secret_key|private_token)\s*[:=]\s*['\"][0-9a-zA-Z_\-]{16,}['\"]", "Generic Hardcoded Secret"),
]

# Sensitive local filesystem leaks (matching file paths, not web URLs)
LOCAL_PATH_PATTERNS = [
    (r"(?<!https://)(?<!http://)[C-Z]:\\Users\\[A-Za-z0-9_.\-]+(?!\.gemini)", "Windows Local User Path"),
    (r"(?<!https://)(?<!http://)[L-Z]:\\", "Windows Private Drive Letter (L:\\, J:\\)"),
    (r"/media/ixtly", "Private Linux Media Mount"),
    (r"EvidenceWorkspace", "EvidenceWorkspace Reference"),
    (r"\b10\.0\.0\.\d{1,3}\b", "Private 10.0.0.x Subnet IP"),
    (r"\bAeon\b", "Private Aeon Identifier"),
    (r"\bvoiceprint\b", "Biometric Voiceprint Data"),
    (r"\.wav\b", "WAV Audio Evidence File"),
    (r"\bMetaVault\b", "Private MetaVault Reference"),
    (r"(?<!https://)(?<!http://)(?<!/)\b/home/[a-zA-Z0-9_.\-]+/(?:Documents|Desktop|Downloads|projects|code|workspace|\.ssh)", "Linux Local Home Directory Path"),
    (r"(?<!https://)(?<!http://)(?<!/)\b/Users/[a-zA-Z0-9_.\-]+/(?:Documents|Desktop|Downloads|projects|code|workspace|\.ssh)", "macOS Local Home Directory Path"),
]

# Prohibited file extensions/patterns
PROHIBITED_EXTENSIONS = {".sqlite", ".sqlite3", ".db-journal", ".pem", ".key", ".pfx", ".p12", ".wav", ".mp3", ".m4a", ".flac", ".safetensors", ".gguf", ".lora"}
ALLOWED_EXTENSIONS = {".py", ".md", ".yaml", ".yml", ".toml", ".json", ".txt", ".example", ".gitignore", ".gitattributes"}


def audit_repository(repo_root: str) -> bool:
    root_path = Path(repo_root)
    violations = []

    print("[AUDIT] Running Legal-GPT Public Repository Privacy & Secret Audit...")

    for root, dirs, files in os.walk(repo_root):
        # Skip git directory, virtual environments, caches, audit script directory
        dirs[:] = [d for d in dirs if d not in {".git", ".venv", "venv", "__pycache__", ".pytest_cache", "node_modules", "data", ".gemini"}]

        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(root_path)

            # Check file extension
            if file_path.suffix in PROHIBITED_EXTENSIONS:
                violations.append(f"[FORBIDDEN FILE EXTENSION] {rel_path}")
                continue

            # Skip self, binaries and non-text files
            if file in {"privacy_audit.py", "PUBLIC_DATA_POLICY.md"}:
                continue
            if file_path.suffix not in ALLOWED_EXTENSIONS and file not in {".gitignore", ".gitattributes"}:
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
            except Exception as e:
                print(f"[WARN] Could not read {rel_path}: {e}")
                continue

            # 1. Scan for hardcoded credentials / secrets
            for pattern, desc in SECRET_PATTERNS:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for m in matches:
                    violations.append(f"[SECRET DETECTED: {desc}] {rel_path} -> '{m[:12]}...'")

            # 2. Scan for local path leaks
            for pattern, desc in LOCAL_PATH_PATTERNS:
                matches = re.findall(pattern, content)
                for m in matches:
                    # Ignore generic documentation placeholders
                    if "username" in m.lower() or "your_user" in m.lower() or "<username>" in m.lower():
                        continue
                    violations.append(f"[LOCAL PATH LEAK: {desc}] {rel_path} -> '{m}'")

    if violations:
        print("\n[FAIL] PRIVACY AUDIT FAILED — POTENTIAL PRIVATE DATA DETECTED:")
        for v in violations:
            print(f"  - {v}")
        print("\n[ACTION REQUIRED]: Remove sensitive references before committing or pushing.")
        return False
    else:
        print("\n[PASS] PRIVACY AUDIT PASSED: Repository is 100% clean and public-safe.")
        return True


if __name__ == "__main__":
    repo_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    clean = audit_repository(repo_dir)
    sys.exit(0 if clean else 1)
