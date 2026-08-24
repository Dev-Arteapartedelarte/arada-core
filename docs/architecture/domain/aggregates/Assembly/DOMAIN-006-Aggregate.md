# DOMAIN-006 — Assembly Aggregate

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Assembly Management

Aggregate:
Assembly

Autor:
ARADA

Documentos Relacionados:

- CORE-002-Bounded-Context-Map.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-006-Domain-Invariants.md
- CORE-007-Strategic-Design.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md
- DOMAIN-001-Aggregate.md
- DOMAIN-002-Aggregate.md
- DOMAIN-003-Aggregate.md
- DOMAIN-004-Aggregate.md
- DOMAIN-005-Aggregate.md

---

# Objetivo

El Aggregate **Assembly** representa una instancia formal de
reunión, deliberación y participación colectiva dentro del
ecosistema AURA.

Constituye el espacio organizacional en el cual los integrantes
de una Organization pueden reunirse, conocer materias,
deliberar, registrar decisiones y desarrollar procesos formales
de participación.

Assembly conecta la estructura organizacional con los procesos
de participación y gobernanza de AURA, manteniendo la
consistencia de la reunión como una unidad de dominio.

Assembly permite representar la existencia formal de una
reunión independientemente de los procesos posteriores que
puedan desarrollarse dentro de ella.

No reemplaza ni absorbe otros Aggregates del dominio.

Cada proceso que posea identidad, ciclo de vida o reglas de
consistencia propias permanece bajo la responsabilidad de su
respectivo Aggregate.

---

# Propósito

El propósito del Aggregate Assembly es proporcionar una
representación consistente de una instancia formal de reunión
dentro de una Organization.

Assembly permite establecer:

- identidad de la reunión;
- organización convocante;
- territorio asociado cuando corresponda;
- tipo de Asamblea;
- propósito de la reunión;
- fecha y horario;
- modalidad de realización;
- estado de la Asamblea;
- condiciones de convocatoria;
- condiciones de realización;
- reglas propias de la Asamblea;
- trazabilidad de cambios relevantes;
- publicación de hechos del dominio.

Assembly constituye el límite de consistencia de la reunión.

No constituye el límite de consistencia de los procesos que
ocurren dentro de ella.

---

# Definición

Una Assembly representa una reunión formal convocada dentro del
contexto de una Organization.

Una Assembly posee identidad propia y mantiene su ciclo de vida,
estado, convocatoria, contexto organizacional y condiciones
necesarias para su desarrollo.

La Assembly puede representar reuniones tales como:

- Asamblea ordinaria;
- Asamblea extraordinaria;
- reunión organizacional;
- reunión de directorio;
- reunión comunitaria;
- sesión deliberativa;
- instancia formal de participación;
- reunión territorial;
- sesión de trabajo;
- instancia formal de consulta.

La naturaleza específica de una Assembly dependerá de las reglas
de la Organization y del contexto en que sea convocada.

Assembly no representa:

- una Organization;
- un Citizen;
- una Membership;
- un Role;
- un Territory;
- una Proposal;
- una Participation;
- una Voting;
- un Document;
- una Notification;
- un Audit;
- una Integration.

Estos corresponden a otros Aggregates del dominio.

---

# Responsabilidades

El Aggregate Assembly es responsable de:

- mantener la identidad de la Asamblea;
- mantener la Organization a la cual pertenece;
- mantener el contexto territorial cuando corresponda;
- administrar su ciclo de vida;
- controlar su estado;
- mantener la información formal de convocatoria;
- establecer las condiciones de realización;
- mantener la modalidad de la reunión;
- registrar el contexto formal de la reunión;
- controlar las reglas propias de la Asamblea;
- proteger sus invariantes;
- mantener la trazabilidad de sus cambios;
- controlar las condiciones necesarias para iniciar la Asamblea;
- controlar las condiciones necesarias para finalizarla;
- publicar Domain Events;
- mantener la consistencia de la Asamblea como unidad de dominio.

Assembly es responsable de representar la reunión como un hecho
formal del dominio.

No administra directamente:

- Organizations;
- Citizens;
- Memberships;
- Roles;
- Territories;
- Proposals;
- Participations;
- Votings;
- Documents;
- Notifications;
- Audits;
- Integrations.

---

# Responsabilidades Fuera del Aggregate

No es responsabilidad de Assembly:

- administrar Organizations;
- administrar Citizens;
- crear o modificar Memberships;
- definir Roles;
- administrar Territories;
- administrar permisos técnicos;
- ejecutar autenticación;
- administrar sesiones;
- administrar Proposals;
- ejecutar Votings;
- administrar procesos de Participation;
- almacenar Documents;
- enviar Notifications;
- ejecutar procesos de Audit;
- administrar Integrations externas.

Estas responsabilidades pertenecen a sus respectivos Aggregates
o Bounded Contexts.

