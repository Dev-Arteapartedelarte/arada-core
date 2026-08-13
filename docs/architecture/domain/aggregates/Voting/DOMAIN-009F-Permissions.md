# DOMAIN-009F — Voting Permissions

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Voting Management

Aggregate:
Voting

Autor:
ARADA

Documentos relacionados:

- DOMAIN-009-Aggregate.md
- DOMAIN-009A-Lifecycle.md
- DOMAIN-009B-State-Machine.md
- DOMAIN-009C-Commands.md
- DOMAIN-009D-Domain-Events.md
- DOMAIN-009E-Invariants.md
- DOMAIN-009G-Repository-Contract.md
- DOMAIN-009I-Versioning.md
- DOMAIN-009J-Consistency-Boundary.md
- DOMAIN-009O-Security-Model.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir formalmente las **Permissions** asociadas a las operaciones
del Aggregate **Voting**.

Las Permissions determinan si un actor posee capacidad para
solicitar una operación determinada sobre Voting.

Una Permission:

- representa una capacidad de autorización;
- se relaciona con una operación explícita;
- no constituye un Command;
- no constituye un Domain Event;
- no modifica el Aggregate;
- no modifica VotingStatus;
- no reemplaza Lifecycle;
- no reemplaza State Machine;
- no reemplaza Invariants;
- no garantiza que una operación autorizada sea válida.

Debe mantenerse siempre la separación:

```text
Authorization

≠

Domain Validation
```

La autorización responde:

```text
¿Puede el actor solicitar esta operación?
```

El Aggregate responde:

```text
¿Puede esta operación ejecutarse válidamente
sobre el estado actual de Voting?
```

---

# Principios

El modelo de Permissions de Voting cumple los siguientes
principios:

- toda operación protegida requiere la Permission correspondiente;
- una Permission concedida permite solicitar una operación;
- una Permission concedida no garantiza que el Command sea
  aceptado;
- una Permission denegada impide continuar con la operación
  protegida;
- las Permissions no modifican las Invariants;
- las Permissions no crean transiciones de estado;
- las Permissions no amplían el Lifecycle;
- las Permissions no modifican VotingId;
- las Permissions no modifican OrganizationId;
- las Permissions no modifican Version;
- las Permissions no forman parte de VotingStatus;
- las Permissions no representan Roles;
- los Roles no forman parte del Aggregate Voting;
- la evaluación de autorización permanece separada del
  comportamiento interno del Aggregate;
- Voting conserva la autoridad final sobre la validez de sus
  operaciones.

---

# Principio Fundamental

Debe mantenerse:

```text
Permission Granted

↓

Command may be requested

↓

Voting validates domain rules

↓

Accepted or Rejected
```

No debe interpretarse:

```text
Permission Granted

=

Operation Accepted
```

Una operación puede estar autorizada y aun así ser rechazada por:

```text
Lifecycle

State Machine

Invariants

Current State

Invalid Command Data

Concurrency
```

---

# Modelo Conceptual

La relación entre autorización y dominio es:

```text
Actor

↓

Permission Evaluation

↓

Command

↓

Voting Aggregate

↓

Lifecycle

State Machine

Invariants

↓

Valid Domain Change
```

La Permission pertenece al control de acceso.

La decisión de dominio pertenece a Voting.

---

# Permissions Oficiales

La versión 1.0 define las siguientes Permissions:

```text
Voting.Create

Voting.Open

Voting.Close

Voting.Cancel

Voting.Archive

Voting.ChangeType

Voting.ChangeTitle

Voting.ChangeDescription

Voting.ChangeRules

Voting.AddOption

Voting.RemoveOption

Voting.Read
```

Estas Permissions corresponden exclusivamente a las capacidades
definidas por el modelo actual de Voting.

No se introducen Permissions para comportamientos que no existen
en:

```text
DOMAIN-009C-Commands.md
```

---

# Voting.Create

## Objetivo

