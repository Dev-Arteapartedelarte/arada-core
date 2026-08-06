# DOMAIN-003K — Membership Integration Events

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Membership Management

Aggregate:
Membership

Documentos relacionados:

- DOMAIN-003-Aggregate.md
- DOMAIN-003D-Domain-Events.md
- DOMAIN-003J-Consistency-Boundary.md
- DOMAIN-001K-Integration-Events.md
- DOMAIN-002K-Integration-Events.md
- CORE-005-Domain-Events.md

---

# Objetivo

Este documento define los **Integration Events** oficiales del
Aggregate **Membership**.

Un Integration Event representa un hecho de negocio que debe
ser compartido con otros Bounded Contexts o sistemas externos
sin exponer el modelo interno del dominio.

Los Integration Events son la única forma autorizada para que
el Aggregate Membership comunique cambios relevantes fuera de su
límite de consistencia.

---

# Principios

Todo Integration Event debe cumplir los siguientes principios:

- representar un hecho consumado;
- publicarse únicamente después del commit;
- ser inmutable;
- ser independiente de la infraestructura;
- desacoplar Aggregates y Bounded Contexts;
- mantener compatibilidad evolutiva.

---

# Diferencia entre Domain Event e Integration Event

```text
Command

↓

Aggregate

↓

Domain Event

↓

Commit

↓

Outbox

↓

Integration Event

↓

Message Broker

↓

Otros Contextos
```

Los Domain Events pertenecen exclusivamente al dominio.

Los Integration Events representan contratos públicos de
integración.

---

# Catálogo Oficial

| Integration Event | Descripción |
|-------------------|-------------|
| MembershipCreatedIntegrationEvent | Nueva Membership creada |
| MembershipRequestedIntegrationEvent | Solicitud enviada |
| MembershipApprovedIntegrationEvent | Solicitud aprobada |
| MembershipRejectedIntegrationEvent | Solicitud rechazada |
| MembershipActivatedIntegrationEvent | Membership activada |
| MembershipSuspendedIntegrationEvent | Membership suspendida |
| MembershipReactivatedIntegrationEvent | Membership reactivada |
| MembershipTerminatedIntegrationEvent | Membership finalizada |
| MembershipArchivedIntegrationEvent | Membership archivada |

---

# Estructura Base

Todo Integration Event debe contener conceptualmente:

```text
EventId

EventType

AggregateId

AggregateType

AggregateVersion

OccurredOn

CorrelationId

CausationId

Publisher

SchemaVersion

Payload
```

Los metadatos permiten trazabilidad y evolución del contrato.

---

# Payload Conceptual

El contenido mínimo esperado es:

```text
MembershipId

CitizenId

OrganizationId

Status

OccurredOn

Version
```

No deben incluirse objetos completos de otros Aggregates.

---

# Publicación

La publicación ocurre exclusivamente después de una
transacción exitosa.

Proceso conceptual:

```text
Execute Command

↓

Persist Aggregate

↓

Persist Domain Events

↓

Commit

↓

Outbox

↓

Integration Event

↓

Broker
```

Nunca se publican eventos antes del commit.

---

# Destinatarios

Los Integration Events pueden ser consumidos por:

- Identity Context;
- Role Management;
- Permission Management;
- Notification;
- Audit;
- Analytics;
- Reporting;
- Search;
- Workflow;
- Smart City Integration;
- API Gateway;
- Sistemas Municipales.

Todos permanecen desacoplados del Aggregate.

---

# Casos de Uso

## MembershipApprovedIntegrationEvent

Puede ser utilizado para:

- enviar notificaciones;
- generar auditoría;
- iniciar procesos administrativos;
- actualizar paneles de control.

---

## MembershipActivatedIntegrationEvent

Puede desencadenar:

```text
Asignación de Roles

↓

Creación de Permisos

↓

Actualización de estadísticas

↓

Habilitación de servicios

↓

Sincronización externa
```

---

## MembershipTerminatedIntegrationEvent

