# DOMAIN-001P — Extension Points

Versión: 1.0

Estado:
Oficial

Proyecto:
AURA Core

Bounded Context:
Organization Management

Aggregate:
Organization

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-001-Aggregate.md
- DOMAIN-001D-Domain-Events.md
- DOMAIN-001K-Integration-Events.md
- DOMAIN-001L-Read-Model.md
- CORE-003-Shared-Kernel.md
- CORE-007-Strategic-Design.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Definir los puntos oficiales de extensión del Aggregate
Organization.

Los Extension Points permiten que el dominio evolucione
sin modificar el comportamiento existente, respetando el
Principio Open/Closed (OCP).

El Aggregate debe permanecer estable mientras nuevas
capacidades pueden incorporarse mediante adaptadores,
políticas, servicios de aplicación o nuevos Bounded
Contexts.

---

# Principios

Todo punto de extensión debe cumplir las siguientes
reglas.

- no modifica las invariantes;
- no altera la State Machine;
- no rompe la compatibilidad hacia atrás;
- no introduce dependencias de infraestructura;
- no modifica el Aggregate Root.

---

# Filosofía

El Aggregate representa el núcleo del dominio.

Las funcionalidades futuras deben conectarse alrededor
del Aggregate, nunca dentro de él.

```text
             Nuevas capacidades

                    │

        ┌───────────┼───────────┐

        ▼           ▼           ▼

 Analytics     Blockchain    FIWARE

        │           │           │

        └───────────┼───────────┘

                    ▼

            Organization Aggregate
```

---

# EP-001

## Domain Policies

Las reglas variables pueden implementarse mediante
Domain Policies.

Ejemplos.

```text
OrganizationApprovalPolicy

MembershipPolicy

GovernancePolicy

EligibilityPolicy
```

El Aggregate consume la abstracción.

Nunca conoce la implementación.

---

# EP-002

## Domain Services

Cuando una regla involucra múltiples Aggregates o
requiere cálculos complejos, debe implementarse mediante
Domain Services.

Ejemplos.

```text
OrganizationValidationService

OrganizationEligibilityService

TerritoryAssignmentService
```

---

# EP-003

## Application Services

Los casos de uso orquestan el Aggregate sin modificarlo.

Ejemplos.

```text
CreateOrganizationUseCase

ApproveOrganizationUseCase

SuspendOrganizationUseCase

ArchiveOrganizationUseCase
```

---

# EP-004

## Integration Events

Los eventos permiten incorporar nuevos consumidores sin
modificar el Aggregate.

Ejemplo.

```text
OrganizationApproved

↓

Municipality

↓

Blockchain

↓

Analytics

↓

Notifications

↓

FIWARE

↓

Future Modules
```

El Aggregate continúa siendo exactamente el mismo.

---

# EP-005

## Read Models

Nuevas proyecciones pueden añadirse libremente.

Ejemplos.

```text
OrganizationDashboardProjection

OrganizationMapProjection

OrganizationStatisticsProjection

OrganizationTimelineProjection

OrganizationSearchProjection
```

No afectan el modelo de escritura.

---

# EP-006

## External Adapters

Los sistemas externos se integran mediante adaptadores.

Ejemplos.

```text
Municipality Adapter

FIWARE Adapter

Open Data Adapter

Identity Adapter

Email Adapter

Blockchain Adapter
```

Nunca desde el Aggregate.

---

# EP-007

## Authorization

El sistema de permisos puede evolucionar mediante nuevas
políticas.

Ejemplos.

```text
Role Policy

ABAC Policy

RBAC Policy

Organization Scope Policy
```

El Aggregate únicamente recibe la decisión.

---

# EP-008

## Validation Rules

Nuevas validaciones pueden agregarse mediante políticas
especializadas.

Ejemplos.

```text
OrganizationNamePolicy

RepresentativePolicy

TerritoryPolicy

LegalValidationPolicy
```

---

# EP-009

## Notification Channels

La incorporación de nuevos canales de comunicación no
requiere modificar el dominio.