La colaboración entre ellos se realiza mediante contratos de
dominio, identificadores, Domain Events e Integration Events.

Assembly nunca modifica directamente el estado interno de otro
Aggregate.

---

# Aggregate Root

La única Aggregate Root es:

```text
Assembly
```

Toda modificación sobre una Assembly debe realizarse
exclusivamente mediante la Aggregate Root.

Ninguna entidad interna, Value Object o componente perteneciente
al Aggregate puede modificar directamente el estado de la
Assembly desde fuera de su límite de consistencia.

La Aggregate Root controla:

- las transiciones de estado;
- las modificaciones de sus datos;
- las condiciones de convocatoria;
- las condiciones de inicio;
- las condiciones de finalización;
- las invariantes;
- la generación de Domain Events;
- el incremento de versión.

---

# Identidad

La identidad del Aggregate está determinada por:

```text
AssemblyId
```

Este identificador:

- es único;
- es global dentro del dominio;
- es inmutable;
- nunca cambia;
- nunca se reutiliza;
- no depende del mecanismo de persistencia.

Una Assembly conserva su AssemblyId durante todo su ciclo de
vida.

El cambio de nombre, fecha, modalidad, estado, territorio o
cualquier otra propiedad no modifica su identidad.

---

# Propietario Organizacional

Toda Assembly debe pertenecer a una Organization.

La relación se representa mediante:

```text
OrganizationId
```

OrganizationId:

- es obligatorio;
- identifica la Organization propietaria;
- no puede cambiar durante la vida de la Assembly;
- no constituye una referencia directa a otro Aggregate;
- no permite modificar la Organization desde Assembly.

Assembly conoce la identidad de la Organization, pero no administra
su estado.

---

# Contexto Territorial

Una Assembly puede mantener un territorio asociado mediante:

```text
TerritoryId
```

El TerritoryId:

- representa el territorio en cuyo contexto se desarrolla la
  Asamblea;
- se mantiene como identificador;
- no contiene el Aggregate Territory;
- no permite modificar el territorio desde Assembly.

La obligatoriedad del TerritoryId depende de las reglas de la
Organization y del tipo de Assembly.

Cuando una Assembly requiera territorio por definición de dominio,
la ausencia de TerritoryId constituye una violación de la
invariante correspondiente.

---

# Atributos Conceptuales

Una Assembly mantiene conceptualmente información equivalente a:

```text
AssemblyId

OrganizationId

TerritoryId

AssemblyType

Title

Description

Purpose

Status

ScheduledStartAt

ScheduledEndAt

ActualStartedAt

ActualEndedAt

Location

Modality

Convocation

QuorumPolicy

ParticipationPolicy

Rules

Version

CreatedAt

UpdatedAt
```

Los nombres y tipos concretos de implementación pertenecen al
modelo de dominio y deberán respetar los contratos definidos para
el Aggregate.

No se debe interpretar esta estructura como una autorización
para exponer setters públicos.

---

# Descripción de Atributos

## AssemblyId

Identificador único de la Assembly.

Es inmutable durante toda la vida del Aggregate.

---

## OrganizationId

Identificador de la Organization propietaria de la Assembly.

Es obligatorio e inmutable.

---

## TerritoryId

Identificador del Territory asociado cuando corresponda.

Puede ser obligatorio según el tipo de Assembly y las reglas de
la Organization.

---

## AssemblyType

Define la naturaleza formal de la reunión.

Ejemplos conceptuales:

```text
Ordinary

Extraordinary

Board

Community

Deliberative

Territorial

WorkingSession

Consultation
```

El conjunto definitivo de tipos debe respetar el lenguaje
ubícuo y las reglas del dominio.

---

## Title

Nombre identificable de la Asamblea.

Debe permitir distinguir formalmente la instancia de reunión
dentro de su contexto organizacional.

No constituye la identidad del Aggregate.

---

## Description

Descripción funcional de la Asamblea.

Permite registrar información contextual que no altera la
identidad del Aggregate.

---

## Purpose

Propósito formal de la Asamblea.

Define para qué se convoca la reunión.

El propósito debe estar disponible antes de que la Assembly sea
formalmente convocada cuando las reglas del dominio lo exijan.

---

## Status

Representa el estado actual de la Assembly.

El estado solamente puede cambiar mediante las transiciones
definidas por el Aggregate.

Estados conceptuales:

```text
Draft

Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

Las transiciones completas se definen en:

```text
DOMAIN-006B-State-Machine.md
```

---

## ScheduledStartAt

Fecha y hora planificada para el inicio.

---

## ScheduledEndAt

Fecha y hora planificada para el término.

Cuando exista, debe ser coherente con ScheduledStartAt.

---

## ActualStartedAt

Fecha y hora efectiva en que la Asamblea fue iniciada.

Debe existir únicamente cuando la Assembly haya alcanzado el
estado correspondiente a su inicio.

---

## ActualEndedAt

Fecha y hora efectiva en que la Asamblea fue completada.

Debe existir únicamente cuando la Assembly haya finalizado.

---

## Location

Representa el lugar físico, lógico o contextual de realización
cuando corresponda.

Puede utilizar Value Objects específicos del dominio.

---

## Modality

Representa la modalidad de realización.

Ejemplos:

```text
InPerson

