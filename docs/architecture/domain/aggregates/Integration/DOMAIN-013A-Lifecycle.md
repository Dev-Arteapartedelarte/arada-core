# DOMAIN-013A — Integration Lifecycle

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Integration Management

Aggregate:
Integration

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-013-Aggregate.md
- DOMAIN-013B-State-Machine.md
- DOMAIN-013C-Commands.md
- DOMAIN-013D-Domain-Events.md
- DOMAIN-013E-Invariants.md
- DOMAIN-013F-Permissions.md
- DOMAIN-013G-Repository-Contract.md
- DOMAIN-013H-Examples.md
- DOMAIN-013I-Versioning.md
- DOMAIN-013J-Consistency-Boundary.md
- DOMAIN-013K-Integration-Events.md
- DOMAIN-013L-Read-Model.md
- DOMAIN-013M-Test-Scenarios.md
- DOMAIN-013N-Performance-Rules.md
- DOMAIN-013O-Security-Model.md
- DOMAIN-013P-Extension-Points.md

---

# Objetivo

Este documento define formalmente el **Lifecycle** conceptual del
Aggregate **Integration**.

El Lifecycle representa la evolución de una relación formal de
interoperabilidad administrada por AURA.

Su propósito es distinguir claramente entre:

- definición de una Integration;
- habilitación formal de la relación de interoperabilidad;
- suspensión formal de dicha relación;
- retiro de la Integration del ciclo operativo.

El Lifecycle pertenece exclusivamente al Aggregate Integration.

---

# Principio Fundamental

Debe mantenerse:

```text
Integration Lifecycle

≠

Technical Connection Lifecycle
```

El estado de una Integration representa una condición del dominio.

No representa directamente:

- disponibilidad de red;
- conexión TCP;
- sesión HTTP;
- conexión a broker;
- disponibilidad de endpoint;
- estado de un worker;
- estado de una queue;
- estado de un adapter;
- estado de FIWARE;
- estado de un sistema municipal.

---

# Lifecycle Oficial

La versión 1.0 define los siguientes estados conceptuales:

```text
Draft

Active

Suspended

Archived
```

Estos estados pertenecen al Lifecycle de Integration.

No deben confundirse con estados técnicos de Infrastructure.

---

# Flujo Principal

Conceptualmente:

```text
No Integration
      │
      ▼
    Draft
      │
      ▼
    Active
      │
      ▼
  Suspended
      │
      └──────────────► Active
```

El retiro del ciclo operativo puede producirse mediante:

```text
Draft ───────────────► Archived

Active ──────────────► Archived

Suspended ───────────► Archived
```

---

# No Integration

`No Integration` representa la inexistencia del Aggregate.

No constituye un estado persistido.

Debe mantenerse:

```text
No Integration

≠

Integration State
```

Antes de la creación no existe:

- IntegrationId persistido;
- Version persistida;
- estado persistido;
- Lifecycle interno.

---

# Draft

`Draft` representa una Integration creada formalmente pero que todavía
no se encuentra habilitada para participar como relación operativa de
interoperabilidad.

En Draft:

- la Integration posee identidad;
- la Integration pertenece al dominio;
- puede completar o modificar la información permitida por sus reglas;
- todavía no representa una relación activa;
- debe respetar sus Invariants;
- posee Version;
- conserva trazabilidad.

Debe mantenerse:

```text
Draft

≠

Active Integration
```

---

# Active

`Active` representa una Integration formalmente habilitada para
participar en interoperabilidad conforme a sus contratos de dominio.

Debe mantenerse:

```text
Active

=

Domain Authorization to Participate as an Integration
```

Esto no significa:

```text
Network Connected

Endpoint Available

Broker Connected

External System Online
```

---

# Active no Representa Conectividad

Una Integration puede permanecer:

```text
Active
```

aunque exista temporalmente:

- un timeout;
- una caída de red;
- indisponibilidad del sistema externo;
- indisponibilidad de FIWARE;
- error del broker;
- error de transporte;
- retry técnico.