Autorizar la solicitud de creación de un nuevo Voting.

---

## Command protegido

```text
CreateVoting
```

---

## Alcance

La Permission permite solicitar:

```text
CreateVoting
```

No permite por sí misma:

- crear un Voting inválido;
- omitir OrganizationId;
- utilizar un VotingId inválido;
- crear un Voting directamente en Open;
- crear un Voting directamente en Closed;
- crear un Voting directamente en Cancelled;
- crear un Voting directamente en Archived;
- evitar las Invariants de creación.

---

## Resultado de autorización

Cuando:

```text
Voting.Create = Granted
```

el Command puede continuar hacia la validación del dominio.

Debe mantenerse:

```text
Voting.Create

+

Invalid Creation Invariant

=

Rejected
```

---

# Voting.Open

## Objetivo

Autorizar la solicitud de apertura formal de un Voting.

---

## Command protegido

```text
OpenVoting
```

---

## Alcance

La Permission permite solicitar la operación.

No permite alterar la transición oficial:

```text
Draft → Open
```

---

## Restricción de dominio

Debe mantenerse:

```text
Voting.Open = Granted

+

VotingStatus = Draft

+

Valid Opening Invariants

=

Operation may succeed
```

Mientras:

```text
Voting.Open = Granted

+

VotingStatus != Draft

=

Rejected
```

La Permission no crea una transición alternativa.

---

# Voting.Close

## Objetivo

Autorizar la solicitud de cierre formal de un Voting.

---

## Command protegido

```text
CloseVoting
```

---

## Alcance

La Permission se relaciona exclusivamente con la operación:

```text
CloseVoting
```

La transición válida continúa siendo:

```text
Open → Closed
```

---

## Restricción de dominio

Debe mantenerse:

```text
Voting.Close = Granted

+

VotingStatus = Open

+

Valid Closing Invariants

=

Operation may succeed
```

No:

```text
Voting.Close = Granted

↓

Draft → Closed
```

La Permission no permite evitar la State Machine.

---

# Voting.Cancel

## Objetivo

Autorizar la solicitud de cancelación de Voting.

---

## Command protegido

```text
CancelVoting
```

---

## Alcance

La versión 1.0 mantiene la transición definida:

```text
Draft → Cancelled
```

La Permission no amplía esa transición.

---

## Restricción de dominio

Debe mantenerse:

```text
Voting.Cancel = Granted

+

VotingStatus = Draft

+

Valid Cancellation Invariants

=

Operation may succeed
```

No debe interpretarse:

```text
Voting.Cancel = Granted

=

Cancel from any state
```

En particular, la versión 1.0 no permite:

```text
Open → Cancelled
```

---

# Voting.Archive

## Objetivo

Autorizar la solicitud de archivado de Voting.

---

## Command protegido

```text
ArchiveVoting
```

---

## Alcance

La Permission puede utilizarse para solicitar ArchiveVoting desde
los estados reconocidos por la State Machine:

```text
Closed

Cancelled
```

---

## Restricción de dominio

Debe mantenerse:

```text
Voting.Archive = Granted

+

VotingStatus = Closed | Cancelled

+

Valid Archive Invariants

=

Operation may succeed
```

La Permission no permite:

```text
Draft → Archived

Open → Archived
```

ni modificar un Voting ya Archived.

---

# Voting.ChangeType

## Objetivo

Autorizar la solicitud de modificación de VotingType.

---

## Command protegido

```text
ChangeVotingType
```

---

## Alcance

La Permission permite solicitar el cambio.

No permite:

- utilizar un VotingType inválido;
- romper Rules;
- romper Options;
- modificar VotingStatus;
- modificar VotingId;
- modificar OrganizationId;
- evitar las Invariants aplicables.

---

## Restricción de dominio

Debe mantenerse:

```text
Voting.ChangeType = Granted

+

Valid Domain State

+

Valid NewVotingType

+

Preserved Invariants

=

Operation may succeed
```