Remote

Hybrid
```

La modalidad no determina por sí sola la infraestructura
tecnológica utilizada.

---

## Convocation

Representa las condiciones formales asociadas a la convocatoria.

Puede incluir conceptualmente:

```text
ConvokedAt

ConvocationDeadline

ConvocationMethod

ConvocationStatus
```

Estas condiciones pertenecen al dominio de Assembly y no deben
confundirse con Notification.

---

## QuorumPolicy

Representa las condiciones de quórum que deben respetarse para
los procesos que dependan de la Asamblea.

La política pertenece al contexto de la Assembly cuando forma
parte de sus invariantes.

La determinación de participantes concretos no pertenece a este
Aggregate.

---

## ParticipationPolicy

Representa las reglas propias de participación aplicables a la
Asamblea.

No administra las participaciones individuales.

Las participaciones con identidad propia pertenecen al Aggregate
Participation.

---

## Rules

Representa las reglas específicas que gobiernan la instancia de
Asamblea y que forman parte de su definición formal.

No debe utilizarse para almacenar reglas de infraestructura,
autenticación o autorización técnica.

---

## Version

Número de versión utilizado para control de concurrencia
optimista.

Cada modificación válida del Aggregate incrementa la versión.

---

## CreatedAt

Fecha y hora de creación de la Assembly.

No cambia durante la vida del Aggregate.

---

## UpdatedAt

Fecha y hora de la última modificación válida del Aggregate.

Se actualiza únicamente como consecuencia de una modificación
aceptada por la Aggregate Root.

---

# Entidades Internas

El Aggregate puede contener entidades internas necesarias para
representar conceptos propios de la Asamblea.

Entre ellas pueden existir:

```text
AssemblyConvocation

AssemblySchedule

AssemblyLocation

AssemblyRules

AssemblySession
```

Estas entidades:

- pertenecen al Aggregate Assembly;
- no poseen existencia independiente fuera del Aggregate;
- no pueden ser modificadas directamente desde otros Aggregates;
- deben respetar las invariantes de Assembly;
- no deben transformarse en Aggregates independientes sin una
  decisión explícita de diseño.

Una entidad interna puede poseer identidad propia dentro del
Aggregate, pero esa identidad no reemplaza AssemblyId.

---

# Value Objects

Entre los Value Objects del dominio pueden considerarse:

```text
AssemblyTitle

AssemblyDescription

AssemblyPurpose

AssemblyType

AssemblyStatus

AssemblySchedule

AssemblyLocation

AssemblyModality

AssemblyConvocation

AssemblyRules

QuorumPolicy

ParticipationPolicy
```

Todos los Value Objects son inmutables.

Los Value Objects no poseen identidad independiente del contexto
en que son utilizados.

Cuando un concepto necesite identidad, ciclo de vida,
consistencia independiente o colaboración propia entre
transacciones, debe evaluarse como Entity o Aggregate según las
reglas de diseño de AURA.

---

# Estado

El ciclo de vida de Assembly se representa mediante AssemblyStatus.

Estados conceptuales:

```text
Draft

Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

La interpretación de cada estado es:

## Draft

La Assembly existe como definición inicial y todavía no ha sido
formalmente programada o convocada.

## Scheduled

La Asamblea posee una fecha y condiciones de realización
establecidas.

## Convoked

La convocatoria formal ha sido realizada y la Asamblea se
encuentra disponible para su instancia programada.

## InProgress

La Asamblea se encuentra en ejecución después de haber comenzado formalmente.

## Completed

La Asamblea ha finalizado formalmente.

## Cancelled

La Asamblea fue cancelada antes de completar su realización.

## Archived

La Assembly ha sido retirada del ciclo operativo y pasa a un
estado histórico.

Las transiciones válidas se encuentran formalmente definidas en:

```text
DOMAIN-006A-Lifecycle.md

DOMAIN-006B-State-Machine.md
```

---

# Reglas de Estado

El Aggregate debe garantizar como mínimo:

- una Assembly nueva comienza en un estado válido;
- una Assembly no puede iniciarse si no cumple las condiciones
  requeridas para su inicio;
- una Assembly no puede completarse antes de haber sido iniciada;
- una Assembly cancelada no puede continuar normalmente sin una
  operación explícita permitida por el dominio;
- una Assembly completada no puede volver a estado InProgress;
- una Assembly archivada no puede modificarse mediante operaciones
  ordinarias;
- toda transición debe estar definida por la máquina de estados;
- ninguna transición puede omitir las invariantes del Aggregate.

