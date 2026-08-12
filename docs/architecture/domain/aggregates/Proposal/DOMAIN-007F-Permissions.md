# DOMAIN-007F — Proposal Permissions

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
- DOMAIN-007G-Repository-Contract.md
- DOMAIN-007J-Consistency-Boundary.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir el modelo conceptual oficial de permisos aplicable al
Aggregate **Proposal**.

Los permisos determinan qué actores pueden intentar ejecutar
Commands sobre una Proposal.

Este documento establece:

- principios de autorización;
- relación entre permisos y Commands;
- relación entre permisos e invariantes;
- relación entre permisos y estado;
- actores conceptuales;
- capacidades sobre Proposal;
- restricciones de autorización;
- reglas para creación;
- reglas para edición;
- reglas para presentación;
- reglas para revisión;
- reglas para aceptación;
- reglas para rechazo;
- reglas para retiro;
- reglas para archivado;
- reglas para consulta;
- reglas de delegación;
- trazabilidad de autorización;
- separación entre autorización y dominio.

Los permisos no reemplazan las invariantes del Aggregate.

Un actor autorizado puede intentar una operación, pero Proposal
mantiene la autoridad final para determinar si esa operación es
válida según su estado, Lifecycle, State Machine e invariantes.

---

# Propósito

El modelo de permisos protege las operaciones que pueden
realizarse sobre Proposal sin introducir mecanismos técnicos de
autenticación o autorización dentro del Aggregate.

Conceptualmente:

```text
Actor

↓

Authorization

↓

Permission

↓

Command

↓

Proposal Aggregate

↓

Domain Validation

↓

State Change
```

La autorización determina:

```text
Who may attempt an operation?
```

Proposal determina:

```text
Can the operation occur while preserving the domain?
```

Ambas responsabilidades permanecen separadas.

---

# Principios

El modelo de permisos de Proposal cumple los siguientes
principios:

- los permisos expresan capacidades del dominio;
- los permisos se evalúan antes de ejecutar operaciones
  protegidas;
- un permiso no modifica directamente Proposal;
- un permiso no reemplaza una invariante;
- un permiso no reemplaza la State Machine;
- un permiso no reemplaza el Lifecycle;
- un permiso concedido no garantiza el éxito del Command;
- un actor puede poseer múltiples capacidades;
- una capacidad puede ser otorgada mediante diferentes Roles;
- los Roles pertenecen a su propio Aggregate;
- Membership mantiene su propio ciclo de vida;
- Proposal no administra Roles;
- Proposal no administra Memberships;
- Proposal no almacena credenciales;
- Proposal no autentica actores;
- Proposal no interpreta tokens;
- Proposal no administra sesiones;
- la autorización técnica permanece fuera del Aggregate.

---

# Separación entre Autenticación, Autorización y Dominio

El modelo distingue tres responsabilidades.

```text
Authentication

↓

Who is the actor?
```

```text
Authorization

↓

What may the actor attempt?
```

```text
Proposal Domain

↓

Is the requested operation valid?
```

Estas responsabilidades no deben mezclarse.

Proposal no autentica.

Proposal no resuelve credenciales.

Proposal no determina la validez de JWT.

Proposal no administra sesiones.

Proposal protege exclusivamente las reglas de dominio que
pertenecen a su límite de consistencia.

---

# Regla Fundamental

Debe mantenerse:

```text
Permission Granted
    ≠
Operation Guaranteed
```

Un permiso concedido significa únicamente:

```text
Actor may attempt Command
```

Después de la autorización:

```text
Proposal
```

debe validar:

- estado actual;
- transición solicitada;
- precondiciones;
- invariantes;
- consistencia;
- ExpectedVersion cuando corresponda.

Por lo tanto:

```text
Authorized Command

↓

Domain Validation

↓

Accepted
```

o:

```text
Authorized Command

↓

Domain Validation

↓

Rejected
```

---

# Regla de Denegación

Cuando un actor no posee la capacidad requerida:

```text
Permission Denied
```

el Command no debe alcanzar una modificación válida del
Aggregate.

Debe mantenerse:

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

La ausencia de permiso impide intentar legítimamente la
operación protegida.

---

# Actores Conceptuales

Proposal puede ser utilizado por diferentes actores del dominio.

Entre los actores conceptuales pueden existir:

```text
Citizen

Member

ProposalAuthor

OrganizationRepresentative

Reviewer

DecisionAuthority

Administrator

SystemActor
```

Estos nombres representan responsabilidades conceptuales.

No constituyen necesariamente Roles persistidos con esos nombres.

La capacidad efectiva de un actor depende de:

- Organization;
- Membership;
- Role;
- estado de Membership;
- permisos otorgados;
- contexto de Proposal;
- operación solicitada;
- políticas aplicables.

---

# Actor

Toda operación protegida debe encontrarse asociada a un actor
identificable.

Conceptualmente:

```text
ActorId
```

ActorId permite establecer quién intenta realizar la operación.

ActorId:

- no sustituye CitizenId;
- no sustituye MembershipId;
- no sustituye RoleId;
- no convierte al actor en entidad interna de Proposal;
- permite mantener trazabilidad de la intención.

---

# Contexto Organizacional

Toda autorización sobre Proposal debe respetar el contexto de:

```text
OrganizationId
```

La Proposal pertenece a una única Organization.

Por lo tanto, una capacidad concedida dentro de una Organization
no debe interpretarse automáticamente como válida sobre
Proposals pertenecientes a otra Organization.

Debe mantenerse:

```text
Permission Context.OrganizationId
    =
Proposal.OrganizationId
```

cuando la autorización depende del contexto organizacional.

---

# Membership como Contexto de Autorización

Cuando la autorización dependa de pertenencia organizacional,
puede utilizarse:

```text
MembershipId
```

Membership determina la relación entre:

```text
Citizen

and

Organization
```

Proposal no valida internamente el ciclo de vida completo de
Membership.