Estos hechos técnicos no modifican por sí mismos el Lifecycle.

---

# Suspended

`Suspended` representa una Integration cuya participación operativa en
interoperabilidad ha sido suspendida formalmente por una decisión
válida del dominio.

La identidad continúa existiendo.

La suspensión conserva:

- IntegrationId;
- Version;
- historial;
- trazabilidad;
- referencias formales;
- contratos conceptuales asociados.

Debe mantenerse:

```text
Suspended

≠

Deleted
```

y:

```text
Suspended

≠

Technical Disconnected
```

---

# Reactivación

Una Integration Suspended puede regresar a:

```text
Active
```

mediante una transición explícita válida.

Conceptualmente:

```text
Suspended
    │
    ▼
  Active
```

La reactivación:

- debe respetar Permissions;
- debe respetar Invariants;
- debe respetar Versioning;
- debe producir el hecho de dominio correspondiente cuando sea
  definido;
- no puede realizarse mediante modificación directa del estado.

---

# Archived

`Archived` representa una Integration retirada formalmente del ciclo
operativo.

Una Integration Archived:

- conserva IntegrationId;
- conserva su significado histórico;
- conserva trazabilidad;
- conserva Version;
- no participa nuevamente del flujo operativo ordinario;
- no se reactiva mediante operaciones ordinarias.

Debe mantenerse:

```text
Archived

≠

Deleted
```

---

# Archived es Terminal

`Archived` es un estado terminal en versión 1.0.

No existen transiciones oficiales desde:

```text
Archived
```

hacia:

```text
Draft

Active

Suspended
```

---

# Creación

La creación válida establece:

```text
No Integration
    │
    ▼
   Draft
```

Una nueva Integration comienza en:

```text
Draft
```

---

# Creación Atómica

La transición:

```text
No Integration → Draft
```

debe establecer coherentemente:

- IntegrationId;
- estado Draft;
- Version inicial conforme al contrato de Versioning;
- CreatedAt;
- información mínima requerida por las Invariants;
- Domain Event correspondiente cuando sea formalmente definido.

No debe existir una Integration parcialmente creada.

---

# Draft hacia Active

La transición:

```text
Draft → Active
```

representa la habilitación formal de una Integration.

Solamente puede ocurrir cuando la Integration cumple las condiciones
de dominio requeridas.

---

# Activación

Activar una Integration no equivale a:

- abrir una conexión;
- crear un socket;
- establecer una sesión;
- autenticar contra un proveedor;
- validar un endpoint;
- conectar un broker;
- iniciar un worker.

Debe mantenerse:

```text
Activate Integration

≠

Connect Infrastructure
```

---

# Active hacia Suspended

La transición:

```text
Active → Suspended
```

representa una suspensión formal del dominio.

No debe ejecutarse automáticamente por un error técnico.

---

# Suspensión Formal

Debe mantenerse:

```text
Domain Suspension

≠

Infrastructure Failure
```

Un fallo de transporte no constituye por sí mismo una transición
válida hacia Suspended.

---

# Suspended hacia Active

La transición:

```text
Suspended → Active
```

representa una reactivación formal.

La disponibilidad técnica de un sistema externo no reactiva
automáticamente la Integration.

---

# Draft hacia Archived

Una Integration en Draft puede retirarse formalmente antes de ser
activada:

```text
Draft → Archived
```

Esta transición conserva la existencia histórica de la Integration.

---

# Active hacia Archived

Una Integration Active puede retirarse formalmente:

```text
Active → Archived
```

El archivado representa la finalización de su participación
operativa.

---

# Suspended hacia Archived

Una Integration Suspended puede retirarse definitivamente del ciclo
operativo:

```text
Suspended → Archived
```

---

# Transiciones Oficiales

La versión 1.0 establece conceptualmente:

```text
No Integration → Draft

Draft          → Active

Draft          → Archived

Active         → Suspended

Active         → Archived

Suspended      → Active

Suspended      → Archived
```

La formalización completa de Guards y validez pertenece a:

```text
DOMAIN-013B-State-Machine.md
```

---

# Transiciones no Permitidas

No se permiten en versión 1.0:

```text
Active → Draft

Suspended → Draft

Archived → Draft

Archived → Active

Archived → Suspended
```

Tampoco se permite alterar el estado mediante setters públicos.

---

# No Transición Implícita

Debe mantenerse:

```text
Technical Condition

≠

Automatic Lifecycle Transition
```

Todo cambio de estado requiere una intención de dominio válida.

---

# Estado versus Technical Health

Debe mantenerse:

```text
Lifecycle State

≠

Technical Health
```

Por ejemplo:

```text
Integration = Active

External System = Unavailable
```

es una condición conceptualmente posible.

También:

```text
Integration = Suspended

External System = Available
```

es conceptualmente posible.

---

# Estados Técnicos Excluidos

No forman parte del Lifecycle oficial:

```text
Connected

Disconnected

Connecting

Reconnecting

Retrying

Queued

Processing

Published

DeliveryFailed

Timeout

DeadLettered

Healthy

Unhealthy

Degraded
```

---

# Failed no es Estado de Integration

La versión 1.0 no define:

```text
Failed
```

como estado del Lifecycle.

Debe mantenerse:

```text
Infrastructure Failure

≠

Integration = Failed
```

---

# Pending no es Estado de Integration

La versión 1.0 no define:

```text
Pending
```

como estado del Aggregate.

Un mensaje pendiente, una publicación pendiente o una operación
pendiente pertenecen a otra responsabilidad.

---

# Connected no es Estado de Integration

La versión 1.0 no define:

```text
Connected
```

como estado.

Una Integration Active puede utilizar tecnologías que ni siquiera
mantengan una conexión persistente.

---

# Disconnected no es Estado de Integration

La versión 1.0 no define:

```text
Disconnected
```

como estado del dominio.

---

# Deleted no es Estado de Integration

La versión 1.0 no define:

```text
Deleted
```

como estado.

La finalización formal del Lifecycle se representa mediante:

```text
Archived
```

---

# Cancelled no es Estado de Integration

La versión 1.0 no define:

```text
Cancelled
```

como estado.

Una Integration que deja de participar operativamente se representa
mediante las transiciones formalmente definidas hacia Archived o
Suspended según corresponda.

---

# Estado Inicial

Toda Integration persistida comienza en:

```text
Draft
```

No se permite crear directamente una Integration en:

```text
Active

Suspended

Archived
```

---

# Estado Terminal

La versión 1.0 establece:

```text
Archived
```

como único estado terminal.

---

# Estado Reversible

La relación:

```text
Active ↔ Suspended
```

constituye la única reversibilidad oficial del Lifecycle.

Esta reversibilidad no permite regresar a Draft.

---

# Draft no se Recupera

Después de abandonar Draft mediante:

```text
Draft → Active
```

no existe transición de regreso a Draft.

Draft representa exclusivamente la etapa inicial de definición de la
Integration.

---

# Archivado no se Revierte

Debe mantenerse:

```text
Archived

=

Terminal Lifecycle State
```

Una nueva necesidad de interoperabilidad posterior no debe
reinterpretar arbitrariamente una Integration Archived.

Si el dominio requiere una nueva Integration independiente, deberá
poseer su propia identidad conforme a las reglas aplicables.

---

# Identidad durante el Lifecycle

IntegrationId permanece constante durante:

```text
Draft

Active

Suspended

Archived
```

Debe mantenerse:

```text
State Change

≠

Identity Change
```

---

# Version durante el Lifecycle

Toda modificación válida debe mantener la evolución de:

```text
Version
```

según:

```text
DOMAIN-013I-Versioning.md
```

Una transición aceptada representa una modificación válida del
Aggregate.

---

# Rechazo y Version

Una transición rechazada:

- no cambia estado;
- no incrementa Version;
- no modifica UpdatedAt;
- no produce un Domain Event de éxito.

---

# CreatedAt

CreatedAt se establece durante:

```text
No Integration → Draft
```

