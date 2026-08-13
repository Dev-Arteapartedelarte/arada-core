# DOMAIN-008 — Participation Aggregate

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Participation Management

Aggregate:
Participation

Autor:
ARADA

Documentos relacionados:

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
- DOMAIN-006-Aggregate.md
- DOMAIN-007-Aggregate.md

---

# Objetivo

El Aggregate **Participation** representa una instancia formal de
participación de un actor habilitado dentro de un proceso
participativo del ecosistema AURA.

Participation permite registrar y controlar la existencia de una
participación como concepto independiente del dominio,
manteniendo su identidad, contexto organizacional, actor,
contexto participativo, estado, ciclo de vida, trazabilidad y
reglas de consistencia.

El Aggregate constituye el límite de consistencia de una
participación individual.

Participation conecta a los actores habilitados con las
instancias en las cuales pueden ejercer acciones de participación
dentro de una Organization.

Una Participation puede existir en el contexto de:

- una Assembly;
- una Proposal;
- una instancia deliberativa;
- una consulta;
- una instancia organizacional;
- una instancia comunitaria;
- un proceso territorial;
- otro contexto participativo reconocido por el dominio.

Participation no representa el proceso completo dentro del cual
participa el actor.

Representa exclusivamente la instancia formal mediante la cual
dicho actor participa en ese contexto.

Participation no reemplaza ni absorbe Assembly, Proposal o
Voting.

Cada uno de estos conceptos mantiene identidad, responsabilidades,
invariantes y ciclo de vida propios.

---

# Propósito

El Aggregate Participation tiene como propósito representar de
forma consistente la participación formal de un actor dentro de
un contexto reconocido por AURA.

Participation proporciona la identidad y el contexto necesarios
para determinar que una participación:

- existe;
- pertenece a una Organization;
- corresponde a un actor determinado;
- ocurre dentro de un contexto participativo determinado;
- posee un tipo reconocido;
- mantiene un estado propio;
- respeta un ciclo de vida;
- puede ser validada;
- puede ser completada;
- puede ser retirada cuando las reglas lo permitan;
- puede ser invalidada cuando corresponda;
- mantiene trazabilidad;
- mantiene Version;
- produce Domain Events.

Participation constituye la unidad formal mediante la cual el
dominio puede representar que un actor intervino en un proceso
participativo sin incorporar dentro del Aggregate los procesos
externos relacionados.

---

# Definición

Una Participation representa una instancia formal de
participación asociada a un actor dentro de una Organization y
dentro de un contexto participativo determinado.

La Participation posee:

- identidad propia;
- Organization propietaria;
- actor participante;
- contexto participativo;
- tipo de participación;
- estado;
- ciclo de vida;
- información temporal;
- referencias externas cuando correspondan;
- trazabilidad;
- Version.

Una Participation puede representar conceptualmente:

- asistencia;
- intervención;
- deliberación;
- presentación de una contribución;
- expresión de opinión;
- participación en una consulta;
- participación en una Proposal;
- participación dentro de una Assembly;
- participación territorial;
- otra forma reconocida de participación.

El tipo específico de Participation dependerá de las reglas del
dominio y del contexto en el cual se origine.

Participation no representa:

- una Organization;
- un Citizen;
- una Membership;
- un Role;
- un Territory;
- una Assembly;
- una Proposal;
- una Voting;
- un Document;
- una Notification;
- un Audit;
- una Integration.

Estos conceptos corresponden a otros Aggregates o Bounded
Contexts.

---

# Significado de Participation

Dentro del lenguaje ubicuo de AURA, **Participation** no debe
interpretarse simplemente como actividad técnica, presencia en
una interfaz, autenticación, sesión o interacción de usuario.

Participation representa una acción o instancia reconocida por el
dominio como participación formal.

Por lo tanto:

```text
Login

≠

Participation
```

```text
Session

≠

Participation
```

```text
Page View

≠

Participation
```

```text
Authentication

≠

Participation
```

```text
Membership

≠

Participation
```

```text
Voting

≠

Participation
```

Una Membership puede habilitar a un actor para participar.

Una Participation representa el ejercicio formal de dicha
participación cuando corresponda.

Voting representa un proceso específico de votación y mantiene su
propio Aggregate.

---

# Responsabilidades

El Aggregate Participation es responsable de:

- mantener la identidad de la Participation;
- mantener la Organization a la cual pertenece;
- mantener la referencia al actor participante;
- mantener el contexto participativo;
- mantener el tipo de Participation;
- administrar su ciclo de vida;
- controlar su estado;
- registrar su creación;
- controlar su activación cuando corresponda;
- controlar su validación cuando corresponda;
- controlar su finalización;
- controlar su retiro cuando las reglas lo permitan;
- controlar su invalidación cuando corresponda;
- mantener información temporal relevante;
- proteger las invariantes del Aggregate;
- impedir modificaciones incompatibles con su estado;
- mantener trazabilidad;
- incrementar Version ante modificaciones válidas;
- publicar Domain Events;
- mantener la consistencia de Participation como unidad de
  dominio.

Participation es responsable de representar exclusivamente la
participación formal de un actor.

No administra el proceso completo en el cual dicha participación
ocurre.

---

# Responsabilidades Fuera del Aggregate

No es responsabilidad de Participation:

- administrar Organizations;
- administrar Citizens;
- administrar Memberships;
- definir Roles;
- administrar Territories;
- administrar Assemblies;
- administrar Proposals;
- ejecutar Votings;
- administrar Documents;
- enviar Notifications;
- ejecutar Audit;
- administrar Integrations;
- autenticar actores;
- administrar credenciales;
- administrar sesiones;
- resolver identidad externa;
- modificar permisos técnicos;
- modificar el estado de otros Aggregates.

Estas responsabilidades pertenecen a sus respectivos Aggregates,
Bounded Contexts o capas arquitectónicas.

La colaboración se realiza mediante:

- identificadores;
- contratos de dominio;
- Domain Events;
- Integration Events;
- Application Services.

Participation nunca modifica directamente el estado interno de
otro Aggregate.

---

# Modelo Conceptual

```text
Organization
      │
      │
      ▼
Participation
      │
      ├──────── Citizen
      │
      ├──────── Membership
      │
      ├──────── Role
      │
      ├──────── Territory
      │
      ├──────── Assembly
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

Cada Participation pertenece a una única Organization.

Una Organization puede contener múltiples Participation.

Participation mantiene referencias hacia otros Aggregates
mediante identificadores de dominio cuando dichas relaciones sean
necesarias.

Participation no contiene Aggregates externos dentro de su límite
de consistencia.

---

# Modelo Conceptual del Actor

El actor que participa debe ser identificable dentro del dominio.

Conceptualmente:

```text
Actor
   │
   ▼