La capa responsable de autorización debe determinar que la
Membership utilizada para autorizar una operación sea válida
conforme a las reglas correspondientes.

Proposal recibe una intención previamente autorizada y protege
sus propias invariantes.

---

# Role como Contexto de Autorización

Los Roles pueden proporcionar capacidades dentro de una
Organization.

Conceptualmente:

```text
Membership

↓

Role

↓

Permission

↓

Command
```

Proposal no administra:

```text
Role
```

ni:

```text
Permission Assignment
```

La relación entre Role y Permission pertenece al modelo de
autorización.

Proposal únicamente recibe Commands cuya ejecución ha sido
autorizada por la capa correspondiente.

---

# Capacidades Oficiales

Las capacidades conceptuales asociadas a Proposal son:

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

Estas capacidades expresan acciones del dominio.

No representan:

- endpoints;
- scopes OAuth;
- claims JWT;
- rutas HTTP;
- nombres de tablas;
- políticas específicas de un proveedor.

La infraestructura puede mapear estas capacidades hacia
mecanismos técnicos sin alterar su significado conceptual.

---

# Permiso de Creación

La creación de Proposal requiere:

```text
proposal:create
```

El permiso autoriza intentar:

```text
CreateProposal
```

La autorización debe considerar el contexto:

```text
OrganizationId
```

La creación continúa sujeta a:

- datos iniciales válidos;
- Organization válida;
- reglas de identidad;
- invariantes iniciales;
- reglas establecidas por Proposal.

Cuando la operación es válida:

```text
Nonexistent

↓

Draft
```

y se produce:

```text
ProposalCreated
```

---

# Permiso de Lectura

La consulta de Proposal requiere conceptualmente:

```text
proposal:read
```

La lectura:

- no modifica Proposal;
- no incrementa Version;
- no produce Domain Events de modificación;
- puede estar limitada por Organization;
- puede estar limitada por políticas de privacidad;
- puede utilizar Read Models.

El permiso de lectura no implica capacidad de modificación.

Debe mantenerse:

```text
proposal:read

≠

proposal:update-content
```

---

# Permiso de Renombrado

La modificación del nombre requiere:

```text
proposal:rename
```

y corresponde al Command:

```text
RenameProposal
```

Además del permiso:

```text
ProposalStatus = Draft
```

debe cumplirse.

Por lo tanto:

```text
proposal:rename
+
Draft
+
Valid ProposalName
+
Valid Invariants

↓

ProposalRenamed
```

Un actor con `proposal:rename` no puede renombrar una Proposal
en Submitted, UnderReview, Accepted, Rejected, Withdrawn o
Archived.

---

# Permiso de Cambio de Propósito

La modificación del propósito requiere:

```text
proposal:change-purpose
```

y corresponde a:

```text
ChangeProposalPurpose
```

Debe cumplirse:

```text
ProposalStatus = Draft
```

El permiso no permite modificar ProposalPurpose después de la
presentación formal.

---

# Permiso de Cambio de Descripción

La modificación de la descripción requiere:

```text
proposal:change-description
```

y corresponde a:

```text
ChangeProposalDescription
```

Debe cumplirse:

```text
ProposalStatus = Draft
```

La capacidad autoriza la intención de modificar la descripción,
pero Proposal debe validar el nuevo valor antes de aceptar el
cambio.

---

# Permiso de Cambio de Tipo

La modificación de ProposalType requiere:

```text
proposal:change-type
```

y corresponde a:

```text
ChangeProposalType
```

Debe cumplirse:

```text
ProposalStatus = Draft
```

El actor autorizado no puede utilizar esta capacidad para cambiar
el tipo después de la presentación formal.

---

# Permiso de Actualización de Contenido

La actualización del contenido requiere:

```text
proposal:update-content
```

y corresponde a:

```text
UpdateProposalContent
```

Debe cumplirse:

```text
ProposalStatus = Draft
```

El contenido actualizado debe satisfacer las invariantes
correspondientes.

El permiso no permite:

- modificar ProposalId;
- modificar OrganizationId;
- modificar ProposalStatus;
- modificar Version;
- modificar otros Aggregates.

---

# Permiso de Cambio Territorial

La modificación de la referencia territorial requiere:

```text
proposal:change-territory
```

y corresponde a:

```text
ChangeProposalTerritory
```

Debe cumplirse:

```text
ProposalStatus = Draft
```

La autorización permite modificar únicamente:

```text
Proposal.TerritoryId
```

No autoriza modificar:

```text
Territory Aggregate
```

---

# Permiso de Asociación con Assembly

La asociación de Proposal con una Assembly requiere:

```text
proposal:associate-assembly
```

y corresponde a:

```text
AssociateProposalAssembly
```

Debe cumplirse:

```text
ProposalStatus = Draft
```

El permiso permite establecer una referencia mediante:

```text
AssemblyId
```

No permite modificar:

```text
Assembly
```

ni su:

- estado;
- programación;
- convocatoria;
- modalidad;
- Lifecycle.

---

# Permiso de Presentación

La presentación formal requiere:

```text
proposal:submit
```

y corresponde a:

```text
SubmitProposal
```

El permiso solo puede producir una modificación válida cuando:

```text
ProposalStatus = Draft
```

y todas las condiciones de presentación se encuentran
satisfechas.

Conceptualmente:

```text
proposal:submit

+

Draft

+

Valid Proposal

↓

Submitted
```

El evento esperado es:

```text
ProposalSubmitted
```

---

# Autor de Proposal

Cuando las reglas organizacionales permitan que el autor
administre su propia Proposal durante Draft, las capacidades
pueden estar asociadas conceptualmente al contexto de autoría.

Ejemplo:

```text
ProposalAuthor

↓

proposal:rename

proposal:change-purpose

proposal:change-description

proposal:change-type

proposal:update-content

proposal:change-territory

proposal:associate-assembly

proposal:submit

proposal:withdraw
```