y permanece inmutable durante todo el Lifecycle.

---

# UpdatedAt

Una transición válida actualiza UpdatedAt conforme a las reglas del
Aggregate.

Una lectura o una transición rechazada no debe modificarlo.

---

# Domain Events y Lifecycle

Cada transición válida debe poder expresarse mediante un hecho de
dominio cuando el correspondiente Domain Event sea definido en:

```text
DOMAIN-013D-Domain-Events.md
```

Este documento define estados y transiciones.

No establece por sí mismo los nombres definitivos de los Domain
Events.

---

# Commands y Lifecycle

Los Commands que provoquen transiciones se definen exclusivamente en:

```text
DOMAIN-013C-Commands.md
```

Debe mantenerse:

```text
Lifecycle Transition

requires

Valid Domain Behavior
```

---

# Permissions y Lifecycle

Una transición puede requerir Permission.

Sin embargo:

```text
Authorized

≠

Transition Automatically Valid
```

La operación debe además respetar:

- estado actual;
- Guards;
- Invariants;
- Versioning.

---

# Invariants y Lifecycle

Ninguna transición puede producir un Aggregate que viole:

```text
DOMAIN-013E-Invariants.md
```

---

# State Machine

Este documento establece la semántica general del Lifecycle.

La máquina formal de estados se define en:

```text
DOMAIN-013B-State-Machine.md
```

La State Machine determina exactamente:

- estados de origen;
- estados de destino;
- transiciones permitidas;
- transiciones rechazadas;
- Guards.

---

# Consistency Boundary

Toda transición afecta exclusivamente:

```text
Integration
```

dentro de su propio Consistency Boundary.

No modifica atómicamente:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Participation

Voting

Document

Notification

Audit

External System
```

---

# Source Aggregate Lifecycle

El Lifecycle de otro Aggregate no se transfiere a Integration.

Debe mantenerse:

```text
Source Aggregate State

≠

Integration State
```

---

# External System Lifecycle

El estado operativo de un sistema externo tampoco determina el
Lifecycle de Integration.

Debe mantenerse:

```text
External System State

≠

Integration State
```

---

# FIWARE y Lifecycle

Estados técnicos o conceptuales presentes en FIWARE no se incorporan
automáticamente a Integration.

Debe mantenerse:

```text
FIWARE State

≠

Integration Lifecycle State
```

---

# Context Broker y Lifecycle

La disponibilidad de un Context Broker no cambia automáticamente:

```text
Draft

Active

Suspended

Archived
```

---

# Sistemas Municipales y Lifecycle

Un sistema municipal puede encontrarse disponible o no disponible sin
que esto produzca automáticamente una transición de Integration.

---

# Error de Transporte

Ejemplo:

```text
Integration = Active

HTTP Request = Timeout
```

Resultado conceptual:

```text
Integration remains Active
```

El timeout no constituye una transición del Lifecycle.

---

# Error de Broker

Ejemplo:

```text
Integration = Active

Broker = Unavailable
```

La Integration no se convierte automáticamente en Suspended.

---

# Error de FIWARE

Ejemplo:

```text
Integration = Active

Context Broker = Unavailable
```

El estado del Aggregate continúa determinado por sus reglas de
dominio.

---

# Retry Técnico

Un retry técnico:

```text
Active
    │
    ▼
Active
```

no constituye una transición de Lifecycle.

No modifica Version por el solo hecho de reintentar transporte.

---

# Health Check

Un Health Check no constituye una transición.

Debe mantenerse:

```text
Health Check Result

≠