Las reglas exhaustivas se documentan en:

```text
DOMAIN-006E-Invariants.md
```

---

# Invariantes

El Aggregate Assembly mantiene como mínimo las siguientes
invariantes:

- AssemblyId siempre existe;
- AssemblyId nunca cambia;
- OrganizationId siempre existe;
- OrganizationId nunca cambia;
- TerritoryId debe existir cuando el tipo de Assembly lo exige;
- AssemblyType siempre es válido;
- Title debe cumplir las reglas de identidad descriptiva del
  dominio;
- Purpose debe existir cuando sea obligatorio para la convocatoria;
- ScheduledStartAt debe ser una fecha válida;
- ScheduledEndAt no puede preceder a ScheduledStartAt;
- ActualStartedAt solamente puede existir después del inicio;
- ActualEndedAt solamente puede existir después de la finalización;
- ActualEndedAt no puede preceder a ActualStartedAt;
- una Assembly no puede iniciarse sin cumplir sus condiciones de
  convocatoria;
- una Assembly no puede completarse si no ha sido iniciada;
- una Assembly archivada no puede modificarse mediante comandos
  ordinarios;
- toda modificación válida incrementa Version;
- toda transición debe pertenecer a la máquina de estados;
- las invariantes deben mantenerse antes y después de cada
  operación del Aggregate.

Las reglas completas se desarrollan en:

```text
DOMAIN-006E-Invariants.md
```

---

# Relaciones

Assembly mantiene relaciones con otros Aggregates exclusivamente
mediante identificadores.

```text
Assembly
    │
    ├──────── OrganizationId
    │
    ├──────── TerritoryId
    │
    ├──────── MembershipId
    │
    ├──────── CitizenId
    │
    ├──────── RoleId
    │
    ├──────── ProposalId
    │
    ├──────── ParticipationId
    │
    ├──────── VotingId
    │
    ├──────── DocumentId
    │
    ├──────── NotificationId
    │
    └──────── AuditId
```

Estas relaciones no implican que Assembly almacene Aggregates
completos.

Assembly solamente mantiene las referencias necesarias para
expresar su contexto de dominio.

Las relaciones con Membership, Citizen, Role, Proposal,
Participation, Voting, Document, Notification y Audit no
convierten a esos conceptos en entidades internas de Assembly.

---

# Organización y Assembly

Una Organization puede poseer múltiples Assemblies.

La relación conceptual es:

```text
Organization
      │
      │ 1
      │
      ├────────── N
      │
    Assembly
```

Assembly pertenece a una única Organization.

Assembly no puede cambiar de Organization mediante una operación
ordinaria.

Si una reunión debe pertenecer a otra Organization, debe crearse
una nueva instancia de Assembly conforme a las reglas del
dominio.

---

# Territorio y Assembly

Una Assembly puede estar vinculada a un Territory.

La relación se mantiene mediante:

```text
TerritoryId
```

Assembly no administra el Territory.

La validez del territorio debe ser comprobada mediante las
reglas de dominio correspondientes y, cuando sea necesario,
mediante coordinación entre Aggregates.

No se permite resolver esta relación almacenando el Aggregate
Territory dentro de Assembly.

---

# Membership y Assembly

La pertenencia a una Organization es administrada por
Membership.

Assembly no crea, activa, suspende ni termina Memberships.

Cuando una Asamblea necesite determinar quién puede participar,
la decisión se realiza mediante los contratos y políticas
correspondientes.

Assembly puede utilizar referencias como:

```text
MembershipId
```

sin asumir la responsabilidad sobre el ciclo de vida de la
Membership.

---

# Citizen y Assembly

Citizen representa la identidad cívica.

Assembly no administra Citizens.

La identificación de una persona participante se realiza mediante
CitizenId cuando el proceso de dominio correspondiente lo requiera.

Assembly no modifica el estado de un Citizen.

---

# Role y Assembly

Role representa una función organizacional.

Assembly puede utilizar Roles como parte de sus reglas de
participación o convocatoria.

No administra Roles.

La relación se mantiene mediante:

```text
RoleId
```

---

# Proposal y Assembly

Una Assembly puede constituir el contexto dentro del cual una
Proposal sea presentada o deliberada.

Assembly no administra el ciclo de vida de Proposal.

La relación se mantiene mediante:

```text
ProposalId
```

La Proposal conserva su propia identidad, reglas, invariantes,
estado y eventos.

---

# Participation y Assembly

Participation representa la participación de un actor en un
proceso de participación.

Assembly proporciona el contexto de reunión, pero no reemplaza
el Aggregate Participation.

La relación puede expresarse mediante:

```text
ParticipationId
```

Assembly no administra el historial individual de participación.

---

# Voting y Assembly

Una Assembly puede contener el contexto organizacional para uno o
más procesos de Voting.

Voting posee su propio Aggregate Root y sus propias invariantes.

