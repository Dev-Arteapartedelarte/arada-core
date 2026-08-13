# DOMAIN-009 — Voting Aggregate

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
- DOMAIN-006-Aggregate.md
- DOMAIN-007-Aggregate.md
- DOMAIN-008-Aggregate.md

---

# Objetivo

El Aggregate **Voting** representa un proceso formal de
votación dentro del ecosistema AURA.

Constituye la unidad de dominio responsable de representar
la existencia, configuración, apertura, desarrollo,
finalización y conservación histórica de un proceso de
votación.

Voting permite que una Organization disponga de procesos
formales mediante los cuales una materia, decisión o
alternativa pueda ser sometida a votación conforme a reglas
previamente establecidas.

Un Voting puede desarrollarse dentro del contexto de una
Assembly y puede relacionarse con una Proposal cuando la
votación corresponda a una materia representada por dicho
Aggregate.

Voting mantiene su propia:

- identidad;
- ciclo de vida;
- estado;
- reglas;
- opciones cuando correspondan;
- resultado formal;
- invariantes;
- versión;
- trazabilidad.

Voting no reemplaza ni absorbe otros Aggregates del dominio.

La participación individual de Citizens permanece separada
del proceso formal de Voting y corresponde al modelo de
Participation definido por AURA.

---

# Propósito

El propósito del Aggregate Voting es proporcionar una
representación consistente de un proceso formal de votación.

Voting permite establecer:

- identidad del proceso de votación;
- Organization propietaria;
- contexto de Assembly cuando corresponda;
- Proposal asociada cuando corresponda;
- naturaleza del proceso de votación;
- título;
- descripción;
- estado;
- reglas aplicables;
- opciones disponibles cuando correspondan;
- condiciones necesarias para abrir la votación;
- condiciones necesarias para cerrar la votación;
- resultado formal;
- trazabilidad de modificaciones;
- publicación de hechos relevantes del dominio.

Voting constituye el límite de consistencia del proceso
formal de votación.

No constituye el límite de consistencia de:

- la Organization;
- la Assembly;
- la Proposal;
- la Membership;
- el Citizen;
- la Participation individual;
- los Documents;
- las Notifications;
- el Audit;
- las Integrations.

---

# Definición

Voting representa el proceso formal mediante el cual una
Organization habilita una instancia de votación bajo reglas
determinadas.

El proceso posee identidad propia y existe
independientemente de:

- la Assembly que pueda proporcionar su contexto;
- la Proposal que pueda constituir su materia;
- las Participations individuales asociadas al proceso;
- los Documents relacionados;
- las Notifications generadas;
- los procesos de Audit;
- las Integrations externas.

Conceptualmente:

```text
Organization

      │

      │ OrganizationId

      ▼

    Voting
```

Cuando Voting se desarrolla dentro de una Assembly:

```text
Assembly

    │

    │ AssemblyId

    ▼

  Voting
```

Cuando Voting se encuentra relacionado con una Proposal:

```text
Proposal

    │

    │ ProposalId

    ▼

  Voting
```

Estos vínculos representan relaciones entre Aggregates.

No representan composición de Aggregates.

---

# Alcance del Aggregate

Voting representa exclusivamente el proceso formal de
votación.

Dentro de su alcance se encuentran:

- identidad del Voting;
- propiedad organizacional;
- contexto formal;
- tipo de Voting;
- reglas propias del proceso;
- opciones cuando correspondan;
- estado;
- apertura;
- cierre;
- cancelación;
- archivado;
- resultado formal;
- versión;
- hechos relevantes producidos por el proceso.

Fuera de su alcance permanecen:

- identidad cívica;
- pertenencia organizacional;
- Roles;
- estructura territorial;
- Lifecycle de Assembly;
- Lifecycle de Proposal;
- Lifecycle de Participation;
- gestión documental;
- entrega de Notifications;
- Audit;
- Integrations externas.

---

# Responsabilidades

El Aggregate Voting es responsable de:

- mantener VotingId;
- mantener OrganizationId;
- mantener AssemblyId cuando corresponda;
- mantener ProposalId cuando corresponda;
- mantener VotingType;
- mantener su información descriptiva;
- administrar su ciclo de vida;
- controlar VotingStatus;
- mantener las reglas propias de la votación;
- mantener las opciones cuando formen parte del proceso;
- controlar cuándo puede abrirse;
- controlar cuándo puede cerrarse;
- controlar cuándo puede cancelarse;
- controlar cuándo puede archivarse;
- preservar el resultado formal cuando corresponda;
- proteger sus invariantes;
- incrementar Version ante modificaciones válidas;
- mantener trazabilidad;
- generar Domain Events;
- preservar su límite de consistencia.

Voting representa el proceso de votación como una unidad
formal del dominio.

---

# Responsabilidades Fuera del Aggregate

No es responsabilidad de Voting:

- administrar Organizations;
- administrar Citizens;
- crear Memberships;
- modificar Memberships;
- definir Roles;
- administrar Territories;
- crear Assemblies;
- modificar Assemblies;
- administrar el Lifecycle de Assembly;
- crear Proposals;
- modificar Proposals;
- administrar el Lifecycle de Proposal;
- administrar el Lifecycle de Participation;
- administrar la identidad individual del participante;
- autenticar usuarios;
- administrar credenciales;
- administrar sesiones;
- almacenar Documents completos;
- enviar Notifications;
- ejecutar Audit;
- administrar Integrations externas.

Estas responsabilidades permanecen bajo sus respectivos
Aggregates o Bounded Contexts.

Voting nunca modifica directamente el estado interno de
otro Aggregate.

---

# Separación entre Voting y Participation

Voting y Participation representan conceptos diferentes
del dominio.

Voting representa:

```text
Formal Voting Process
```

Participation representa:

```text
Individual Participation in a Domain Process
```

Por lo tanto:

```text
Voting

≠

Participation
```

Voting administra el proceso formal.

Participation mantiene la participación individual bajo
su propio:

- Aggregate Root;
- identidad;
- Lifecycle;
- Invariants;
- Version;
- Consistency Boundary.

Voting no absorbe Participation como entidad interna.

Participation tampoco reemplaza al proceso formal de
Voting.

---

# Separación entre Voting y Assembly

Assembly representa una instancia formal de reunión.

Voting representa un proceso formal de votación.

Debe mantenerse:

```text
Assembly

≠

Voting
```

Una Assembly puede proporcionar contexto para uno o más
procesos de Voting.

La existencia de Voting dentro del contexto de una
Assembly no convierte Voting en una entidad interna de
Assembly.

Voting conserva:

- VotingId;
- Lifecycle;
- VotingStatus;
- Invariants;
- Version;
- Repository;
- Domain Events.

---

# Separación entre Voting y Proposal

Proposal representa una propuesta con identidad y
Lifecycle propios.

Voting puede utilizar:

```text
ProposalId
```

cuando una Proposal constituya la materia relacionada con
el proceso de votación.

Debe mantenerse:

```text
Proposal

≠

Voting
```

Voting no modifica:

- ProposalStatus;
- ProposalContent;
- ProposalVersion;
- Proposal Lifecycle.

Proposal tampoco administra el Lifecycle de Voting.

---

# Aggregate Root

La única Aggregate Root es:

```text
Voting
```

Toda modificación sobre un Voting debe realizarse
exclusivamente mediante esta Aggregate Root.

Ningún componente externo puede modificar directamente el
estado interno del Aggregate.

La Aggregate Root controla:

- identidad;
- contexto organizacional;
- contexto de Assembly;
- referencia a Proposal;
- VotingType;
- VotingStatus;
- reglas;
- opciones;
- condiciones de apertura;
- condiciones de cierre;
- resultado;
- transiciones de estado;
- invariantes;
- Version;
- generación de Domain Events.

---

# Identidad

La identidad del Aggregate está determinada por:

```text
VotingId
```

VotingId:

- es único;
- es inmutable;
- nunca cambia;
- nunca se reutiliza;
- no depende del mecanismo de persistencia;
- permanece durante todo el Lifecycle.

Conceptualmente:

```text
VotingId = VOT-001
```

continúa identificando el mismo Voting independientemente
de cambios en:

- Status;
- VotingType;
- Title;
- Description;
- Rules;
- Options;
- Result;
- Version.

---

# Propietario Organizacional

Todo Voting pertenece a una Organization.

La relación se representa mediante:

```text
OrganizationId
```

OrganizationId:

- es obligatorio;
- identifica la Organization propietaria;
- es inmutable durante toda la vida del Aggregate;
- no incorpora Organization dentro de Voting;
- no permite modificar Organization desde Voting.

Conceptualmente:

```text
Organization

      │

      │ OrganizationId

      ▼

    Voting
```

Una Organization puede disponer de múltiples procesos de
Voting.

Cada Voting pertenece a una única Organization.

---

# Contexto de Assembly

Voting puede desarrollarse dentro del contexto de una
Assembly.

La relación se mantiene mediante:

```text
AssemblyId
```

AssemblyId:

- identifica la Assembly relacionada;
- permanece como referencia de identidad;
- no incorpora Assembly dentro de Voting;
- no permite modificar Assembly desde Voting.

Voting no administra:

- convocatoria de Assembly;
- apertura de Assembly;
- cierre de Assembly;
- cancelación de Assembly;
- reglas internas de Assembly.

La obligatoriedad de AssemblyId depende del contexto del
Voting y de las reglas de dominio correspondientes.

---

# Contexto de Proposal

Voting puede relacionarse con una Proposal mediante:

```text
ProposalId
```

cuando la votación se refiera a una Proposal formal del
dominio.

ProposalId:

- identifica la Proposal relacionada;
- no incorpora Proposal dentro de Voting;
- no permite modificar Proposal desde Voting;
- no transfiere el Lifecycle de Proposal al Aggregate
  Voting.

La obligatoriedad de ProposalId depende del contexto y de
la naturaleza del Voting.

---

# Atributos Conceptuales

Voting mantiene conceptualmente información equivalente a:

```text
VotingId

OrganizationId

AssemblyId

ProposalId

VotingType

Title

Description

Status

Rules

Options

Result

OpenedAt

ClosedAt

CancelledAt

ArchivedAt

Version

CreatedAt

UpdatedAt
```

Los nombres y tipos concretos de implementación deben
respetar los contratos definidos por el modelo de dominio.

Esta representación no constituye autorización para
exponer setters públicos.

---

# Descripción de Atributos

## VotingId

Identificador único del Voting.

Es inmutable durante toda la vida del Aggregate.

---

## OrganizationId

Identificador de la Organization propietaria.

Es obligatorio e inmutable.

---

## AssemblyId

Identificador de la Assembly que proporciona contexto al
Voting cuando corresponda.

No convierte Assembly en parte interna del Aggregate.

---

## ProposalId

Identificador de la Proposal relacionada cuando
corresponda.

No convierte Proposal en parte interna del Aggregate.

---

## VotingType

Representa la naturaleza del proceso de votación.

VotingType pertenece al lenguaje ubicuo de Voting
Management.

El conjunto formal de valores válidos debe mantenerse
definido por el dominio.

VotingType puede condicionar:

- reglas aplicables;
- estructura de opciones;
- condiciones de apertura;
- condiciones de cierre;
- interpretación del resultado.

VotingType no modifica la identidad del Aggregate.

---

## Title

Nombre descriptivo del proceso de votación.

Permite identificar la materia o proceso de forma
comprensible dentro de su contexto.

Title:

- no constituye VotingId;
- debe respetar las reglas del dominio;
- puede modificarse únicamente mientras las reglas del
  Lifecycle lo permitan.

---

## Description

Descripción funcional del proceso de votación.

Permite proporcionar contexto adicional sin modificar la
identidad del Aggregate.

---

## Status

Representa el estado actual de Voting.

Conceptualmente se consideran los estados:

```text
Draft

Open

Closed

Cancelled

Archived
```

Las transiciones exactas entre estos estados se definen
formalmente en:

```text
DOMAIN-009A-Lifecycle.md

DOMAIN-009B-State-Machine.md
```

No deben inferirse transiciones adicionales desde la sola
existencia de los estados.

---

## Rules

Representa las reglas formales aplicables al proceso de
Voting.

Las Rules pertenecen al dominio de Voting.

Pueden expresar las condiciones necesarias para:

- configurar el proceso;
- determinar cuándo puede abrirse;
- determinar qué estructura de opciones es válida;
- determinar las condiciones aplicables durante la
  votación;
- determinar cuándo puede cerrarse;
- determinar cómo debe interpretarse el resultado.

Rules no debe utilizarse para almacenar:

- credenciales;
- configuración de Infrastructure;
- configuración HTTP;
- tokens;
- configuración de UI;
- mecanismos técnicos de autenticación.

---

## Options

Representa las alternativas formales disponibles cuando
la naturaleza del Voting requiera opciones explícitas.

Las Options pertenecen al proceso de Voting.

Su estructura debe respetar:

- VotingType;
- Rules;
- Lifecycle;
- Invariants.

Una Option no constituye un Aggregate independiente por el
solo hecho de formar parte de Voting.

Las reglas detalladas sobre modificación de Options se
formalizan en los documentos especializados del
Aggregate.

---

## Result

Representa el resultado formal consolidado de Voting
cuando el proceso ha alcanzado las condiciones requeridas
para producirlo.

Result:

- pertenece al Aggregate Voting;
- no sustituye las Participations individuales;
- no convierte Participation en entidad interna;
- debe corresponder a las Rules vigentes;
- solo puede existir en condiciones válidas del Lifecycle.

La estructura detallada del resultado debe permanecer
coherente con las reglas formales del Aggregate.

---

## OpenedAt

Fecha y hora efectiva en que Voting fue abierto.

Debe existir únicamente cuando el proceso haya alcanzado
la apertura conforme a su Lifecycle.

---

## ClosedAt

Fecha y hora efectiva en que Voting fue cerrado.

Debe existir únicamente cuando el proceso haya sido
cerrado válidamente.

Cuando existan ambos:

```text
OpenedAt

ClosedAt
```

debe preservarse coherencia temporal.

---

## CancelledAt

Fecha y hora en que Voting fue cancelado.

Solo puede establecerse mediante una transición válida de
cancelación.

---

## ArchivedAt

Fecha y hora en que Voting fue archivado.

Archive representa conservación histórica y no eliminación
física.

---

## Version

Número de versión utilizado para control de concurrencia
optimista.

Toda modificación válida incrementa Version.

Las reglas completas se definen en:

```text
DOMAIN-009I-Versioning.md
```

---

## CreatedAt

Fecha y hora de creación de Voting.

Permanece inmutable durante toda la vida del Aggregate.

---

## UpdatedAt

Fecha y hora de la última modificación válida.

Solo cambia como consecuencia de comportamiento aceptado
por la Aggregate Root.

---

# Value Objects

Los conceptos internos de Voting pueden representarse
mediante Value Objects cuando corresponda.

Conceptualmente pueden considerarse:

```text
VotingType

VotingStatus

VotingTitle

VotingDescription

VotingRules

VotingOption

VotingResult
```

Los Value Objects:

- son inmutables;
- no poseen identidad independiente;
- pertenecen al lenguaje ubicuo;
- no exponen comportamiento de Infrastructure;
- deben ser válidos desde su creación;
- no pueden modificar directamente Aggregates externos.

La decisión concreta sobre su representación de código
pertenece al modelo de implementación del dominio y debe
respetar la arquitectura consolidada.

---

# Entidades Internas

Voting puede contener únicamente entidades internas que
sean necesarias para representar conceptos pertenecientes
realmente al proceso de votación.

Una entidad interna:

- pertenece exclusivamente a Voting;
- no posee Lifecycle independiente fuera del Aggregate;
- no posee Repository independiente;
- no puede modificarse desde otro Aggregate;
- se encuentra protegida por la Aggregate Root;
- comparte el Consistency Boundary de Voting.

La existencia de un concepto dentro del proceso no debe
utilizarse automáticamente para crear un nuevo Aggregate.

La incorporación de nuevas entidades internas requiere
respetar las reglas de diseño de AURA.

---

# Estado

VotingStatus representa el estado operativo del proceso.

Estados conceptuales:

```text
Draft

Open

Closed

Cancelled

Archived
```

---

## Draft

Voting existe como definición formal inicial.

En este estado puede mantenerse la configuración necesaria
para que el proceso pueda ser abierto posteriormente.

El hecho de existir en Draft no significa que la votación
se encuentre disponible para participar.

---

## Open

Voting se encuentra formalmente abierto.

La apertura representa el inicio efectivo del proceso de
votación.

Las reglas aplicables durante Open permanecen protegidas
por las Invariants del Aggregate.

---

## Closed

Voting ha finalizado formalmente.

Closed representa el cierre válido del proceso.

El Voting conserva:

- identidad;
- reglas históricas;
- contexto;
- información temporal;
- resultado cuando corresponda;
- Version.

---

## Cancelled

Voting fue cancelado conforme a una transición permitida
por el dominio.

Cancelar no significa eliminar.

Voting conserva su identidad y su historial.

Las condiciones y estados desde los cuales puede
cancelarse se definen formalmente en:

```text
DOMAIN-009A-Lifecycle.md

DOMAIN-009B-State-Machine.md
```

---

## Archived

Voting ha sido retirado del ciclo operativo y se conserva
como referencia histórica.

Una instancia Archived:

- conserva VotingId;
- conserva OrganizationId;
- conserva su historial;
- conserva su resultado cuando exista;
- conserva Version;
- no se modifica mediante operaciones ordinarias.

Archivar no equivale a eliminar físicamente el Aggregate.

---

# Ciclo de Vida

