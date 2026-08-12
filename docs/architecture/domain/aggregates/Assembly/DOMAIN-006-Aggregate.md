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

Documentos relacionados:

* DOMAIN-001-Aggregate.md
* DOMAIN-002-Aggregate.md
* DOMAIN-003-Aggregate.md
* DOMAIN-004-Aggregate.md
* DOMAIN-005-Aggregate.md
* DOMAIN-006A-Lifecycle.md
* DOMAIN-006B-State-Machine.md
* DOMAIN-006C-Commands.md
* DOMAIN-006D-Domain-Events.md
* DOMAIN-006E-Invariants.md
* DOMAIN-006F-Permissions.md
* DOMAIN-006G-Repository-Contract.md
* DOMAIN-006H-Examples.md
* DOMAIN-006I-Versioning.md
* DOMAIN-006J-Consistency-Boundary.md
* DOMAIN-006K-Integration-Events.md
* DOMAIN-006L-Read-Model.md
* DOMAIN-006M-Test-Scenarios.md
* DOMAIN-006N-Performance-Rules.md
* DOMAIN-006O-Security-Model.md
* DOMAIN-006P-Extension-Points.md
* CORE-002-Bounded-Context-Map.md
* CORE-003-Shared-Kernel.md
* CORE-004-Ubiquitous-Language.md
* CORE-006-Domain-Invariants.md
* CORE-007-Strategic-Design.md
* CORE-008-Aggregate-Design-Rules.md
* CORE-011-Repository-Contracts.md

---

# Objetivo

Definir el Aggregate **Assembly**, responsable de representar una
instancia formal de reunión, deliberación y participación
colectiva dentro del ecosistema AURA.

Una Assembly constituye el contexto formal en el cual los
integrantes de una **Organization** pueden reunirse, tratar
materias, deliberar y desarrollar procesos organizacionales o
comunitarios.

El Aggregate centraliza la identidad de la reunión, su
clasificación, programación, convocatoria, modalidad, estado y
ciclo de vida, proporcionando un contexto consistente para los
procesos de Participation, Proposal, Voting, Document,
Notification y Audit.

Assembly representa exclusivamente la reunión formal.

Los procesos que ocurran dentro de ella y posean identidad,
ciclo de vida o invariantes propias permanecen bajo la
responsabilidad de sus respectivos Aggregates.

---

# Definición

Una **Assembly** representa una reunión formal convocada dentro
del contexto de una Organization.

Dependiendo de las reglas organizacionales y del propósito de la
reunión, una Assembly puede corresponder a:

* Asamblea ordinaria;
* Asamblea extraordinaria;
* reunión de directorio;
* reunión organizacional;
* reunión comunitaria;
* reunión territorial;
* sesión deliberativa;
* sesión de trabajo;
* instancia formal de consulta;
* instancia formal de participación.

La naturaleza de la Assembly se expresa mediante su tipo y sus
reglas de dominio.

El Aggregate no impone que todas las organizaciones utilicen los
mismos tipos de reunión.

La clasificación puede evolucionar mediante los mecanismos de
extensión definidos para el dominio, manteniendo siempre la
identidad y las invariantes fundamentales de Assembly.

---

# Propósito

Assembly proporciona una representación consistente de una
reunión formal dentro del dominio AURA.

Su propósito es garantizar que toda Assembly posea:

* identidad única;
* Organization propietaria;
* contexto territorial cuando corresponda;
* nombre;
* tipo;
* propósito;
* programación;
* modalidad;
* ubicación cuando corresponda;
* convocatoria;
* condiciones de realización;
* estado;
* ciclo de vida;
* trazabilidad;
* versión.

Assembly permite que otros Aggregates utilicen:

```text
AssemblyId
```

como referencia estable hacia una reunión sin requerir acceso
directo al estado interno del Aggregate.

---

# Responsabilidades

El Aggregate Assembly es responsable de:

* mantener su identidad;
* mantener la Organization propietaria;
* mantener el Territory asociado cuando corresponda;
* administrar su ciclo de vida;
* controlar su estado;
* definir su clasificación;
* mantener su nombre;
* mantener su propósito;
* mantener su descripción;
* administrar su programación;
* administrar su modalidad;
* mantener su ubicación cuando corresponda;
* mantener la información formal de convocatoria;
* mantener las reglas propias de la reunión;
* mantener las condiciones necesarias para su realización;
* controlar las condiciones necesarias para iniciar;
* controlar las condiciones necesarias para finalizar;
* controlar las condiciones necesarias para cancelar;
* controlar las condiciones necesarias para archivar;
* proteger sus invariantes;
* mantener Version;
* publicar Domain Events.