La condición de autor no sustituye las reglas organizacionales.

La autorización efectiva debe respetar el contexto de
Organization y las políticas establecidas.

---

# Permiso de Inicio de Revisión

El inicio formal de revisión requiere:

```text
proposal:start-review
```

y corresponde a:

```text
StartProposalReview
```

Debe cumplirse:

```text
ProposalStatus = Submitted
```

Conceptualmente:

```text
Authorized Reviewer

↓

StartProposalReview

↓

Submitted → UnderReview
```

El evento esperado es:

```text
ProposalReviewStarted
```

La capacidad no permite aceptar o rechazar automáticamente la
Proposal.

---

# Reviewer

Reviewer representa un actor autorizado para participar en el
proceso formal de revisión.

Un Reviewer puede poseer:

```text
proposal:start-review
```

La capacidad de iniciar revisión no implica necesariamente:

```text
proposal:accept
```

ni:

```text
proposal:reject
```

Las capacidades deben permanecer explícitas.

---

# Permiso de Aceptación

La aceptación formal requiere:

```text
proposal:accept
```

y corresponde a:

```text
AcceptProposal
```

Debe cumplirse:

```text
ProposalStatus = UnderReview
```

Conceptualmente:

```text
proposal:accept

+

UnderReview

+

Valid Decision Conditions

↓

Accepted
```

El evento esperado es:

```text
ProposalAccepted
```

El permiso de aceptación no permite aceptar una Proposal desde:

```text
Draft

Submitted

Accepted

Rejected

Withdrawn

Archived
```

---

# Permiso de Rechazo

El rechazo formal requiere:

```text
proposal:reject
```

y corresponde a:

```text
RejectProposal
```

Debe cumplirse:

```text
ProposalStatus = UnderReview
```

Cuando el modelo requiera:

```text
RejectionReason
```

este debe satisfacer las reglas correspondientes.

Conceptualmente:

```text
proposal:reject

+

UnderReview

+

Valid Rejection Conditions

↓

Rejected
```

El evento esperado es:

```text
ProposalRejected
```

---

# Decision Authority

DecisionAuthority representa un actor con capacidad formal para
resolver una Proposal en revisión.

Conceptualmente puede poseer:

```text
proposal:accept

proposal:reject
```

La existencia de ambas capacidades no permite producir ambas
decisiones.

La State Machine y las invariantes garantizan:

```text
UnderReview

├────────► Accepted
│
└────────► Rejected
```

Una vez confirmada una transición, la otra deja de ser válida.

---

# Separación entre Reviewer y Decision Authority

El modelo permite distinguir conceptualmente:

```text
Reviewer
```

de:

```text
DecisionAuthority
```

Por ejemplo:

```text
Reviewer

↓

proposal:start-review
```

mientras:

```text
DecisionAuthority

↓

proposal:accept

proposal:reject
```

Esta separación permite representar organizaciones donde la
revisión y la decisión corresponden a responsabilidades
diferentes.

No obliga a que todas las Organizations utilicen Roles
diferentes.

La asignación concreta pertenece al modelo de autorización de
cada Organization.

---

# Permiso de Retiro

El retiro requiere:

```text
proposal:withdraw
```

y corresponde a:

```text
WithdrawProposal
```

El permiso puede utilizarse únicamente cuando:

```text
ProposalStatus = Draft
```

o:

```text
ProposalStatus = Submitted
```

No permite retirar una Proposal en:

```text
UnderReview

Accepted

Rejected

Withdrawn

Archived
```

Conceptualmente:

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

El evento esperado es:

```text
ProposalWithdrawn
```

---

# Autoría y Retiro

Cuando las reglas organizacionales permitan al autor retirar su
Proposal, debe mantenerse una relación de autorización válida
entre:

```text
ActorId
```

y la autoría correspondiente.

El hecho de poseer:

```text
proposal:withdraw
```

no elimina las restricciones del Lifecycle.

Una Proposal bajo revisión no puede retirarse mediante el flujo
establecido para Draft o Submitted.

---

# Permiso de Archivado

El archivado requiere:

```text
proposal:archive
```

y corresponde a:

```text
ArchiveProposal
```

Debe cumplirse que Proposal se encuentre en:

```text
Accepted
```

o:

```text
Rejected
```

o:

```text
Withdrawn
```

Conceptualmente:

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

El evento esperado es:

```text
ProposalArchived
```

---

# Administrator

Administrator representa conceptualmente un actor con
capacidades administrativas sobre Proposal.

Puede poseer un conjunto de capacidades como:

```text
proposal:read

proposal:start-review

proposal:archive
```

y otras capacidades cuando las reglas organizacionales así lo
establezcan.

Administrator no significa:

```text
Bypass Domain Rules
```

Un administrador no puede:

- modificar ProposalId;
- modificar OrganizationId;
- modificar Version directamente;
- realizar transiciones inválidas;
- modificar una Proposal archivada;
- ignorar invariantes;
- evitar control de concurrencia.

---

# SystemActor

Un SystemActor puede ejecutar operaciones automatizadas cuando
posea explícitamente la capacidad correspondiente.

Ejemplos conceptuales:

```text
Scheduled Process

Integration Process

Administrative Automation
```

El hecho de ser un proceso del sistema no concede autorización
ilimitada.

Debe mantenerse:

```text
SystemActor

↓

Explicit Permission

↓

Command

↓

Proposal Invariants
```

No:

```text
SystemActor

↓

Bypass Domain
```

---

# Matriz de Permisos por Command

