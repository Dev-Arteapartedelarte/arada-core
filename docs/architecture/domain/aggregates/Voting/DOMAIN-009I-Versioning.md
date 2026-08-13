# DOMAIN-009I — Voting Versioning

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

- DOMAIN-009-Aggregate.md
- DOMAIN-009C-Commands.md
- DOMAIN-009D-Domain-Events.md
- DOMAIN-009G-Repository-Contract.md
- DOMAIN-009K-Integration-Events.md
- CORE-011-Repository-Contracts.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Definir el modelo oficial de **Versioning** del Aggregate
**Voting**.

Version permite identificar la evolución secuencial del estado del
Aggregate y constituye la base conceptual para detectar
modificaciones concurrentes incompatibles.

Toda modificación válida de Voting produce una nueva Version.

El Versioning permite:

- preservar la secuencia lógica de modificaciones;
- detectar escrituras concurrentes incompatibles;
- relacionar Domain Events con el estado que los produjo;
- mantener trazabilidad;
- preservar consistencia durante persistencia;
- soportar reconstrucción histórica;
- mantener compatibilidad con Event Sourcing;
- mantener compatibilidad con CQRS.

Version pertenece al Aggregate.

No pertenece al mecanismo concreto de persistencia.

---

# Principios

El Versioning de Voting sigue los siguientes principios:

- Version forma parte del estado del Aggregate;
- toda instancia válida posee una Version;
- toda modificación válida incrementa Version;
- las operaciones de lectura no incrementan Version;
- las operaciones rechazadas no incrementan Version;
- Version es monotónica;
- Version nunca disminuye;
- una Version utilizada no se reutiliza para representar otra
  modificación;
- el Repository debe preservar Version;
- la concurrencia se controla comparando la versión esperada con la
  versión persistida;
- los Domain Events identifican la AggregateVersion que produjo el
  hecho;
- los Integration Events pueden preservar AggregateVersion;
- la reconstrucción del Aggregate debe restaurar Version sin
  modificarla.

---

# Concepto

Voting mantiene conceptualmente:

```text
Version
```

Version representa la posición lógica actual del estado del
Aggregate dentro de su propia evolución.

Ejemplo:

```text
Voting

Version = 1
```

después de una modificación válida:

```text
Voting

Version = 2
```

y posteriormente:

```text
Voting

Version = 3
```

Debe mantenerse:

```text
Version N

↓

Valid Modification

↓

Version N + 1
```

Version no representa:

- VotingStatus;
- número de Domain Events globales;
- número de registros persistidos;
- versión de API;
- versión de base de datos;
- versión del documento;
- versión de otro Aggregate.

---

# Ciclo de Vida

Version acompaña a Voting durante todo su Lifecycle.

Conceptualmente:

```text
CreateVoting

↓

Draft

Version = 1
```

Posteriormente:

```text
Valid Modification

↓

Version = 2
```

Una transición válida posterior:

```text
Draft

↓

OpenVoting

↓

Open

Version = 3
```

y así sucesivamente.

El cambio de VotingStatus y el cambio de Version son conceptos
distintos.

Debe mantenerse:

```text
Lifecycle Transition

↓

Version Increment
```

cuando la transición es válida.

Sin embargo, una modificación válida que no cambia VotingStatus
también incrementa Version.

Ejemplo:

```text
Draft

Version = 2

↓

ChangeVotingTitle

↓

Draft

Version = 3
```

---

# Operaciones que Incrementan la Versión

Toda modificación válida del estado de Voting incrementa Version.

Entre las operaciones oficiales se encuentran:

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

Conceptualmente:

```text
Version = N

↓

Valid Command

↓

Version = N + 1
```

La nueva Version representa el estado resultante de la modificación.

---

# Operaciones que No Incrementan la Versión

No incrementan Version las operaciones que no producen una
modificación válida del Aggregate.

Entre ellas:

```text
getById()

exists()

Read Voting
```

Tampoco incrementa Version:

```text
Rejected Command

Permission Denied

Invalid State Transition

Invariant Violation

Concurrency Conflict

Rehydration

Replay
```

Debe mantenerse:

```text
Version Before

=

Version After
```

cuando no existe una nueva modificación válida del dominio.

---

# Concurrencia Optimista

Voting utiliza concurrencia optimista.

El modelo compara:

```text
ExpectedVersion
```

con:

```text
PersistedVersion
```

antes de confirmar una modificación sobre un Voting existente.

Debe cumplirse:

```text
ExpectedVersion

=

PersistedVersion
```

para aceptar la escritura correspondiente.

Conceptualmente:

```text
Load Voting

Version = N

↓

Execute Valid Command

↓

Voting Version = N + 1

↓

Persist

ExpectedVersion = N
```

Si la versión persistida continúa siendo:

```text
N
```

la modificación puede confirmarse.

Si la versión persistida cambió:

```text
PersistedVersion != ExpectedVersion
```

la modificación debe ser rechazada como conflicto de concurrencia.

---

# Conflicto de Concurrencia

Ejemplo conceptual:

```text
Voting

PersistedVersion = 5
```

Dos operaciones recuperan:

```text
Version = 5
```

La primera confirma una modificación:

```text
Version = 6
```

La segunda intenta persistir una modificación calculada sobre:

```text
ExpectedVersion = 5
```

pero encuentra:

```text
PersistedVersion = 6
```

Debe producirse:

```text
ConcurrencyConflict
```

La segunda operación no puede sobrescribir silenciosamente el
estado confirmado por la primera.

---

# Persistencia

El Repository debe persistir Version como parte del estado de
Voting.

Conceptualmente:

```text
Voting

Version = N

↓

save()

↓

Persisted Voting

Version = N
```

Al recuperar:

```text
Persisted Voting

Version = N

↓

getById()

↓

Voting

Version = N
```

El Repository no debe:

- reiniciar Version;
- disminuir Version;
- inventar una Version diferente;
- incrementar Version durante una lectura;
- modificar Version fuera de una operación válida del Aggregate.

El contrato correspondiente se define en:

```text
DOMAIN-009G-Repository-Contract.md
```

---

# Relación con Domain Events

Toda modificación válida que produce un Domain Event debe mantener
coherencia entre:

```text
Voting.Version
```

y:

```text
DomainEvent.AggregateVersion
```

Conceptualmente:

```text
Voting

Version = N

↓

Valid Command

↓

Voting

Version = N + 1

↓

Domain Event

AggregateVersion = N + 1
```

Ejemplo:

```text
VotingCreated

AggregateVersion = 1
```

posteriormente:

```text
VotingTitleChanged

AggregateVersion = 2
```

posteriormente:

```text
VotingOpened

AggregateVersion = 3
```

AggregateVersion identifica la Version del Aggregate que produjo el
hecho.

---

# Orden de Domain Events

Dentro de un mismo Voting, AggregateVersion permite establecer el
orden lógico de los hechos.

Ejemplo:

```text
VotingCreated
AggregateVersion = 1

VotingRulesChanged
AggregateVersion = 2

VotingOpened
AggregateVersion = 3

VotingClosed
AggregateVersion = 4
```

Debe mantenerse:

```text
AggregateVersion N

<

AggregateVersion N + 1
```

para modificaciones consecutivas del mismo Aggregate.

OccurredAt representa tiempo.

AggregateVersion representa orden lógico de evolución del Aggregate.

---

# Relación con Integration Events

Cuando un Domain Event da origen a un Integration Event, el
Integration Event puede preservar:

```text
AggregateVersion
```

para mantener trazabilidad respecto del estado de Voting que originó
el hecho.

Conceptualmente:

```text
Voting

Version = N

↓

Domain Event

AggregateVersion = N

↓

Integration Event

AggregateVersion = N
```

El Integration Event no modifica Version.

Tampoco controla la evolución interna de Voting.

La definición de los contratos correspondientes pertenece a:

```text
DOMAIN-009K-Integration-Events.md
```

---

# Relación con Outbox

Cuando los eventos asociados a una modificación confirmada deban
ser preservados para su publicación posterior, la información de
Version debe mantenerse coherente con el hecho producido.

Conceptualmente:

```text
Voting

Version = N + 1

↓

Domain Event

AggregateVersion = N + 1

↓

Outbox

AggregateVersion = N + 1
```

El mecanismo de Outbox no modifica:

```text
Voting.Version
```

Tampoco crea una nueva Version del Aggregate.

Debe preservar la relación entre el evento y la Version que lo
originó.

---

# Recuperación

La recuperación de Voting debe restaurar exactamente la Version
persistida.

Ejemplo:

```text
Persisted Voting

Version = 8
```

después de recuperación:

```text
Voting

Version = 8
```

La recuperación no produce:

```text
Version = 9
```

porque recuperar un Aggregate no constituye una modificación del
dominio.

Debe mantenerse:

```text
Recovery

↓

Same Version
```

---

# Rehidratación

La rehidratación restaura el estado histórico o persistido del
Aggregate.

No representa una nueva intención del dominio.

Por tanto:

```text
Rehydrate Voting

↓

No Version Increment
```

La rehidratación tampoco genera nuevos Domain Events como
consecuencia de restaurar el estado.

---

# Integración con Event Store

Voting puede mantener compatibilidad conceptual con un Event Store.

Cuando el Aggregate sea reconstruido mediante su historial de
Domain Events, AggregateVersion permite preservar la secuencia
lógica de evolución.

Conceptualmente:

```text
VotingCreated
AggregateVersion = 1

↓

VotingTitleChanged
AggregateVersion = 2

↓

VotingOpened
AggregateVersion = 3
```

La reconstrucción debe producir:

```text
Voting

Version = 3
```

sin generar una nueva Version por el hecho de realizar el Replay.

Debe mantenerse:

```text
Replay

≠

New Domain Modification
```

---

# Replay

Durante Replay:

```text
Domain Event History

↓

Rehydrate Voting

↓

Restore Version
```

Los eventos históricos ya poseen su AggregateVersion.

Replay no debe transformar:

```text
AggregateVersion = N
```

en:

```text
AggregateVersion = N + 1
```

por el solo hecho de aplicar nuevamente el hecho para reconstrucción.

---

# Integración con CQRS

En un modelo CQRS, Version pertenece al Write Side de Voting.

Conceptualmente:

```text
Command

↓

Voting Aggregate

↓

Valid Modification

↓

Version + 1

↓

Domain Event
```

El Read Side puede proyectar:

```text
AggregateVersion
```

cuando dicha información sea necesaria para representar el estado
derivado.

El Read Model no incrementa Version del Aggregate.

Debe mantenerse:

```text
Read Side Update

≠

Voting Version Increment
```

---

# Versionado del Contrato

La Version del Aggregate y la versión de los contratos documentales
representan conceptos diferentes.

Debe mantenerse:

```text
Voting.Version
```

como versión de estado del Aggregate.

Mientras:

```text
Documento Versión: 1.0
```

representa la versión del contrato conceptual documentado.

Asimismo, la evolución de un Integration Event puede poseer su
propio esquema de versionado sin alterar automáticamente:

```text
Voting.Version
```

Debe mantenerse la separación:

```text
Aggregate State Version

≠

Contract Version
```

---

# Version y VotingStatus

Version y VotingStatus no son equivalentes.

Ejemplo:

```text
VotingStatus = Draft

Version = 1
```

después de modificar Title:

```text
VotingStatus = Draft

Version = 2
```

después de modificar Rules:

```text
VotingStatus = Draft

Version = 3
```

El estado permanece Draft mientras Version evoluciona.

Por lo tanto:

```text
VotingStatus

≠

Version
```

---

# Version y Result

Result no controla Version directamente.

Una modificación válida que produzca o preserve Result conforme al
comportamiento oficial del Aggregate genera el incremento normal de
Version correspondiente.

Debe mantenerse:

```text
Result

≠

Version
```

Version representa evolución del Aggregate completo.

---

# Version y Options

Agregar o eliminar una VotingOption mediante una operación válida
modifica el estado del Aggregate.

Por tanto:

```text
AddVotingOption

↓

Version + 1
```

y:

```text
RemoveVotingOption

↓

Version + 1
```

cuando dichas operaciones son aceptadas.

Una operación rechazada conserva Version.

---

# Version y Archived

Archived no reinicia Version.

Ejemplo:

```text
Closed

Version = 7

↓

ArchiveVoting

↓

Archived

Version = 8
```

Version 8 permanece como Version del Aggregate archivado.

Debe mantenerse:

```text
Archive

≠

Version Reset
```

---

# Version e Identidad

Version no modifica:

```text
VotingId
```

Debe mantenerse durante toda la vida del Aggregate:

```text
VotingId = constant
```

mientras:

```text
Version
```

evoluciona.

Ejemplo:

```text
VotingId = VOT-001
Version = 1

VotingId = VOT-001
Version = 2

VotingId = VOT-001
Version = 3
```