Participation
```

La identidad concreta del actor puede relacionarse con los
Aggregates existentes mediante identificadores.

Cuando la participación corresponde a un Citizen:

```text
CitizenId
```

Cuando la participación se ejerce dentro de una relación
organizacional:

```text
MembershipId
```

Participation no duplica ni reconstruye el Aggregate Citizen o
Membership.

Mantiene únicamente las referencias necesarias para expresar el
contexto de participación.

---

# Aggregate Root

La única Aggregate Root es:

```text
Participation
```

Participation constituye la única puerta de entrada para
modificar el estado interno del Aggregate.

No existen modificaciones directas sobre sus atributos.

Toda operación que altere una propiedad, condición o estado de
Participation debe ejecutarse mediante comportamiento definido
por el Aggregate Root.

---

# Identidad

La identidad del Aggregate está determinada por:

```text
ParticipationId
```

ParticipationId:

- es único;
- es global dentro del dominio;
- es inmutable;
- no depende de la persistencia;
- no cambia durante el ciclo de vida;
- no se reutiliza después de la desaparición lógica del
  Aggregate.

La identidad de Participation no depende de:

- CitizenId;
- MembershipId;
- OrganizationId;
- AssemblyId;
- ProposalId;
- TerritoryId;
- tipo;
- estado;
- fecha;
- identificadores externos.

Dos Participation pueden relacionarse con un mismo actor o
contexto cuando las reglas del dominio permitan múltiples
instancias, pero nunca pueden compartir el mismo ParticipationId.

---

# Identidad Organizacional

Cada Participation pertenece exactamente a una Organization.

La relación se representa mediante:

```text
OrganizationId
```

OrganizationId:

- es obligatorio;
- identifica la Organization propietaria;
- permanece inmutable durante la vida del Aggregate;
- no representa una copia de Organization;
- no permite modificar Organization;
- establece el límite organizacional de Participation.

Participation mantiene la referencia mediante identidad.

No incorpora el Aggregate Organization.

---

# Actor Participante

Participation mantiene la referencia necesaria al actor que
origina o ejerce la participación.

Conceptualmente pueden utilizarse:

```text
CitizenId

MembershipId
```

según el contexto del dominio.

CitizenId identifica al ciudadano cuando la participación se
encuentra vinculada directamente a su identidad cívica.

MembershipId identifica la relación organizacional mediante la
cual el actor participa cuando dicha relación sea necesaria.

Estas referencias no convierten Citizen o Membership en
entidades internas de Participation.

---

# Contexto de Participación

Toda Participation ocurre dentro de un contexto reconocido por el
dominio.

El contexto puede relacionarse con:

```text
AssemblyId

ProposalId

TerritoryId

VotingId
```

según corresponda.

La presencia de una referencia depende de la naturaleza de la
Participation.

No todas las Participation requieren todas estas referencias.

El contexto debe ser suficiente para expresar dónde o respecto de
qué se produjo la participación.

---

# Tipo de Participation

Participation mantiene una clasificación conceptual que describe
la naturaleza de la participación.

Tipos conceptuales pueden comprender:

```text
Attendance

Intervention

Deliberation

Contribution

Consultation

ProposalParticipation

AssemblyParticipation

TerritorialParticipation
```

El tipo:

- pertenece al Aggregate;
- expresa el significado de la participación;
- no modifica ParticipationId;
- puede determinar reglas específicas;
- debe ser reconocido por el dominio.

La clasificación no debe utilizarse para absorber
responsabilidades pertenecientes a otros Aggregates.

---

# Atributos Conceptuales

Participation mantiene conceptualmente:

```text
ParticipationId

OrganizationId

CitizenId

MembershipId

TerritoryId

AssemblyId

ProposalId

VotingId

ParticipationType

Status

StartedAt

CompletedAt

WithdrawnAt

InvalidatedAt

CreatedAt

UpdatedAt

Version
```

Las referencias opcionales dependen del contexto específico de la
Participation.

---

# Descripción de Atributos

## ParticipationId

Identificador único e inmutable del Aggregate.

Nunca cambia durante la vida de Participation.

---

## OrganizationId

Identificador de la Organization propietaria.

Es obligatorio e inmutable.

---

## CitizenId

Referencia al Citizen relacionado con la Participation cuando
corresponda.

No contiene el Aggregate Citizen.

---

## MembershipId

Referencia a la Membership mediante la cual el actor participa
cuando el contexto organizacional lo requiera.

No contiene el Aggregate Membership.

---

## TerritoryId

Referencia opcional al contexto territorial asociado.

No contiene ni modifica Territory.

---

## AssemblyId

Referencia opcional a la Assembly dentro de cuyo contexto ocurre
la Participation.

No contiene ni modifica Assembly.

---

## ProposalId

Referencia opcional a la Proposal respecto de la cual ocurre la
Participation.

No contiene ni modifica Proposal.

---

## VotingId

Referencia opcional a Voting cuando resulte necesario
contextualizar una Participation respecto de un proceso de
votación.

Voting mantiene su propio límite de consistencia.

Participation no ejecuta la votación.

---

## ParticipationType

Clasificación conceptual de la Participation.

Debe corresponder a un tipo reconocido por el dominio.

---

## Status

Estado actual del Aggregate.

Solo puede modificarse mediante comportamiento válido de
Participation.

---

## StartedAt

Fecha y hora en la cual la Participation comenzó formalmente.

Puede ser nula antes del inicio.

---

## CompletedAt

Fecha y hora de finalización válida.

Puede ser nula mientras Participation no se encuentre completada.

---

## WithdrawnAt

Fecha y hora de retiro cuando la Participation haya sido retirada.

Puede ser nula.

---

## InvalidatedAt

Fecha y hora de invalidación cuando corresponda.

Puede ser nula.

---

## CreatedAt

Fecha y hora de creación del Aggregate.

Es inmutable después de la creación.

---

## UpdatedAt

Fecha y hora de la última modificación válida.

---

## Version

Número de versión utilizado para controlar la evolución del
Aggregate y la concurrencia optimista.

---

# Estado

Participation mantiene un estado propio.

Estados conceptuales:

```text
Registered

Active

Completed

Withdrawn

Invalidated

Archived
```

El estado:

- pertenece al Aggregate;
- representa su condición actual;
- no puede modificarse directamente;
- determina las operaciones permitidas;
- participa en la protección de invariantes;
- solo cambia mediante transiciones válidas.

La definición formal de estados y transiciones se documentará en:

```text
DOMAIN-008B-State-Machine.md
```

---

# Ciclo de Vida

El ciclo de vida conceptual principal de Participation es:

```text
Registered
     │
     ▼
  Active
     │
     ▼
 Completed
     │
     ▼
 Archived