Lifecycle Command
```

---

# Monitoring

Monitoring puede observar:

- disponibilidad;
- latencia;
- errores;
- retries;
- throughput;

sin modificar el Lifecycle.

---

# Active y Procesamiento de Contratos

Una Integration Active puede participar en los contratos de
interoperabilidad que el dominio haya definido.

El mecanismo técnico utilizado para materializar esa participación
permanece fuera del Aggregate.

---

# Suspended y Procesamiento de Contratos

Una Integration Suspended no debe participar como relación operativa
habilitada mientras permanezca en dicho estado.

Esto representa una regla del dominio.

No implica modificar o destruir:

- contratos históricos;
- Domain Events previos;
- Integration Events previos;
- Read Models históricos.

---

# Archived y Procesamiento de Contratos

Una Integration Archived ha finalizado su participación operativa.

No debe reactivarse mediante procesamiento técnico o recepción de un
mensaje externo.

---

# Entrada Externa no Cambia Lifecycle Directamente

Debe mantenerse:

```text
External Message

≠

Direct Lifecycle Transition
```

Una entrada externa debe atravesar los contratos y comportamiento
definidos por AURA antes de poder provocar una modificación válida.

---

# Integration Event no Cambia Estado Directamente

Recibir un Integration Event no concede autoridad para:

```text
setState()
```

sobre Integration.

---

# Domain Event Externo no Cambia Estado Directamente

El Aggregate tampoco debe modificar su Lifecycle directamente por
observar un Domain Event de otro Aggregate.

Toda modificación debe ejecutarse mediante comportamiento propio.

---

# Estado y Contratos

El estado de Integration no debe confundirse con la versión o estado
de un Integration Contract.

Debe mantenerse:

```text
Integration Lifecycle

≠

Integration Contract Lifecycle
```

salvo que una relación específica sea definida formalmente en una
evolución futura.

---

# Estado y Contract Version

Debe mantenerse:

```text
Integration State

≠

Contract Version
```

Una nueva versión contractual no cambia automáticamente el estado del
Aggregate.

---

# Estado y API Version

Una API puede evolucionar sin producir automáticamente:

```text
Draft → Active

Active → Suspended

Active → Archived
```

---

# Estado y Deployment

Un deployment no constituye una transición.

Debe mantenerse:

```text
Deployment

≠

Integration Lifecycle Event
```

---

# Estado y Configuration

Cambios técnicos de configuración no son transiciones de Lifecycle
por definición.

Si una futura configuración posee significado real de dominio deberá
definirse explícitamente.

---

# Estado y Credenciales

La expiración de:

- AccessToken;
- certificate;
- API key;
- secret;

no constituye por sí misma una transición del Lifecycle.

Las credenciales permanecen fuera del Aggregate.

---

# Estado y Security

Un fallo de Authentication o Authorization técnico no modifica
automáticamente el estado de Integration.

Debe mantenerse:

```text
Authentication Failure

≠

Suspended
```

y:

```text
Authorization Failure

≠

Archived
```

---

# Suspensión no es Error

Suspended representa una decisión formal del dominio.

No representa:

```text
Error
```

ni:

```text
Failure
```

---

# Archivado no es Error

Archived representa finalización operativa formal.

No representa fallo técnico.

---

# Draft no es Error

Draft representa una etapa válida de definición.

No representa una Integration incompleta técnicamente ni una
operación fallida.

---

# Active no Garantiza Éxito Técnico

Debe mantenerse:

```text
Active

≠

Every Technical Operation Succeeds
```

El estado Active solamente expresa habilitación formal de dominio.

---

# Integración con Audit

Las transiciones válidas pueden generar hechos relevantes para Audit.

Sin embargo:

```text
Audit

∉

Integration Lifecycle
```

y un fallo de Audit no revierte automáticamente una transición
confirmada de Integration.

---

# Integración con Notification

Una transición puede originar posteriormente una necesidad de
comunicación.

Notification permanece fuera del Aggregate.

Debe mantenerse:

```text
Integration State Transition

≠

Notification Delivery
```

---

# Integración con Read Models

Los Read Models pueden proyectar:

```text
Draft

Active

Suspended

Archived
```

pero no poseen autoridad para ejecutar transiciones.

---

# Read Model Lag

Puede existir:

```text
Integration = Active

Read Model = Draft
```

temporalmente bajo consistencia eventual.

Esto no significa que existan dos estados autoritativos.

El Write Model continúa siendo autoridad del Lifecycle.

---

# Integration Events y Lifecycle

Un hecho de transición puede originar posteriormente un Integration
Event cuando exista un contrato explícito.

Debe mantenerse:

```text
Lifecycle Domain Event

