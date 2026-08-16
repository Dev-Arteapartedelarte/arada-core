# DOMAIN-001I — Organization Versioning

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## AggregateVersion

Toda Organization posee una AggregateVersion monotónica. La creación
confirmada establece la versión inicial; cada Command que modifica estado
la incrementa exactamente una vez.

Lecturas, validaciones rechazadas, fallos de autorización, publicación de
eventos y actualización de Read Models no incrementan la versión.

El Repository compara ExpectedAggregateVersion con la persistida y
rechaza escrituras obsoletas sin sobrescribir cambios confirmados.

AggregateVersion no es versión documental ni versión de Integration
Event. Event Sourcing puede usarla en el futuro, pero no es obligatorio.