No administra directamente:

* Organizations;
* Citizens;
* Memberships;
* Roles;
* Territories;
* Proposals;
* Participations;
* Votings;
* Documents;
* Notifications;
* Audits;
* Integrations.

Estos conceptos mantienen sus propios límites de consistencia.

---

# Aggregate Root

La única Aggregate Root es:

```text
Assembly
```

Toda modificación de la reunión debe realizarse exclusivamente a
través de esta entidad.

No existen modificaciones directas sobre atributos internos,
entidades internas o Value Objects desde fuera del Aggregate.

Assembly protege sus invariantes y controla todas las
transiciones válidas de su ciclo de vida.

---

# Identidad

Cada Assembly posee un identificador único e inmutable.

```text
AssemblyId
```

Este identificador:

* es global dentro del dominio;
* es inmutable;
* nunca cambia;
* nunca se reutiliza;
* no depende del almacenamiento;
* no depende del nombre de la reunión;
* no depende de su estado;
* no depende de su programación;
* no depende de identificadores externos.

AssemblyId permanece constante durante todo el ciclo de vida del
Aggregate.

---

# Contexto Organizacional

Toda Assembly pertenece exactamente a una Organization.

La relación se mantiene mediante:

```text
OrganizationId
```

OrganizationId:

* es obligatorio;
* identifica la Organization propietaria;
* permanece inmutable durante toda la vida de Assembly;
* no representa una referencia directa al objeto Organization.

Assembly no administra la Organization.

Una Assembly no puede cambiar de Organization mediante una
operación ordinaria del dominio.

---

# Contexto Territorial

Una Assembly puede estar asociada a un Territory.

La relación se mantiene mediante:

```text
TerritoryId
```

TerritoryId puede ser opcional cuando la naturaleza de la
reunión no requiere un contexto territorial explícito.

Cuando existe, permite asociar la reunión con:

* una Región;
* una Provincia;
* una Comuna;
* un Distrito;
* un Barrio;
* un Sector;
* una Unidad Vecinal;
* una Comunidad;
* un Territorio Indígena;
* cualquier otra unidad reconocida por Territory.

Assembly no administra la estructura territorial.

Territory conserva su identidad, jerarquía, clasificación,
geometría y ciclo de vida dentro de su propio Aggregate.

---

# Modelo Conceptual

```text
Organization
      │
      │ 1
      ▼
Assembly
      │
      ├──────── Territory
      │
      ├──────── Participation
      │
      ├──────── Proposal
      │
      ├──────── Voting
      │
      ├──────── Document
      │
      ├──────── Notification
      │
      └──────── Audit
```

Una Organization puede poseer múltiples Assemblies.

Cada Assembly pertenece a una única Organization.

Una Assembly puede utilizar Territory como contexto geográfico.

Participation, Proposal, Voting, Document, Notification y Audit
pueden relacionarse con Assembly mediante AssemblyId.

Estas relaciones no representan composición interna.

---

# Estado del Aggregate

El Aggregate mantiene, como mínimo, la siguiente información:

```text
AssemblyId

OrganizationId

TerritoryId

AssemblyName

AssemblyType

AssemblyPurpose

AssemblyDescription

AssemblyStatus

ScheduledStartAt

ScheduledEndAt

TimeZone

AssemblyModality

AssemblyLocation

Convocation

AssemblyRules

ExecutionConditions

CreatedAt

UpdatedAt

ConvokedAt

StartedAt

CompletedAt

CancelledAt

ArchivedAt

Version
```

Los atributos opcionales dependen del estado, tipo y reglas
aplicables a la Assembly.

---

# Atributos Conceptuales

## AssemblyId

Identificador único e inmutable del Aggregate.

---

## OrganizationId

Identificador de la Organization propietaria.

Es obligatorio e inmutable.

---

## TerritoryId

Identificador del Territory asociado cuando corresponda.

Puede ser opcional.

---

## AssemblyName

Nombre formal de la reunión.

Ejemplos:

```text
Asamblea General Ordinaria

Asamblea Extraordinaria

Reunión de Directorio

Asamblea Comunitaria

Asamblea Territorial
```

El nombre no constituye la identidad del Aggregate.

---

## AssemblyType

Clasificación conceptual de la reunión.

Ejemplos:

```text
Ordinary

Extraordinary

Organizational

Board

Community

Deliberative

Participatory

Territorial

WorkingSession

Consultation
```

El tipo permite clasificar la reunión sin modificar su identidad.

---

## AssemblyPurpose

Representa el propósito formal de la reunión.

Describe la razón por la cual la Assembly existe y para qué fue
convocada.

