# DOMAIN-007H — Proposal Examples

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
- DOMAIN-007C-Commands.md
- DOMAIN-007D-Domain-Events.md
- DOMAIN-007E-Invariants.md
- DOMAIN-007F-Permissions.md
- DOMAIN-007G-Repository-Contract.md
- DOMAIN-007I-Versioning.md
- DOMAIN-007J-Consistency-Boundary.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Documentar ejemplos conceptuales del comportamiento del
Aggregate **Proposal**.

Los ejemplos permiten representar de manera explícita cómo las
reglas definidas por el Aggregate, Lifecycle, State Machine,
Commands, Domain Events, Invariants, Permissions y Repository
Contract interactúan durante situaciones concretas del dominio.

Este documento no introduce nuevas reglas.

Los ejemplos contenidos aquí deben interpretarse exclusivamente
como representaciones de las reglas oficiales definidas en los
documentos conceptuales del Aggregate Proposal.

Cuando exista una diferencia entre un ejemplo y una regla
normativa establecida en otro documento oficial del Aggregate,
prevalece siempre la regla normativa.

---

# Propósito

Los ejemplos permiten verificar conceptualmente que Proposal
mantiene un comportamiento coherente durante todo su ciclo de
vida.

Cada escenario busca mostrar la relación entre:

```text
Actor

↓

Permission

↓

Command

↓

Proposal

↓

State Validation

↓

Invariant Validation

↓

Version Validation

↓

State Change

↓

Domain Event

↓

Repository
```

Los ejemplos también permiten representar situaciones en las que
una operación debe ser rechazada.

En esos casos debe mantenerse:

```text
Proposal State
    =
Unchanged
```

```text
Version
    =
Unchanged
```

```text
Success Domain Event
    =
Not Produced
```

---

# Principios

Los ejemplos de Proposal cumplen los siguientes principios:

- utilizan exclusivamente conceptos oficiales del Aggregate;
- no reemplazan las invariantes;
- no reemplazan la State Machine;
- no reemplazan el Lifecycle;
- no reemplazan los Commands;
- no reemplazan los Domain Events;
- no reemplazan las reglas de Permissions;
- no reemplazan el Repository Contract;
- no introducen dependencias tecnológicas;
- no representan implementaciones;
- no representan endpoints;
- no representan estructuras de base de datos;
- no introducen comportamiento perteneciente a otros Aggregates;
- mantienen Proposal como único límite de consistencia;
- utilizan referencias externas mediante identificadores.

---

# Convención de Escenarios

Los escenarios utilizan conceptualmente la estructura:

```text
Given

Estado inicial y precondiciones.

When

Command o acción ejecutada.

Then

Resultado esperado.
```

Cuando corresponda también se especifican:

```text
Permission

State Transition

Version

Domain Event
```

Esta estructura permite relacionar cada ejemplo con las reglas
normativas del Aggregate.

---

# Proposal de Referencia

Para varios ejemplos se utilizará conceptualmente una Proposal
con los siguientes datos:

```text
ProposalId:
proposal-001

OrganizationId:
organization-001

AuthorId:
citizen-001

TerritoryId:
territory-001

AssemblyId:
assembly-001

ProposalType:
CommunityInitiative

ProposalName:
Mejoramiento de iluminación comunitaria

ProposalPurpose:
Mejorar las condiciones de iluminación de espacios comunitarios.

ProposalDescription:
Instalación y mejoramiento de luminarias en sectores definidos
por la comunidad.

ProposalStatus:
Draft

Version:
1
```

Estos valores son únicamente ilustrativos.

No constituyen identificadores reservados ni valores obligatorios
del dominio.

---

# Ejemplo — Creación de Proposal

## Estado inicial

La Proposal todavía no existe.

```text
ProposalId = proposal-001
```

El actor posee:

```text
proposal:create
```

La Organization correspondiente es:

```text
OrganizationId = organization-001
```

## Command

```text
CreateProposal
```

Datos conceptuales:

```text
ProposalId:
proposal-001

OrganizationId:
organization-001

AuthorId:
citizen-001

ProposalType:
CommunityInitiative

ProposalName:
Mejoramiento de iluminación comunitaria

ProposalPurpose:
Mejorar las condiciones de iluminación de espacios comunitarios.

ProposalDescription:
Instalación y mejoramiento de luminarias en sectores definidos
por la comunidad.
```

## Resultado

Proposal valida sus invariantes iniciales.

La Proposal es creada en:

```text
Draft
```

Se produce:

```text
ProposalCreated
```

El Aggregate queda disponible para las operaciones permitidas en
Draft.

---

# Ejemplo — Creación con Datos Inválidos

## Given

El actor posee:

```text
proposal:create
```

pero los datos proporcionados no satisfacen las invariantes
necesarias para crear Proposal.

## When

```text
CreateProposal
```

es solicitado.

## Then

La creación es rechazada.

Debe mantenerse:

```text
Proposal
    =
Not Created
```

y:

```text
ProposalCreated
    =
Not Produced
```

La existencia del permiso no permite evitar las invariantes.

---

# Ejemplo — Creación sin Permiso

## Given

El actor no posee:

```text
proposal:create
```

## When

intenta ejecutar:

```text
CreateProposal
```

## Then

la operación es rechazada antes de producir una modificación
válida del dominio.

Debe mantenerse:

```text
Proposal
    =
Not Created
```

```text
ProposalCreated
    =
Not Produced
```

---

# Ejemplo — Edición del Nombre en Draft

## Given

```text
ProposalStatus = Draft

Version = 1
```

El actor posee:

```text
proposal:rename
```

## When

ejecuta:

```text
RenameProposal
```

con:

```text
ProposalName:
Plan de mejoramiento de iluminación comunitaria
```

## Then

Proposal valida el nuevo nombre.

El nombre es actualizado.

El estado permanece:

```text
Draft
```

Version incrementa:

```text
1 → 2
```

Se produce:

```text
ProposalRenamed
```

---

# Ejemplo — Cambio de Propósito en Draft

## Given

```text
ProposalStatus = Draft

Version = 2
```

El actor posee:

```text
proposal:change-purpose
```

## When

ejecuta:

```text
ChangeProposalPurpose
```

con un propósito válido.

## Then

ProposalPurpose es actualizado.

El estado permanece:

```text
Draft
```

Version incrementa:

```text
2 → 3
```

Se produce:

```text
ProposalPurposeChanged
```

---

# Ejemplo — Cambio de Descripción en Draft

## Given

```text
ProposalStatus = Draft

Version = 3
```

El actor posee:

```text
proposal:change-description
```

## When

ejecuta:

```text
ChangeProposalDescription
```

## Then

la descripción es modificada.

El estado permanece:

```text
Draft
```

Version incrementa:

```text
3 → 4
```

Se produce:

```text
ProposalDescriptionChanged
```

---

# Ejemplo — Cambio de Tipo en Draft

## Given

```text
ProposalStatus = Draft

Version = 4
```

El actor posee:

```text
proposal:change-type
```

## When

ejecuta:

```text
ChangeProposalType
```

con un ProposalType válido.

## Then

ProposalType es actualizado.

El estado permanece:

```text
Draft
```

Version incrementa:

```text
4 → 5
```

Se produce:

```text
ProposalTypeChanged
```

---

# Ejemplo — Actualización de Contenido

## Given

```text
ProposalStatus = Draft

Version = 5
```

El actor posee:

```text
proposal:update-content
```

