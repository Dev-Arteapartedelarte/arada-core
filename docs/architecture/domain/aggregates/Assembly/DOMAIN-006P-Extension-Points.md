# DOMAIN-006P — Assembly Extension Points

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
* DOMAIN-006N-Performance-Rules.md
* DOMAIN-006O-Security-Model.md
* CORE-003-Shared-Kernel.md
* CORE-004-Ubiquitous-Language.md
* CORE-006-Domain-Invariants.md
* CORE-007-Strategic-Design.md
* CORE-008-Aggregate-Design-Rules.md
* CORE-011-Repository-Contracts.md

---

# Objetivo

Definir los **Extension Points** oficiales del Aggregate
**Assembly**.

Los Extension Points representan lugares controlados en los cuales
el modelo de Assembly puede evolucionar para incorporar nuevas
necesidades del dominio sin romper:

* identidad del Aggregate;
* Aggregate Root;
* Lifecycle;
* State Machine;
* invariantes;
* Consistency Boundary;
* relaciones entre Aggregates;
* Commands;
* Domain Events;
* Permissions;
* Versioning;
* Repository Contract;
* Integration Events;
* Read Models;
* independencia tecnológica.

Un Extension Point no constituye una autorización para modificar
arbitrariamente el modelo.

Toda extensión debe respetar las reglas ya establecidas por el
Aggregate Assembly.

---

# Propósito

El propósito de los Extension Points es permitir que Assembly
evolucione de manera controlada frente a nuevas necesidades del
ecosistema AURA.

El dominio puede requerir en el futuro:

* nuevas modalidades de Assembly;
* nuevos tipos de Assembly;
* nuevas reglas de convocatoria;
* nuevas condiciones de realización;
* nuevos comportamientos;
* nuevos Domain Events;
* nuevas necesidades de autorización;
* nuevas representaciones de lectura;
* nuevas integraciones;
* nuevas reglas específicas del dominio.

Estas extensiones deben incorporarse sin convertir Assembly en un
Aggregate responsable de procesos que pertenecen a otros límites
del dominio.

---

# Principios

Toda extensión debe seguir los siguientes principios:

* preservar el lenguaje ubicuo;
* preservar la identidad de Assembly;
* preservar una única Aggregate Root;
* mantener explícito el Consistency Boundary;
* proteger las invariantes existentes;
* evitar acoplamiento entre Aggregates;
* mantener referencias externas mediante identificadores;
* no introducir Infrastructure dentro del dominio;
* no introducir Frameworks dentro del dominio;
* no transformar necesidades de UI en reglas del Aggregate;
* no transformar necesidades de integración en estado interno;
* no introducir cambios silenciosos;
* mantener compatibilidad documental;
* mantener evolución controlada.

---

# Principio Fundamental

Debe mantenerse:

```text
Extension
    ≠
Uncontrolled Modification
```

Una extensión válida amplía una capacidad del modelo sin destruir
las garantías existentes.

Toda extensión debe responder a una necesidad real del dominio.

No debe incorporarse únicamente por conveniencia técnica.

---

# Fuente Conceptual Oficial

La fuente conceptual oficial continúa siendo:

```text
DOMAIN-006-Aggregate.md
```

Los Extension Points no sustituyen dicha definición.

Cuando una extensión modifique conceptualmente el significado,
responsabilidad, identidad, Lifecycle, relación o límite de
Assembly, la definición correspondiente debe quedar reflejada en
los documentos oficiales afectados.

Debe mantenerse:

```text
DOMAIN-006-Aggregate.md

↓

Official Assembly Model

↓

Extension Points

↓

Controlled Evolution
```

---

# Regla de Coherencia

Una extensión no puede existir de manera aislada si modifica una
regla documentada en otro artefacto.

Cuando una extensión afecte un concepto existente debe mantenerse
coherencia con el documento responsable de dicho concepto.

Ejemplos:

```text
Lifecycle extension
    ↓
DOMAIN-006A-Lifecycle.md
```

```text
State transition extension
    ↓
DOMAIN-006B-State-Machine.md
```

```text
Command extension
    ↓
DOMAIN-006C-Commands.md
```

```text
Domain Event extension
    ↓
DOMAIN-006D-Domain-Events.md
```

```text
Invariant extension
    ↓
DOMAIN-006E-Invariants.md
```

```text
Permission extension
    ↓
DOMAIN-006F-Permissions.md
```

---

# Tipos de Extension Points

Los Extension Points conceptuales de Assembly pueden comprender:

```text
Assembly Types

Assembly Modalities

Assembly Rules

Convocation Rules

Realization Conditions

Commands

Domain Events

Permissions

Integration Events

Read Models

Repository Implementations

External Integrations
```

Cada uno posee límites específicos.

---

# Extensión de AssemblyType

Assembly mantiene un concepto:

```text
AssemblyType
```

Los tipos definidos oficialmente incluyen:

```text
Ordinary

Extraordinary

Organizational

Board

Community

Deliberative

Participatory

Territorial

WorkingSession

Consultation
```

El catálogo puede evolucionar cuando el dominio requiera
representar una nueva naturaleza formal de reunión.

---

# Regla de Extensión de AssemblyType

Un nuevo AssemblyType debe representar una diferencia conceptual
real dentro del dominio.

No debe utilizarse para representar:

* una variación visual;
* una configuración técnica;
* una integración externa;
* una pantalla;
* un canal de comunicación;
* una tecnología.

Debe mantenerse:

```text
AssemblyType
    =
Domain Classification
```

---

# Nueva Clasificación

La incorporación de un nuevo tipo debe evaluar si introduce reglas
específicas sobre:

* Lifecycle;
* convocatoria;
* programación;
* modalidad;
* condiciones de realización;
* Permissions;
* invariantes.

Si no modifica ninguna de estas reglas, puede constituir únicamente
una nueva clasificación conceptual.

Si modifica alguna de ellas, deben actualizarse los documentos
correspondientes.

---

# Extensión de AssemblyModality

Assembly mantiene:

```text
AssemblyModality
```

con modalidades oficiales:

```text
InPerson

Remote

Hybrid
```

El modelo puede admitir futuras modalidades si el dominio requiere
nuevas formas reconocibles de realización.

---

# Regla de Extensión de AssemblyModality

Una nueva modalidad debe representar una forma distinta de
realización de la reunión.

No debe representar una tecnología concreta.

Debe mantenerse:

```text
AssemblyModality
    ≠
Technology Provider
```

Por lo tanto una modalidad no debe llamarse según:

* proveedor de videoconferencia;
* plataforma web;
* aplicación;
* protocolo;
* fabricante.

---

# Modalidad e Infrastructure