AssemblyPurpose no representa una Proposal.

Una Proposal puede ser presentada o tratada dentro del contexto
de una Assembly manteniendo su propio Aggregate.

---

## AssemblyDescription

Descripción complementaria de la reunión.

Permite incorporar contexto adicional sin modificar el propósito
formal.

Puede ser opcional.

---

## ScheduledStartAt

Fecha y hora programadas para el inicio.

Representa planificación.

No representa necesariamente el momento efectivo de inicio.

---

## ScheduledEndAt

Fecha y hora programadas para la finalización.

Cuando exista, debe ser posterior a ScheduledStartAt.

---

## TimeZone

Zona horaria utilizada para interpretar la programación.

Permite representar de forma inequívoca las fechas y horas de la
Assembly.

---

## AssemblyModality

Modalidad mediante la cual se desarrollará la reunión.

Valores conceptuales:

```text
InPerson

Remote

Hybrid
```

La modalidad pertenece al dominio de Assembly.

No representa la infraestructura tecnológica utilizada para
ejecutar una reunión remota.

---

## AssemblyLocation

Representa la ubicación cuando corresponda.

Puede incluir conceptos como:

```text
Address

Venue

Room

Reference
```

Una Assembly remota puede no requerir ubicación física.

Una Assembly presencial debe mantener una ubicación compatible
con las reglas aplicables.

---

## Convocation

Representa la información formal de convocatoria.

Puede incluir:

```text
ConvocationStatus

ConvocationDate

ConvocationDeadline

ConvocationMethod

ConvocationReference
```

Convocation representa el estado formal de la convocatoria.

No representa una Notification.

Notification pertenece a su propio Aggregate.

---

## AssemblyRules

Representa reglas propias de la reunión.

Puede incluir condiciones como:

```text
QuorumRequired

RemoteParticipationAllowed

PublicParticipationAllowed

ProposalSubmissionAllowed

VotingAllowed

RecordingAllowed
```

Estas reglas pertenecen a Assembly únicamente cuando forman parte
de las condiciones de la reunión.

Las reglas internas de Participation, Proposal o Voting
permanecen bajo sus respectivos Aggregates.

---

## ExecutionConditions

Representa las condiciones necesarias para que la Assembly pueda
realizarse.

Puede incluir:

```text
RequiredConvocation

RequiredSchedule

RequiredLocation

RequiredDocumentation

MinimumAttendance

RequiredQuorum
```

ExecutionConditions permite que Assembly determine si se
encuentra en condiciones válidas para iniciar.

No convierte a Citizen, Membership o Participation en entidades
internas del Aggregate.

---

## AssemblyStatus

Representa el estado actual del ciclo de vida.

Valores oficiales iniciales:

```text
Draft

Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

Toda transición debe ser controlada por la Aggregate Root.

---

## CreatedAt

Fecha y hora de creación.

Es inmutable.

---

## UpdatedAt

Fecha y hora de la última modificación válida.

---

## ConvokedAt

Fecha y hora efectiva en que la Assembly fue formalmente
convocada.

Puede ser nula antes de alcanzar Convoked.

---

## StartedAt

Fecha y hora efectiva de inicio.

Puede ser nula antes de InProgress.

---

## CompletedAt

Fecha y hora efectiva de finalización.

Puede ser nula antes de Completed.

---

## CancelledAt

Fecha y hora de cancelación.

Puede ser nula mientras la Assembly no se encuentre Cancelled.

---

## ArchivedAt

Fecha y hora de archivado.

Puede ser nula mientras la Assembly no se encuentre Archived.

---

## Version

Número de versión utilizado para concurrencia optimista.

Toda modificación válida incrementa Version.

---

# Entidades Internas

El Aggregate puede contener entidades internas cuando estas
posean identidad local dentro del límite de consistencia de
Assembly.

Ejemplos conceptuales:

```text
Convocation

AssemblyRule
```

Una entidad interna:

* pertenece exclusivamente a Assembly;
* no existe independientemente fuera del Aggregate;
* no constituye una Aggregate Root;
* no puede modificarse directamente desde fuera;
* no puede persistirse como un Aggregate independiente.

Los conceptos sin identidad local deben modelarse
preferentemente mediante Value Objects.

---

# Value Objects

Entre los Value Objects del Aggregate se consideran:

```text
AssemblyName

AssemblyType

AssemblyPurpose

AssemblyDescription

AssemblySchedule

AssemblyModality

AssemblyLocation

ConvocationStatus

ConvocationMethod

ExecutionConditions

AssemblyRules