El Lifecycle de Voting distingue la configuración del
proceso, su ejecución y su conservación histórica.

Conceptualmente comprende:

```text
Draft

Open

Closed

Cancelled

Archived
```

El flujo operativo principal considera:

```text
Draft

  │

  ▼

Open

  │

  ▼

Closed

  │

  ▼

Archived
```

Cancelled representa una terminación alternativa cuando
las reglas del dominio permitan cancelar el proceso.

Las rutas exactas hacia Cancelled y todas las
precondiciones de transición no deben inferirse desde este
documento.

Se encuentran formalmente definidas en:

```text
DOMAIN-009A-Lifecycle.md

DOMAIN-009B-State-Machine.md
```

---

# Configuración

Mientras Voting se encuentre en el estado que permita su
configuración, la Aggregate Root controla los cambios
permitidos sobre:

- VotingType;
- Title;
- Description;
- Rules;
- Options;
- contexto permitido.

La existencia de una operación de configuración no implica
que pueda ejecutarse desde cualquier estado.

Las restricciones correspondientes pertenecen a:

```text
DOMAIN-009B-State-Machine.md

DOMAIN-009E-Invariants.md
```

---

# Apertura

Abrir Voting representa iniciar formalmente el proceso de
votación.

La apertura debe producirse únicamente cuando el Aggregate
cumpla las condiciones requeridas.

Conceptualmente:

```text
Voting

Status = Draft

↓

OpenVoting

↓

Validate State

Validate Rules

Validate Invariants

↓

Status = Open
```

Una apertura válida:

- cambia VotingStatus;
- establece OpenedAt;
- incrementa Version;
- genera VotingOpened.

La apertura no modifica otros Aggregates.

---

# Voting Abierto

Cuando Voting se encuentra Open, el proceso formal de
votación se encuentra activo.

El Aggregate debe preservar las reglas que determinan la
validez del proceso.

Las configuraciones cuya modificación pudiera alterar el
significado de una votación ya abierta deben quedar
protegidas por las Invariants correspondientes.

La participación individual permanece bajo el Aggregate
Participation.

Voting no incorpora Citizens completos dentro de su
estado.

---

# Cierre

Cerrar Voting representa finalizar formalmente el proceso.

Conceptualmente:

```text
Voting

Status = Open

↓

CloseVoting

↓

Validate State

Validate Rules

Validate Invariants

↓

Status = Closed
```

Un cierre válido:

- cambia VotingStatus;
- establece ClosedAt;
- preserva el resultado formal cuando corresponda;
- incrementa Version;
- genera VotingClosed.

El cierre no modifica directamente:

- Assembly;
- Proposal;
- Participation;
- Organization;
- Document;
- Audit.

---

# Resultado

El resultado pertenece al proceso formal de Voting.

Debe mantenerse coherencia entre:

```text
Rules

Options

VotingStatus

Result
```

Result no debe existir como sustituto de las participaciones
individuales.

Conceptualmente:

```text
Participation

↓

Individual Domain Participation
```

mientras:

```text
Voting

↓

Formal Voting Result
```

Ambos conceptos permanecen separados.

El resultado no autoriza a Voting a modificar directamente
el estado de Proposal, Assembly u otro Aggregate.

Los procesos posteriores derivados del resultado deben
respetar los límites de cada Aggregate.

---

# Cancelación

CancelVoting representa la decisión formal de cancelar un
proceso cuando las reglas del dominio lo permitan.

Cancelar:

```text
Voting
```

no significa:

```text
Delete Voting
```

Una cancelación válida:

- conserva VotingId;
- conserva OrganizationId;
- establece CancelledAt;
- incrementa Version;
- genera VotingCancelled;
- preserva la trazabilidad del proceso.

Las precondiciones exactas se desarrollan en:

```text
DOMAIN-009A-Lifecycle.md

DOMAIN-009B-State-Machine.md

DOMAIN-009E-Invariants.md
```

---

# Archivado

ArchiveVoting retira Voting del ciclo operativo y lo
mantiene como registro histórico del dominio.

Una instancia Archived:

- conserva identidad;
- conserva referencias;
- conserva reglas históricas;
- conserva resultado cuando exista;
- conserva timestamps;
- conserva Version;
- puede continuar siendo consultada mediante Read Models.

Archive no constituye eliminación física.

---

# Reglas de Estado

El Aggregate debe garantizar como mínimo:

- todo Voting posee un estado válido;
- un Voting nuevo comienza conforme al estado inicial
  definido por el Lifecycle;
- un Voting solo puede abrirse mediante una transición
  válida;
- un Voting solo puede cerrarse mediante una transición
  válida;
- un Voting cancelado no continúa normalmente sin una
  transición explícitamente definida;
- un Voting Closed no vuelve arbitrariamente a Open;
- un Voting Archived no admite modificaciones ordinarias;
- las modificaciones de Rules deben respetar el estado;
- las modificaciones de Options deben respetar el estado;
- Result debe corresponder a una condición válida del
  proceso;
- toda transición debe respetar las Invariants;
- toda modificación válida incrementa Version.

Las reglas exhaustivas se definen en:

```text
DOMAIN-009E-Invariants.md
```

---

# Invariantes

Voting mantiene como mínimo las siguientes Invariants:

- VotingId siempre existe;
- VotingId nunca cambia;
- VotingId nunca se reutiliza;
- OrganizationId siempre existe;
- OrganizationId nunca cambia;
- VotingType siempre debe ser válido;
- VotingStatus siempre debe ser válido;
- Title debe cumplir las reglas del dominio;
- Rules deben permanecer válidas;
- Options deben ser coherentes con VotingType y Rules
  cuando correspondan;
- Voting no puede abrirse si su configuración requerida es
  inválida;
- OpenedAt solo puede establecerse mediante una apertura
  válida;
- ClosedAt solo puede establecerse mediante un cierre
  válido;
- ClosedAt no puede preceder a OpenedAt;
- CancelledAt solo puede establecerse mediante una
  cancelación válida;