---

# Voting.ChangeTitle

## Objetivo

Autorizar la solicitud de modificación de Title.

---

## Command protegido

```text
ChangeVotingTitle
```

---

## Alcance

La Permission permite solicitar el cambio descriptivo cuando el
estado del Aggregate permita la operación.

No constituye autorización para modificar la identidad de Voting.

Debe mantenerse:

```text
Title

≠

VotingId
```

---

# Voting.ChangeDescription

## Objetivo

Autorizar la solicitud de modificación de Description.

---

## Command protegido

```text
ChangeVotingDescription
```

---

## Alcance

La Permission permite solicitar la modificación de Description
cuando las reglas del dominio permitan realizarla.

No permite utilizar Description para modificar indirectamente:

```text
VotingId

OrganizationId

VotingStatus

Version
```

---

# Voting.ChangeRules

## Objetivo

Autorizar la solicitud de modificación de las Rules pertenecientes
a Voting.

---

## Command protegido

```text
ChangeVotingRules
```

---

## Alcance

La Permission permite solicitar una modificación de Rules.

No permite:

- establecer Rules inválidas;
- romper coherencia con VotingType;
- romper coherencia con Options;
- modificar VotingStatus;
- evitar Invariants;
- modificar otro Aggregate.

---

## Restricción de dominio

Debe mantenerse:

```text
Voting.ChangeRules = Granted

+

Valid Current State

+

Valid NewRules

+

Preserved Invariants

=

Operation may succeed
```

---

# Voting.AddOption

## Objetivo

Autorizar la solicitud de incorporación de una VotingOption.

---

## Command protegido

```text
AddVotingOption
```

---

## Alcance

La Permission permite solicitar:

```text
AddVotingOption
```

No permite incorporar una Option que produzca un Voting inválido.

---

## Restricción de dominio

Debe mantenerse:

```text
Voting.AddOption = Granted

+

Valid VotingOption

+

Compatible VotingType

+

Compatible Rules

+

Valid State

=

Operation may succeed
```

---

# Voting.RemoveOption

## Objetivo

Autorizar la solicitud de eliminación de una VotingOption.

---

## Command protegido

```text
RemoveVotingOption
```

---

## Alcance

La Permission permite solicitar la eliminación de una Option
existente.

No permite dejar el Aggregate en un estado incompatible con:

```text
VotingType

Rules

Options
```

---

## Restricción de dominio

Debe mantenerse:

```text
Voting.RemoveOption = Granted

+

Existing VotingOption

+

Valid Resulting Options

+

Preserved Invariants

=

Operation may succeed
```

---

# Voting.Read

## Objetivo

Autorizar el acceso de lectura a información de Voting cuando dicho
acceso se encuentre protegido por el modelo de autorización.

---

## Operación protegida

```text
Read Voting
```

---

## Alcance

Voting.Read permite consultar la representación autorizada de
Voting.

No permite:

- modificar el Aggregate;
- ejecutar Commands;
- modificar VotingStatus;
- modificar Version;
- modificar Read Models;
- obtener automáticamente cualquier representación disponible.

Debe mantenerse:

```text
Voting.Read

≠

Voting.Write
```

---

# Permission y Command

Una Permission se relaciona con la capacidad para solicitar un
Command.

Debe mantenerse:

```text
Permission

↓

Authorization Decision

↓

Command
```

No:

```text
Permission

=

Command
```

La Permission no contiene comportamiento de dominio.

El Command expresa la intención que Voting debe evaluar.

---

# Matriz Permission / Command

| Permission | Command |
| --- | --- |
| Voting.Create | CreateVoting |
| Voting.Open | OpenVoting |
| Voting.Close | CloseVoting |
| Voting.Cancel | CancelVoting |
| Voting.Archive | ArchiveVoting |
| Voting.ChangeType | ChangeVotingType |
| Voting.ChangeTitle | ChangeVotingTitle |
| Voting.ChangeDescription | ChangeVotingDescription |
| Voting.ChangeRules | ChangeVotingRules |
| Voting.AddOption | AddVotingOption |
| Voting.RemoveOption | RemoveVotingOption |

