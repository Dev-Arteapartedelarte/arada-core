# ============================================================
# ARADA
# ============================================================

# Proyecto

AURA Core

---

# Unidad

CORE-003

---

# Documento

Shared Kernel

---

# ADR relacionados

ADR-001
ADR-002
ADR-003 (pendiente)

---

# Objetivo

Definir el Shared Kernel oficial de la plataforma AURA.

El Shared Kernel representa el único espacio del dominio
que puede ser utilizado por múltiples Bounded Contexts
sin romper su independencia.

Su propósito es compartir únicamente conceptos estables,
inmutables y universales.

Nunca contendrá reglas de negocio específicas.

Nunca contendrá lógica de aplicación.

Nunca contendrá infraestructura.

---

# Principios

El Shared Kernel debe ser:

• pequeño

• estable

• altamente reutilizable

• independiente

• libre de dependencias externas

Todo cambio en este módulo requiere evaluación
arquitectónica.

---

# Contenido Permitido

Únicamente pueden existir los siguientes elementos.

---

## 1. Value Objects

Ejemplos

Identifier

Email

PhoneNumber

Address

GeoLocation

Coordinates

Money

DateRange

TimeRange

Slug

Url

Color

Language

Locale

Version

---

## 2. Enumeraciones Universales

Ejemplos

CountryCode

Currency

LanguageCode

WeekDay

PermissionScope

NotificationChannel

Priority

Severity

Status

Visibility

---

## 3. Errores de Dominio

Ejemplos

DomainError

ValidationError

InvariantViolation

BusinessRuleViolation

EntityNotFound

ConcurrencyViolation

---

## 4. Eventos Base

Todos los eventos del dominio
deben heredar del mismo contrato.

Ejemplo

DomainEvent

EventId

OccurredOn

AggregateId

CorrelationId

Version

---

## 5. Entidades Base

Sólo abstracciones.

Nunca entidades concretas.

Ejemplo

Entity

AggregateRoot

AuditableEntity

SoftDeleteEntity

---

## 6. Interfaces

Repository

Specification

UnitOfWork

Clock

IdGenerator

DomainService

EventPublisher

---

## 7. Result Pattern

Result<T>

Success

Failure

ValidationResult

Notification

---

## 8. Especificaciones

Specification

CompositeSpecification

AndSpecification

OrSpecification

NotSpecification

---

## 9. Objetos Matemáticos

Percentage

Distance

Area

Volume

Weight

Temperature

Duration

---

## 10. Objetos Geográficos

Coordinates

Polygon

BoundingBox

GeoPoint

GeoArea

---

## 11. Seguridad Base

UserId

RoleId

PermissionId

TenantId

CorrelationId

TraceId

SessionId

---

## 12. Contratos Compartidos

PagedResult

Pagination

Sort

Filter

SearchCriteria

AuditInfo

Metadata

---

# Contenido Prohibido

El Shared Kernel nunca contendrá:

Usuarios

Juntas de vecinos

Solicitudes

Participación

Workflow

Sensores

Municipios

Notificaciones

Organizaciones

Smart City

FIWARE

NGSI-LD

LoRaWAN

Open311

Blockchain

Estos pertenecen a sus respectivos
Bounded Contexts.

---

# Dependencias

Todos los Bounded Contexts pueden depender
del Shared Kernel.

El Shared Kernel no depende
de ningún contexto.

Representación:

                    Shared Kernel
                    /     |      \
                   /      |       \
                  /       |        \
          Identity Community Requests
                 \         |        /
                  \        |       /
                   \       |      /
                  Organization Workflow

Dependencia unidireccional.

Nunca inversa.

---

# Reglas Arquitectónicas

Una modificación del Shared Kernel
debe cumplir las siguientes condiciones.

1.

No romper compatibilidad.

2.

No introducir dependencias.

3.

No incorporar reglas de negocio.

4.

No conocer infraestructura.

5.

No depender de frameworks.

6.

Ser reutilizable por cualquier contexto.

7.

Ser estable en el tiempo.

---

# Organización Física

shared/

├── domain/
│
├── value_objects/
│
├── entities/
│
├── events/
│
├── repositories/
│
├── specifications/
│
├── errors/
│
├── contracts/
│
├── primitives/
│
├── enums/
│
├── result/
│
└── utils/

---

# Ejemplo Conceptual

Community

↓

NeighborhoodId

↓

Shared Kernel

↓

Identifier

Identity

↓

UserId

↓

Shared Kernel

↓

Identifier

Requests

↓

RequestId

↓

Shared Kernel

↓

Identifier

Cada contexto define su propio
modelo utilizando los mismos
primitivos compartidos.

---

# Beneficios

• Reduce duplicación.

• Mantiene coherencia.

• Favorece la reutilización.

• Minimiza acoplamiento.

• Facilita pruebas.

• Incrementa mantenibilidad.

• Permite evolución independiente
  de los Bounded Contexts.

---

# Estado

Versión

1.0

Estado

Aprobado

Proyecto

AURA Core

Autor

ARADA