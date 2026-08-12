# DOMAIN-007 — Proposal Aggregate

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

---

# Objetivo

El Aggregate **Proposal** representa una propuesta formal
presentada dentro del ecosistema AURA para expresar una
iniciativa, necesidad, idea, solicitud, solución o materia que
pueda ser conocida, evaluada, deliberada o sometida a procesos
posteriores de participación y gobernanza.

Proposal constituye la unidad formal mediante la cual una
iniciativa adquiere identidad propia dentro del dominio.

Una Proposal puede originarse dentro del contexto de una
Organization, una Assembly, un Territory o un proceso de
participación, manteniendo siempre su propia identidad, ciclo de
vida, estado e invariantes.

Proposal permite representar formalmente una iniciativa sin
absorber los procesos que puedan desarrollarse posteriormente
sobre ella.

La existencia de una Proposal no implica necesariamente:

- deliberación;
- participación;
- votación;
- aprobación;
- ejecución;
- documentación;
- notificación;
- integración externa.

Cada proceso que posea identidad, ciclo de vida o reglas de
consistencia propias permanece bajo la responsabilidad de su
respectivo Aggregate.

---

# Propósito

El Aggregate Proposal tiene como propósito representar de forma
consistente una iniciativa formal dentro del dominio AURA.

Proposal proporciona la identidad y el contexto necesarios para
que una propuesta pueda existir independientemente de los
procesos organizacionales, participativos o de gobernanza que
puedan relacionarse posteriormente con ella.

El Aggregate permite establecer y controlar:

- identidad de la Proposal;
- Organization asociada;
- Citizen proponente cuando corresponda;
- Membership proponente cuando corresponda;
- Territory asociado cuando corresponda;
- Assembly asociada cuando corresponda;
- tipo de Proposal;
- título;
- descripción;
- propósito;
- contenido conceptual;
- contexto de presentación;
- fecha de presentación;
- estado;
- ciclo de vida;
- condiciones de modificación;
- condiciones de retiro;
- condiciones de aceptación o rechazo;
- trazabilidad de modificaciones;
- versión del Aggregate;
- publicación de Domain Events.

Proposal constituye el límite de consistencia de la propuesta.

No constituye el límite de consistencia de los procesos que
puedan evaluar, deliberar, votar, documentar, notificar o
integrar la propuesta.

---

# Definición

Una Proposal representa una iniciativa formal registrada dentro
del ecosistema AURA.

La Proposal posee identidad propia, ciclo de vida, estado,
contenido, contexto organizacional y referencias hacia los
conceptos del dominio necesarios para establecer su origen y
ámbito.

Una Proposal puede representar:

- iniciativa ciudadana;
- propuesta organizacional;
- propuesta comunitaria;
- propuesta territorial;
- propuesta presentada en una Assembly;
- solicitud de mejora;
- iniciativa de proyecto;
- propuesta normativa;
- propuesta de acuerdo;
- propuesta de acción;
- propuesta de solución;
- iniciativa de participación.

La naturaleza específica de una Proposal dependerá de las reglas
de la Organization y del contexto en que sea presentada.

Proposal no representa:

- una Organization;
- un Citizen;
- una Membership;
- un Role;
- un Territory;
- una Assembly;
- una Participation;
- una Voting;
- un Document;
- una Notification;
- un Audit;
- una Integration.

Estos conceptos corresponden a otros Aggregates o Bounded
Contexts del dominio.

---

# Responsabilidades

El Aggregate Proposal es responsable de:

- mantener la identidad de la Proposal;
- mantener la Organization asociada;
- mantener la identidad del proponente cuando corresponda;
- mantener el contexto territorial cuando corresponda;
- mantener el contexto de Assembly cuando corresponda;
- definir el tipo de Proposal;
- mantener el título;
- mantener la descripción;
- mantener el propósito;
- mantener el contenido conceptual de la propuesta;
- administrar su ciclo de vida;
- controlar su estado;
- controlar las condiciones para su presentación;
- controlar las condiciones para su modificación;
- controlar las condiciones para su retiro;
- controlar las condiciones para su aceptación;
- controlar las condiciones para su rechazo;
- proteger las invariantes del Aggregate;
- mantener la trazabilidad de los cambios relevantes;
- incrementar la versión ante modificaciones válidas;
- publicar Domain Events;
- mantener la consistencia de la Proposal como unidad de dominio.

Proposal es responsable de representar la iniciativa como un
hecho formal del dominio.

No administra directamente:

- Organizations;
- Citizens;
- Memberships;
- Roles;
- Territories;
- Assemblies;
- Participations;
- Votings;
- Documents;
- Notifications;
- Audits;
- Integrations.

---

# Responsabilidades Fuera del Aggregate

No es responsabilidad de Proposal:

- administrar Organizations;
- administrar Citizens;
- crear o modificar Memberships;
- definir Roles;
- administrar Territories;
- administrar Assemblies;
- administrar permisos técnicos;
- ejecutar autenticación;
- administrar sesiones;
- ejecutar procesos de Participation;
- ejecutar procesos de Voting;
- almacenar Documents externos;
- enviar Notifications;
- ejecutar procesos de Audit;
- administrar Integrations externas;
- ejecutar materialmente la iniciativa propuesta;
- determinar resultados de procesos pertenecientes a otros
  Aggregates.

Estas responsabilidades pertenecen a sus respectivos Aggregates
o Bounded Contexts.

La colaboración entre ellos se realiza mediante contratos de
dominio, identificadores, Domain Events e Integration Events.

Proposal nunca modifica directamente el estado interno de otro
Aggregate.

---

# Modelo Conceptual

```text
Organization
      │
      │
      ▼
   Proposal
      │
      ├──────── Citizen
      │
      ├──────── Membership
      │
      ├──────── Territory
      │
      ├──────── Assembly
      │
      ├──────── Participation
      │
      ├──────── Voting
      │
      ├──────── Document
      │
      ├──────── Notification
      │
      └──────── Audit
```

