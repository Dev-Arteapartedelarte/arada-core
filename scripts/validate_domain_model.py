#!/usr/bin/env python3
"""Validate and fingerprint the AURA Core domain documentation baseline."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


ROOT_SUFFIX = "Aggregate"
SECTIONS = {
    "A": "Lifecycle",
    "B": "State-Machine",
    "C": "Commands",
    "D": "Domain-Events",
    "E": "Invariants",
    "F": "Permissions",
    "G": "Repository-Contract",
    "H": "Examples",
    "I": "Versioning",
    "J": "Consistency-Boundary",
    "K": "Integration-Events",
    "L": "Read-Model",
    "M": "Test-Scenarios",
    "N": "Performance-Rules",
    "O": "Security-Model",
    "P": "Extension-Points",
}
REFERENCE_RE = re.compile(r"\b(?:DOMAIN-\d{3}[A-P]?|CORE-\d{3})-[A-Za-z0-9-]+\.md\b")
ADR_REFERENCE_RE = re.compile(r"\bADR-(\d{3})\b")
PROHIBITED_RULES = {
    "PUBLIC_DOMAIN_EVENT": re.compile(
        r"Domain Events son contratos públicos|"
        r"Domain Events pueden ser utilizados internamente por otros\s+Bounded Contexts|"
        r"Domain Events de \w+ pueden ser consumidos por otros\s+Aggregates",
        re.IGNORECASE,
    ),
    "IDENTITY_CONTEXT": re.compile(
        r"autenticación pertenece al Bounded Context(?: de)? Identity",
        re.IGNORECASE,
    ),
    "MULTI_AGGREGATE_TRANSACTION": re.compile(
        r"Cuando un caso de uso modifica múltiples Aggregates, la\s+transacción se controla aquí",
        re.IGNORECASE,
    ),
    "PERMISSION_AGGREGATE": re.compile(r"Aggregate \*\*Permission(?:\s|\(|\*)", re.IGNORECASE),
}


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    path: str
    message: str


def read_manifest(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = {"schema_version", "baseline_status", "required_sequence", "aggregates"}
    missing = required.difference(data)
    if missing:
        raise ValueError(f"manifest fields missing: {', '.join(sorted(missing))}")
    if data["schema_version"] not in {1, 2}:
        raise ValueError("unsupported manifest schema_version")
    return data


def expected_documents(entry: dict, sequence: str) -> list[str]:
    number = entry["number"]
    not_applicable = set(entry.get("not_applicable", []))
    documents = [f"DOMAIN-{number}-{ROOT_SUFFIX}.md"]
    for letter in sequence:
        if letter not in not_applicable:
            documents.append(f"DOMAIN-{number}{letter}-{SECTIONS[letter]}.md")
    return documents


def metadata_value(text: str, labels: Iterable[str]) -> str | None:
    lines = text.splitlines()[:40]
    label_pattern = "|".join(re.escape(label) for label in labels)
    pattern = re.compile(rf"^(?:{label_pattern}):\s*(.*)$", re.IGNORECASE)
    for index, line in enumerate(lines):
        match = pattern.match(line.strip())
        if not match:
            continue
        if match.group(1).strip():
            return match.group(1).strip()
        for following in lines[index + 1 :]:
            if following.strip():
                return following.strip()
    return None


def content_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tracked_files(repo_root: Path) -> set[Path]:
    result = subprocess.run(
        ["git", "ls-files"], cwd=repo_root, check=False, capture_output=True, text=True
    )
    if result.returncode != 0:
        return set()
    return {(repo_root / line).resolve() for line in result.stdout.splitlines() if line}


def refresh_manifest(repo_root: Path, manifest_path: Path) -> None:
    manifest = read_manifest(manifest_path)
    aggregates_root = repo_root / "docs" / "architecture" / "domain" / "aggregates"
    manifest["schema_version"] = 2
    manifest["baseline_status"] = "approved"
    manifest["release_tag"] = "domain-model-v1.0.0"
    manifest.pop("source_revision", None)
    for entry in manifest["aggregates"]:
        aggregate_dir = aggregates_root / entry["name"]
        documents = {}
        for filename in expected_documents(entry, manifest["required_sequence"]):
            path = aggregate_dir / filename
            if not path.is_file():
                raise ValueError(f"cannot fingerprint missing document: {path}")
            text = path.read_text(encoding="utf-8")
            version = metadata_value(text, ("Versión", "Version"))
            if version is None:
                raise ValueError(f"cannot fingerprint document without version: {path}")
            documents[filename] = {"version": version, "sha256": content_sha256(path)}
        entry["documents"] = documents
        entry.pop("document_version", None)
        entry.pop("working_tree_candidate", None)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def validate(repo_root: Path, manifest_path: Path, check_git: bool = True) -> list[Finding]:
    manifest = read_manifest(manifest_path)
    domain_root = repo_root / "docs" / "architecture" / "domain"
    aggregates_root = domain_root / "aggregates"
    findings: list[Finding] = []
    tracked = tracked_files(repo_root) if check_git else set()
    entries = manifest["aggregates"]

    numbers = [entry["number"] for entry in entries]
    names = [entry["name"] for entry in entries]
    if len(entries) != 13:
        findings.append(Finding("REGISTRY_COUNT", "error", str(manifest_path), f"expected 13 aggregates, found {len(entries)}"))
    if len(numbers) != len(set(numbers)) or len(names) != len(set(names)):
        findings.append(Finding("REGISTRY_DUPLICATE", "error", str(manifest_path), "aggregate numbers and names must be unique"))

    if manifest["required_sequence"] != "ABCDEFGHIJKLMNOP":
        findings.append(Finding("SEQUENCE", "error", str(manifest_path), "required_sequence must be ABCDEFGHIJKLMNOP"))
    if manifest["schema_version"] == 2:
        if manifest["baseline_status"] != "approved":
            findings.append(Finding("BASELINE_STATUS", "error", str(manifest_path), "schema 2 baseline must be approved"))
        if manifest.get("release_tag") != "domain-model-v1.0.0":
            findings.append(Finding("RELEASE_TAG", "error", str(manifest_path), "unexpected or missing release tag"))

    reference_files = list(domain_root.rglob("*.md")) + list((repo_root / "adr").glob("*.md"))
    by_basename: dict[str, list[Path]] = {}
    for path in reference_files:
        by_basename.setdefault(path.name, []).append(path)
    for basename, paths in by_basename.items():
        if len(paths) > 1:
            findings.append(Finding("DUPLICATE_BASENAME", "error", basename, "reference resolution is ambiguous"))

    expected_dirs = set()
    for entry in entries:
        aggregate_dir = aggregates_root / entry["name"]
        expected_dirs.add(aggregate_dir.resolve())
        if not aggregate_dir.is_dir():
            findings.append(Finding("AGGREGATE_DIR", "error", str(aggregate_dir), "aggregate directory is missing"))
            continue
        manifest_documents = entry.get("documents", {})
        for letter in entry.get("not_applicable", []):
            if letter not in SECTIONS:
                findings.append(Finding("INVALID_NA", "error", str(manifest_path), f"{entry['name']} declares invalid N/A section {letter}"))
        for filename in expected_documents(entry, manifest["required_sequence"]):
            path = aggregate_dir / filename
            relative = str(path.relative_to(repo_root))
            if not path.is_file():
                findings.append(Finding("MISSING_DOCUMENT", "error", relative, "required document is missing"))
                continue
            text = path.read_text(encoding="utf-8")
            expected_id = filename.split("-", 2)[1]
            first_heading = next((line for line in text.splitlines() if line.startswith("# ")), "")
            if expected_id not in first_heading:
                findings.append(Finding("TITLE_ID", "error", relative, f"first heading must identify {expected_id}"))
            version = metadata_value(text, ("Versión", "Version"))
            status = metadata_value(text, ("Estado", "Status"))
            if version is None:
                findings.append(Finding("MISSING_VERSION", "error", relative, "document version metadata is missing"))
            if status is None:
                findings.append(Finding("MISSING_STATUS", "error", relative, "document status metadata is missing"))
            elif status.casefold() not in {"official", "oficial"}:
                findings.append(Finding("NON_OFFICIAL", "warning", relative, f"document status is {status!r}"))
            if manifest["schema_version"] == 2:
                fingerprint = manifest_documents.get(filename)
                if not fingerprint:
                    findings.append(Finding("MISSING_FINGERPRINT", "error", relative, "document fingerprint is absent"))
                else:
                    if fingerprint.get("version") != version:
                        findings.append(Finding("VERSION_MISMATCH", "error", relative, "manifest version differs from document"))
                    if fingerprint.get("sha256") != content_sha256(path):
                        findings.append(Finding("HASH_MISMATCH", "error", relative, "manifest hash differs from document"))
            if check_git and tracked and path.resolve() not in tracked:
                findings.append(Finding("UNTRACKED_DOCUMENT", "error", relative, "required document is not tracked by Git"))

    actual_dirs = {path.resolve() for path in aggregates_root.iterdir() if path.is_dir()}
    for unexpected in sorted(actual_dirs - expected_dirs):
        findings.append(Finding("UNREGISTERED_AGGREGATE", "error", str(unexpected.relative_to(repo_root)), "aggregate directory is absent from manifest"))

    adr_ids = {path.stem.removeprefix("ADR-") for path in (repo_root / "adr").glob("ADR-*.md")}
    for path in reference_files:
        if path.name == "DOMAIN-MODEL-CLOSURE.md":
            continue
        text = path.read_text(encoding="utf-8")
        for reference in sorted(set(REFERENCE_RE.findall(text))):
            if reference not in by_basename:
                findings.append(Finding("BROKEN_REFERENCE", "error", str(path.relative_to(repo_root)), f"unresolved reference: {reference}"))
        for adr_id in sorted(set(ADR_REFERENCE_RE.findall(text))):
            if adr_id not in adr_ids:
                findings.append(Finding("BROKEN_ADR_REFERENCE", "error", str(path.relative_to(repo_root)), f"unresolved ADR: ADR-{adr_id}"))
        if path.is_relative_to(domain_root / "core") or path.is_relative_to(aggregates_root):
            for code, pattern in PROHIBITED_RULES.items():
                if pattern.search(text):
                    findings.append(Finding(code, "error", str(path.relative_to(repo_root)), "prohibited legacy architecture statement"))

    canonical = domain_root / "DOMAIN-MODEL-CLOSURE.md"
    exported = repo_root / "DOMAIN-MODEL-CLOSURE.md"
    if not canonical.is_file() or not exported.is_file():
        findings.append(Finding("CLOSURE_EXPORT", "error", "DOMAIN-MODEL-CLOSURE.md", "canonical or exported closure report is missing"))
    elif canonical.read_bytes() != exported.read_bytes():
        findings.append(Finding("CLOSURE_EXPORT", "error", str(exported), "root export differs from canonical report"))

    return sorted(findings, key=lambda item: (item.severity != "error", item.code, item.path, item.message))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--no-git", action="store_true", help="skip Git tracking checks")
    parser.add_argument("--json", action="store_true", help="emit machine-readable findings")
    parser.add_argument("--refresh-manifest", action="store_true", help="write schema 2 versions and hashes")
    args = parser.parse_args()

    repo_root = args.root.resolve()
    manifest_path = (args.manifest or repo_root / "docs" / "architecture" / "domain" / "domain-model-baseline.json").resolve()
    try:
        if args.refresh_manifest:
            refresh_manifest(repo_root, manifest_path)
        findings = validate(repo_root, manifest_path, check_git=not args.no_git)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"validator configuration error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([asdict(finding) for finding in findings], ensure_ascii=False, indent=2))
    else:
        for finding in findings:
            print(f"{finding.severity.upper()} {finding.code} {finding.path}: {finding.message}")
        errors = sum(finding.severity == "error" for finding in findings)
        warnings = len(findings) - errors
        print(f"Domain model validation: {errors} error(s), {warnings} warning(s)")
    return 1 if any(finding.severity == "error" for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