AssemblyModality expresa cómo se desarrolla conceptualmente la reunión.

Infrastructure determina mediante qué herramientas se implementa.

Debe mantenerse:

```text
Remote
    =
Domain Modality
```

mientras:

```text
Video Platform
    =
Infrastructure Choice
```

---

# Modalidad y Location

Una extensión de AssemblyModality puede requerir revisar las reglas
relacionadas con:

```text
Location
```

cuando la nueva modalidad cambie las condiciones necesarias para
representar ubicación.

Toda modificación debe preservar las invariantes oficiales.

---

# Extensión de Assembly Rules

Assembly puede mantener reglas propias relacionadas con la
realización de la reunión.

Conceptualmente:

```text
AssemblyRule
```

puede evolucionar conforme aparezcan nuevas reglas reales del
dominio.

Las reglas deben permanecer dentro de Assembly únicamente cuando
formen parte de su propia consistencia.

---

# Regla de Propiedad de AssemblyRule

Una regla pertenece a Assembly cuando determina la validez del
estado o comportamiento de la propia reunión.

No pertenece a Assembly si controla exclusivamente el estado de:

```text
Organization

Citizen

Membership

Role

Territory

Proposal

Participation

Voting

Document

Notification

Audit
```

En esos casos debe mantenerse dentro del Aggregate correspondiente.

---

# Extensión de Convocation Rules

La convocatoria forma parte del modelo oficial de Assembly.

Conceptualmente puede comprender:

```text
ConvocationStatus

ConvokedAt

ConvocationDeadline

ConvocationRules
```

Las reglas de convocatoria pueden evolucionar conforme a
necesidades organizacionales o normativas del dominio.

---

# Regla de Extensión de Convocation

Una nueva regla de convocatoria debe determinar una condición
formal de Assembly.

No debe transformar Assembly en responsable de ejecutar la entrega
de comunicaciones.

Debe mantenerse:

```text
Convocation
    ≠
Notification Delivery
```

Assembly mantiene el estado formal de convocatoria.

Notification mantiene la responsabilidad de comunicación.

---

# Convocatoria y Notification

Una extensión puede exigir nuevos hechos relacionados con
convocatoria.

Por ejemplo, una nueva condición formal puede producir un Domain
Event correspondiente.

Esto no permite incorporar dentro de Assembly:

```text
Notification

NotificationChannel

DeliveryAttempt

ProviderCredentials
```

---

# Extensión de Realization Conditions

Assembly mantiene condiciones necesarias para que una reunión pueda
desarrollarse formalmente.

Estas condiciones pueden evolucionar.

Toda nueva condición debe pertenecer realmente a la validez de la
Assembly.

---

# Condiciones Propias de Assembly

Una condición puede pertenecer a Assembly cuando determina si la
reunión puede:

```text
start()

complete()
```

válidamente.

La condición debe expresarse mediante conceptos del dominio y no
mediante detalles técnicos.

---

# Condiciones Externas

Una condición que dependa de otro Aggregate no permite absorber ese
Aggregate.

Cuando corresponda obtener información externa, la coordinación
debe mantenerse fuera de Assembly conforme al Consistency Boundary.

Debe mantenerse:

```text
External Validation
    ≠
External Aggregate Ownership
```

---

# Extensión del Lifecycle

El Lifecycle oficial se encuentra definido en:

```text
DOMAIN-006A-Lifecycle.md
```

y utiliza los estados:

```text
Draft

Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

Una extensión del Lifecycle constituye un cambio significativo del
dominio.

No debe incorporarse silenciosamente.

---

# Regla de Extensión del Lifecycle

Un nuevo estado solo debe añadirse cuando represente una condición
del dominio que no pueda expresarse correctamente mediante los
estados existentes.

No debe añadirse un estado para representar:

* una operación técnica;
* una respuesta HTTP;
* una espera de infraestructura;
* una cola de procesamiento;
* una ejecución de integración;
* una condición de UI.

---

# Nuevo Estado

Si el dominio requiere un nuevo estado, deben actualizarse
coherentemente:

```text
DOMAIN-006-Aggregate.md

DOMAIN-006A-Lifecycle.md

DOMAIN-006B-State-Machine.md

DOMAIN-006C-Commands.md

DOMAIN-006D-Domain-Events.md

DOMAIN-006E-Invariants.md

DOMAIN-006F-Permissions.md

DOMAIN-006M-Test-Scenarios.md
```

y cualquier otro documento afectado.

---

# Estado Técnico

No debe incorporarse dentro de Assembly un estado como:

```text
Saving

Publishing

Synchronizing

Retrying

SendingNotification

WaitingForBroker
```

si dichos conceptos corresponden a Infrastructure o integración.

Debe mantenerse:

```text
Domain State
    ≠
Technical Processing State
```

---

# Extensión de State Machine

La State Machine oficial se encuentra definida en:

```text
DOMAIN-006B-State-Machine.md
```

Una nueva transición debe corresponder a una evolución válida del
Lifecycle.

---

# Regla de Nueva Transición

Una transición debe definir claramente:

```text
Origin State

Command

Guards

Destination State

Domain Event
```

cuando corresponda al modelo oficial.

No debe existir una transición implícita no documentada.

---

# Compatibilidad de Transiciones

Una nueva transición no debe hacer inválidas silenciosamente las
invariantes existentes.

Cuando una transición afecte reglas previas, las reglas deben
actualizarse explícitamente.

---

# Extensión de Commands

Los Commands oficiales se encuentran definidos en:

```text
DOMAIN-006C-Commands.md
```

Nuevos Commands pueden incorporarse cuando exista una nueva
intención de dominio sobre Assembly.

---

# Regla de Nuevo Command

Un nuevo Command debe:

* representar una intención;
* modificar únicamente Assembly;
* respetar el Consistency Boundary;
* poseer datos suficientes para expresar la intención;
* respetar Permissions;
* respetar State Machine;
* respetar invariantes;
* participar en Versioning;
* producir Domain Events cuando corresponda.

---

# Command Técnico

No debe agregarse un Command de dominio únicamente para representar
una operación de Infrastructure.

Ejemplos incompatibles con el modelo de dominio:

```text
SaveAssemblyToDatabase

SendAssemblyHttpRequest

PublishAssemblyToKafka

CacheAssembly