- ArchivedAt solo puede establecerse mediante un archivado
  válido;
- una instancia Archived no puede modificarse mediante
  Commands ordinarios;
- Result solamente puede representar un resultado válido
  del proceso;
- toda transición debe pertenecer a la State Machine;
- toda modificación válida incrementa Version;
- ninguna operación puede modificar directamente otro
  Aggregate;
- las Invariants deben ser verdaderas antes y después de
  toda operación válida.

Las reglas completas se desarrollan en:

```text
DOMAIN-009E-Invariants.md
```

---

# Relaciones

Voting mantiene relaciones con otros Aggregates mediante
identificadores.

Conceptualmente:

```text
Voting
   │
   ├──────── OrganizationId
   │
   ├──────── AssemblyId
   │
   ├──────── ProposalId
   │
   ├──────── DocumentId
   │
   └──────── AuditId
```

Las referencias utilizadas por procesos externos pueden
relacionar además Participation con Voting mediante:

```text
VotingId
```

Voting no necesita absorber Participation para expresar
esta relación.

Las relaciones no implican composición de Aggregates.

---

# Organization y Voting

Una Organization puede poseer múltiples procesos de
Voting.

Conceptualmente:

```text
Organization
      │
      │ 1
      │
      ├────────── N
      │
    Voting
```

Cada Voting pertenece a una única Organization.

La relación se mantiene mediante:

```text
OrganizationId
```

Voting no administra Organization.

---

# Assembly y Voting

Una Assembly puede proporcionar contexto para uno o más
procesos de Voting.

La relación se expresa mediante:

```text
AssemblyId
```

Conceptualmente:

```text
Assembly

   │

   └──────── Voting
```

Assembly conserva su propio Lifecycle.

Voting conserva su propio Lifecycle.

La existencia de una relación no fusiona ambos
Consistency Boundaries.

---

# Proposal y Voting

Una Proposal puede constituir la materia asociada a un
Voting.

La relación se mantiene mediante:

```text
ProposalId
```

Voting no administra Proposal.

Proposal no se convierte en entidad interna.

Una modificación sobre Voting no modifica automáticamente
Proposal.

---

# Participation y Voting

Participation representa la participación individual de un
actor dentro de un proceso reconocido por AURA.

Cuando una Participation corresponda a un Voting, la
relación puede expresarse desde el contexto correspondiente
mediante:

```text
VotingId
```

Debe mantenerse:

```text
Voting

=

Formal Process
```

y:

```text
Participation

=

Individual Participation
```

Voting no administra el Lifecycle de Participation.

Participation no administra el Lifecycle de Voting.

---

# Citizen y Voting

Citizen representa identidad cívica.

Voting no administra Citizens.

El proceso de Voting no debe incorporar:

```text
Citizen[]
```

como sustituto del Aggregate Citizen o del modelo de
Participation.

Cuando sea necesario determinar la participación de un
Citizen, la colaboración debe respetar los Aggregates y
contratos correspondientes.

---

# Membership y Voting

Membership representa la pertenencia de un Citizen a una
Organization.

Voting no:

- crea Memberships;
- activa Memberships;
- suspende Memberships;
- termina Memberships.

Cuando las reglas del proceso requieran condiciones de
pertenencia, estas deben evaluarse mediante los contratos y
políticas definidos por AURA sin incorporar Membership
dentro del Aggregate.

---

# Role y Voting

Role representa una función organizacional.

Voting no administra Roles.

Cuando las reglas de autorización o elegibilidad utilicen
Roles, la evaluación correspondiente permanece separada
del estado interno del Aggregate.

Voting no modifica Role.

---

# Territory y Voting

Territory conserva su propio Aggregate Root y su propio
Consistency Boundary.

Voting no administra:

- geometría;
- jerarquía territorial;
- límites territoriales;
- estado territorial.

Cuando el contexto de una votación dependa de una
Organization, Assembly, Proposal o Participation con
dimensión territorial, dicha relación no autoriza a Voting
a absorber Territory.

---

# Document y Voting

Documents pueden asociarse a Voting para representar
información formal relacionada con el proceso.

Voting no almacena ni administra el contenido completo de
Document.

La relación, cuando corresponda, se mantiene mediante:

```text
DocumentId
```

Document conserva:

- identidad;
- Lifecycle;
- Version;
- Repository;
- Invariants.

---

# Notification y Voting

Los hechos producidos por Voting pueden originar procesos
de Notification.

Voting no envía Notifications directamente.

Debe mantenerse:

```text
Voting Domain Event

↓

Notification Process
```

La entrega efectiva pertenece al Bounded Context
responsable de Notification.

---

# Audit y Voting

Los cambios relevantes de Voting pueden proporcionar
información al contexto de Audit.

Voting no administra el Aggregate Audit.

La trazabilidad puede apoyarse en:

- VotingId;
- Version;
- Domain Events;
- timestamps;
- identificadores de correlación cuando correspondan.

Audit permanece fuera del Consistency Boundary.

---

# Integration y Voting

Voting puede originar hechos relevantes para Integration.

Voting no ejecuta directamente integraciones externas.

Las comunicaciones hacia sistemas externos se realizan
mediante:

- Domain Events;
- Integration Events;
- contratos definidos por AURA.

Integration conserva su propio Aggregate y
responsabilidades.

---

# Consistencia

Voting constituye un límite de consistencia independiente.

Todas las modificaciones internas deben respetar:

- una única Aggregate Root;
- un estado válido;
- una transición válida;
- Invariants válidas;
- Version coherente;
- generación coherente de Domain Events.

No deben existir actualizaciones parciales que dejen el
Aggregate en un estado inválido.

Dentro de Voting:

```text
Consistency

=

Immediate
```

Entre Voting y otros Aggregates:

```text
Consistency

=

Eventual
```

cuando corresponda coordinación posterior.

---

# Límite de Consistencia

El Consistency Boundary comprende:

```text
Voting
   │
   ├── Internal State
   │
   ├── Internal Entities
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

Assembly

Proposal

Participation

Document

Notification

Audit

Integration
```

Estos conceptos permanecen bajo límites independientes.

La definición formal se desarrolla en:

```text
DOMAIN-009J-Consistency-Boundary.md
```

---

# Regla de No Absorción

Voting no puede absorber otro Aggregate para simplificar
una operación.

No debe existir:

```text
Voting
   │
   ├── Organization Aggregate
   ├── Assembly Aggregate
   ├── Proposal Aggregate
   └── Participation Aggregate
```

Debe mantenerse:

```text
Voting
   │
   ├── OrganizationId
   ├── AssemblyId
   └── ProposalId
```

y las referencias necesarias definidas por los contratos
del dominio.

Los Aggregates externos permanecen independientes.

---

# Commands

Voting responde a Commands que representan intenciones de
cambio.

Conceptualmente:

```text
CreateVoting

OpenVoting

CloseVoting

CancelVoting

ArchiveVoting

ChangeVotingType

ChangeVotingTitle

ChangeVotingDescription

ChangeVotingRules

AddVotingOption

RemoveVotingOption
```

Cada Command:

- expresa una intención;
- se dirige al Aggregate;
- debe respetar Permissions;
- debe respetar VotingStatus;
- debe respetar Invariants;
- no constituye un hecho consumado;
- puede producir uno o más Domain Events cuando la
  operación es válida.

La definición completa se encuentra en:

```text
DOMAIN-009C-Commands.md
```

---

# Operaciones Públicas

La Aggregate Root expone comportamiento explícito de
dominio.

Conceptualmente:

```text
create()

open()

close()

cancel()

archive()

changeType()

changeTitle()

changeDescription()

changeRules()

addOption()

removeOption()
```

No se exponen setters públicos.

No debe permitirse modificar directamente:

```text
votingId

organizationId

status

version

openedAt

closedAt

cancelledAt

archivedAt

result
```

Estos valores son controlados mediante comportamiento del
Aggregate.

---

# Eventos del Dominio

Voting genera Domain Events cuando ocurre un hecho
relevante y válido.

Conceptualmente:

```text
VotingCreated

VotingOpened

VotingClosed

VotingCancelled

VotingArchived

VotingTypeChanged

VotingTitleChanged

VotingDescriptionChanged

VotingRulesChanged

VotingOptionAdded

VotingOptionRemoved
```

Los eventos representan hechos ya ocurridos.

No representan Commands.

Debe mantenerse:

```text
OpenVoting

↓

VotingOpened
```

y no:

```text
VotingOpened

↓

Request to Open
```

La especificación completa se encuentra en:

```text
DOMAIN-009D-Domain-Events.md
```

---

# Reglas de Modificación

Toda modificación debe cumplir:

- debe realizarse mediante la Aggregate Root;
- VotingId nunca se modifica;
- OrganizationId nunca se modifica;
- ninguna modificación puede violar la State Machine;
- ninguna modificación puede violar las Invariants;
- ninguna modificación puede dejar el Aggregate en estado
  parcial;
- toda modificación válida incrementa Version;
- toda modificación relevante produce los Domain Events
  correspondientes;
- ninguna modificación puede alterar directamente otro
  Aggregate.

Las reglas completas se desarrollan en:

```text
DOMAIN-009E-Invariants.md
```

---

# Fuente de Verdad

La fuente de verdad del proceso es:

```text
Voting Aggregate
```

y, cuando corresponda a la estrategia de persistencia,
su historial de:

```text
Domain Events
```

Los Read Models:

- son derivados;
- pueden reconstruirse;
- no constituyen fuente de verdad;
- no pueden modificar Voting.

---

# Persistencia

El Repository persiste Voting como una unidad de
consistencia.

Conceptualmente:

```text
Voting
   │
   ├── State
   ├── Rules
   ├── Options
   ├── Result
   ├── Value Objects
   └── Version
```

No deben persistirse partes del Aggregate mediante
operaciones independientes que permitan evitar sus
Invariants.

El contrato formal se define en:

```text
DOMAIN-009G-Repository-Contract.md
```

---

# Versionado

Voting utiliza el modelo de Versioning consolidado por
AURA.

Toda modificación válida incrementa:

```text
Version
```

Conceptualmente:

```text
Version N

↓

Valid Modification

↓

Version N + 1
```

El Repository debe detectar modificaciones concurrentes
incompatibles.

Ante una versión obsoleta debe producirse el
comportamiento de concurrencia definido por el contrato
correspondiente.

La especificación completa se encuentra en:

```text
DOMAIN-009I-Versioning.md
```

---

# Seguridad

Voting no administra autenticación.

Voting no almacena:

- passwords;
- tokens;
- sesiones;
- claves privadas;
- secretos;
- credenciales.

La autorización determina quién puede solicitar
operaciones.

El Aggregate continúa siendo responsable de determinar si
la operación es válida según:

- estado;
- Lifecycle;
- State Machine;
- Invariants.

Debe mantenerse:

```text
Permission Granted

≠

Operation Guaranteed
```

Las reglas formales se desarrollan en:

```text
DOMAIN-009F-Permissions.md

DOMAIN-009O-Security-Model.md
```

---

# Permisos

Las operaciones de Voting pueden requerir Permissions
correspondientes a las capacidades oficiales del
Aggregate.

Conceptualmente pueden existir permisos asociados a:

```text
create voting

open voting

close voting

cancel voting

archive voting

change voting configuration
```

La definición concreta pertenece a:

```text
DOMAIN-009F-Permissions.md
```

Este documento no sustituye el modelo formal de
Permissions.

---

# Integración

Voting puede colaborar con otros Bounded Contexts y
sistemas externos mediante contratos.

Puede relacionarse estratégicamente con:

- Organization Management;
- Membership Management;
- Authorization Management;
- Assembly Management;
- Proposal Management;
- Participation Management;
- Document Management;
- Notification Management;
- Audit;
- Integration;
- Governance;
- Analytics;
- plataformas municipales;
- Smart City Integration;
- FIWARE.