## When

ejecuta:

```text
UpdateProposalContent
```

con contenido válido.

## Then

ProposalContent es actualizado.

El estado permanece:

```text
Draft
```

Version incrementa:

```text
5 → 6
```

Se produce:

```text
ProposalContentUpdated
```

---

# Ejemplo — Actualización de Contenido después de Presentación

## Given

```text
ProposalStatus = Submitted

Version = 7
```

El actor posee:

```text
proposal:update-content
```

## When

intenta ejecutar:

```text
UpdateProposalContent
```

## Then

la operación es rechazada porque Submitted no permite esa
modificación.

Debe mantenerse:

```text
ProposalStatus = Submitted

Version = 7
```

y:

```text
ProposalContentUpdated
    =
Not Produced
```

El permiso no crea una transición ni elimina una restricción del
estado.

---

# Ejemplo — Asociación Territorial

## Given

```text
ProposalStatus = Draft

TerritoryId = null

Version = 6
```

El actor posee:

```text
proposal:change-territory
```

## When

ejecuta:

```text
ChangeProposalTerritory
```

con:

```text
TerritoryId = territory-001
```

## Then

Proposal mantiene la referencia:

```text
TerritoryId = territory-001
```

Version incrementa.

El Aggregate Territory no es incorporado dentro de Proposal.

La relación permanece:

```text
Proposal

↓

TerritoryId

↓

Territory
```

No:

```text
Proposal

↓

Territory Aggregate
```

---

# Ejemplo — Asociación con Assembly

## Given

```text
ProposalStatus = Draft

AssemblyId = null

Version = 7
```

El actor posee:

```text
proposal:associate-assembly
```

## When

ejecuta:

```text
AssociateProposalAssembly
```

con:

```text
AssemblyId = assembly-001
```

## Then

Proposal mantiene:

```text
AssemblyId = assembly-001
```

como referencia.

Assembly no se convierte en entidad interna de Proposal.

Proposal no modifica:

- AssemblyStatus;
- programación de Assembly;
- convocatoria;
- modalidad;
- Version de Assembly.

La consistencia de ambos Aggregates permanece separada.

---

# Ejemplo — Presentación de Proposal

## Given

```text
ProposalStatus = Draft

Version = 8
```

La Proposal satisface todas las condiciones necesarias para su
presentación.

El actor posee:

```text
proposal:submit
```

## When

ejecuta:

```text
SubmitProposal
```

## Then

se produce la transición:

```text
Draft

↓

Submitted
```

ProposalStatus queda:

```text
Submitted
```

Version incrementa:

```text
8 → 9
```

Se registra el momento de presentación cuando corresponda:

```text
SubmittedAt
```

Se produce:

```text
ProposalSubmitted
```

---

# Ejemplo — Presentación de Proposal Incompleta

## Given

```text
ProposalStatus = Draft
```

El actor posee:

```text
proposal:submit
```

pero Proposal no satisface una o más invariantes necesarias para
su presentación.

## When

ejecuta:

```text
SubmitProposal
```

## Then

la operación es rechazada.

Debe mantenerse:

```text
ProposalStatus = Draft
```

Version no cambia.

No se produce:

```text
ProposalSubmitted
```

---

# Ejemplo — Presentación Duplicada

## Given

```text
ProposalStatus = Submitted
```

## When

un actor intenta ejecutar nuevamente:

```text
SubmitProposal
```

## Then

la operación es rechazada.

No existe:

```text
Submitted → Submitted
```

como transición de presentación.

Debe mantenerse:

```text
ProposalStatus = Submitted
```

y ningún nuevo:

```text
ProposalSubmitted
```

es producido.

---

# Ejemplo — Edición después de Presentación

## Given

```text
ProposalStatus = Submitted
```

El actor posee:

```text
proposal:rename
```

## When

ejecuta:

```text
RenameProposal
```

## Then

la operación es rechazada por el estado del Aggregate.

El permiso no permite modificar una Proposal formalmente
presentada cuando la State Machine no admite esa modificación.

Debe mantenerse:

```text
ProposalStatus = Submitted

ProposalName = PreviousValue

Version = PreviousVersion
```

y:

```text
ProposalRenamed
    =
Not Produced
```

---

# Ejemplo — Inicio de Revisión

## Given

```text
ProposalStatus = Submitted

Version = 9
```

El actor posee:

```text
proposal:start-review
```

## When

ejecuta:

```text
StartProposalReview
```

## Then

se produce:

```text
Submitted

↓

UnderReview
```

ProposalStatus queda:

```text
UnderReview
```

Version incrementa:

```text
9 → 10
```

Puede registrarse:

```text
ReviewStartedAt
```

Se produce:

```text
ProposalReviewStarted
```

---

# Ejemplo — Inicio de Revisión desde Draft

## Given

```text
ProposalStatus = Draft
```

El actor posee:

```text
proposal:start-review
```

## When

intenta ejecutar:

```text
StartProposalReview
```

## Then

la operación es rechazada.

No existe la transición:

```text
Draft

↓

UnderReview
```

dentro del Lifecycle establecido.

Debe mantenerse:

```text
ProposalStatus = Draft
```

Version no cambia.

No se produce:

```text
ProposalReviewStarted
```

---

# Ejemplo — Inicio de Revisión sin Permiso

## Given

```text
ProposalStatus = Submitted
```

El actor no posee:

```text
proposal:start-review
```

## When

intenta ejecutar:

```text
StartProposalReview
```

## Then

la operación es rechazada por autorización.

Proposal permanece:

```text
Submitted
```

Version permanece sin cambios.

No se produce:

```text
ProposalReviewStarted
```

---

# Ejemplo — Aceptación de Proposal

## Given

```text
ProposalStatus = UnderReview

Version = 10
```

El actor posee:

```text
proposal:accept
```

Las condiciones de decisión son válidas.

## When

ejecuta:

```text
AcceptProposal
```

## Then

se produce:

```text
UnderReview

↓

Accepted
```

ProposalStatus queda:

```text
Accepted
```

Version incrementa:

```text
10 → 11
```

Puede registrarse:

```text
DecidedAt
```

Se produce:

```text
ProposalAccepted
```

---

# Ejemplo — Aceptación desde Submitted

## Given

```text
ProposalStatus = Submitted
```

El actor posee:

```text
proposal:accept
```

## When

intenta ejecutar:

```text
AcceptProposal
```

## Then

la operación es rechazada.

El permiso no permite omitir:

```text
UnderReview
```

Debe mantenerse:

```text
ProposalStatus = Submitted
```

Version no cambia.

No se produce:

```text
ProposalAccepted
```

---

# Ejemplo — Aceptación sin Permiso

## Given

```text
ProposalStatus = UnderReview
```

El actor no posee:

```text
proposal:accept
```

## When

intenta ejecutar:

```text
AcceptProposal
```

## Then

la operación es rechazada por autorización.

Proposal permanece:

```text
UnderReview
```

No se incrementa Version.

No se produce:

```text
ProposalAccepted
```

---

# Ejemplo — Rechazo de Proposal

## Given

```text
ProposalStatus = UnderReview

Version = 10
```

El actor posee:

```text
proposal:reject
```

Las condiciones necesarias para el rechazo son válidas.

## When

ejecuta:

```text
RejectProposal
```

## Then

se produce:

```text
UnderReview

↓

Rejected
```

ProposalStatus queda:

```text
Rejected
```

Version incrementa:

```text
10 → 11
```

Puede registrarse:

```text
DecidedAt
```

Se produce:

```text
ProposalRejected
```

---

# Ejemplo — Rechazo desde Draft

## Given

```text
ProposalStatus = Draft
```

El actor posee:

```text
proposal:reject
```

## When

intenta ejecutar:

```text
RejectProposal
```

## Then

la operación es rechazada.

No existe:

```text
Draft

↓

Rejected
```

como transición válida.

Proposal permanece:

```text
Draft
```

Version no cambia.

No se produce:

```text
ProposalRejected
```

---

# Ejemplo — Decisiones Mutuamente Excluyentes

## Given

```text
ProposalStatus = UnderReview
```

## When

una decisión válida produce:

```text
ProposalStatus = Accepted
```

## Then

una operación posterior:

```text
RejectProposal
```

debe ser rechazada.

Del mismo modo, si la primera decisión produce:

```text
ProposalStatus = Rejected
```

una operación posterior:

```text
AcceptProposal
```

debe ser rechazada.

Debe mantenerse:

```text
Accepted
    ≠
Rejected
```

y una misma versión lógica de Proposal no puede encontrarse
simultáneamente en ambos estados.

---

# Ejemplo — Retiro desde Draft

## Given

```text
ProposalStatus = Draft

Version = 4
```

El actor posee:

```text
proposal:withdraw
```

y satisface las reglas de autorización aplicables.

## When

ejecuta:

```text
WithdrawProposal
```

## Then

se produce:

```text
Draft

↓

Withdrawn
```

ProposalStatus queda:

```text
Withdrawn
```

Version incrementa:

```text
4 → 5
```

Puede registrarse:

```text
WithdrawnAt
```

Se produce:

```text
ProposalWithdrawn
```

---

# Ejemplo — Retiro desde Submitted

## Given

```text
ProposalStatus = Submitted

Version = 9
```

El actor posee:

```text
proposal:withdraw
```

## When

ejecuta:

```text
WithdrawProposal
```

## Then

se produce:

```text
Submitted

↓

Withdrawn
```

ProposalStatus queda:

```text
Withdrawn
```

Version incrementa:

```text
9 → 10
```

Se produce:

```text
ProposalWithdrawn
```

---

# Ejemplo — Retiro durante Revisión

## Given

```text
ProposalStatus = UnderReview
```

El actor posee:

```text
proposal:withdraw
```

## When

intenta ejecutar:

```text
WithdrawProposal
```

## Then

la operación es rechazada.

El permiso no modifica el Lifecycle.

Debe mantenerse:

```text
ProposalStatus = UnderReview
```

Version no cambia.

No se produce:

```text
ProposalWithdrawn
```

---

# Ejemplo — Archivado de Proposal Aceptada

## Given

```text
ProposalStatus = Accepted

Version = 11
```

El actor posee:

```text
proposal:archive
```

## When

ejecuta:

```text
ArchiveProposal
```

## Then

se produce:

```text
Accepted

↓

Archived
```

ProposalStatus queda:

```text
Archived
```

Version incrementa:

```text
11 → 12
```

Puede registrarse:

```text
ArchivedAt
```

Se produce:

```text
ProposalArchived
```

---

# Ejemplo — Archivado de Proposal Rechazada

## Given

```text
ProposalStatus = Rejected
```

El actor posee:

```text
proposal:archive
```

## When

ejecuta:

```text
ArchiveProposal
```

## Then

se produce:

```text
Rejected

↓

Archived
```

Se produce:

```text
ProposalArchived
```

---

# Ejemplo — Archivado de Proposal Retirada

## Given

```text
ProposalStatus = Withdrawn
```

El actor posee:

```text
proposal:archive
```

## When

ejecuta:

```text
ArchiveProposal
```

## Then

se produce:

```text
Withdrawn

↓

Archived
```

Se produce:

```text
ProposalArchived
```

---

# Ejemplo — Archivado desde Draft

## Given

```text
ProposalStatus = Draft
```

El actor posee:

```text
proposal:archive
```

## When

intenta ejecutar:

```text
ArchiveProposal
```

## Then

la operación es rechazada.

No existe:

```text
Draft

↓

Archived
```

como transición válida dentro del Lifecycle establecido.

Proposal permanece:

```text
Draft
```

Version no cambia.

No se produce:

```text
ProposalArchived
```

---

# Ejemplo — Modificación de Proposal Archivada

## Given

```text
ProposalStatus = Archived

Version = 15
```

## When

un actor intenta ejecutar:

```text
RenameProposal
```

o:

```text
UpdateProposalContent
```

o:

```text
ChangeProposalPurpose
```

## Then

la operación es rechazada.

Debe mantenerse:

```text
ProposalStatus = Archived

Version = 15
```

Una Proposal archivada no admite nuevas modificaciones ordinarias
del dominio.

---

# Ejemplo — Referencia a Organization

## Given

Proposal pertenece a:

```text
OrganizationId = organization-001
```

## When

Proposal es recuperada o modificada.

## Then

la relación permanece mediante:

```text
OrganizationId
```

Proposal no contiene:

```text
Organization Aggregate
```

como parte de su límite de consistencia.

Proposal tampoco puede modificar:

```text
Organization
```

---

# Ejemplo — Intento de Cambio de Organization

## Given

```text
Proposal.OrganizationId = organization-001
```

## When

una operación intenta cambiarlo por:

```text
organization-002
```

## Then

la operación debe ser rechazada.

Debe mantenerse:

```text
OrganizationId = organization-001
```

OrganizationId permanece inmutable durante la vida de Proposal.

---

# Ejemplo — Intento de Cambio de ProposalId

## Given

```text
ProposalId = proposal-001
```

## When

una operación intenta modificarlo por:

```text
proposal-002
```

## Then

la operación es rechazada.

Debe mantenerse:

```text
ProposalId = proposal-001
```

La identidad del Aggregate nunca cambia.

---

# Ejemplo — Actor de Otra Organization

## Given

Proposal pertenece a:

```text
OrganizationId = organization-001
```

El actor posee una Membership válida únicamente dentro de:

```text
OrganizationId = organization-002
```

La capacidad solicitada depende del contexto organizacional.

## When

el actor intenta ejecutar un Command modificador sobre Proposal.

## Then

la autorización debe ser rechazada.

Proposal permanece sin cambios.

Version permanece sin cambios.

No se produce un Domain Event de éxito.

---

# Ejemplo — Permission no Reemplaza Invariant

## Given

El actor posee:

```text
proposal:submit
```

pero Proposal no satisface las condiciones necesarias para ser
presentada.

## When

ejecuta:

```text
SubmitProposal
```

## Then

la operación es rechazada por el dominio.

Debe mantenerse:

```text
Permission Granted

≠

Operation Guaranteed
```

---

# Ejemplo — Permission no Reemplaza State Machine

## Given

```text
ProposalStatus = Draft
```

El actor posee:

```text
proposal:accept
```

## When

ejecuta:

```text
AcceptProposal
```

## Then

la operación es rechazada.

Debe mantenerse:

```text
Permission

≠

Valid Transition
```

---

# Ejemplo — Permission no Reemplaza Version

## Given

El actor posee:

```text
proposal:accept
```

Proposal se encuentra:

```text
UnderReview
```

El Command utiliza:

```text
ExpectedVersion = 10
```

pero el estado persistido posee:

```text
PersistedVersion = 11
```

