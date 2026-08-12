# DOMAIN-007I — Proposal Versioning

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
- DOMAIN-007H-Examples.md
- DOMAIN-007J-Consistency-Boundary.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Definir el modelo oficial de versionado del Aggregate
**Proposal**.

El versionado permite identificar de forma explícita la evolución
del estado de una Proposal y proteger el Aggregate frente a
modificaciones concurrentes incompatibles.

Cada Proposal mantiene una versión propia que representa la
versión lógica de su estado dentro del dominio.

El versionado forma parte de las reglas de consistencia del
Aggregate y no constituye un detalle de infraestructura.

Su propósito principal es garantizar que una modificación sea
persistida únicamente cuando se realiza sobre la versión del
Aggregate que el proceso esperaba modificar.

---

# Propósito

El modelo de versionado de Proposal permite:

- identificar la versión lógica actual del Aggregate;
- detectar modificaciones concurrentes;
- impedir sobrescrituras silenciosas;
- proteger las invariantes frente a concurrencia;
- mantener consistencia entre lectura y escritura;
- garantizar evolución ordenada del Aggregate;
- proporcionar trazabilidad sobre modificaciones válidas;
- permitir persistencia mediante concurrencia optimista;
- mantener independencia respecto de la tecnología de
  persistencia.

Version no representa:

- una versión del esquema de base de datos;
- una versión de API;
- una versión de contrato HTTP;
- una versión de aplicación;
- una versión de Deployment;
- una versión de Domain Event;
- una versión de Integration Event.

Version representa exclusivamente la evolución lógica de una
instancia concreta de Proposal.

---

# Principios

El versionado de Proposal cumple los siguientes principios:

- cada Proposal posee su propia Version;
- Version pertenece al Aggregate;
- Version representa modificaciones válidas del estado;
- Version es monotónicamente creciente;
- Version nunca retrocede;
- Version no puede modificarse directamente;
- toda modificación válida incrementa Version;
- una operación rechazada no incrementa Version;
- una lectura no incrementa Version;
- la rehidratación no incrementa Version;
- la reconstrucción desde persistencia no incrementa Version;
- la reproducción histórica de eventos no constituye una nueva
  modificación;
- el Repository utiliza Version para detectar conflictos de
  concurrencia;
- una escritura incompatible no puede sobrescribir silenciosamente
  una versión posterior;
- el mecanismo es independiente de la tecnología de persistencia.

---

# Concepto de Version

Cada Proposal mantiene:

```text
Version
```

Version representa la revisión lógica actual del estado del
Aggregate.

Conceptualmente:

```text
ProposalId

+

Version

=

Specific Aggregate Revision
```

Una Proposal puede mantener durante su existencia:

```text
ProposalId = proposal-001
```

mientras Version evoluciona:

```text
1

↓

2

↓

3

↓

4
```

La identidad permanece constante.

La versión cambia conforme evoluciona válidamente el estado del
Aggregate.

---

# Propiedad de Version

Version pertenece exclusivamente a:

```text
Proposal
```

No pertenece a:

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

Cada Aggregate mantiene su propio mecanismo de versionado cuando
corresponda.

La Version de Proposal no representa ni sincroniza las versiones
de otros Aggregates.

---

# Identidad y Version

ProposalId y Version representan conceptos distintos.

```text
ProposalId
```

identifica permanentemente al Aggregate.

```text
Version
```

identifica la revisión lógica de su estado.

Por lo tanto:

```text
ProposalId
    =
Immutable Identity
```

mientras:

```text
Version
    =
Mutable Monotonic Revision
```

Una modificación válida cambia Version.

Nunca cambia ProposalId.

---

# Atributo Conceptual

El Aggregate mantiene:

```text
Version
```

como atributo conceptual obligatorio.

Version debe estar disponible para:

- validación de concurrencia;
- persistencia;
- reconstrucción;
- trazabilidad;
- detección de modificaciones incompatibles.

Version no debe exponerse como un atributo libremente editable.

---

# Estado Inicial de Version

Cuando una Proposal es creada correctamente, el Aggregate
establece una versión inicial válida.

Conceptualmente:

```text
CreateProposal

↓

ProposalCreated

↓

Version = InitialVersion
```

Para los ejemplos conceptuales del Aggregate se utiliza:

```text
InitialVersion = 1
```

La versión inicial representa la primera revisión válida de la
Proposal creada.

El valor inicial debe mantenerse consistente dentro de la
implementación y del Repository Contract.

---

# Incremento de Version

Toda modificación válida del Aggregate incrementa Version.

Conceptualmente:

```text
Valid State Change

↓

Version = Version + 1
```

Ejemplo:

```text
Version = 5

↓

RenameProposal

↓

ProposalRenamed

↓

Version = 6
```

El incremento forma parte de la misma modificación lógica del
Aggregate.

---

# Regla de Incremento

Version se incrementa únicamente cuando una operación modifica
válidamente el estado del Aggregate.

Ejemplos:

```text
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

Cuando cualquiera de estas operaciones produce una modificación
válida, Version debe avanzar.

---

# Modificación Válida

Una modificación se considera válida únicamente cuando:

- el Command corresponde al comportamiento permitido;
- la autorización necesaria ha sido satisfecha;
- el estado actual permite la operación;
- las precondiciones aplicables son válidas;
- las invariantes permanecen satisfechas;
- la modificación produce un nuevo estado válido del Aggregate.

Conceptualmente:

```text
Authorized Intent

+

Valid State

+

Valid Invariants

+

Valid Domain Operation

=

Valid Modification
```

Solo entonces:

```text
Version
    =
Version + 1
```

---

# Operación Rechazada

Una operación rechazada no incrementa Version.

Conceptualmente:

```text
Rejected Command

↓

No State Change

↓

No Version Change

↓

No Success Domain Event
```

Ejemplo:

```text
ProposalStatus = Submitted

Version = 8
```

Se intenta:

```text
RenameProposal
```

Si Submitted no permite esa modificación:

```text
ProposalStatus = Submitted

Version = 8
```

deben permanecer sin cambios.

---

# Violación de Invariante

Cuando una operación viola una invariante:

```text
Invariant Violation

↓

Operation Rejected
```

Debe mantenerse:

```text
State = PreviousState

Version = PreviousVersion
```

No debe producirse un Domain Event de éxito correspondiente a la
operación rechazada.

---

# Transición de Estado Inválida

Una transición inválida no modifica Version.

Ejemplo:

```text
ProposalStatus = Draft

Version = 4
```

Se intenta:

```text
AcceptProposal
```

La transición:

```text
Draft

↓

Accepted
```

no pertenece a la State Machine establecida.

Por lo tanto:

```text
ProposalStatus = Draft

Version = 4
```

permanecen sin cambios.

---

# Autorización Rechazada

Cuando el actor no posee la capacidad necesaria para ejecutar una
operación, no debe producirse una modificación válida del
Aggregate.

Conceptualmente:

```text
Permission Denied

↓

No Domain Modification

↓

No Version Increment
```

La autorización y el versionado mantienen responsabilidades
separadas.

---

# Lecturas

Las operaciones de lectura no modifican Version.

Ejemplo:

```text
Version = 12
```

Se ejecutan:

```text
Read Proposal

Read Proposal

Read Proposal
```

El resultado continúa siendo:

```text
Version = 12
```

Version representa cambios del estado del Aggregate, no cantidad
de accesos.

---

# Consultas

Las consultas sobre Proposal no incrementan Version.

Esto incluye consultas realizadas mediante:

```text
Proposal Read Model
```

o recuperación del Aggregate para lectura.

Debe mantenerse:

```text
Query

≠

Aggregate Modification
```

---

# Rehidratación

La reconstrucción de una Proposal desde persistencia no constituye
una nueva modificación del dominio.

Ejemplo:

```text
Persisted Proposal

ProposalId = proposal-001

ProposalStatus = UnderReview

Version = 15
```

Al reconstruir el Aggregate:

```text
ProposalId = proposal-001

ProposalStatus = UnderReview

Version = 15
```

Version permanece:

```text
15
```

No debe convertirse en:

```text
16
```

por el solo hecho de reconstruir el Aggregate.

---

# Reconstrucción y Domain Events

La reconstrucción del Aggregate no produce nuevos Domain Events
de negocio.

Conceptualmente:

```text
Persisted State

↓

Rehydrate Proposal

↓

Same Logical State

Same Version

No New Domain Event
```

Rehidratar una Proposal existente no equivale a crearla
nuevamente.

---

# Event Sourcing

Cuando la infraestructura utilice Event Sourcing, Proposal puede
reconstruirse mediante la reproducción de eventos históricos.

Ejemplo:

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

La reproducción histórica permite reconstruir el estado actual.

El replay no representa nuevas modificaciones actuales.

Por lo tanto:

```text
Replay

≠

New Version Increment caused by replay
```

y:

```text
Replay

≠

New Event Publication
```

La Version reconstruida debe corresponder a la revisión lógica
resultante del historial persistido.

---

# Concurrencia

Dos procesos pueden recuperar simultáneamente la misma Proposal.

Ejemplo:

```text
Persisted Proposal

Version = 10
```

Proceso A recupera:

```text
Version = 10
```

Proceso B recupera:

```text
Version = 10
```

Ambos poseen inicialmente una representación válida de la misma
revisión.

El conflicto aparece cuando ambos intentan persistir
modificaciones incompatibles sobre la misma versión esperada.

---

# Concurrencia Optimista

Proposal utiliza control de concurrencia optimista.

El modelo conceptual se basa en:

```text
ExpectedVersion

PersistedVersion
```

Una escritura es aceptada únicamente cuando:

```text
ExpectedVersion
    =
PersistedVersion
```

Si ambas versiones son distintas:

```text
ExpectedVersion
    ≠