```

Existen caminos alternativos controlados:

```text
Registered
     │
     ├──────────────► Withdrawn
     │
     └──────────────► Invalidated

Active
     │
     ├──────────────► Withdrawn
     │
     └──────────────► Invalidated

Completed
     │
     └──────────────► Invalidated

Withdrawn
     │
     ▼
 Archived

Invalidated
     │
     ▼
 Archived
```

No todas las transiciones son válidas desde todos los estados.

La definición formal del ciclo de vida se desarrollará en:

```text
DOMAIN-008A-Lifecycle.md

DOMAIN-008B-State-Machine.md
```

---

# Registered

Registered representa una Participation formalmente creada pero
que aún no se encuentra activa.

En este estado el Aggregate posee identidad y contexto válidos.

La existencia de Participation ya constituye un hecho formal del
dominio.

Registered no implica que la participación haya sido ejecutada o
completada.

---

# Active

Active representa una Participation cuyo ejercicio formal se
encuentra en curso.

La transición hacia Active requiere que las condiciones
necesarias del dominio se encuentren satisfechas.

Una Participation Active puede evolucionar hacia:

```text
Completed

Withdrawn

Invalidated
```

según las reglas correspondientes.

---

# Completed

Completed representa una Participation que finalizó
correctamente.

La finalización no implica necesariamente aceptación, aprobación,
voto favorable o resultado sobre otro Aggregate.

Significa exclusivamente que la instancia de Participation
completó su propio ciclo válido.

Por lo tanto:

```text
ParticipationCompleted

≠

ProposalAccepted
```

y:

```text
ParticipationCompleted

≠

VotingCompleted
```

---

# Withdrawn

Withdrawn representa una Participation retirada de acuerdo con
las reglas del dominio.

El retiro constituye una transición explícita.

No equivale a eliminar el Aggregate.

La Participation continúa existiendo para efectos de:

- identidad;
- trazabilidad;
- auditoría;
- eventos;
- reconstrucción;
- referencias históricas.

---

# Invalidated

Invalidated representa una Participation que dejó de ser
considerada válida dentro del dominio.

La invalidación debe responder a una regla explícita.

Invalidated no equivale a eliminación física.

El Aggregate conserva su identidad e historia.

---

# Archived

Archived representa el estado terminal de conservación lógica de
Participation.

Una Participation archivada:

- mantiene identidad;
- mantiene historia;
- mantiene trazabilidad;
- no participa de operaciones normales;
- no puede modificarse salvo reglas explícitas de conservación que
  no alteren su significado de dominio.

---

# Información Temporal

Participation mantiene información temporal necesaria para
representar su ciclo de vida.

Conceptualmente:

```text
CreatedAt

StartedAt

CompletedAt

WithdrawnAt

InvalidatedAt

UpdatedAt
```

Los timestamps deben ser coherentes con el estado del Aggregate.

Ejemplos:

```text
Status = Completed
```

requiere coherencia con:

```text
CompletedAt
```

y:

```text
Status = Withdrawn
```

requiere coherencia con:

```text
WithdrawnAt
```

Las reglas temporales completas pertenecen a las invariantes.

---

# Entidades Internas

Participation debe mantener un límite de consistencia reducido.

No se incorporan como entidades internas:

```text
Citizen

Membership

Role

Territory

Assembly

Proposal

Voting

Document

Notification

Audit
```

Estos conceptos poseen identidad y responsabilidades
independientes.

Si en la evolución del dominio se identifica un concepto interno
que:

- pertenece exclusivamente a Participation;
- no puede existir independientemente;
- requiere consistencia fuerte con Participation;
- no posee Repository propio;

podrá evaluarse como entidad interna conforme a las reglas de
diseño del Aggregate.

Su incorporación deberá documentarse explícitamente.

---

# Value Objects

Entre los Value Objects conceptuales de Participation se
consideran:

```text
ParticipationId

OrganizationId

CitizenId

MembershipId

TerritoryId

AssemblyId

ProposalId

VotingId

ParticipationType

ParticipationStatus

Version
```

Los Value Objects:

- son inmutables;
- no poseen identidad autónoma;
- representan conceptos del dominio;
- validan sus propias reglas de valor;
- no dependen de Infrastructure;
- no dependen de Frameworks.

Las referencias hacia otros Aggregates mediante identificadores no
convierten dichos Aggregates en parte de Participation.

---

# Relaciones con Otros Aggregates

Participation mantiene relaciones con otros Aggregates mediante
identificadores.

```text
Participation
      │
      ├──────── OrganizationId
      │
      ├──────── CitizenId
      │
      ├──────── MembershipId
      │
      ├──────── RoleId
      │
      ├──────── TerritoryId
      │
      ├──────── AssemblyId
      │
      ├──────── ProposalId
      │
      ├──────── VotingId
      │
      ├──────── DocumentId
      │
      ├──────── NotificationId
      │
      └──────── AuditId
```

No todas estas referencias forman necesariamente parte del estado
persistente de cada Participation.

El modelo utiliza únicamente las referencias necesarias para cada
contexto.

Las relaciones conceptuales no implican inclusión estructural.

---

# Organization

Cada Participation pertenece a una única Organization.

La relación se mantiene mediante:

```text
OrganizationId
```

Una Organization puede poseer múltiples Participation.

Participation no administra:

- identidad de Organization;
- Lifecycle de Organization;
- estructura de Organization;
- configuración de Organization.

OrganizationId permanece inmutable durante la vida del Aggregate.

---

# Citizen

Participation puede relacionarse con Citizen mediante:

```text
CitizenId
```

Citizen mantiene:

- identidad propia;
- Lifecycle propio;
- invariantes propias;
- Repository propio;
- consistencia propia.

Participation no administra la identidad cívica.

Participation únicamente mantiene la referencia necesaria para
identificar al actor cuando corresponda.

---

# Membership

Participation puede relacionarse con Membership mediante:

```text
MembershipId
```

Membership representa la relación formal entre Citizen y
Organization.

Participation representa el ejercicio participativo dentro de un
contexto determinado.

Por lo tanto:

```text
Membership

≠

Participation
```

La existencia de una Membership no implica automáticamente una
Participation.

La existencia de una Participation tampoco modifica directamente
Membership.

---

# Role

Los Roles pueden participar en las reglas de autorización o
responsabilidad asociadas a determinados procesos participativos.

Participation no incorpora Role.

La relación, cuando resulte necesaria, se mantiene mediante:

```text
RoleId
```

o mediante las capacidades resueltas por el contexto de
autorización.

Participation no administra Roles ni Permissions.

---

# Territory

Participation puede poseer contexto territorial.

La referencia se mantiene mediante:

```text
TerritoryId
```

Participation no administra:

- geometría;
- límites;
- jerarquía;
- clasificación;
- Lifecycle;
- estado territorial.

Estas responsabilidades pertenecen al Aggregate Territory.

---

# Assembly

Participation puede producirse dentro del contexto de una
Assembly.

La relación se mantiene mediante:

```text
AssemblyId
```

Assembly representa la reunión formal.

Participation representa la participación del actor.

Por lo tanto:

```text
Assembly