```text
Command                      Required Permission
────────────────────────────────────────────────────────
CreateProposal               proposal:create

RenameProposal               proposal:rename

ChangeProposalPurpose        proposal:change-purpose

ChangeProposalDescription    proposal:change-description

ChangeProposalType           proposal:change-type

UpdateProposalContent        proposal:update-content

ChangeProposalTerritory      proposal:change-territory

AssociateProposalAssembly    proposal:associate-assembly

SubmitProposal               proposal:submit

StartProposalReview          proposal:start-review

AcceptProposal               proposal:accept

RejectProposal               proposal:reject

WithdrawProposal             proposal:withdraw

ArchiveProposal              proposal:archive
```

Las consultas utilizan:

```text
proposal:read
```

cuando las políticas de autorización requieran acceso protegido.

---

# Matriz de Permisos y Estados

```text
Permission                    Draft  Submitted  UnderReview  Accepted  Rejected  Withdrawn  Archived
────────────────────────────────────────────────────────────────────────────────────────────────────
proposal:read                   ✓        ✓           ✓           ✓         ✓          ✓         ✓

proposal:rename                 ✓        ✗           ✗           ✗         ✗          ✗         ✗

proposal:change-purpose         ✓        ✗           ✗           ✗         ✗          ✗         ✗

proposal:change-description     ✓        ✗           ✗           ✗         ✗          ✗         ✗

proposal:change-type            ✓        ✗           ✗           ✗         ✗          ✗         ✗

proposal:update-content         ✓        ✗           ✗           ✗         ✗          ✗         ✗

proposal:change-territory       ✓        ✗           ✗           ✗         ✗          ✗         ✗

proposal:associate-assembly     ✓        ✗           ✗           ✗         ✗          ✗         ✗

proposal:submit                 ✓        ✗           ✗           ✗         ✗          ✗         ✗

proposal:start-review           ✗        ✓           ✗           ✗         ✗          ✗         ✗

proposal:accept                 ✗        ✗           ✓           ✗         ✗          ✗         ✗

proposal:reject                 ✗        ✗           ✓           ✗         ✗          ✗         ✗

proposal:withdraw               ✓        ✓           ✗           ✗         ✗          ✗         ✗

proposal:archive                ✗        ✗           ✗           ✓         ✓          ✓         ✗
```

La matriz expresa simultáneamente:

- existencia de una capacidad;
- compatibilidad del Command con el estado.

Poseer una capacidad marcada como inválida para un estado no
permite evitar la State Machine.

---

# Matriz Conceptual de Actores

La siguiente matriz representa capacidades conceptuales posibles.

No constituye una asignación obligatoria de Roles para todas las
Organizations.

```text
Actor Conceptual            Capacidades posibles
────────────────────────────────────────────────────────────────
Citizen                     create, read

Member                      create, read

ProposalAuthor              read, edit, submit, withdraw

Reviewer                    read, start-review

DecisionAuthority           read, accept, reject

Administrator               read, review, archive

SystemActor                 capacidades explícitamente otorgadas
```

Las capacidades efectivas deben resolverse mediante el modelo de
autorización correspondiente.

---

# Regla de Mínimo Privilegio

Un actor debe recibir únicamente las capacidades necesarias para
cumplir su responsabilidad.

Debe preferirse:

```text
Required Permission Only
```

sobre:

```text
Unlimited Proposal Access
```

Por ejemplo, un actor encargado exclusivamente de revisión puede
poseer:

```text
proposal:read

proposal:start-review
```

sin poseer:

```text
proposal:accept

proposal:reject

proposal:archive
```

---

# Separación de Responsabilidades

Cuando las reglas organizacionales lo requieran, las capacidades
pueden distribuirse entre actores diferentes.

Ejemplo:

```text
ProposalAuthor
    │
    └── proposal:submit

Reviewer
    │
    └── proposal:start-review

DecisionAuthority
    │
    ├── proposal:accept
    └── proposal:reject

Administrator
    │
    └── proposal:archive
```

Esta separación permite mantener responsabilidades explícitas sin
introducirlas dentro del Aggregate Proposal.

---

# Permisos Compuestos

Un flujo completo puede requerir diferentes permisos en
diferentes momentos.

Ejemplo:

```text
CreateProposal
    │
    └── proposal:create
            │
            ▼
          Draft
            │
            ├── proposal:update-content
            │
            ├── proposal:rename
            │
            └── proposal:submit
                    │
                    ▼
                Submitted
                    │
                    └── proposal:start-review
                            │
                            ▼
                       UnderReview
                         │       │
             proposal:accept   proposal:reject
                         │       │
                         ▼       ▼
                     Accepted  Rejected
                         │       │
                         └──┬────┘
                            │
                    proposal:archive
                            │
                            ▼
                         Archived
```

Ningún permiso individual representa necesariamente autoridad
sobre todo el Lifecycle.

---

# Regla de Contexto

Un permiso debe evaluarse dentro del contexto en que fue
otorgado.

Conceptualmente:

```text
Permission

+

Actor

+

Organization

+

Proposal

+

Command

=

Authorization Decision
```

No debe asumirse:

```text
Permission Name

=

Global Unlimited Authority
```

---

# Regla de Propiedad Organizacional

Cuando una capacidad depende de Membership o Role dentro de una
Organization, debe existir correspondencia entre:

```text
Authorization.OrganizationId
```

y:

```text
Proposal.OrganizationId
```

Ejemplo inválido:

```text
Actor Membership
OrganizationId = Organization-A

Proposal
OrganizationId = Organization-B
```

La Membership de Organization-A no concede automáticamente
autoridad sobre Proposal de Organization-B.

---

# Regla de Autoría

Cuando una capacidad dependa de ser autor de Proposal, debe
existir correspondencia entre:

```text
ActorId
```

y la referencia de autoría utilizada por el dominio o por la capa
de autorización correspondiente.

No debe inferirse autoría exclusivamente porque un actor posea:

```text
proposal:read
```

o:

```text
proposal:create
```

La creación de una Proposal y la autoridad posterior sobre ella
son conceptos relacionados, pero no equivalentes.

---

# Delegación

Las capacidades pueden ser delegadas únicamente cuando el modelo
de autorización de la Organization lo permita.