Voting.Read corresponde a operaciones de consulta y no produce un
Command de modificación del Aggregate.

---

# Permission y Domain Event

Una Permission no genera directamente Domain Events.

Debe mantenerse:

```text
Permission Granted

↓

Command

↓

Valid Domain Behavior

↓

Domain Event
```

No:

```text
Permission Granted

↓

Domain Event
```

Un Domain Event solo puede existir cuando la operación fue
efectivamente aceptada por Voting.

---

# Matriz Permission / Domain Event

| Permission | Command | Domain Event esperado si la operación es válida |
| --- | --- | --- |
| Voting.Create | CreateVoting | VotingCreated |
| Voting.Open | OpenVoting | VotingOpened |
| Voting.Close | CloseVoting | VotingClosed |
| Voting.Cancel | CancelVoting | VotingCancelled |
| Voting.Archive | ArchiveVoting | VotingArchived |
| Voting.ChangeType | ChangeVotingType | VotingTypeChanged |
| Voting.ChangeTitle | ChangeVotingTitle | VotingTitleChanged |
| Voting.ChangeDescription | ChangeVotingDescription | VotingDescriptionChanged |
| Voting.ChangeRules | ChangeVotingRules | VotingRulesChanged |
| Voting.AddOption | AddVotingOption | VotingOptionAdded |
| Voting.RemoveOption | RemoveVotingOption | VotingOptionRemoved |

La Permission no garantiza la producción del Event.

El Event solo existe después de una operación válida.

---

# Permission e Invariants

Las Permissions no reemplazan:

```text
DOMAIN-009E-Invariants.md
```

Debe mantenerse:

```text
Permission Granted

+

Invariant Violation

=

Rejected
```

No existe una Permission que autorice violar deliberadamente una
Invariant del Aggregate.

---

# Permission y Lifecycle

Las Permissions no alteran:

```text
DOMAIN-009A-Lifecycle.md
```

Por ejemplo:

```text
Voting.Open = Granted
```

no permite:

```text
Closed → Open
```

porque dicha transición no pertenece al Lifecycle versión 1.0.

Igualmente:

```text
Voting.Cancel = Granted
```

no permite:

```text
Open → Cancelled
```

---

# Permission y State Machine

Las Permissions no alteran:

```text
DOMAIN-009B-State-Machine.md
```

Debe mantenerse:

```text
Permission

+

Allowed State Transition

+

Valid Invariants

=

Potentially Valid Operation
```

La State Machine conserva autoridad sobre las transiciones.

---

# Permission y VotingStatus

VotingStatus no concede Permissions.

Debe mantenerse:

```text
VotingStatus

≠

Authorization
```

El hecho de que Voting se encuentre:

```text
Draft
```

no significa que cualquier actor pueda abrirlo.

Igualmente, poseer:

```text
Voting.Open
```

no significa que el Aggregate se encuentre en un estado válido para
ser abierto.

---

# Permission y Version

Las Permissions no modifican Version.

Debe mantenerse:

```text
Permission Check

↓

No Aggregate Modification
```

Por lo tanto:

```text
Version Before Permission Check

=

Version After Permission Check
```

Version solamente cambia como consecuencia de una modificación
válida del Aggregate.

---

# Permission Denied

Cuando la Permission requerida no está concedida:

```text
Permission Denied

↓

Operation Rejected
```

No debe producirse:

```text
Aggregate State Change

Version Increment

Success Domain Event
```

---

# Permission Granted

Cuando una Permission está concedida:

```text
Permission Granted

↓

Domain Validation Required
```

Voting continúa validando:

- estado actual;
- Lifecycle;
- State Machine;
- Command Data;
- Rules;
- Options;
- Result cuando corresponda;
- Invariants;
- Version y concurrencia cuando corresponda.

