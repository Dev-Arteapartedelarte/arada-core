# AURA Core — Backlog

Estado: consolidación transversal completada

Baseline normativo: `domain-model-v1.0.0`

## Hitos cerrados

- [x] CROSS-001 — Auditar cobertura, referencias y contradicciones.
- [x] CROSS-002 — Mapear relaciones, IDs, ownership y dirección semántica.
- [x] CROSS-003 — Mapear consistencia inmediata, eventual y operaciones prohibidas.
- [x] CROSS-004 — Inventariar contratos K, versiones, productores y consumidores explícitos.
- [x] Catalogar 120 relaciones Command → Domain Event sin conversiones automáticas.
- [x] Inventariar 83 Integration Events públicos definidos por los documentos K.
- [x] Completar diagramas de Aggregates, Context Map, eventos y State Machines.
- [x] Añadir validaciones documentales de cobertura, referencias y fronteras.

## Decisiones de dominio pendientes

Estas decisiones requieren aprobación explícita antes de modificar cualquiera
de los 221 documentos normativos:

- [ ] Resolver TA-001: origen único o semántica de `AssemblyPublished`.
- [ ] Resolver TA-002: origen de `ProposalUpdatedForIntegration`.
- [ ] Resolver TA-008: `AssemblyModeChanged` frente a `AssemblyModalityChanged`.
- [ ] Revisar la normalización futura de nombres registrada por la auditoría.
- [ ] Aprobar consumidores concretos para contratos que hoy no los declaran.

## Etapas futuras

### Producto y Application

- [ ] Validar casos de uso y prioridades con usuarios reales.
- [ ] Definir autorización y puertos de entrada/salida sin redefinir Domain.
- [ ] Definir coordinación explícita entre commits de un solo Aggregate.
- [ ] Evaluar Sagas o Process Managers sólo para procesos duraderos demostrados.

### Arquitectura técnica

- [ ] Decidir API, identidad, persistencia y publicación mediante ADR.
- [ ] Definir semántica operativa, observabilidad, recuperación y despliegue.
- [ ] Seleccionar proveedores o protocolos sólo después de establecer requisitos.
- [ ] Diseñar pruebas de aceptación para el primer corte vertical aprobado.

### Implementación

- [ ] Implementar un corte vertical pequeño después de cerrar Application y ADR.
- [ ] Incorporar adapters e infraestructura sin dependencias hacia Domain.
- [ ] Validar el corte antes de abrir nuevas capacidades.

## Diferido expresamente

No se considera adoptado ningún framework, broker, motor de persistencia,
plataforma IoT, proveedor de contexto ni herramienta de observabilidad. Tampoco
existen endpoints, runtime o laboratorio soportados por `main`.