SerializeAssembly
```

Estas operaciones pertenecen a capas técnicas.

---

# Command y External Aggregate

No debe crearse un Command de Assembly que modifique directamente
otro Aggregate.

No:

```text
CreateVotingFromAssembly
```

si su implementación significa modificar directamente Voting desde
Assembly.

La coordinación debe respetar los límites oficiales.

---

# Extensión de Domain Events

Los Domain Events oficiales se encuentran definidos en:

```text
DOMAIN-006D-Domain-Events.md
```

Nuevos eventos pueden incorporarse cuando Assembly produzca nuevos
hechos relevantes.

---

# Regla de Nuevo Domain Event

Todo nuevo Domain Event debe:

* representar un hecho consumado;
* originarse en una modificación válida;
* utilizar lenguaje ubicuo;
* pertenecer al dominio de Assembly;
* ser inmutable;
* mantener trazabilidad según el contrato;
* no representar una intención.

Debe mantenerse:

```text
Domain Event
    ≠
Command
```

---

# Evento Técnico

No deben definirse como Domain Events de Assembly hechos
exclusivamente técnicos como:

```text
AssemblySavedToDatabase

AssemblySerialized

AssemblyCacheUpdated

AssemblyHttpResponseSent
```

Estos hechos no representan cambios conceptuales del Aggregate.

---

# Extensión de Invariants

Las invariantes oficiales se encuentran definidas en:

```text
DOMAIN-006E-Invariants.md
```

Nuevas invariantes pueden surgir cuando el dominio incorpore nuevas
reglas obligatorias sobre el estado de Assembly.

---

# Regla de Nueva Invariante

Toda nueva invariante debe:

* proteger un estado válido;
* pertenecer al Aggregate;
* mantenerse verdadera después de toda modificación válida;
* ser independiente de una tecnología específica;
* poder relacionarse con los Commands y transiciones afectados.

---

# Invariante Externa

No debe introducirse dentro de Assembly una invariante que requiera
mantener transaccionalmente el estado mutable de otro Aggregate.

Debe mantenerse:

```text
Assembly Invariant
    inside
Assembly Boundary
```

---

# Extensión de Permissions

Los Permissions oficiales se encuentran definidos en:

```text
DOMAIN-006F-Permissions.md
```

Nuevas capacidades pueden incorporarse cuando aparezcan nuevas
operaciones protegidas sobre Assembly.

---

# Regla de Nuevo Permission

Un Permission debe relacionarse con una capacidad real sobre
Assembly.

No debe utilizarse para:

* evitar invariantes;
* omitir State Machine;
* modificar Version directamente;
* modificar otros Aggregates;
* conceder acceso técnico a Infrastructure.

---

# Permission e Invariant

Toda extensión debe mantener:

```text
Permission
    ≠
Invariant
```

Un nuevo Permission puede determinar quién intenta una nueva
operación.

No determina que el resultado sea válido.

---

# Extensión del Repository Contract

El Repository Contract oficial se encuentra definido en:

```text
DOMAIN-006G-Repository-Contract.md
```

La implementación del Repository puede evolucionar sin modificar el
Aggregate.

---

# Implementaciones del Repository

Pueden existir distintas implementaciones técnicas del contrato
siempre que todas mantengan exactamente la misma semántica de
dominio.

Debe mantenerse:

```text
Repository Implementation
    ≠
Domain Model
```

---

# Nueva Tecnología de Persistencia

La incorporación de una nueva tecnología de almacenamiento no
constituye una extensión del Aggregate.

Ejemplos:

```text
PostgreSQL

MongoDB

Event Store

Other Storage
```

pertenecen a Infrastructure.

---

# Repository y Nuevas Consultas

Una nueva necesidad de lectura no debe agregarse automáticamente al
Repository del Aggregate.

Debe evaluarse conforme al modelo de Read Models establecido en:

```text
DOMAIN-006L-Read-Model.md
```

---

# Extensión de Versioning

El modelo de Versioning se encuentra definido en:

```text
DOMAIN-006I-Versioning.md
```

Una extensión funcional de Assembly debe continuar respetando
Version.

Todo cambio válido de estado debe seguir las reglas oficiales de
Versioning.

---

# Regla de Compatibilidad con Version

Un nuevo Command que modifique Assembly debe integrarse al modelo de
Versioning.

No puede declararse una modificación de dominio fuera del control de
Version únicamente por tratarse de una nueva funcionalidad.

---

# Extension y Concurrency

Las nuevas operaciones deben mantener protección frente a
modificaciones concurrentes incompatibles.

Debe mantenerse:

```text
New Behavior
    ≠
Versioning Bypass
```

---

# Extensión del Consistency Boundary

El Consistency Boundary se encuentra definido en:

```text
DOMAIN-006J-Consistency-Boundary.md
```

No debe ampliarse únicamente porque aparezca una nueva relación o
caso de uso.

---

# Regla de Extensión del Boundary

Una modificación del Consistency Boundary constituye una decisión
fundamental del modelo DDD.

Solo debe producirse cuando cambien las invariantes que requieren
consistencia transaccional conjunta.

No debe producirse por:

* conveniencia de consultas;
* facilidad de implementación;
* estructura de base de datos;
* estructura de UI;
* integración;
* rendimiento;
* reducción del número de eventos.

---

# Regla de No Absorción

Una nueva funcionalidad no puede transformar automáticamente en
entidades internas de Assembly a:

```text
Organization

Citizen

Membership

Role

Territory

Proposal

Participation

Voting

Document

Notification

Audit

Integration
```

Estos conceptos continúan fuera del Aggregate.

---

# Nueva Relación

Assembly puede relacionarse con nuevos Aggregates cuando el dominio
lo requiera.

La relación debe mantenerse mediante:

```text
AggregateId
```

y mecanismos de colaboración del dominio.

Debe mantenerse:

```text
Relationship
    ≠
Ownership
```

---

# Referencias por Identidad

Las extensiones deben preservar el principio:

```text
Assembly
    │
    └── ExternalAggregateId
```

No:

```text
Assembly
    │
    └── MutableExternalAggregate
```

---

# Extensión de Integration Events

Los Integration Events oficiales se encuentran definidos en:

```text
DOMAIN-006K-Integration-Events.md
```

Nuevas integraciones pueden requerir nuevos contratos externos.

---

# Regla de Nuevo Integration Event

Un nuevo Integration Event debe:

* representar un hecho confirmado;
* derivarse de un hecho válido del dominio cuando corresponda;
* mantener contrato explícito;
* poseer versión contractual;
* minimizar información;
* no exponer el Aggregate completo;
* no transportar credenciales;
* no introducir lógica del consumidor dentro de Assembly.

---

# Nuevo Consumidor

La aparición de un nuevo consumidor no debe modificar Assembly si
el dominio no ha cambiado.

Debe mantenerse:

```text
New Consumer
    ≠
New Aggregate Responsibility
```

---

# Nueva Integración

Una nueva integración puede añadirse mediante:

```text
Domain Event

↓

Integration Event

↓

Adapter

↓