---

# Ausencia de Permission

La ausencia de la Permission requerida equivale a no disponer de
capacidad para solicitar la operación protegida.

Debe mantenerse:

```text
Required Permission

not granted

↓

Operation Denied
```

---

# Permissions y Roles

Permissions y Roles representan conceptos diferentes.

Debe mantenerse:

```text
Role

≠

Permission
```

Un Role puede participar en el modelo de autorización de AURA,
pero Voting no define dentro de este Aggregate qué Roles poseen qué
Permissions.

Voting tampoco almacena:

```text
Role Aggregate
```

dentro de su estado.

La asignación entre Roles y Permissions pertenece al modelo de
autorización correspondiente.

---

# Permissions y Membership

Membership representa pertenencia organizacional.

Voting no define dentro de este Aggregate la relación completa entre:

```text
Membership

↓

Permission
```

La autorización puede utilizar información proveniente de otros
contextos, pero Membership no se incorpora dentro de Voting.

---

# Permissions y Citizen

Citizen representa identidad cívica.

Voting no almacena el Aggregate Citizen para resolver Permissions.

Cuando un actor se encuentre relacionado con un Citizen, dicha
identidad permanece como referencia externa conforme al modelo de
AURA.

---

# Contexto Organizacional

Todo Voting pertenece a:

```text
OrganizationId
```

La evaluación de Permissions debe respetar el contexto
organizacional correspondiente sin modificar OrganizationId.

Debe mantenerse:

```text
Permission Evaluation

+

Voting Organization Context
```

sin convertir Organization en una entidad interna de Voting.

---

# Aislamiento Organizacional

La existencia de una Permission no permite ignorar el contexto
organizacional de Voting.

Debe mantenerse la relación:

```text
Voting

↓

OrganizationId
```

durante toda evaluación y operación autorizada.

Una Permission no puede utilizarse para transferir Voting a otra
Organization.

---

# Permissions y Assembly

Cuando Voting se encuentre relacionado mediante:

```text
AssemblyId
```

una Permission de Voting autoriza exclusivamente una operación
sobre Voting.

No concede capacidad para modificar:

```text
Assembly
```

Debe mantenerse:

```text
Voting.Open

≠

Assembly.Open
```

---

# Permissions y Proposal

Cuando Voting se encuentre relacionado mediante:

```text
ProposalId
```

una Permission de Voting no concede capacidad para modificar
Proposal.

Debe mantenerse:

```text
Voting Permission

≠

Proposal Permission
```

Los Aggregates permanecen separados.

---

# Permissions y Participation

Voting y Participation poseen modelos de autorización separados.

Debe mantenerse:

```text
Voting Permission

≠

Participation Permission
```

Una Permission sobre Voting no concede automáticamente capacidad
para modificar Participation.

Una Permission sobre Participation tampoco concede automáticamente
capacidad sobre Voting.

---

# Permissions y Consistency Boundary

Las Permissions no amplían el Consistency Boundary.

Debe mantenerse:

```text
Voting Permission

↓

Voting Operation
```

No:

```text
Voting Permission

↓

Modify Voting
+
Modify Assembly
+
Modify Proposal
+
Modify Participation
```

Cada Aggregate conserva su propio límite.

---

# Permissions y Repository

El Repository no determina Permissions.

Debe mantenerse:

```text
Authorization

↓

Domain Operation

↓

Repository
```

No:

```text
Repository Access

=

Voting Permission
```

La capacidad técnica de acceder a persistencia no constituye una
Permission de dominio.

---

# Permissions y Read Models

Voting.Read puede controlar el acceso autorizado a representaciones
de lectura.

Los Read Models permanecen:

```text
Read Only
```

La Permission de lectura no permite:

```text
Read Model

↓

Modify Voting
```

---

# Permissions y Integration Events

Los Integration Events no conceden Permissions.