≠

Mandatory Integration Event
```

---

# Fallo de Publicación

Si una publicación externa falla después de una transición confirmada:

```text
Integration State

remains

Confirmed Domain State
```

La publicación no revierte automáticamente el Aggregate.

---

# Consistencia Eventual

Puede existir una ventana temporal donde:

```text
Integration State Changed

+

External Consumer Not Yet Updated
```

Esto es coherente con la separación de Consistency Boundaries.

---

# Repository

El Repository debe preservar el estado confirmado de Integration.

No decide:

- transiciones;
- Guards;
- Lifecycle;
- Permissions;
- Invariants.

---

# Repository no Cambia Estado

Debe mantenerse:

```text
Repository

≠

Lifecycle Authority
```

Persistir no equivale a activar, suspender o archivar.

---

# Rehidratación

Al rehidratar una Integration debe recuperarse exactamente su estado
persistido válido.

Rehydration no constituye una transición.

---

# Event Sourcing

El Lifecycle es compatible con Event Sourcing.

Si dicha estrategia fuese utilizada, la rehidratación debe producir
el mismo estado que la evolución histórica confirmada.

Event Sourcing no es obligatorio.

---

# Replay

Replay no debe provocar:

- nuevas transiciones;
- nuevo Version increment;
- nuevos Domain Events;
- nuevas publicaciones externas.

Debe reconstruir el estado existente.

---

# CQRS

En CQRS:

```text
Command Side

owns

Lifecycle Transitions
```

mientras:

```text
Query Side

projects

Lifecycle State
```

---

# Performance

Evaluar una transición no debe requerir cargar:

- todos los Integration Aggregates;
- sistemas externos completos;
- históricos globales;
- Read Models;
- infraestructura de transporte.

---

# Security

Ningún privilegio permite:

- cambiar estado directamente;
- reactivar Archived;
- evitar Guards;
- evitar Invariants;
- evitar Versioning.

---

# Eliminación Física

La eliminación física no forma parte del Lifecycle versión 1.0.

Debe mantenerse:

```text
Archived

≠

Physically Deleted
```

Este documento no define política de retención o eliminación física.

---

# Retención

La existencia de Archived no define:

- período de retención;
- expiración;
- purga;
- eliminación automática.

Estas reglas no deben inferirse.

---

# Archivado y Trazabilidad

Una Integration Archived conserva su significado histórico.

Las relaciones y hechos ocurridos antes del archivado no se
reinterpretan.

---

# Evolución Futura

Nuevos estados solamente podrán incorporarse mediante definición
explícita.

Una futura evolución deberá revisar de forma coordinada:

```text
DOMAIN-013A-Lifecycle.md

DOMAIN-013B-State-Machine.md

DOMAIN-013C-Commands.md

DOMAIN-013D-Domain-Events.md

DOMAIN-013E-Invariants.md

DOMAIN-013F-Permissions.md

DOMAIN-013I-Versioning.md

DOMAIN-013J-Consistency-Boundary.md

DOMAIN-013M-Test-Scenarios.md
```

---

# Nuevos Estados

No debe introducirse un nuevo estado solamente porque exista un
concepto equivalente en:

- un proveedor;
- FIWARE;
- un broker;
- una API;
- un sistema municipal;
- una librería;
- un framework.

---

# Nuevas Transiciones

Toda nueva transición deberá poseer:

- significado de dominio;
- estado de origen;
- estado de destino;
- Command correspondiente cuando aplique;
- Guards;
- Invariants;
- Permission;
- Versioning;
- Domain Event cuando corresponda;
- Test Scenarios.

---

# Regla de No Inferencia

Debe mantenerse:

```text
Infrastructure State

≠

Permission to Extend Lifecycle
```

y:

```text
External Model State

≠

AURA Integration State
```

---

# Matriz Conceptual del Lifecycle

```text
State       Operational Domain Meaning