## When

se intenta persistir la aceptación.

## Then

la operación debe ser rechazada por conflicto de concurrencia.

Debe mantenerse:

```text
Permission Granted

+

Version Conflict

=

No Persisted Modification
```

---

# Ejemplo — Concurrencia entre Accept y Reject

## Estado inicial

```text
ProposalStatus = UnderReview

Version = 20
```

Dos procesos recuperan simultáneamente Proposal.

Proceso A:

```text
ProposalStatus = UnderReview

Version = 20
```

Proceso B:

```text
ProposalStatus = UnderReview

Version = 20
```

## Proceso A

Ejecuta:

```text
AcceptProposal
```

Resultado local:

```text
ProposalStatus = Accepted

Version = 21
```

Persiste con:

```text
ExpectedVersion = 20
```

El Repository encuentra:

```text
PersistedVersion = 20
```

La escritura es aceptada.

Estado persistido:

```text
ProposalStatus = Accepted

Version = 21
```

## Proceso B

Ejecuta sobre su copia previa:

```text
RejectProposal
```

Resultado local:

```text
ProposalStatus = Rejected

Version = 21
```

Intenta persistir con:

```text
ExpectedVersion = 20
```

El Repository encuentra:

```text
PersistedVersion = 21
```

## Resultado

La escritura del Proceso B es rechazada mediante:

```text
ProposalConcurrencyConflict
```

El estado persistido permanece:

```text
ProposalStatus = Accepted

Version = 21
```

No se utiliza:

```text
Last Write Wins
```

---

# Ejemplo — Concurrencia entre Dos Ediciones

## Estado inicial

```text
ProposalStatus = Draft

ProposalName = Propuesta Comunitaria

Version = 5
```

Proceso A y Proceso B recuperan Version 5.

Proceso A ejecuta:

```text
RenameProposal
```

Resultado:

```text
ProposalName = Plan Comunitario

Version = 6
```

La modificación es persistida.

Proceso B intenta posteriormente modificar el contenido utilizando:

```text
ExpectedVersion = 5
```

pero:

```text
PersistedVersion = 6
```

La persistencia debe ser rechazada.

El proceso debe recuperar nuevamente el Aggregate antes de
intentar una nueva modificación válida.

---

# Ejemplo — Recuperación desde Repository

## Given

Existe una Proposal persistida:

```text
ProposalId = proposal-001

ProposalStatus = Submitted

Version = 9
```

## When

se ejecuta:

```text
ProposalRepository.getById(
    proposal-001
)
```

## Then

el Repository reconstruye:

```text
Proposal
```

manteniendo:

```text
ProposalId = proposal-001

ProposalStatus = Submitted

Version = 9
```

La reconstrucción no produce:

```text
ProposalCreated
```

y no incrementa Version.

---

# Ejemplo — Proposal No Encontrada

## Given

```text
ProposalId = proposal-999
```

no existe.

## When

se ejecuta:

```text
ProposalRepository.getById(
    proposal-999
)
```

## Then

el Repository expresa:

```text
ProposalNotFound
```

No crea una Proposal vacía.

No crea una Proposal en Draft.

No produce:

```text
ProposalCreated
```

---

# Ejemplo — Persistencia Exitosa

## Given

Proposal fue recuperada con:

```text
Version = 12
```

Un comportamiento válido produce:

```text
Version = 13
```

## When

se ejecuta:

```text
ProposalRepository.save(
    Proposal,
    ExpectedVersion = 12
)
```

y la persistencia mantiene:

```text
PersistedVersion = 12
```

## Then

la escritura es aceptada.

El estado completo del Aggregate es persistido.

La versión persistida queda:

```text
13
```

---

# Ejemplo — Persistencia con Conflicto

## Given

Proposal fue recuperada con:

```text
Version = 12
```

pero otra operación ya persistió:

```text
Version = 13
```

## When

se ejecuta:

```text
ProposalRepository.save(
    Proposal,
    ExpectedVersion = 12
)
```

## Then

se produce conceptualmente:

```text
ProposalConcurrencyConflict
```

La escritura es rechazada.

No se sobrescribe Version 13.

---

# Ejemplo — Proposal Archivada en Repository

## Given

```text
ProposalStatus = Archived

Version = 25
```

## When

ProposalRepository recupera Proposal.

## Then

la Proposal es reconstruida con:

```text
ProposalStatus = Archived

Version = 25
```

Debe mantenerse:

```text
Archived

≠

NotFound
```

---

# Ejemplo — Persistencia No Modifica el Dominio

## Given

Proposal se encuentra:

```text
Submitted
```

## When

el Repository persiste Proposal.

## Then

el Repository no puede decidir cambiarla a:

```text
UnderReview
```

La transición solo puede ocurrir mediante comportamiento válido
del Aggregate.

Debe mantenerse:

```text
Repository

≠

Domain Behavior
```

---

# Ejemplo — Read Model no Modifica Proposal

## Given

existe una proyección:

```text
ProposalSummary
```

con:

```text
ProposalId

ProposalName

ProposalStatus
```

## When

un consumidor necesita modificar Proposal.

## Then

no modifica:

```text
ProposalSummary
```

como sustituto del Aggregate.

Debe utilizarse conceptualmente:

```text
ProposalRepository.getById()

↓

Proposal

↓

Domain Behavior

↓

ProposalRepository.save()
```

---

# Ejemplo — Proposal dentro de Assembly

Una Proposal puede estar relacionada con:

```text
AssemblyId = assembly-001
```

Esto significa:

```text
Proposal

↓

AssemblyId

↓

Assembly
```

No significa:

```text
Assembly
    └── Proposal
        └── Proposal Internal State
```

ni:

```text
Proposal
    └── Assembly Aggregate
```

Ambos mantienen límites de consistencia independientes.

---

# Ejemplo — Proposal y Participation

Una Proposal puede originar o contextualizar procesos de
Participation.

La relación conceptual puede expresarse mediante:

```text
ProposalId
```

desde el Aggregate correspondiente.

Proposal no absorbe:

```text
Participation
```

Participation mantiene:

- identidad propia;
- Lifecycle propio;
- State Machine propia;
- invariantes propias;
- Repository propio;
- Domain Events propios.

---

# Ejemplo — Proposal y Voting

Una Proposal aceptada o sometida a determinados procesos puede
relacionarse posteriormente con Voting según las reglas del
Aggregate correspondiente.

La relación puede utilizar:

```text
ProposalId
```

como referencia.

Esto no convierte:

```text
Voting
```

en una entidad interna de Proposal.

Proposal no ejecuta:

- apertura de votación;
- registro de votos;
- conteo;
- cierre de votación;
- determinación del resultado de Voting.

Estas responsabilidades pertenecen al Aggregate Voting.

---

# Ejemplo — Proposal y Document

Una Proposal puede relacionarse con Documents.

La relación puede utilizar:

```text
ProposalId
```

y:

```text
DocumentId
```

según el contexto correspondiente.

Proposal no almacena el contenido documental completo como parte
de su límite de consistencia.

Document mantiene su propia identidad y ciclo de vida.

---

# Ejemplo — Proposal y Notification

Un hecho relevante de Proposal puede producir posteriormente una
notificación.

Ejemplo conceptual:

```text
ProposalSubmitted

↓

Notification Process
```

Proposal no ejecuta:

```text
SendEmail

SendSMS

SendPushNotification
```

La responsabilidad de comunicación pertenece al contexto
correspondiente.