Recibir un Integration Event relacionado con Voting no autoriza al
consumidor a modificar el Aggregate.

Debe mantenerse:

```text
Integration Event Received

≠

Voting Permission Granted
```

---

# Permissions y Domain Events

Los Domain Events tampoco constituyen Permissions.

Debe mantenerse:

```text
VotingOpened

≠

Permission to Open Voting
```

El Event representa un hecho ocurrido.

La Permission representa una capacidad para solicitar una
operación.

---

# Permissions y Seguridad

Las Permissions forman parte del modelo conceptual de control de
acceso sobre las capacidades de Voting.

Las reglas complementarias se desarrollan en:

```text
DOMAIN-009O-Security-Model.md
```

El modelo no introduce mecanismos concretos de autenticación o
Infrastructure.

---

# Autenticación y Permissions

Debe mantenerse:

```text
Authentication

≠

Authorization
```

La autenticación permite identificar al actor según el modelo
correspondiente.

La Permission determina si dicho actor puede solicitar una
capacidad protegida.

Un actor autenticado no posee automáticamente:

```text
Voting.Create

Voting.Open

Voting.Close

Voting.Cancel

Voting.Archive
```

ni ninguna otra Permission de Voting.

---

# Independencia Tecnológica

Las Permissions definidas en este documento son conceptos del
modelo de autorización de AURA.

No dependen directamente de:

```text
OAuth

JWT

Keyrock

PEP Proxy

HTTP

REST

Database

Framework
```

Estos mecanismos pueden implementar o transportar decisiones de
autorización, pero no definen la semántica de las Permissions.

---

# Sin Escalamiento Implícito

Una Permission no concede automáticamente otra Permission.

Debe mantenerse:

```text
Voting.Create

≠

Voting.Open
```

```text
Voting.Open

≠

Voting.Close
```

```text
Voting.Close

≠

Voting.Archive
```

```text
Voting.ChangeRules

≠

Voting.AddOption
```

Cada Permission conserva una capacidad explícita.

---

# Sin Permission Global Implícita

La versión 1.0 no presupone una Permission global que sustituya
automáticamente las Permissions específicas definidas.

La existencia de capacidades superiores, agrupaciones o políticas
de autorización pertenece al modelo correspondiente y no debe
inferirse desde este documento.

---

# Archived y Permissions

Cuando:

```text
VotingStatus = Archived
```

la existencia de una Permission de modificación no crea una
operación válida.

Debe mantenerse:

```text
Permission Granted

+

VotingStatus = Archived

+

Ordinary Modification Command

=

Rejected
```

Archived continúa protegido por Lifecycle e Invariants.

---

# Closed y Voting.Open

Debe mantenerse:

```text
Voting.Open = Granted

+

VotingStatus = Closed

=

Rejected
```

La Permission no permite reapertura.

La versión 1.0 no define:

```text
Voting.Reopen
```

---

# Cancelled y Voting.Open

Debe mantenerse:

```text
Voting.Open = Granted

+

VotingStatus = Cancelled

=

Rejected
```

La Permission no permite reactivación.

La versión 1.0 no define:

```text
Voting.Reactivate
```

---

# Archived y Desarchivado

La versión 1.0 no define:

```text
Voting.Unarchive
```

Por lo tanto, ninguna Permission existente puede interpretarse como
capacidad de desarchivado.

---

# Permissions no Definidas

La versión 1.0 no define Permissions para comportamientos que no
forman parte del Aggregate.

No se definen:

```text
Voting.Reopen

Voting.Reactivate

Voting.Unarchive

Voting.Delete

Voting.Suspend

Voting.Resume
```

porque sus Commands correspondientes no existen en el modelo
actual.

Una nueva Permission requiere primero una evolución explícita del
comportamiento del dominio.

---

# Regla para Incorporar una Permission

Una nueva Permission solo puede incorporarse cuando exista una
capacidad protegida explícitamente definida por el modelo.

