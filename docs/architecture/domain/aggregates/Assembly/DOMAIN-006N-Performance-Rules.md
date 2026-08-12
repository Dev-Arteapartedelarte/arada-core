# DOMAIN-006N — Assembly Performance Rules

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Assembly Management

Aggregate:
Assembly

Documentos relacionados:

* DOMAIN-006-Aggregate.md
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
* CORE-008-Aggregate-Design-Rules.md
* CORE-011-Repository-Contracts.md

---

# Objetivo

Definir las reglas conceptuales de rendimiento aplicables al
Aggregate **Assembly** sin alterar su modelo de dominio, sus
invariantes, su Consistency Boundary ni sus responsabilidades.

Las reglas de rendimiento establecen los principios que deben
respetarse cuando la implementación de Assembly requiera optimizar:

* escritura;
* recuperación del Aggregate;
* concurrencia;
* publicación de eventos;
* consultas;
* Read Models;
* integración;
* reconstrucción de proyecciones;
* procesamiento de grandes volúmenes de información.

El rendimiento nunca constituye una justificación para romper las
reglas del dominio.

Debe mantenerse:

```text
Performance Optimization
    ≠
Domain Model Redesign
```

cuando la optimización modifica exclusivamente aspectos técnicos.

---

# Propósito

El propósito de estas reglas es permitir que Assembly pueda
evolucionar hacia escenarios de mayor carga y volumen manteniendo
intactos los principios arquitectónicos definidos para AURA Core.

Las optimizaciones deben respetar:

* Aggregate Root;
* identidad;
* Lifecycle;
* State Machine;
* Commands;
* Domain Events;
* invariantes;
* Permissions;
* Repository Contract;
* Versioning;
* Consistency Boundary;
* Integration Events;
* Read Models.

La necesidad de mejorar tiempos de respuesta, capacidad de
procesamiento o volumen de consultas no permite trasladar
responsabilidades entre Aggregates.

---

# Principio Fundamental

Debe mantenerse:

```text
Correct Domain Model
    before
Performance Optimization
```

Una optimización es válida únicamente cuando preserva la semántica
del dominio.

No está permitido modificar una regla de negocio simplemente para
reducir:

* consultas;
* tiempo de procesamiento;
* cantidad de persistencias;
* cantidad de eventos;
* tamaño de una respuesta;
* complejidad de infraestructura.

---

# Regla de Prioridad del Dominio

Ante un conflicto entre:

```text
Performance
```

y:

```text
Domain Invariant
```

prevalece:

```text
Domain Invariant
```

Ante un conflicto entre:

```text
Performance
```

y:

```text
Consistency Boundary
```

prevalece:

```text
Consistency Boundary
```

Ante un conflicto entre:

```text
Performance
```

y:

```text
Valid State Transition
```

prevalece:

```text
Valid State Transition
```

---

# Responsabilidad

Las Performance Rules son responsables de establecer límites para
que las optimizaciones técnicas no alteren el comportamiento
conceptual de Assembly.

Estas reglas deben preservar:

* corrección del dominio;
* consistencia interna;
* aislamiento del Aggregate;
* independencia tecnológica;
* separación entre escritura y lectura;
* concurrencia optimista;
* comunicación mediante eventos;
* autonomía de otros Aggregates.

---

# Responsabilidades Fuera de este Documento

Este documento no define:

* infraestructura concreta;
* base de datos concreta;
* tamaño de servidores;
* cantidad de CPU;
* cantidad de memoria;
* configuración de contenedores;
* topología de despliegue;
* proveedor Cloud;
* sistema de caché específico;
* motor de búsqueda específico;
* broker específico;
* índices físicos;
* configuración de red;
* límites HTTP;
* políticas de autoscaling.

Estas decisiones pertenecen a Infrastructure y operación.

---

# Rendimiento y Aggregate Root

La única Aggregate Root continúa siendo:

```text
Assembly
```

Una necesidad de rendimiento no permite crear nuevas Aggregate
Roots dentro de Assembly únicamente para reducir el costo de una
operación.

Debe mantenerse:

```text
Performance Requirement
    ≠
New Aggregate Root
```

La definición del Aggregate permanece gobernada por consistencia
del dominio.

---

# Rendimiento y Consistency Boundary

El Consistency Boundary definido en:

```text
DOMAIN-006J-Consistency-Boundary.md
```

no puede ampliarse por conveniencia de rendimiento.

Tampoco puede reducirse artificialmente si ello rompe una
invariante que debe mantenerse dentro de Assembly.

Debe mantenerse:

```text
Aggregate Boundary
    =
Domain Consistency Decision
```

No:

```text
Aggregate Boundary
    =
Database Performance Decision
```

---

# Regla de No Absorción por Rendimiento

No está permitido incorporar dentro de Assembly:

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

únicamente para evitar consultas o comunicaciones entre
Aggregates.

Debe mantenerse:

```text
Fewer Queries
    ≠
Reason to Merge Aggregates
```

---

# Regla de No Fragmentación por Rendimiento

Los conceptos internos que requieren consistencia conjunta no deben
separarse en Aggregates independientes únicamente para obtener
persistencias menores.

La decisión de separación corresponde al modelo del dominio.

No al tamaño físico de los datos.

---

# Escritura

Toda operación de escritura sobre Assembly debe continuar
ejecutándose mediante el Aggregate Root.

Conceptualmente:

```text
Command

↓

Assembly

↓

Domain Validation

↓

State Change

↓

Domain Events
```

