# DOMAIN-007C — Proposal Commands

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Proposal Management

Aggregate:
Proposal

Autor:
ARADA

Documentos relacionados:

- DOMAIN-007-Aggregate.md
- DOMAIN-007A-Lifecycle.md
- DOMAIN-007B-State-Machine.md
- DOMAIN-007D-Domain-Events.md
- DOMAIN-007E-Invariants.md
- DOMAIN-007F-Permissions.md
- DOMAIN-007J-Consistency-Boundary.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir los Commands oficiales que representan la intención de
crear o modificar el estado del Aggregate **Proposal**.

Un Command expresa una solicitud explícita de cambio sobre una
Proposal.

Un Command:

- representa intención;
- no representa un hecho consumado;
- no garantiza su ejecución;
- no modifica directamente la persistencia;
- no constituye un Domain Event;
- no constituye un Integration Event;
- no constituye un Read Model;
- no sustituye las invariantes del Aggregate.

Todo Command debe ser evaluado por el Aggregate antes de producir
una modificación válida.

---

# Propósito

Los Commands constituyen el mecanismo conceptual mediante el cual
un actor solicita cambios sobre Proposal.

El flujo conceptual es:

```text
Actor

↓

Command

↓

Authorization

↓

Proposal Aggregate

↓

State Machine

↓

Invariants

↓

State Change

↓

Domain Events
```

La recepción de un Command no implica que el Aggregate deba
aceptarlo.

Proposal conserva la autoridad final para determinar si la
operación solicitada es válida.

---

# Principios

Todos los Commands de Proposal deben cumplir los siguientes
principios:

- representan una intención explícita;
- poseen semántica de dominio;
- son inmutables;
- poseen identidad propia;
- son auditables;
- identifican el Aggregate objetivo;
- identifican el actor cuando corresponda;
- modifican exclusivamente un Proposal Aggregate;
- respetan la State Machine;
- respetan las invariantes;
- respetan Permissions;
- respetan Versioning;
- pueden producir uno o más Domain Events;
- nunca representan hechos consumados;
- nunca retornan el estado mutable del Aggregate;
- nunca modifican directamente otros Aggregates.

---

# Command

Un Command representa una solicitud para ejecutar una operación
de dominio.

Conceptualmente:

```text
Command
    =
Intent
```

No:

```text
Command
    =
Fact
```

Por ejemplo:

```text
SubmitProposal
```

representa la intención de presentar una Proposal.

El hecho consumado correspondiente puede ser:

```text
ProposalSubmitted
```

únicamente después de que el Aggregate haya aceptado y ejecutado
válidamente la operación.

---

# Command y Domain Event

Commands y Domain Events poseen responsabilidades diferentes.

```text
Command
    ↓
Intent
```

```text
Domain Event
    ↓
Fact
```

Ejemplo:

```text
AcceptProposal
```

no significa que Proposal haya sido aceptada.

Solo después de una operación válida puede producirse:

```text
ProposalAccepted
```

Debe mantenerse:

```text
Command
    ≠
Domain Event
```

---

# Command y Integration Event

Un Command tampoco constituye un Integration Event.

Debe mantenerse:

```text
Command

↓

Aggregate

↓

Domain Event

↓

Integration Event
```

No:

```text
Command

↓

Integration Event

↓

Aggregate
```

Los Integration Events se desarrollarán formalmente en:

```text
DOMAIN-007K-Integration-Events.md
```

---

# Command y Estado

Un Command puede solicitar una transición de estado.

No puede asignar directamente:

```text
ProposalStatus
```

No debe existir un mecanismo genérico como:

```text
SetProposalStatus
```

Las operaciones deben expresar intención mediante lenguaje de
dominio.

Ejemplos:

```text
SubmitProposal

StartProposalReview

AcceptProposal

RejectProposal

WithdrawProposal

ArchiveProposal
```

---

# Estructura General

Todo Command debe contener, como mínimo, la información necesaria
para identificar:

```text
CommandId

ProposalId

OrganizationId

ActorId

Timestamp

ExpectedVersion

CorrelationId

CausationId
```

Campos adicionales deben incorporarse únicamente cuando sean
necesarios para expresar la intención específica del Command.

---

# CommandId

Identifica de forma única la instancia del Command.

```text
CommandId
```

Debe permitir distinguir solicitudes diferentes incluso cuando
apunten al mismo ProposalId.

CommandId:

- es inmutable;
- pertenece al Command;
- no constituye ProposalId;
- permite trazabilidad;
- permite correlación operativa;
- puede participar en mecanismos de idempotencia.

---

# ProposalId

Identifica el Aggregate objetivo.

```text
ProposalId
```

Todo Command dirigido a una Proposal existente debe identificar
inequívocamente el Aggregate sobre el cual se solicita la
operación.

ProposalId no puede modificarse mediante un Command.

---

# OrganizationId

Identifica el contexto organizacional al cual pertenece la
Proposal.

```text
OrganizationId
```

OrganizationId permite preservar el contexto organizacional de la
operación.

El Command no puede utilizar OrganizationId para transferir una
Proposal entre Organizations.

---

# ActorId

Identifica al actor que solicita la operación.

```text
ActorId
```

ActorId permite:

- autorización;
- trazabilidad;
- auditoría;
- atribución de intención.

ActorId no convierte al actor en parte del Aggregate Proposal.

---

# Timestamp

Representa el instante asociado a la solicitud.

```text
Timestamp
```

Timestamp no debe utilizarse para eludir las reglas temporales del
Aggregate.

El tiempo asociado al Command no determina por sí mismo que la
operación sea válida.

---

# ExpectedVersion

Representa la versión del Aggregate sobre la cual el emisor espera
ejecutar la operación.

```text
ExpectedVersion
```

Permite proteger Proposal frente a modificaciones concurrentes.

Debe mantenerse:

```text
ExpectedVersion
    =
CurrentVersion
```

