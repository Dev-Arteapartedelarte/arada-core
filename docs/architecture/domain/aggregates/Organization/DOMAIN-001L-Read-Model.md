# DOMAIN-001L — Organization Read Model

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
- DOMAIN-001G-Repository-Contract.md
- DOMAIN-001I-Versioning.md
- DOMAIN-001J-Consistency-Boundary.md
- DOMAIN-001K-Integration-Events.md
- CORE-007-Strategic-Design.md

---

# Objetivo

Definir el modelo oficial de lectura (Read Model) del
Aggregate Organization.

El Read Model constituye una representación optimizada
para consultas y visualización de información, separada
del modelo de escritura del dominio.

Su propósito es ofrecer alto rendimiento, escalabilidad
y flexibilidad sin comprometer la integridad del
Aggregate.

---

# Motivación

El Aggregate Organization está diseñado para proteger las
reglas de negocio.

No está diseñado para responder consultas complejas.

Las necesidades de lectura son diferentes a las de
escritura.

Ejemplos.

- listado de organizaciones;
- búsqueda por nombre;
- organizaciones por territorio;
- organizaciones por estado;
- estadísticas;
- paneles municipales;
- dashboards ciudadanos.

Estas consultas no deben ejecutarse directamente sobre el
Aggregate.

---

# Principios

El Read Model debe cumplir los siguientes principios.

- solo lectura;
- optimizado para consultas;
- desacoplado del dominio;
- reconstruible;
- eventual consistente;
- independiente del Repository del Aggregate.

---

# Separación CQRS

```text
                 COMMAND SIDE

Command

↓

Aggregate

↓

Repository

↓

Domain Events

↓

Integration Events


                 QUERY SIDE

Read Repository

↓

Read Model

↓

Consultas
```

El modelo de escritura nunca depende del modelo de
lectura.

---

# Fuente de Verdad

La única fuente de verdad del sistema es el Aggregate.

El Read Model puede eliminarse completamente y
reconstruirse a partir de los eventos publicados.

---

# Construcción

El Read Model se actualiza mediante consumidores de
Integration Events.

```text
OrganizationCreated

↓

Projection

↓

OrganizationReadModel
```

No existe escritura directa sobre el Read Model desde el
Aggregate.

---

# Información Contenida

El Read Model puede incluir.

- OrganizationId;
- nombre;
- tipo;
- estado;
- representante;
- territorio;
- comuna;
- región;
- fecha de creación;
- fecha de aprobación;
- indicadores;
- número de integrantes;
- versión;
- última actualización.

Esta información puede desnormalizarse para acelerar las
consultas.

---

# Información Excluida

El Read Model no contiene.

- lógica de negocio;
- invariantes;
- validaciones;
- comportamiento;
- reglas de transición;
- servicios de dominio.

---

# Ejemplo Conceptual

```text
OrganizationReadModel

Id

Name

Type

Status

RepresentativeName

TerritoryName

Region

CreatedAt

ApprovedAt

Version
```

Este modelo existe únicamente para responder consultas.

---

# Flujo de Actualización

```text
Approve Organization

↓

OrganizationApproved

↓

Integration Event

↓

Projection

↓

Read Model
```

La actualización puede producirse algunos segundos
después del Commit.

---

# Consistencia

El Read Model utiliza consistencia eventual.

Durante un breve intervalo pueden coexistir.

```text
Aggregate

Version 8

↓

Read Model

Version 7
```

Esta situación es aceptable.

---

# Proyecciones

Cada consulta puede tener su propia proyección.

Ejemplos.

```text
OrganizationListProjection

OrganizationDetailsProjection

OrganizationStatisticsProjection

OrganizationDashboardProjection
```

Cada una responde a necesidades diferentes.

---

# Índices

El Read Model puede optimizar consultas mediante índices.

Ejemplos.

```text
OrganizationId

Status

TerritoryId

RepresentativeId

CreatedAt
```

La existencia de índices no modifica el dominio.

---

# Caché

El Read Model puede almacenarse en memoria.

```text
Projection

↓

Cache

↓

Client
```

La invalidación ocurre mediante nuevos eventos.

---

# Integración con APIs

Las APIs públicas consumen el Read Model.

```text
REST API

↓

Read Repository

↓

Read Model
```

Nunca consultan directamente el Aggregate para operaciones
de lectura generales.

---

# Integración con FIWARE

Los adaptadores FIWARE pueden construir vistas derivadas
a partir del Read Model.

```text
Projection

↓

NGSI-LD Projection

↓

Context Broker
```

El Aggregate permanece completamente aislado.

---

# Recuperación

En caso de pérdida.

```text
Eliminar Read Model

↓

Reprocesar Integration Events

↓

Reconstrucción completa
```

La recuperación no requiere modificar el dominio.

---

# Versionado

Cada registro del Read Model debe conservar.

```text
AggregateVersion
```

Esto permite detectar información desactualizada.

---

# Rendimiento

El Read Model puede utilizar.

- bases documentales;
- motores de búsqueda;
- índices geoespaciales;
- caché distribuida;
- almacenamiento especializado.

Estas decisiones pertenecen a infraestructura.

---

# Reglas

## REG-001

El Read Model nunca contiene lógica de negocio.

---

## REG-002

La única fuente de verdad es el Aggregate.

---

## REG-003

Toda actualización proviene de Integration Events.

---

## REG-004

El Read Model puede reconstruirse completamente.

---

## REG-005

La consistencia es eventual.

---

## REG-006

Las consultas nunca modifican el Aggregate.

---

## REG-007

El Aggregate nunca depende del Read Model.

---

## REG-008

Las proyecciones pertenecen a la capa de Application.

---

## REG-009

El Read Repository es independiente del Repository del
Aggregate.

---

## REG-010

Cada registro conserva la versión del Aggregate para
garantizar trazabilidad y sincronización.

---

# Diagrama Conceptual

```text
                    WRITE SIDE

Command
    │
    ▼
Organization Aggregate
    │
    ▼
Repository
    │
    ▼
Domain Events
    │
    ▼
Integration Events
    │
    ▼
Projection Engine
    │
    ▼
Organization Read Model
    │
    ▼
Read Repository
    │
    ▼
REST API / GraphQL / Dashboard / Mobile / Municipality
```

---

# Beneficios

El modelo propuesto proporciona:

- consultas de alta velocidad;
- desacoplamiento entre lectura y escritura;
- escalabilidad independiente;
- soporte natural para CQRS;
- integración sencilla con motores analíticos;
- reconstrucción completa mediante eventos;
- preparación para Data Lake y BI;
- compatibilidad con futuras proyecciones geoespaciales y Smart City.

---

# Definición de Éxito

El Aggregate `Organization` mantiene un modelo de lectura completamente independiente del modelo de escritura. Todas las consultas de la plataforma AURA Core son atendidas mediante proyecciones construidas a partir de Integration Events, garantizando consultas eficientes, consistencia eventual, escalabilidad horizontal y un dominio libre de responsabilidades de presentación o consulta.