Una optimización no puede omitir este flujo para escribir
directamente sobre estructuras persistidas.

---

# Regla de Escritura

No está permitido:

```text
Direct Database Update
```

para modificar atributos de Assembly evitando:

* Aggregate Root;
* State Machine;
* Guards;
* invariantes;
* Versioning;
* Domain Events.

Debe mantenerse:

```text
Write Optimization
    ≠
Bypass Domain Model
```

---

# Escrituras Parciales

El Repository puede utilizar la estrategia técnica que corresponda
para persistencia.

Sin embargo, desde la perspectiva del dominio, la modificación
continúa representando una única unidad consistente.

Debe mantenerse:

```text
Physical Persistence Strategy
    ≠
Domain Consistency Boundary
```

---

# Atomicidad

Una optimización de escritura no puede producir estados
parcialmente confirmados.

Si una operación modifica internamente varios conceptos:

```text
AssemblyStatus

Schedule

Convocation

Location

Version
```

cuando corresponda, el resultado confirmado debe conservar todas
las invariantes aplicables.

---

# Rendimiento y Commands

Los Commands definidos en:

```text
DOMAIN-006C-Commands.md
```

continúan siendo las intenciones oficiales de modificación.

Una necesidad de rendimiento no permite sustituir varios Commands
semánticamente diferentes por una operación técnica ambigua que
oculte los hechos del dominio.

Debe mantenerse:

```text
Command
    =
Explicit Domain Intention
```

---

# Command Batch

La agrupación técnica de solicitudes no convierte múltiples
modificaciones de dominio en una única operación conceptual.

Cada intención debe mantener:

* validación correspondiente;
* Permission correspondiente;
* estado válido;
* invariantes;
* Versioning;
* eventos correspondientes.

---

# Rendimiento y State Machine

La State Machine definida en:

```text
DOMAIN-006B-State-Machine.md
```

no puede omitirse para acelerar una operación.

No está permitido pasar directamente:

```text
Draft
```

a:

```text
InProgress
```

si el modelo requiere transiciones intermedias.

Debe mantenerse:

```text
Faster Transition
    ≠
Valid Transition
```

---

# Rendimiento e Invariantes

Las invariantes definidas en:

```text
DOMAIN-006E-Invariants.md
```

deben evaluarse siempre que correspondan.

Una optimización no puede asumir que una invariante es válida sin
la información necesaria para comprobarla.

---

# Invariantes Temporales

Reglas como:

```text
ScheduledEnd
    >=
ScheduledStart
```

cuando corresponda, deben mantenerse independientemente de la
estrategia de persistencia o lectura.

No puede confirmarse un estado inválido para reducir procesamiento.

---

# Rendimiento y Permissions

Los Permissions definidos en:

```text
DOMAIN-006F-Permissions.md
```

no pueden omitirse por razones de rendimiento.

Debe mantenerse:

```text
Authorization Cost
    ≠
Reason to Skip Authorization
```

La optimización de autorización pertenece a las capas
correspondientes.

La semántica del Permission permanece intacta.

---

# Rendimiento y Versioning

Assembly utiliza Versioning conforme a:

```text
DOMAIN-006I-Versioning.md
```

Una optimización no puede eliminar el control de Version para
evitar conflictos de concurrencia.

Debe mantenerse:

```text
ExpectedVersion
    =
PersistedVersion
```

como condición aplicable al modelo de concurrencia establecido.

---

# Concurrencia Optimista

El modelo utiliza concurrencia optimista para proteger Assembly
frente a modificaciones incompatibles.

Este mecanismo permite evitar bloqueos de dominio prolongados sin
sacrificar la protección contra sobrescrituras concurrentes.

Una colisión válida debe resolverse como conflicto.

No como sobrescritura silenciosa.

---

# Conflicto de Concurrencia

Debe evitarse:

```text
Last Write Wins
```

cuando ello omite la validación de Version establecida para el
Aggregate.

Si:

```text
ExpectedVersion
    ≠
PersistedVersion
```

la modificación incompatible debe ser rechazada conforme al modelo
oficial.

---

# Reintentos

Un conflicto de concurrencia puede requerir que la operación sea
evaluada nuevamente sobre el estado actualizado.

El retry técnico no puede reutilizar ciegamente una decisión
calculada sobre un estado anterior.

Debe mantenerse:

```text
Retry
    ≠
Ignore Version Conflict
```

---

# Repository

El Repository definido en:

```text
DOMAIN-006G-Repository-Contract.md
```

debe preservar el contrato del Aggregate independientemente de las
optimizaciones de persistencia.

El Repository puede ser implementado mediante diferentes
tecnologías.

No puede modificar la semántica de Assembly.

---

# Recuperación del Aggregate

Una operación de escritura debe disponer de la información
necesaria para reconstruir un estado válido de Assembly antes de
ejecutar comportamiento del dominio.

No debe utilizarse una representación parcial que impida proteger
las invariantes necesarias para la operación.

---

# Carga Parcial

La carga parcial es una decisión técnica y solo puede utilizarse
cuando preserve íntegramente las reglas requeridas por la operación
del dominio.

No puede producir:

```text
Partially Known Aggregate

↓

Domain Decision
```

si la información omitida participa en una invariante relevante.

---

# Lazy Loading

El Lazy Loading no debe utilizarse para introducir referencias
mutables implícitas hacia otros Aggregates.

Debe mantenerse:

```text
Assembly
    references
AggregateId
```

No:

```text
Assembly
    transparently owns
External Aggregate
```

La optimización de acceso no puede cambiar relaciones de dominio.

---

# Persistencia Física

La forma física de persistir Assembly puede optimizarse.

Sin embargo:

```text
Database Schema
    ≠
Aggregate Model
```

Una tabla, colección, documento o conjunto de estructuras físicas
no redefine las fronteras del Aggregate.

---

# Índices

Los mecanismos de almacenamiento pueden utilizar optimizaciones de
consulta sobre los atributos necesarios.

La existencia de un índice físico:

* no crea una invariante;
* no crea una relación de dominio;
* no crea una Aggregate Root;
* no modifica el Lifecycle;
* no modifica la State Machine.

Los índices pertenecen a Infrastructure.

---

# Read Model

Las consultas intensivas deben resolverse utilizando el modelo de
lectura definido en:

```text
DOMAIN-006L-Read-Model.md
```

cuando corresponda.

Debe evitarse utilizar el Aggregate Root como estructura de
consulta masiva.

---

# Principio de Separación de Lectura

Debe mantenerse:

```text
High Read Volume

↓

Read Model
```

No:

```text
High Read Volume

↓

Load Aggregate Repeatedly
```

cuando la consulta pueda resolverse mediante una proyección
oficial.

---

# Read Models y Rendimiento

Los Read Models están destinados a permitir:

* lecturas masivas;
* filtros;
* búsquedas;
* ordenamiento;
* agregaciones;
* visualización;
* consultas especializadas.

Estas optimizaciones no modifican Assembly.

---

# Desnormalización

Los Read Models pueden desnormalizar información conforme al modelo
oficial de lectura.

Debe mantenerse:

```text
Read Model Denormalization
    ≠
Aggregate Denormalization
```

La duplicación controlada de información para consulta no convierte
esa información en estado autoritativo del Aggregate.

---

# Proyecciones

Las proyecciones oficiales definidas en:

```text
DOMAIN-006L-Read-Model.md
```

pueden optimizar diferentes necesidades de consulta.

La existencia de múltiples proyecciones evita introducir
responsabilidades de lectura dentro del Write Model.

---

# Fuente de Verdad

Las optimizaciones de lectura no modifican la fuente oficial de
verdad.

Debe mantenerse:

```text
Assembly Aggregate
+
Domain Events
```

como fuente oficial definida para el modelo.

Los Read Models continúan siendo reconstruibles.

---

# Caché

Una representación temporal utilizada para acelerar consultas no
modifica la autoridad del dominio.

Debe mantenerse:

```text
Cached Representation
    ≠
Source of Truth
```

Una representación de lectura desactualizada no puede utilizarse
para sobrescribir Assembly.

---

# Consistencia Eventual

Los Read Models pueden encontrarse temporalmente detrás del Write
Model.

Debe mantenerse:

```text
Projection Delay
    ≠
Aggregate Inconsistency
```

El retraso de una proyección es aceptable dentro del modelo de
consistencia eventual establecido para lectura.

---

# Rendimiento y Consistencia

La búsqueda de menor latencia no puede convertir una regla de
consistencia fuerte interna en consistencia eventual.

Dentro de Assembly debe mantenerse:

```text
Strong Consistency
```

para las invariantes propias del Aggregate.

Entre Aggregates puede mantenerse:

```text
Eventually Consistent
```

conforme al Consistency Boundary oficial.

---

# No Transacciones Distribuidas por Optimización

No debe ampliarse una transacción para incluir múltiples Aggregates
con el objetivo de evitar eventos o simplificar sincronización.

Debe mantenerse:

```text
One Aggregate
    =
One Consistency Boundary
```

para Assembly.

---

# Domain Events

Los Domain Events definidos en:

```text
DOMAIN-006D-Domain-Events.md
```

deben producirse conforme a hechos válidamente confirmados.

Una optimización no puede eliminar un Domain Event requerido por el
modelo únicamente para reducir procesamiento.

---

# Publicación de Domain Events

La estrategia técnica utilizada para manejar Domain Events debe
preservar:

* orden semántico cuando corresponda;
* identidad del hecho;
* relación con la modificación confirmada;
* trazabilidad;
* consistencia del modelo.

La estrategia técnica concreta pertenece a Infrastructure.

---

# No Evento por Lectura

Una optimización de observabilidad o métricas no debe convertir una
consulta ordinaria en un Domain Event del Aggregate.

Debe mantenerse:

```text
Read
    ≠
Domain State Change
```

---

# Integration Events

Los Integration Events definidos en:

```text
DOMAIN-006K-Integration-Events.md
```

permiten desacoplar Assembly de otros sistemas.

El procesamiento externo puede realizarse fuera de la transacción
del Aggregate.

Esto permite mantener:

```text
Assembly Commit
```

separado de:

```text
External Consumer Processing
```

---

# Consumidores Externos

Assembly no debe esperar que todos los consumidores externos hayan
completado su procesamiento para considerar válido un estado ya
confirmado.

Ejemplo:

```text
AssemblyCompleted
```

puede haber ocurrido válidamente aunque:

```text
Document

Notification

Audit
```

todavía no hayan procesado las consecuencias correspondientes.

---

# Fallo de Consumidor

Un fallo de un consumidor externo:

```text
Consumer Failure
```

no debe obligar a mantener abierta la transacción del Aggregate.