---

# Ejemplo — Proposal y Audit

Una transición:

```text
UnderReview

↓

Accepted
```

produce:

```text
ProposalAccepted
```

Este hecho puede ser utilizado por Audit.

Proposal no almacena internamente un Aggregate Audit.

La trazabilidad puede utilizar:

```text
ProposalId

Version

ActorId

Timestamp

Domain Event

CorrelationId

CausationId
```

sin absorber la responsabilidad de Audit.

---

# Ejemplo — Proposal e Integration

Un Domain Event como:

```text
ProposalAccepted
```

puede dar origen a un Integration Event cuando otro Bounded
Context o sistema externo requiera conocer el hecho.

Conceptualmente:

```text
ProposalAccepted

↓

Integration Mapping

↓

ProposalAcceptedForIntegration
```

Proposal no conoce:

- endpoint;
- protocolo;
- proveedor;
- sistema municipal;
- FIWARE;
- NGSI-LD;
- credenciales.

La integración permanece fuera del Aggregate.

---

# Ejemplo — Integración Municipal

Una Proposal puede necesitar ser comunicada a un sistema
municipal.

Conceptualmente:

```text
Proposal

↓

Domain Event

↓

Integration Event

↓

Integration Adapter

↓

Municipal System
```

No:

```text
Proposal

↓

HTTP Request

↓

Municipal API
```

El Aggregate no conoce detalles técnicos de la integración.

---

# Ejemplo — Interoperabilidad FIWARE

Cuando una Proposal deba ser representada en un ecosistema
FIWARE, la transformación ocurre fuera del Aggregate.

Conceptualmente:

```text
Proposal Domain Event

↓

Integration Event

↓

Mapper

↓

External Representation
```

Proposal no conoce:

```text
NGSI-LD

Orion-LD

Keyrock

PEP Proxy
```

La interoperabilidad no modifica el modelo conceptual interno de
Proposal.

---

# Ejemplo — Cambio de Infraestructura

## Given

Proposal se encuentra persistida utilizando un mecanismo de
almacenamiento.

## When

la infraestructura cambia desde:

```text
PostgreSQL
```

hacia:

```text
MongoDB
```

o hacia otro mecanismo compatible.

## Then

el modelo conceptual de Proposal permanece sin cambios.

No deben modificarse por esta razón:

```text
ProposalId

ProposalStatus

Lifecycle

State Machine

Commands

Domain Events

Invariants

Permissions

Version
```

---

# Ejemplo — Cambio de Proveedor de Identidad

## Given

la autorización utiliza un proveedor determinado.

## When

la infraestructura cambia de proveedor.

## Then

las capacidades conceptuales continúan siendo:

```text
proposal:create

proposal:read

proposal:rename

proposal:change-purpose

proposal:change-description

proposal:change-type

proposal:update-content

proposal:change-territory

proposal:associate-assembly

proposal:submit

proposal:start-review

proposal:accept

proposal:reject

proposal:withdraw

proposal:archive
```

Proposal no necesita cambiar debido al proveedor técnico de
identidad.

---

# Ejemplo — Role no Codificado en Proposal

## Given

una Organization utiliza un Role denominado:

```text
Presidente
```

y otra utiliza:

```text
Coordinador General
```

Ambos pueden recibir:

```text
proposal:accept
```

según las reglas organizacionales.

Proposal no debe implementar:

```text
if RoleName == "Presidente"
```

ni:

```text
if RoleName == "Coordinador General"
```

Debe recibir una intención previamente autorizada.

---

# Ejemplo — Membership no Otorga Autoridad Ilimitada

## Given

un Citizen posee una Membership activa dentro de una
Organization.

## Then

esto no implica automáticamente:

```text
proposal:accept

proposal:reject

proposal:archive
```

Las capacidades deben resolverse mediante el modelo de
autorización correspondiente.

Debe mantenerse:

```text
Membership

≠

Unlimited Proposal Authority
```

---

# Ejemplo — Aggregate no Confía en la Autorización para sus Invariantes

## Given

la capa de autorización acepta:

```text
proposal:accept
```

## When

Proposal recibe:

```text
AcceptProposal
```

## Then

Proposal todavía debe validar:

```text
ProposalStatus

Invariant Conditions

Version Conditions
```

La autorización no sustituye la protección interna del
Aggregate.

---

# Ejemplo — Operación Rechazada no Incrementa Version

## Given

```text
ProposalStatus = Submitted

Version = 14
```

## When

se intenta:

```text
RenameProposal
```

## Then

la operación es rechazada.

Debe mantenerse:

```text
Version = 14
```

No debe producirse:

```text
Version = 15
```

por una operación inválida.

---

# Ejemplo — Operación Rechazada no Produce Evento de Éxito

## Given

```text
ProposalStatus = Draft
```

## When

se intenta:

```text
AcceptProposal
```

## Then

la operación es rechazada.

No debe producirse:

```text
ProposalAccepted
```

Debe mantenerse:

```text
Rejected Command

↓

No Success Domain Event
```

---

# Ejemplo — Una Operación Válida Incrementa Version

## Given

```text
ProposalStatus = Draft

Version = 30
```

## When

un Command válido modifica el Aggregate.

## Then

Version debe avanzar:

```text
30 → 31
```

La modificación y Version forman parte del mismo cambio lógico
del Aggregate.

---

# Ejemplo — Version no Puede Modificarse Directamente

## Given

```text
Version = 31
```

## When

un consumidor intenta establecer:

```text
Version = 100
```

sin ejecutar una modificación válida del Aggregate.

## Then

la operación debe ser rechazada.

Version no constituye un atributo administrativo libremente
editable.

---

# Ejemplo — Estado no Puede Modificarse Directamente

## Given

```text
ProposalStatus = Draft
```

## When

un consumidor intenta asignar directamente:

```text
ProposalStatus = Accepted
```

## Then

la operación debe ser rechazada.

La transición válida requiere:

```text
Draft

↓

Submitted

↓

UnderReview

↓

Accepted
```

según el Lifecycle establecido.

---

# Ejemplo — Flujo Completo de Proposal Aceptada

```text
CreateProposal
    │
    ▼
Draft
    │
    │ edit
    │ rename
    │ update content
    │ associate context
    │
    ▼
SubmitProposal
    │
    ▼
Submitted
    │
    ▼
StartProposalReview
    │
    ▼
UnderReview
    │
    ▼
AcceptProposal
    │
    ▼
Accepted
    │
    ▼
ArchiveProposal
    │
    ▼
Archived
```

Eventos conceptuales correspondientes:

```text
ProposalCreated

↓

ProposalSubmitted

↓

ProposalReviewStarted

↓

ProposalAccepted

↓

ProposalArchived
```

Entre estas transiciones pueden producirse eventos de
modificación válidos mientras el estado correspondiente lo
permita.

---

# Ejemplo — Flujo Completo de Proposal Rechazada

```text
CreateProposal

↓

Draft

↓

SubmitProposal

↓

Submitted

↓

StartProposalReview

↓

UnderReview

↓

RejectProposal

↓

Rejected

↓

ArchiveProposal

↓

Archived
```

Eventos principales:

```text
ProposalCreated

ProposalSubmitted

ProposalReviewStarted

ProposalRejected

ProposalArchived
```

---

# Ejemplo — Flujo de Proposal Retirada desde Draft