Una delegación debe conservar:

- identidad del actor delegado;
- Organization;
- capacidades delegadas;
- alcance;
- vigencia cuando corresponda;
- trazabilidad.

La delegación no modifica Proposal.

Proposal no almacena la política completa de delegación.

---

# Restricciones de Delegación

Una delegación no puede:

- crear nuevas invariantes dentro de Proposal;
- modificar ProposalStatus;
- otorgar autoridad superior a la permitida por las reglas de
  autorización;
- evitar la State Machine;
- evitar el Lifecycle;
- evitar ExpectedVersion;
- permitir modificación de Archived;
- convertir un permiso en autoridad ilimitada.

Debe mantenerse:

```text
Delegated Permission

≤

Allowed Authorization Scope
```

---

# Permisos y Estado

La autorización y el estado deben evaluarse conjuntamente.

Ejemplo:

```text
Actor has proposal:accept
```

pero:

```text
ProposalStatus = Submitted
```

Resultado:

```text
AcceptProposal

↓

Rejected
```

porque la transición válida exige:

```text
ProposalStatus = UnderReview
```

Por lo tanto:

```text
Permission
+
Valid State
+
Valid Invariants

=

Potentially Valid Operation
```

---

# Permisos e Invariantes

Los permisos no pueden modificar las invariantes establecidas en:

```text
DOMAIN-007E-Invariants.md
```

Ejemplo:

```text
Actor has proposal:update-content
```

pero:

```text
ProposalStatus = Submitted
```

La operación continúa siendo inválida.

Otro ejemplo:

```text
Actor has proposal:archive
```

pero:

```text
ProposalStatus = Draft
```

La operación continúa siendo inválida.

---

# Permisos y State Machine

La State Machine definida en:

```text
DOMAIN-007B-State-Machine.md
```

mantiene autoridad sobre las transiciones posibles.

Los permisos únicamente determinan quién puede intentar cada
transición.

Conceptualmente:

```text
Permission

↓

May Attempt Transition
```

mientras:

```text
State Machine

↓

Determines Whether Transition Exists
```

---

# Permisos y Commands

Cada Command modificador debe poseer una capacidad explícita.

No debe existir un Command protegido cuyo acceso dependa
únicamente de convenciones implícitas.

Debe mantenerse:

```text
Command

↓

Required Permission

↓

Authorization Decision

↓

Aggregate Execution
```

La definición de Commands se encuentra en:

```text
DOMAIN-007C-Commands.md
```

---

# Permisos y Domain Events

Los permisos no producen Domain Events por sí mismos.

Debe mantenerse:

```text
Permission Granted

≠

Domain Event
```

El Domain Event ocurre únicamente después de una modificación
válida del Aggregate.

Ejemplo:

```text
proposal:accept granted

↓

AcceptProposal

↓

Proposal validates

↓

UnderReview → Accepted

↓

ProposalAccepted
```

Si la validación falla:

```text
ProposalAccepted
```

no se produce.

---

# Permisos y Versionado

La autorización no permite ignorar el control de concurrencia.

Un actor puede poseer:

```text
proposal:accept
```

pero si:

```text
ExpectedVersion
    ≠
CurrentVersion
```

la modificación debe ser rechazada.

Debe mantenerse:

```text
Permission Granted

+

Version Conflict

=

Operation Rejected
```

El modelo de versionado se desarrolla en:

```text
DOMAIN-007I-Versioning.md
```

---

# Permisos y Consistencia

La autorización no amplía el límite de consistencia de Proposal.

Un actor autorizado para:

```text
proposal:associate-assembly
```

puede solicitar modificar:

```text
Proposal.AssemblyId
```

pero no puede utilizar ese permiso para modificar:

```text
Assembly Aggregate
```

Del mismo modo:

```text
proposal:change-territory
```

no concede autoridad para modificar:

```text
Territory Aggregate
```

---

# Permisos y Otros Aggregates

Proposal puede utilizar referencias relacionadas con:

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

Los permisos definidos en este documento se aplican
exclusivamente a operaciones sobre Proposal.

No conceden automáticamente permisos sobre otros Aggregates.

Debe mantenerse:

```text
proposal:accept

≠

voting:open
```

```text
proposal:associate-assembly

≠

assembly:update
```

```text
proposal:change-territory

≠

territory:update
```

---

# Permisos de Consulta y Read Models

Los Read Models pueden aplicar reglas de autorización diferentes
según el consumidor.

Una consulta puede requerir:

```text
proposal:read
```

y además estar limitada por:

- Organization;
- Territory;
- Membership;
- visibilidad de Proposal;
- políticas de privacidad;
- contexto del consumidor.

Estas restricciones de lectura no modifican el Aggregate.

---

# Datos Expuestos

Poseer permiso de lectura no implica acceso irrestricto a toda
información relacionada con Proposal.

Los Read Models pueden exponer únicamente la información
autorizada para cada consumidor.

Conceptualmente pueden existir:

```text
Public Proposal View

Member Proposal View

Reviewer Proposal View

Administrative Proposal View
```

Estas vistas no modifican la fuente de verdad del dominio.

---

# Auditoría de Autorización

Toda operación modificadora debe permitir trazabilidad del actor
que la solicitó.

Conceptualmente:

```text
CommandId

ProposalId

OrganizationId

ActorId

Timestamp

CorrelationId

CausationId
```

pueden formar parte del contexto de ejecución.

La trazabilidad permite conocer:

```text
Who

Attempted What

On Which Proposal

Within Which Organization

When

Under Which Correlation
```

Proposal no necesita almacenar un sistema completo de auditoría
dentro del Aggregate.

---

# Intentos Denegados

Los intentos denegados por autorización pueden ser registrados
por los mecanismos de seguridad o Audit correspondientes.

Sin embargo:

```text
PermissionDenied
```

no constituye necesariamente un Domain Event de Proposal.

