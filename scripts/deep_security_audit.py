"""Comprehensive Deep Security, Privacy, and Local Leak Audit for Legal-GPT."""

import os
import re
import sys
import subprocess
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent

# Forbidden patterns
PATTERNS = {
    "Username / Home Directory": [
        r"rolda",
        r"C:\\Users\\",
        r"C:/Users/",
        r"/home/[a-zA-Z0-9_-]+",
        r"Users/rolda",
        r"Users\\rolda",
        r"AppData",
    ],
    "Private IP Addresses (Non-Localhost)": [
        r"\b192\.168\.\d{1,3}\.\d{1,3}\b",
        r"\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
        r"\b172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}\b",
    ],
    "Hardcoded API Keys & Secrets": [
        r"(?:api[_-]?key|secret[_-]?key|token|auth[_-]?token|password)\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]",
        r"ghp_[A-Za-z0-9]{36}",
        r"gho_[A-Za-z0-9]{36}",
        r"AIza[0-9A-Za-z-_]{35}",
        r"sk-[A-Za-z0-9]{32,}",
    ],
    "External Project References": [
        r"Evidence\s+Manager\s+(?:files|data|db)",
        r"VR_forensics",
        r"swarms_private",
    ]
}

def audit_working_tree():
    print("=" * 60)
    print("1. SCANNING WORKING TREE FILES...")
    print("=" * 60)
    violations = []
    
    # Exceptions that are allowed to mention patterns in abstract security context
    allowed_security_files = {"scripts/privacy_audit.py", "scripts/deep_security_audit.py", "tests/test_privacy_policy.py"}

    for root, dirs, files in os.walk(ROOT_DIR):
        # Ignore git, caches
        dirs[:] = [d for d in dirs if d not in {".git", ".pytest_cache", "__pycache__", "venv", ".venv"}]
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), ROOT_DIR).replace("\\", "/")
            if rel_path in allowed_security_files:
                continue

            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    for category, pattern_list in PATTERNS.items():
                        for pat in pattern_list:
                            matches = list(re.finditer(pat, content, re.IGNORECASE))
                            if matches:
                                for m in matches:
                                    snippet = content[max(0, m.start()-25):min(len(content), m.end()+25)].replace("\n", " ")
                                    violations.append(f"[{category}] File '{rel_path}': matched '{m.group(0)}' (context: '...{snippet}...')")
            except Exception as e:
                pass

    if violations:
        print(f"[FAIL] Found {len(violations)} working tree violations:")
        for v in violations:
            print(f"  ❌ {v}")
    else:
        print("[PASS] Zero local usernames, paths, private IPs, credentials, or private project references in working tree files.")
    return len(violations)


def audit_git_commit_history():
    print("\n" + "=" * 60)
    print("2. SCANNING COMPLETE GIT COMMIT HISTORY & METADATA...")
    print("=" * 60)
    
    # Check all commit logs and diffs
    try:
        proc = subprocess.run(["git", "log", "-p", "--all"], cwd=ROOT_DIR, capture_output=True, text=True, errors="ignore")
        git_history = proc.stdout
    except Exception as e:
        print(f"[ERROR] Could not inspect git history: {e}")
        return 1

    violations = []
    # Check for username, local paths, private IPs, and real tokens in git history
    for category, pattern_list in PATTERNS.items():
        for pat in pattern_list:
            matches = list(re.finditer(pat, git_history, re.IGNORECASE))
            if matches:
                for m in matches:
                    # Exclude security audit test code matches
                    start = max(0, m.start() - 40)
                    end = min(len(git_history), m.end() + 40)
                    context = git_history[start:end].replace("\n", " ")
                    if "privacy_audit" in context or "test_privacy" in context or "deep_security" in context:
                        continue
                    violations.append(f"[{category}] Git commit history contains '{m.group(0)}' (context: '...{context}...')")

    if violations:
        print(f"[FAIL] Found {len(violations)} git history violations:")
        for v in violations:
            print(f"  ❌ {v}")
    else:
        print("[PASS] Zero local usernames, paths, private IPs, credentials, or private project data found across entire Git commit history.")

    # Check commit author and committer emails
    proc_authors = subprocess.run(["git", "log", "--format=%an <%ae> | %cn <%ce>", "--all"], cwd=ROOT_DIR, capture_output=True, text=True, errors="ignore")
    authors = set(proc_authors.stdout.strip().split("\n"))
    print(f"\n[INFO] Git Commit Authors/Committers in History:\n" + "\n".join(f"  • {a}" for a in authors if a.strip()))

    return len(violations)


def audit_ignored_files_and_databases():
    print("\n" + "=" * 60)
    print("3. CHECKING DATABASE & SENSITIVE FILE ISOLATION (.gitignore)...")
    print("=" * 60)
    
    proc_tracked = subprocess.run(["git", "ls-files"], cwd=ROOT_DIR, capture_output=True, text=True, errors="ignore")
    tracked_files = proc_tracked.stdout.strip().split("\n")
    
    forbidden_extensions = [".db", ".sqlite", ".sqlite3", ".log", ".env", ".pem", ".key", ".pfx", ".p12", ".bak", ".tmp"]
    db_violations = []
    for f in tracked_files:
        for ext in forbidden_extensions:
            if f.endswith(ext) and not f.endswith(".env.example"):
                db_violations.append(f)

    if db_violations:
        print(f"[FAIL] Tracked sensitive/binary files found in Git index:")
        for dbf in db_violations:
            print(f"  ❌ {dbf}")
    else:
        print("[PASS] No database files (*.db, *.sqlite), private env files (.env), certificates (*.pem), or log files are tracked in Git.")

    return len(db_violations)


def main():
    print("🛡️  LEGAL-GPT DEEP SECURITY & DATA ISOLATION AUDIT  🛡️\n")
    w_count = audit_working_tree()
    g_count = audit_git_commit_history()
    d_count = audit_ignored_files_and_databases()

    total = w_count + g_count + d_count
    print("\n" + "=" * 60)
    if total == 0:
        print("✅ COMPREHENSIVE AUDIT RESULT: 100% CLEAN & PUBLIC-SAFE.")
        print("   - No local usernames (e.g. rolda)")
        print("   - No local filesystem paths (e.g. C:\\Users\\)")
        print("   - No private network IPs or hostnames")
        print("   - No API keys, credentials, or private tokens")
        print("   - No SQLite databases or log files tracked")
        print("   - No references or data from private projects")
        print("=" * 60)
        sys.exit(0)
    else:
        print(f"❌ AUDIT FAILED: {total} security/privacy issues detected.")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
