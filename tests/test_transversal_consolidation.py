from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = ROOT / "docs" / "architecture" / "domain"

AGGREGATES = (
    "Organization",
    "Citizen",
    "Membership",
    "Role",
    "Territory",
    "Assembly",
    "Proposal",
    "Participation",
    "Voting",
    "Document",
    "Notification",
    "Audit",
    "Integration",
)

TRANSVERSAL_DOCUMENTS = (
    DOMAIN / "cross-context" / "CROSS-001-Transversal-Audit.md",
    DOMAIN / "cross-context" / "CROSS-002-Aggregate-Relationship-Map.md",
    DOMAIN / "cross-context" / "CROSS-003-Consistency-Boundary-Map.md",
    DOMAIN / "cross-context" / "CROSS-004-Cross-Domain-Contracts.md",
    DOMAIN / "events" / "event-catalog.md",
)

DEFERRED_DOCUMENTS = (
    DOMAIN / "services" / "application-services.md",
    DOMAIN / "services" / "domain-services.md",
    DOMAIN / "services" / "sagas.md",
    DOMAIN / "repositories" / "repository-guidelines.md",
)

DIAGRAMS = tuple((DOMAIN / "diagrams").glob("*.drawio"))


def test_transversal_documents_cover_all_aggregates() -> None:
    for path in TRANSVERSAL_DOCUMENTS:
        content = path.read_text(encoding="utf-8")
        missing = [aggregate for aggregate in AGGREGATES if aggregate not in content]
        assert not missing, f"{path} does not cover: {', '.join(missing)}"


def test_event_catalog_has_one_hundred_twenty_official_mappings() -> None:
    catalog = (DOMAIN / "events" / "event-catalog.md").read_text(encoding="utf-8")
    rows: list[tuple[str, str, str]] = []
    current_aggregate: str | None = None
    for line in catalog.splitlines():
        heading = re.fullmatch(r"## DOMAIN-\d{3} — ([A-Za-z]+)", line)
        if heading:
            current_aggregate = heading.group(1)
            continue
        if not line.startswith("| ") or line.startswith("|---") or "Command |" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if current_aggregate and len(cells) == 3 and re.fullmatch(r"[A-Z][A-Za-z]+", cells[0]):
            rows.append((current_aggregate, cells[0], cells[1]))
    assert len(rows) == 120

    for aggregate, command, domain_event in rows:
        directory = DOMAIN / "aggregates" / aggregate
        commands_document = next(directory.glob("*C-Commands.md")).read_text(encoding="utf-8")
        events_document = next(directory.glob("*D-Domain-Events.md")).read_text(encoding="utf-8")
        assert command in commands_document
        assert domain_event in events_document


def test_public_contract_inventory_is_explicit() -> None:
    catalog = (DOMAIN / "events" / "event-catalog.md").read_text(encoding="utf-8")
    contracts = set(re.findall(r"\b[A-Z][A-Za-z]+(?:IntegrationEvent|ForIntegration)\b", catalog))
    contracts.update(
        name
        for name in ("AssemblyPublished", "AssemblyConvocationPublished", "AssemblyDetailsChanged")
        if name in catalog
    )
    assert len(contracts) == 83
    assert "AssemblyPublished" in contracts
    assert "ProposalUpdatedForIntegration" in contracts


def test_transversal_artifacts_are_not_empty_and_diagrams_are_valid_xml() -> None:
    for path in (*TRANSVERSAL_DOCUMENTS, *DEFERRED_DOCUMENTS, *DIAGRAMS):
        assert path.stat().st_size > 0, f"empty transversal artifact: {path}"
    assert len(DIAGRAMS) == 4
    for path in DIAGRAMS:
        assert ET.parse(path).getroot().tag == "mxfile"


def test_cross_context_documents_preserve_event_boundary() -> None:
    content = "\n".join(path.read_text(encoding="utf-8") for path in TRANSVERSAL_DOCUMENTS)
    assert "Domain Event != Integration Event" in content
    assert "no convierte eventos automáticamente" in content
