"""Automated Security & Privacy Policy Unit Tests."""

import re
from pathlib import Path
from scripts.privacy_audit import audit_repository
from scripts.privacy_audit import WINDOWS_PRIVATE_DRIVE_PATTERN as PRIVACY_WINDOWS_PRIVATE_DRIVE_PATTERN
from scripts.deep_security_audit import WINDOWS_PRIVATE_DRIVE_PATTERN as DEEP_WINDOWS_PRIVATE_DRIVE_PATTERN
from scripts.deep_security_audit import _is_documented_media_mount_pattern_reference
from scripts.deep_security_audit import _is_local_file_uri_reference


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


def test_private_drive_pattern_matches_only_real_path_prefixes():
    samples = [
        r'L:\n',
        r'L:\r',
        r'L:\t',
        r'L:\b',
        r'L:\f',
        r'L:\"',
    ]

    for pattern in (PRIVACY_WINDOWS_PRIVATE_DRIVE_PATTERN, DEEP_WINDOWS_PRIVATE_DRIVE_PATTERN):
        for sample in samples:
            assert re.search(pattern, sample) is None

        assert re.search(pattern, r"L:\Legal") is not None
        assert re.search(pattern, r"L:\A") is not None
        assert re.search(pattern, r"fooL:\Legal") is None


def test_local_file_uri_reference_detection():
    positive_samples = [
        "- [`x`](" + "file:///" + "C:/Users/test/Documents/file.py)",
        "file://C:/Windows/System32/",
        "file:///var/tmp/report.txt",
        "<" + "file://localhost/C:/Users/test/Documents/file.py>",
        "file://localhost/etc/hosts",
        "file://server/share/path",
        "file://server/share/",
        "file:///tmp/",
    ]
    negative_samples = [
        "https://example.com/path",
        "normal text without uri",
    ]

    for sample in positive_samples:
        assert _is_local_file_uri_reference(sample) is True

    for sample in negative_samples:
        assert _is_local_file_uri_reference(sample) is False


def test_documented_media_mount_pattern_reference_detection():
    media_mount = "/" + "media/ixtly"
    positive_samples = [
        f"+- Documented `{media_mount}` pattern with `# scan pattern, not a live mount`.",
        f"Documented {media_mount} path pattern for scanner coverage.",
    ]
    negative_samples = [
        media_mount,
        "Documented private Linux media-mount scan pattern with no literal path",
        f"Real live mount at {media_mount}",
    ]

    for sample in positive_samples:
        assert _is_documented_media_mount_pattern_reference(sample) is True

    for sample in negative_samples:
        assert _is_documented_media_mount_pattern_reference(sample) is False