External System
```

sin introducir el sistema externo dentro del Aggregate.

---

# Integración Municipal

Nuevas plataformas municipales pueden incorporarse mediante
adaptadores y contratos de integración.

Assembly no debe conocer:

* endpoints;
* credenciales;
* formatos propietarios;
* SDKs;
* protocolos específicos.

---

# Integración Smart City

Nuevos sistemas Smart City pueden consumir hechos de Assembly sin
modificar su Consistency Boundary.

Debe mantenerse:

```text
Smart City Integration
    outside
Assembly
```

---

# Integración FIWARE

La integración con FIWARE puede evolucionar independientemente del
Aggregate.

Assembly no conoce:

```text
NGSI-LD

Context Broker

Orion-LD

FIWARE Credentials

FIWARE API
```

El Adapter transforma los contratos correspondientes.

---

# Extensión de Read Models

Los Read Models oficiales se encuentran definidos en:

```text
DOMAIN-006L-Read-Model.md
```

El lado de lectura constituye uno de los principales Extension
Points de Assembly.

Nuevas necesidades de consulta pueden producir nuevas proyecciones
sin modificar el Write Model.

---

# Regla de Nueva Proyección

Una nueva proyección debe:

* derivarse del dominio;
* ser de solo lectura;
* ser reconstruible;
* no introducir lógica de negocio;
* no constituir Aggregate Root;
* no convertirse en fuente transaccional de verdad;
* respetar el lenguaje ubicuo.

---

# Nueva Necesidad de Consulta

Debe preferirse:

```text
New Query Requirement

↓

Read Model Extension
```

cuando la necesidad corresponde exclusivamente a lectura.

No:

```text
New Query Requirement

↓

Add State to Assembly
```

si dicho estado no pertenece al dominio.

---

# Dashboards

Nuevos dashboards pueden incorporar nuevas proyecciones o
combinaciones de lectura.

No requieren modificar Assembly cuando no introducen nuevas reglas
de dominio.

---

# Analytics

Nuevas necesidades analíticas deben mantenerse fuera del Write
Model.

Debe mantenerse:

```text
Analytics
    ≠
Aggregate State
```

---

# Reporting

Nuevos reportes pueden combinar información de distintos Read
Models.

Debe mantenerse:

```text
Report Composition
    ≠
Aggregate Composition
```

---

# UI

Cambios de interfaz no constituyen por sí mismos extensiones del
Aggregate.

Debe mantenerse:

```text
UI Requirement
    ≠
Domain Requirement
```

Una nueva pantalla puede requerir una nueva proyección.

No necesariamente una nueva propiedad de Assembly.

---

# API

Cambios en una API no constituyen automáticamente cambios del
Aggregate.

Debe mantenerse:

```text
API Contract
    ≠
Aggregate Contract
```

Una API puede evolucionar mediante adaptadores, DTOs o Read Models
sin modificar el dominio cuando su significado permanece igual.

---

# Extension Points de Seguridad

El Security Model oficial se encuentra definido en:

```text
DOMAIN-006O-Security-Model.md
```

Las tecnologías de seguridad pueden evolucionar sin modificar
Assembly.

---

# Nuevas Tecnologías de Authentication

La incorporación de tecnologías como:

```text
OAuth

OpenID Connect

SAML

Keyrock

Other Identity Provider
```

no modifica Assembly.

Authentication permanece fuera del Aggregate.

---

# Nuevos Permissions

Una nueva funcionalidad de dominio sí puede requerir un nuevo
Permission.

En ese caso debe actualizarse:

```text
DOMAIN-006F-Permissions.md
```

y mantenerse la separación:

```text
Permission
    ≠
Invariant
```

---

# Extension Points de Performance

Las Performance Rules se encuentran definidas en:

```text
DOMAIN-006N-Performance-Rules.md
```

Las optimizaciones técnicas pueden evolucionar sin modificar el
significado de Assembly.

---

# Nuevos Mecanismos de Caché

Una nueva estrategia de caché pertenece a Infrastructure.

No modifica:

* identidad;
* Lifecycle;
* State Machine;
* invariantes;
* Version;
* Consistency Boundary.

---

# Nuevos Motores de Búsqueda

La incorporación de un nuevo motor de búsqueda pertenece al lado de
lectura e Infrastructure.

No constituye una nueva responsabilidad del Aggregate.

---

# Nuevas Estrategias de Escalabilidad

El escalado técnico puede evolucionar siempre que mantenga:

```text
One Assembly
    =
One Assembly Consistency Boundary
```

No debe fusionar múltiples Assemblies dentro de una misma unidad de
consistencia de dominio.

---

# Extension Points de Test Scenarios

Los Test Scenarios oficiales se encuentran definidos en:

```text
DOMAIN-006M-Test-Scenarios.md
```

Toda extensión del dominio debe incorporar los escenarios
conceptuales necesarios para verificarla.

---

# Regla de Cobertura

Una nueva regla debe producir pruebas que cubran:

```text
Valid Scenario

Invalid Scenario
```

cuando corresponda.

Una nueva transición debe verificar:

```text
Allowed Transition

Rejected Transition
```

Una nueva invariante debe verificar:

```text
Invariant Preserved

Invariant Violation Rejected
```

---

# Extensión de Value Objects

Assembly utiliza Value Objects conceptuales definidos por su modelo.

Nuevos Value Objects pueden aparecer cuando el dominio necesite
representar un concepto con reglas propias de valor.

---

# Regla de Nuevo Value Object

Un Value Object debe:

* representar un concepto del dominio;
* carecer de identidad propia;
* ser inmutable;
* validar sus propias reglas de valor;
* permanecer independiente de Infrastructure.

No debe crearse únicamente para envolver un tipo técnico sin valor
semántico para el dominio.

---

# Value Objects Externos

Un Value Object perteneciente a otro Aggregate no debe copiarse
arbitrariamente dentro de Assembly si ello produce duplicación de
responsabilidad.

Debe evaluarse el lenguaje y Boundary correspondiente.

---

# Extensión de Entidades Internas

Assembly puede contener entidades internas únicamente cuando estas
formen parte de su consistencia.

Conceptualmente se han identificado:

```text
AssemblySchedule

Convocation

AssemblyRule

AssemblyLocation
```

cuando su existencia concreta sea necesaria conforme al modelo.

---

# Regla de Nueva Entidad Interna

Una entidad interna debe:

* existir únicamente dentro de Assembly;
* no requerir autonomía fuera del Aggregate;
* no poseer Repository independiente;
* no poseer Consistency Boundary independiente;
* ser modificada únicamente mediante Assembly;
* participar en invariantes internas.

---

# Entidad con Autonomía

Si un nuevo concepto requiere:

* identidad global propia;
* Lifecycle propio;
* Repository propio;
* invariantes propias;
* autonomía transaccional;

debe evaluarse como posible Aggregate independiente.

No debe incorporarse automáticamente como entidad interna.

---

# Regla de Identidad

Debe mantenerse:

```text
Independent Identity
+
Independent Lifecycle
+
Independent Consistency