```text
CreateProposal

↓

Draft

↓

WithdrawProposal

↓

Withdrawn

↓

ArchiveProposal

↓

Archived
```

Eventos principales:

```text
ProposalCreated

ProposalWithdrawn

ProposalArchived
```

---

# Ejemplo — Flujo de Proposal Retirada después de Presentación

```text
CreateProposal

↓

Draft

↓

SubmitProposal

↓

Submitted

↓

WithdrawProposal

↓

Withdrawn

↓

ArchiveProposal

↓

Archived
```

Una vez iniciada formalmente la revisión:

```text
UnderReview
```

el flujo de retiro definido para Draft y Submitted deja de estar
disponible.

---

# Ejemplo — Flujo Inválido

El siguiente flujo no está permitido:

```text
Draft

↓

Accepted
```

Tampoco:

```text
Submitted

↓

Accepted
```

Tampoco:

```text
UnderReview

↓

Withdrawn
```

Tampoco:

```text
Archived

↓

Draft
```

Tampoco:

```text
Accepted

↓

Rejected
```

Estas secuencias violan el Lifecycle o la State Machine definida
para Proposal.

---

# Ejemplo — No Absorción de Aggregates

Una Proposal puede relacionarse conceptualmente con:

```text
Organization

Citizen

Territory

Assembly

Participation

Voting

Document

Notification

Audit

Integration
```

pero debe mantener:

```text
Proposal
    │
    ├── OrganizationId
    ├── AuthorId
    ├── TerritoryId
    └── AssemblyId
```

y relaciones externas mediante contratos o eventos cuando
corresponda.

No debe transformarse en:

```text
Proposal
    ├── Organization Aggregate
    ├── Citizen Aggregate
    ├── Territory Aggregate
    ├── Assembly Aggregate
    ├── Participation Aggregate
    ├── Voting Aggregate
    ├── Document Aggregate
    ├── Notification Aggregate
    └── Audit Aggregate
```

---

# Ejemplo — Límite de Consistencia

Una modificación válida sobre Proposal puede cambiar:

```text
ProposalName

ProposalPurpose

ProposalDescription

ProposalContent

ProposalType

TerritoryId

AssemblyId

ProposalStatus

Version
```

según las reglas correspondientes.

La misma transacción del Aggregate no debe modificar
directamente:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Participation

Voting

Document

Notification

Audit

Integration
```

---

# Ejemplo — Consistencia Eventual

Una Proposal aceptada puede requerir que otros contextos conozcan
el hecho.

Conceptualmente:

```text
Proposal

↓

ProposalAccepted

↓

Commit

↓

Integration Event

↓

Other Bounded Context
```

El otro contexto puede actualizar posteriormente su propio
estado.

No es necesario ampliar el límite transaccional de Proposal para
incluir al consumidor.

---

# Ejemplo — Fallo de Persistencia

## Given

Proposal ejecuta una modificación válida localmente.

## When

```text
ProposalRepository.save()
```

no logra completar el commit.

## Then

la modificación no debe considerarse persistida.

Los eventos asociados no deben considerarse confirmados para
publicación externa antes de la confirmación correspondiente de
persistencia.

Debe mantenerse:

```text
Persistence Failure

↓

No Confirmed External Effect
```

---

# Ejemplo — Rehidratación

## Given

una Proposal existente posee:

```text
ProposalStatus = Accepted

Version = 42
```

## When

el Repository reconstruye el Aggregate desde persistencia.

## Then

Proposal vuelve a memoria con:

```text
ProposalStatus = Accepted

Version = 42
```

La reconstrucción no ejecuta:

```text
CreateProposal
```

No produce:

```text
ProposalCreated
```

No incrementa Version.

No reinicia el Lifecycle.

---

# Ejemplo — Event Sourcing

Cuando la infraestructura utilice Event Sourcing, una Proposal
puede reconstruirse conceptualmente mediante:

```text
ProposalCreated

↓

ProposalRenamed

↓

ProposalSubmitted

↓

ProposalReviewStarted

↓

ProposalAccepted
```

produciendo finalmente:

```text
ProposalStatus = Accepted
```

La reproducción histórica de estos eventos no debe publicarlos
nuevamente como hechos actuales.

Debe mantenerse:

```text
Replay

≠

New Event Publication
```

---

# Ejemplo — Consulta mediante Read Model

Una interfaz necesita mostrar:

```text
ProposalName

ProposalStatus

ProposalType

TerritoryId
```

La consulta puede utilizar:

```text
ProposalSummary
```

sin cargar el Aggregate completo.

Conceptualmente:

```text
Query

↓

Proposal Read Model

↓

Result
```

No:

```text
Query

↓

Modify Proposal
```

Los Read Models son de solo lectura.

---

# Ejemplo — Consulta no Incrementa Version

## Given

```text
Proposal.Version = 50
```

## When

la Proposal es consultada.

## Then

debe mantenerse:

```text
Version = 50
```

Las lecturas no constituyen modificaciones del Aggregate.

---

# Ejemplo — Escenario Comunitario

Una Organization comunitaria desea presentar una iniciativa para
mejorar la iluminación de un espacio común.

El flujo conceptual puede ser:

```text
Citizen / Member

↓

CreateProposal

↓

Proposal
Draft

↓

Edit Proposal

↓

SubmitProposal

↓

Submitted

↓

Authorized Reviewer

↓

StartProposalReview

↓

UnderReview

↓

Decision Authority

↓

AcceptProposal

↓

Accepted
```

Posteriormente otros Aggregates o Bounded Contexts pueden
utilizar:

```text
ProposalId
```

para desarrollar procesos adicionales.

Proposal no absorbe esos procesos.

---

# Ejemplo — Proposal Territorial

Una Proposal puede referirse a:

```text
TerritoryId = territory-sector-01
```

para expresar el contexto territorial de la iniciativa.

La Proposal puede representar conceptualmente:

```text
Nombre:
Recuperación de plaza comunitaria

Territorio:
territory-sector-01
```

La Proposal no modifica:

- geometría territorial;
- límites;
- jerarquía;
- clasificación;
- estado del Territory.

Esas responsabilidades continúan perteneciendo a Territory.

---

# Ejemplo — Proposal Asociada a Assembly

Una Organization puede discutir una Proposal dentro del contexto
de una Assembly.

Conceptualmente:

```text
ProposalId:
proposal-001

AssemblyId:
assembly-010
```

Esto permite relacionar ambos conceptos.

No significa que Proposal controle:

```text
AssemblyStatus
```

ni que Assembly controle directamente:

```text
ProposalStatus
```

Cada Aggregate protege su propio estado.

---

# Ejemplo — Proposal Aceptada no Ejecuta Voting

Una Proposal puede alcanzar:

```text
Accepted
```

sin que Proposal ejecute directamente un Voting.

Si posteriormente el dominio requiere una votación, Voting debe
mantener su propia:

- identidad;
- State Machine;
- Lifecycle;
- Commands;
- Domain Events;
- invariantes;
- Repository.

Debe mantenerse:

```text
Proposal Accepted

≠

Voting Executed
```

---

# Ejemplo — Proposal Submitted no Significa Notification Sent

Cuando ocurre:

```text
ProposalSubmitted
```

puede existir una reacción posterior que genere una Notification.

Sin embargo:

```text
ProposalSubmitted

≠

NotificationSent
```

Proposal únicamente declara el hecho perteneciente a su dominio.

---

# Ejemplo — Proposal Accepted no Significa Integration Completed

Cuando ocurre:

```text
ProposalAccepted
```

puede generarse posteriormente un Integration Event.

Pero debe mantenerse:

```text
ProposalAccepted

