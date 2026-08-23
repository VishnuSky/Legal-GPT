"""Automated Security & Privacy Policy Unit Tests."""

import os
from pathlib import Path
from scripts.privacy_audit import audit_repository


def test_repository_privacy_audit_passes():
    repo_root = str(Path(__file__).parent.parent)
    is_clean = audit_repository(repo_root)
    assert is_clean is True, "Repository privacy audit failed: Detected potential sensitive data or secrets."


def test_required_security_and_policy_files_exist():
    repo_root = Path(__file__).parent.parent
    assert (repo_root / "PUBLIC_DATA_POLICY.md").exists()
    assert (repo_root / "SECURITY.md").exists()
    assert (repo_root / ".gitignore").exists()
    assert (repo_root / ".env.example").exists()


def test_env_example_has_no_real_secrets():
    repo_root = Path(__file__).parent.parent
    env_example = (repo_root / ".env.example").read_text(encoding="utf-8")
    assert "<YOUR_" in env_example
    assert "sk_live_" not in env_example
    assert "ghp_" not in env_example
    assert "AIza" not in env_example


def test_gitignore_covers_critical_exclusions():
    repo_root = Path(__file__).parent.parent
    gitignore_text = (repo_root / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in gitignore_text
    assert "*.sqlite" in gitignore_text
    assert "*.db" in gitignore_text
    assert "credentials.json" in gitignore_text
    assert "data/private/" in gitignore_text
    assert "evidence/" in gitignore_text
    assert "case_files/" in gitignore_text