Draft       Integration formally defined but not active

Active      Integration formally enabled for interoperability

Suspended   Integration formally suspended from operational participation

Archived    Integration formally removed from the operational lifecycle
```

---

# Matriz de Transiciones

```text
From             To            Allowed

No Integration   Draft         Yes

Draft            Active        Yes

Draft            Archived      Yes

Active           Suspended     Yes

Active           Archived      Yes

Suspended        Active        Yes

Suspended        Archived      Yes

Active           Draft         No

Suspended        Draft         No

Archived         Draft         No

Archived         Active        No

Archived         Suspended     No
```

---

# Reglas Fundamentales

El Lifecycle de Integration debe cumplir:

1. No Integration representa inexistencia y no es un estado
   persistido.
2. Toda nueva Integration comienza en Draft.
3. Draft representa una Integration formalmente creada pero todavía
   no activa.
4. Active representa habilitación formal de interoperabilidad.
5. Active no representa conectividad técnica.
6. Suspended representa suspensión formal de dominio.
7. Suspended no representa error técnico.
8. Archived representa retiro formal del ciclo operativo.
9. Archived es terminal.
10. Archived no equivale a Deleted.
11. La transición inicial oficial es No Integration → Draft.
12. Draft puede transicionar a Active.
13. Draft puede transicionar a Archived.
14. Active puede transicionar a Suspended.
15. Active puede transicionar a Archived.
16. Suspended puede transicionar a Active.
17. Suspended puede transicionar a Archived.
18. Active no puede volver a Draft.
19. Suspended no puede volver a Draft.
20. Archived no puede regresar a ningún estado operativo.
21. IntegrationId permanece inmutable durante todo el Lifecycle.
22. Toda transición válida respeta Versioning.
23. Toda transición válida actualiza UpdatedAt conforme a las reglas
    del Aggregate.
24. Una transición rechazada no modifica estado.
25. Una transición rechazada no incrementa Version.
26. Una transición rechazada no produce un Domain Event de éxito.
27. No existe estado Failed en versión 1.0.
28. No existe estado Pending en versión 1.0.
29. No existe estado Connected en versión 1.0.
30. No existe estado Disconnected en versión 1.0.
31. No existe estado Deleted en versión 1.0.
32. No existe estado Cancelled en versión 1.0.
33. Estados técnicos de queue no son estados del Aggregate.
34. Estados técnicos de broker no son estados del Aggregate.
35. Estados técnicos de red no son estados del Aggregate.
36. Technical Health no determina Lifecycle.
37. Un timeout no produce una transición.
38. Un error HTTP no produce una transición.
39. Un error de broker no produce una transición.
40. Un error de FIWARE no produce una transición.
41. Un retry técnico no produce una transición.
42. Un Health Check no produce una transición.
43. La expiración de una credencial no produce una transición por sí
    misma.
44. Un External Message no cambia estado directamente.
45. Un Integration Event externo no cambia estado directamente.
46. Un Domain Event de otro Aggregate no cambia estado directamente.
47. Una transición afecta solamente el Aggregate Integration.
48. Source Aggregate State no determina Integration State.
49. External System State no determina Integration State.
50. FIWARE State no determina Integration State.
51. Municipal System State no determina Integration State.
52. Integration Lifecycle no equivale a Integration Contract
    Lifecycle.
53. Contract Version no determina estado.
54. API Version no determina estado.
55. Deployment no constituye transición.
56. Configuration técnica no constituye transición automáticamente.
57. Authentication Failure no produce Suspended automáticamente.
58. Authorization Failure no produce Archived automáticamente.
59. Read Models proyectan estado pero no lo controlan.
60. Projection Lag no modifica el estado autoritativo.
61. Integration Events no son obligatorios para toda transición.
62. Publication Failure no revierte automáticamente una transición
    confirmada.
63. El Repository no decide Lifecycle.
64. Rehydration no constituye transición.
65. Replay no constituye transición.
66. Event Sourcing permanece compatible pero no obligatorio.
67. Command Side controla transiciones.
68. Query Side solamente proyecta estado.
69. La eliminación física no forma parte del Lifecycle.
70. Archived no define una política de retención.
71. Nuevos estados requieren definición explícita.
72. Nuevas transiciones requieren definición explícita.
73. Ningún estado externo se incorpora automáticamente.
74. Ninguna condición técnica extiende el Lifecycle.
75. Toda evolución debe preservar el significado histórico.

---

# Restricciones

No está permitido:

- crear una Integration directamente en Active;
- crear una Integration directamente en Suspended;
- crear una Integration directamente en Archived;
- volver de Active a Draft;
- volver de Suspended a Draft;
- reactivar una Integration Archived;
- modificar estado mediante setter público;
- utilizar Connected como estado de dominio;
- utilizar Disconnected como estado de dominio;
- utilizar Failed como estado de dominio;
- utilizar Pending como estado de dominio;
- utilizar Deleted como estado de dominio;
- utilizar Cancelled como estado de dominio;
- suspender automáticamente por timeout;
- suspender automáticamente por error HTTP;
- suspender automáticamente por caída de broker;
- suspender automáticamente por caída de FIWARE;
- suspender automáticamente por indisponibilidad municipal;
- reactivar automáticamente porque un sistema externo vuelve a estar
  disponible;
- cambiar estado por recepción directa de un mensaje;
- cambiar estado desde Read Model;
- cambiar estado desde Repository;
- cambiar estado desde Infrastructure;
- utilizar estado externo como estado interno;
- utilizar Contract Version como Lifecycle State;
- utilizar API Version como Lifecycle State;
- utilizar retry técnico como transición;
- utilizar deployment como transición;
- interpretar Archived como eliminación física;
- inferir una política de retención desde Archived;
- introducir un nuevo estado sin definición formal;
- introducir una nueva transición sin actualizar State Machine,
  Commands, Invariants, Permissions y Test Scenarios cuando
  corresponda.

---

# Compatibilidad Arquitectónica

El Lifecycle de Integration es compatible con:

- Domain-Driven Design;
- Aggregate Pattern;
- State Machine Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- consistencia eventual;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no imponen ninguna tecnología concreta.

---

# Definición de Éxito

El Lifecycle del Aggregate **Integration** representa de forma clara
la evolución de una relación formal de interoperabilidad sin
confundir dominio con conectividad técnica.

El flujo oficial versión 1.0 queda definido como:

```text
No Integration
      │
      ▼
    Draft
      │
      ▼
    Active
      │
      ▼
  Suspended
      │
      └──────────────► Active
