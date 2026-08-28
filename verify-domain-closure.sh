#!/usr/bin/env bash

set -euo pipefail

ROOT="${1:-.}"
BASELINE_TAG="domain-model-v1.0.0"

cd "$ROOT"

echo "== AURA Core — verificación de cierre y regresión del Domain Model =="

if [[ ! -d .git ]]; then
  echo "ERROR: no se encontró .git en: $(pwd)" >&2
  exit 2
fi

if [[ ! -d src ]]; then
  echo "ERROR: no se encontró el directorio src en: $(pwd)" >&2
  exit 2
fi

if [[ ! -d tests ]]; then
  echo "ERROR: no se encontró el directorio tests en: $(pwd)" >&2
  exit 2
fi

if [[ ! -f scripts/validate_domain_model.py ]]; then
  echo "ERROR: no se encontró scripts/validate_domain_model.py" >&2
  exit 2
fi

echo
echo "[1/7] HEAD actual"

git rev-parse --short HEAD

echo
echo "[2/7] Verificación del baseline normativo ${BASELINE_TAG}"

if ! git rev-parse --verify --quiet "refs/tags/${BASELINE_TAG}" >/dev/null; then
  echo "ERROR: no existe el tag normativo ${BASELINE_TAG}" >&2
  exit 2
fi

baseline_root="$(mktemp -d)"

cleanup() {
  rm -rf "$baseline_root"
}

trap cleanup EXIT

git archive "$BASELINE_TAG" | tar -x -C "$baseline_root"

python3 "$baseline_root/scripts/validate_domain_model.py" \
  --root "$baseline_root" \
  --no-git

echo
echo "BASELINE NORMATIVO ${BASELINE_TAG}: PASS"

echo
echo "[3/7] Verificación de regresiones semánticas transversales"

fail=0

check_absent() {
  local pattern="$1"
  shift

  local label="$1"
  shift

  local result_file

  result_file="$(mktemp)"

  if grep -nE "$pattern" "$@" >"$result_file" 2>/dev/null; then
    echo "FAIL: $label"
    cat "$result_file"
    fail=1
  else
    echo "PASS: $label"
  fi

  rm -f "$result_file"
}

check_absent \
  'AssemblyMode([^A-Za-z]|$)|ChangeAssemblyMode([^A-Za-z]|$)' \
  "AssemblyMode / ChangeAssemblyMode fuera de artefactos históricos de normalización" \
  docs/architecture/domain/aggregates/Assembly/DOMAIN-006O-Security-Model.md \
  docs/architecture/domain/aggregates/Assembly/DOMAIN-006P-Extension-Points.md \
  docs/architecture/domain/aggregates/Proposal/DOMAIN-007J-Consistency-Boundary.md

check_absent \
  'OpenAssemblyService|CloseAssemblyService' \
  "Application Services usa StartAssemblyService / CompleteAssemblyService" \
  docs/architecture/domain/core/CORE-013-Application-Services.md

check_absent \
  'AssemblyClosed' \
  "CORE-008 no usa AssemblyClosed" \
  docs/architecture/domain/core/CORE-008-Aggregate-Design-Rules.md

check_absent \
  'Assembly[[:space:]]+(Open|Opened|Closed)' \
  "Document Lifecycle no usa lifecycle legado de Assembly" \
  docs/architecture/domain/aggregates/Document/DOMAIN-010A-Lifecycle.md

check_absent \
  'Assembly[[:space:]]+(Open|Opened|Closed)' \
  "Voting no usa lifecycle legado de Assembly" \
  docs/architecture/domain/aggregates/Voting/DOMAIN-009A-Lifecycle.md \
  docs/architecture/domain/aggregates/Voting/DOMAIN-009D-Domain-Events.md \
  docs/architecture/domain/aggregates/Voting/DOMAIN-009K-Integration-Events.md

check_absent \
  'No mapping determinista|Mapping inconsistente|TA-001 impide|TA-002 exige|Relevant Proposal Changes|origen indeterminado|creada o programada' \
  "Hallazgos transversales antiguos eliminados" \
  docs/architecture/domain/cross-context/TA-001-AssemblyPublished-Origin.md \
  docs/architecture/domain/cross-context/TA-002-ProposalUpdatedForIntegration-Origin.md \
  docs/architecture/domain/cross-context/TA-008-AssemblyModalityChanged-Naming.md \
  docs/architecture/domain/cross-context/CROSS-001-Transversal-Audit.md \
  docs/architecture/domain/cross-context/CROSS-004-Cross-Domain-Contracts.md \
  docs/architecture/domain/events/event-catalog.md \
  docs/architecture/domain/aggregates/Proposal/DOMAIN-007K-Integration-Events.md

if [[ "$fail" -ne 0 ]]; then
  echo
  echo "VERIFICACIÓN DE REGRESIONES SEMÁNTICAS: FAIL"
  exit 1
fi

echo
echo "VERIFICACIÓN DE REGRESIONES SEMÁNTICAS: PASS"

echo
echo "[4/7] Tests de consolidación transversal"

python3 -m pytest -q \
  tests/test_transversal_consolidation.py \
  tests/test_validate_domain_model.py

echo
echo "[5/7] Ruff"

ruff check src tests

echo
echo "[6/7] MyPy"

mypy src

echo
echo "[7/7] Pytest completo"

python3 -m pytest -q

echo
echo "== Estado Git =="

git status --short

echo
echo "VERIFICACIÓN FINAL: PASS"
echo
echo "Baseline normativo preservado: ${BASELINE_TAG}"
echo "Este script no modifica archivos, no realiza staging, no crea commits y no ejecuta push."