≠

External System Updated
```

El estado del sistema externo pertenece a otra responsabilidad.

---

# Ejemplo — Trazabilidad

Un Command puede incluir conceptualmente:

```text
CommandId:
command-100

ProposalId:
proposal-001

OrganizationId:
organization-001

ActorId:
citizen-001

Timestamp:
2026-08-12T16:00:00Z

CorrelationId:
correlation-500

CausationId:
command-099
```

Estos datos permiten relacionar:

```text
Intent

↓

Aggregate Change

↓

Domain Event

↓

Subsequent Processing
```

sin convertir Audit en parte interna de Proposal.

---

# Ejemplo — Causalidad

Un flujo puede producir:

```text
SubmitProposal
```

que genera:

```text
ProposalSubmitted
```

Posteriormente otro proceso puede reaccionar al evento.

La relación conceptual puede conservar:

```text
CorrelationId

CausationId
```

permitiendo seguir la cadena causal sin acoplar Proposal al
consumidor.

---

# Ejemplo — Operación Administrativa no Evita Reglas

## Given

un actor administrativo posee:

```text
proposal:archive
```

pero Proposal se encuentra:

```text
Draft
```

## When

intenta ejecutar:

```text
ArchiveProposal
```

## Then

la operación es rechazada.

Debe mantenerse:

```text
Administrator

≠

Bypass Domain Rules
```

---

# Ejemplo — SystemActor no Evita Reglas

## Given

un proceso automático posee una capacidad válida.

## When

ejecuta un Command sobre Proposal.

## Then

Proposal aplica exactamente las mismas:

- invariantes;
- reglas de estado;
- reglas de Version;
- restricciones del Aggregate.

Debe mantenerse:

```text
SystemActor

≠

Bypass Domain
```

---

# Ejemplo — Error de Dominio no es Error de Persistencia

Una operación:

```text
AcceptProposal
```

ejecutada sobre:

```text
ProposalStatus = Draft
```

produce un rechazo del dominio.

No representa:

```text
ProposalPersistenceFailure
```

ni:

```text
ProposalConcurrencyConflict
```

La causa corresponde a una transición inválida.

Las categorías de error deben permanecer separadas.

---

# Ejemplo — Error de Persistencia no es Invariante

Una Proposal puede encontrarse en un estado válido después de
ejecutar un Command.

Si el mecanismo de almacenamiento falla durante:

```text
save()
```

el problema pertenece a persistencia.

No debe reinterpretarse como:

```text
ProposalInvariantViolation
```

La separación permite mantener responsabilidades claras.

---

# Ejemplo — Error de Autorización no es Error de Dominio

Un actor sin:

```text
proposal:accept
```

no debe ejecutar legítimamente:

```text
AcceptProposal
```

La denegación pertenece a autorización.

No debe utilizarse una falsa invariante del Aggregate para
representar la ausencia de permiso.

Debe mantenerse:

```text
Authorization Failure

≠

Domain Invariant Failure
```

---

# Ejemplo — Identidad Persistente

Una Proposal puede evolucionar:

```text
Draft

↓

Submitted

↓

UnderReview

↓

Accepted

↓

Archived
```

Durante todo el flujo:

```text
ProposalId = proposal-001
```

permanece constante.

El estado cambia.

La identidad no cambia.

---

# Ejemplo — Organization Persistente

Durante todo el ciclo de vida:

```text
OrganizationId = organization-001
```

permanece inmutable.

Una Proposal no puede ser trasladada a otra Organization mediante
una modificación ordinaria del Aggregate.

---

# Ejemplo — Evolución de Version

Un flujo conceptual puede mostrar:

```text
ProposalCreated
Version = 1

↓

ProposalRenamed
Version = 2

↓

ProposalContentUpdated
Version = 3

↓

ProposalSubmitted
Version = 4

↓

ProposalReviewStarted
Version = 5

↓

ProposalAccepted
Version = 6

↓

ProposalArchived
Version = 7
```

Los números son ilustrativos.

La regla relevante es:

```text
Valid Modification

↓

Version Increases
```

---

# Ejemplo — Lectura entre Modificaciones

Si:

```text
Version = 6
```

y se realizan múltiples consultas sin modificar Proposal:

```text
Read

Read

Read
```

debe mantenerse:

```text
Version = 6
```

Version representa modificaciones válidas del Aggregate, no
cantidad de accesos.

---

# Ejemplo — Domain Event como Hecho Consumado

El Command:

```text
SubmitProposal
```

expresa intención.

El evento:

```text
ProposalSubmitted
```

expresa un hecho consumado.

Debe mantenerse:

```text
SubmitProposal

≠

ProposalSubmitted
```

El evento solo existe después de que el Aggregate acepta la
operación.

---

# Ejemplo — Command Rechazado

## Given

```text
ProposalStatus = Archived
```

## When

se ejecuta:

```text
RenameProposal
```

## Then

el Command es rechazado.

No se produce:

```text
ProposalRenamed
```

Debe mantenerse:

```text
Rejected Command

↓

No State Change

No Version Change

No Success Domain Event
```

---

# Ejemplo — Evento no Ejecuta el Command

Un evento histórico:

```text
ProposalAccepted
```

representa que la aceptación ya ocurrió.

No debe utilizarse como si fuera:

```text
AcceptProposal
```

Los eventos representan hechos.

Los Commands representan intención.

---

# Ejemplo — Secuencia Conceptual Completa

```text
Actor
    │
    ▼
Permission Check
    │
    ▼
Command
    │
    ▼
Application Service
    │
    ▼
ProposalRepository.getById()
    │
    ▼
Proposal Aggregate
    │
    ├── Validate State
    │
    ├── Validate Invariants
    │
    ├── Execute Behavior
    │
    ├── Increment Version
    │
    └── Produce Domain Event
    │
    ▼
ProposalRepository.save()
    │
    ├── Check ExpectedVersion
    │
    └── Persist Aggregate
    │
    ▼
Commit
    │
    ▼
Domain Event Processing
```

Este flujo representa la separación de responsabilidades
establecida por los documentos conceptuales de Proposal.

---

# Ejemplo — Flujo Rechazado por Autorización

```text
Actor
    │
    ▼
Permission Check
    │
    ▼
Denied
    │
    ▼
No Command Execution
    │
    ▼
Proposal Unchanged
```

---

# Ejemplo — Flujo Rechazado por Dominio

```text
Actor
    │
    ▼
Permission Granted
    │
    ▼
Command
    │
    ▼
Proposal
    │
    ▼
Invalid State or Invariant
    │
    ▼
Rejected
    │
    ▼
State Unchanged
Version Unchanged
No Success Domain Event
```

---

# Ejemplo — Flujo Rechazado por Concurrencia

```text
Actor
    │
    ▼
Permission Granted
    │
    ▼
Valid Command
    │
    ▼
Valid Local Aggregate Change
    │
    ▼
Repository.save()
    │
    ▼
ExpectedVersion ≠ PersistedVersion
    │
    ▼
ProposalConcurrencyConflict
    │
    ▼