Assembly no ejecuta directamente el ciclo de vida de Voting.

La relación se mantiene mediante:

```text
VotingId
```

---

# Document y Assembly

Documents pueden estar asociados a una Assembly para representar
convocatorias, antecedentes, actas u otros documentos formales.

Assembly no almacena ni administra el contenido del Document.

La relación se mantiene mediante:

```text
DocumentId
```

---

# Notification y Assembly

Las Notifications pueden utilizar eventos de Assembly para
informar a los actores correspondientes.

Assembly no envía Notifications directamente.

La comunicación se realiza mediante Domain Events o Integration
Events.

---

# Audit y Assembly

Las modificaciones relevantes de Assembly pueden producir
información utilizada por el contexto de auditoría.

Assembly no administra el Aggregate Audit.

La trazabilidad se propaga mediante eventos y contratos
establecidos por la arquitectura.

---

# Consistencia

Assembly constituye un límite de consistencia.

Todas las modificaciones sobre el Aggregate deben respetar:

- una única operación de dominio;
- una única Aggregate Root;
- invariantes válidas;
- transición válida;
- control de concurrencia;
- generación coherente de eventos.

No existen actualizaciones parciales del Aggregate.

Las operaciones internas deben finalizar con el Aggregate en un
estado válido.

La consistencia dentro de Assembly es inmediata.

La consistencia entre Assembly y otros Aggregates es eventual.

---

# Límite de Consistencia

El límite de consistencia de Assembly comprende:

```text
Assembly
    │
    ├── entidades internas;
    │
    └── Value Objects
```

No comprende:

```text
Organization
Citizen
Membership
Role
Territory
Proposal
Participation
Voting
Document
Notification
Audit
Integration
```

Estos permanecen fuera del límite.

La definición formal se desarrolla en:

```text
DOMAIN-006J-Consistency-Boundary.md
```

---

# Commands

El Aggregate Assembly responde a Commands que expresan
intenciones del dominio.

Ejemplos:

```text
CreateAssembly

ScheduleAssembly

RescheduleAssembly

ConvokeAssembly

RenameAssembly

ChangeAssemblyType

ChangeAssemblyPurpose

ChangeAssemblyDescription

ChangeAssemblyModality

ChangeAssemblyLocation

UpdateAssemblyConvocation

UpdateAssemblyRules

UpdateAssemblyExecutionConditions

StartAssembly

CompleteAssembly

CancelAssembly

ArchiveAssembly
```

Los Commands:

- expresan intención;
- no modifican directamente propiedades;
- son validados por el Aggregate;
- solamente producen cambios si las invariantes lo permiten;
- pueden generar Domain Events.

La especificación completa se encuentra en:

```text
DOMAIN-006C-Commands.md
```

---

# Operaciones Públicas

La Aggregate Root expone comportamiento de dominio.

Conceptualmente:

```text
create()

schedule()

reschedule()

convoke()

rename()

changeType()

changePurpose()

changeDescription()

changeModality()

changeLocation()

updateConvocation()

updateRules()

updateExecutionConditions()

start()

complete()

cancel()

archive()
```

No se exponen setters públicos.

No se permite modificar directamente:

```text
status

version

organizationId

assemblyId

actualStartedAt

actualEndedAt
```

Estos valores son controlados por comportamiento de dominio.

---

# Eventos del Dominio

Assembly publica Domain Events cuando ocurre un hecho relevante
y aceptado por el Aggregate.

Ejemplos:

```text
AssemblyCreated

AssemblyScheduled

AssemblyRescheduled

AssemblyConvoked

AssemblyRenamed

AssemblyTypeChanged

AssemblyPurposeChanged

AssemblyDescriptionChanged

AssemblyModalityChanged

AssemblyLocationChanged

AssemblyConvocationUpdated

AssemblyRulesUpdated

AssemblyExecutionConditionsUpdated

AssemblyStarted

AssemblyCompleted

AssemblyCancelled

AssemblyArchived
```

Los eventos representan hechos consumados.

No deben utilizarse como Commands.

La especificación completa se encuentra en:

```text
DOMAIN-006D-Domain-Events.md
```

---

# Ciclo de Vida

El ciclo de vida de Assembly permite distinguir claramente entre
la existencia de la instancia de reunión y su ejecución.

Conceptualmente:

```text
Draft
   │
   ▼
Scheduled
   │
   ▼
Convoked
   │
   ▼
InProgress
   │
   ▼
Completed
   │
   ▼
Archived
```

Existe además una ruta de cancelación:

```text
Draft ─────────► Cancelled

Scheduled ─────► Cancelled

Convoked ──────► Cancelled
```

Las rutas exactas, condiciones y transiciones permitidas no deben
inferirse desde este documento.

Se encuentran formalmente definidas en:

```text
DOMAIN-006A-Lifecycle.md
DOMAIN-006B-State-Machine.md
```