Una Organization puede contener el contexto organizacional de
múltiples Proposals.

Una Proposal pertenece al contexto de una única Organization.

Una Proposal puede ser presentada por un Citizen o por una
Membership según las reglas del dominio y del contexto
organizacional.

Una Proposal puede mantener referencias hacia Territory y
Assembly cuando estos conceptos formen parte de su contexto.

Proposal puede posteriormente relacionarse con procesos de
Participation y Voting sin absorberlos dentro de su límite de
consistencia.

Proposal no contiene Aggregates externos.

Los procesos representados por Participation, Voting, Document,
Notification y Audit mantienen sus propias identidades, reglas y
ciclos de vida.

---

# Aggregate Root

La única Aggregate Root es:

```text
Proposal
```

Proposal constituye la única puerta de entrada para modificar el
estado interno del Aggregate.

No existen entidades internas que puedan ser modificadas
directamente desde fuera del Aggregate.

Toda operación que altere una propiedad o condición de Proposal
debe ejecutarse mediante comportamiento definido por el
Aggregate Root.

---

# Identidad

La identidad del Aggregate está determinada por:

```text
ProposalId
```

ProposalId:

- es único;
- es global dentro del dominio;
- es inmutable;
- no depende de la persistencia;
- no cambia durante el ciclo de vida;
- no se reutiliza después de la desaparición lógica del
  Aggregate.

La identidad de Proposal no depende de:

- título;
- OrganizationId;
- CitizenId;
- MembershipId;
- TerritoryId;
- AssemblyId;
- tipo;
- estado;
- fecha de presentación;
- identificadores externos.

Dos Proposals pueden poseer títulos similares o contenidos
relacionados, pero nunca pueden compartir el mismo ProposalId.

---

# Identidad Organizacional

Cada Proposal pertenece al contexto de una Organization.

La relación se representa mediante:

```text
OrganizationId
```

OrganizationId:

- identifica la Organization asociada;
- es obligatorio;
- permanece inmutable durante la vida de Proposal;
- no representa una copia de Organization;
- no permite modificar el estado de Organization.

Proposal mantiene la referencia mediante identidad, no mediante
agregación de la Organization completa.

---

# Proponente

Proposal puede mantener la identidad del actor de dominio que
presenta formalmente la iniciativa.

Dependiendo del contexto, el proponente puede estar representado
mediante:

```text
CitizenId

MembershipId
```

CitizenId identifica al Citizen relacionado con la presentación.

MembershipId identifica la relación organizacional desde la cual
el Citizen actúa cuando las reglas de la Organization así lo
requieran.

La referencia al proponente:

- establece el origen de la Proposal;
- permite mantener trazabilidad;
- no incorpora Citizen dentro del Aggregate;
- no incorpora Membership dentro del Aggregate;
- no permite modificar Citizen;
- no permite modificar Membership.

La validación de existencia, vigencia o habilitación del
proponente debe realizarse mediante los mecanismos de
coordinación definidos entre Aggregates.

---

# Contexto Territorial

Proposal puede estar asociada a un Territory cuando la
naturaleza de la iniciativa posea un ámbito territorial.

La referencia se mantiene mediante:

```text
TerritoryId
```

TerritoryId:

- identifica el territorio asociado;
- puede ser opcional cuando la Proposal no posea ámbito
  territorial;
- no contiene el Aggregate Territory;
- no permite modificar Territory;
- permite contextualizar geográficamente la iniciativa.

El territorio asociado no convierte a Territory en parte del
Aggregate Proposal.

---

# Contexto de Assembly

Una Proposal puede relacionarse con una Assembly cuando sea
presentada, conocida o tratada dentro del contexto formal de una
reunión.

La referencia se mantiene mediante:

```text
AssemblyId
```

AssemblyId:

- identifica la Assembly relacionada;
- puede ser opcional;
- no contiene el Aggregate Assembly;
- no permite modificar Assembly;
- no convierte la Proposal en una entidad interna de Assembly.

Proposal mantiene su identidad y ciclo de vida
independientemente de la Assembly.

La finalización, cancelación o archivado de una Assembly no
modifica automáticamente el estado de Proposal.

Cualquier coordinación necesaria debe ocurrir mediante reglas de
aplicación, Domain Events o Integration Events según corresponda.

---

# Tipo de Proposal

Proposal mantiene una clasificación conceptual que permite
distinguir la naturaleza de la iniciativa.

Tipos conceptuales pueden incluir:

```text
CitizenInitiative

Organizational

Community

Territorial

Project

Improvement

Agreement

Regulatory

Action

Solution

Consultative
```

La clasificación no modifica la identidad de Proposal.

El tipo forma parte del modelo conceptual y puede estar sujeto a
reglas específicas del dominio.

Nuevos tipos podrán incorporarse mediante los mecanismos de
extensión definidos para el Aggregate sin modificar su identidad
fundamental.

---

# Título

Proposal posee un título que permite identificar la iniciativa
de forma comprensible dentro de su contexto.

Ejemplos:

```text
Mejoramiento de iluminación del sector

Recuperación de espacio comunitario

Creación de huerto comunitario

Solicitud de mejoramiento vial
```

El título pertenece al Aggregate Proposal.

No constituye su identidad.

El título puede modificarse mientras el estado del Aggregate y
las invariantes aplicables lo permitan.

---

# Propósito

Proposal mantiene el propósito formal de la iniciativa.

El propósito describe la finalidad que busca alcanzar la
Proposal.

El propósito:

- pertenece al contexto de la iniciativa;
- forma parte del estado del Aggregate;
- debe encontrarse definido cuando las reglas del dominio lo
  exijan;
- no representa una Assembly;
- no representa una Participation;
- no representa una Voting;
- no representa el resultado de una votación.

El propósito puede permanecer estable aunque posteriormente la
Proposal participe en distintos procesos del dominio.

---

# Descripción

Proposal mantiene una descripción formal de la iniciativa.

La descripción permite registrar información contextual que
complemente:

- título;
- propósito;
- tipo;
- ámbito territorial;
- contexto organizacional;
- contexto de presentación.