Estas relaciones no introducen dependencias directas desde
el Aggregate hacia Infrastructure.

---

# Integration Events

Los hechos relevantes de Voting pueden convertirse en
Integration Events.

Conceptualmente:

```text
VotingCreatedIntegrationEvent

VotingOpenedIntegrationEvent

VotingClosedIntegrationEvent

VotingCancelledIntegrationEvent

VotingArchivedIntegrationEvent
```

Los Integration Events:

- representan hechos confirmados;
- no reemplazan Domain Events;
- permanecen fuera del estado interno del Aggregate;
- no permiten modificar directamente Voting;
- permiten comunicación entre Bounded Contexts;
- constituyen contratos externos.

La definición formal se encuentra en:

```text
DOMAIN-009K-Integration-Events.md
```

---

# Read Model

Voting puede disponer de Read Models especializados para
consulta.

Conceptualmente:

```text
VotingSummary

VotingDetailView

VotingStatusView

VotingResultView

VotingHistoryView
```

Los Read Models:

- son proyecciones;
- son reconstruibles;
- son de solo lectura;
- no constituyen fuente de verdad;
- no ejecutan lógica de negocio;
- no modifican Voting.

La definición formal se encuentra en:

```text
DOMAIN-009L-Read-Model.md
```

---

# Rendimiento

Voting debe mantenerse enfocado en la consistencia del
proceso formal de votación.

No debe cargar Aggregates externos completos para
operaciones ordinarias.

Debe utilizar:

- identificadores;
- Value Objects;
- contratos de dominio;
- Read Models para consultas.

Las consultas complejas, estadísticas y visualizaciones no
deben expandir innecesariamente el Aggregate.

Las reglas específicas se encuentran en:

```text
DOMAIN-009N-Performance-Rules.md
```

---

# Extensibilidad

Voting debe poder evolucionar sin modificar
innecesariamente su núcleo.

Los puntos de extensión pueden relacionarse con:

```text
VotingType

VotingRules

VotingOption

VotingResult

Domain Events

Integration Events

Read Models
```

Toda extensión debe:

- respetar VotingId;
- respetar OrganizationId;
- preservar Invariants;
- preservar Lifecycle;
- preservar Versioning;
- preservar Consistency Boundary;
- evitar dependencias de Infrastructure;
- evitar absorber Aggregates externos.

La definición formal se encuentra en:

```text
DOMAIN-009P-Extension-Points.md
```

---

# Compatibilidad Arquitectónica

Voting está diseñado para cumplir:

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

El Aggregate pertenece al dominio.

No depende de tecnologías concretas de Infrastructure.

---

# Dependencias

Voting depende conceptualmente de:

- Shared Kernel;
- Value Objects;
- Domain Events;
- Repository Contracts;
- contratos de dominio definidos por AURA.

Voting no depende directamente de:

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

Las implementaciones concretas pertenecen a capas
externas.

---

# Relaciones Estratégicas

Voting participa estratégicamente en procesos de:

- gobernanza organizacional;
- participación ciudadana;
- deliberación;
- decisión colectiva;
- Assemblies;
- Proposals;
- Participation;
- Documents;
- Notifications;
- Audit;
- Analytics;
- Smart City Integration.

Voting proporciona el proceso formal mediante el cual una
materia puede ser sometida a votación sin absorber la
estructura organizacional ni las participaciones
individuales asociadas.

---

# CQRS

Voting es compatible con CQRS.

Write Side:

```text
Command
   │
   ▼
Voting Aggregate
   │
   ├── Invariants
   ├── State Transition
   └── Domain Events
```

Read Side:

```text
Domain Events
      │
      ▼
Projection
      │
      ▼
Voting Read Models
```

Los Read Models no reemplazan al Aggregate.

---

# Event Sourcing

Voting es compatible con Event Sourcing.

Los Domain Events pueden representar conceptualmente la
evolución histórica del proceso.

Ejemplo:

```text
VotingCreated

      ↓

VotingOpened

      ↓

VotingClosed

      ↓

VotingArchived
```

Una ruta cancelada puede conservar:

```text
VotingCreated

      ↓

VotingCancelled

      ↓

VotingArchived
```

Los eventos históricos:

- son inmutables;
- representan hechos ocurridos;
- no representan instrucciones futuras.

La implementación técnica de Event Sourcing pertenece a
Infrastructure.

---

# Trazabilidad

Voting debe permitir reconstruir conceptualmente:

- cuándo fue creado;
- cuándo fue abierto;
- cuándo fue cerrado;
- cuándo fue cancelado;
- cuándo fue archivado;
- qué configuración poseía;
- qué cambios relevantes ocurrieron;
- cuál fue el resultado formal cuando corresponda;
- qué Version produjo cada modificación.

La trazabilidad no convierte Audit en una entidad interna
de Voting.

---

# Reglas de Diseño del Aggregate

Voting debe respetar:

- una única Aggregate Root;
- identidad única;
- identidad inmutable;
- OrganizationId inmutable;
- alto nivel de cohesión;
- bajo acoplamiento;
- Invariants protegidas;
- comportamiento explícito;
- ausencia de setters públicos;
- colaboración entre Aggregates mediante identificadores;
- ausencia de referencias mutables a Aggregates externos;
- consistencia inmediata dentro del Aggregate;
- consistencia eventual entre Aggregates;
- Domain Events para hechos internos;
- Integration Events para comunicación externa;
- Read Models para consultas;
- Repository Contract para persistencia;
- Versioning para concurrencia;
- separación entre proceso de Voting y Participation
  individual.

---

# Reglas de Interacción entre Aggregates

Voting nunca debe modificar directamente:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Participation

Document

Notification

Audit