---

# Convocatoria

La convocatoria constituye una condición formal del ciclo de
vida de Assembly.

Convocar una Assembly no equivale a enviar una Notification.

La convocatoria es un hecho de dominio.

El mecanismo utilizado para comunicarla puede pertenecer a otro
Bounded Context.

La Assembly debe conservar las condiciones necesarias para
determinar que su convocatoria es válida.

Entre ellas pueden existir:

```text
fecha de convocatoria;

fecha programada;

condiciones de convocatoria;

modalidad;

lugar;

propósito;

reglas aplicables.
```

La entrega efectiva de comunicaciones corresponde al contexto
responsable de Notifications.

---

# Inicio

Una Assembly puede ser iniciada únicamente cuando cumple las
condiciones establecidas por su ciclo de vida y sus invariantes.

El inicio:

- cambia el estado;
- registra ActualStartedAt;
- incrementa Version;
- genera el Domain Event correspondiente.

El inicio no debe modificar directamente otros Aggregates.

---

# Finalización

La finalización representa el término formal de la Asamblea.

Al completar:

- el estado cambia a Completed;
- ActualEndedAt queda registrado;
- Version se incrementa;
- se publica AssemblyCompleted.

Una Assembly completada no puede continuar como Assembly InProgress
mediante una modificación ordinaria.

Los procesos derivados, como actas, votaciones o documentos,
permanecen bajo sus propios Aggregates.

---

# Cancelación

La cancelación representa la decisión formal de no realizar una
Assembly programada o convocada.

Cancelar no significa eliminar.

La identidad de la Assembly permanece.

El historial del Aggregate debe conservar el hecho de que la
instancia fue cancelada.

Las condiciones de cancelación se encuentran en:

```text
DOMAIN-006E-Invariants.md

DOMAIN-006C-Commands.md
```

---

# Archivado

Archivar una Assembly significa retirar la instancia del ciclo
operativo y conservarla como parte del historial del dominio.

Una Assembly archivada:

- conserva su AssemblyId;
- conserva su historial;
- no puede modificarse mediante operaciones ordinarias;
- puede continuar siendo consultada por Read Models;
- puede ser utilizada como referencia histórica.

Archivar no equivale a eliminar físicamente el Aggregate.

---

# Reglas de Modificación

Las modificaciones deben cumplir:

- ninguna modificación directa de atributos;
- ninguna modificación fuera de la Aggregate Root;
- ninguna modificación de AssemblyId;
- ninguna modificación de OrganizationId;
- ninguna modificación que viole la máquina de estados;
- ninguna modificación que deje el Aggregate en estado inválido;
- toda modificación válida incrementa Version;
- toda modificación relevante genera el Domain Event
  correspondiente.

Las reglas detalladas se encuentran en:

```text
DOMAIN-006E-Invariants.md
```

---

# Fuente de Verdad

La fuente de verdad de Assembly es el Aggregate Assembly y,
cuando corresponda, su historial de Domain Events.

Los Read Models no constituyen la fuente de verdad.

Los Read Models pueden ser reconstruidos.

Una proyección de Assembly no puede utilizarse para modificar
directamente el Aggregate.

---

# Persistencia

El Repository persiste Assembly como una unidad de consistencia.

Conceptualmente:

```text
Assembly
    │
    ├── State
    ├── Value Objects
    ├── Internal Entities
    └── Version
```

No se deben persistir partes del Aggregate de forma independiente
mediante operaciones que permitan violar sus invariantes.

El contrato formal se define en:

```text
DOMAIN-006G-Repository-Contract.md
```

---

# Versionado

Assembly utiliza Versionado Optimista.

Cada modificación válida incrementa:

```text
Version
```

El Repository debe verificar que la versión esperada coincida
con la versión persistida antes de aceptar la escritura.

Ante una concurrencia incompatible:

```text
ConcurrencyConflict
```

debe producirse el comportamiento definido por el contrato de
persistencia.

La especificación se encuentra en:

```text
DOMAIN-006I-Versioning.md
```

---

# Seguridad

Assembly no administra autenticación.

Assembly no almacena:

- contraseñas;
- tokens;
- claves privadas;
- secretos criptográficos;
- credenciales de usuarios;
- sesiones.

La autorización de las operaciones se evalúa mediante las
políticas y permisos definidos por el modelo de seguridad de
AURA.

La operación de dominio debe recibir una intención autorizada,
pero el Aggregate continúa siendo responsable de proteger sus
invariantes.

Las reglas formales se encuentran en:

```text
DOMAIN-006F-Permissions.md

DOMAIN-006O-Security-Model.md
```

---

# Permisos

Los permisos determinan quién puede solicitar determinadas
operaciones sobre Assembly.

Conceptualmente pueden existir permisos para:

```text
create assembly

schedule assembly

convoke assembly

start assembly

complete assembly

cancel assembly

archive assembly

change assembly rules
```