La descripción pertenece al Aggregate.

No sustituye el propósito ni modifica la identidad de Proposal.

---

# Contenido de la Proposal

Proposal mantiene el contenido conceptual necesario para
representar la iniciativa.

El contenido puede comprender información estructurada necesaria
para expresar:

- problema identificado;
- necesidad;
- justificación;
- solución propuesta;
- objetivos;
- alcance;
- beneficiarios conceptuales;
- contexto;
- antecedentes;
- resultados esperados.

El contenido forma parte del estado de Proposal cuando sea
necesario para preservar la consistencia de la iniciativa.

Proposal no debe utilizarse como repositorio documental.

Los documentos, archivos, imágenes, anexos o evidencias que
posean identidad y ciclo de vida documental pertenecen al
Aggregate Document.

Proposal mantiene únicamente las referencias necesarias hacia
ellos.

---

# Presentación

La presentación constituye el acto mediante el cual una Proposal
deja de ser únicamente una elaboración en preparación y pasa a
ser una iniciativa formalmente presentada dentro del dominio.

La presentación puede registrar conceptualmente:

```text
SubmittedAt

SubmittedBy

SubmissionContext
```

La presentación:

- debe ocurrir desde un estado válido;
- requiere que las condiciones mínimas de la Proposal se
  encuentren satisfechas;
- no puede ejecutarse directamente mediante modificación de
  estado;
- produce un cambio formal dentro del ciclo de vida;
- puede producir Domain Events.

Una Proposal presentada deja de comportarse como un borrador
libremente editable.

Las modificaciones posteriores quedan sujetas a las reglas
definidas por el Aggregate.

---

# Estado

El ciclo de vida de Proposal se representa mediante un estado
propio.

Estados conceptuales:

```text
Draft

Submitted

UnderReview

Accepted

Rejected

Withdrawn

Archived
```

El estado:

- pertenece al Aggregate;
- solo puede cambiar mediante transiciones válidas;
- no puede ser modificado directamente;
- determina qué operaciones están permitidas;
- participa en la protección de las invariantes.

Las transiciones completas se especificarán en:

```text
DOMAIN-007B-State-Machine.md
```

---

# Ciclo de Vida

El ciclo de vida conceptual de Proposal comprende:

```text
Draft
    │
    ▼
Submitted
    │
    ▼
UnderReview
    │
    ├──────────────► Accepted
    │
    └──────────────► Rejected
```

La Proposal puede ser retirada cuando las reglas y el estado lo
permitan:

```text
Draft
    │
    └──────────────► Withdrawn

Submitted
    │
    └──────────────► Withdrawn
```

Los estados terminales pueden conducir al archivado:

```text
Accepted
    │
    ▼
Archived

Rejected
    │
    ▼
Archived

Withdrawn
    │
    ▼
Archived
```

No todas las transiciones son válidas desde todos los estados.

El Aggregate Root controla cada transición.

La definición formal se documentará en:

```text
DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md
```

---

# Entidades Internas

Proposal puede contener entidades internas únicamente cuando
estas formen parte inseparable de su propia consistencia.

Conceptualmente pueden existir estructuras internas destinadas a
representar aspectos del contenido de la Proposal.

Estas estructuras:

- pertenecen exclusivamente al Aggregate Proposal;
- no poseen autonomía fuera del Aggregate;
- no constituyen Aggregates independientes;
- no pueden modificarse directamente desde el exterior;
- existen únicamente cuando sean necesarias para proteger la
  consistencia interna de Proposal.

No deben convertirse en entidades internas de Proposal conceptos
que ya poseen identidad y ciclo de vida propios dentro de AURA.

Por lo tanto, no son entidades internas de Proposal:

```text
Citizen

Membership

Territory

Assembly

Participation

Voting

Document

Notification

Audit
```

---

# Value Objects

Entre los Value Objects conceptuales del Aggregate se consideran:

```text
ProposalId

ProposalTitle

ProposalType

ProposalPurpose

ProposalDescription

ProposalContent

OrganizationId

CitizenId

MembershipId

TerritoryId

AssemblyId

SubmissionContext

SubmittedAt

ProposalStatus

Version
```

Los Value Objects:

- son inmutables;
- no poseen identidad propia;
- representan conceptos del dominio;
- validan sus propias reglas de valor;
- no dependen de Infrastructure;
- no dependen de Frameworks.

La definición concreta de cada Value Object debe preservar el
lenguaje ubicuo establecido por AURA.

---

# Atributos Conceptuales

El estado conceptual de Proposal puede representarse mediante:

```text
ProposalId

OrganizationId

CitizenId

MembershipId

TerritoryId

AssemblyId

ProposalType

ProposalTitle

ProposalPurpose

ProposalDescription

ProposalContent

ProposalStatus

SubmittedAt

CreatedAt

UpdatedAt

ArchivedAt

Version
```

La existencia de un atributo conceptual no implica una decisión
sobre su representación física, esquema de base de datos,
serialización o implementación tecnológica.

El modelo de dominio define significado y reglas.

Infrastructure define posteriormente la representación técnica.

---

# Relaciones con Otros Aggregates

Proposal mantiene relaciones con otros Aggregates mediante
identificadores.

```text
Proposal
    │
    ├──────── OrganizationId
    │
    ├──────── CitizenId
    │
    ├──────── MembershipId
    │
    ├──────── TerritoryId
    │
    ├──────── AssemblyId
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

Estas referencias no implican que los Aggregates formen parte
del Aggregate Proposal.

Proposal no almacena Aggregates completos.

Proposal no modifica Aggregates externos.

Proposal no ejecuta comportamiento perteneciente a otros
Aggregates.

---

# Organization

Cada Proposal pertenece al contexto de una Organization.

La relación conceptual es:

```text
Organization
        │
        │ 1
        ▼
     Proposal
        │
        │ N