Si el Command no alcanza una modificación del Aggregate:

```text
Proposal State = Unchanged
```

y:

```text
Proposal Version = Unchanged
```

La observabilidad de intentos de acceso pertenece a los
mecanismos correspondientes fuera del Aggregate.

---

# Autorización Técnica

La implementación puede utilizar mecanismos técnicos como:

- OAuth2;
- OpenID Connect;
- JWT;
- API Gateway;
- PEP Proxy;
- Identity Provider;
- Policy Enforcement Point;
- Policy Decision Point.

Estos mecanismos pertenecen a Infrastructure o a los contextos
de seguridad correspondientes.

No forman parte del modelo interno de Proposal.

---

# Mapeo Técnico

Una implementación puede mapear:

```text
proposal:create
```

hacia un scope, claim, policy o mecanismo equivalente.

Sin embargo, el concepto oficial del dominio permanece:

```text
proposal:create
```

El mecanismo técnico puede cambiar sin modificar el significado
del permiso.

Debe mantenerse:

```text
Domain Permission

≠

Technology-Specific Representation
```

---

# Independencia de Keyrock

Cuando AURA utilice FIWARE Keyrock u otro proveedor de identidad,
Proposal no depende directamente de ese proveedor.

No debe existir dentro del Aggregate una regla como:

```text
if keyrock_role == ...
```

El dominio trabaja con capacidades conceptuales.

La traducción desde mecanismos externos hacia esas capacidades
pertenece a las capas correspondientes.

---

# Independencia de PEP Proxy

La existencia de un PEP Proxy puede proteger el acceso técnico a
servicios.

Sin embargo:

```text
PEP Authorization Success
```

no reemplaza:

```text
Proposal Domain Validation
```

Debe mantenerse:

```text
PEP Proxy

↓

Technical Access Decision

↓

Application Authorization

↓

Proposal Command

↓

Domain Invariants
```

---

# Independencia de JWT

Proposal no interpreta:

```text
JWT
```

ni conoce:

```text
issuer

audience

signature

expiration

claims
```

La capa de seguridad correspondiente transforma la identidad y
capacidades verificadas en un contexto de autorización que pueda
utilizar la aplicación.

El Aggregate permanece independiente del mecanismo de token.

---

# Regla de No Elevación de Privilegios

Una operación sobre Proposal no puede otorgar al actor permisos
adicionales sobre Proposal ni sobre otros Aggregates.

Ejemplo:

```text
AcceptProposal
```

no debe producir:

```text
Grant proposal:archive
```

La administración de capacidades pertenece al modelo de
autorización.

---

# Regla de No Autorización por Estado

El estado de Proposal no concede permisos por sí mismo.

Por ejemplo:

```text
ProposalStatus = UnderReview
```

no significa que cualquier actor pueda ejecutar:

```text
AcceptProposal
```

Debe existir simultáneamente:

```text
Required Permission
```

y:

```text
Valid State
```

---

# Regla de No Autorización por Referencia

La existencia de una relación con Proposal no concede
automáticamente permisos.

Por ejemplo:

```text
Actor referenced by Proposal
```

no implica:

```text
Actor may modify Proposal
```

Las capacidades deben determinarse mediante el modelo de
autorización correspondiente.

---

# Regla de No Autorización Implícita por Role

El nombre de un Role no debe codificarse directamente como regla
interna de Proposal.

No debe existir:

```text
if role.name == "President":
    accept proposal
```

El modelo correcto es:

```text
Role

↓

Authorization Mapping

↓

proposal:accept

↓

AcceptProposal
```

Esto mantiene Proposal desacoplado de la estructura concreta de
Roles de cada Organization.

---

# Regla de No Autorización Implícita por Membership

Poseer una Membership no concede automáticamente todas las
capacidades sobre Proposal.

Debe mantenerse:

```text
Active Membership

≠

Unlimited Proposal Permissions
```

Membership proporciona contexto organizacional.

Las capacidades específicas deben resolverse mediante las reglas
de autorización correspondientes.

---

# Flujo de Autorización

El flujo conceptual para un Command protegido es:

```text
Actor

↓

Authentication

↓

Actor Identity

↓

Organization Context

↓

Membership / Role Context

↓

Permission Resolution

↓

Permission Check

↓

Command

↓

Proposal Aggregate

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
```

Este flujo mantiene separadas las responsabilidades de seguridad
y dominio.

---

# Flujo de Rechazo por Permiso

```text
Actor

↓

Command Request

↓

Required Permission

↓

Permission Not Granted

↓

Command Rejected

↓

Proposal Not Modified
```

Debe mantenerse:

```text
State = Unchanged

Version = Unchanged

Success Domain Event = Not Produced
```

---

# Flujo de Rechazo por Dominio

```text
Actor

↓

Permission Granted

↓

Command

↓

Proposal Aggregate

↓

Invariant or State Violation

↓

Command Rejected
```

Debe mantenerse:

```text
State = Unchanged

Version = Unchanged

Success Domain Event = Not Produced
```

Este escenario demuestra que autorización y validez del dominio
son controles independientes.

---

# Escenario — Creación Autorizada

```text
Given

Actor posee proposal:create

And

OrganizationId corresponde al contexto autorizado

And

los datos iniciales son válidos

When

CreateProposal es solicitado

Then

la autorización permite intentar el Command

And

Proposal valida sus invariantes

And

ProposalStatus = Draft

And

ProposalCreated es producido
```

---

# Escenario — Creación sin Permiso

```text
Given

Actor no posee proposal:create

When

CreateProposal es solicitado

Then

el Command es rechazado por autorización

And

Proposal no es creada

And

ProposalCreated no es producido
```

---

# Escenario — Edición Autorizada en Draft

```text
Given

Actor posee proposal:update-content

And

ProposalStatus = Draft

When

UpdateProposalContent es solicitado

Then

la autorización permite intentar el Command

And

Proposal valida el nuevo contenido

And

el contenido es actualizado

And

Version incrementa

And

ProposalContentUpdated es producido
```