Persisted Aggregate Unchanged
```

---

# Reglas Derivadas de los Ejemplos

Los ejemplos confirman las siguientes reglas ya establecidas por
el Aggregate:

- Proposal posee identidad propia;
- Proposal pertenece a una única Organization;
- ProposalId es inmutable;
- OrganizationId es inmutable;
- Proposal posee un Lifecycle explícito;
- las transiciones dependen de la State Machine;
- los Commands expresan intención;
- los Domain Events expresan hechos consumados;
- las operaciones requieren permisos cuando corresponda;
- los permisos no reemplazan las invariantes;
- los permisos no reemplazan la State Machine;
- los permisos no reemplazan Version;
- toda modificación válida incrementa Version;
- toda operación rechazada mantiene Version;
- toda operación rechazada mantiene el estado previo;
- un Command rechazado no produce un Domain Event de éxito;
- ProposalRepository persiste el Aggregate completo;
- ExpectedVersion protege contra modificaciones concurrentes;
- Last Write Wins no reemplaza el control de concurrencia;
- Archived no equivale a eliminación física;
- Proposal no absorbe otros Aggregates;
- Read Models no modifican Proposal;
- Integration permanece fuera del Aggregate;
- Infrastructure permanece fuera del dominio.

Estas reglas no son creadas por este documento.

Los ejemplos únicamente muestran su aplicación conceptual.

---

# Restricciones de los Ejemplos

Los ejemplos de este documento no deben utilizarse para:

- introducir nuevos estados;
- introducir nuevas transiciones;
- introducir nuevos Commands;
- introducir nuevos Domain Events;
- introducir nuevos permisos;
- modificar invariantes;
- ampliar el límite de consistencia;
- absorber otros Aggregates;
- definir tecnologías de persistencia;
- definir endpoints;
- definir protocolos;
- reemplazar los documentos normativos.

Cuando se necesite modificar una regla del Aggregate, debe
actualizarse primero el documento normativo correspondiente.

---

# Relación con Aggregate

La definición conceptual principal permanece en:

```text
DOMAIN-007-Aggregate.md
```

Los ejemplos deben permanecer consistentes con esa definición.

---

# Relación con Lifecycle

Los escenarios de transición deben respetar:

```text
DOMAIN-007A-Lifecycle.md
```

No puede existir en este documento un flujo que contradiga el
Lifecycle oficial.

---

# Relación con State Machine

Las transiciones utilizadas por los ejemplos deben corresponder
a:

```text
DOMAIN-007B-State-Machine.md
```

Los ejemplos no pueden crear transiciones adicionales.

---

# Relación con Commands

Los Commands utilizados en los escenarios deben corresponder a:

```text
DOMAIN-007C-Commands.md
```

Los ejemplos no definen Commands nuevos.

---

# Relación con Domain Events

Los eventos utilizados deben corresponder a:

```text
DOMAIN-007D-Domain-Events.md
```

Los ejemplos no sustituyen la definición formal de sus
estructuras.

---

# Relación con Invariantes

Todos los escenarios deben respetar:

```text
DOMAIN-007E-Invariants.md
```

Un escenario exitoso nunca puede depender de violar una
invariante.

---

# Relación con Permissions

Los actores y capacidades utilizados deben respetar:

```text
DOMAIN-007F-Permissions.md
```

Los ejemplos no otorgan permisos por sí mismos.

---

# Relación con Repository Contract

Los escenarios de persistencia deben respetar:

```text
DOMAIN-007G-Repository-Contract.md
```

El Repository no puede utilizarse para evitar comportamiento del
Aggregate.

---

# Relación con Versioning

Los ejemplos de Version deben permanecer consistentes con:

```text
DOMAIN-007I-Versioning.md
```

Toda modificación válida debe respetar el mecanismo oficial de
versionado.

---

# Relación con Consistency Boundary

Los ejemplos deben mantener el límite establecido en:

```text
DOMAIN-007J-Consistency-Boundary.md
```

Ningún escenario puede convertir otro Aggregate en parte interna
de Proposal.

---

# Documentación Complementaria

Los ejemplos deben interpretarse conjuntamente con:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007D-Domain-Events.md

DOMAIN-007E-Invariants.md

DOMAIN-007F-Permissions.md

DOMAIN-007G-Repository-Contract.md

DOMAIN-007I-Versioning.md

DOMAIN-007J-Consistency-Boundary.md

DOMAIN-007K-Integration-Events.md

DOMAIN-007L-Read-Model.md

DOMAIN-007M-Test-Scenarios.md

DOMAIN-007N-Performance-Rules.md

DOMAIN-007O-Security-Model.md

DOMAIN-007P-Extension-Points.md
```

Estos documentos constituyen la definición complementaria del
Aggregate Proposal y deben mantenerse conceptualmente
consistentes entre sí.

---

# Compatibilidad Arquitectónica

Los ejemplos documentados son compatibles con:

- Domain-Driven Design;
- Clean Architecture;
- Hexagonal Architecture;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Repository Pattern;
- Optimistic Concurrency Control;
- arquitectura distribuida;
- interoperabilidad basada en contratos.

Los ejemplos permanecen independientes de la tecnología utilizada
para implementar estas capacidades.

---

# Principios Arquitectónicos

Los escenarios de este documento mantienen:

```text
Command

≠

Domain Event
```

```text
Permission Granted

≠

Operation Guaranteed
```

```text
Valid Permission

+

Invalid State

=

Rejected Operation
```

```text
Valid Command

+

Invariant Violation

=

Rejected Operation
```

```text
Valid Local Change

+

Version Conflict

=

Rejected Persistence
```

```text
Rejected Operation

=

State Unchanged
+
Version Unchanged
+
No Success Domain Event
```

```text
Proposal

≠

Assembly
```

```text
Proposal

≠

Participation
```

```text
Proposal

≠

Voting
```

```text
Proposal

≠

Document
```

```text
Proposal

≠

Notification
```

```text
Proposal

≠

Audit
```

```text
Proposal

≠

Integration
```

```text
Repository Reconstruction

≠

Domain Creation
```

```text
Archived

≠

Deleted
```

```text
Read Model

≠

Aggregate
```

Estos principios permiten utilizar los ejemplos sin alterar los
límites conceptuales establecidos para Proposal.

---

# Definición de Éxito

**DOMAIN-007H-Examples.md** constituye la referencia oficial de
ejemplos conceptuales del Aggregate **Proposal** dentro de AURA
Core.

Los escenarios documentados permiten observar de forma concreta
la aplicación de:

```text
Lifecycle

State Machine

Commands

Domain Events

Invariants

Permissions

Repository Contract

Versioning

Consistency Boundary
```

sin introducir reglas nuevas ni sustituir los documentos
normativos correspondientes.

Los ejemplos demuestran que Proposal mantiene el flujo:

```text
Actor

↓

Permission

↓

Command

↓

Proposal Aggregate

↓

State Validation

↓

Invariant Validation

↓

Domain Behavior

↓

Version Increment

↓

Domain Event

↓

Repository

↓

ExpectedVersion Validation

↓

Persistence
```

y que cualquier operación inválida mantiene:

```text
State
    =
Unchanged
```

```text
Version
    =
Unchanged
```

```text
Success Domain Event
    =
Not Produced
```

Los escenarios también confirman que Proposal conserva su límite
de consistencia y se relaciona con otros Aggregates mediante
identificadores, eventos y contratos sin absorber sus
responsabilidades.

De esta forma, los ejemplos proporcionan una representación
coherente, trazable y tecnológicamente independiente del
comportamiento esperado de Proposal, manteniendo íntegramente el
patrón DDD consolidado para AURA Core.