AssemblyStatus
```

Los identificadores relacionados pueden utilizar Value Objects
del Shared Kernel:

```text
AssemblyId

OrganizationId

TerritoryId
```

Todos los Value Objects son inmutables.

No poseen ciclo de vida independiente.

---

# Estados

```text
Draft

Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

Toda transición de estado es controlada exclusivamente por la
Aggregate Root.

---

# Definición de Estados

## Draft

Representa una Assembly creada pero todavía no formalmente
programada.

En este estado puede prepararse la información necesaria para la
reunión.

---

## Scheduled

Representa una Assembly que posee una programación formal
válida.

La reunión todavía puede no haber sido convocada.

---

## Convoked

Representa una Assembly formalmente convocada.

Debe existir información de convocatoria válida conforme a las
reglas del dominio.

---

## InProgress

Representa una Assembly que ha comenzado formalmente.

Debe existir:

```text
StartedAt
```

---

## Completed

Representa una Assembly finalizada correctamente.

Debe existir:

```text
CompletedAt
```

Una Assembly Completed no vuelve a InProgress mediante una
transición ordinaria.

---

## Cancelled

Representa una Assembly cuya realización fue cancelada.

Debe existir:

```text
CancelledAt
```

Una Assembly Cancelled no puede iniciar posteriormente mediante
una operación ordinaria.

---

## Archived

Representa una Assembly retirada del ciclo operativo.

Debe existir:

```text
ArchivedAt
```

El archivado conserva la identidad y la trazabilidad histórica.

---

# Transiciones Permitidas

El flujo principal es:

```text
Draft
    ↓
Scheduled
    ↓
Convoked
    ↓
InProgress
    ↓
Completed
    ↓
Archived
```

Las transiciones de cancelación permitidas conceptualmente son:

```text
Draft
    ↓
Cancelled

Scheduled
    ↓
Cancelled

Convoked
    ↓
Cancelled
```

Una Assembly Cancelled puede posteriormente alcanzar:

```text
Archived
```

No existen transiciones directas que omitan estados cuando las
reglas del dominio exijan completar los estados intermedios.

La definición formal de las transiciones pertenece a:

```text
DOMAIN-006B-State-Machine.md
```

---

# Invariantes

Siempre deben cumplirse, como mínimo, las siguientes reglas:

* existe exactamente un AssemblyId;
* AssemblyId nunca cambia;
* toda Assembly pertenece exactamente a una Organization;
* OrganizationId es obligatorio;
* OrganizationId es inmutable;
* AssemblyName debe ser válido;
* AssemblyType debe ser válido;
* AssemblyStatus debe ser válido;
* ScheduledStartAt debe ser válido cuando la Assembly esté
  programada;
* ScheduledEndAt, cuando exista, debe ser posterior a
  ScheduledStartAt;
* TimeZone debe ser válido cuando exista programación temporal;
* AssemblyModality debe ser válida;
* AssemblyLocation debe ser compatible con la modalidad cuando
  corresponda;
* una Assembly no puede iniciar sin satisfacer sus condiciones
  de realización;
* una Assembly no puede finalizar antes de haber iniciado;
* una Assembly Completed no puede regresar a InProgress;
* una Assembly Cancelled no puede iniciar;
* una Assembly Archived no admite modificaciones ordinarias;
* todo cambio de estado debe respetar la State Machine;
* toda modificación válida incrementa Version;
* Assembly nunca modifica directamente otro Aggregate;
* Assembly nunca contiene otros Aggregates completos.

Las invariantes completas se desarrollan en:

```text
DOMAIN-006E-Invariants.md
```

---

# Operaciones Públicas

Assembly expone únicamente comportamiento de dominio.

Ejemplos:

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

El Aggregate nunca expone setters públicos.

No se permiten operaciones genéricas como:

```text
setStatus()

setValue()

updateEverything()

forceState()
```

Toda modificación debe expresar una intención concreta del
dominio.

---

# Commands

Assembly responde a Commands como:

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

Los Commands representan intenciones.

No representan hechos consumados.

La definición formal se desarrolla en:

```text
DOMAIN-006C-Commands.md
```

---

# Eventos del Dominio

El Aggregate puede publicar eventos como:

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

Todos representan hechos consumados.

La definición formal se desarrolla en:

```text
DOMAIN-006D-Domain-Events.md
```

---

# Relaciones

Assembly mantiene relaciones exclusivamente mediante
identificadores.

Ejemplos:

```text
OrganizationId

TerritoryId

CitizenId

MembershipId

RoleId

ProposalId

ParticipationId

VotingId

DocumentId

NotificationId

AuditId
```

Nunca mantiene referencias directas a otros Aggregates.

