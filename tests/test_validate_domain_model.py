from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_domain_model.py"
SPEC = importlib.util.spec_from_file_location("validate_domain_model", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_expected_documents_honors_not_applicable() -> None:
    documents = MODULE.expected_documents({"number": "001", "not_applicable": ["H"]}, "ABCDEFGHIJKLMNOP")
    assert "DOMAIN-001-Aggregate.md" in documents
    assert "DOMAIN-001H-Examples.md" not in documents
    assert "DOMAIN-001I-Versioning.md" in documents


def test_metadata_value_supports_inline_and_multiline_values() -> None:
    assert MODULE.metadata_value("Versión: 1.0", ("Versión", "Version")) == "1.0"
    assert MODULE.metadata_value("Estado:\nOfficial", ("Estado", "Status")) == "Official"


def test_sha256_changes_with_content(tmp_path: Path) -> None:
    path = tmp_path / "document.md"
    path.write_text("first", encoding="utf-8")
    first = MODULE.content_sha256(path)
    path.write_text("second", encoding="utf-8")
    assert MODULE.content_sha256(path) != first


def test_validator_reports_missing_sequence_document(tmp_path: Path) -> None:
    aggregate_dir = tmp_path / "docs" / "architecture" / "domain" / "aggregates" / "Example"
    aggregate_dir.mkdir(parents=True)
    (tmp_path / "adr").mkdir()
    (tmp_path / "DOMAIN-MODEL-CLOSURE.md").write_text("closure", encoding="utf-8")
    domain_root = tmp_path / "docs" / "architecture" / "domain"
    (domain_root / "DOMAIN-MODEL-CLOSURE.md").write_text("closure", encoding="utf-8")
    (aggregate_dir / "DOMAIN-001-Aggregate.md").write_text(
        "# DOMAIN-001 — Example Aggregate\n\nVersión: 1.0\n\nEstado: Official\n", encoding="utf-8"
    )
    manifest = {
        "schema_version": 1,
        "baseline_status": "candidate",
        "required_sequence": "ABCDEFGHIJKLMNOP",
        "aggregates": [{"number": "001", "name": "Example", "not_applicable": list("ACDEFGHIJKLMNOP")}],
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    findings = MODULE.validate(tmp_path, manifest_path, check_git=False)
    assert any(item.code == "MISSING_DOCUMENT" and item.path.endswith("DOMAIN-001B-State-Machine.md") for item in findings)


def test_prohibited_rules_detect_legacy_event_contract() -> None:
    assert MODULE.PROHIBITED_RULES["PUBLIC_DOMAIN_EVENT"].search("Los Domain Events son contratos públicos.")


def test_adr_reference_pattern_extracts_identifier() -> None:
    assert MODULE.ADR_REFERENCE_RE.findall("ADR-001 and ADR-003") == ["001", "003"]