PersistedVersion
```

la escritura debe ser rechazada.

---

# ExpectedVersion

ExpectedVersion representa la versión del Aggregate sobre la cual
el proceso realizó su modificación.

Ejemplo:

```text
Proposal loaded at Version = 10
```

Entonces:

```text
ExpectedVersion = 10
```

Después de una modificación válida, la instancia puede quedar:

```text
Version = 11
```

La persistencia debe comprobar que la versión almacenada continúa
siendo:

```text
10
```

antes de aceptar la nueva revisión.

---

# PersistedVersion

PersistedVersion representa la versión actualmente confirmada en
persistencia.

Antes de guardar una nueva revisión:

```text
ExpectedVersion
```

debe compararse con:

```text
PersistedVersion
```

La comparación protege contra modificaciones realizadas por otros
procesos después de que el Aggregate fue recuperado.

---

# Persistencia Exitosa

Ejemplo:

```text
Proposal loaded

Version = 10
```

Una operación válida produce:

```text
Version = 11
```

El Repository recibe conceptualmente:

```text
ProposalRepository.save(
    Proposal,
    ExpectedVersion = 10
)
```

La persistencia mantiene:

```text
PersistedVersion = 10
```

Entonces:

```text
ExpectedVersion
    =
PersistedVersion
```

La escritura puede ser aceptada.

Después del commit:

```text
PersistedVersion = 11
```

---

# Conflicto de Concurrencia

Ejemplo:

```text
ExpectedVersion = 10

PersistedVersion = 11
```

La condición es:

```text
ExpectedVersion
    ≠
PersistedVersion
```

La escritura debe ser rechazada.

Conceptualmente se produce:

```text
ProposalConcurrencyConflict
```

El estado persistido no debe ser sobrescrito.

---

# Ejemplo de Concurrencia

Estado inicial:

```text
ProposalStatus = UnderReview

Version = 20
```

Proceso A recupera:

```text
ProposalStatus = UnderReview

Version = 20
```

Proceso B recupera:

```text
ProposalStatus = UnderReview

Version = 20
```

Proceso A ejecuta:

```text
AcceptProposal
```

Su instancia válida queda:

```text
ProposalStatus = Accepted

Version = 21
```

Proceso A persiste con:

```text
ExpectedVersion = 20
```

La persistencia contiene:

```text
PersistedVersion = 20
```

La escritura es aceptada.

El estado persistido pasa a:

```text
ProposalStatus = Accepted

Version = 21
```

Proceso B ejecuta sobre su copia previa:

```text
RejectProposal
```

Su instancia local queda:

```text
ProposalStatus = Rejected

Version = 21
```

Proceso B intenta persistir con:

```text
ExpectedVersion = 20
```

pero el Repository encuentra:

```text
PersistedVersion = 21
```

La operación debe ser rechazada.

El estado persistido permanece:

```text
ProposalStatus = Accepted

Version = 21
```

---

# Protección contra Lost Update

El versionado protege Proposal contra:

```text
Lost Update
```

Sin validación de Version podría ocurrir:

```text
Process A

Version 10
→
Accepted
```

y posteriormente:

```text
Process B

Version 10
→
Rejected
```

sobrescribiendo silenciosamente la decisión anterior.

Esto no está permitido.

Debe utilizarse:

```text
ExpectedVersion Validation
```

antes de aceptar la persistencia.

---

# Prohibición de Last Write Wins

Proposal no utiliza:

```text
Last Write Wins
```

como mecanismo para resolver modificaciones concurrentes
incompatibles.

La última escritura recibida no puede reemplazar automáticamente
una revisión posterior válida.

Debe mantenerse:

```text
Version Conflict

↓

Explicit Rejection
```

No:

```text
Version Conflict

↓

Silent Overwrite
```

---

# Resolución de Conflictos

Cuando ocurre:

```text
ProposalConcurrencyConflict
```

la modificación conflictiva no debe ser aplicada automáticamente
sobre la versión actual.

Conceptualmente, el proceso que necesita continuar debe:

```text
Reload Proposal

↓

Obtain Current Version

↓

Reevaluate Intended Operation

↓

Validate Current State

↓

Validate Invariants

↓

Execute New Valid Operation

↓

Persist with Current ExpectedVersion
```

La operación original no puede asumirse válida sobre una versión
que no fue utilizada durante su evaluación.

---

# Reintento

Un conflicto de concurrencia no implica que el mismo cambio pueda
reintentarse ciegamente.

Después de recuperar la versión actual:

```text
Proposal
```

debe volver a evaluar:

- estado;
- invariantes;
- transición;
- permisos cuando corresponda;
- validez de la intención original.

Ejemplo:

```text
Process B intended RejectProposal
```

pero después de recargar encuentra:

```text
ProposalStatus = Accepted
```

La State Machine puede impedir:

```text
Accepted

↓

Rejected
```

Por lo tanto, el reintento debe ser rechazado por el dominio.

---

# Version y State Machine

Version no reemplaza la State Machine.

Una coincidencia válida:

```text
ExpectedVersion
    =
PersistedVersion
```

no convierte una transición inválida en válida.

Debe mantenerse:

```text
Valid Version

+

Invalid Transition

=

Rejected Operation
```

---

# Version e Invariantes

Version no reemplaza las invariantes.

Debe mantenerse:

```text
Valid Version