---

# Escenario — Edición Autorizada en Estado Inválido

```text
Given

Actor posee proposal:update-content

And

ProposalStatus = Submitted

When

UpdateProposalContent es solicitado

Then

la autorización permite intentar el Command

But

Proposal rechaza la operación por estado

And

el contenido permanece sin cambios

And

Version permanece sin cambios

And

ProposalContentUpdated no es producido
```

---

# Escenario — Presentación por Actor Autorizado

```text
Given

Actor posee proposal:submit

And

ProposalStatus = Draft

And

Proposal satisface las condiciones de presentación

When

SubmitProposal es solicitado

Then

ProposalStatus = Submitted

And

Version incrementa

And

ProposalSubmitted es producido
```

---

# Escenario — Inicio de Revisión sin Permiso

```text
Given

ProposalStatus = Submitted

And

Actor no posee proposal:start-review

When

StartProposalReview es solicitado

Then

el Command es rechazado

And

ProposalStatus permanece Submitted

And

Version permanece sin cambios

And

ProposalReviewStarted no es producido
```

---

# Escenario — Aceptación Autorizada

```text
Given

Actor posee proposal:accept

And

ProposalStatus = UnderReview

And

ExpectedVersion = CurrentVersion

When

AcceptProposal es solicitado

Then

Proposal valida sus invariantes

And

ProposalStatus = Accepted

And

Version incrementa

And

ProposalAccepted es producido
```

---

# Escenario — Aceptación con Permiso pero Estado Inválido

```text
Given

Actor posee proposal:accept

And

ProposalStatus = Submitted

When

AcceptProposal es solicitado

Then

el Command es rechazado por el dominio

And

ProposalStatus permanece Submitted

And

Version permanece sin cambios

And

ProposalAccepted no es producido
```

---

# Escenario — Rechazo sin Permiso

```text
Given

ProposalStatus = UnderReview

And

Actor no posee proposal:reject

When

RejectProposal es solicitado

Then

el Command es rechazado por autorización

And

ProposalStatus permanece UnderReview

And

Version permanece sin cambios

And

ProposalRejected no es producido
```

---

# Escenario — Retiro por Autor Autorizado

```text
Given

Actor posee proposal:withdraw

And

Actor satisface las reglas de autoría aplicables

And

ProposalStatus = Submitted

When

WithdrawProposal es solicitado

Then

ProposalStatus = Withdrawn

And

Version incrementa

And

ProposalWithdrawn es producido
```

---

# Escenario — Retiro durante Revisión

```text
Given

Actor posee proposal:withdraw

And

ProposalStatus = UnderReview

When

WithdrawProposal es solicitado

Then

la operación es rechazada por el dominio

And

ProposalStatus permanece UnderReview

And

Version permanece sin cambios

And

ProposalWithdrawn no es producido
```

---

# Escenario — Archivado Autorizado

```text
Given

Actor posee proposal:archive

And

ProposalStatus = Accepted

When

ArchiveProposal es solicitado

Then

ProposalStatus = Archived

And

Version incrementa

And

ProposalArchived es producido
```

---

# Escenario — Actor de Otra Organization

```text
Given

Proposal.OrganizationId = Organization-A

And

Actor posee una Membership válida únicamente en Organization-B

And

la capacidad depende del contexto organizacional

When

Actor intenta modificar Proposal

Then

la autorización es rechazada

And

Proposal permanece sin cambios

And

Version permanece sin cambios

And

ningún Domain Event de éxito es producido
```

---

# Escenario — Conflicto de Concurrencia con Permiso Válido

```text
Given

Actor posee proposal:accept

And

ProposalStatus = UnderReview

And

CurrentVersion = 15

And

AcceptProposal.ExpectedVersion = 14

When

AcceptProposal es solicitado

Then

la autorización puede ser válida

But

la operación es rechazada por conflicto de concurrencia

And

ProposalStatus permanece UnderReview

And

Version permanece 15

And

ProposalAccepted no es producido
```

---

# Restricciones

No está permitido:

- ejecutar un Command protegido sin la capacidad correspondiente;
- utilizar un permiso para evitar una invariante;
- utilizar un permiso para evitar la State Machine;
- utilizar un permiso para evitar el Lifecycle;
- utilizar un permiso para evitar control de concurrencia;
- utilizar un permiso para modificar ProposalId;
- utilizar un permiso para modificar OrganizationId;
- modificar ProposalStatus directamente;
- modificar Version directamente;
- interpretar un permiso como autoridad global ilimitada;
- asumir que una Membership concede todas las capacidades;
- asumir que un Role concede capacidades por su nombre;
- asumir que ser autor concede automáticamente todas las
  capacidades;
- utilizar permisos de Proposal para modificar otros Aggregates;
- utilizar `proposal:associate-assembly` para modificar Assembly;
- utilizar `proposal:change-territory` para modificar Territory;
- utilizar `proposal:accept` para modificar Voting;
- utilizar `proposal:read` como permiso de escritura;
- almacenar credenciales dentro de Proposal;
- almacenar tokens dentro de Proposal;
- interpretar JWT dentro de Proposal;
- acoplar Proposal a Keyrock;
- acoplar Proposal a PEP Proxy;
- acoplar Proposal a un proveedor específico de identidad;
- producir un Domain Event de éxito por la mera concesión de un
  permiso;
- incrementar Version ante una denegación de autorización;
- modificar Proposal ante una denegación de autorización.

---

# Consistencia con Commands

Las capacidades de este documento deben permanecer alineadas con:

```text
DOMAIN-007C-Commands.md
```

Toda incorporación futura de un Command modificador debe definir
explícitamente la capacidad necesaria para intentarlo.

No debe existir un Command de modificación sin una regla de
autorización definida.

---

# Consistencia con Lifecycle