↓

Potential Independent Aggregate
```

La decisión debe basarse en el dominio.

No en conveniencia técnica.

---

# Extension Point de Políticas

Las futuras políticas relacionadas con Assembly pueden modelarse
cuando representen reglas del dominio.

Una política puede determinar condiciones sobre:

* convocatoria;
* programación;
* realización;
* modificación;
* finalización;
* archivado.

---

# Regla de Política

Una política no debe utilizarse como contenedor genérico de lógica
sin responsabilidad clara.

Toda política debe tener:

* propósito definido;
* lenguaje de dominio;
* responsabilidad delimitada;
* relación explícita con las invariantes o comportamiento
  correspondientes.

---

# Políticas Organizacionales

Organization puede mantener políticas propias.

Assembly no debe copiar automáticamente dichas políticas dentro de
su estado.

Cuando una operación requiera aplicar una política de Organization,
la coordinación debe respetar los límites entre Aggregates.

---

# Extension Point de Reglas Territoriales

Una Assembly territorial puede requerir reglas relacionadas con su
contexto territorial.

Estas reglas no convierten Territory en parte de Assembly.

Debe mantenerse:

```text
Territorial Context
    ≠
Territory Ownership
```

---

# Extensiones Jurídicas o Normativas

El dominio puede evolucionar por cambios normativos que afecten
Assembly.

Una nueva regla normativa debe traducirse al lenguaje del dominio
antes de incorporarse.

No debe copiarse directamente una estructura legal o administrativa
como estructura técnica sin modelar su significado.

---

# Regla de Lenguaje Ubicuo

Toda extensión debe expresarse utilizando conceptos comprensibles
dentro del dominio AURA.

Debe evitarse introducir nombres derivados exclusivamente de:

* tablas;
* endpoints;
* frameworks;
* librerías;
* proveedores;
* protocolos.

---

# Evolución del Lenguaje

Si aparece un nuevo concepto real del dominio, debe incorporarse de
forma consistente al lenguaje ubicuo y a la documentación
correspondiente.

La terminología debe permanecer coherente entre todos los
artefactos.

---

# Compatibilidad Documental

Toda extensión debe analizar qué documentos oficiales resultan
afectados.

Conceptualmente:

```text
New Domain Concept

↓

Affected Documents

↓

Consistent Update
```

No debe quedar una regla definida exclusivamente en un documento
secundario si modifica la fuente conceptual oficial.

---

# Cambios Locales

Una extensión puede ser local cuando no modifica otras reglas del
Aggregate.

Ejemplo conceptual:

```text
New Read Projection
```

puede requerir modificar únicamente:

```text
DOMAIN-006L-Read-Model.md
```

si no cambia el dominio de escritura.

---

# Cambios Transversales

Una extensión es transversal cuando afecta múltiples dimensiones del
Aggregate.

Ejemplo:

```text
New Lifecycle State
```

puede afectar:

```text
Aggregate

Lifecycle

State Machine

Commands

Domain Events

Invariants

Permissions

Versioning

Integration Events

Read Model

Tests
```

Todos los documentos afectados deben permanecer coherentes.

---

# Versionado Documental

La evolución conceptual debe reflejarse mediante el mecanismo de
versionado documental establecido por AURA.

Una modificación significativa no debe incorporarse silenciosamente
sin dejar trazabilidad de su evolución.

---

# Compatibilidad con Domain Events Existentes

Una nueva extensión no debe cambiar retrospectivamente el
significado de un Domain Event ya definido.

Debe mantenerse:

```text
Existing Event Meaning
    =
Stable Meaning
```

Si aparece un nuevo hecho diferente, debe modelarse como un nuevo
evento cuando corresponda.

---

# Compatibilidad con Integration Events Existentes

Los Integration Events mantienen contratos externos.

Una extensión no debe cambiar silenciosamente la semántica de un
contrato publicado.

La evolución debe respetar:

```text
EventVersion
```

conforme al modelo oficial de Integration Events.

---

# Compatibilidad con Read Models

Las nuevas propiedades del dominio pueden incorporarse a
proyecciones cuando sean necesarias para consulta.

No todas las propiedades nuevas deben aparecer en todas las
proyecciones.

Cada Read Model mantiene su propósito.

---

# Compatibilidad con Security Model

Toda extensión que cree una nueva operación protegida debe evaluar
si requiere un nuevo Permission.

Debe mantenerse:

```text
New Command
    ↓
Permission Evaluation
```

cuando corresponda.

La nueva operación continúa sujeta a invariantes y State Machine.

---

# Compatibilidad con Performance Rules

Toda extensión debe poder implementarse sin romper las reglas de
rendimiento establecidas.

Performance no puede utilizarse como argumento para alterar la
semántica de la extensión.

---

# Compatibilidad con Test Scenarios

Toda extensión de comportamiento debe generar nuevos Test Scenarios
o actualizar los escenarios afectados.

Una extensión no se considera completamente documentada si sus
reglas no pueden verificarse conceptualmente.

---

# Extension Point — Nuevos Tipos

Ejemplo conceptual:

```text
New AssemblyType
```

requiere verificar:

* significado real de dominio;
* compatibilidad con Lifecycle;
* compatibilidad con State Machine;
* reglas de convocatoria;
* condiciones de realización;
* Permissions;
* eventos afectados;
* Read Models afectados.

---

# Extension Point — Nueva Modalidad

Ejemplo conceptual:

```text
New AssemblyModality
```

requiere verificar:

* significado de la modalidad;
* relación con Location;
* reglas de realización;
* invariantes;
* Read Models;
* Integration Events cuando corresponda.

---

# Extension Point — Nueva Regla de Convocatoria

Ejemplo conceptual:

```text
New Convocation Rule
```

requiere verificar:

* pertenencia a Assembly;
* invariantes;
* Commands afectados;
* State Machine;
* Domain Events;
* Permissions;
* Test Scenarios.

---

# Extension Point — Nueva Condición de Inicio

Ejemplo conceptual:

```text
New Start Condition
```

requiere verificar:

```text
DOMAIN-006A-Lifecycle.md

DOMAIN-006B-State-Machine.md

DOMAIN-006C-Commands.md

DOMAIN-006E-Invariants.md