≠

Participation
```

Una Assembly puede relacionarse con múltiples Participation.

Cada Participation mantiene identidad independiente.

Participation no modifica Assembly.

---

# Proposal

Participation puede relacionarse con Proposal mediante:

```text
ProposalId
```

Una Proposal puede constituir el objeto o contexto respecto del
cual se ejerce una Participation.

Proposal mantiene:

- identidad propia;
- Lifecycle propio;
- State Machine propia;
- invariantes propias;
- Repository propio;
- Domain Events propios.

Participation no modifica directamente Proposal.

---

# Voting

Participation y Voting representan conceptos diferentes.

Participation representa una instancia de participación.

Voting representa un proceso formal de votación.

Por lo tanto:

```text
Participation

≠

Voting
```

Cuando resulte necesario relacionarlos se utilizará:

```text
VotingId
```

Participation no:

- abre una votación;
- cierra una votación;
- contabiliza votos;
- determina resultados;
- modifica el estado de Voting.

Estas responsabilidades corresponden al Aggregate Voting.

---

# Document

Participation puede relacionarse con Documents cuando exista
información documental asociada.

La relación se mantiene mediante:

```text
DocumentId
```

Document mantiene su propio Aggregate.

Participation no almacena el contenido completo del Document
dentro de su límite de consistencia.

---

# Notification

Los hechos relevantes de Participation pueden originar procesos de
Notification.

Conceptualmente:

```text
Participation Domain Event

↓

Notification Process
```

Participation no envía Notifications directamente.

Notification mantiene su propia responsabilidad.

---

# Audit

Los cambios relevantes de Participation pueden ser utilizados por
Audit.

Participation no incorpora registros de Audit como entidades
internas.

La trazabilidad se establece mediante:

```text
ParticipationId

Version

Domain Events

timestamps

actor references
```

Audit permanece fuera del Aggregate.

---

# Integration

Participation puede producir información relevante para
integraciones externas.

La integración se realiza mediante:

```text
Domain Events

↓

Integration Events

↓

Adapters

↓

External Systems
```

Participation no conoce directamente sistemas externos.

---

# Invariantes Iniciales

El Aggregate Participation garantiza, como mínimo:

- ParticipationId es único;
- ParticipationId nunca cambia;
- OrganizationId es obligatorio;
- OrganizationId nunca cambia;
- el actor debe estar identificado según las reglas del contexto;
- ParticipationType debe ser válido;
- Status debe ser válido;
- el contexto participativo debe ser válido;
- las referencias externas deben utilizar identificadores;
- las transiciones de estado deben ser válidas;
- una Participation archivada no puede modificarse normalmente;
- una Participation retirada no puede continuar como Active;
- una Participation invalidada no puede continuar su ciclo normal;
- una Participation completada no puede volver arbitrariamente a
  Active;
- los timestamps deben ser coherentes con el Lifecycle;
- toda modificación válida incrementa Version;
- una operación rechazada no modifica Version;
- Participation no modifica directamente otros Aggregates;
- Participation no contiene otros Aggregates completos.

Las invariantes completas se desarrollarán formalmente en:

```text
DOMAIN-008E-Invariants.md
```

---

# Invariante de Identidad

Debe mantenerse siempre:

```text
ParticipationId(t0)

=

ParticipationId(tn)
```

para toda la vida del Aggregate.

Ningún Command puede sustituir ParticipationId.

---

# Invariante Organizacional

Debe mantenerse:

```text
OrganizationId(t0)

=

OrganizationId(tn)
```

Participation no puede trasladarse de una Organization a otra.

Si el dominio requiere una nueva participación en otra
Organization debe crearse una nueva Participation conforme a las
reglas correspondientes.

---

# Invariante del Actor

Una Participation debe representar una participación atribuible a
un actor válido dentro del contexto correspondiente.

La identidad del actor no puede sustituirse arbitrariamente
después de creada la Participation.

Participation no puede convertirse en la participación de otro
actor mediante una modificación ordinaria.

---

# Invariante de Contexto

Participation debe poseer contexto suficiente para determinar el
proceso o instancia participativa a la cual pertenece.

El contexto puede estar determinado mediante referencias como:

```text
AssemblyId

ProposalId

TerritoryId

VotingId
```

según la naturaleza de la Participation.

No deben introducirse referencias sin significado dentro del
dominio.

---

# Invariante de Estado

Status solo puede cambiar mediante comportamiento explícito del
Aggregate.

No está permitido:

```text
setStatus(...)
```

como mecanismo arbitrario de modificación.

Debe utilizarse comportamiento de dominio que exprese la
transición correspondiente.

---

# Invariante Temporal

Los tiempos registrados deben mantener coherencia causal.

Conceptualmente:

```text
CreatedAt
    │
    ▼
StartedAt
    │
    ▼
CompletedAt
```

cuando se recorra el camino normal.

Una fecha de finalización no puede representar un momento anterior
al inicio de la Participation.

Las rutas alternativas deben mantener coherencia equivalente.

---

# Reglas de Consistencia

Participation constituye un único límite de consistencia.

Todas las modificaciones internas deben producir un estado válido
del Aggregate.

Una operación no puede dejar parcialmente actualizado:

```text
ParticipationId

OrganizationId

Actor References

Context References

ParticipationType

Status

Lifecycle Timestamps

Version
```

La modificación válida del Aggregate constituye una única
transacción lógica.

La coordinación con otros Aggregates utiliza consistencia eventual
cuando corresponda.

---

# Consistency Boundary

El límite de consistencia comprende exclusivamente el estado
necesario para proteger la identidad y el comportamiento de una
Participation.

Conceptualmente:

```text
┌───────────────────────────────────────┐
│       Participation Aggregate         │
│                                       │
│  ParticipationId                      │
│  OrganizationId                       │
│  Actor References                     │
│  Context References                   │
│  ParticipationType                    │
│  Status                               │
│  Lifecycle Timestamps                 │
│  Version                              │
│                                       │
└───────────────────────────────────────┘
```

Fuera del límite permanecen:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Voting

Document

Notification

Audit

Integration
```

La definición formal se desarrollará en:

```text
DOMAIN-008J-Consistency-Boundary.md
```

---

# Regla de No Absorción

Participation no absorbe otros Aggregates debido a que estos
participen en un mismo proceso.

Por ejemplo:

```text
Assembly
    │
    └── Participation
            │
            └── Proposal
```