Los permisos no modifican las transiciones establecidas en:

```text
DOMAIN-007A-Lifecycle.md
```

Un permiso puede habilitar a un actor para intentar una
transición, pero no puede crear una transición inexistente.

---

# Consistencia con State Machine

Las operaciones autorizadas deben permanecer dentro de la State
Machine definida en:

```text
DOMAIN-007B-State-Machine.md
```

Debe mantenerse:

```text
Permission

≠

New Transition
```

---

# Consistencia con Domain Events

Los eventos definidos en:

```text
DOMAIN-007D-Domain-Events.md
```

solo pueden producirse después de una operación válida del
Aggregate.

La autorización por sí misma no produce hechos de dominio sobre
Proposal.

---

# Consistencia con Invariantes

Las reglas de:

```text
DOMAIN-007E-Invariants.md
```

permanecen obligatorias independientemente de la capacidad del
actor.

No existe ningún permiso conceptual equivalente a:

```text
proposal:bypass-invariants
```

ni:

```text
proposal:force-transition
```

ni:

```text
proposal:ignore-version
```

Estas capacidades no forman parte del modelo de dominio.

---

# Evolución del Modelo de Permisos

El modelo puede incorporar nuevas capacidades cuando aparezcan
nuevos Commands o responsabilidades formalmente reconocidas por
el dominio.

Una nueva capacidad debe:

- utilizar lenguaje ubicuo;
- corresponder a una responsabilidad explícita;
- mantener alcance mínimo;
- respetar Organization;
- respetar Membership cuando corresponda;
- respetar Role cuando corresponda;
- respetar Lifecycle;
- respetar State Machine;
- respetar invariantes;
- mantener independencia tecnológica.

---

# Incorporación de Nuevos Commands

Cuando se incorpore un nuevo Command:

```text
NewProposalCommand
```

debe definirse una capacidad correspondiente cuando la operación
requiera autorización:

```text
proposal:new-capability
```

La incorporación debe actualizar de manera coherente:

```text
DOMAIN-007C-Commands.md

DOMAIN-007E-Invariants.md

DOMAIN-007F-Permissions.md
```

y los demás documentos afectados por la operación.

---

# Independencia Tecnológica

Los permisos definidos en este documento pertenecen al dominio y
no dependen de:

- OAuth2;
- OpenID Connect;
- JWT;
- Keyrock;
- PEP Proxy;
- API Gateway;
- HTTP;
- REST;
- GraphQL;
- FastAPI;
- Django;
- React;
- Flutter;
- PostgreSQL;
- MongoDB;
- FIWARE.

La infraestructura puede implementar estas capacidades mediante
cualquiera de estas tecnologías sin modificar el significado
conceptual del modelo.

---

# Compatibilidad Arquitectónica

El modelo de permisos de Proposal es compatible con:

- Domain-Driven Design;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Role-Based Access Control;
- Policy-Based Authorization;
- arquitectura distribuida;
- interoperabilidad basada en contratos.

La compatibilidad con diferentes mecanismos de autorización no
implica que estos mecanismos formen parte del Aggregate.

---

# Principios Arquitectónicos

El modelo mantiene:

```text
Authentication
    ≠
Authorization
```

```text
Authorization
    ≠
Domain Validation
```

```text
Permission Granted
    ≠
Operation Guaranteed
```

```text
Role
    ≠
Hardcoded Domain Permission
```

```text
Membership
    ≠
Unlimited Authority
```

```text
Proposal Permission
    ≠
Permission Over External Aggregate
```

```text
Technical Security Mechanism
    ≠
Domain Permission
```

```text
Permission Denied
    =
No Proposal Mutation
```

```text
Permission Granted
+
Invalid Domain State
    =
No Proposal Mutation
```

Estas reglas mantienen separadas las responsabilidades de
seguridad, autorización y consistencia del dominio.

---

# Documentación Complementaria

El modelo de permisos debe interpretarse conjuntamente con:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007D-Domain-Events.md

DOMAIN-007E-Invariants.md

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

Estos documentos desarrollan responsabilidades complementarias
sin reemplazar las reglas de autorización establecidas en este
archivo.

---

# Definición de Éxito

El modelo de permisos del Aggregate **Proposal** define de forma
explícita quién puede intentar cada operación relevante sobre una
iniciativa dentro del ecosistema AURA, manteniendo una separación
estricta entre autorización y reglas del dominio.

El modelo garantiza que:

```text
Actor

↓

Permission

↓

Command

↓

Proposal

↓

State Machine

↓

Invariants

↓

Version Validation

↓

Domain Event
```

permanezca como flujo conceptual de modificación.

Las capacidades oficiales:

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

permiten expresar autorización sin acoplar Proposal a Roles
específicos, mecanismos de autenticación, proveedores de
identidad o tecnologías de infraestructura.

El modelo mantiene:

```text
Permission Granted
    ≠
Domain Operation Guaranteed
```

y:

```text
Permission Denied
    =
State Unchanged
+
Version Unchanged
+
No Success Domain Event
```

La Organization establece el contexto de autorización.

Membership y Role pueden participar en la resolución de
capacidades sin convertirse en partes internas del Aggregate.

Proposal conserva la autoridad exclusiva sobre sus invariantes,
Lifecycle y State Machine.

Ningún actor, incluso cuando posea permisos administrativos,
puede utilizar la autorización para:

- alterar identidad;
- cambiar Organization;
- forzar estados;
- omitir transiciones;
- modificar Version directamente;
- evitar concurrencia;
- modificar una Proposal archivada;
- absorber o modificar otros Aggregates.

De esta forma, **DOMAIN-007F-Permissions.md** constituye la
definición conceptual oficial de las capacidades aplicables al
Aggregate Proposal, proporcionando autorización explícita,
trazable, desacoplada de la infraestructura y coherente con el
modelo Domain-Driven Design establecido para AURA Core.