---

# Version y OrganizationId

OrganizationId permanece inmutable independientemente del número de
Version.

Conceptualmente:

```text
OrganizationId = ORG-001
Version = 1
```

posteriormente:

```text
OrganizationId = ORG-001
Version = N
```

Version no permite transferir Voting a otra Organization.

---

# Version entre Aggregates

La Version de Voting pertenece exclusivamente a Voting.

No debe utilizarse como Version de:

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

Cada Aggregate mantiene su propio control de evolución.

Debe mantenerse:

```text
Voting.Version

≠

ExternalAggregate.Version
```

---

# Restricciones

No está permitido:

- crear un Voting válido sin Version;
- modificar Version directamente mediante Commands;
- disminuir Version;
- reiniciar Version durante el Lifecycle;
- reutilizar una Version para representar dos modificaciones
  consecutivas;
- incrementar Version durante una lectura;
- incrementar Version durante exists();
- incrementar Version durante getById();
- incrementar Version durante rehidratación;
- incrementar Version durante Replay;
- incrementar Version ante un Command rechazado;
- incrementar Version ante una Permission denegada;
- incrementar Version ante una transición inválida;
- incrementar Version ante una violación de Invariant;
- confirmar una escritura cuando ExpectedVersion no coincide con
  PersistedVersion;
- utilizar sobrescritura silenciosa para resolver conflictos de
  concurrencia;
- modificar AggregateVersion de un Domain Event histórico;
- utilizar Version como sustituto de VotingStatus;
- utilizar Version como versión de contrato;
- compartir Voting.Version como Version interna de otro Aggregate;
- permitir que un Read Model modifique Voting.Version;
- permitir que un Integration Event incremente Voting.Version;
- permitir que Outbox genere una nueva Version del Aggregate.

---

# Reglas

## REG-001

Todo Voting válido debe poseer una Version.

---

## REG-002

Toda modificación válida incrementa Version exactamente una vez
para representar el nuevo estado resultante.

---

## REG-003

Las operaciones que no modifican válidamente Voting no incrementan
Version.

---

## REG-004

Version es monotónica y nunca puede disminuir ni reutilizarse para
representar otra modificación consecutiva.

---

## REG-005

El Repository debe preservar Version durante persistencia y
recuperación.

---

## REG-006

Toda escritura sobre un Voting existente debe comprobar
ExpectedVersion contra PersistedVersion.

---

## REG-007

Cuando:

```text
ExpectedVersion != PersistedVersion
```

la modificación debe ser rechazada mediante el conflicto de
concurrencia correspondiente.

---

## REG-008

Todo Domain Event producido por una modificación válida debe
identificar la AggregateVersion correspondiente al estado
resultante.

---

## REG-009

Rehidratación y Replay restauran Version y no producen un nuevo
incremento.

---

## REG-010

Voting.Version pertenece exclusivamente al estado del Aggregate y
no debe confundirse con versiones de contratos, documentos,
Integration Events o Aggregates externos.

---

# Definición de Éxito

El Aggregate **Voting** mantiene un modelo explícito y consistente
de Versioning durante toda su evolución.

Version permite representar:

```text
Current Logical Aggregate State
```

y garantiza que:

- toda modificación válida produce una nueva Version;
- las lecturas no alteran Version;
- las operaciones rechazadas no alteran Version;
- Version nunca disminuye;
- Version nunca se reinicia;
- el Repository preserva Version;
- ExpectedVersion protege la escritura concurrente;
- PersistedVersion representa la versión actualmente confirmada;
- una concurrencia incompatible es rechazada;
- los Domain Events preservan AggregateVersion;
- los Integration Events pueden mantener la referencia a
  AggregateVersion;
- Outbox preserva la Version asociada al hecho sin modificar el
  Aggregate;
- la recuperación restaura Version;
- Replay no genera una nueva Version;
- CQRS mantiene separado el Versioning del Write Side respecto de
  las proyecciones de lectura;
- Event Store puede reconstruir la secuencia histórica mediante
  AggregateVersion;
- Version permanece separada de VotingStatus;
- Version permanece separada del versionado de contratos;
- Version pertenece exclusivamente a Voting.

De esta forma, `DOMAIN-009I-Versioning.md` establece el modelo
oficial de evolución y concurrencia del Aggregate **Voting**,
manteniendo el patrón consolidado de AURA Core.