+

Invariant Violation

=

Rejected Operation
```

La validación de concurrencia y la validación del dominio
protegen aspectos diferentes.

---

# Version y Permissions

Version no reemplaza Permissions.

Debe mantenerse:

```text
Valid Version

+

Permission Denied

=

Rejected Operation
```

Del mismo modo:

```text
Permission Granted

+

Version Conflict

=

Rejected Persistence
```

Los permisos determinan quién puede intentar una operación.

Version protege qué revisión puede modificarse.

---

# Version y Commands

Los Commands expresan intención de modificar Proposal.

Cuando corresponda, el proceso de aplicación debe mantener la
versión esperada utilizada para ejecutar la operación.

Conceptualmente:

```text
Command

↓

Load Proposal at Version N

↓

Execute Domain Behavior

↓

Proposal Version N+1

↓

Save with ExpectedVersion N
```

La Version no convierte al Command en un evento ni forma parte de
la identidad del Command.

---

# Version y Domain Events

Una modificación válida puede producir:

```text
Domain Event
```

y una nueva:

```text
Version
```

Ejemplo:

```text
Version = 7

↓

SubmitProposal

↓

ProposalStatus = Submitted

Version = 8

ProposalSubmitted
```

El evento representa el hecho ocurrido.

Version representa la revisión lógica resultante del Aggregate.

Ambos conceptos se relacionan, pero no son equivalentes.

---

# Version de Aggregate y Version de Evento

Debe mantenerse la separación conceptual entre:

```text
Aggregate Version
```

y:

```text
Event Schema Version
```

La Version de Proposal representa la evolución de una instancia
del Aggregate.

Una eventual versión del contrato de un Domain Event representa
la evolución estructural del evento.

No deben confundirse.

---

# Version de Aggregate y Version de Integration Event

Debe mantenerse:

```text
Proposal.Version

≠

Integration Event Version
```

La evolución de contratos de integración pertenece al modelo de
Integration Events.

No modifica por sí misma Version de Proposal.

---

# Version y Repository

El Repository utiliza Version para proteger la persistencia del
Aggregate.

Conceptualmente:

```text
ProposalRepository
```

debe poder recibir:

```text
Proposal

ExpectedVersion
```

y validar:

```text
ExpectedVersion
    =
PersistedVersion
```

antes de confirmar la nueva revisión.

El Repository no decide cuándo una operación del dominio debe
incrementar Version.

Esa regla pertenece al modelo del Aggregate.

---

# Repository Contract

El comportamiento de persistencia debe respetar:

```text
DOMAIN-007G-Repository-Contract.md
```

El Repository:

- recupera Proposal preservando Version;
- persiste Proposal como una unidad;
- valida ExpectedVersion;
- detecta conflictos;
- no sobrescribe silenciosamente una versión posterior;
- no modifica Version arbitrariamente;
- no ejecuta comportamiento de dominio;
- no altera el Lifecycle;
- no altera la State Machine.

---

# Persistencia Atómica

La persistencia de una nueva versión debe representar una única
modificación lógica del Aggregate.

Conceptualmente:

```text
Previous Aggregate State

+

Valid Domain Modification

+

Version Increment

=

New Aggregate State
```

La persistencia no debe confirmar parcialmente una modificación
dejando Version y estado en revisiones incompatibles.

---

# Estado y Version

El estado y Version pertenecen a la misma revisión lógica.

Ejemplo inválido:

```text
ProposalStatus = Accepted

Version = 10
```

cuando Accepted corresponde a una modificación que debería haber
producido:

```text
Version = 11
```

No debe persistirse una combinación parcial de revisiones.

---

# Domain Events y Persistencia

Los Domain Events generados por una modificación corresponden a
la revisión lógica producida por esa modificación.

Una modificación no confirmada por persistencia no debe
considerarse una revisión persistida del Aggregate.

Conceptualmente:

```text
Domain Behavior

↓

New Local State

↓

New Version

↓

Repository Validation

↓

Commit
```

Solo después de una persistencia válida existe una nueva revisión
confirmada.

---

# Fallo de Persistencia

Si una modificación válida ocurre en memoria pero la persistencia
falla:

```text
Persistence Failure
```

la nueva versión no debe considerarse confirmada en el estado
persistido.

Ejemplo:

```text
PersistedVersion = 10
```

La instancia local alcanza:

```text
Version = 11
```

pero:

```text
save()
```

falla.

Entonces la versión confirmada continúa siendo:

```text
PersistedVersion = 10
```

---

# Fallo de Persistencia y Eventos

Cuando el commit no se confirma, los efectos externos derivados
de la nueva revisión no deben tratarla como una revisión
persistida correctamente.

Debe mantenerse:

```text
Failed Commit

↓

No Confirmed Aggregate Revision
```

La coordinación técnica para garantizar la publicación
consistente pertenece a las capas correspondientes y no modifica
las reglas conceptuales de Version.

---

# Version y Audit

Version contribuye a la trazabilidad del Aggregate.

Conceptualmente pueden relacionarse:

```text
ProposalId