Ejemplos.

```text
Email

SMS

Push

WhatsApp

Signal

Telegram

Citizen Portal
```

Todos consumen Integration Events.

---

# EP-010

## Smart City Integration

La plataforma Smart City evoluciona fuera del dominio.

Ejemplo.

```text
OrganizationApproved

↓

NGSI-LD Adapter

↓

Context Broker

↓

Digital Twin

↓

Dashboards
```

El dominio desconoce completamente estas tecnologías.

---

# EP-011

## Geospatial Extensions

El territorio puede enriquecerse mediante nuevos modelos.

Ejemplos.

```text
GIS

GeoJSON

PostGIS

Spatial Indexes

Map Layers
```

El Aggregate continúa almacenando únicamente
identificadores de territorio.

---

# EP-012

## Artificial Intelligence

Los servicios de IA operan sobre eventos o modelos de
lectura.

Ejemplos.

```text
Risk Analysis

Participation Prediction

Fraud Detection

Community Insights

Recommendation Engine
```

Nunca modifican directamente el Aggregate.

---

# EP-013

## Observability

Los mecanismos de monitoreo se implementan fuera del
dominio.

Ejemplos.

```text
Tracing

Metrics

Audit

Telemetry

Health Monitoring
```

---

# EP-014

## Event Bus

El mecanismo de mensajería puede cambiar sin alterar el
dominio.

Ejemplos.

```text
RabbitMQ

Kafka

NATS

Azure Service Bus

Google Pub/Sub
```

El Aggregate únicamente publica Domain Events.

---

# EP-015

## Persistence

La persistencia es reemplazable mediante el contrato del
Repository.

Ejemplos.

```text
PostgreSQL

MongoDB

Event Store

CockroachDB

CosmosDB
```

El dominio permanece inalterado.

---

# EP-016

## Future Bounded Contexts

El Aggregate está preparado para interactuar con nuevos
contextos.

Ejemplos.

```text
Budget

Projects

Voting

Assets

Facilities

Volunteer

Emergency

Education

Culture

Health

Security
```

La comunicación será exclusivamente mediante Integration
Events.

---

# Reglas

## REG-001

Ningún punto de extensión modifica el Aggregate Root.

---

## REG-002

Toda integración utiliza eventos o contratos.

---

## REG-003

Las invariantes permanecen exclusivamente dentro del
Aggregate.

---

## REG-004

Los adaptadores pertenecen a Infrastructure.

---

## REG-005

Las nuevas funcionalidades respetan el Principio
Open/Closed.

---

## REG-006

El dominio nunca depende de tecnologías específicas.

---

## REG-007

Las extensiones pueden añadirse sin recompilar otros
Bounded Contexts.

---

## REG-008

Las integraciones son opcionales y desacopladas.

---

## REG-009

Los consumidores externos nunca modifican directamente el
estado del Aggregate.

---

## REG-010

Todo nuevo módulo debe integrarse mediante contratos
estables definidos por el dominio.

---

# Diagrama Conceptual

```text
                     Organization Aggregate
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
      Domain Events   Repository Contract   Domain Policies
             │
             ▼
      Integration Events
             │
 ┌───────────┼─────────────┬─────────────┬─────────────┐
 ▼           ▼             ▼             ▼             ▼
FIWARE   Municipality   Analytics   Notifications   Blockchain
             │
             ▼
      Read Model Projections
             │
             ▼
 APIs · Mobile · Dashboard · BI · IA
```

---

# Definición de Éxito

El Aggregate **Organization** define puntos de extensión claros y estables que permiten incorporar nuevas capacidades —como Smart Cities, FIWARE, inteligencia artificial, analítica, blockchain, georreferenciación, nuevos canales de comunicación o futuros Bounded Contexts— sin modificar el núcleo del dominio. Esta arquitectura garantiza que AURA Core pueda evolucionar durante años preservando la estabilidad, la mantenibilidad y el desacoplamiento del modelo de negocio.