DOMAIN-006M-Test-Scenarios.md
```

cuando corresponda.

---

# Extension Point — Nueva Condición de Finalización

Una nueva condición para:

```text
complete()
```

debe pertenecer realmente a la consistencia de Assembly.

No debe utilizarse para controlar el estado interno de Voting,
Proposal, Participation o Document.

---

# Extension Point — Nuevo Domain Event

Un nuevo hecho de Assembly puede generar:

```text
NewDomainEvent
```

únicamente después de una modificación válida.

Debe mantener:

* semántica;
* inmutabilidad;
* trazabilidad;
* coherencia con Commands;
* coherencia con Version.

---

# Extension Point — Nuevo Integration Event

Una nueva necesidad de interoperabilidad puede producir un nuevo
Integration Event sin modificar el Aggregate si el hecho ya existe
en el dominio.

Debe mantenerse:

```text
Existing Domain Fact

↓

New Integration Contract
```

sin introducir una nueva responsabilidad de Assembly.

---

# Extension Point — Nuevo Read Model

Una nueva necesidad de consulta puede producir:

```text
New Projection
```

sin modificar Assembly.

La proyección debe mantenerse:

* reconstruible;
* de solo lectura;
* desacoplada;
* libre de lógica de negocio.

---

# Extension Point — Nueva Integración Externa

Una nueva plataforma externa se integra mediante:

```text
Integration Contract

↓

Adapter

↓

External Platform
```

No:

```text
Assembly

↓

External Platform SDK
```

---

# Extension Point — Nueva Implementación de Repository

Una nueva implementación del Repository puede utilizar otra
tecnología de persistencia.

Debe cumplir exactamente:

```text
DOMAIN-006G-Repository-Contract.md
```

sin modificar la semántica de Assembly.

---

# Regla de Compatibilidad con Consistency Boundary

Toda extensión debe responder explícitamente:

```text
Does this concept need strong consistency
with Assembly?
```

Si la respuesta es no, el concepto no debe incorporarse dentro del
Aggregate únicamente por cercanía funcional.

---

# Regla de Autonomía

Cuando un nuevo concepto puede evolucionar independientemente de
Assembly, debe evaluarse su autonomía.

Conceptualmente:

```text
Independent Lifecycle

+

Independent Invariants

+

Independent Repository

↓

Independent Domain Boundary
```

cuando corresponda.

---

# Regla de Cohesión

Las extensiones internas deben aumentar o mantener la cohesión de
Assembly.

No deben convertir el Aggregate en un contenedor de funcionalidades
heterogéneas.

Debe mantenerse:

```text
High Cohesion

Low Coupling
```

---

# Regla de Acoplamiento

Una extensión no debe obligar a Assembly a conocer detalles internos
de otros Bounded Contexts.

Debe utilizar:

* identificadores;
* Domain Events;
* Integration Events;
* contratos;
* coordinación externa;

según corresponda.

---

# Regla de Independencia Tecnológica

Ningún Extension Point debe obligar al dominio a depender de:

```text
Database

ORM

HTTP

REST

GraphQL

OAuth

JWT

Kafka

RabbitMQ

FIWARE

React

Next.js

FastAPI

Django
```

Las tecnologías pueden evolucionar independientemente.

---

# Regla de No Inferencia Técnica

Una necesidad técnica no debe declararse automáticamente como nueva
regla del dominio.

Debe mantenerse:

```text
Technical Requirement
    ≠
Domain Requirement
```

hasta que exista una necesidad conceptual real que justifique el
cambio del modelo.

---

# Regla de No Inferencia desde UI

Una nueva pantalla, formulario, botón o flujo visual no constituye
por sí mismo una nueva capacidad del Aggregate.

Debe evaluarse primero si representa:

* nueva intención de dominio;
* nueva consulta;
* nueva integración;
* nueva representación.

---

# Regla de No Inferencia desde Persistencia

Una nueva tabla, colección, columna o índice no constituye por sí
mismo una nueva entidad, Value Object o Aggregate.

Debe mantenerse:

```text
Persistence Structure
    ≠
Domain Structure
```

---

# Regla de No Inferencia desde Integración

La estructura de un sistema externo no debe copiarse dentro de
Assembly.

Debe mantenerse:

```text
External Model
    ≠
Assembly Model
```

Los Adapters realizan la traducción correspondiente.

---

# Regla de No Inferencia desde Performance

Un problema de rendimiento no puede utilizarse para cambiar:

* Aggregate Root;
* Boundary;
* invariantes;
* identidad;
* Lifecycle;

sin una justificación de dominio.

---

# Regla de No Inferencia desde Seguridad

Una tecnología de Authentication o Authorization no debe
incorporarse como concepto interno de Assembly si no pertenece al
dominio.

Debe mantenerse:

```text
Security Technology
    ≠
Domain Concept
```

---

# Regla de Evolución Compatible

Una extensión compatible debe preservar:

```text
Existing Valid Behavior
```

salvo que el dominio haya cambiado explícitamente.

Los casos existentes deben continuar respetando las reglas
oficiales.

---

# Regla de Evolución Incompatible

Cuando una extensión cambie una regla existente debe documentarse
como evolución explícita del dominio.

No debe alterarse silenciosamente el significado de:

* estados;
* Commands;
* Domain Events;
* Permissions;
* invariantes;
* relaciones;
* contratos.

---

# Test de Extension Point

Toda extensión de comportamiento debe poder expresarse
conceptualmente mediante:

```text
Given

existing valid Assembly model

When

extension behavior is applied

Then

existing invariants remain valid

And

Consistency Boundary remains valid

And

Versioning remains valid

And

affected domain rules are explicitly documented
```

---

# Test de No Absorción

```text
Given

a new Assembly capability requires information
from another Aggregate

When

the capability is modeled

Then

the external Aggregate remains outside Assembly

And

the relationship uses domain identifiers or contracts
```

---

# Test de Nueva Proyección

```text
Given

a new query requirement

When

a new Read Model is introduced

Then

Assembly remains unchanged

And

the projection contains no domain mutation logic
```

---

# Test de Nueva Integración

```text
Given

a new external consumer

When

integration is added

Then

Assembly does not depend on the external technology

And

integration occurs through contracts and adapters
```

---

# Test de Nuevo Permission

```text
Given

a new protected Assembly operation

When

a Permission is introduced

Then

the Permission only determines who may attempt the operation

And

State Machine and Invariants still determine domain validity
```

---

# Test de Nuevo AssemblyType

```text
Given

a new AssemblyType

When

the type is incorporated

Then

it represents a real domain classification

And

all affected rules remain coherent
```

---

# Test de Nueva Modalidad

```text
Given

a new AssemblyModality

When

the modality is incorporated

Then

it represents a domain realization modality

And

it does not introduce a technology provider into Assembly
```

---

# Test de Nueva Invariante

```text
Given