Version

ActorId

Timestamp

CommandId

CorrelationId

CausationId

Domain Event
```

Esto permite identificar qué revisión del Aggregate resultó de
una modificación.

Audit permanece fuera del límite de consistencia de Proposal.

---

# Version y Read Models

Los Read Models pueden exponer:

```text
Version
```

cuando resulte necesario para consulta o trazabilidad.

Sin embargo:

```text
Read Model Version
```

no constituye la fuente oficial para modificar Proposal.

La fuente de verdad del lado de escritura continúa siendo:

```text
Proposal Aggregate
```

y su estado persistido conforme al Repository Contract.

---

# Read Model Desactualizado

Debido a consistencia eventual, un Read Model puede mostrar:

```text
Version = 15
```

mientras el lado de escritura ya mantiene:

```text
Version = 16
```

La aplicación no debe utilizar la proyección desactualizada como
sustituto de la versión persistida del Aggregate para validar una
modificación.

Debe mantenerse:

```text
Read Projection

≠

Write Concurrency Authority
```

---

# Version e Integration

Integration Events pueden transportar información suficiente para
identificar la revisión de Proposal cuando el contrato
correspondiente lo requiera.

Esto no convierte al sistema externo en autoridad sobre Version.

Debe mantenerse:

```text
Proposal
    =
Owner of Aggregate Version
```

Los sistemas externos no modifican directamente Version.

---

# Sistemas Externos

Un sistema municipal, Smart City o cualquier consumidor externo
puede recibir información relacionada con Proposal.

Sin embargo, no puede establecer directamente:

```text
Proposal.Version
```

La modificación de Proposal debe ingresar mediante los mecanismos
de aplicación y dominio establecidos.

---

# Version y FIWARE

Una representación externa de Proposal en un ecosistema FIWARE
puede mantener metadatos propios de sincronización o versión.

Estos valores no sustituyen:

```text
Proposal.Version
```

La versión del Aggregate continúa perteneciendo al dominio AURA.

Debe mantenerse:

```text
External Representation Version

≠

Proposal Aggregate Version
```

---

# Independencia Tecnológica

El modelo de Version no depende de:

- PostgreSQL;
- MongoDB;
- MySQL;
- SQLite;
- Redis;
- Elasticsearch;
- OpenSearch;
- ORM;
- Event Store específico;
- HTTP;
- REST;
- GraphQL;
- FIWARE;
- NGSI-LD;
- Frameworks.

La infraestructura debe implementar las reglas de concurrencia
establecidas por el dominio.

---

# Implementación de Infraestructura

La infraestructura puede utilizar mecanismos técnicos distintos
para implementar la validación de Version.

El detalle técnico pertenece a Infrastructure.

Independientemente del mecanismo utilizado, debe preservarse la
regla conceptual:

```text
ExpectedVersion
    =
PersistedVersion
```

antes de aceptar una escritura.

La tecnología no puede alterar esta semántica.

---

# Cambio de Persistencia

Si la infraestructura cambia de:

```text
PostgreSQL
```

a:

```text
MongoDB
```

o a cualquier otro mecanismo compatible, las reglas de Version
permanecen iguales.

No deben modificarse por esta razón:

- incremento monotónico;
- ExpectedVersion;
- PersistedVersion;
- detección de conflictos;
- rechazo de sobrescrituras incompatibles;
- relación entre modificación válida y nueva Version.

---

# Ciclo de Version

Un ciclo conceptual puede representarse como:

```text
Load Proposal

↓

Version = N

↓

Validate Permission

↓

Execute Command

↓

Validate State

↓

Validate Invariants

↓

Modify Aggregate

↓

Version = N + 1

↓

Produce Domain Event

↓

Save with ExpectedVersion = N

↓

Compare with PersistedVersion

↓

Commit or Conflict
```

---

# Flujo Exitoso

```text
ExpectedVersion = 8

PersistedVersion = 8

↓

Valid

↓

Persist Proposal Version = 9
```

Resultado:

```text
PersistedVersion = 9
```

---

# Flujo Conflictivo

```text
ExpectedVersion = 8

PersistedVersion = 9

↓

Conflict

↓

Reject Write
```

Resultado:

```text
PersistedVersion = 9
```

La revisión existente no cambia.

---

# Flujo con Invariante Inválida

```text
Version = 8

↓

Command

↓

Invariant Violation

↓

Rejected
```

Resultado:

```text
Version = 8
```

No se alcanza la fase de persistencia de una nueva revisión
válida.

---

# Flujo con Estado Inválido

```text
ProposalStatus = Archived

Version = 18

↓

RenameProposal

↓

Invalid State

↓

Rejected
```

Resultado:

```text
ProposalStatus = Archived

Version = 18
```

---

# Flujo con Permiso Inválido

```text
ProposalStatus = UnderReview

Version = 20

↓

Actor without proposal:accept

↓

AcceptProposal

↓

Permission Denied
```

Resultado:

```text
ProposalStatus = UnderReview

Version = 20
```

---

# Flujo de Evolución Completo

Un ejemplo conceptual puede evolucionar:

```text
ProposalCreated
Version = 1