no significa que Assembly o Proposal formen parte del Aggregate
Participation.

La representación correcta mantiene límites independientes:

```text
Assembly Aggregate

        │
        │ AssemblyId
        ▼

Participation Aggregate

        │
        │ ProposalId
        ▼

Proposal Aggregate
```

Cada Aggregate conserva:

- identidad;
- Lifecycle;
- State Machine;
- invariantes;
- Repository;
- Version;
- Domain Events;
- consistencia.

---

# Regla de No Confusión con Membership

Membership y Participation poseen responsabilidades diferentes.

```text
Membership
```

representa una relación organizacional.

```text
Participation
```

representa una instancia de participación.

Por lo tanto:

```text
Active Membership

≠

Active Participation
```

Una Membership puede existir durante meses o años.

Una Participation puede representar una instancia específica
dentro de una Assembly, Proposal, consulta u otro contexto
participativo.

---

# Regla de No Confusión con Voting

Voting no debe modelarse como un subtipo de Participation dentro
de este Aggregate.

Voting posee responsabilidades propias relacionadas con el proceso
formal de votación.

Participation puede proporcionar contexto sobre la participación
del actor, pero no administra el proceso de Voting.

---

# Reglas de Modificación

El estado de Participation solo puede modificarse mediante
comportamientos definidos por el Aggregate.

No se permiten setters públicos para modificar directamente:

```text
ParticipationId

OrganizationId

ActorId

Status

Version
```

Las operaciones deben validar previamente:

- identidad;
- estado actual;
- transición solicitada;
- contexto;
- invariantes;
- condiciones temporales;
- reglas organizacionales aplicables.

---

# Comportamiento del Aggregate

Participation expone comportamiento de dominio.

Operaciones conceptuales:

```text
register()

activate()

complete()

withdraw()

invalidate()

archive()
```

Pueden existir comportamientos adicionales relacionados con
información propia de Participation siempre que se mantengan
dentro del límite definido.

Cada comportamiento debe:

- expresar intención del dominio;
- validar el estado actual;
- validar precondiciones;
- preservar invariantes;
- modificar únicamente Participation;
- actualizar timestamps cuando corresponda;
- incrementar Version ante modificación válida;
- producir Domain Events cuando corresponda.

La definición formal de Commands se desarrollará en:

```text
DOMAIN-008C-Commands.md
```

---

# Register

`register()` crea una nueva instancia formal de Participation.

La operación debe establecer como mínimo:

```text
ParticipationId

OrganizationId

Actor Reference

ParticipationType

Context

Status

CreatedAt

Version
```

El estado inicial conceptual es:

```text
Registered
```

La creación debe producir el hecho de dominio correspondiente.

---

# Activate

`activate()` representa el inicio efectivo de una Participation
previamente registrada.

Conceptualmente:

```text
Registered

↓

Active
```

La operación debe:

- verificar estado;
- verificar condiciones del contexto;
- proteger invariantes;
- registrar StartedAt;
- incrementar Version;
- producir el Domain Event correspondiente.

---

# Complete

`complete()` representa la finalización válida de una
Participation.

Conceptualmente:

```text
Active

↓

Completed
```

La operación debe:

- validar que Participation pueda finalizar;
- registrar CompletedAt;
- preservar la historia;
- incrementar Version;
- producir el Domain Event correspondiente.

---

# Withdraw

`withdraw()` representa el retiro explícito de una Participation
cuando las reglas lo permitan.

Conceptualmente puede producirse desde estados habilitados por la
State Machine.

La operación debe:

- validar estado;
- validar reglas de retiro;
- registrar WithdrawnAt;
- incrementar Version;
- producir el Domain Event correspondiente.

Withdraw no elimina Participation.

---

# Invalidate

`invalidate()` representa la invalidación formal de Participation.

La invalidación debe estar respaldada por una regla válida del
dominio.

La operación debe:

- validar que el estado permita invalidación;
- preservar identidad;
- registrar InvalidatedAt;
- incrementar Version;
- producir el Domain Event correspondiente.

Invalidation no equivale a eliminación física.

---

# Archive

`archive()` representa el paso de una Participation terminal hacia
conservación lógica.

Conceptualmente:

```text
Completed

↓

Archived
```

o:

```text
Withdrawn

↓

Archived
```

o:

```text
Invalidated

↓

Archived
```

según las reglas formales del Lifecycle.

Una Participation archivada deja de aceptar modificaciones
ordinarias.

---

# Commands

El Aggregate responde conceptualmente a Commands como:

```text
RegisterParticipation

ActivateParticipation

CompleteParticipation

WithdrawParticipation

InvalidateParticipation

ArchiveParticipation
```

Los Commands:

- representan intención;
- no representan hechos consumados;
- deben dirigirse a un único Aggregate;
- deben respetar Permissions;
- deben respetar State Machine;
- deben preservar invariantes.

La definición formal se desarrollará en:

```text
DOMAIN-008C-Commands.md
```

---

# Domain Events

Participation publica Domain Events cuando ocurren hechos
relevantes.

Eventos conceptuales:

```text
ParticipationRegistered

ParticipationActivated

ParticipationCompleted

ParticipationWithdrawn

ParticipationInvalidated

ParticipationArchived
```

Los eventos:

- representan hechos consumados;
- son inmutables;
- pertenecen al lenguaje del dominio;
- mantienen trazabilidad;
- no representan Commands.

La definición formal se documentará en:

```text
DOMAIN-008D-Domain-Events.md
```

---

# Relación entre Commands y Domain Events

Debe mantenerse la separación:

```text
RegisterParticipation
```

representa intención.

```text
ParticipationRegistered
```

representa un hecho ocurrido.

De forma equivalente:

```text
CompleteParticipation

↓

ParticipationCompleted
```

El Command puede ser rechazado.

El Domain Event solo existe cuando la operación fue aceptada y el
hecho ocurrió.

---

# Integration Events

Los Domain Events de Participation pueden originar Integration
Events cuando otros Bounded Contexts o sistemas externos requieran
información.

Conceptualmente:

```text
Participation Domain Event

↓

Integration Mapping

↓

Participation Integration Event

↓

External Consumer
```

Los Integration Events:

- no exponen el Aggregate completo;
- no permiten modificar Participation;
- constituyen contratos externos;
- pueden evolucionar independientemente del modelo interno.

La definición formal se desarrollará en:

```text
DOMAIN-008K-Integration-Events.md
```

---

# Persistencia

El Repository de Participation persiste el Aggregate completo como
unidad de consistencia.

El Repository no debe permitir modificar atributos individuales
evitando el comportamiento del Aggregate.

Conceptualmente:

```text
ParticipationRepository

    getById()

    exists()

    save()
```

El contrato exacto se desarrollará en:

```text
DOMAIN-008G-Repository-Contract.md
```

---

# Independencia de Persistencia

Participation no depende de:

- PostgreSQL;
- MongoDB;
- MySQL;
- SQLite;
- Redis;
- ORM;
- documentos JSON;
- tablas;
- colecciones.

El modelo de persistencia implementa el dominio.

El dominio no se diseña a partir del modelo de persistencia.

---

# Versionado

Participation mantiene:

```text
Version
```

Version representa la evolución lógica del Aggregate y permite
controlar concurrencia optimista.

Cada modificación válida incrementa Version.

Conceptualmente:

```text
Version(n)

↓

Valid Modification

↓

Version(n + 1)
```

Una operación rechazada mantiene:

```text
Version(n)
```

La especificación formal se documentará en:

```text
DOMAIN-008I-Versioning.md
```

---

# Concurrencia

Dos modificaciones concurrentes sobre la misma Participation no
deben sobrescribirse silenciosamente.

El Repository debe poder comparar:

```text
ExpectedVersion
```

con:

```text
PersistedVersion
```

Cuando ambas no coincidan debe producirse un conflicto de
concurrencia.

La resolución no debe violar las invariantes del Aggregate.

---

# Consultas

Las consultas sobre Participation no modifican el Aggregate.

La arquitectura puede utilizar modelos especializados de lectura
cuando corresponda.

Conceptualmente pueden existir vistas como:

```text
ParticipationSummary

ParticipationDetail

ParticipationByCitizen

ParticipationByMembership

ParticipationByAssembly

ParticipationByProposal

ParticipationByTerritory

ParticipationStatus

ParticipationStatistics
```

Estas vistas no forman parte del Aggregate.

La definición formal se desarrollará en:

```text
DOMAIN-008L-Read-Model.md
```

---

# CQRS

Participation es compatible con separación entre escritura y
lectura.

Conceptualmente:

```text
Commands

↓

Participation Aggregate

↓

Domain Events

↓

Projection

↓

Read Models
```

El Aggregate protege el lado de escritura.

Los Read Models proporcionan vistas optimizadas para consulta.

---

# Event Sourcing

Participation es compatible con Event Sourcing.

Cuando dicha estrategia sea utilizada, los Domain Events pueden
representar la historia necesaria para reconstruir el estado del
Aggregate.

Conceptualmente:

```text
ParticipationRegistered

↓

ParticipationActivated

↓

ParticipationCompleted
```

puede reconstruir una Participation completada.

La compatibilidad con Event Sourcing no obliga a una tecnología
específica de persistencia.

---

# Seguridad

Participation no administra autenticación.

No almacena:

- contraseñas;
- tokens;
- JWT;
- claves privadas;
- secretos;
- credenciales;
- sesiones.

La identidad autenticada del actor se resuelve fuera del
Aggregate.

Participation recibe una intención autorizada y protege sus
propias reglas de dominio.

---

# Permisos

La autorización determina si un actor puede intentar ejecutar un
Command.

El Aggregate determina si dicho Command es válido de acuerdo con
su estado e invariantes.

Debe mantenerse:

```text
Authorization

≠

Domain Invariants
```

Un actor autorizado no puede ejecutar una transición inválida.

Una transición válida tampoco implica que cualquier actor se
encuentre autorizado para ejecutarla.

La definición formal de Permissions se desarrollará en:

```text
DOMAIN-008F-Permissions.md
```

---

# Aislamiento Organizacional

Participation pertenece a una única Organization.

Las operaciones deben respetar el límite organizacional
determinado por:

```text
OrganizationId
```

Un actor perteneciente a otro contexto organizacional no debe
obtener capacidad implícita para modificar Participation.

La autorización concreta se resuelve fuera del Aggregate.

La inmutabilidad de OrganizationId permanece protegida dentro del
dominio.

---

# Privacidad

Participation puede relacionarse con información asociada a
Citizen o Membership.

El Aggregate debe mantener únicamente la información necesaria
para cumplir su responsabilidad.

No debe duplicar información personal perteneciente a Citizen
cuando una referencia sea suficiente.

Debe mantenerse el principio:

```text
Reference when possible

instead of

Personal Data Duplication
```

Las necesidades de lectura o integración deben utilizar
proyecciones y contratos apropiados.

---

# Auditoría

Participation produce hechos de dominio que permiten construir
trazabilidad.

Conceptualmente:

```text
ParticipationId

Version

Domain Events

Actor References

Timestamps

CorrelationId

CausationId
```

pueden contribuir al proceso de auditoría.

Participation no administra el Aggregate Audit.

---

# Trazabilidad

Toda modificación relevante debe poder relacionarse con:

- ParticipationId;
- Version;
- actor;
- momento;
- Command;
- Domain Event;
- contexto;
- correlación cuando corresponda.

La trazabilidad no autoriza la modificación directa del Aggregate.

---

# Integraciones

Participation puede integrarse conceptualmente con:

- plataformas municipales;
- plataformas de participación ciudadana;
- sistemas de gobierno abierto;
- ecosistemas Smart City;
- sistemas territoriales;
- sistemas de análisis;
- sistemas de notificación;
- sistemas de auditoría;
- sistemas de interoperabilidad.

Estas integraciones permanecen fuera del Aggregate.

Participation no conoce:

- endpoints HTTP;
- APIs externas;
- OAuth;
- JWT;
- proveedores;
- SDKs;
- brokers;
- bases de datos externas.

---

# Interoperabilidad

Participation puede proporcionar información a otros contextos
mediante contratos explícitos.

Conceptualmente:

```text
Participation

↓

Domain Event

↓

Integration Event

↓

Adapter

↓

External System
```

El modelo externo no sustituye al modelo de dominio.

Debe mantenerse:

```text
Participation Domain Model

≠

External Integration Model
```

---

# Dependencias

Participation depende conceptualmente de:

- Shared Kernel;
- Value Objects;
- Domain Events;
- Repository Contracts;
- reglas de dominio;
- identificadores de otros Aggregates.

Participation no depende de:

- Infrastructure;
- Frameworks;
- bases de datos;
- HTTP;
- OAuth;
- JWT;
- React;
- Flutter;
- FastAPI;
- Django;
- proveedores externos.

---

# Límites del Aggregate

El límite de Participation comprende exclusivamente los conceptos
necesarios para mantener:

- identidad;
- propiedad organizacional;
- actor participante;
- contexto;
- tipo;
- estado;
- Lifecycle;
- temporalidad;
- Version;
- invariantes.

No forman parte del límite:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Voting

Document

Notification

Audit

Integration
```

Estos conceptos pueden relacionarse con Participation, pero
conservan sus propios límites.

---

# Reglas de Interacción entre Aggregates

La interacción con otros Aggregates se realiza mediante:

```text
AggregateId