Debe mantenerse coherencia con:

```text
DOMAIN-009-Aggregate.md

DOMAIN-009A-Lifecycle.md

DOMAIN-009B-State-Machine.md

DOMAIN-009C-Commands.md

DOMAIN-009D-Domain-Events.md

DOMAIN-009E-Invariants.md

DOMAIN-009F-Permissions.md
```

cuando corresponda.

No debe crearse una Permission para introducir indirectamente un
Command o transición que aún no existe.

---

# Matriz de Permissions

| Permission | Capacidad |
| --- | --- |
| Voting.Create | Crear Voting |
| Voting.Open | Abrir Voting |
| Voting.Close | Cerrar Voting |
| Voting.Cancel | Cancelar Voting |
| Voting.Archive | Archivar Voting |
| Voting.ChangeType | Cambiar VotingType |
| Voting.ChangeTitle | Cambiar Title |
| Voting.ChangeDescription | Cambiar Description |
| Voting.ChangeRules | Cambiar Rules |
| Voting.AddOption | Agregar VotingOption |
| Voting.RemoveOption | Eliminar VotingOption |
| Voting.Read | Consultar Voting |

---

# Matriz Permission / Lifecycle

| Permission | Transición de Lifecycle |
| --- | --- |
| Voting.Create | No Voting → Draft |
| Voting.Open | Draft → Open |
| Voting.Close | Open → Closed |
| Voting.Cancel | Draft → Cancelled |
| Voting.Archive | Closed → Archived |
| Voting.Archive | Cancelled → Archived |
| Voting.ChangeType | No cambia VotingStatus |
| Voting.ChangeTitle | No cambia VotingStatus |
| Voting.ChangeDescription | No cambia VotingStatus |
| Voting.ChangeRules | No cambia VotingStatus |
| Voting.AddOption | No cambia VotingStatus |
| Voting.RemoveOption | No cambia VotingStatus |
| Voting.Read | No modifica Voting |

La Permission nunca reemplaza la validación de la transición.

---

# Matriz de Separación de Responsabilidades

| Concepto | Responsabilidad |
| --- | --- |
| Authentication | Identificar al actor |
| Permission | Determinar si puede solicitar una operación |
| Command | Expresar la intención |
| Voting Aggregate | Validar y ejecutar comportamiento |
| Lifecycle | Definir evolución conceptual |
| State Machine | Definir transición permitida |
| Invariants | Proteger estado válido |
| Domain Event | Representar hecho consumado |
| Repository | Persistir el Aggregate |

---

# Rechazo por Permission

Cuando una operación requiere una Permission y esta no se encuentra
concedida:

```text
Permission Check

↓

Denied
```

La operación termina antes de producir una modificación válida del
Aggregate.

Debe mantenerse:

```text
VotingStatus unchanged

Version unchanged

No success Domain Event
```

---

# Rechazo por Dominio

Una Permission concedida puede ser seguida por rechazo del dominio.

Conceptualmente:

```text
Voting.Close = Granted

↓

CloseVoting

↓

VotingStatus = Draft

↓

Rejected
```

La causa del rechazo corresponde a las reglas del Aggregate.

No a la ausencia de Permission.

---

# Distinción de Rechazos

Debe distinguirse conceptualmente:

```text
Authorization Denied
```

de:

```text
Domain Rejected
```

En ambos casos no existe una modificación válida.

Sin embargo, representan motivos diferentes.

---

# Restricciones

No está permitido:

- interpretar una Permission como un Command;
- interpretar una Permission como un Domain Event;
- utilizar una Permission para modificar VotingStatus directamente;
- utilizar una Permission para modificar Version;
- utilizar una Permission para modificar VotingId;
- utilizar una Permission para modificar OrganizationId;
- utilizar una Permission para evitar Lifecycle;
- utilizar una Permission para evitar State Machine;
- utilizar una Permission para evitar Invariants;
- utilizar una Permission para crear transiciones inexistentes;
- utilizar Voting.Open para reabrir un Voting Closed;
- utilizar Voting.Cancel para cancelar un Voting Open en la versión
  1.0;