```

Una Organization puede relacionarse con múltiples Proposals.

Cada Proposal pertenece a una única Organization.

La propiedad organizacional constituye una condición fundamental
del contexto de Proposal.

Proposal mantiene únicamente:

```text
OrganizationId
```

No administra:

- identidad de Organization;
- ciclo de vida de Organization;
- estructura organizacional;
- reglas internas de Organization.

---

# Citizen

Proposal puede relacionarse con un Citizen como origen ciudadano
de la iniciativa.

La relación se mantiene mediante:

```text
CitizenId
```

Citizen conserva:

- identidad propia;
- estado propio;
- ciclo de vida propio;
- invariantes propias.

Proposal no administra la identidad cívica.

Proposal no modifica Citizen.

---

# Membership

Cuando una Proposal sea presentada dentro de una Organization,
puede ser necesario identificar la Membership desde la cual el
proponente actúa.

La relación se mantiene mediante:

```text
MembershipId
```

Membership conserva su propia identidad y ciclo de vida.

Proposal no:

- crea Membership;
- activa Membership;
- suspende Membership;
- asigna Roles;
- modifica Membership.

Las reglas de pertenencia corresponden al Aggregate Membership.

---

# Territory

Proposal puede mantener una relación con Territory.

```text
Proposal ─────── Territory
```

La relación es opcional según la naturaleza de la iniciativa.

Proposal referencia:

```text
TerritoryId
```

No administra:

- límites territoriales;
- jerarquía territorial;
- estado territorial;
- geometría;
- clasificación territorial.

Estas responsabilidades corresponden al Aggregate Territory.

---

# Assembly

Una Proposal puede relacionarse con una Assembly.

La referencia se mantiene mediante:

```text
AssemblyId
```

La relación permite establecer que una Proposal:

- fue presentada en una Assembly;
- será conocida en una Assembly;
- fue tratada dentro de una Assembly;
- mantiene un contexto formal de reunión.

Assembly conserva:

- identidad propia;
- estado propio;
- ciclo de vida propio;
- invariantes propias.

Proposal no modifica Assembly.

Assembly no se convierte en parte del Aggregate Proposal.

---

# Participation

Proposal puede constituir el objeto o contexto de un proceso de
Participation.

La relación puede establecerse mediante:

```text
ParticipationId
```

Participation mantiene:

- identidad propia;
- ciclo de vida propio;
- reglas propias;
- invariantes propias.

Proposal representa la iniciativa.

Participation representa el proceso mediante el cual actores del
dominio participan respecto de esa iniciativa.

Ambos conceptos permanecen separados.

La actividad participativa no se almacena como estado interno de
Proposal cuando posee identidad y consistencia propias.

---

# Voting

Una Proposal puede constituir la materia sometida a un proceso
de Voting.

La relación puede establecerse mediante:

```text
VotingId
```

Voting posee:

- identidad propia;
- ciclo de vida propio;
- estado propio;
- reglas propias;
- invariantes propias;
- resultado propio.

Proposal no ejecuta la votación.

Proposal no contabiliza votos.

Proposal no determina directamente el resultado de Voting.

Cuando un resultado de Voting deba producir una consecuencia
sobre Proposal, la coordinación ocurre mediante los mecanismos
de dominio definidos entre Aggregates.

---

# Document

Proposal puede relacionarse con Documents.

La referencia se mantiene mediante:

```text
DocumentId
```

Los Documents pueden representar, según corresponda:

- antecedentes;
- anexos;
- evidencias;
- informes;
- archivos complementarios;
- documentación formal relacionada.

Document es responsable de su propio contenido, identidad,
versionado y ciclo de vida.

Proposal no almacena el contenido documental externo como parte
de su Aggregate.

---

# Notification

Proposal puede producir hechos de dominio que originen procesos
de Notification.

Ejemplos conceptuales:

- Proposal presentada;
- Proposal aceptada;
- Proposal rechazada;
- Proposal retirada;
- Proposal archivada.

Proposal no administra el envío de notificaciones.

Notification permanece bajo la responsabilidad de su propio
Aggregate o Bounded Context.

---

# Audit

Los cambios relevantes de Proposal pueden producir información
utilizada por Audit.

Proposal no ejecuta directamente procesos de auditoría.

La trazabilidad se establece mediante:

- ProposalId;
- Version;
- Domain Events;
- referencias de actor cuando correspondan;
- información temporal del Aggregate;
- CorrelationId y CausationId cuando formen parte del flujo
  correspondiente.

Audit conserva su propio límite de consistencia.

---

# Invariantes

El Aggregate Proposal mantiene, como mínimo, las siguientes
invariantes:

- ProposalId nunca cambia.
- ProposalId es único.
- OrganizationId es obligatorio.
- OrganizationId no cambia durante la vida del Aggregate.
- Proposal debe poseer un tipo válido.
- Proposal debe poseer un estado válido.
- Proposal debe poseer un título válido.
- Proposal debe mantener contenido suficiente para la operación
  que intenta ejecutar.
- una Proposal solo puede presentarse desde un estado que permita
  su presentación;
- una Proposal solo puede entrar en revisión desde un estado
  compatible;
- una Proposal solo puede aceptarse desde un estado compatible;
- una Proposal solo puede rechazarse desde un estado compatible;
- una Proposal solo puede retirarse cuando su estado lo permita;
- una Proposal archivada no puede modificarse;
- una Proposal retirada no continúa normalmente hacia estados de
  evaluación;
- una Proposal rechazada no puede convertirse directamente en
  Accepted;
- las transiciones de estado deben ser válidas;
- toda modificación válida incrementa Version;
- Proposal no modifica directamente otros Aggregates;
- las referencias externas se mantienen mediante identificadores;
- los Documents relacionados no forman parte del límite de
  consistencia de Proposal;
- Participation y Voting no forman parte del estado interno de
  Proposal.

Las reglas completas se desarrollarán formalmente en:

```text
DOMAIN-007E-Invariants.md
```

---

# Reglas de Consistencia

Proposal constituye un límite de consistencia.

Todas las modificaciones internas deben producir un estado
válido del Aggregate.

Una operación no puede dejar parcialmente actualizado el estado
de Proposal.

La transacción lógica de Proposal protege conceptualmente:

```text
ProposalId