↓

ProposalRenamed
Version = 2

↓

ProposalPurposeChanged
Version = 3

↓

ProposalContentUpdated
Version = 4

↓

ProposalSubmitted
Version = 5

↓

ProposalReviewStarted
Version = 6

↓

ProposalAccepted
Version = 7

↓

ProposalArchived
Version = 8
```

Los valores concretos son ilustrativos.

La regla normativa es:

```text
Every Valid Modification

↓

Version Increases
```

---

# Version y Archived

Una Proposal archivada conserva su Version.

Ejemplo:

```text
ProposalStatus = Archived

Version = 25
```

La recuperación posterior debe preservar:

```text
Version = 25
```

Archived no significa:

```text
Version = null
```

ni:

```text
Version = 0
```

ni reinicio de la secuencia.

---

# Version y Eliminación Lógica

El archivado no elimina la identidad ni la historia lógica de la
Proposal.

Debe mantenerse:

```text
Archived Proposal

↓

Same ProposalId

Same Final Version
```

Una eventual estrategia técnica de eliminación física no debe
redefinir estas reglas conceptuales.

---

# Prohibición de Reinicio

Version nunca debe reiniciarse durante el ciclo de vida de una
Proposal.

No está permitido:

```text
Version 15

↓

Archive

↓

Version 1
```

Tampoco:

```text
Version 15

↓

Reload

↓

Version 1
```

La secuencia permanece monotónica.

---

# Prohibición de Retroceso

No está permitido:

```text
Version 10

↓

Version 9
```

como consecuencia de una modificación válida.

Version nunca retrocede.

---

# Prohibición de Edición Directa

No debe existir comportamiento público equivalente a:

```text
setVersion(100)
```

ni:

```text
changeVersion(100)
```

Version evoluciona exclusivamente como consecuencia de
modificaciones válidas del Aggregate.

---

# Prohibición de Incremento por Lectura

No está permitido:

```text
Read Proposal

↓

Version + 1
```

Las consultas no modifican la revisión lógica.

---

# Prohibición de Incremento por Rehidratación

No está permitido:

```text
Load Proposal Version 10

↓

Rehydrate

↓

Version 11
```

La reconstrucción debe preservar exactamente la revisión
persistida.

---

# Prohibición de Incremento por Command Rechazado

No está permitido:

```text
Invalid Command

↓

Version + 1
```

Debe mantenerse:

```text
Invalid Command

↓

No Version Change
```

---

# Prohibición de Sobrescritura Silenciosa

No está permitido:

```text
ExpectedVersion = 10

PersistedVersion = 11

↓

Overwrite Version 11
```

La operación debe producir un conflicto explícito.

---

# Prohibición de Version Compartida

No existe una única Version global para todas las Proposals.

Cada Aggregate mantiene su propia secuencia.

Ejemplo:

```text
Proposal A
Version = 8
```

```text
Proposal B
Version = 3
```

Ambas versiones son independientes.

---

# Prohibición de Sincronización entre Aggregates

La modificación de Proposal no incrementa automáticamente la
Version de:

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
```

Del mismo modo, modificaciones en esos Aggregates no incrementan
automáticamente Proposal.Version.

Cada Aggregate protege su propio límite de consistencia.

---

# Version y Consistency Boundary

Version protege exclusivamente el límite de consistencia de
Proposal.

Conceptualmente:

```text
Proposal
    │
    ├── State
    ├── Invariants
    └── Version
```

No:

```text
Proposal Version
    │
    ├── Organization Version
    ├── Territory Version
    ├── Assembly Version
    └── Voting Version
```

La coordinación entre Aggregates utiliza los mecanismos
establecidos para arquitectura distribuida.

---

# Invariantes de Version

El modelo de versionado mantiene como mínimo las siguientes
invariantes:

- Version es obligatoria;
- Version pertenece a una única Proposal;
- Version representa una revisión lógica del Aggregate;
- Version nunca retrocede;
- Version no se reinicia;
- Version no se modifica directamente;
- toda modificación válida incrementa Version;
- una operación rechazada no incrementa Version;
- una lectura no incrementa Version;
- una rehidratación no incrementa Version;
- una reconstrucción histórica no representa una nueva
  modificación;
- una escritura requiere validación de ExpectedVersion;
- ExpectedVersion debe coincidir con PersistedVersion;
- un conflicto impide la escritura;
- un conflicto no puede resolverse mediante sobrescritura
  silenciosa;
- Version no reemplaza invariantes;
- Version no reemplaza Permissions;
- Version no reemplaza la State Machine;
- Version no sincroniza automáticamente otros Aggregates.

Estas reglas complementan las invariantes establecidas en:

```text
DOMAIN-007E-Invariants.md
```

---

# Relación con Lifecycle

Version acompaña la evolución de Proposal durante su Lifecycle.

Ejemplo:

```text
Draft
Version = 1

↓

Submitted
Version = 2

↓

UnderReview
Version = 3

↓

Accepted
Version = 4

↓

Archived
Version = 5
```