- utilizar Voting.Archive para archivar desde Draft;
- utilizar Voting.Archive para archivar desde Open;
- utilizar una Permission de Voting para modificar Assembly;
- utilizar una Permission de Voting para modificar Proposal;
- utilizar una Permission de Voting para modificar Participation;
- utilizar una Permission de Voting para modificar Organization;
- asumir que un Role específico posee una Permission sin que el
  modelo de autorización correspondiente lo establezca;
- asumir que una Membership concede automáticamente una Permission;
- asumir que Authentication implica Authorization;
- asumir que una Permission concede automáticamente otras
  Permissions;
- definir Permissions para Commands inexistentes;
- introducir Permissions de reapertura, reactivación,
  desarchivado, suspensión, reanudación o eliminación sin una
  evolución explícita del modelo.

---

# Reglas

## REG-001

Toda operación protegida de Voting requiere la Permission
correspondiente.

---

## REG-002

Una Permission concedida permite solicitar una operación, pero no
garantiza su aceptación.

---

## REG-003

Una Permission denegada impide la ejecución de la operación
protegida.

---

## REG-004

Las Permissions no reemplazan Lifecycle.

---

## REG-005

Las Permissions no reemplazan State Machine.

---

## REG-006

Las Permissions no reemplazan Invariants.

---

## REG-007

Las Permissions no modifican VotingId.

---

## REG-008

Las Permissions no modifican OrganizationId.

---

## REG-009

Las Permissions no modifican VotingStatus.

---

## REG-010

Las Permissions no modifican Version.

---

## REG-011

Una Permission no concede automáticamente otra Permission.

---

## REG-012

Los Roles no se incorporan dentro de Voting para representar
Permissions.

---

## REG-013

Una Permission de Voting no concede autoridad sobre otro
Aggregate.

---

## REG-014

Voting.Read no concede capacidad de modificación.

---

## REG-015

Una operación denegada por autorización no modifica el Aggregate
ni produce el Domain Event de éxito.

---

## REG-016

Una operación autorizada pero inválida para el dominio debe ser
rechazada por Voting.

---

## REG-017

No pueden definirse Permissions para comportamientos inexistentes
sin una evolución explícita del modelo.

---

# Definición de Éxito

El modelo de Permissions del Aggregate **Voting** define
explícitamente las capacidades de autorización correspondientes a
las operaciones oficiales de la versión 1.0:

```text
Voting.Create

Voting.Open

Voting.Close

Voting.Cancel

Voting.Archive

Voting.ChangeType

Voting.ChangeTitle

Voting.ChangeDescription

Voting.ChangeRules

Voting.AddOption

Voting.RemoveOption

Voting.Read
```

Cada Permission:

- representa una capacidad explícita;
- mantiene correspondencia con una operación definida;
- permanece separada de Commands;
- permanece separada de Domain Events;
- no modifica el Aggregate;
- no reemplaza Lifecycle;
- no reemplaza State Machine;
- no reemplaza Invariants;
- no altera Version;
- no amplía el Consistency Boundary;
- no concede autoridad sobre otros Aggregates.

El modelo mantiene la separación:

```text
Authentication

↓

Authorization

↓

Command

↓

Voting Domain Validation
```

Una autorización concedida permite que una intención llegue al
Aggregate.

Voting conserva siempre la responsabilidad de decidir si la
operación es válida según su estado, Lifecycle, State Machine,
Rules e Invariants.

Una autorización denegada no produce modificación.

Una autorización concedida sobre una operación inválida tampoco
produce modificación.

De esta forma, `DOMAIN-009F-Permissions.md` establece el modelo
conceptual oficial de capacidades para **Voting**, manteniendo
separadas autorización y lógica de dominio y preservando el patrón
consolidado de AURA Core.
````