antes de confirmar una modificación.

El modelo formal se desarrolla en:

```text
DOMAIN-007I-Versioning.md
```

---

# CorrelationId

Permite relacionar el Command con un flujo lógico mayor.

```text
CorrelationId
```

Puede utilizarse para mantener trazabilidad entre:

- Commands;
- Domain Events;
- Integration Events;
- procesos distribuidos;
- auditoría.

CorrelationId no modifica la semántica de dominio de Proposal.

---

# CausationId

Permite identificar la causa inmediata que originó el Command.

```text
CausationId
```

Puede referenciar conceptualmente:

- otro Command;
- un Domain Event;
- un Integration Event;
- una acción externa autorizada.

CausationId no sustituye CommandId.

---

# Commands Oficiales

Los Commands oficiales del Aggregate Proposal son:

```text
CreateProposal

RenameProposal

ChangeProposalPurpose

ChangeProposalDescription

ChangeProposalType

UpdateProposalContent

ChangeProposalTerritory

AssociateProposalAssembly

SubmitProposal

StartProposalReview

AcceptProposal

RejectProposal

WithdrawProposal

ArchiveProposal
```

Cada Command expresa una intención específica.

No existe un Command genérico para modificar arbitrariamente el
Aggregate.

---

# CreateProposal

## Objetivo

Crear una nueva Proposal dentro del contexto de una Organization.

## Datos mínimos

```text
CommandId

ProposalId

OrganizationId

ActorId

ProposalName

ProposalType

ProposalPurpose

Timestamp

CorrelationId

CausationId
```

Los datos adicionales requeridos dependen de las reglas
conceptuales establecidas en:

```text
DOMAIN-007-Aggregate.md
```

## Precondiciones

- ProposalId es válido;
- no existe otra Proposal con el mismo ProposalId;
- OrganizationId es válido;
- el contexto organizacional es válido;
- ProposalName satisface las reglas del dominio;
- ProposalType es válido;
- ProposalPurpose satisface las reglas del dominio;
- el actor posee Permission de creación;
- las invariantes iniciales pueden satisfacerse.

## Estado origen

No aplica.

Conceptualmente:

```text
Nonexistent
```

`Nonexistent` no constituye un ProposalStatus.

## Estado destino

```text
Draft
```

## Evento esperado

```text
ProposalCreated
```

## Resultado

La creación válida establece una nueva Proposal en:

```text
Draft
```

con identidad propia y Version inicial conforme al modelo de
Versioning.

---

# RenameProposal

## Objetivo

Modificar el nombre de una Proposal.

## Datos

```text
ProposalName
```

## Estados permitidos

```text
Draft
```

## Precondiciones

- Proposal existe;
- ProposalStatus es Draft;
- ProposalName es válido;
- el nuevo nombre satisface las invariantes;
- el actor posee Permission;
- ExpectedVersion coincide con CurrentVersion.

## Evento esperado

```text
ProposalRenamed
```

## Restricciones

RenameProposal no modifica:

```text
ProposalId

OrganizationId

ProposalStatus
```

---

# ChangeProposalPurpose

## Objetivo

Modificar el propósito formal de una Proposal.

## Datos

```text
ProposalPurpose
```

## Estados permitidos

```text
Draft
```

## Precondiciones

- Proposal existe;
- ProposalStatus es Draft;
- ProposalPurpose es válido;
- las invariantes permanecen satisfechas;
- el actor posee Permission;
- ExpectedVersion coincide con CurrentVersion.

## Evento esperado

```text
ProposalPurposeChanged
```

---

# ChangeProposalDescription

## Objetivo

Modificar la descripción de una Proposal.

## Datos

```text
ProposalDescription
```

## Estados permitidos

```text
Draft
```

## Precondiciones

- Proposal existe;
- ProposalStatus es Draft;
- la descripción satisface las reglas del dominio;
- el actor posee Permission;
- ExpectedVersion coincide con CurrentVersion;
- las invariantes permanecen válidas.

## Evento esperado

```text
ProposalDescriptionChanged
```

---

# ChangeProposalType

## Objetivo

Modificar la clasificación conceptual de una Proposal.

## Datos

```text
ProposalType
```

## Estados permitidos

```text
Draft
```

## Precondiciones

- Proposal existe;
- ProposalStatus es Draft;
- ProposalType pertenece al conjunto válido;
- el cambio no viola invariantes;
- el actor posee Permission;
- ExpectedVersion coincide con CurrentVersion.

## Evento esperado

```text
ProposalTypeChanged
```

## Restricciones

ChangeProposalType no crea un nuevo Aggregate.

La identidad permanece:

```text
ProposalId
```

---

# UpdateProposalContent

## Objetivo

Actualizar el contenido propio de una Proposal mientras el
Lifecycle permita su edición.

## Datos

```text
ProposalContent
```

La estructura concreta de ProposalContent debe corresponder al
modelo conceptual definido para Proposal.

## Estados permitidos

```text
Draft
```

## Precondiciones

- Proposal existe;
- ProposalStatus es Draft;
- el contenido es válido;
- el contenido pertenece al límite de Proposal;
- no se incorporan otros Aggregates como entidades internas;
- el actor posee Permission;
- ExpectedVersion coincide con CurrentVersion;
- las invariantes permanecen satisfechas.

## Evento esperado

```text
ProposalContentUpdated
```

---

# ChangeProposalTerritory

## Objetivo

Modificar la referencia territorial de una Proposal cuando el
modelo permita contexto territorial.

## Datos

```text
TerritoryId
```

## Estados permitidos

```text
Draft
```

## Precondiciones

- Proposal existe;
- ProposalStatus es Draft;
- TerritoryId es válido cuando sea requerido;
- la referencia territorial es compatible con el contexto de
  Proposal;
- el actor posee Permission;
- ExpectedVersion coincide con CurrentVersion;
- las invariantes permanecen válidas.

## Evento esperado