Debe mantenerse:

```text
Consumer Failure
    ≠
Assembly Transaction Failure
```

cuando el hecho interno ya fue válidamente confirmado.

---

# Integración y Rendimiento

La comunicación con:

* sistemas municipales;
* plataformas ciudadanas;
* sistemas Smart City;
* FIWARE;
* otros sistemas externos;

permanece fuera del Aggregate.

Assembly no debe realizar llamadas directas a estos sistemas dentro
de su comportamiento de dominio.

---

# Integraciones Lentas

La latencia de un sistema externo no debe mantener bloqueada la
consistencia interna de Assembly.

Conceptualmente:

```text
Assembly

↓

Domain Event

↓

Integration Event

↓

External System
```

preserva el desacoplamiento temporal.

---

# FIWARE

La generación o actualización de representaciones FIWARE pertenece
a Integration.

No debe añadirse procesamiento NGSI-LD dentro de Assembly con el
objetivo de reducir pasos de integración.

Debe mantenerse:

```text
Assembly Domain Processing
    ≠
FIWARE Processing
```

---

# Sistemas Municipales

La latencia o disponibilidad de una plataforma municipal no puede
convertirse en una dependencia directa de las invariantes internas
de Assembly salvo que una regla de dominio oficial establezca una
precondición externa previamente resuelta.

Assembly no realiza directamente la integración técnica.

---

# Eventos y Volumen

El aumento del número de eventos no justifica fusionar hechos
semánticamente distintos.

Debe mantenerse:

```text
Domain Meaning
    before
Event Count Reduction
```

Un evento representa un hecho de dominio.

No una optimización de transporte.

---

# Event Sourcing

Cuando la implementación utilice Event Sourcing, la reconstrucción
del Aggregate debe preservar exactamente el mismo estado conceptual
que el modelo oficial.

Una estrategia de optimización de rehidratación no modifica:

* Domain Events;
* Lifecycle;
* State Machine;
* invariantes;
* Version;
* Aggregate Boundary.

---

# Replay

El Replay de eventos no debe ejecutar nuevamente efectos externos
como si fueran nuevos hechos.

Debe mantenerse:

```text
Historical Replay
    ≠
New Domain Operation
```

---

# Snapshot

Cuando una implementación compatible con Event Sourcing utilice
mecanismos técnicos para acelerar rehidratación, dichos mecanismos
no modifican la fuente conceptual del dominio.

Debe mantenerse:

```text
Rehydration Optimization
    ≠
New Source of Truth
```

La estrategia concreta pertenece a Infrastructure.

---

# Read Model Reconstruction

La reconstrucción definida en:

```text
DOMAIN-006L-Read-Model.md
```

puede procesarse independientemente del Write Model.

Reconstruir una proyección:

* no modifica Assembly;
* no incrementa Version;
* no ejecuta Commands;
* no genera nuevas transiciones de dominio.

---

# Reconstruction Performance

Una necesidad de acelerar la reconstrucción del Read Model no puede
modificar la semántica de los Domain Events históricos.

Los hechos históricos permanecen inmutables.

---

# Rendimiento y Test Scenarios

Las optimizaciones deben continuar cumpliendo:

```text
DOMAIN-006M-Test-Scenarios.md
```

Una optimización que hace fallar un escenario conceptual válido
debe considerarse incompatible con el modelo del Aggregate.

---

# Regla de Regresión

Toda optimización debe preservar:

* comportamiento válido;
* comportamiento de rechazo;
* invariantes;
* State Machine;
* Versioning;
* Domain Events;
* Permissions;
* Consistency Boundary.

Debe mantenerse:

```text
Optimization

↓

Same Domain Semantics
```

---

# Optimización de Lecturas

Las necesidades de lectura deben resolverse preferentemente fuera
del Write Model cuando no requieren comportamiento del Aggregate.

Debe mantenerse:

```text
Query Requirement

↓

Read Model
```

cuando corresponda.

No debe agregarse estado interno a Assembly únicamente para
facilitar una consulta.

---

# Optimización de Escrituras

Las optimizaciones del Write Model deben preservar siempre:

```text
Command

↓

Aggregate Root

↓

Invariants

↓

State Transition

↓

Version

↓

Domain Events
```

La implementación puede optimizar los mecanismos alrededor de este
flujo.

No puede eliminar su semántica.

---

# Optimización de Relaciones

Las relaciones con otros Aggregates deben continuar mediante
identificadores.

Ejemplos:

```text
OrganizationId

TerritoryId

MembershipId

CitizenId

ProposalId

ParticipationId

VotingId

DocumentId

NotificationId

AuditId
```

cuando correspondan al modelo oficial.

No debe copiarse un Aggregate completo dentro de Assembly para
evitar una consulta.

---

# Datos Externos para Decisiones

Cuando una operación de dominio requiere información perteneciente
a otro Aggregate, dicha información debe resolverse conforme a los
límites establecidos.

Una necesidad de reducir accesos no permite introducir el estado
mutable del otro Aggregate dentro de Assembly.

---

# Información Derivada

La información utilizada únicamente para:

* dashboards;
* estadísticas;
* búsquedas;
* reportes;
* visualizaciones;

debe mantenerse fuera del Write Model cuando no participe en las
invariantes propias de Assembly.

Los Read Models constituyen el mecanismo conceptual establecido
para estas necesidades de lectura.

---

# Estadísticas