La existencia de un identificador asociado no implica que dicho
Aggregate pertenezca al límite de consistencia de Assembly.

---

# Relación con Organization

Cada Assembly pertenece exactamente a una Organization.

La relación se representa mediante:

```text
OrganizationId
```

Assembly no administra:

* identidad de Organization;
* estado de Organization;
* configuración;
* políticas;
* ciclo de vida.

---

# Relación con Territory

Assembly puede asociarse a un Territory mediante:

```text
TerritoryId
```

Territory proporciona contexto geográfico.

Assembly no administra:

* geometría;
* jerarquía territorial;
* códigos administrativos;
* estado de Territory.

---

# Relación con Citizen

Los Citizens pueden participar en procesos relacionados con una
Assembly.

Assembly puede ser referenciada junto con:

```text
CitizenId
```

en Aggregates o procesos de participación.

Assembly no administra Citizen.

---

# Relación con Membership

Membership representa la relación formal entre Citizen y
Organization.

Assembly no administra Membership.

Cuando una regla necesite verificar pertenencia organizacional,
la coordinación debe realizarse fuera del límite de consistencia
de Assembly.

---

# Relación con Role

Role puede participar en reglas de autorización o
responsabilidad organizacional relacionadas con Assembly.

Assembly no administra Role.

---

# Relación con Proposal

Una Proposal puede ser presentada, tratada o deliberada dentro
del contexto de una Assembly.

La asociación puede utilizar:

```text
AssemblyId
```

o:

```text
ProposalId
```

según el Aggregate responsable de la referencia.

Proposal conserva su propia identidad, ciclo de vida,
invariantes, Repository y Domain Events.

---

# Relación con Participation

Participation representa la participación dentro de procesos del
ecosistema AURA.

Una Participation puede utilizar AssemblyId para establecer el
contexto de reunión.

Assembly no administra el ciclo de vida de Participation.

---

# Relación con Voting

Voting puede desarrollarse dentro del contexto de una Assembly.

Voting mantiene:

* identidad propia;
* estado propio;
* reglas propias;
* participantes;
* opciones;
* resultados;
* invariantes propias.

Assembly no ejecuta internamente la votación.

---

# Relación con Document

Documents pueden asociarse a una Assembly.

Ejemplos:

* convocatoria;
* tabla;
* antecedentes;
* acta;
* anexos;
* resoluciones.

Assembly no almacena ni administra el contenido documental.

---

# Relación con Notification

Los eventos de Assembly pueden producir procesos de
Notification.

Ejemplos:

```text
AssemblyConvoked

AssemblyRescheduled

AssemblyCancelled
```

Assembly no envía Notifications directamente.

---

# Relación con Audit

Los cambios relevantes de Assembly pueden ser registrados por
Audit.

Assembly produce hechos de dominio.

Audit conserva su propio límite de consistencia.

---

# Límites del Aggregate

Assembly administra exclusivamente los conceptos que requieren
consistencia inmediata para representar la reunión.

Dentro del límite se encuentran conceptualmente:

```text
Assembly
    ├── AssemblyId
    ├── OrganizationId
    ├── TerritoryId
    ├── AssemblyName
    ├── AssemblyType
    ├── AssemblyPurpose
    ├── AssemblyDescription
    ├── AssemblySchedule
    ├── AssemblyModality
    ├── AssemblyLocation
    ├── Convocation
    ├── AssemblyRules
    ├── ExecutionConditions
    ├── AssemblyStatus
    └── Version
```

Fuera del límite se encuentran:

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

La relación contextual con Assembly nunca implica composición de
estos Aggregates.

---

# Regla de No Absorción

Assembly no absorbe otros Aggregates por el solo hecho de que sus
procesos ocurran durante una reunión.

Conceptualmente:

```text
Assembly
    ├──────── Proposal
    ├──────── Participation
    ├──────── Voting
    └──────── Document
```

representa relaciones entre Aggregates.

No representa:

```text
Assembly
    └── Proposal
        └── Participation
            └── Voting
                └── Document
```

Proposal, Participation, Voting y Document mantienen:

* identidad independiente;
* ciclo de vida independiente;
* invariantes independientes;
* Repository independiente;
* Domain Events propios;
* límites de consistencia propios.

---

# Consistencia

Toda modificación de Assembly ocurre dentro de una única
transacción lógica del Aggregate.

Al finalizar una operación válida:

* todas las invariantes deben cumplirse;
* el estado debe ser válido;
* los timestamps deben ser coherentes;
* Version debe representar la nueva versión;
* los Domain Events resultantes deben corresponder a hechos
  realmente ocurridos.

