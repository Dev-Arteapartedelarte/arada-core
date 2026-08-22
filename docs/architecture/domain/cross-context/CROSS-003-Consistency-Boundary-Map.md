# CROSS-003 — Consistency Boundary Map

Versión: 1.0

Estado: Consolidated

Baseline: `domain-model-v1.0.0`

## Principio

```text
One Aggregate Root
    =
One Immediate Consistency Boundary
    =
One Write Commit
```

## Límites inmediatos

| Aggregate Boundary | Estado protegido inmediatamente | Estado excluido |
|---|---|---|
| Organization | identidad, lifecycle, configuración y políticas | Membership, Citizen, Territory |
| Citizen | identidad cívica, perfil, contacto y consentimiento | Membership y Organization |
| Membership | relación Citizen–Organization y lifecycle | Citizen, Organization y Role |
| Role | catálogo y lifecycle del Role | Membership y Permission assignment |
| Territory | identidad, jerarquía propia, geometría y lifecycle | Organization y procesos territoriales |
| Assembly | sesión, programación, convocatoria y lifecycle | Proposal, Participation y Voting |
| Proposal | contenido, referencias y lifecycle | Assembly, Participation y Voting |
| Participation | instancia, contexto y lifecycle | Citizen, Membership, Proposal y Voting |
| Voting | configuración, opciones, resultado y lifecycle | Assembly, Proposal y Participation |
| Document | identidad, metadatos y lifecycle documental | contenido de otros Aggregates |
| Notification | intención, entrega y lifecycle | destinatarios y hechos externos completos |
| Audit | registro inmutable del hecho recibido | Aggregate y evento fuente |
| Integration | vínculo, configuración conceptual y lifecycle | sistema externo y credenciales |

## Colaboración eventual

| Situación | Regla |
|---|---|
| validar una referencia | lectura explícita; no comparte transacción |
| reaccionar a un hecho externo | Integration Event o API Contract explícito |
| producir Notification | inbound adapter y Command propio de Notification |
| producir Audit | inbound adapter y `RecordAudit` |
| actualizar una proyección | después del hecho confirmado; sin autoridad de escritura |
| fallo del consumidor | no revierte el Aggregate productor |
| reentrega | consumidor idempotente según arquitectura futura |

## Operaciones prohibidas

- confirmar dos Aggregates en un mismo commit de dominio;
- modificar un Aggregate mediante Repository de otro contexto;
- incorporar Entities o Value Objects externos dentro del boundary;
- ejecutar cascadas de escritura por una referencia ID;
- tratar un Domain Event ajeno como contrato público;
- usar un Read Model para autorizar o reconstruir silenciosamente escritura;
- revertir un hecho confirmado por fallo de integración;
- asumir orden global entre eventos de Aggregates distintos.

## Coordinación permitida

Un caso de uso futuro puede leer varios Aggregates o coordinar varios pasos,
pero cada modificación conserva commit, versión y resultado independientes. Un
proceso duradero deberá expresar compensaciones de negocio explícitas; no
simulará atomicidad distribuida.

## Resultado

Los trece límites de consistencia son independientes. Toda colaboración entre
ellos se modela como lectura o efecto eventual explícito.