OrganizationId

Proposer References

TerritoryId

AssemblyId

ProposalType

ProposalTitle

ProposalPurpose

ProposalDescription

ProposalContent

ProposalStatus

Submission Information

Version
```

La coordinación con otros Aggregates utiliza consistencia
eventual cuando corresponda.

No se utilizan transacciones distribuidas para modificar
simultáneamente el estado interno de Proposal y otros Aggregates.

La definición formal del límite de consistencia se documentará
en:

```text
DOMAIN-007J-Consistency-Boundary.md
```

---

# Reglas de Modificación

El estado de Proposal solo puede modificarse mediante
comportamientos definidos por el Aggregate.

No se permiten setters públicos que permitan modificar
directamente:

```text
ProposalId

OrganizationId

ProposalStatus

Version
```

Las modificaciones deben validar previamente:

- estado actual;
- transición solicitada;
- invariantes;
- contexto organizacional;
- condiciones de presentación;
- condiciones de revisión;
- condiciones de retiro;
- reglas aplicables al tipo de Proposal.

La modificación de información editable debe respetar el ciclo
de vida.

Una Proposal en Draft puede permitir un nivel de modificación
diferente al de una Proposal ya presentada.

---

# Comportamiento del Aggregate

Proposal expone comportamiento de dominio y no simples
operaciones de almacenamiento.

Operaciones conceptuales:

```text
create()

changeType()

rename()

changePurpose()

changeDescription()

updateContent()

changeTerritory()

associateAssembly()

submit()

startReview()

accept()

reject()

withdraw()

archive()
```

Cada comportamiento debe proteger las invariantes
correspondientes.

La existencia conceptual de estas operaciones no define todavía
su firma técnica ni su implementación.

La especificación formal de Commands se desarrollará en:

```text
DOMAIN-007C-Commands.md
```

---

# Presentación y Evaluación

Proposal diferencia explícitamente la existencia de una
iniciativa de los procesos posteriores que puedan actuar sobre
ella.

Conceptualmente:

```text
Proposal Created
       │
       ▼
     Draft
       │
       ▼
   Submitted
       │
       ▼
  UnderReview
       │
       ├────────► Accepted
       │
       └────────► Rejected
```

La evaluación representada por el ciclo de vida de Proposal
determina la condición formal de la iniciativa dentro de su
propio Aggregate.

Esto no significa que Proposal implemente internamente:

- deliberación colectiva;
- participación ciudadana;
- votación;
- conteo de votos;
- documentación;
- notificación.

Si una decisión depende de Voting, Participation u otro
Aggregate, el resultado correspondiente debe llegar a Proposal
mediante coordinación explícita.

---

# Aceptación

Accepted representa que la Proposal ha alcanzado una condición
formal de aceptación dentro de su ciclo de vida.

Accepted no significa necesariamente:

- ejecución inmediata;
- implementación material;
- aprobación presupuestaria;
- creación automática de un proyecto;
- modificación automática de otro Aggregate;
- resultado directo de una Voting específica.

El significado concreto de la aceptación debe permanecer dentro
del lenguaje ubicuo y de las reglas establecidas para Proposal.

Cuando la aceptación dependa de otro proceso, la coordinación
debe conservar los límites entre Aggregates.

---

# Rechazo

Rejected representa que la Proposal ha sido formalmente
rechazada dentro de su ciclo de vida.

El rechazo:

- no elimina la Proposal;
- no modifica ProposalId;
- conserva la trazabilidad;
- constituye un hecho de dominio;
- puede producir Domain Events;
- puede conducir posteriormente al archivado.

Una Proposal rechazada conserva su identidad histórica.

---

# Retiro

Withdrawn representa que la Proposal ha sido retirada de su flujo
normal de tratamiento mediante una operación válida del dominio.

El retiro:

- no elimina físicamente la Proposal;
- conserva ProposalId;
- conserva trazabilidad;
- impide continuar normalmente el flujo desde el estado retirado;
- puede conducir al archivado.

Las condiciones exactas de retiro serán definidas en los
documentos de Lifecycle, State Machine e Invariants.

---

# Archivado

Archived representa la condición en la cual Proposal deja de
admitir modificaciones operativas normales y permanece
disponible como referencia histórica del dominio.

El archivado:

- no elimina la identidad;
- no elimina la trazabilidad;
- no elimina los Domain Events ya producidos;
- no permite modificaciones ordinarias;
- constituye una transición controlada.

Archived no equivale a eliminación física.

---

# Persistencia

El Repository de Proposal persiste el Aggregate como una unidad
de consistencia.

El Repository no expone operaciones destinadas a modificar
atributos internos individualmente fuera del Aggregate.

El modelo de persistencia no define el modelo de dominio.

Proposal no depende de:

- MongoDB;
- PostgreSQL;
- MySQL;
- SQLite;
- ORM;
- HTTP;
- Frameworks.

El contrato del Repository se especificará en:

```text
DOMAIN-007G-Repository-Contract.md
```

---

# Versionado

Proposal utiliza versionado optimista.

El Aggregate mantiene:

```text
Version
```

Cada modificación válida incrementa la versión.

El Repository debe validar que la versión esperada coincida con
la versión persistida antes de aceptar una modificación.

Una modificación concurrente incompatible debe producir un
conflicto de concurrencia.

Version pertenece al control de consistencia del Aggregate.

No representa:

- versión de un Document;
- versión de una API;
- versión de un Integration Event;
- versión del esquema de persistencia.

La especificación formal se documentará en:

```text
DOMAIN-007I-Versioning.md
```

---

# Domain Events

Proposal publica Domain Events cuando ocurren hechos relevantes
dentro de su ciclo de vida.

Eventos conceptuales:

```text
ProposalCreated

ProposalTypeChanged

ProposalRenamed

ProposalPurposeChanged

ProposalDescriptionChanged

ProposalContentUpdated

