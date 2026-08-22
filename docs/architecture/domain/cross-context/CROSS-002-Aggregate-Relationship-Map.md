# CROSS-002 — Aggregate Relationship Map

Versión: 1.0

Estado: Consolidated

Baseline: `domain-model-v1.0.0`

## Regla de lectura

La flecha parte del Aggregate que conserva una referencia y apunta al dueño de
la identidad. Una referencia no permite modificar el Aggregate destino.

## Relaciones oficiales

| Consumidor | Dueño | Referencia | Obligatoriedad | Ownership | Consistencia |
|---|---|---|---|---|---|
| Organization | Territory | TerritoryId | Condicional según tipo | Territory | Eventual |
| Membership | Citizen | CitizenId | Obligatoria | Citizen | Eventual |
| Membership | Organization | OrganizationId | Obligatoria | Organization | Eventual |
| Role | Organization | OrganizationId | Opcional en v1 | Organization | Eventual |
| Territory | Territory | ParentTerritoryId | Opcional | Territory padre | Eventual entre instancias |
| Assembly | Organization | OrganizationId | Obligatoria | Organization | Eventual |
| Assembly | Territory | TerritoryId | Opcional | Territory | Eventual |
| Proposal | Organization | OrganizationId | Obligatoria | Organization | Eventual |
| Proposal | Citizen | CitizenId | Condicional al origen | Citizen | Eventual |
| Proposal | Membership | MembershipId | Condicional al origen | Membership | Eventual |
| Proposal | Territory | TerritoryId | Opcional | Territory | Eventual |
| Proposal | Assembly | AssemblyId | Opcional | Assembly | Eventual |
| Participation | Organization | OrganizationId | Obligatoria | Organization | Eventual |
| Participation | Citizen | CitizenId | Condicional al actor | Citizen | Eventual |
| Participation | Membership | MembershipId | Condicional al actor | Membership | Eventual |
| Participation | Territory | TerritoryId | Opcional | Territory | Eventual |
| Participation | Assembly | AssemblyId | Opcional | Assembly | Eventual |
| Participation | Proposal | ProposalId | Opcional | Proposal | Eventual |
| Participation | Voting | VotingId | Opcional | Voting | Eventual |
| Voting | Organization | OrganizationId | Obligatoria | Organization | Eventual |
| Voting | Assembly | AssemblyId | Condicional al contexto | Assembly | Eventual |
| Voting | Proposal | ProposalId | Condicional al contexto | Proposal | Eventual |
| Document | Contexto origen | ReferenceId tipado | Condicional | Contexto referenciado | Eventual |
| Notification | Hecho/destinatario | ReferenceId tipado | Condicional | Contexto referenciado | Eventual |
| Audit | Hecho origen | SourceAggregateId/SourceEventId | Obligatoria | Contexto productor | Eventual |
| Integration | Sistema externo | ExternalSystemReference | Condicional al vínculo | Sistema externo | Eventual |

## Reglas

- sólo el dueño valida y modifica su identidad;
- el consumidor puede validar existencia mediante un contrato de lectura;
- la eliminación o suspensión del destino no muta automáticamente al consumidor;
- ninguna fila habilita joins de escritura, foreign Aggregate objects o cascadas;
- las relaciones opcionales no se vuelven obligatorias por conveniencia técnica;
- las referencias a hechos de Document, Notification y Audit son tipadas y
  minimizadas.

## Relación conceptual

```text
Consumer Aggregate
    │ stores TargetId
    ▼
Explicit validation or confirmed contract
    ▼
Owner Aggregate
```

## Resultado

Todas las relaciones del Context Map conservan dirección, ownership y
consistencia explícitos sin ampliar ningún Aggregate Boundary.