a new domain rule belonging to Assembly

When

the invariant is introduced

Then

every valid operation preserves it

And

operations violating it are rejected
```

---

# Test de Nuevo Estado

```text
Given

a proposed new AssemblyStatus

When

the domain model is evaluated

Then

the status must represent a real lifecycle condition

And

all affected documents must be updated coherently
```

---

# Test de Nueva Entidad Interna

```text
Given

a proposed internal entity

When

its autonomy is evaluated

Then

it belongs inside Assembly only if it cannot exist
independently from the Aggregate

And

it participates in Assembly consistency
```

---

# Test de Aggregate Independiente

```text
Given

a new concept with independent identity

And

independent lifecycle

And

independent invariants

And

independent consistency

When

the model is evaluated

Then

it must not be absorbed into Assembly merely for convenience
```

---

# Restricciones

No está permitido:

* introducir extensiones que contradigan DOMAIN-006-Aggregate.md;
* crear nuevas Aggregate Roots dentro de Assembly sin una decisión
  explícita del dominio;
* incorporar otros Aggregates como entidades internas por
  conveniencia;
* ampliar el Consistency Boundary por necesidades de UI;
* ampliar el Consistency Boundary por necesidades de reporting;
* ampliar el Consistency Boundary por necesidades de integración;
* ampliar el Consistency Boundary por rendimiento;
* incorporar estados técnicos al Lifecycle;
* introducir Commands técnicos como Commands de dominio;
* introducir eventos de Infrastructure como Domain Events;
* utilizar Permissions para evitar invariantes;
* utilizar nuevas funcionalidades para evitar Versioning;
* modificar Assembly directamente desde una integración;
* modificar otros Aggregates desde Assembly;
* convertir Read Models en fuente de escritura;
* convertir Integration Events en Commands;
* convertir APIs externas en modelos internos;
* introducir credenciales dentro del Aggregate;
* introducir Frameworks dentro del dominio;
* introducir bases de datos dentro del modelo conceptual;
* modificar silenciosamente contratos existentes;
* modificar silenciosamente estados existentes;
* modificar silenciosamente el significado de Domain Events;
* modificar silenciosamente Permissions;
* introducir nuevas reglas sin actualizar los documentos afectados.

---

# Principios Arquitectónicos

Los Extension Points mantienen:

```text
Extension
    ≠
Architecture Bypass
```

```text
Extension
    ≠
Aggregate Boundary Expansion
```

```text
Relationship
    ≠
Ownership
```

```text
New Consumer
    ≠
New Aggregate Responsibility
```

```text
New Query
    ≠
New Aggregate State
```

```text
New Integration
    ≠
New Aggregate Dependency
```

```text
New Technology
    ≠
New Domain Concept
```

```text
New UI Requirement
    ≠
New Domain Rule
```

```text
New Database Structure
    ≠
New Domain Entity
```

```text
New Permission
    ≠
Invariant Bypass
```

```text
New Command
    ≠
Direct External Aggregate Mutation
```

```text
New Domain Event
    ≠
Technical Event
```

```text
Read Model Extension
    ≠
Write Model Extension
```

```text
Integration Contract Evolution
    ≠
Aggregate Evolution
```

```text
Infrastructure Evolution
    ≠
Domain Evolution
```

Estas separaciones permiten que Assembly evolucione sin perder su
coherencia arquitectónica.

---

# Compatibilidad Arquitectónica

Los Extension Points son compatibles con:

* Domain-Driven Design;
* Strategic DDD;
* Tactical DDD;
* Aggregate Pattern;
* Clean Architecture;
* Hexagonal Architecture;
* CQRS;
* Event-Driven Architecture;
* Event Sourcing Compatible;
* Optimistic Concurrency;
* arquitectura distribuida;
* consistencia eventual;
* interoperabilidad basada en contratos;
* evolución incremental del dominio.

La compatibilidad no introduce tecnologías concretas dentro del
Aggregate.

---

# Relación con DOMAIN-006-Aggregate

`DOMAIN-006-Aggregate.md` constituye la fuente conceptual oficial de
Assembly.

Toda extensión que modifique conceptos fundamentales debe reflejarse
en dicha fuente.

Este documento identifica los límites dentro de los cuales puede
producirse evolución controlada.

---

# Relación con Lifecycle

`DOMAIN-006A-Lifecycle.md` define el Lifecycle oficial.

Nuevos estados o reglas de evolución deben mantenerse coherentes con
dicho documento.

---

# Relación con State Machine

`DOMAIN-006B-State-Machine.md` define las transiciones oficiales.

Toda nueva transición debe documentarse explícitamente y preservar
las invariantes.

---

# Relación con Commands

`DOMAIN-006C-Commands.md` define las intenciones oficiales.

Nuevos comportamientos que representen intención de modificar
Assembly deben incorporarse coherentemente allí.

---

# Relación con Domain Events

`DOMAIN-006D-Domain-Events.md` define los hechos consumados.

Toda nueva capacidad que produzca un nuevo hecho relevante debe
evaluar la incorporación del Domain Event correspondiente.

---

# Relación con Invariants

`DOMAIN-006E-Invariants.md` define las reglas obligatorias del
Aggregate.

Toda extensión debe preservar las invariantes existentes y
documentar nuevas invariantes cuando el dominio lo requiera.

---

# Relación con Permissions

`DOMAIN-006F-Permissions.md` define las capacidades autorizadas.

Toda nueva operación protegida debe evaluar los Permissions
correspondientes.

---

# Relación con Repository Contract

`DOMAIN-006G-Repository-Contract.md` define el contrato de
persistencia.

Las nuevas implementaciones técnicas deben respetar dicho contrato.

---

# Relación con Examples

`DOMAIN-006H-Examples.md` documenta escenarios conceptuales.

Nuevas capacidades pueden requerir ejemplos adicionales sin
redefinir las reglas desde dicho documento.

---

# Relación con Versioning

`DOMAIN-006I-Versioning.md` define la evolución concurrente del
Aggregate.

Toda nueva modificación de estado debe respetar Versioning.

---

# Relación con Consistency Boundary

`DOMAIN-006J-Consistency-Boundary.md` define la frontera
transaccional.

Las extensiones no deben modificarla implícitamente.

---

# Relación con Integration Events

`DOMAIN-006K-Integration-Events.md` define los contratos externos.

Nuevos consumidores o plataformas pueden incorporarse mediante
nuevos contratos sin modificar necesariamente Assembly.

---

# Relación con Read Model

`DOMAIN-006L-Read-Model.md` define las proyecciones de lectura.

Nuevas necesidades de consulta constituyen un Extension Point
natural del lado de lectura.

---

# Relación con Test Scenarios

`DOMAIN-006M-Test-Scenarios.md` define escenarios conceptuales de
verificación.

Toda extensión de comportamiento debe quedar cubierta por pruebas
coherentes.

---

# Relación con Performance Rules

`DOMAIN-006N-Performance-Rules.md` define las reglas de rendimiento.

Una extensión no puede utilizar Performance como justificación para
violar el dominio.

---

# Relación con Security Model

`DOMAIN-006O-Security-Model.md` define las reglas conceptuales de
seguridad.

Toda nueva capacidad protegida debe mantener la separación entre
Authentication, Authorization, Permissions e Invariants.

---

# Regla de Coherencia Documental

Los Extension Points deben mantenerse coherentes con:

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

DOMAIN-006N-Performance-Rules.md

DOMAIN-006O-Security-Model.md
```