El permiso no reemplaza la validación del Aggregate.

Una operación puede ser autorizada técnicamente y aun así ser
rechazada por una invariante de dominio.

La especificación completa se encuentra en:

```text
DOMAIN-006F-Permissions.md
```

---

# Integración

Assembly puede integrarse con otros Bounded Contexts y sistemas
externos mediante eventos y contratos.

Puede relacionarse con:

- Organization Management;
- Citizen Management;
- Membership Management;
- Authorization Management;
- Territory Management;
- Proposal Management;
- Participation Management;
- Voting Management;
- Document Management;
- Notification Management;
- Audit;
- Smart City Integration;
- plataformas municipales;
- FIWARE.

Estas integraciones no deben introducir dependencias directas
sobre la implementación interna del Aggregate.

---

# Integration Events

Los hechos de dominio relevantes pueden transformarse en
Integration Events para otros contextos.

Ejemplos:

```text
AssemblyPublished

AssemblyRescheduledForIntegration

AssemblyConvocationPublished

AssemblyConvocationUpdatedForIntegration

AssemblyStartedForIntegration

AssemblyCompletedForIntegration

AssemblyCancelledForIntegration

AssemblyArchivedForIntegration

AssemblyDetailsChanged
```

Los Integration Events:

- no reemplazan Domain Events;
- no forman parte del estado interno del Aggregate;
- no permiten modificar directamente Assembly;
- representan contratos de integración.

La definición formal se encuentra en:

```text
DOMAIN-006K-Integration-Events.md
```

---

# Read Model

Assembly puede disponer de Read Models especializados para
consulta.

Ejemplos:

```text
AssemblySummary

AssemblyCalendarView

AssemblyDetailView

AssemblyHistoryView

AssemblyPublicView
```

Los Read Models:

- son proyecciones;
- pueden reconstruirse;
- no constituyen fuente de verdad;
- no contienen autoridad para modificar el Aggregate;
- pueden optimizarse para diferentes necesidades de consulta.

La definición se encuentra en:

```text
DOMAIN-006L-Read-Model.md
```

---

# Rendimiento

El Aggregate debe mantenerse pequeño y enfocado en la
consistencia de la Assembly.

No debe cargar Aggregates externos para ejecutar operaciones
ordinarias.

Debe utilizar identificadores y contratos de dominio.

Las consultas complejas deben resolverse mediante Read Models y
no mediante expansión innecesaria del Aggregate.

Las reglas específicas de rendimiento se encuentran en:

```text
DOMAIN-006N-Performance-Rules.md
```

---

# Extensibilidad

Assembly debe permitir evolución sin modificar innecesariamente
su núcleo.

Los puntos de extensión pueden incluir:

```text
AssemblyType

AssemblyRules

ParticipationPolicy

QuorumPolicy

AssemblyModality

Domain Events

Integration Events

Read Models
```

Las extensiones no deben:

- romper invariantes existentes;
- modificar retrospectivamente la identidad;
- introducir dependencias con Infrastructure;
- convertir otros Aggregates en entidades internas;
- crear acoplamiento directo con sistemas externos.

La especificación se encuentra en:

```text
DOMAIN-006P-Extension-Points.md
```

---

# Compatibilidad Arquitectónica

Assembly está diseñado para cumplir:

- Domain-Driven Design;
- Aggregate Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- Event-Driven Architecture;
- CQRS;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- High Cohesion;
- Low Coupling.

El Aggregate pertenece al dominio y no depende de tecnologías de
Infrastructure.

---

# Dependencias

Assembly depende conceptualmente de:

- Shared Kernel;
- Value Objects;
- Domain Events;
- Repository Contracts;
- contratos de dominio definidos por AURA.

Assembly no depende directamente de:

```text
Infrastructure

Frameworks

Bases de datos

HTTP

REST

GraphQL

OAuth

JWT

React

Next.js

FastAPI

Django

FIWARE SDK

MongoDB

PostgreSQL
```

Las implementaciones tecnológicas pertenecen a capas externas.

---

# Relaciones Estratégicas

Assembly es utilizado o consumido estratégicamente por:

- Organization Management;
- Membership Management;
- Participation;
- Proposal Management;
- Voting;
- Documents;
- Notifications;
- Audit;
- Governance;
- Analytics;
- Smart City Integration.

Assembly constituye uno de los Aggregates centrales para los
procesos formales de deliberación y participación colectiva.

---

# CQRS

Assembly es compatible con CQRS.

En el lado de escritura:

```text
Command
   │
   ▼
Assembly Aggregate
   │
   ├── Invariants
   ├── State Transition
   └── Domain Events
```

En el lado de lectura:

```text
Domain Events
      │
      ▼
Projection
      │
      ▼
Read Model
```

El Read Model no reemplaza al Aggregate.

---

# Event Sourcing