```text
ProposalTerritoryChanged
```

## Restricciones

ChangeProposalTerritory no modifica el Aggregate Territory.

Debe mantenerse:

```text
Proposal

↓

TerritoryId
```

No:

```text
Proposal

↓

Mutable Territory Aggregate
```

---

# AssociateProposalAssembly

## Objetivo

Asociar una Proposal con una Assembly cuando la Proposal deba
mantener contexto formal de reunión.

## Datos

```text
AssemblyId
```

## Estados permitidos

```text
Draft
```

## Precondiciones

- Proposal existe;
- ProposalStatus es Draft;
- AssemblyId es válido;
- la asociación satisface las reglas del dominio;
- el actor posee Permission;
- ExpectedVersion coincide con CurrentVersion;
- las invariantes permanecen válidas.

## Evento esperado

```text
ProposalAssemblyAssociated
```

## Restricciones

AssociateProposalAssembly:

- no modifica Assembly;
- no incorpora Assembly dentro del Aggregate Proposal;
- no modifica AssemblyStatus;
- no transfiere responsabilidad de Proposal hacia Assembly.

La relación se mantiene mediante:

```text
AssemblyId
```

---

# SubmitProposal

## Objetivo

Presentar formalmente una Proposal que se encuentra en Draft.

## Estado origen

```text
Draft
```

## Estado destino

```text
Submitted
```

## Precondiciones

- Proposal existe;
- ProposalStatus es Draft;
- los datos obligatorios están completos;
- ProposalType es válido;
- ProposalName es válido;
- ProposalPurpose es válido;
- ProposalContent satisface las reglas requeridas;
- las referencias obligatorias son válidas;
- el actor posee Permission;
- las invariantes de presentación se cumplen;
- ExpectedVersion coincide con CurrentVersion.

## Evento esperado

```text
ProposalSubmitted
```

## Resultado

```text
Draft

↓

Submitted
```

La transición debe respetar:

```text
DOMAIN-007B-State-Machine.md
```

---

# StartProposalReview

## Objetivo

Iniciar formalmente el proceso de revisión de una Proposal
presentada.

## Estado origen

```text
Submitted
```

## Estado destino

```text
UnderReview
```

## Precondiciones

- Proposal existe;
- ProposalStatus es Submitted;
- la presentación permanece válida;
- se cumplen las condiciones necesarias para iniciar revisión;
- el actor posee Permission;
- las invariantes permanecen válidas;
- ExpectedVersion coincide con CurrentVersion.

## Evento esperado

```text
ProposalReviewStarted
```

## Resultado

```text
Submitted

↓

UnderReview
```

---

# AcceptProposal

## Objetivo

Aceptar formalmente una Proposal que se encuentra en proceso de
revisión.

## Estado origen

```text
UnderReview
```

## Estado destino

```text
Accepted
```

## Precondiciones

- Proposal existe;
- ProposalStatus es UnderReview;
- las condiciones de aceptación están satisfechas;
- las reglas de decisión aplicables se cumplen;
- el actor posee Permission;
- las invariantes permanecen válidas;
- ExpectedVersion coincide con CurrentVersion.

## Evento esperado

```text
ProposalAccepted
```

## Resultado

```text
UnderReview

↓

Accepted
```

## Restricciones

AcceptProposal no representa automáticamente:

- ejecución de la iniciativa;
- creación de un Voting;
- finalización de una Assembly;
- creación de un Document;
- modificación de Participation;
- modificación de Organization.

La aceptación constituye exclusivamente una decisión de dominio
sobre Proposal.

---

# RejectProposal

## Objetivo

Rechazar formalmente una Proposal que se encuentra en proceso de
revisión.

## Datos adicionales

Cuando el modelo de dominio lo requiera puede incluir:

```text
RejectionReason
```

## Estado origen

```text
UnderReview
```

## Estado destino

```text
Rejected
```

## Precondiciones

- Proposal existe;
- ProposalStatus es UnderReview;
- las condiciones de rechazo están satisfechas;
- las reglas de decisión aplicables se cumplen;
- RejectionReason es válido cuando sea obligatorio;
- el actor posee Permission;
- las invariantes permanecen válidas;
- ExpectedVersion coincide con CurrentVersion.

## Evento esperado

```text
ProposalRejected
```

## Resultado

```text
UnderReview

↓

Rejected
```

Rejected conserva:

- ProposalId;
- OrganizationId;
- trazabilidad;
- historial de eventos;
- Version.

---

# WithdrawProposal

## Objetivo

Retirar formalmente una Proposal del flujo normal.

## Datos adicionales

Cuando las reglas del dominio lo requieran puede incluir:

```text
WithdrawalReason
```

## Estados origen permitidos

```text
Draft

Submitted
```

## Estado destino

```text
Withdrawn
```

## Precondiciones

- Proposal existe;
- ProposalStatus es Draft o Submitted;
- el retiro está permitido por el Lifecycle;
- WithdrawalReason es válido cuando sea obligatorio;
- el actor posee Permission;
- las invariantes permanecen válidas;
- ExpectedVersion coincide con CurrentVersion.

## Evento esperado

```text
ProposalWithdrawn
```

## Resultados válidos

```text
Draft

↓

Withdrawn
```

o:

```text
Submitted

↓

Withdrawn
```

## Restricciones

No está permitido ejecutar WithdrawProposal desde:

```text
UnderReview

Accepted

Rejected

Archived
```

en la versión 1.0.

Withdrawn no equivale a Rejected.

---

# ArchiveProposal

## Objetivo

Archivar una Proposal cuyo flujo activo ha finalizado.

## Estados origen permitidos

```text
Accepted

Rejected

Withdrawn
```

## Estado destino

```text
Archived
```

## Precondiciones

- Proposal existe;
- ProposalStatus pertenece a los estados archivables;
- se cumplen las condiciones de archivado;
- el actor posee Permission;
- las invariantes permanecen válidas;
- ExpectedVersion coincide con CurrentVersion.