Las estadísticas relacionadas con Assembly no deben almacenarse
dentro del Aggregate únicamente para acelerar dashboards si no
forman parte de sus invariantes.

Debe mantenerse:

```text
Analytics
    ≠
Aggregate State
```

---

# Dashboards

Los dashboards deben consumir modelos de lectura.

No deben cargar y modificar Aggregates para obtener indicadores.

Debe mantenerse:

```text
Dashboard
    ≠
Write Model
```

---

# Reporting

Los reportes pueden combinar información de distintos Aggregates.

Esto no justifica ampliar Assembly.

Debe mantenerse:

```text
Reporting Requirement
    ≠
Aggregate Ownership
```

---

# Búsquedas

Las búsquedas no deben ejecutarse mediante comportamiento del
Aggregate.

La necesidad de localizar Assemblies pertenece al lado de lectura.

Assembly continúa siendo recuperado mediante su identidad para
operaciones del Write Model conforme al Repository Contract.

---

# Paginación

Las necesidades de paginación pertenecen a las consultas y Read
Models.

No forman parte del Aggregate.

Una necesidad de paginación no modifica:

* AssemblyId;
* Lifecycle;
* State Machine;
* Version;
* invariantes.

---

# Ordenamiento

El ordenamiento de resultados pertenece al modelo de lectura.

No debe incorporarse ordenamiento de colecciones externas dentro de
Assembly únicamente para satisfacer una interfaz.

---

# Filtros

Los filtros utilizados para consultar Assemblies pertenecen al Read
Model.

No constituyen reglas del Aggregate salvo que una definición
explícita del dominio así lo establezca.

---

# Agregaciones

Las agregaciones para análisis pertenecen al lado de lectura.

No deben introducirse dentro del Write Model únicamente para
acelerar consultas analíticas.

---

# Rendimiento y UI

La necesidad de renderizar rápidamente una interfaz no redefine
Assembly.

Debe mantenerse:

```text
UI Performance Requirement
    ≠
Aggregate Boundary
```

Las interfaces consumen representaciones apropiadas de lectura.

---

# Rendimiento y API

La forma en que una API responde a un cliente no redefine el
Aggregate.

Debe mantenerse:

```text
API Payload Optimization
    ≠
Domain Model Optimization
```

Las respuestas pueden utilizar Read Models o contratos externos sin
convertirlos en estado interno de Assembly.

---

# Rendimiento e Infrastructure

Las decisiones de Infrastructure pueden optimizar:

* persistencia;
* lectura;
* transporte;
* serialización;
* comunicación;
* almacenamiento;
* disponibilidad.

Estas optimizaciones deben permanecer fuera del modelo de dominio
cuando no expresen reglas de negocio.

---

# Independencia Tecnológica

Las Performance Rules conceptuales de Assembly no dependen de:

```text
PostgreSQL

MongoDB

MySQL

SQLite

Redis

Elasticsearch

OpenSearch

Kafka

RabbitMQ

NATS

HTTP

GraphQL

gRPC

Docker

Kubernetes
```

La elección de tecnología pertenece a Infrastructure.

---

# Frameworks

Assembly no debe modificarse para acomodar limitaciones o
características particulares de:

```text
Django

FastAPI

Flask

React

Next.js
```

u otros Frameworks.

Debe mantenerse:

```text
Framework Constraint
    ≠
Domain Rule
```

---

# Base de Datos

La elección de base de datos no modifica:

* Aggregate Root;
* identidad;
* Lifecycle;
* State Machine;
* invariantes;
* Version;
* eventos;
* relaciones.

Debe mantenerse:

```text
Database Choice
    ≠
Domain Architecture
```

---

# Rendimiento y Escalabilidad

Assembly debe poder escalar preservando la autonomía del Aggregate.

El aumento del número de Assemblies no modifica el hecho de que
cada Assembly constituye su propia unidad de consistencia.

Conceptualmente:

```text
Assembly A
    =
Consistency Boundary A

Assembly B
    =
Consistency Boundary B

Assembly N
    =
Consistency Boundary N
```

Una Assembly no comparte estado mutable interno con otra Assembly.

---

# Concurrencia entre Assemblies

Operaciones sobre Assemblies diferentes no deben convertirlas en
una única unidad de consistencia únicamente para facilitar
procesamiento.

Cada Assembly mantiene:

```text
AssemblyId

Version

State

Invariants
```

propios.

---

# Escalado de Lectura

El escalado de lectura debe aprovechar la separación establecida
por los Read Models.

El Write Model no debe convertirse en el mecanismo principal para
resolver grandes volúmenes de consultas.

---

# Escalado de Integración

La incorporación de nuevos consumidores de Integration Events no
debe requerir ampliar Assembly.

Debe mantenerse:

```text
New Consumer
    ≠
New Aggregate Responsibility
```

---

# Observabilidad

La medición técnica de rendimiento puede observar:

* duración de operaciones;
* tiempos de persistencia;
* tiempos de proyección;
* tiempos de procesamiento de eventos;
* latencia de integración;
* volumen de consultas.

Estas métricas no forman parte del estado del Aggregate.

---

# Métricas Técnicas

Las métricas técnicas no deben incorporarse como propiedades de
Assembly únicamente para observabilidad.

Debe mantenerse:

```text
Operational Metric
    ≠
Domain State
```

salvo que una métrica sea explícitamente definida en el futuro como
concepto real del dominio.

---

# Logging

El logging técnico pertenece a Infrastructure.

No sustituye:

```text
Domain Events
```

ni:

```text
Audit
```

Cada concepto mantiene su responsabilidad.

---

# Audit

Audit permanece fuera de Assembly.

La necesidad de auditar operaciones no justifica almacenar grandes
colecciones de registros de Audit dentro del Aggregate.

Debe mantenerse:

```text
Audit History
    ≠
Assembly Internal Collection
```

---

# Regla de Memoria

Assembly debe representar únicamente el estado necesario para
proteger su propia consistencia.

No debe cargar colecciones de otros Aggregates únicamente por
conveniencia.

La cantidad de datos internos debe estar determinada por el modelo
del dominio.

---

# Colecciones Externas

No deben incorporarse como colecciones internas de Assembly:

```text
Citizens[]

Memberships[]

Proposals[]

Participations[]

Votings[]

Documents[]

Notifications[]

Audits[]
```

si estos conceptos corresponden a Aggregates independientes.

---

# Relaciones de Alta Cardinalidad

Una relación potencialmente numerosa con otros Aggregates debe
mantenerse fuera del Boundary cuando esos conceptos posean
identidad y consistencia propias.

El volumen de la relación refuerza la necesidad de respetar los
límites establecidos.

No autoriza su absorción.

---

# Regla de No Duplicación Autoritativa

Puede existir información desnormalizada en Read Models.

No debe existir una segunda copia autoritativa mutable del estado de
Assembly fuera del Write Model.

Debe mantenerse:

```text
Projection Copy
    =
Derived
```

No:

```text
Projection Copy
    =
Independent Source of Truth
```

---

# Regla de No Optimización Prematura del Dominio

El modelo conceptual no debe complicarse por anticipar problemas de
rendimiento no pertenecientes al dominio.

Las optimizaciones técnicas se introducen fuera del Aggregate
cuando sea posible.

La arquitectura debe preservar primero:

* claridad;
* invariantes;
* cohesión;
* límites;
* semántica.

---

# Regla de Optimización Controlada

Toda optimización debe poder responder:

```text
What is being optimized?
```

sin cambiar la respuesta a:

```text
What does Assembly mean?
```

Si la optimización cambia el significado del Aggregate, deja de ser
una optimización técnica y pasa a constituir una decisión de
dominio que debe definirse explícitamente en la fuente conceptual
oficial.

---

# Escenario — Consulta Masiva

```text
Given

se requiere consultar un conjunto amplio de Assemblies

When

la necesidad corresponde exclusivamente a lectura

Then

la consulta utiliza los Read Models correspondientes

And

no requiere cargar cada Aggregate para ejecutar lógica de lectura
```

---

# Escenario — Modificación Individual

```text
Given

se requiere modificar una Assembly específica

When

el Command es ejecutado

Then

se recupera la Assembly correspondiente conforme al Repository
Contract

And

la operación se ejecuta mediante la Aggregate Root

And

se preservan las invariantes

And

se valida Version
```

---

# Escenario — Consulta no Incrementa Version

```text
Given

Assembly Version igual a N

When

se realizan múltiples consultas sobre Read Models

Then

Assembly Version permanece N
```

---

# Escenario — Optimización no Evita Invariante

```text
Given

una operación que produciría ScheduledEnd anterior a ScheduledStart

When

una implementación intenta reducir validaciones

Then

la operación continúa siendo rechazada

And

la optimización no puede omitir la invariante
```

---

# Escenario — Optimización no Evita State Machine

```text
Given

una Assembly en Draft

When

se intenta iniciar directamente la Assembly

Then

la transición continúa siendo rechazada

And

la optimización no puede omitir estados requeridos
```

---

# Escenario — Optimización no Evita Permission

```text
Given

un Actor sin Permission requerido

When

intenta ejecutar un Command

Then

la operación continúa siendo rechazada

And

la necesidad de menor latencia no modifica la autorización
```

---

# Escenario — Optimización no Evita Versioning

```text
Given

ExpectedVersion distinta de PersistedVersion

When

se intenta confirmar una modificación

Then

la operación es rechazada

And

no se utiliza sobrescritura silenciosa para reducir conflictos
```

---

# Escenario — Read Model Desactualizado

```text
Given

Assembly se encuentra en Version N

And

Read Model todavía representa Version N-1

When

se consulta la proyección

Then

puede existir temporalmente información anterior

And

la proyección no modifica Assembly

And

no se utiliza como autoridad para persistir cambios
```

---

# Escenario — Consumidor Lento

```text
Given

AssemblyCompleted fue confirmado

And

se produjo el contrato de integración correspondiente

When

un consumidor externo procesa lentamente el evento

Then

Assembly permanece Completed

And

la transacción del Aggregate no permanece abierta esperando al
consumidor
```

---

# Escenario — Sistema Externo No Disponible

```text
Given

un hecho válido de Assembly debe ser comunicado externamente

When

el sistema externo no se encuentra disponible

Then

la indisponibilidad externa no redefine el estado válido ya
confirmado de Assembly
```

---

# Escenario — Vista Compuesta

```text
Given

una interfaz necesita mostrar:

Assembly

Proposal

Voting

Document

When

se construye la vista

Then

la información puede componerse desde modelos de lectura
independientes

And

los Aggregates permanecen separados
```

---

# Escenario — Alto Volumen de Proposals

```text
Given

una Assembly relacionada con múltiples Proposals

When

la cantidad de Proposals aumenta

Then

Proposal continúa fuera del Consistency Boundary de Assembly

And

el volumen no convierte Proposal en entidad interna de Assembly
```

