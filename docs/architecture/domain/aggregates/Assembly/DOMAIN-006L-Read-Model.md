# DOMAIN-006L — Assembly Read Model

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Assembly Management

Aggregate:
Assembly

Documentos relacionados:

* DOMAIN-006-Aggregate.md
* DOMAIN-006D-Domain-Events.md
* DOMAIN-006K-Integration-Events.md
* CORE-005-Domain-Events.md

---

# Objetivo

Este documento define el modelo oficial de lectura (Read
Model) del Aggregate **Assembly**.

Los Read Models representan vistas optimizadas para consulta y
visualización. No contienen lógica de negocio y no forman parte
del Aggregate.

Su propósito es proporcionar consultas rápidas y escalables sin
afectar la consistencia del lado de escritura.

---

# Principios

Los Read Models siguen los siguientes principios:

* son derivados del dominio;
* son reconstruibles;
* son de solo lectura;
* están desacoplados del Aggregate;
* pueden desnormalizar información;
* pueden existir múltiples proyecciones para un mismo
  Aggregate.

---

# Arquitectura

```text
                Commands

                    │

                    ▼

            Assembly Aggregate

                    │

             Domain Events

                    │

                    ▼

             Projection Engine

                    │

      ┌─────────────┼─────────────┐

      ▼             ▼             ▼

Assembly View   Dashboard     Analytics
```

---

# Fuente de Verdad

La única fuente oficial de verdad es:

```text
Assembly Aggregate
```

y su historial de:

```text
Domain Events
```

Los Read Models pueden eliminarse y reconstruirse en cualquier
momento.

---

# Proyecciones Oficiales

El Bounded Context Assembly mantiene las siguientes
proyecciones.

```text
AssemblySummary

AssemblyDetail

AssemblySchedule

AssemblyConvocation

AssemblyStatus

AssemblyTerritory
```

---

# AssemblySummary

Vista utilizada para listados rápidos.

Campos conceptuales:

```text
AssemblyId

OrganizationId

TerritoryId

AssemblyName

AssemblyType

AssemblyStatus

ScheduledStart

ScheduledEnd

AssemblyMode
```

Uso:

* tablas;
* listados;
* buscadores;
* selección de Assemblies.

---

# AssemblyDetail

Vista completa de la Assembly.

Campos conceptuales:

```text
AssemblyId

OrganizationId

TerritoryId

AssemblyName

AssemblyType

AssemblyPurpose

AssemblyDescription

ScheduledStart

ScheduledEnd

AssemblyMode

Location

ConvocationStatus

ConvokedAt

ConvocationDeadline

AssemblyStatus

CreatedAt

UpdatedAt

ArchivedAt

Version
```

Uso:

* detalle de Assembly;
* panel administrativo;
* consulta detallada;
* visualización del estado actual.

---

# AssemblySchedule

Representa la programación formal de la Assembly.

Campos conceptuales:

```text
AssemblyId

OrganizationId

TerritoryId

AssemblyName

AssemblyType

ScheduledStart

ScheduledEnd

AssemblyMode

Location

AssemblyStatus
```

Uso:

* agendas;
* calendarios;
* programación;
* consultas temporales.

---

# AssemblyConvocation

Representa la información formal de convocatoria.

Campos conceptuales:

```text
AssemblyId

OrganizationId

AssemblyName

AssemblyType

ScheduledStart

ScheduledEnd

AssemblyMode

Location

ConvocationStatus

ConvokedAt

ConvocationDeadline

AssemblyStatus
```

Uso:

* consulta de convocatoria;
* seguimiento de Assemblies convocadas;
* visualización de información formal de convocatoria.

---

# AssemblyStatus

Resume únicamente el estado operativo del Aggregate.

```text
AssemblyId

AssemblyStatus

ScheduledStart

ScheduledEnd

ConvocationStatus

ConvokedAt

StartedAt

CompletedAt

CancelledAt

ArchivedAt

Version
```

Uso:

* validaciones;
* dashboards;
* control operativo;
* seguimiento del Lifecycle.

---

# AssemblyTerritory