## Evento esperado

```text
ProposalArchived
```

## Resultados válidos

```text
Accepted

↓

Archived
```

```text
Rejected

↓

Archived
```

```text
Withdrawn

↓

Archived
```

## Restricciones

No está permitido ejecutar ArchiveProposal desde:

```text
Draft

Submitted

UnderReview
```

Archived constituye un estado terminal.

---

# Commands de Transición

Los Commands que producen una transición válida de
ProposalStatus son:

```text
CreateProposal

SubmitProposal

StartProposalReview

AcceptProposal

RejectProposal

WithdrawProposal

ArchiveProposal
```

Su relación con la State Machine es:

```text
Command                 From           To

CreateProposal          Nonexistent    Draft

SubmitProposal          Draft          Submitted

StartProposalReview     Submitted      UnderReview

AcceptProposal          UnderReview    Accepted

RejectProposal          UnderReview    Rejected

WithdrawProposal        Draft          Withdrawn

WithdrawProposal        Submitted      Withdrawn

ArchiveProposal         Accepted       Archived

ArchiveProposal         Rejected       Archived

ArchiveProposal         Withdrawn      Archived
```

---

# Commands sin Transición de Estado

Los siguientes Commands pueden modificar información de Proposal
sin cambiar ProposalStatus:

```text
RenameProposal

ChangeProposalPurpose

ChangeProposalDescription

ChangeProposalType

UpdateProposalContent

ChangeProposalTerritory

AssociateProposalAssembly
```

Una modificación sin transición de estado continúa siendo una
modificación del Aggregate.

Por lo tanto debe:

- validar el estado actual;
- validar Permissions;
- validar invariantes;
- validar ExpectedVersion;
- modificar únicamente información permitida;
- incrementar Version;
- producir el Domain Event correspondiente.

---

# Restricción de Edición por Estado

Las operaciones editoriales definidas en esta versión se
encuentran restringidas a:

```text
Draft
```

Debe mantenerse:

```text
Draft

↓

Editable
```

y:

```text
Submitted

UnderReview

Accepted

Rejected

Withdrawn

Archived

↓

Not Editable by Draft Commands
```

Esta regla evita modificar retroactivamente el contenido que fue
formalmente presentado, revisado o resuelto.

---

# Tabla General de Commands

```text
Command                      Allowed State        Changes State
───────────────────────────────────────────────────────────────
CreateProposal               Nonexistent          Yes

RenameProposal               Draft                No

ChangeProposalPurpose        Draft                No

ChangeProposalDescription    Draft                No

ChangeProposalType           Draft                No

UpdateProposalContent        Draft                No

ChangeProposalTerritory      Draft                No

AssociateProposalAssembly    Draft                No

SubmitProposal               Draft                Yes

StartProposalReview          Submitted            Yes

AcceptProposal               UnderReview          Yes

RejectProposal               UnderReview          Yes

WithdrawProposal             Draft                Yes

WithdrawProposal             Submitted            Yes

ArchiveProposal              Accepted             Yes

ArchiveProposal              Rejected             Yes

ArchiveProposal              Withdrawn            Yes
```

---

# Validación de Commands

Todo Command debe pasar conceptualmente por:

```text
Command Received

↓

Command Structure Validation

↓

Identity Validation

↓

Aggregate Load

↓

Current State Validation

↓

Permission Validation

↓

Command Preconditions

↓

Invariant Validation

↓

ExpectedVersion Validation

↓

Aggregate Behavior

↓

State Mutation

↓

Version Increment

↓

Domain Events
```

Una implementación puede distribuir responsabilidades entre las
capas correspondientes sin alterar el significado conceptual del
flujo.

---

# Validación Estructural

Antes de interpretar una solicitud como Command válido deben
existir los datos obligatorios definidos para su operación.

Un Command estructuralmente inválido no debe alcanzar el
comportamiento de dominio como una intención válida.

---

# Validación de Identidad

ProposalId debe identificar exactamente el Aggregate objetivo.

No está permitido utilizar un Command para modificar:

```text
ProposalId
```

ni:

```text
OrganizationId
```

cuando este último sea inmutable conforme al Aggregate.

---

# Validación de Estado

Todo Command debe ser compatible con el ProposalStatus actual.

Ejemplo:

```text
AcceptProposal
```

requiere:

```text
UnderReview
```

Si Proposal se encuentra:

```text
Draft
```

el Command debe rechazarse.

---

# Validación de Permissions

El actor debe poseer autorización para solicitar la operación.

La autorización se desarrolla formalmente en:

```text
DOMAIN-007F-Permissions.md
```

Debe mantenerse:

```text
Permission Granted
    ≠
Command Accepted
```

Una operación autorizada todavía puede ser rechazada por:

- estado;
- invariantes;
- precondiciones;
- Versioning.

---

# Validación de Invariantes

Todo Command debe preservar las invariantes definidas en:

```text
DOMAIN-007E-Invariants.md
```

No existe Command capaz de suspender o ignorar una invariante.

Debe mantenerse:

```text
Command

↓

Invariant Violation

↓

Rejected
```

---

# Validación de Version

Los Commands dirigidos a una Proposal existente deben validar:

```text
ExpectedVersion
```

contra:

```text
CurrentVersion
```

Si no coinciden:

```text
Command

↓

Concurrency Conflict

↓

Rejected
```

No debe utilizarse:

```text
Last Write Wins
```

para resolver modificaciones concurrentes de dominio.

---

# Ejecución Atómica

La aceptación de un Command debe producir una modificación
atómica dentro del Consistency Boundary de Proposal.

Conceptualmente:

```text
Validate Command

↓

Validate State

↓

Validate Permission

↓

Validate Invariants

↓

Validate Version

↓

Apply Behavior

↓

Update Proposal

↓

Increment Version

↓

Record Domain Events
```

El resultado no puede quedar parcialmente aplicado.