---

# Escenario — Alto Volumen de Participants

```text
Given

una Assembly relacionada con múltiples procesos de Participation

When

el volumen aumenta

Then

Participation continúa bajo su propio Aggregate

And

Assembly no incorpora toda la información de Participation dentro
de su estado
```

---

# Escenario — Alto Volumen de Documents

```text
Given

una Assembly relacionada con múltiples Documents

When

la cantidad de Documents aumenta

Then

Document continúa fuera de Assembly

And

el contenido documental no se incorpora al Aggregate para acelerar
consultas
```

---

# Pruebas de Rendimiento y Dominio

Las pruebas técnicas de rendimiento pueden medir comportamiento de
la implementación.

Sin embargo, toda optimización debe continuar superando los
escenarios conceptuales definidos en:

```text
DOMAIN-006M-Test-Scenarios.md
```

Las pruebas de rendimiento no sustituyen las pruebas de dominio.

---

# Regla de No Regresión

Después de una optimización deben continuar siendo verdaderas todas
las reglas documentadas para Assembly.

No debe producirse regresión en:

* identidad;
* Lifecycle;
* State Machine;
* Commands;
* Domain Events;
* invariantes;
* Permissions;
* Repository Contract;
* Versioning;
* Consistency Boundary;
* Integration Events;
* Read Models.

---

# Restricciones

No está permitido:

* modificar el Aggregate directamente desde Infrastructure para
  mejorar rendimiento;
* omitir Commands;
* omitir State Machine;
* omitir invariantes;
* omitir Permissions;
* omitir Versioning;
* sobrescribir conflictos concurrentes silenciosamente;
* ampliar el Consistency Boundary para reducir consultas;
* absorber otros Aggregates para evitar accesos externos;
* fragmentar Assembly si ello rompe una invariante interna;
* utilizar Read Models como fuente de escritura;
* utilizar proyecciones desactualizadas como autoridad del dominio;
* modificar Domain Events para satisfacer únicamente una
  optimización de transporte;
* mantener transacciones del Aggregate abiertas esperando sistemas
  externos;
* convertir llamadas externas en dependencias directas del dominio;
* introducir FIWARE dentro de Assembly;
* introducir APIs municipales dentro de Assembly;
* incorporar estadísticas dentro del Write Model únicamente para
  dashboards;
* incorporar información de reporting dentro de Assembly;
* utilizar una estructura de base de datos para redefinir el
  Aggregate;
* utilizar un Framework para redefinir las reglas del dominio;
* utilizar una caché como fuente oficial de verdad;
* introducir nuevas reglas de dominio bajo la justificación de
  performance.

---

# Principios Arquitectónicos

Las Performance Rules mantienen:

```text
Domain Correctness
    >
Performance Optimization
```

```text
Aggregate Boundary
    ≠
Database Optimization Boundary
```

```text
Write Model
    ≠
Read Model
```

```text
Aggregate
    ≠
Cache
```

```text
Aggregate
    ≠
Search Index
```

```text
Projection
    ≠
Source of Truth
```

```text
Database Structure
    ≠
Domain Structure
```

```text
External Latency
    ≠
Aggregate Transaction
```

```text
Consumer Failure
    ≠
Aggregate Rollback
```

```text
High Cardinality Relationship
    ≠
Aggregate Ownership
```

```text
Fewer Queries
    ≠
Reason to Merge Aggregates
```

```text
Higher Throughput
    ≠
Reason to Skip Invariants
```

```text
Lower Latency
    ≠
Reason to Skip Permissions
```

```text
Concurrent Writes
    ≠
Reason to Ignore Versioning
```

---

# Compatibilidad Arquitectónica

Las Performance Rules de Assembly son compatibles con:

* Domain-Driven Design;
* Aggregate Pattern;
* Clean Architecture;
* Hexagonal Architecture;
* CQRS;
* Event-Driven Architecture;
* Event Sourcing Compatible;
* Optimistic Concurrency;
* arquitectura distribuida;
* consistencia eventual entre Aggregates;
* Read Models reconstruibles.

Estas reglas preservan la independencia tecnológica del dominio.

---

# Relación con DOMAIN-006-Aggregate

`DOMAIN-006-Aggregate.md` constituye la fuente conceptual oficial
del Aggregate Assembly.

Ninguna Performance Rule puede contradecir o sustituir las
definiciones allí establecidas.

El rendimiento debe adaptarse al Aggregate.

El Aggregate no debe deformarse para adaptarse a una optimización
técnica.

---

# Relación con Lifecycle

`DOMAIN-006A-Lifecycle.md` define el ciclo de vida oficial.

Una optimización no puede eliminar estados ni transiciones del
Lifecycle para reducir operaciones.

---

# Relación con State Machine

`DOMAIN-006B-State-Machine.md` define las transiciones permitidas.

Toda estrategia de rendimiento debe continuar respetándolas.

---

# Relación con Commands

`DOMAIN-006C-Commands.md` define las intenciones de modificación.

Las optimizaciones no pueden escribir directamente sobre Assembly
evitando los Commands establecidos.

---

# Relación con Domain Events

`DOMAIN-006D-Domain-Events.md` define hechos consumados.

Una optimización no puede omitir los eventos necesarios para
representar hechos establecidos por el dominio.

---

# Relación con Invariants

`DOMAIN-006E-Invariants.md` define las reglas obligatorias del
Aggregate.