Representa el contexto territorial asociado a la Assembly.

```text
AssemblyId

OrganizationId

TerritoryId

AssemblyName

AssemblyType

AssemblyStatus

ScheduledStart

AssemblyMode
```

Uso:

* mapas;
* estadísticas;
* planificación territorial;
* consulta de Assemblies por Territory.

---

# Actualización

Los Read Models se actualizan mediante:

```text
AssemblyCreated

↓

Projection
```

```text
AssemblyScheduled

↓

Projection
```

```text
AssemblyRescheduled

↓

Projection
```

```text
AssemblyConvoked

↓

Projection
```

```text
AssemblyStarted

↓

Projection
```

```text
AssemblyCompleted

↓

Projection
```

```text
AssemblyCancelled

↓

Projection
```

```text
AssemblyArchived

↓

Projection
```

```text
AssemblyRenamed

↓

Projection
```

```text
AssemblyPurposeChanged

↓

Projection
```

```text
AssemblyDescriptionChanged

↓

Projection
```

```text
AssemblyTypeChanged

↓

Projection
```

```text
AssemblyModeChanged

↓

Projection
```

```text
AssemblyLocationChanged

↓

Projection
```

```text
AssemblyConvocationUpdated

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

* Assemblies por Organization;
* Assemblies por Territory;
* Assemblies por estado;
* Assemblies por tipo;
* Assemblies por modalidad;
* Assemblies programadas;
* Assemblies convocadas;
* Assemblies en curso;
* Assemblies completadas;
* Assemblies canceladas;
* Assemblies archivadas;
* Assemblies dentro de un período determinado;
* información formal de convocatoria;
* información territorial de una Assembly.

Estas consultas nunca acceden directamente al Aggregate.

---

# Persistencia

Las proyecciones pueden almacenarse en:

* PostgreSQL;
* MongoDB;
* Elasticsearch;
* Redis;
* OpenSearch;
* cualquier motor optimizado para lectura.

La elección pertenece a la infraestructura.

---

# Rendimiento

Las proyecciones están optimizadas para:

* lecturas masivas;
* paginación;
* filtros;
* búsquedas;
* ordenamiento;
* agregaciones.

Nunca ejecutan lógica de negocio.

---

# Seguridad

Cada Read Model expone únicamente la información autorizada.

Dependiendo del consumidor, una proyección puede:

* ocultar información no autorizada;
* excluir atributos sensibles;
* limitar información según Organization;
* aplicar políticas de privacidad.

La autorización pertenece a la capa de aplicación.

---

# Compatibilidad con CQRS

Este documento representa el lado de lectura del patrón CQRS.

```text
Write Side

Assembly Aggregate

↓

Domain Events

↓

Read Side

Assembly Read Models
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

* consuman Domain Events;
* no introduzcan lógica de negocio;
* mantengan independencia del lado de escritura;
* respeten el lenguaje ubicuo.

---

# Principios Arquitectónicos

Los Read Models siguen:

* Domain-Driven Design (DDD);
* CQRS;
* Event Sourcing;
* Event-Driven Architecture;
* Clean Architecture;
* Single Responsibility Principle.

---

# Definición de Éxito

Los Read Models del Aggregate **Assembly** proporcionan vistas
especializadas, reconstruibles y optimizadas para consulta,
permitiendo que el ecosistema AURA ofrezca búsquedas,
programación, seguimiento de convocatoria, visualización de
estado, consultas territoriales, paneles de control y servicios
de alta disponibilidad sin comprometer la consistencia del
dominio ni acoplar el lado de lectura al Aggregate de escritura.

Las proyecciones de Assembly representan exclusivamente
información derivada de hechos válidamente confirmados por el
Aggregate y nunca constituyen una vía alternativa para modificar
su estado.

De esta forma, el modelo de lectura de **Assembly** mantiene la
separación entre escritura y consulta, preserva la autonomía del
Aggregate, permite reconstrucción a partir de Domain Events y
mantiene compatibilidad con la arquitectura CQRS, Event Sourcing
y Event-Driven Architecture definida para AURA Core.
