# DOMAIN-003N — Membership Performance Rules

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
- DOMAIN-003G-Repository-Contract.md
- DOMAIN-003J-Consistency-Boundary.md
- DOMAIN-003K-Integration-Events.md
- DOMAIN-003L-Read-Model.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Este documento define las reglas oficiales de rendimiento
(**Performance Rules**) para el Aggregate **Membership**.

El objetivo es garantizar que el Aggregate mantenga tiempos de
respuesta predecibles y un comportamiento escalable,
independientemente del crecimiento del ecosistema AURA.

Las reglas aquí descritas son principios arquitectónicos del
dominio y no dependen de una tecnología específica.

---

# Principios

El Aggregate Membership debe cumplir los siguientes principios:

- tiempo de ejecución constante cuando sea posible;
- mínima cantidad de datos en memoria;
- una única transacción por Command;
- ausencia de consultas innecesarias;
- alta escalabilidad;
- comportamiento determinístico.

---

# Objetivos de Rendimiento

Las siguientes metas sirven como referencia para la
implementación:

| Operación | Objetivo |
|-----------|---------:|
| Cargar Membership | < 50 ms |
| Persistir Membership | < 100 ms |
| Validar invariantes | < 10 ms |
| Emitir Domain Events | < 5 ms |
| Commit transaccional | < 150 ms |
| Publicar Integration Events | Asíncrono |

Estos valores son objetivos arquitectónicos y podrán ajustarse
según la infraestructura utilizada.

---

# Regla 1 — Un Aggregate por Transacción

Cada Command debe modificar únicamente una instancia del
Aggregate Membership.

Ejemplo:

```text
✔ Correcto

ActivateMembership

↓

Membership
```

```text
✖ Incorrecto

Membership

↓

Organization

↓

Citizen
```

No deben existir transacciones distribuidas entre Aggregates.

---

# Regla 2 — Carga Mínima

El Repository debe recuperar únicamente el Aggregate necesario.

Correcto:

```text
Membership
```

Incorrecto:

```text
Membership

+

Citizen

+

Organization

+

Roles

+

Permissions
```

Los demás Aggregates se identifican exclusivamente mediante sus
identidades.

---

# Regla 3 — Validaciones Locales

Las invariantes deben verificarse utilizando únicamente la
información contenida en el Aggregate o mediante consultas de
dominio estrictamente necesarias.

Ejemplos:

```text
✔ Estado actual

✔ Version

✔ MembershipId

✔ CitizenId

✔ OrganizationId
```

Evitar consultas externas durante la ejecución de Commands.

---

# Regla 4 — Consultas Complejas

Las consultas que involucren:

- filtros múltiples;
- estadísticas;
- agregaciones;
- historiales;
- dashboards;
- búsquedas textuales;

deben resolverse mediante el **Read Model**.

Nunca deben ejecutarse desde el Aggregate.

---

# Regla 5 — Domain Events Livianos

Los Domain Events deben contener únicamente la información
necesaria para describir el hecho ocurrido.

Ejemplo:

```text
MembershipActivated

MembershipId

CitizenId

OrganizationId

OccurredOn

Version
```

No deben transportar objetos completos.

---

# Regla 6 — Integration Events Asíncronos

La publicación de Integration Events nunca forma parte del
tiempo de respuesta del Command.

Proceso:

```text
Command

↓

Commit

↓

Outbox

↓

Broker

↓

Consumers
```

El usuario recibe la respuesta antes de la publicación del
evento.

---

# Regla 7 — Optimistic Concurrency

El Aggregate utiliza control de concurrencia optimista.

No se permiten bloqueos pesimistas prolongados.

Proceso:

```text
Load

↓

Validate Version

↓

Save
```

---

# Regla 8 — Sin Consultas Cruzadas

Membership nunca consulta directamente:

- Role;
- Permission;
- Organization;
- Citizen;
- Assembly.

La comunicación ocurre mediante:

- Commands;
- Domain Events;
- Integration Events.

---

# Regla 9 — Tamaño del Aggregate

El Aggregate debe permanecer pequeño.

Debe contener únicamente:

```text
Identidad

Estado

Version

Fechas

Eventos pendientes
```

No debe crecer con información histórica, analítica o
documental.

---

# Regla 10 — Historial

El historial pertenece al flujo de eventos.

Nunca debe cargarse el historial completo para ejecutar un
Command.