ProposalTerritoryChanged

ProposalAssemblyAssociated

ProposalSubmitted

ProposalReviewStarted

ProposalAccepted

ProposalRejected

ProposalWithdrawn

ProposalArchived
```

Los eventos representan hechos consumados.

No representan Commands.

Los Domain Events pertenecen al lenguaje del dominio y expresan
cambios que ya fueron aceptados por el Aggregate.

La definición formal se documentará en:

```text
DOMAIN-007D-Domain-Events.md
```

---

# Integration Events

Los Domain Events de Proposal pueden dar origen a Integration
Events cuando otros Bounded Contexts o sistemas externos
requieran conocer cambios relevantes.

Conceptualmente pueden existir eventos de integración
relacionados con:

```text
ProposalSubmitted

ProposalAccepted

ProposalRejected

ProposalWithdrawn

ProposalArchived
```

Los Integration Events:

- no exponen el Aggregate completo;
- no permiten modificar directamente Proposal;
- representan contratos de interoperabilidad;
- pueden poseer una representación diferente a los Domain Events;
- evolucionan bajo reglas de integración.

La especificación formal se desarrollará en:

```text
DOMAIN-007K-Integration-Events.md
```

---

# Commands

El Aggregate Proposal responde conceptualmente a Commands como:

```text
CreateProposal

ChangeProposalType

RenameProposal

ChangeProposalPurpose

ChangeProposalDescription

UpdateProposalContent

ChangeProposalTerritory

AssociateProposalWithAssembly

SubmitProposal

StartProposalReview

AcceptProposal

RejectProposal

WithdrawProposal

ArchiveProposal
```

Los Commands expresan intención.

No representan hechos consumados.

Un Command puede ser rechazado cuando:

- el estado actual no permite la operación;
- las invariantes no se cumplen;
- la información requerida es inválida;
- el actor no se encuentra autorizado;
- existe un conflicto de versión;
- las precondiciones de dominio no se cumplen.

Un Command rechazado no modifica el estado del Aggregate.

La definición formal se desarrollará en:

```text
DOMAIN-007C-Commands.md
```

---

# Consultas

Las consultas sobre Proposal no deben modificar el Aggregate.

La lectura puede utilizar modelos especializados cuando la
arquitectura CQRS lo requiera.

El Read Model puede proyectar información como:

```text
ProposalId

OrganizationId

CitizenId

MembershipId

TerritoryId

AssemblyId

ProposalTitle

ProposalType

ProposalPurpose

ProposalStatus

SubmittedAt

CreatedAt

UpdatedAt

Version
```

Los Read Models:

- no forman parte del límite de consistencia de Proposal;
- no ejecutan lógica de negocio;
- pueden ser reconstruibles;
- pueden estar desnormalizados;
- pueden optimizar búsquedas y visualización.

La especificación del Read Model se desarrollará en:

```text
DOMAIN-007L-Read-Model.md
```

---

# Seguridad

Proposal no administra autenticación.

Proposal no almacena:

- contraseñas;
- tokens;
- JWT;
- claves privadas;
- secretos criptográficos;
- credenciales;
- sesiones.

La autorización para ejecutar Commands corresponde a las
capacidades de autorización del sistema y a las reglas de dominio
aplicables.

Proposal recibe una intención autorizada y protege sus propias
invariantes.

La seguridad específica del Aggregate se documentará en:

```text
DOMAIN-007O-Security-Model.md
```

---

# Permisos

Los permisos técnicos y de autorización no forman parte del
estado interno de Proposal.

La autorización debe determinar si un actor puede intentar
ejecutar una operación sobre Proposal.

Proposal, una vez invocado, valida las reglas propias del
dominio.

Debe mantenerse la separación entre:

```text
Authorization
```

y:

```text
Domain Invariants
```

La autorización determina quién puede intentar una operación.

El Aggregate determina si la operación es válida dentro de su
estado.

Las reglas conceptuales de permisos se documentarán en:

```text
DOMAIN-007F-Permissions.md
```

---

# Auditoría

Proposal produce hechos de dominio que pueden ser utilizados por
el contexto de Audit.

La auditoría no forma parte del Aggregate.

Proposal no mantiene una colección de registros de auditoría
externos como entidades internas.

La trazabilidad conceptual se basa en:

```text
ProposalId

Version

Domain Events

timestamps

actor references cuando correspondan

CorrelationId cuando corresponda

CausationId cuando corresponda
```

La información de auditoría no debe alterar las invariantes de
Proposal ni convertir Audit en una dependencia interna del
Aggregate.

---

# Integraciones

Proposal puede integrarse con:

- plataformas municipales;
- plataformas de participación ciudadana;
- sistemas de gestión comunitaria;
- sistemas territoriales;
- sistemas Smart City;
- sistemas documentales;
- sistemas de notificación;
- plataformas de gobierno abierto;
- sistemas de interoperabilidad.

Estas integraciones no forman parte del Aggregate.

Proposal no conoce:

- endpoints HTTP;
- proveedores externos;
- credenciales;
- OAuth;
- JWT;
- SDKs;
- protocolos específicos;
- bases de datos externas.

La integración se realiza mediante contratos y eventos.

---

# Dependencias

Proposal depende conceptualmente de:

- Shared Kernel;
- Value Objects;
- Domain Events;
- Repository Contracts;
- reglas de dominio;
- identificadores de otros Aggregates.

Proposal no depende de:

- Infrastructure;
- Frameworks;
- Bases de datos;
- HTTP;
- OAuth;
- JWT;
- React;
- FastAPI;
- Django;
- proveedores externos.

La dirección de dependencias siempre debe preservar la
independencia del dominio.

---

# Compatibilidad Arquitectónica

El Aggregate Proposal está diseñado conforme a:

- Domain-Driven Design;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- Event-Driven Architecture;
- CQRS;
- Event Sourcing Compatible;
- arquitectura distribuida;
- interoperabilidad basada en contratos.

El modelo de dominio permanece independiente de la tecnología de
implementación.

La compatibilidad con estos patrones no obliga a adoptar una
tecnología específica.

---

# Límites del Aggregate

El límite de consistencia de Proposal comprende exclusivamente
los conceptos necesarios para mantener:

- identidad;
- contexto organizacional;
- proponente;
- contexto territorial;
- contexto de Assembly;
- clasificación;
- título;
- propósito;
- descripción;
- contenido propio;
- presentación;
- estado;
- ciclo de vida;
- invariantes;
- versión.

No forman parte de este límite:

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

Estos conceptos pueden relacionarse con Proposal, pero conservan
sus propios límites de consistencia.

---

# Regla de No Absorción

Proposal no absorbe otros Aggregates debido a que estos
participen en el tratamiento de una iniciativa.

La coexistencia contextual no implica pertenencia estructural.

Por lo tanto:

```text
Proposal
    │
    ├── Assembly
    ├── Participation
    ├── Voting
    └── Document