No existen actualizaciones parciales.

---

# Consistencia entre Aggregates

La coordinación con otros Aggregates utiliza consistencia
eventual.

Assembly no mantiene una transacción distribuida con:

```text
Organization

Territory

Citizen

Membership

Role

Proposal

Participation

Voting

Document

Notification

Audit
```

La interacción se realiza mediante:

* identificadores;
* Domain Events;
* Integration Events;
* Application Services;
* Process Managers;
* políticas de dominio cuando corresponda.

---

# Persistencia

El Repository persiste Assembly como una unidad.

Nunca se persisten entidades internas como Aggregates
independientes cuando pertenecen al mismo límite de consistencia.

El modelo de persistencia no define el modelo de dominio.

Assembly no conoce:

* tablas;
* colecciones;
* SQL;
* MongoDB;
* PostgreSQL;
* ORM;
* drivers;
* mecanismos físicos de almacenamiento.

---

# Repository

El Repository Contract representa la abstracción mediante la cual
Assembly puede ser recuperada y persistida.

Conceptualmente:

```text
AssemblyRepository
```

Puede proporcionar operaciones como:

```text
save(Assembly)

findById(AssemblyId)

existsById(AssemblyId)
```

La definición formal se desarrolla en:

```text
DOMAIN-006G-Repository-Contract.md
```

El Repository no contiene las invariantes de Assembly.

Las reglas del dominio permanecen dentro del Aggregate.

---

# Versionado

Assembly utiliza Versionado Optimista.

Cada modificación válida incrementa:

```text
Version
```

Version:

* nunca disminuye;
* no puede modificarse arbitrariamente;
* permite detectar conflictos de concurrencia;
* forma parte del estado técnico necesario para preservar la
  consistencia del Aggregate.

El Repository valida la versión esperada antes de persistir.

La definición formal se desarrolla en:

```text
DOMAIN-006I-Versioning.md
```

---

# Seguridad

Assembly no administra autenticación.

Assembly nunca almacena:

* contraseñas;
* tokens;
* JWT;
* certificados privados;
* claves privadas;
* secretos criptográficos;
* sesiones;
* credenciales externas.

La autenticación pertenece al Bounded Context correspondiente.

La autorización determina quién puede solicitar una operación.

Assembly determina si dicha operación es válida según las
invariantes del dominio.

---

# Permisos

Las capacidades necesarias para operar sobre Assembly se
desarrollan formalmente en:

```text
DOMAIN-006F-Permissions.md
```

Conceptualmente pueden existir permisos como:

```text
Assembly.Create

Assembly.View

Assembly.Update

Assembly.Schedule

Assembly.Convoke

Assembly.Start

Assembly.Complete

Assembly.Cancel

Assembly.Archive
```

Assembly no implementa mecanismos técnicos de autorización.

No depende de:

* OAuth;
* JWT;
* middleware;
* PEP Proxy;
* sistemas externos de identidad.

---

# Auditoría

Assembly publica hechos relevantes que pueden ser consumidos por
Audit.

Ejemplos:

```text
AssemblyCreated

AssemblyScheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted

AssemblyCancelled

AssemblyArchived
```

Assembly no mantiene registros Audit como entidades internas.

La auditoría constituye una responsabilidad independiente.

---

# Integración

Assembly puede participar en integraciones con:

* plataformas municipales;
* plataformas de participación ciudadana;
* sistemas Smart City;
* sistemas territoriales;
* sistemas documentales;
* sistemas de notificación;
* plataformas de transparencia;
* FIWARE;
* otros sistemas externos.

Las integraciones no acceden directamente al estado interno del
Aggregate.

---

# Integration Events

Los Domain Events relevantes pueden transformarse en Integration
Events.

Ejemplos conceptuales:

```text
AssemblyCreatedIntegrationEvent

AssemblyScheduledIntegrationEvent

AssemblyConvokedIntegrationEvent

AssemblyStartedIntegrationEvent

AssemblyCompletedIntegrationEvent

AssemblyCancelledIntegrationEvent

AssemblyArchivedIntegrationEvent
```

La definición formal se desarrolla en:

```text
DOMAIN-006K-Integration-Events.md
```

Los Integration Events pertenecen a la frontera del Bounded
Context y no sustituyen a los Domain Events internos.

---

# FIWARE

Assembly puede proyectarse hacia FIWARE cuando AURA necesite
representar reuniones organizacionales o comunitarias dentro de
un ecosistema Smart City.

El flujo conceptual es:

```text
Assembly
    │
    │ Domain Event
    ▼
Application Layer
    │
    │ Integration Event
    ▼
Integration Adapter
    │
    ▼
FIWARE
```