---

# Resultado de un Command Válido

Un Command válido puede producir:

```text
State Change
```

o:

```text
Attribute Change
```

junto con:

```text
Version Increment
```

y:

```text
Domain Event
```

cuando corresponda.

---

# Resultado de un Command Rechazado

Cuando un Command es rechazado:

```text
Proposal State
    =
Previous State
```

```text
Proposal Data
    =
Previous Valid Data
```

```text
Version
    =
Previous Version
```

```text
Success Domain Event
    =
Not Produced
```

No debe existir mutación parcial.

---

# Rechazo de Commands

El Aggregate rechazará un Command cuando ocurra cualquiera de las
siguientes situaciones:

- ProposalId no identifica un Aggregate válido;
- OrganizationId no corresponde al contexto esperado;
- el estado actual no permite la operación;
- el actor no posee Permission;
- faltan datos obligatorios;
- los datos son inválidos;
- se violan invariantes;
- ExpectedVersion no coincide;
- se intenta modificar ProposalId;
- se intenta modificar OrganizationId;
- se intenta modificar ProposalStatus directamente;
- se intenta modificar una Proposal Archived;
- se intenta utilizar un Command editorial fuera de Draft;
- se intenta omitir una transición obligatoria;
- se intenta ejecutar una transición no definida.

---

# No Command Genérico de Actualización

No debe existir un Command como:

```text
UpdateProposal
```

capaz de modificar arbitrariamente múltiples conceptos sin
expresar intención de dominio.

Las modificaciones deben expresarse mediante Commands
semánticamente explícitos.

Ejemplos:

```text
RenameProposal
```

en lugar de:

```text
UpdateProposal(name)
```

```text
ChangeProposalPurpose
```

en lugar de:

```text
UpdateProposal(purpose)
```

```text
SubmitProposal
```

en lugar de:

```text
UpdateProposal(status = Submitted)
```

---

# No SetProposalStatus

Está explícitamente prohibido definir:

```text
SetProposalStatus
```

como Command público.

ProposalStatus solo puede cambiar como consecuencia de
comportamiento de dominio válido.

---

# No DeleteProposal

La versión 1.0 no utiliza:

```text
DeleteProposal
```

como mecanismo para finalizar el ciclo de vida.

La conservación histórica se representa mediante:

```text
Archived
```

Debe mantenerse:

```text
ArchiveProposal
    ≠
DeleteProposal
```

---

# Commands y Aggregate Root

Todos los Commands modificadores deben terminar ejecutando
comportamiento sobre:

```text
Proposal
```

como Aggregate Root.

No está permitido modificar directamente:

- entidades internas;
- Value Objects internos;
- atributos persistidos;
- registros de base de datos.

---

# Commands y Repository

El Repository:

- recupera Proposal;
- persiste Proposal;
- participa en la protección de Versioning según su contrato.

El Repository no decide si un Command es válido.

No debe existir:

```text
Repository.acceptProposal()
```

como sustitución del comportamiento del Aggregate.

La secuencia conceptual correcta es:

```text
Repository

↓

Load Proposal

↓

Proposal Behavior

↓

Repository

↓

Persist Proposal
```

---

# Commands y Application Services

Application Services pueden:

- recibir solicitudes;
- construir Commands;
- resolver dependencias externas;
- coordinar autorización;
- cargar Aggregates;
- invocar comportamiento;
- persistir resultados;
- publicar eventos confirmados.

Application Services no deben:

- modificar ProposalStatus directamente;
- reproducir las invariantes del Aggregate como sustitución de
  Proposal;
- decidir unilateralmente una transición;
- modificar atributos internos directamente.

---

# Commands y Organization

Proposal pertenece al contexto de una Organization.

Un Command puede incluir:

```text
OrganizationId
```

para mantener el contexto de la operación.

No puede utilizarse un Command de Proposal para modificar
Organization.

---

# Commands y Territory

ChangeProposalTerritory puede modificar únicamente la referencia:

```text
TerritoryId
```

cuando la operación sea válida.

No puede modificar:

```text
Territory
```

como Aggregate.

---

# Commands y Assembly

AssociateProposalAssembly puede establecer una referencia:

```text
AssemblyId
```

cuando el modelo lo permita.

No puede:

- crear Assembly;
- modificar Assembly;
- iniciar Assembly;
- completar Assembly;
- cancelar Assembly;
- archivar Assembly.

---

# Commands y Participation

Los Commands de Proposal no modifican Participation.

Si una acción de Participation requiere posteriormente una
operación sobre Proposal, la coordinación debe producir un
Command explícito dirigido a Proposal.

Debe mantenerse:

```text
Participation

↓

Coordination

↓

Proposal Command

↓

Proposal Aggregate
```

---

# Commands y Voting

Voting no modifica directamente Proposal.

Un resultado de Voting puede originar una intención posterior.

Conceptualmente:

```text
Voting Result

↓

Coordination

↓

AcceptProposal
```

o:

```text
RejectProposal
```

cuando las reglas del dominio lo establezcan.

Proposal vuelve a validar:

- ProposalStatus;
- Permission;
- invariantes;
- ExpectedVersion.

---

# Commands y Document

Los Commands de Proposal no modifican Document.

Una referencia documental puede participar como precondición
cuando el dominio lo requiera.

Document conserva:

- identidad propia;
- ciclo de vida propio;
- invariantes propias;
- Repository propio.

---

# Commands y Notification

Un Command no debe enviar Notifications directamente como parte
del Aggregate.

El flujo esperado es:

```text
Command

↓

Proposal

↓

Domain Event

↓

Notification Process
```

Notification conserva su propio límite.

---

# Commands y Audit

Los Commands deben permitir trazabilidad suficiente para Audit.

La información conceptual puede incluir:

```text
CommandId

ProposalId

OrganizationId

ActorId

Timestamp

ExpectedVersion

CorrelationId

CausationId

CommandType
```