```

no significa:

```text
Proposal
    └── Assembly
        └── Participation
            └── Voting
                └── Document
```

Cada Aggregate mantiene:

- identidad propia;
- ciclo de vida propio;
- invariantes propias;
- Repository propio;
- Domain Events propios;
- consistencia propia.

Esta separación evita convertir Proposal en un Aggregate
excesivamente grande y preserva los límites establecidos por el
modelo DDD de AURA.

---

# Separación entre Proposal y Assembly

Proposal y Assembly representan conceptos diferentes.

```text
Assembly
```

representa una instancia formal de reunión.

```text
Proposal
```

representa una iniciativa formal.

Una Proposal puede ser conocida o tratada dentro de una Assembly,
pero no forma parte estructural de ella.

Una Assembly puede finalizar mientras una Proposal continúa
existiendo.

Una Proposal puede existir antes de una Assembly.

Una Proposal puede relacionarse posteriormente con otra instancia
del dominio sin perder su identidad.

La relación entre ambas se mantiene mediante identificadores y
eventos.

---

# Separación entre Proposal y Participation

Proposal representa aquello sobre lo cual puede desarrollarse un
proceso participativo.

Participation representa el proceso de participación.

Conceptualmente:

```text
Proposal
    │
    ▼
Participation
```

no significa que Participation sea una entidad interna de
Proposal.

La Participation puede poseer:

- participantes;
- reglas;
- estado;
- período;
- resultados;
- eventos.

Estas responsabilidades pertenecen al Aggregate Participation.

---

# Separación entre Proposal y Voting

Proposal puede constituir una materia sometida a Voting.

Proposal no representa:

- padrón de votación;
- apertura de votación;
- emisión de votos;
- conteo;
- quorum;
- cierre;
- resultado electoral.

Estas responsabilidades pertenecen al Aggregate Voting.

Conceptualmente:

```text
Proposal
    │
    ▼
Voting
```

representa una relación entre Aggregates.

No representa composición interna.

El resultado de Voting puede producir posteriormente una
consecuencia sobre Proposal mediante coordinación explícita entre
los límites correspondientes.

---

# Separación entre Proposal y Document

Proposal mantiene información conceptual propia de la
iniciativa.

Document representa contenido documental con identidad y ciclo de
vida propios.

Una Proposal puede referenciar múltiples Documents.

Proposal no debe transformarse en un repositorio de archivos.

La relación conceptual es:

```text
Proposal
    │
    └──────── DocumentId
```

y no:

```text
Proposal
    └──────── Document Aggregate completo
```

---

# Separación entre Proposal y Notification

Los cambios de Proposal pueden requerir comunicación hacia
actores del ecosistema.

Proposal expresa el hecho.

Notification administra la comunicación.

Conceptualmente:

```text
ProposalSubmitted
        │
        ▼
Notification
```

Proposal no:

- selecciona canales técnicos;
- envía correos electrónicos;
- envía mensajes;
- administra reintentos;
- administra proveedores;
- mantiene credenciales de comunicación.

---

# Separación entre Estado y Resultado Externo

El estado de Proposal pertenece exclusivamente al Aggregate.

Un resultado proveniente de otro Aggregate no debe modificar
Proposal evitando sus comportamientos e invariantes.

Por ejemplo, un resultado de Voting no puede escribir
directamente:

```text
ProposalStatus = Accepted
```

La coordinación debe expresar una intención válida sobre
Proposal.

Proposal debe evaluar esa intención conforme a:

- estado actual;
- transición permitida;
- invariantes;
- versión;
- reglas del dominio.

De esta forma, Proposal conserva autoridad exclusiva sobre su
propio estado.

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

Proposal nunca obtiene una referencia mutable a otro Aggregate.

Proposal nunca modifica directamente:

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
```

La coordinación entre estos conceptos se produce fuera del
Aggregate cuando sea necesaria.

---

# Consistencia entre Aggregates

Proposal mantiene consistencia fuerte únicamente dentro de su
propio límite.

Cuando una operación requiera información perteneciente a otro
Aggregate, la coordinación debe preservar la autonomía de ambos
límites.

Conceptualmente:

```text
Proposal
    │
    │ Domain Event
    ▼
Application / Coordination
    │
    ▼
Other Aggregate
```

No se establece una única transacción de dominio que modifique
simultáneamente múltiples Aggregates.

La consistencia entre Aggregates es eventual cuando el flujo lo
requiera.

---

# Eliminación

Proposal no utiliza la eliminación física como mecanismo normal
para representar el final de su ciclo de vida.

Los estados:

```text
Rejected

Withdrawn

Archived
```

mantienen la identidad histórica de la iniciativa.

La conservación de la identidad permite mantener:

- trazabilidad;
- auditoría;
- relaciones históricas;
- referencias desde otros Aggregates;
- consistencia de eventos.

La política técnica de retención pertenece a las capas y
políticas correspondientes y no modifica esta regla conceptual.

---

# Casos de Uso Conceptuales

Proposal soporta conceptualmente casos de uso como:

```text
Crear una Proposal.

Definir su tipo.

Definir su título.

Definir su propósito.

Describir la iniciativa.

Actualizar su contenido.

Relacionarla con un Territory.

Relacionarla con una Assembly.

Presentar formalmente la Proposal.

Iniciar su revisión.

Aceptar la Proposal.

Rechazar la Proposal.

Retirar la Proposal.

Archivar la Proposal.
```

Cada caso de uso debe respetar las invariantes y transiciones
definidas por el Aggregate.

Los casos de uso no autorizan acceso directo al estado interno.

---

# Restricciones

No está permitido:

- modificar ProposalId;
- modificar OrganizationId;
- modificar Version directamente;
- modificar ProposalStatus directamente;
- modificar un Aggregate externo desde Proposal;
- presentar una Proposal desde un estado inválido;
- iniciar revisión desde un estado inválido;
- aceptar una Proposal desde un estado inválido;
- rechazar una Proposal desde un estado inválido;
- retirar una Proposal cuando el estado no lo permita;
- modificar una Proposal archivada;
- continuar normalmente una Proposal retirada;
- almacenar otros Aggregates completos dentro de Proposal;
- convertir Assembly en una entidad interna de Proposal;
- convertir Participation en una entidad interna de Proposal;
- convertir Voting en una entidad interna de Proposal;
- convertir Document en una entidad interna de Proposal;
- utilizar Infrastructure como dependencia del dominio;
- utilizar resultados externos para modificar directamente el
  estado del Aggregate;
- omitir la validación de invariantes ante una modificación.

---

# Extension Points

Proposal puede extenderse mediante conceptos que no alteren su
límite fundamental de consistencia.

Los puntos de extensión pueden incluir:

- nuevos tipos de Proposal;
- nuevas reglas de presentación;
- nuevas clasificaciones;
- nuevos estados únicamente cuando una evolución formal del
  modelo así lo establezca;
- nuevas políticas de evaluación;
- nuevos Domain Events;
- nuevos Integration Events;
- nuevas proyecciones;
- nuevas integraciones;
- nuevas políticas de dominio.

Las extensiones no deben convertir otros Aggregates en entidades
internas de Proposal.

Las extensiones tampoco deben introducir dependencias de
Infrastructure dentro del dominio.

La especificación correspondiente se documentará en:

```text
DOMAIN-007P-Extension-Points.md
```

---

# Documentación Complementaria

El Aggregate Proposal se descompone en los siguientes artefactos
conceptuales:

```text
DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007D-Domain-Events.md

DOMAIN-007E-Invariants.md

DOMAIN-007F-Permissions.md

DOMAIN-007G-Repository-Contract.md

DOMAIN-007H-Examples.md

DOMAIN-007I-Versioning.md

DOMAIN-007J-Consistency-Boundary.md

DOMAIN-007K-Integration-Events.md

DOMAIN-007L-Read-Model.md

DOMAIN-007M-Test-Scenarios.md

DOMAIN-007N-Performance-Rules.md

DOMAIN-007O-Security-Model.md

DOMAIN-007P-Extension-Points.md
```

Estos documentos desarrollan aspectos específicos del Aggregate
sin reemplazar la definición conceptual establecida en
DOMAIN-007-Aggregate.md.

DOMAIN-007-Aggregate.md constituye la fuente conceptual oficial
del Aggregate Proposal.

Las definiciones, reglas, relaciones, límites, invariantes,
responsabilidades, restricciones y conceptos establecidos en
este documento deben ser respetados por los documentos
complementarios.

Los documentos posteriores profundizan este modelo.

No deben redefinirlo de manera incompatible.

---

# Principios de Diseño

Proposal cumple los siguientes principios:

- una única Aggregate Root;
- identidad propia;
- límite de consistencia explícito;
- invariantes protegidas por el Aggregate;
- referencias externas mediante identificadores;
- ausencia de dependencias tecnológicas;
- comportamiento de dominio explícito;
- consistencia interna fuerte;
- consistencia eventual entre Aggregates;
- separación entre Commands y Domain Events;
- separación entre Domain Events e Integration Events;
- separación entre dominio y autorización;
- separación entre dominio e infraestructura;
- separación entre Proposal y Assembly;
- separación entre Proposal y Participation;
- separación entre Proposal y Voting;
- separación entre Proposal y Document;
- alta cohesión;
- bajo acoplamiento;
- evolución controlada.

---

# Objetivos de Diseño

El Aggregate Proposal busca garantizar:

- identidad única de cada iniciativa;
- representación formal de propuestas;
- consistencia de su ciclo de vida;
- protección de sus invariantes;
- independencia respecto de los procesos participativos;
- independencia respecto de los procesos de votación;
- independencia respecto de Assembly;
- independencia respecto de Infrastructure;
- trazabilidad;
- interoperabilidad;
- evolución controlada;
- capacidad de integración con procesos municipales y
  comunitarios;
- compatibilidad con una arquitectura distribuida.

---

# Definición de Éxito

El Aggregate **Proposal** representa de forma oficial y
consistente una iniciativa formal dentro del ecosistema AURA.

Proposal establece la identidad, contexto organizacional,
proponente, contexto territorial, contexto de Assembly,
clasificación, título, propósito, contenido, presentación y ciclo
de vida de una iniciativa, protegiendo sus invariantes y
manteniendo un límite de consistencia claramente definido.

El Aggregate permite que los procesos de Assembly,
Participation, Voting, Document, Notification y Audit se
relacionen con una Proposal sin absorber sus respectivas
responsabilidades.

Proposal conserva autoridad exclusiva sobre su propio estado.

Ningún proceso externo puede modificar directamente el estado
interno del Aggregate sin atravesar sus comportamientos,
transiciones e invariantes.

De esta forma, Proposal constituye el punto de referencia formal
para las iniciativas ciudadanas, organizacionales, comunitarias
y territoriales de AURA, manteniendo independencia tecnológica,
trazabilidad, interoperabilidad, alta cohesión, bajo acoplamiento
y capacidad de evolución dentro de una arquitectura DDD
distribuida.