```

junto con las rutas de retiro:

```text
Draft ───────────────► Archived

Active ──────────────► Archived

Suspended ───────────► Archived
```

El modelo garantiza que:

- toda Integration comienza en Draft;
- Active expresa habilitación formal;
- Suspended expresa suspensión formal;
- Archived expresa retiro definitivo del ciclo operativo;
- Archived es terminal;
- Active y Suspended pueden alternarse únicamente mediante
  comportamiento válido;
- Draft no puede recuperarse después de activación;
- Archived no puede reactivarse;
- IntegrationId permanece inmutable;
- Version evoluciona solamente ante modificaciones válidas;
- fallos técnicos no se convierten en estados de dominio;
- conectividad no se confunde con Lifecycle;
- FIWARE no determina el estado;
- sistemas municipales no determinan el estado;
- brokers, endpoints y redes no determinan el estado;
- Read Models no controlan transiciones;
- Repository no controla transiciones;
- Infrastructure no controla transiciones;
- External Events no modifican directamente el Aggregate;
- cada transición permanece dentro del Consistency Boundary de
  Integration;
- consistencia externa permanece eventual;
- eliminación física y retención no se infieren desde el Lifecycle;
- cualquier evolución futura requiere definición explícita.

De esta forma, `DOMAIN-013A-Lifecycle.md` establece formalmente el
Lifecycle oficial del Aggregate **Integration** conforme al patrón
consolidado de AURA Core.