Assembly no depende directamente de:

* NGSI-LD;
* Context Broker;
* Orion;
* HTTP;
* OAuth;
* PEP Proxy.

La representación FIWARE es una proyección de integración y no
constituye la fuente de verdad del Aggregate.

---

# Read Model

Assembly puede proyectarse hacia modelos especializados de
lectura.

Ejemplos:

```text
AssemblyCalendar

AssemblyDirectory

AssemblyPublicView

AssemblyTimeline

AssemblyTerritorialView

AssemblyGovernanceView
```

Los Read Models pueden contener información derivada como:

```text
AssemblyId

OrganizationId

TerritoryId

AssemblyName

AssemblyType

AssemblyPurpose

ScheduledStartAt

ScheduledEndAt

AssemblyModality

AssemblyLocation

AssemblyStatus
```

El Read Model no modifica el Aggregate.

La especificación formal se desarrolla en:

```text
DOMAIN-006L-Read-Model.md
```

---

# CQRS

Assembly es compatible con CQRS.

El lado de escritura utiliza:

```text
Assembly
```

como modelo de consistencia.

El lado de lectura utiliza Read Models especializados.

Los Commands modifican el Aggregate.

Las Queries consultan proyecciones.

Nunca se utiliza un Read Model para evitar la ejecución de las
invariantes del Aggregate.

---

# Event Sourcing

Assembly es compatible conceptualmente con Event Sourcing.

Los cambios de estado pueden expresarse mediante eventos como:

```text
AssemblyCreated

AssemblyScheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted
```

La compatibilidad con Event Sourcing no obliga a utilizarlo como
mecanismo de persistencia.

El modelo de dominio permanece independiente de esa decisión de
infraestructura.

---

# Dependencias

Assembly depende únicamente de conceptos del dominio y del
Shared Kernel.

Puede utilizar:

* identificadores;
* Value Objects;
* Domain Events;
* Domain Rules;
* Repository Contracts.

Nunca depende de:

* Infrastructure;
* Frameworks;
* Bases de datos;
* HTTP;
* REST;
* GraphQL;
* OAuth;
* JWT;
* React;
* Next.js;
* FastAPI;
* Django;
* FIWARE;
* MongoDB;
* PostgreSQL.

---

# Reglas de Diseño

Assembly cumple las siguientes reglas:

* una única Aggregate Root;
* AssemblyId único e inmutable;
* OrganizationId obligatorio e inmutable;
* límite de consistencia explícito;
* Value Objects inmutables;
* comportamiento orientado al dominio;
* ausencia de setters públicos;
* invariantes protegidas internamente;
* referencias externas mediante identificadores;
* ninguna referencia directa a otros Aggregates completos;
* persistencia mediante Repository;
* Versionado Optimista;
* Domain Events para hechos relevantes;
* Integration Events en la frontera;
* consistencia fuerte dentro del Aggregate;
* consistencia eventual entre Aggregates;
* alta cohesión;
* bajo acoplamiento;
* independencia tecnológica.

---

# Casos de Uso

Ejemplos:

```text
Crear una nueva Asamblea.

Programar una Asamblea.

Reprogramar una Asamblea.

Convocar formalmente una Asamblea.

Cambiar el nombre de una Asamblea.

Cambiar el tipo de Asamblea.

Cambiar el propósito de una Asamblea.

Modificar su descripción.

Cambiar la modalidad.

Cambiar la ubicación.

Actualizar las reglas propias de la Asamblea.

Actualizar las condiciones de realización.

Iniciar una Asamblea.

Finalizar una Asamblea.

Cancelar una Asamblea.

Archivar una Asamblea.
```

Los casos de uso coordinan el Aggregate mediante Commands.

No modifican directamente su estado interno.

---

# Restricciones

No está permitido:

* modificar AssemblyId;
* modificar OrganizationId;
* modificar Status directamente;
* modificar Version directamente;
* utilizar setters públicos;
* modificar entidades internas desde fuera del Aggregate;
* almacenar Aggregates externos dentro de Assembly;
* modificar Organization desde Assembly;
* modificar Territory desde Assembly;
* modificar Citizen desde Assembly;
* modificar Membership desde Assembly;
* modificar Role desde Assembly;
* modificar Proposal desde Assembly;
* modificar Participation desde Assembly;
* modificar Voting desde Assembly;
* modificar Document desde Assembly;
* modificar Notification desde Assembly;
* modificar Audit desde Assembly;
* iniciar una Assembly desde un estado inválido;
* finalizar una Assembly desde un estado inválido;
* reactivar una Assembly Completed;
* reactivar una Assembly Cancelled mediante una operación
  ordinaria;
