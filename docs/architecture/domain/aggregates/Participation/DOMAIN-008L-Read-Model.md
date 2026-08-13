# DOMAIN-008L — Participation Read Model

Versión: 1.0

Estado:
Oficial

Proyecto:
AURA Core

Bounded Context:
Participation Management

Aggregate:
Participation

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-008-Aggregate.md
- DOMAIN-008D-Domain-Events.md
- DOMAIN-008K-Integration-Events.md
- CORE-005-Domain-Events.md

---

# Objetivo

Este documento define el modelo oficial de lectura (Read
Model) del Aggregate **Participation**.

Los Read Models representan vistas optimizadas para consulta y
visualización. No contienen lógica de negocio y no forman parte
del Aggregate.

Su propósito es proporcionar consultas rápidas y escalables sin
afectar la consistencia del lado de escritura.

---

# Principios

Los Read Models siguen los siguientes principios:

- son derivados del dominio;
- son reconstruibles;
- son de solo lectura;
- están desacoplados del Aggregate;
- pueden desnormalizar información;
- pueden existir múltiples proyecciones para un mismo
  Aggregate.

---

# Arquitectura

```text
                Commands

                    │

                    ▼

         Participation Aggregate

                    │

             Domain Events

                    │

                    ▼

             Projection Engine

                    │

      ┌─────────────┼─────────────┐

      ▼             ▼             ▼

Participation   Dashboard     Analytics
    View

```

---

# Fuente de Verdad

La única fuente oficial de verdad es:

```text
Participation Aggregate
```

y su historial de:

```text
Domain Events
```

Los Read Models pueden eliminarse y reconstruirse en cualquier
momento.

---

# Proyecciones Oficiales

El Bounded Context Participation mantiene las siguientes
proyecciones.

```text
ParticipationSummary

ParticipationDetail

ParticipationDirectory

ParticipationStatus

ParticipationContext

ParticipationByCitizen

ParticipationByOrganization

ParticipationStatistics
```

---

# ParticipationSummary

Vista utilizada para listados rápidos.

Campos conceptuales:

```text
ParticipationId

ParticipationType

Status

CitizenId

OrganizationId

CreatedAt

LastUpdated
```

Uso:

- tablas;
- buscadores;
- selección de participaciones.

---

# ParticipationDetail

Vista completa de la participación.

Campos conceptuales:

```text
ParticipationId

ParticipationType

Status

Context

CitizenId

OrganizationId

AssemblyId

ProposalId

Metadata

CreatedAt

ActivatedAt

CompletedAt

WithdrawnAt

InvalidatedAt

ArchivedAt

Version
```

Uso:

- detalle de participación;
- panel administrativo;
- consulta detallada.

---

# ParticipationDirectory

Optimizada para búsquedas.

Campos indexables:

```text
ParticipationId

ParticipationType

Status

CitizenId

OrganizationId

AssemblyId

ProposalId
```

Uso:

- búsqueda rápida;
- filtros;
- selección de participaciones.

---

# ParticipationStatus

Resume únicamente el estado operativo.

```text
ParticipationId

Status

Registered

Active

Completed

Withdrawn

Invalidated

Archived
```

Uso:

- validaciones;
- dashboards;
- control operativo.

---

# ParticipationContext

Representa el contexto asociado a la participación.

```text
ParticipationId

ParticipationType

CitizenId

OrganizationId

AssemblyId

ProposalId

Context
```

Uso:

- consultas contextuales;
- navegación;
- correlación con otros elementos del dominio.

---

# ParticipationByCitizen

Resume las participaciones asociadas a un ciudadano.

```text
CitizenId

Participations

ParticipationTypes

ParticipationStatuses

Organizations

Assemblies

Proposals
```

Uso:

- historial de participación;
- perfil ciudadano;
- indicadores de participación.

---

# ParticipationByOrganization

Resume las participaciones asociadas a una organización.

```text
OrganizationId

Participations

Citizens

ParticipationTypes

ParticipationStatuses

Assemblies

Proposals
```

Uso:

- gestión organizacional;
- indicadores;
- dashboards.