Cuando se utilice Event Sourcing, podrán emplearse
**Snapshots** para acelerar la reconstrucción.

---

# Regla 11 — Proyecciones

Toda información destinada a:

- reportes;
- BI;
- indicadores;
- gráficos;
- dashboards;
- portales públicos;

debe generarse mediante proyecciones independientes.

---

# Regla 12 — Escalabilidad Horizontal

El Aggregate debe poder ejecutarse en múltiples instancias.

Para ello:

- no mantiene estado compartido;
- no utiliza memoria distribuida;
- no depende de sesiones;
- no conserva información temporal.

---

# Regla 13 — Reintentos

Los reintentos deben ser seguros.

Los Commands deben ser:

```text
Idempotentes

o

Detectar duplicados
```

cuando el caso de uso lo requiera.

---

# Regla 14 — Caché

El Aggregate no utiliza caché interno.

Si existe caché, ésta pertenece a:

- Read Models;
- API Gateway;
- infraestructura;
- consultas.

Nunca al modelo de escritura.

---

# Regla 15 — Rendimiento de Lectura

Las consultas frecuentes deben resolverse mediante índices
adecuados sobre el Read Model.

Índices recomendados:

```text
MembershipId

CitizenId

OrganizationId

Status

AdmissionDate

ActivationDate
```

---

# Regla 16 — Rendimiento de Escritura

La escritura debe minimizar:

- consultas redundantes;
- serialización innecesaria;
- bloqueos;
- operaciones distribuidas.

Cada Command debe producir un único Commit.

---

# Regla 17 — Escalabilidad mediante Eventos

El crecimiento del sistema no debe afectar el Aggregate.

Las nuevas funcionalidades deben consumir eventos ya
existentes.

Ejemplo:

```text
MembershipActivated

↓

Analytics

↓

Notification

↓

Audit

↓

FIWARE

↓

Workflow
```

El Aggregate permanece sin modificaciones.

---

# Regla 18 — Observabilidad

Toda operación relevante debe generar métricas.

Ejemplos:

```text
Execution Time

Repository Time

Commit Time

Concurrency Conflicts

Rejected Commands

Published Events
```

Estas métricas pertenecen a la infraestructura y no al dominio.

---

# Regla 19 — Objetivos de Escalabilidad

El diseño debe permitir:

- millones de Memberships;
- miles de organizaciones;
- procesamiento concurrente;
- múltiples instancias del servicio;
- integración con numerosos consumidores de eventos.

Sin modificar el modelo del dominio.

---

# Regla 20 — Degradación Controlada

La indisponibilidad de servicios externos no debe impedir la
ejecución del Aggregate.

Ejemplo:

```text
MembershipActivated

↓

Commit exitoso

↓

Broker caído

↓

Evento permanece en Outbox

↓

Reintento posterior
```

El dominio mantiene su consistencia.

---

# Indicadores Recomendados

Monitorear periódicamente:

- tiempo medio de ejecución de Commands;
- conflictos de concurrencia;
- tasa de Commands rechazados;
- tiempo de reconstrucción del Aggregate;
- tiempo de actualización del Read Model;
- latencia de publicación de Integration Events;
- tamaño promedio del Aggregate.

---

# Compatibilidad con CQRS

Las optimizaciones de lectura pertenecen al Read Model.

El Aggregate mantiene únicamente la lógica de negocio.

---

# Compatibilidad con Event Sourcing

Cuando se utilice Event Sourcing:

- snapshots aceleran la reconstrucción;
- los eventos permanecen inmutables;
- las proyecciones pueden regenerarse;
- el rendimiento evoluciona sin afectar el dominio.

---

# Principios Arquitectónicos

Este documento sigue:

- Domain-Driven Design (DDD);
- Clean Architecture;
- CQRS;
- Event Sourcing;
- Repository Pattern;
- Outbox Pattern;
- Optimistic Concurrency Control;
- Performance by Design.

---

# Definición de Éxito

Las reglas de rendimiento del Aggregate **Membership** garantizan
que la gestión de la relación entre un **Citizen** y una
**Organization** mantenga un comportamiento predecible,
escalable y eficiente. El Aggregate conserva un tamaño reducido,
opera mediante transacciones atómicas y delega las operaciones
de lectura, integración y análisis a componentes especializados,
permitiendo que AURA escale desde organizaciones locales hasta
ecosistemas Smart City de gran escala sin comprometer la
consistencia del dominio.