Audit no forma parte del Aggregate Proposal.

---

# Commands e Integration

Sistemas externos no deben modificar Proposal mediante acceso
directo a su estado.

Una intención externa debe traducirse a un Command reconocido por
el dominio.

Conceptualmente:

```text
External Request

↓

Integration / Application Boundary

↓

Proposal Command

↓

Proposal Aggregate
```

No:

```text
External System

↓

ProposalStatus Update
```

---

# Commands y Read Models

Los Read Models no reciben Commands de modificación del dominio.

Debe mantenerse:

```text
Command

↓

Write Side

↓

Proposal Aggregate
```

y:

```text
Query

↓

Read Side
```

El Read Model nunca sustituye al Aggregate como destino de un
Command de dominio.

---

# Commands y CQRS

Dentro de CQRS:

```text
Commands
```

pertenecen al lado de escritura.

```text
Queries
```

pertenecen al lado de lectura.

Debe mantenerse:

```text
Command
    ≠
Query
```

Un Command no debe utilizarse como mecanismo de consulta.

---

# Commands y Event Sourcing

Cuando la arquitectura utilice Event Sourcing Compatible, un
Command aceptado produce Domain Events que representan los hechos
ocurridos.

Ejemplo:

```text
SubmitProposal

↓

ProposalSubmitted
```

La reconstrucción mediante Event Replay no vuelve a ejecutar:

```text
SubmitProposal
```

Replay aplica hechos históricos.

---

# Commands y Seguridad

Los Commands no contienen:

- contraseñas;
- tokens de acceso;
- JWT;
- claves privadas;
- secretos;
- credenciales técnicas;
- sesiones.

La autenticación ocurre fuera del Aggregate.

El dominio recibe una identidad de actor válida conforme a los
contratos establecidos.

---

# Commands y Autorización

La autorización determina:

```text
Who may attempt this Command?
```

El Aggregate determina:

```text
Can this operation be performed now?
```

Estas responsabilidades no deben mezclarse.

---

# Commands e Idempotencia

CommandId permite identificar una solicitud específica.

Cuando el mismo Command sea recibido nuevamente, la arquitectura
puede reconocer que corresponde a la misma intención.

La idempotencia técnica no debe permitir ejecutar dos veces una
transición de dominio que solo puede ocurrir una vez.

Ejemplo:

```text
SubmitProposal

Draft → Submitted
```

Una repetición sobre Submitted no debe generar una segunda
transición ni un segundo hecho de presentación.

---

# Commands y Concurrencia

Dos Commands pueden intentar modificar simultáneamente la misma
Proposal.

Ejemplo:

```text
ProposalStatus = UnderReview

Version = 12
```

Command A:

```text
AcceptProposal

ExpectedVersion = 12
```

Command B:

```text
RejectProposal

ExpectedVersion = 12
```

Solo una modificación puede confirmarse sobre Version 12.

Si AcceptProposal confirma primero:

```text
ProposalStatus = Accepted

Version = 13
```

RejectProposal debe fallar por conflicto de Version.

---

# Commands y Trazabilidad

Todo Command debe permitir reconstruir conceptualmente:

```text
Who

requested

What

against

Which Proposal

When

under

Which Correlation

caused by

Which prior action
```

Esto permite relacionar intención, modificación y eventos sin
convertir Audit en parte del Aggregate.

---

# Auditoría

La información mínima de trazabilidad de un Command comprende:

```text
CommandId

CommandType

ProposalId

OrganizationId

ActorId

Timestamp

ExpectedVersion

CorrelationId

CausationId
```

La persistencia histórica de esta información pertenece al modelo
de Audit cuando corresponda.

---

# Matriz Command — Event

```text
Command                      Expected Domain Event
──────────────────────────────────────────────────────────
CreateProposal               ProposalCreated

RenameProposal               ProposalRenamed

ChangeProposalPurpose        ProposalPurposeChanged

ChangeProposalDescription    ProposalDescriptionChanged

ChangeProposalType           ProposalTypeChanged

UpdateProposalContent        ProposalContentUpdated

ChangeProposalTerritory      ProposalTerritoryChanged

AssociateProposalAssembly    ProposalAssemblyAssociated

SubmitProposal               ProposalSubmitted

StartProposalReview          ProposalReviewStarted

AcceptProposal               ProposalAccepted

RejectProposal               ProposalRejected

WithdrawProposal             ProposalWithdrawn

ArchiveProposal              ProposalArchived
```

La existencia de un Command no garantiza la existencia del evento.

El evento solo puede producirse después de una operación válida.

---

# Matriz Command — State

```text
Command                      Required State       Resulting State
────────────────────────────────────────────────────────────────
CreateProposal               Nonexistent           Draft

RenameProposal               Draft                 Draft

ChangeProposalPurpose        Draft                 Draft

ChangeProposalDescription    Draft                 Draft

ChangeProposalType           Draft                 Draft

UpdateProposalContent        Draft                 Draft

ChangeProposalTerritory      Draft                 Draft

AssociateProposalAssembly    Draft                 Draft

SubmitProposal               Draft                 Submitted

StartProposalReview          Submitted             UnderReview

AcceptProposal               UnderReview           Accepted

RejectProposal               UnderReview           Rejected

WithdrawProposal             Draft                 Withdrawn

WithdrawProposal             Submitted             Withdrawn

ArchiveProposal              Accepted              Archived

ArchiveProposal              Rejected              Archived

ArchiveProposal              Withdrawn             Archived
```

---

# Escenario — CreateProposal válido

```text
Given

ProposalId no existe

And

los datos iniciales son válidos

And

Actor posee Permission

When

CreateProposal es ejecutado

Then

Proposal es creada

And

ProposalStatus = Draft

And

ProposalCreated es producido
```

---

# Escenario — RenameProposal válido