---

# ParticipationStatistics

Vista agregada para análisis.

Ejemplos:

```text
Total Participations

Active Participations

Completed Participations

Withdrawn Participations

Invalidated Participations

Archived Participations

Participations per Type

Participations per Organization

Participations per Citizen

Participations per Assembly

Participations per Proposal
```

Uso:

- BI;
- KPIs;
- dashboards ejecutivos;
- análisis de participación ciudadana.

---

# Actualización

Los Read Models se actualizan mediante:

```text
ParticipationRegistered

↓

Projection
```

```text
ParticipationActivated

↓

Projection
```

```text
ParticipationCompleted

↓

Projection
```

```text
ParticipationWithdrawn

↓

Projection
```

```text
ParticipationInvalidated

↓

Projection
```

```text
ParticipationArchived

↓

Projection
```

```text
ParticipationTypeChanged

↓

Projection
```

```text
ParticipationContextChanged

↓

Projection
```

```text
ParticipationMetadataUpdated

↓

Projection
```

Cada evento actualiza únicamente las proyecciones afectadas.

---

# Reconstrucción

Todas las proyecciones pueden regenerarse.

Proceso:

```text
Replay

↓

Domain Events

↓

Projection Engine

↓

Read Models
```

No se requiere información adicional.

---

# Consistencia

Los Read Models utilizan:

```text
Eventually Consistent
```

Puede existir un pequeño retraso entre:

```text
Command

↓

Commit

↓

Projection Update
```

Este comportamiento es esperado.

---

# Consultas

Los Read Models permiten consultas como:

- participaciones activas;
- participaciones completadas;
- participaciones retiradas;
- participaciones invalidadas;
- participaciones archivadas;
- participaciones por tipo;
- participaciones por ciudadano;
- participaciones por organización;
- participaciones por asamblea;
- participaciones por propuesta;
- indicadores de participación;
- estadísticas agregadas.

Estas consultas nunca acceden directamente al Aggregate.

---

# Persistencia

Las proyecciones pueden almacenarse en:

- PostgreSQL;
- MongoDB;
- Elasticsearch;
- Redis;
- OpenSearch;
- cualquier motor optimizado para lectura.

La elección pertenece a la infraestructura.

---

# Rendimiento

Las proyecciones están optimizadas para:

- lecturas masivas;
- paginación;
- filtros;
- búsquedas;
- ordenamiento;
- agregaciones.

Nunca ejecutan lógica de negocio.

---

# Seguridad

Cada Read Model expone únicamente la información autorizada.

Dependiendo del consumidor, una proyección puede:

- ocultar datos personales;
- anonimizar información;
- excluir atributos sensibles;
- aplicar políticas de privacidad.

La autorización pertenece a la capa de aplicación.

---

# Compatibilidad con CQRS

Este documento representa el lado de lectura del patrón CQRS.

```text
Write Side

Participation Aggregate

↓

Domain Events

↓

Read Side

Participation Read Models
```

Ambos lados evolucionan de forma independiente.

---

# Compatibilidad con Event Sourcing

Los Read Models no almacenan la historia completa.

La historia permanece en los Domain Events.

Las proyecciones son únicamente una representación materializada
de dicha historia.

---

# Evolución

Nuevas proyecciones podrán incorporarse sin modificar el
Aggregate, siempre que:

- consuman Domain Events;
- no introduzcan lógica de negocio;
- mantengan independencia del lado de escritura;
- respeten el lenguaje ubicuo.

---

# Principios Arquitectónicos

Los Read Models siguen:

- Domain-Driven Design (DDD);
- CQRS;
- Event Sourcing;
- Event-Driven Architecture;
- Clean Architecture;
- Single Responsibility Principle.

---

# Definición de Éxito

Los Read Models del Aggregate **Participation** proporcionan vistas
especializadas, reconstruibles y optimizadas para consulta,
permitiendo que el ecosistema AURA ofrezca búsquedas,
estadísticas, paneles de control y servicios de alta
disponibilidad sin comprometer la consistencia del dominio ni
acoplar el lado de lectura al Aggregate de escritura.