Puede provocar:

- revocación de permisos;
- desasignación de Roles;
- cierre de procesos pendientes;
- actualización de reportes.

---

# Integración con FIWARE

Cuando una Membership pasa a estado:

```text
Active
```

puede emitirse:

```text
MembershipActivatedIntegrationEvent
```

para sincronizar el ecosistema Smart City.

Ejemplo conceptual:

```text
MembershipActivatedIntegrationEvent

↓

Integration Service

↓

NGSI-LD Entity

↓

FIWARE Context Broker

↓

Municipal Digital Platform
```

El Aggregate nunca conoce FIWARE.

---

# Integración con la Municipalidad

Ejemplo:

```text
MembershipApprovedIntegrationEvent

↓

Municipal API

↓

Registro de participación

↓

Servicios Digitales
```

La integración se realiza mediante adaptadores externos.

---

# Compatibilidad con Microservicios

Los Integration Events permiten que distintos servicios
trabajen de forma independiente.

Ejemplo:

```text
Membership Service

↓

Kafka / RabbitMQ

↓

Notification Service

↓

Analytics Service

↓

Audit Service
```

No existe dependencia directa entre servicios.

---

# Versionado

Cada Integration Event posee:

```text
SchemaVersion
```

Ejemplo:

```text
1.0
```

La evolución del contrato debe preservar compatibilidad hacia
atrás siempre que sea posible.

---

# Idempotencia

Los consumidores deben ser capaces de procesar el mismo evento
más de una vez sin producir efectos inconsistentes.

La identificación se basa en:

```text
EventId
```

---

# Orden de Publicación

Para un mismo Aggregate:

```text
MembershipCreated

↓

MembershipRequested

↓

MembershipApproved

↓

MembershipActivated
```

debe mantenerse exactamente el mismo orden durante la
publicación de los Integration Events.

---

# Garantías

El sistema debe garantizar:

- publicación después del commit;
- entrega confiable;
- trazabilidad;
- reintentos controlados;
- ausencia de pérdidas.

Estas garantías se implementan mediante:

```text
Outbox Pattern
```

y la infraestructura de mensajería.

---

# Reglas de Evolución

Una vez publicado un Integration Event:

- no cambia su significado;
- no cambia su nombre;
- no se reutiliza;
- no rompe consumidores existentes.

Las nuevas capacidades requieren nuevos eventos o nuevas
versiones del contrato.

---

# Compatibilidad con CQRS

Los Integration Events pertenecen al flujo de sincronización
entre Contextos.

No modifican el estado del Aggregate.

Los Read Models pueden consumirlos para mantener proyecciones
distribuidas.

---

# Compatibilidad con Event Sourcing

Cuando Event Sourcing está habilitado:

```text
Domain Event

↓

Mapper

↓

Integration Event
```

Los Integration Events nunca reemplazan a los Domain Events.

Son representaciones externas derivadas del historial del
Aggregate.

---

# Seguridad

Los Integration Events nunca deben transportar:

- credenciales;
- secretos;
- tokens;
- información sensible innecesaria;
- referencias a objetos internos.

Únicamente deben contener información necesaria para la
integración.

---

# Principios Arquitectónicos

Este modelo sigue:

- Domain-Driven Design (DDD);
- Event-Driven Architecture (EDA);
- CQRS;
- Event Sourcing;
- Outbox Pattern;
- Publisher-Subscriber;
- Clean Architecture.

---

# Definición de Éxito

Los **Integration Events** del Aggregate **Membership**
constituyen el contrato oficial mediante el cual la evolución
de la relación entre un **Citizen** y una **Organization** se
propaga de manera segura, desacoplada y trazable hacia otros
Bounded Contexts y plataformas externas. Este modelo permite
que AURA se integre con servicios de identidad, gobernanza,
analítica, notificaciones y ecosistemas Smart City como FIWARE,
manteniendo la independencia del dominio y la consistencia de la
arquitectura basada en eventos.