```text
Given

ProposalStatus = Draft

And

ProposalName es válido

And

ExpectedVersion = CurrentVersion

When

RenameProposal es ejecutado

Then

ProposalName es actualizado

And

ProposalStatus permanece Draft

And

Version incrementa

And

ProposalRenamed es producido
```

---

# Escenario — RenameProposal después de Submit

```text
Given

ProposalStatus = Submitted

When

RenameProposal es ejecutado

Then

el Command es rechazado

And

Proposal permanece sin cambios

And

Version permanece sin cambios
```

---

# Escenario — SubmitProposal válido

```text
Given

ProposalStatus = Draft

And

la Proposal satisface las condiciones de presentación

And

Actor posee Permission

And

ExpectedVersion = CurrentVersion

When

SubmitProposal es ejecutado

Then

ProposalStatus = Submitted

And

Version incrementa

And

ProposalSubmitted es producido
```

---

# Escenario — SubmitProposal inválido por estado

```text
Given

ProposalStatus = Submitted

When

SubmitProposal es ejecutado

Then

el Command es rechazado

And

ProposalStatus permanece Submitted

And

Version permanece sin cambios

And

ProposalSubmitted no es producido
```

---

# Escenario — StartProposalReview válido

```text
Given

ProposalStatus = Submitted

And

las condiciones de revisión se cumplen

And

Actor posee Permission

When

StartProposalReview es ejecutado

Then

ProposalStatus = UnderReview

And

Version incrementa

And

ProposalReviewStarted es producido
```

---

# Escenario — AcceptProposal válido

```text
Given

ProposalStatus = UnderReview

And

las condiciones de aceptación se cumplen

And

Actor posee Permission

And

ExpectedVersion = CurrentVersion

When

AcceptProposal es ejecutado

Then

ProposalStatus = Accepted

And

Version incrementa

And

ProposalAccepted es producido
```

---

# Escenario — RejectProposal válido

```text
Given

ProposalStatus = UnderReview

And

las condiciones de rechazo se cumplen

And

Actor posee Permission

And

ExpectedVersion = CurrentVersion

When

RejectProposal es ejecutado

Then

ProposalStatus = Rejected

And

Version incrementa

And

ProposalRejected es producido
```

---

# Escenario — WithdrawProposal desde Draft

```text
Given

ProposalStatus = Draft

And

Actor posee Permission

When

WithdrawProposal es ejecutado

Then

ProposalStatus = Withdrawn

And

Version incrementa

And

ProposalWithdrawn es producido
```

---

# Escenario — WithdrawProposal desde Submitted

```text
Given

ProposalStatus = Submitted

And

Actor posee Permission

When

WithdrawProposal es ejecutado

Then

ProposalStatus = Withdrawn

And

Version incrementa

And

ProposalWithdrawn es producido
```

---

# Escenario — WithdrawProposal desde UnderReview

```text
Given

ProposalStatus = UnderReview

When

WithdrawProposal es ejecutado

Then

el Command es rechazado

And

ProposalStatus permanece UnderReview

And

Version permanece sin cambios
```

---

# Escenario — ArchiveProposal válido

```text
Given

ProposalStatus = Accepted

And

Actor posee Permission

And

ExpectedVersion = CurrentVersion

When

ArchiveProposal es ejecutado

Then

ProposalStatus = Archived

And

Version incrementa

And

ProposalArchived es producido
```

---

# Escenario — ArchiveProposal inválido

```text
Given

ProposalStatus = Draft

When

ArchiveProposal es ejecutado

Then

el Command es rechazado

And

ProposalStatus permanece Draft

And

Version permanece sin cambios
```

---

# Escenario — Command sin Permission

```text
Given

ProposalStatus permite conceptualmente la operación

And

Actor no posee Permission

When

el Command es ejecutado

Then

la operación es rechazada

And

Proposal permanece sin cambios
```

---

# Escenario — Command con Invariante Violada

```text
Given

Actor posee Permission

And

el estado permite la operación

And

una invariante sería violada

When

el Command es ejecutado

Then

la operación es rechazada

And

Proposal permanece sin cambios

And

no se produce el Domain Event de éxito
```

---

# Escenario — Command con Version Conflict

```text
Given

ExpectedVersion != CurrentVersion

When

un Command modificador intenta confirmarse

Then

el Command es rechazado

And

Proposal permanece sin cambios

And

Version no incrementa
```

---

# Escenario — Command sobre Archived

```text
Given

ProposalStatus = Archived

When

un Command modificador es ejecutado

Then

el Command es rechazado

And

ProposalStatus permanece Archived

And

Version permanece sin cambios
```

---

# Consistencia

Cada Command aceptado debe:

- modificar exclusivamente un Proposal Aggregate;
- ejecutarse dentro del Consistency Boundary de Proposal;
- preservar todas las invariantes;
- respetar la State Machine;
- respetar Permissions;
- respetar Versioning;
- producir únicamente eventos válidos;
- mantener el Aggregate en un estado completamente consistente.

La definición formal del límite se desarrolla en:

```text
DOMAIN-007J-Consistency-Boundary.md
```

---

# Atomicidad

No está permitido confirmar parcialmente un Command.

Ejemplo inválido:

```text
ProposalStatus = Submitted

Version = oldVersion

ProposalSubmitted = not recorded
```

El resultado válido debe representar una modificación coherente
del Aggregate.

---

# Commands y Transacciones Distribuidas

Un Command de Proposal modifica exclusivamente Proposal.

No debe utilizar una única transacción de dominio para modificar
simultáneamente:

```text
Proposal

+

Assembly

+

Participation

+

Voting

+

Document
```

La coordinación entre Aggregates utiliza los mecanismos definidos
por la arquitectura distribuida.

---

# Independencia Tecnológica

Los Commands del dominio no dependen de:

```text
HTTP

REST

GraphQL

JSON

Kafka

RabbitMQ

PostgreSQL

MongoDB

Redis

OAuth

JWT

FastAPI

Django

React

Next.js

FIWARE
```