* modificar una Assembly Archived;
* mantener una programación temporal inválida;
* introducir dependencias de Infrastructure;
* introducir dependencias de Frameworks;
* ejecutar acceso a base de datos desde el Aggregate;
* ejecutar llamadas HTTP desde el Aggregate.

---

# Extensibilidad

Assembly puede evolucionar mediante puntos de extensión
controlados.

Ejemplos conceptuales:

```text
NewAssemblyType

NewAssemblyModality

NewConvocationRule

NewExecutionCondition

NewAssemblyRule

NewDomainEvent

NewIntegrationEvent

NewReadModelProjection
```

Los puntos de extensión se desarrollan en:

```text
DOMAIN-006P-Extension-Points.md
```

La extensibilidad no permite alterar silenciosamente los límites
fundamentales del Aggregate.

---

# Criterios de Evolución

Una nueva capacidad puede incorporarse dentro de Assembly
solamente cuando:

* pertenece conceptualmente a la reunión;
* requiere consistencia inmediata con Assembly;
* no posee identidad global independiente;
* no posee ciclo de vida independiente;
* no posee invariantes independientes;
* no pertenece claramente a otro Aggregate.

Cuando un concepto posee:

* identidad propia;
* ciclo de vida propio;
* invariantes propias;
* Repository propio;
* consistencia independiente;

debe evaluarse como Aggregate separado.

La conveniencia técnica no determina los límites del Aggregate.

---

# Fuente de Verdad

Assembly constituye la fuente de verdad transaccional para el
estado de una reunión.

Los siguientes elementos son representaciones derivadas:

```text
Read Models

Integration Events

FIWARE Entities

HTTP DTOs

Persistence Models
```

Ninguno de ellos sustituye al Aggregate.

Las invariantes únicamente pueden protegerse mediante el modelo
de dominio oficial.

---

# Beneficios

Este diseño proporciona:

* representación formal y consistente de reuniones;
* identidad estable mediante AssemblyId;
* separación entre reunión y procesos asociados;
* independencia respecto de otros Aggregates;
* consistencia transaccional dentro del límite;
* trazabilidad mediante Domain Events;
* control de concurrencia mediante Version;
* compatibilidad con CQRS;
* compatibilidad con Event Sourcing;
* interoperabilidad mediante Integration Events;
* integración con ecosistemas Smart City;
* independencia tecnológica;
* evolución controlada;
* alta cohesión;
* bajo acoplamiento.

---

# Documentación Derivada

Este documento constituye la definición conceptual principal del
Aggregate Assembly.

Los siguientes documentos desarrollan formalmente dimensiones
específicas del Aggregate:

```text
DOMAIN-006A-Lifecycle.md

DOMAIN-006B-State-Machine.md

DOMAIN-006C-Commands.md

DOMAIN-006D-Domain-Events.md

DOMAIN-006E-Invariants.md

DOMAIN-006F-Permissions.md

DOMAIN-006G-Repository-Contract.md

DOMAIN-006H-Examples.md

DOMAIN-006I-Versioning.md

DOMAIN-006J-Consistency-Boundary.md

DOMAIN-006K-Integration-Events.md

DOMAIN-006L-Read-Model.md

DOMAIN-006M-Test-Scenarios.md

DOMAIN-006N-Performance-Rules.md

DOMAIN-006O-Security-Model.md

DOMAIN-006P-Extension-Points.md
```

Todos los documentos derivados deben preservar la identidad,
responsabilidades, límites, invariantes y reglas conceptuales
establecidas en DOMAIN-006-Aggregate.md.

---

# Definición de Éxito

El Aggregate **Assembly** representa de forma consistente y
oficial una instancia formal de reunión dentro del ecosistema
AURA.

Centraliza la identidad, contexto organizacional, contexto
territorial cuando corresponda, clasificación, propósito,
programación, modalidad, convocatoria, condiciones de
realización, estado y ciclo de vida de una reunión.

Assembly protege sus invariantes mediante una única Aggregate
Root, mantiene consistencia fuerte dentro de su propio límite y
colabora con otros Aggregates exclusivamente mediante
identificadores, Domain Events e Integration Events.

Los procesos de Proposal, Participation, Voting, Document,
Notification y Audit pueden relacionarse con una Assembly sin
ser absorbidos por ella, conservando sus propias identidades,
reglas, ciclos de vida e invariantes.

De esta forma, Assembly proporciona una base consistente,
trazable, desacoplada, interoperable y preparada para una
arquitectura distribuida basada en Domain-Driven Design.