Domain Events

Integration Events

Repository Contracts

Application Services
```

Participation nunca obtiene una referencia mutable a otro
Aggregate.

Participation nunca modifica directamente:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Voting

Document

Notification

Audit
```

La coordinación entre estos conceptos ocurre fuera del Aggregate.

---

# Consistencia entre Aggregates

Cuando una operación requiera información de otros Aggregates,
Participation no amplía automáticamente su límite de consistencia.

Debe mantenerse:

```text
Participation Transaction

≠

Distributed Aggregate Transaction
```

La consistencia interna de Participation es fuerte.

La coordinación entre Aggregates utiliza consistencia eventual
cuando corresponda.

---

# Casos de Uso Conceptuales

Participation soporta conceptualmente casos de uso como:

```text
Registrar una Participation.

Activar una Participation.

Completar una Participation.

Retirar una Participation.

Invalidar una Participation.

Archivar una Participation.

Consultar participaciones de un Citizen.

Consultar participaciones de una Membership.

Consultar participaciones de una Assembly.

Consultar participaciones asociadas a una Proposal.

Consultar participaciones por Territory.
```

Los casos de consulta no modifican el Aggregate.

Cada operación de escritura debe respetar las invariantes y la
State Machine.

---

# Restricciones

No está permitido:

- modificar ParticipationId;
- modificar OrganizationId;
- modificar Version directamente;
- modificar Status directamente;
- sustituir arbitrariamente al actor participante;
- ejecutar una transición inválida;
- modificar una Participation archivada mediante operaciones
  ordinarias;
- continuar normalmente una Participation retirada;
- continuar normalmente una Participation invalidada;
- modificar otros Aggregates desde Participation;
- almacenar otros Aggregates completos dentro de Participation;
- utilizar Voting como entidad interna de Participation;
- utilizar Assembly como entidad interna de Participation;
- utilizar Proposal como entidad interna de Participation;
- utilizar Membership como entidad interna de Participation;
- utilizar Infrastructure como dependencia del dominio;
- utilizar modelos externos como modelo interno del Aggregate.

---

# Rechazo de Operaciones

Participation debe rechazar una operación cuando:

- ParticipationId no corresponde al Aggregate esperado;
- OrganizationId no corresponde al contexto;
- el estado actual no permite la operación;
- la transición solicitada es inválida;
- el contexto participativo no cumple las reglas;
- se viola una invariante;
- la Participation se encuentra archivada;
- existe conflicto de Version;
- la operación intenta modificar identidad;
- la operación intenta modificar otro Aggregate.

Cuando una operación es rechazada:

```text
State Unchanged

Version Unchanged

No Success Domain Event
```

---

# Eliminación

Participation no utiliza eliminación física como comportamiento
normal del dominio.

Los estados:

```text
Withdrawn

Invalidated

Archived
```

preservan la existencia histórica del Aggregate.

La desaparición física de datos pertenece a políticas de
persistencia, privacidad o cumplimiento que no deben reinterpretar
el significado histórico del dominio.

---

# Regla de Historia

Una Participation que existió no deja conceptualmente de haber
existido debido a:

- retiro;
- invalidación;
- archivado.

Su estado puede cambiar.

Su identidad y trazabilidad permanecen.

---

# Performance

Las optimizaciones de rendimiento no pueden alterar las reglas del
Aggregate.

Debe mantenerse:

```text
Performance Optimization

≠

Domain Rule Bypass
```

Las necesidades de consultas masivas deben resolverse mediante
Read Models cuando corresponda.

No debe ampliarse Participation con colecciones externas
únicamente para evitar consultas.

La especificación formal se desarrollará en:

```text
DOMAIN-008N-Performance-Rules.md
```

---

# Security Model

La protección de Participation comprende conceptualmente:

- autorización;
- aislamiento organizacional;
- protección de identidad;
- protección de estado;
- protección de Version;
- minimización de datos;
- protección de Commands;
- protección de eventos;
- protección de proyecciones;
- protección de integraciones.

La definición formal se desarrollará en:

```text
DOMAIN-008O-Security-Model.md
```

---

# Testabilidad

Toda implementación de Participation debe poder demostrar mediante
escenarios verificables que respeta:

- identidad;
- Lifecycle;
- State Machine;
- Commands;
- Domain Events;
- invariantes;
- Permissions;
- Repository Contract;
- Version;
- Consistency Boundary;
- Integration Events;
- Read Models;
- concurrencia;
- seguridad.

Los escenarios conceptuales se desarrollarán en:

```text
DOMAIN-008M-Test-Scenarios.md
```

---

# Extension Points

Participation puede evolucionar mediante nuevos conceptos siempre
que no se altere implícitamente su responsabilidad fundamental.

Los puntos de extensión pueden incluir:

- nuevos tipos de Participation;
- nuevas reglas participativas;
- nuevos comportamientos;
- nuevas políticas;
- nuevos Commands;
- nuevos Domain Events;
- nuevas Permissions;
- nuevas relaciones mediante identificadores;
- nuevos Integration Events;
- nuevos Read Models.

Toda extensión debe preservar:

```text
ParticipationId

Aggregate Root

Organization Boundary

Lifecycle

State Machine

Invariants

Version

Consistency Boundary
```

La definición formal se desarrollará en:

```text
DOMAIN-008P-Extension-Points.md
```

---

# Regla de No Inferencia

La existencia de una relación conceptual no autoriza a incorporar
automáticamente comportamiento perteneciente a otro Aggregate.

Por ejemplo:

```text
Participation → Voting
```

no autoriza a Participation a ejecutar Voting.

```text
Participation → Proposal
```

no autoriza a Participation a modificar Proposal.

```text
Participation → Assembly
```

no autoriza a Participation a modificar Assembly.

Las capacidades deben permanecer dentro del Aggregate responsable.

---

# Regla de No Duplicación

Participation no debe duplicar información cuya fuente oficial
pertenece a otro Aggregate.

Debe preferirse:

```text
CitizenId
```

sobre copiar el perfil completo de Citizen.

Debe preferirse:

```text
MembershipId
```

sobre copiar el estado completo de Membership.

Debe preferirse:

```text
AssemblyId
```

sobre copiar Assembly.

Debe preferirse:

```text
ProposalId
```

sobre copiar Proposal.

Debe preferirse:

```text
TerritoryId
```

sobre copiar Territory.

---

# Regla de Fuente de Verdad

Participation constituye la fuente conceptual oficial de verdad
respecto del estado de una instancia de Participation.

No constituye fuente de verdad para:

- Citizen;
- Membership;
- Role;
- Territory;
- Assembly;
- Proposal;
- Voting;
- Document;
- Notification;
- Audit.