Un endpoint HTTP puede traducir una solicitud a un Command.

El endpoint no define el Command.

---

# Compatibilidad Arquitectónica

El modelo de Commands de Proposal es compatible con:

- Domain-Driven Design;
- Aggregate Pattern;
- CQRS;
- Clean Architecture;
- Hexagonal Architecture;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency;
- arquitectura distribuida;
- interoperabilidad basada en contratos.

---

# Evolución

La incorporación de un nuevo Command debe responder a una nueva
intención explícita del dominio.

Antes de incorporar un Command debe evaluarse su impacto sobre:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007D-Domain-Events.md

DOMAIN-007E-Invariants.md

DOMAIN-007F-Permissions.md

DOMAIN-007I-Versioning.md

DOMAIN-007J-Consistency-Boundary.md

DOMAIN-007K-Integration-Events.md

DOMAIN-007L-Read-Model.md

DOMAIN-007M-Test-Scenarios.md

DOMAIN-007O-Security-Model.md

DOMAIN-007P-Extension-Points.md
```

No debe introducirse un Command únicamente por conveniencia de una
API, UI, base de datos o integración.

---

# Regla de Coherencia Documental

Todo Command oficial debe encontrarse documentado en este archivo.

Los documentos posteriores pueden profundizar:

- eventos;
- invariantes;
- Permissions;
- Versioning;
- consistencia;
- seguridad;
- escenarios.

No deben introducir silenciosamente Commands que contradigan este
modelo.

---

# Restricciones

No está permitido:

- modificar Proposal sin un comportamiento explícito;
- utilizar Commands genéricos para alterar arbitrariamente el
  Aggregate;
- utilizar SetProposalStatus;
- utilizar DeleteProposal como sustitución de ArchiveProposal;
- modificar ProposalId;
- transferir OrganizationId mediante un Command;
- editar Proposal mediante Commands editoriales fuera de Draft;
- aceptar Proposal fuera de UnderReview;
- rechazar Proposal fuera de UnderReview;
- retirar Proposal desde UnderReview en la versión 1.0;
- retirar Proposal desde Accepted;
- retirar Proposal desde Rejected;
- retirar Proposal desde Archived;
- archivar Proposal desde Draft;
- archivar Proposal desde Submitted;
- archivar Proposal desde UnderReview;
- modificar otros Aggregates desde un Command de Proposal;
- ignorar Permissions;
- ignorar State Machine;
- ignorar invariantes;
- ignorar ExpectedVersion;
- producir Domain Events de éxito después de un Command rechazado;
- dejar el Aggregate parcialmente modificado;
- introducir Commands técnicos como conceptos del dominio.

---

# Principios Arquitectónicos

Los Commands preservan las siguientes separaciones:

```text
Command
    ≠
Domain Event
```

```text
Command
    ≠
Integration Event
```

```text
Command
    ≠
Query
```

```text
Command
    ≠
Persistence Operation
```

```text
Permission
    ≠
Domain Validity
```

```text
ExpectedVersion
    ≠
Proposal Version Mutation
```

```text
External Request
    ≠
Domain Command
```

```text
Voting Result
    ≠
Proposal Command
```

```text
ArchiveProposal
    ≠
DeleteProposal
```

Estas separaciones mantienen el lenguaje ubicuo y evitan que
responsabilidades externas sean absorbidas por Proposal.

---

# Documentación Complementaria

El modelo de Commands debe interpretarse conjuntamente con:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007D-Domain-Events.md

DOMAIN-007E-Invariants.md

DOMAIN-007F-Permissions.md

DOMAIN-007G-Repository-Contract.md

DOMAIN-007I-Versioning.md

DOMAIN-007J-Consistency-Boundary.md

DOMAIN-007K-Integration-Events.md

DOMAIN-007L-Read-Model.md

DOMAIN-007M-Test-Scenarios.md

DOMAIN-007O-Security-Model.md

DOMAIN-007P-Extension-Points.md
```

Cada documento profundiza una responsabilidad específica sin
reemplazar el significado conceptual de los Commands establecido
aquí.

---

# Definición de Éxito

Los Commands del Aggregate **Proposal** constituyen el mecanismo
oficial para expresar intenciones de creación y modificación sobre
una iniciativa dentro de AURA Core.

Cada Command posee una semántica explícita del dominio y se dirige
a un único Proposal Aggregate.

Los Commands no garantizan su ejecución.

Toda intención debe ser evaluada mediante:

```text
Command

↓

Identity

↓

Current State

↓

Permissions

↓

Preconditions

↓

Invariants

↓

ExpectedVersion

↓

Proposal Behavior
```

Solo una operación válida puede producir:

```text
State Change
```

o:

```text
Domain Data Change
```

seguido de:

```text
Version Increment

↓

Domain Event
```

cuando corresponda.

Los Commands de transición respetan estrictamente:

```text
Draft

↓

Submitted

↓

UnderReview

├────────► Accepted

└────────► Rejected
```

junto con:

```text
Draft

↓

Withdrawn
```

y:

```text
Submitted

↓

Withdrawn
```

y los caminos de archivado:

```text
Accepted

↓

Archived
```

```text
Rejected

↓

Archived
```

```text
Withdrawn

↓

Archived
```

Los Commands editoriales permanecen restringidos a Draft en la
versión 1.0, preservando la integridad de la información
formalmente presentada.

Ningún Command puede modificar directamente otro Aggregate.

Ningún Command puede eludir la State Machine, Permissions,
Invariants o Versioning.

Un Command rechazado mantiene Proposal íntegramente sin cambios y
no produce el Domain Event de éxito.

De esta forma, **DOMAIN-007C-Commands.md** establece el contrato
conceptual de intención para el Aggregate Proposal, preservando su
identidad, ciclo de vida, consistencia, trazabilidad, concurrencia,
lenguaje ubicuo, independencia tecnológica y los principios
Domain-Driven Design establecidos para AURA Core.