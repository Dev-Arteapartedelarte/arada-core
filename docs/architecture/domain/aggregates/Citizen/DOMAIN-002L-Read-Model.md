# DOMAIN-002L — Citizen Read Model

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Citizen Management

Aggregate:
Citizen

Documentos relacionados:

- DOMAIN-002-Aggregate.md
- DOMAIN-002D-Domain-Events.md
- DOMAIN-002K-Integration-Events.md
- CORE-005-Domain-Events.md

---

# Objetivo

Este documento define el modelo oficial de lectura (Read
Model) del Aggregate **Citizen**.

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

            Citizen Aggregate

                    │

             Domain Events

                    │

                    ▼

             Projection Engine

                    │

      ┌─────────────┼─────────────┐

      ▼             ▼             ▼

 Citizen View   Dashboard     Analytics

```

---

# Fuente de Verdad

La única fuente oficial de verdad es:

```text
Citizen Aggregate
```

y su historial de:

```text
Domain Events
```

Los Read Models pueden eliminarse y reconstruirse en cualquier
momento.

---

# Proyecciones Oficiales

El Bounded Context Citizen mantiene las siguientes
proyecciones.

```text
CitizenSummary

CitizenProfile

CitizenDirectory

CitizenStatus

CitizenContact

CitizenTerritory

CitizenParticipation

CitizenStatistics
```

---

# CitizenSummary

Vista utilizada para listados rápidos.

Campos conceptuales:

```text
CitizenId

FullName

Status

OrganizationId

CreatedAt

LastUpdated
```

Uso:

- tablas;
- buscadores;
- selección de ciudadanos.

---

# CitizenProfile

Vista completa del ciudadano.

Campos conceptuales:

```text
CitizenId

Personal Information

Contact Information

Address

Preferred Language

Status

Verification Status

Consent Status

Version
```

Uso:

- perfil ciudadano;
- panel administrativo;
- consulta detallada.

---

# CitizenDirectory

Optimizada para búsquedas.

Campos indexables:

```text
CitizenId

FullName

Email

Phone

Neighborhood

OrganizationId
```

Uso:

- autocompletado;
- búsqueda rápida;
- filtros.

---

# CitizenStatus

Resume únicamente el estado operativo.

```text
CitizenId

Lifecycle State

Verified

Active

Suspended

Archived
```

Uso:

- validaciones;
- dashboards;
- control operativo.

---

# CitizenContact

Contiene exclusivamente información de contacto.

```text
CitizenId

Email

Phone

Preferred Contact Method
```

Uso:

- notificaciones;
- comunicaciones.

---

# CitizenTerritory

Representa la localización administrativa del ciudadano.

```text
CitizenId

Region

Commune

Neighborhood

TerritoryId
```

Uso:

- mapas;
- estadísticas;
- planificación territorial.

---

# CitizenParticipation

Resume la actividad del ciudadano.

```text
CitizenId

Organizations

Memberships

Assemblies

Votes

Proposals

Participation Score
```

Uso:

- indicadores;
- participación ciudadana;
- gobierno abierto.

---

# CitizenStatistics

Vista agregada para análisis.

Ejemplos:

```text
Active Citizens

Verified Citizens

Suspended Citizens

Citizens per Territory

Growth Rate

Participation Index
```

Uso:

- BI;
- KPIs;
- dashboards ejecutivos.

---

# Actualización

Los Read Models se actualizan mediante:

```text
CitizenRegistered

↓

Projection
```

```text
CitizenVerified

↓

Projection
```

```text
CitizenActivated

↓

Projection
```

```text
CitizenProfileUpdated

↓

Projection
```

```text
CitizenAddressUpdated

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

- ciudadanos activos;
- ciudadanos verificados;
- ciudadanos por territorio;
- ciudadanos por organización;
- ciudadanos suspendidos;
- ciudadanos con participación reciente;
- indicadores de crecimiento;
- distribución geográfica.

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

Citizen Aggregate

↓

Domain Events

↓

Read Side

Citizen Read Models
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

Los Read Models del Aggregate **Citizen** proporcionan vistas
especializadas, reconstruibles y optimizadas para consulta,
permitiendo que el ecosistema AURA ofrezca búsquedas,
estadísticas, paneles de control y servicios de alta
disponibilidad sin comprometer la consistencia del dominio ni
acoplar el lado de lectura al Aggregate de escritura.