Cada Aggregate conserva autoridad sobre su propio estado.

---

# Regla de Autoridad del Aggregate Root

Toda modificación de Participation debe atravesar:

```text
Command

↓

Participation Aggregate Root

↓

Invariant Validation

↓

State Transition

↓

Version Increment

↓

Domain Event
```

No debe existir una ruta alternativa que permita modificar el
estado persistido evitando el Aggregate Root.

---

# Regla de Separación de Intención y Hecho

Debe mantenerse:

```text
Command

≠

Domain Event
```

Un Command solicita una modificación.

Un Domain Event declara que el hecho ocurrió.

Un Command puede ser rechazado.

Un Domain Event de éxito no debe publicarse cuando la operación
fue rechazada.

---

# Regla de Separación entre Dominio y Autorización

Debe mantenerse:

```text
Permission Check

↓

Authorized Intent

↓

Participation Aggregate

↓

Domain Validation
```

La autorización no sustituye las invariantes.

Las invariantes no sustituyen la autorización.

---

# Regla de Separación entre Dominio e Infraestructura

Debe mantenerse:

```text
Domain

↓

Ports

↓

Adapters

↓

Infrastructure
```

Participation permanece independiente de la implementación
tecnológica.

---

# Regla de Separación entre Escritura y Lectura

Cuando se utilice CQRS:

```text
Write Side

Participation Aggregate

↓

Domain Events

↓

Read Side

Participation Read Models
```

Los Read Models no modifican Participation.

Participation no se amplía para satisfacer necesidades exclusivas
de consulta.

---

# Regla de Evolución

Participation puede evolucionar conforme evolucione el dominio.

Toda evolución debe:

- utilizar lenguaje ubicuo;
- preservar identidad;
- preservar límites;
- proteger invariantes;
- mantener trazabilidad;
- evitar acoplamiento tecnológico;
- mantener coherencia documental.

Las extensiones no deben introducir decisiones implícitas que
contradigan los documentos oficiales del Aggregate.

---

# Compatibilidad Arquitectónica

El Aggregate Participation está diseñado conforme a:

- Domain-Driven Design;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS;
- Event Sourcing Compatible;
- Event-Driven Architecture;
- arquitectura distribuida;
- interoperabilidad basada en contratos.

El modelo de dominio permanece independiente de la tecnología de
implementación.

---

# Documentación Complementaria

El Aggregate Participation se desarrolla mediante los siguientes
artefactos conceptuales:

```text
DOMAIN-008-Aggregate.md

DOMAIN-008A-Lifecycle.md

DOMAIN-008B-State-Machine.md

DOMAIN-008C-Commands.md

DOMAIN-008D-Domain-Events.md

DOMAIN-008E-Invariants.md

DOMAIN-008F-Permissions.md

DOMAIN-008G-Repository-Contract.md

DOMAIN-008H-Examples.md

DOMAIN-008I-Versioning.md

DOMAIN-008J-Consistency-Boundary.md

DOMAIN-008K-Integration-Events.md

DOMAIN-008L-Read-Model.md

DOMAIN-008M-Test-Scenarios.md

DOMAIN-008N-Performance-Rules.md

DOMAIN-008O-Security-Model.md

DOMAIN-008P-Extension-Points.md
```

Estos documentos desarrollan dimensiones específicas del
Aggregate sin sustituir la definición conceptual establecida en
`DOMAIN-008-Aggregate.md`.

---

# Coherencia Documental

Todos los documentos de DOMAIN-008 deben mantener coherencia con
esta definición.

No debe existir una regla en:

```text
DOMAIN-008C-Commands.md
```

que contradiga:

```text
DOMAIN-008B-State-Machine.md
```

ni una transición que viole:

```text
DOMAIN-008E-Invariants.md
```

ni una operación de persistencia que evite:

```text
DOMAIN-008G-Repository-Contract.md
```

ni una extensión que viole:

```text
DOMAIN-008J-Consistency-Boundary.md
```

El conjunto documental representa una única definición coherente
del Aggregate Participation.

---

# Principios de Diseño

Participation cumple los siguientes principios:

- una única Aggregate Root;
- identidad propia;
- propiedad organizacional explícita;
- actor identificable;
- contexto participativo explícito;
- límite de consistencia reducido;
- comportamiento de dominio explícito;
- invariantes protegidas;
- referencias externas mediante identificadores;
- ausencia de modificación directa de otros Aggregates;
- consistencia interna fuerte;
- consistencia eventual entre Aggregates;
- Version creciente;
- concurrencia optimista;
- separación entre Commands y Domain Events;
- separación entre Domain Events e Integration Events;
- separación entre Participation y Voting;
- separación entre Participation y Membership;
- separación entre dominio y autorización;
- separación entre dominio e Infrastructure;
- independencia tecnológica;
- alta cohesión;
- bajo acoplamiento;
- trazabilidad;
- evolución controlada.

---

# Definición de Éxito

El Aggregate **Participation** constituye el modelo oficial para
representar una instancia formal de participación dentro del
ecosistema AURA.

Participation permite identificar de manera inequívoca una
participación, asociarla a una Organization y a un actor,
contextualizarla respecto de Assembly, Proposal, Territory,
Voting u otros procesos reconocidos por el dominio cuando
corresponda, y controlar su ciclo de vida sin absorber las
responsabilidades de dichos Aggregates.

El Aggregate protege su identidad, contexto, estado, temporalidad,
invariantes y Version mediante una única Aggregate Root y un
límite de consistencia explícito.

Participation mantiene una separación fundamental entre:

```text
Membership

Participation

Voting
```

Membership representa la relación organizacional que puede
habilitar la participación.

Participation representa la instancia formal mediante la cual el
actor participa.

Voting representa el proceso específico mediante el cual se
desarrolla una votación.

Asimismo, Participation mantiene separados:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Voting

Document

Notification

Audit

Integration
```

conservando para cada uno su propia identidad, ciclo de vida,
invariantes, Repository y límite de consistencia.

Las modificaciones de Participation se realizan exclusivamente
mediante comportamiento de dominio, respetando Lifecycle, State
Machine, Permissions, invariantes, Version y trazabilidad.

Las relaciones con otros Aggregates se mantienen mediante
identificadores, Domain Events, Integration Events y coordinación
externa cuando corresponda.

De esta forma, `DOMAIN-008-Aggregate.md` constituye la fuente
conceptual oficial del Aggregate **Participation** y proporciona
la base normativa para desarrollar Lifecycle, State Machine,
Commands, Domain Events, Invariants, Permissions, Repository
Contract, Examples, Versioning, Consistency Boundary, Integration
Events, Read Models, Test Scenarios, Performance Rules, Security
Model y Extension Points, manteniendo la arquitectura DDD
consolidada de AURA Core.