Ninguna extensión puede introducir silenciosamente:

* nuevos estados;
* nuevas transiciones;
* nuevos Commands;
* nuevos Domain Events;
* nuevas invariantes;
* nuevos Permissions;
* nuevas Aggregate Roots;
* nuevos Aggregates;
* nuevas relaciones de propiedad;
* nuevas dependencias tecnológicas;
* nuevos límites de consistencia.

---

# Regla de Evolución

Toda extensión debe clasificarse conceptualmente antes de
incorporarse.

Debe determinarse si corresponde a:

```text
Domain Extension

Read Extension

Integration Extension

Infrastructure Extension
```

Una extensión del dominio puede modificar Assembly.

Una extensión de lectura debe permanecer en Read Models cuando no
cambia el dominio.

Una extensión de integración debe permanecer fuera del Aggregate
cuando no cambia el dominio.

Una extensión de Infrastructure no debe modificar el modelo
conceptual.

---

# Domain Extension

Una Domain Extension existe cuando cambia realmente:

* comportamiento;
* regla;
* clasificación;
* Lifecycle;
* invariante;
* capacidad;
* hecho del dominio.

Debe actualizar los documentos oficiales afectados.

---

# Read Extension

Una Read Extension existe cuando se requiere una nueva forma de
consultar información ya existente.

Debe resolverse mediante Read Models cuando no exista cambio del
dominio.

---

# Integration Extension

Una Integration Extension existe cuando un nuevo sistema necesita
consumir o producir contratos de interoperabilidad.

Debe mantenerse fuera de Assembly salvo que exista un cambio real
del dominio.

---

# Infrastructure Extension

Una Infrastructure Extension comprende cambios como:

* nueva base de datos;
* nuevo broker;
* nuevo proveedor de identidad;
* nueva plataforma de despliegue;
* nueva estrategia de caché;
* nuevo Framework;
* nuevo Adapter.

Estas extensiones no forman parte del Aggregate.

---

# Criterio de Aceptación de una Extensión

Una extensión puede considerarse válida para Assembly cuando:

* responde a una necesidad real del dominio;
* utiliza lenguaje ubicuo;
* no contradice la fuente conceptual oficial;
* preserva la Aggregate Root;
* preserva el Consistency Boundary o documenta explícitamente una
  modificación de dominio;
* preserva las invariantes existentes;
* respeta Versioning;
* respeta Permissions;
* mantiene independencia tecnológica;
* no absorbe otros Aggregates;
* actualiza los documentos afectados;
* incorpora Test Scenarios cuando corresponde.

---

# Criterio de Rechazo de una Extensión

Una propuesta de extensión debe rechazarse cuando:

* solo responde a conveniencia técnica;
* duplica responsabilidad de otro Aggregate;
* amplía el Boundary sin necesidad de consistencia;
* introduce tecnología en el dominio;
* rompe invariantes existentes;
* evita State Machine;
* evita Versioning;
* evita Permissions;
* utiliza un Read Model como Write Model;
* utiliza Integration Events como Commands;
* transforma UI en dominio;
* transforma persistencia en dominio;
* introduce acoplamiento directo con sistemas externos.

---

# Definición de Éxito

Los **Extension Points** del Aggregate **Assembly** establecen los
mecanismos conceptuales oficiales mediante los cuales el modelo
puede evolucionar sin perder coherencia con la arquitectura DDD de
AURA Core.

Assembly puede extenderse para incorporar:

```text
New Assembly Types

New Assembly Modalities

New Assembly Rules

New Convocation Rules

New Realization Conditions

New Commands

New Domain Events

New Permissions

New Integration Events

New Read Models
```

cuando exista una necesidad real del dominio o del límite
arquitectónico correspondiente.

Toda extensión debe preservar la identidad de Assembly y su única
Aggregate Root.

El Lifecycle, State Machine, invariantes, Permissions, Versioning y
Consistency Boundary continúan siendo las autoridades conceptuales
que determinan la validez del comportamiento.

Organization, Territory, Citizen, Membership, Role, Proposal,
Participation, Voting, Document, Notification y Audit permanecen
fuera de Assembly y no pueden ser absorbidos únicamente para
facilitar nuevos casos de uso.

Una relación nueva no constituye propiedad.

Un nuevo consumidor no constituye una nueva responsabilidad del
Aggregate.

Una nueva consulta no constituye nuevo estado del Write Model.

Una nueva integración no constituye una dependencia interna.

Una nueva tecnología no constituye un nuevo concepto de dominio.

Las nuevas proyecciones pueden incorporarse mediante Read Models sin
modificar Assembly cuando la necesidad corresponda exclusivamente a
lectura.

Las nuevas plataformas externas pueden incorporarse mediante
Integration Events y Adapters sin introducir dependencias
tecnológicas dentro del Aggregate.

Las nuevas implementaciones de persistencia pueden evolucionar
detrás del Repository Contract sin modificar la semántica del
dominio.

Las nuevas capacidades protegidas deben mantener la separación entre
Permissions e Invariants.

Las nuevas modificaciones deben continuar respetando Versioning.

Las nuevas reglas deben producir Test Scenarios que permitan
verificar su comportamiento.

Toda extensión transversal debe actualizar coherentemente los
documentos oficiales afectados.

Debe mantenerse permanentemente:

```text
Extend the Domain

without

Breaking the Domain
```

y:

```text
Controlled Evolution

↓

Preserved Identity

Preserved Invariants

Preserved Boundaries

Preserved Language
```

De esta forma,
**DOMAIN-006P-Extension-Points.md** establece el modelo conceptual y
normativo oficial para la evolución controlada del Aggregate
Assembly, permitiendo incorporar nuevas capacidades, reglas,
proyecciones e integraciones sin romper su identidad, su límite de
consistencia, su independencia tecnológica ni los principios
Domain-Driven Design establecidos para AURA Core.