Los números son ilustrativos.

El Lifecycle define los estados y su evolución.

Version registra la revisión lógica resultante de las
modificaciones válidas.

---

# Relación con State Machine

State Machine determina si una transición es válida.

Version no autoriza transiciones.

Debe mantenerse:

```text
State Machine

↓

Transition Validity
```

y:

```text
Version

↓

Revision and Concurrency Control
```

Ambas reglas cooperan sin reemplazarse.

---

# Relación con Commands

Los Commands pueden producir modificaciones válidas del
Aggregate.

Cuando un Command es aceptado y modifica Proposal:

```text
Version
```

incrementa.

Cuando el Command es rechazado:

```text
Version
```

permanece sin cambios.

---

# Relación con Domain Events

Los Domain Events representan hechos resultantes de operaciones
válidas.

Una nueva revisión puede asociarse conceptualmente con el evento
que produjo el cambio.

Ejemplo:

```text
ProposalSubmitted

ProposalId = proposal-001

AggregateVersion = 8
```

cuando el contrato del evento correspondiente contemple dicha
información.

La definición formal de los eventos permanece en:

```text
DOMAIN-007D-Domain-Events.md
```

---

# Relación con Permissions

Permissions determina si un actor puede solicitar una operación.

Version determina si la revisión utilizada por la operación
continúa siendo compatible con la revisión persistida.

Debe mantenerse:

```text
Authorization

≠

Concurrency Control
```

---

# Relación con Repository Contract

El Repository Contract implementa la frontera de persistencia
necesaria para validar:

```text
ExpectedVersion

PersistedVersion
```

El contrato oficial se encuentra en:

```text
DOMAIN-007G-Repository-Contract.md
```

---

# Relación con Examples

Los escenarios conceptuales de versionado y concurrencia se
desarrollan también en:

```text
DOMAIN-007H-Examples.md
```

Los ejemplos no sustituyen las reglas normativas definidas en
este documento.

---

# Relación con Consistency Boundary

El versionado protege el límite definido en:

```text
DOMAIN-007J-Consistency-Boundary.md
```

Proposal.Version no debe utilizarse para crear una transacción
distribuida sobre múltiples Aggregates.

---

# Casos de Uso Conceptuales

El modelo de Version permite soportar:

```text
Modificar una Proposal recuperada previamente.

Detectar modificaciones concurrentes.

Evitar pérdida de actualizaciones.

Rechazar escrituras sobre revisiones obsoletas.

Reconstruir Proposal preservando su revisión.

Mantener trazabilidad de cambios.

Coordinar Repository y Aggregate sin acoplar el dominio a una
tecnología de persistencia.
```

---

# Escenario — Edición Concurrente

```text
Proposal Version 5

        │
        ├───────────────┐
        │               │
        ▼               ▼
    Process A        Process B
    Version 5        Version 5
        │               │
        ▼               ▼
     Change A         Change B
        │               │
        ▼               ▼
    Version 6        Version 6
        │               │
        ▼               ▼
      Save A           Save B
        │               │
        ▼               ▼
 Expected 5         Expected 5
 Persisted 5        Persisted 6
        │               │
        ▼               ▼
     Commit           Conflict
```

El resultado final mantiene únicamente la modificación confirmada
sobre la versión esperada válida.

---

# Escenario — Consulta Concurrente

Múltiples procesos pueden leer simultáneamente:

```text
Proposal Version 10
```

sin producir conflictos.

Las lecturas no modifican Version.

El conflicto aparece únicamente cuando se intenta persistir una
modificación basada en una revisión obsoleta.

---

# Escenario — Modificaciones Secuenciales

```text
Load Version 10

↓

Valid Modification

↓

Save Version 11

↓

Load Version 11

↓

Valid Modification

↓

Save Version 12
```

Cada modificación parte de la última revisión confirmada.

---

# Escenario — Modificación Obsoleta

```text
Load Version 10

↓

Another Process Saves Version 11

↓

Attempt Save with ExpectedVersion 10

↓

Conflict
```

La operación obsoleta no puede sobrescribir Version 11.

---

# Escenario — Command Inválido

```text
Proposal Version 10

↓

Invalid Command

↓

Rejected

↓

Proposal Version 10
```

No existe una nueva revisión.

---

# Escenario — Rehidratación

```text
Persisted Proposal Version 10

↓

Repository.getById()

↓

Rehydrated Proposal Version 10
```

La recuperación conserva exactamente Version.

---

# Escenario — Archived

```text
Proposal Version 20

↓

ArchiveProposal

↓

Proposal Version 21
Status = Archived
```

Posteriores recuperaciones mantienen:

```text
Version = 21

Status = Archived
```

---

# Restricciones

No está permitido:

- modificar Version directamente;
- decrementar Version;
- reiniciar Version;
- incrementar Version por una lectura;
- incrementar Version por rehidratación;
- incrementar Version por una operación rechazada;
- persistir una modificación sin comprobar la versión esperada;
- sobrescribir una versión posterior mediante Last Write Wins;
- utilizar Version para evitar una invariante;
- utilizar Version para evitar una regla de State Machine;
- utilizar Version para evitar Permissions;
- utilizar la Version de un Read Model como autoridad de
  concurrencia del lado de escritura;