Integration
```

Cuando un proceso requiera colaboración, debe utilizar:

- identificadores;
- contratos de dominio;
- Domain Events;
- Integration Events;
- coordinación de Application cuando corresponda.

La colaboración no amplía automáticamente el Consistency
Boundary.

---

# Escenarios de Uso Conceptuales

Voting debe poder representar procesos formales de
votación dentro de AURA sin asumir responsabilidades de
otros Aggregates.

## Voting dentro de Assembly

Una Organization dispone de una Assembly.

Dentro de ese contexto se crea un Voting relacionado
mediante:

```text
AssemblyId
```

Assembly y Voting conservan Lifecycles independientes.

---

## Voting relacionado con Proposal

Una Proposal puede constituir la materia de un proceso de
Voting.

La relación se expresa mediante:

```text
ProposalId
```

El resultado de Voting no modifica directamente la
Proposal.

---

## Voting con Participación Individual

Citizens pueden participar en el proceso mediante el
modelo correspondiente de Participation.

Voting representa:

```text
Formal Voting Process
```

Participation representa:

```text
Individual Participation
```

Ambos Aggregates permanecen separados.

---

## Voting Cerrado

Un Voting Open puede cerrarse cuando cumple las
condiciones del dominio.

El cierre:

- preserva el proceso;
- conserva su configuración histórica;
- establece ClosedAt;
- conserva el resultado formal cuando corresponda;
- incrementa Version;
- genera VotingClosed.

---

## Voting Cancelado

Un Voting puede alcanzar Cancelled cuando una transición
formal del dominio lo permita.

La cancelación:

- conserva VotingId;
- preserva el historial;
- establece CancelledAt;
- incrementa Version;
- genera VotingCancelled.

---

## Voting Archivado

Un Voting terminado conforme a las reglas del Lifecycle
puede archivarse.

Archived representa conservación histórica.

No representa eliminación física.

---

# Restricciones Arquitectónicas

No está permitido:

- convertir Organization en entidad interna de Voting;
- convertir Citizen en entidad interna de Voting;
- convertir Membership en entidad interna de Voting;
- convertir Role en entidad interna de Voting;
- convertir Territory en entidad interna de Voting;
- convertir Assembly en entidad interna de Voting;
- convertir Proposal en entidad interna de Voting;
- convertir Participation en entidad interna de Voting;
- almacenar Aggregates externos completos dentro de
  Voting;
- utilizar Citizen[] como sustituto de Participation;
- modificar VotingId;
- modificar OrganizationId;
- modificar VotingStatus directamente;
- modificar Version directamente;
- modificar Result directamente evitando comportamiento
  del Aggregate;
- modificar otros Aggregates durante una operación interna
  de Voting;
- acceder directamente a Repositories de otros Aggregates
  desde Voting;
- ejecutar HTTP desde Voting;
- acceder directamente a bases de datos;
- enviar Notifications directamente;
- ejecutar Audit directamente;
- ejecutar Integration directamente;
- introducir lógica de Infrastructure dentro del
  Aggregate;
- utilizar Read Models como fuente de escritura;
- omitir Invariants;
- omitir State Machine;
- omitir Versioning.

---

# Objetivos de Diseño

Voting busca garantizar:

- identidad formal del proceso de votación;
- propiedad organizacional clara;
- separación entre Voting y Assembly;
- separación entre Voting y Proposal;
- separación entre Voting y Participation;
- consistencia del Lifecycle;
- consistencia de Rules;
- consistencia de Options;
- consistencia del resultado formal;
- trazabilidad;
- Versioning;
- concurrencia optimista;
- independencia tecnológica;
- bajo acoplamiento;
- alta cohesión;
- interoperabilidad;
- compatibilidad con CQRS;
- compatibilidad con Event Sourcing;
- compatibilidad con Event-Driven Architecture;
- integración controlada con otros Bounded Contexts.

---

# Documentación Especializada

La definición conceptual contenida en este archivo se
desarrolla mediante la serie documental oficial:

```text
DOMAIN-009-Aggregate.md

DOMAIN-009A-Lifecycle.md

DOMAIN-009B-State-Machine.md

DOMAIN-009C-Commands.md

DOMAIN-009D-Domain-Events.md

DOMAIN-009E-Invariants.md

DOMAIN-009F-Permissions.md

DOMAIN-009G-Repository-Contract.md

DOMAIN-009H-Examples.md

DOMAIN-009I-Versioning.md

DOMAIN-009J-Consistency-Boundary.md

DOMAIN-009K-Integration-Events.md

DOMAIN-009L-Read-Model.md

DOMAIN-009M-Test-Scenarios.md

DOMAIN-009N-Performance-Rules.md

DOMAIN-009O-Security-Model.md

DOMAIN-009P-Extension-Points.md
```

Estos documentos desarrollan dimensiones específicas del
mismo Aggregate.

No constituyen Aggregates adicionales.

---

# Definición de Éxito

El Aggregate **Voting** constituye el modelo oficial de
AURA Core para representar un proceso formal de votación.

Voting mantiene:

- identidad propia mediante VotingId;
- propiedad organizacional mediante OrganizationId;
- contexto de Assembly mediante AssemblyId cuando
  corresponda;
- relación con Proposal mediante ProposalId cuando
  corresponda;
- VotingType;
- VotingStatus;
- Rules;
- Options;
- Result;
- Lifecycle;
- Invariants;
- Version;
- trazabilidad;
- Domain Events;
- Consistency Boundary propio.

Voting permanece separado de Organization, Citizen,
Membership, Role, Territory, Assembly, Proposal,
Participation, Document, Notification, Audit e
Integration.

Assembly puede proporcionar el contexto formal de una
votación, Proposal puede representar una materia
relacionada y Participation puede representar la
participación individual, pero ninguno de estos Aggregates
es absorbido por Voting.

La colaboración se realiza mediante identificadores,
contratos de dominio, Domain Events, Integration Events y
los mecanismos de coordinación ya establecidos por AURA.

De esta forma, **Voting** proporciona un límite de dominio
cohesivo, trazable, versionado e independiente para los
procesos formales de votación, manteniendo el patrón DDD
consolidado de AURA Core sin introducir dependencias
tecnológicas dentro del dominio.