Assembly es compatible con Event Sourcing.

Los Domain Events pueden representar la evolución histórica del
Aggregate.

Conceptualmente:

```text
AssemblyCreated
        ↓
AssemblyScheduled
        ↓
AssemblyConvoked
        ↓
AssemblyStarted
        ↓
AssemblyCompleted
```

El historial debe ser inmutable.

Los eventos representan hechos ocurridos y no instrucciones
futuras.

La implementación concreta de Event Sourcing pertenece a la
infraestructura y no debe introducirse en el modelo de dominio.

---

# Trazabilidad

Assembly debe permitir reconstruir conceptualmente:

- cuándo fue creada;
- cuándo fue programada;
- cuándo fue convocada;
- cuándo fue iniciada;
- cuándo fue completada;
- cuándo fue cancelada;
- cuándo fue archivada;
- qué cambios relevantes ocurrieron;
- qué versión produjo cada modificación.

La trazabilidad no implica que Audit sea una entidad interna del
Aggregate.

La auditoría se integra mediante eventos y contratos.

---

# Reglas de Diseño del Aggregate

Assembly debe respetar:

- una única Aggregate Root;
- identidad única e inmutable;
- alto nivel de cohesión;
- bajo acoplamiento;
- invariantes protegidas;
- comportamiento orientado a métodos;
- ausencia de setters públicos;
- ausencia de referencias directas a otros Aggregates;
- colaboración mediante identificadores;
- consistencia transaccional interna;
- consistencia eventual entre Aggregates;
- Domain Events para hechos del dominio;
- Integration Events para integración externa;
- Read Models para consultas;
- Repository Contract para persistencia;
- Versionado Optimista para concurrencia.

---

# Escenarios de Uso Conceptuales

Assembly debe poder representar escenarios como:

## Asamblea Ordinaria

Una Organization programa una Asamblea ordinaria, establece
fecha, modalidad, propósito y condiciones de convocatoria.

## Asamblea Extraordinaria

Una Organization crea una Asamblea extraordinaria para tratar
una materia específica bajo reglas especiales.

## Asamblea Territorial

Una Assembly se asocia a un Territory mediante TerritoryId.

## Asamblea Híbrida

Una Assembly se configura con modalidad:

```text
Hybrid
```

sin incorporar infraestructura tecnológica dentro del Aggregate.

## Asamblea Cancelada

Una Assembly programada o convocada puede ser cancelada cuando
las condiciones del dominio lo permiten.

## Asamblea Completada

Una Assembly InProgress puede completarse formalmente y conservar su
historial.

---

# Restricciones Arquitectónicas

No está permitido:

- convertir Citizen en entidad interna de Assembly;
- convertir Membership en entidad interna de Assembly;
- convertir Organization en entidad interna de Assembly;
- convertir Proposal en entidad interna de Assembly;
- convertir Voting en entidad interna de Assembly;
- almacenar Aggregates completos dentro de Assembly;
- acceder directamente a repositorios de otros Aggregates desde
  Assembly;
- realizar llamadas HTTP desde el Aggregate;
- acceder directamente a bases de datos desde el Aggregate;
- ejecutar lógica de infraestructura dentro del Aggregate;
- enviar Notifications directamente desde el Aggregate;
- ejecutar integraciones externas directamente desde el Aggregate;
- modificar el estado de otro Aggregate dentro de la misma
  operación interna de Assembly.

---

# Objetivos de Diseño

El Aggregate busca garantizar:

- identidad formal de la Asamblea;
- consistencia del ciclo de vida;
- consistencia de convocatoria;
- trazabilidad;
- independencia tecnológica;
- interoperabilidad;
- bajo acoplamiento;
- alta cohesión;
- evolución controlada;
- compatibilidad con CQRS;
- compatibilidad con Event Sourcing;
- compatibilidad con arquitecturas distribuidas;
- integración con Smart City;
- separación clara entre reunión y procesos derivados.

---

# Definición de Éxito

El Aggregate **Assembly** representa la instancia formal de
reunión, deliberación y participación colectiva del ecosistema
AURA.

Actúa como el punto de referencia para la existencia, convocatoria,
programación, inicio, finalización, cancelación y archivado de una
Asamblea dentro de una Organization.

Mantiene su propia identidad, ciclo de vida, reglas, invariantes,
consistencia y trazabilidad, sin absorber responsabilidades de
Citizen, Organization, Membership, Role, Territory, Proposal,
Participation, Voting, Document, Notification o Audit.

La colaboración con otros Aggregates se realiza mediante
identificadores, Domain Events, Integration Events y contratos
explícitos.

El diseño mantiene los principios de Domain-Driven Design,
Clean Architecture, Hexagonal Architecture, CQRS y Event-Driven
Architecture, permitiendo que Assembly evolucione sin romper los
límites de consistencia ni introducir dependencias tecnológicas
en el dominio.