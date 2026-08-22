# AURA Core

AURA Core es el núcleo conceptual de Smart Community Platform. Este repositorio
contiene el Domain Model normativo y su consolidación transversal; todavía no
expone una aplicación, API ni runtime productivo.

## Estado

- baseline inmutable: `domain-model-v1.0.0`;
- 13 Bounded Contexts y 13 Aggregates;
- 221 documentos normativos de Aggregate;
- 120 relaciones Command → Domain Event verificadas;
- 83 contratos públicos inventariados desde los documentos K;
- mapas de relaciones, consistencia, contratos y eventos completos;
- Application, adapters e infraestructura: diferidos.

Los hallazgos y contradicciones del baseline se registran en
[`CROSS-001-Transversal-Audit.md`](docs/architecture/domain/cross-context/CROSS-001-Transversal-Audit.md).
La consolidación no modifica reglas normativas ni infiere consumidores.

## Documentación principal

- [`DOMAIN-MODEL-CLOSURE.md`](DOMAIN-MODEL-CLOSURE.md): cierre del baseline.
- [`ARCHITECTURE-AND-DEVELOPMENT-PLAN.md`](ARCHITECTURE-AND-DEVELOPMENT-PLAN.md): alcance y evolución aprobada.
- [`Smart-Community-Platform.md`](Smart-Community-Platform.md): visión estratégica.
- [`PENDIENTES.md`](PENDIENTES.md): backlog posterior a la consolidación.
- [`docs/architecture/domain/cross-context/`](docs/architecture/domain/cross-context/): evidencia transversal.
- [`docs/architecture/domain/events/event-catalog.md`](docs/architecture/domain/events/event-catalog.md): trazabilidad de eventos.

## Calidad

```bash
pytest -q
ruff check src tests
mypy src
python3 scripts/validate_domain_model.py
```

El validador comprueba estructura, referencias, manifiesto y hashes del Domain
Model. Las pruebas transversales comprueban cobertura, contratos, límites de
eventos, documentos no vacíos y diagramas válidos.

## Límites actuales

No hay endpoints, workers, simuladores, Compose, servicios externos ni
configuración de laboratorio. La selección de framework, persistencia,
mensajería, identidad, observabilidad e integración requiere una decisión
arquitectónica futura y explícita.