- compartir una única Version entre múltiples Proposals;
- utilizar Proposal.Version para modificar otros Aggregates;
- permitir que sistemas externos establezcan directamente
  Proposal.Version.

---

# Compatibilidad con CQRS

En una arquitectura CQRS:

```text
Write Side

Proposal Aggregate

↓

Version

↓

Repository
```

mantiene la autoridad de concurrencia.

El lado de lectura puede proyectar Version, pero no sustituye la
autoridad del lado de escritura.

Conceptualmente:

```text
Write Model Version

≠

Read Projection Freshness
```

---

# Compatibilidad con Event Sourcing

El modelo de Version es compatible con Event Sourcing.

Cuando Proposal se reconstruye mediante eventos históricos:

```text
Event Stream

↓

Replay

↓

Proposal
```

la revisión resultante debe corresponder al historial persistido.

El replay no constituye nuevas modificaciones y no publica
nuevamente los eventos históricos.

---

# Compatibilidad con Event-Driven Architecture

Version puede acompañar Domain Events o Integration Events cuando
sus contratos requieran información sobre la revisión del
Aggregate.

Sin embargo, el consumidor externo no obtiene autoridad para
modificar Version.

La autoridad permanece dentro del límite de Proposal.

---

# Compatibilidad con Clean Architecture

Las reglas de Version pertenecen al dominio y a los contratos
correspondientes.

La implementación técnica de comparación y persistencia pertenece
a Infrastructure.

Debe mantenerse:

```text
Domain Rule

↓

ExpectedVersion Semantics
```

```text
Infrastructure

↓

Technical Enforcement
```

La dependencia arquitectónica permanece orientada hacia el
dominio.

---

# Compatibilidad con DDD

El versionado protege la regla fundamental de que Proposal
constituye una unidad de consistencia.

Una modificación concurrente no puede romper silenciosamente las
invariantes del Aggregate.

Version permite mantener:

- identidad estable;
- consistencia interna;
- invariantes;
- transiciones válidas;
- persistencia coherente;
- aislamiento entre Aggregates.

---

# Principios Arquitectónicos

El modelo de Version mantiene:

```text
ProposalId

≠

Version
```

```text
Valid Modification

=

Version Increment
```

```text
Rejected Operation

=

No Version Increment
```

```text
Read

=

No Version Increment
```

```text
Rehydration

=

No Version Increment
```

```text
ExpectedVersion
    =
PersistedVersion

→

Write May Proceed
```

```text
ExpectedVersion
    ≠
PersistedVersion

→

Concurrency Conflict
```

```text
Concurrency Conflict

≠

Last Write Wins
```

```text
Permission Granted

≠

Version Valid
```

```text
Version Valid

≠

Invariant Valid
```

```text
Version Valid

≠

State Transition Valid
```

```text
Proposal Version

≠

External System Version
```

```text
Proposal Version

≠

Read Model Authority
```

```text
Proposal Version

≠

Other Aggregate Version
```

---

# Documentación Complementaria

El modelo de versionado debe interpretarse conjuntamente con:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007D-Domain-Events.md

DOMAIN-007E-Invariants.md

DOMAIN-007F-Permissions.md

DOMAIN-007G-Repository-Contract.md

DOMAIN-007H-Examples.md

DOMAIN-007J-Consistency-Boundary.md

DOMAIN-007K-Integration-Events.md

DOMAIN-007L-Read-Model.md

DOMAIN-007M-Test-Scenarios.md

DOMAIN-007N-Performance-Rules.md

DOMAIN-007O-Security-Model.md

DOMAIN-007P-Extension-Points.md
```

Estos documentos desarrollan responsabilidades complementarias
sin alterar la regla de que Version pertenece al Aggregate
Proposal y protege su propia evolución lógica.

---

# Definición de Éxito

El modelo de versionado del Aggregate **Proposal** garantiza que
cada instancia mantenga una revisión lógica explícita,
monotónicamente creciente y protegida contra modificaciones
concurrentes incompatibles.

Cada modificación válida produce:

```text
Previous Version

↓

Valid Domain Modification

↓

New Version
```

mientras una operación rechazada mantiene:

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

La persistencia utiliza:

```text
ExpectedVersion
```

y:

```text
PersistedVersion
```

para garantizar que una modificación únicamente pueda ser
confirmada cuando fue evaluada sobre la revisión actualmente
persistida.

Cuando:

```text
ExpectedVersion
    ≠
PersistedVersion
```

la escritura es rechazada explícitamente, evitando pérdida de
actualizaciones y sobrescrituras silenciosas.

De esta forma, Version protege el límite de consistencia de
Proposal, preserva sus invariantes, mantiene la coherencia entre
estado y persistencia y permite que el Aggregate evolucione de
forma segura dentro de la arquitectura DDD distribuida de AURA
Core, sin introducir dependencias tecnológicas ni extender su
responsabilidad hacia otros Aggregates.