Performance nunca posee prioridad sobre una invariante.

---

# Relación con Permissions

`DOMAIN-006F-Permissions.md` define las capacidades necesarias para
intentar operaciones.

Las optimizaciones no pueden evitar dichas validaciones.

---

# Relación con Repository Contract

`DOMAIN-006G-Repository-Contract.md` define la persistencia del
Aggregate.

Infrastructure puede optimizar su implementación sin modificar el
contrato conceptual.

---

# Relación con Examples

`DOMAIN-006H-Examples.md` representa escenarios conceptuales de
Assembly.

Las optimizaciones deben conservar el comportamiento descrito en
dichos escenarios.

---

# Relación con Versioning

`DOMAIN-006I-Versioning.md` define la concurrencia optimista.

El rendimiento no puede eliminar el control de Version.

---

# Relación con Consistency Boundary

`DOMAIN-006J-Consistency-Boundary.md` define qué debe mantenerse
dentro de Assembly y qué permanece fuera.

Una optimización no puede redefinir este límite.

---

# Relación con Integration Events

`DOMAIN-006K-Integration-Events.md` permite desacoplar Assembly de
consumidores externos.

La comunicación asíncrona o diferida puede mejorar desacoplamiento
operacional sin modificar la semántica del Aggregate.

---

# Relación con Read Model

`DOMAIN-006L-Read-Model.md` constituye el mecanismo conceptual para
representaciones optimizadas de lectura.

Las necesidades de consulta no deben ampliar el Write Model.

---

# Relación con Test Scenarios

`DOMAIN-006M-Test-Scenarios.md` define los escenarios conceptuales
que debe cumplir una implementación válida.

Toda optimización debe preservar estos escenarios.

---

# Regla de Coherencia Documental

Las Performance Rules deben permanecer coherentes con:

```text
DOMAIN-006-Aggregate.md

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
```

Una regla de rendimiento no puede introducir silenciosamente:

* nuevos estados;
* nuevas transiciones;
* nuevos Commands;
* nuevos Domain Events;
* nuevas invariantes;
* nuevos Permissions;
* nuevas entidades internas;
* nuevos Aggregates;
* nuevas relaciones de propiedad;
* nuevos límites de consistencia.

---

# Regla de Evolución

Las estrategias técnicas de rendimiento pueden evolucionar sin
modificar Assembly cuando no alteran el modelo conceptual.

Una nueva optimización debe comprobar que conserva:

* semántica;
* invariantes;
* Lifecycle;
* State Machine;
* Versioning;
* Permissions;
* eventos;
* Consistency Boundary;
* independencia tecnológica.

Si una necesidad de rendimiento exige cambiar una regla de dominio,
dicho cambio no puede incorporarse mediante este documento.

Debe tratarse como una decisión explícita del modelo conceptual de
Assembly.

---

# Definición de Éxito

Las **Performance Rules** del Aggregate **Assembly** establecen los
límites conceptuales dentro de los cuales pueden realizarse
optimizaciones técnicas sin modificar el significado, las reglas o
las responsabilidades del Aggregate.

Assembly continúa siendo la única Aggregate Root de su límite de
consistencia.

Toda modificación continúa ejecutándose mediante comportamiento de
dominio, respetando Commands, State Machine, invariantes,
Permissions y Versioning.

Las optimizaciones de persistencia no pueden convertir estructuras
físicas de almacenamiento en nuevas fronteras del dominio.

Las optimizaciones de consulta deben apoyarse en el Read Model sin
convertir las proyecciones en fuentes transaccionales de verdad.

Los Read Models pueden desnormalizar y optimizar información para
lectura manteniéndose reconstruibles y separados del Write Model.

La consistencia interna de Assembly continúa siendo fuerte.

La coordinación con otros Aggregates y sistemas externos puede
mantener consistencia eventual conforme al Consistency Boundary y
los Integration Events establecidos.

Organization, Territory, Citizen, Membership, Role, Proposal,
Participation, Voting, Document, Notification y Audit permanecen
fuera de Assembly independientemente del volumen de información,
cantidad de relaciones o necesidades de rendimiento.

Las relaciones de alta cardinalidad no justifican absorber otros
Aggregates.

Las necesidades de dashboards, reportes, búsquedas, estadísticas,
filtros, ordenamiento y consultas masivas no justifican ampliar el
Write Model.

Las llamadas a sistemas municipales, Smart City, FIWARE u otras
integraciones permanecen fuera del comportamiento interno del
Aggregate y no deben mantener abierta su transacción.

El control de concurrencia mediante Version continúa protegiendo
Assembly frente a sobrescrituras incompatibles.

Una mejora de rendimiento nunca puede eliminar una invariante,
omitir una transición, evitar un Permission, ignorar Versioning,
publicar un hecho inexistente o modificar directamente otro
Aggregate.

Toda optimización debe producir exactamente la misma semántica de
dominio que la implementación no optimizada.

Debe mantenerse permanentemente:

```text
Optimization

↓

Same Domain Behavior
```

y:

```text
Performance
    never overrides
Domain Correctness
```

De esta forma,
**DOMAIN-006N-Performance-Rules.md** establece las reglas
conceptuales oficiales para permitir la evolución del rendimiento
de Assembly preservando el Aggregate Root, sus invariantes, su
Consistency Boundary, su independencia tecnológica y los
principios Domain-Driven Design establecidos para AURA Core.
