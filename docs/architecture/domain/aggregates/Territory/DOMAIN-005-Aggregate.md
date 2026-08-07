# DOMAIN-005 — Territory Aggregate

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Territorial Management

Aggregate:
Territory

Documentos relacionados:

- DOMAIN-005A-Lifecycle.md
- DOMAIN-005B-State-Machine.md
- DOMAIN-005C-Commands.md
- DOMAIN-005D-Domain-Events.md
- DOMAIN-005E-Invariants.md
- DOMAIN-005F-Permissions.md
- DOMAIN-005G-Repository-Contract.md
- DOMAIN-005I-Versioning.md
- DOMAIN-005J-Consistency-Boundary.md
- DOMAIN-005K-Integration-Events.md
- DOMAIN-005L-Read-Model.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir el Aggregate **Territory**, responsable de representar
la unidad territorial sobre la cual una **Organization** ejerce
su ámbito de actuación.

El Aggregate centraliza la identidad territorial, su
clasificación, delimitación administrativa y estado de
vigencia, permitiendo que las organizaciones y los procesos de
participación ciudadana se desarrollen dentro de un contexto
geográfico consistente.

---

# Definición

Un **Territory** representa una unidad territorial reconocida
por el dominio AURA.

Dependiendo del contexto de despliegue, un territorio puede
corresponder a:

- Región
- Provincia
- Comuna
- Distrito
- Barrio
- Sector
- Unidad Vecinal
- Comunidad
- Territorio Indígena
- Polígono administrativo
- Área de planificación

El dominio no impone una jerarquía fija; la clasificación
depende de la configuración del sistema.

---

# Responsabilidades

El Aggregate Territory es responsable de:

- mantener su identidad;
- administrar su ciclo de vida;
- controlar su estado;
- definir su clasificación territorial;
- mantener sus límites administrativos;
- gestionar relaciones jerárquicas con otros territorios;
- publicar eventos del dominio.

No administra directamente:

- organizaciones;
- ciudadanos;
- membresías;
- roles;
- asambleas;
- propuestas;
- votaciones;
- documentos;
- notificaciones;
- auditorías.

---

# Aggregate Root

La única Aggregate Root es:

```text
Territory
```

Toda modificación del territorio debe realizarse
exclusivamente a través de esta entidad.

---

# Identidad

Cada Territory posee un identificador único e inmutable.

```text
TerritoryId
```

Este identificador permanece constante durante todo el ciclo
de vida del Aggregate.

---

# Estado

El Aggregate mantiene, como mínimo, la siguiente información:

```text
TerritoryId

TerritoryName

TerritoryType

TerritoryStatus

ParentTerritoryId

AdministrativeCode

GeometryReference

Metadata
```

---

# Value Objects

Ejemplos de Value Objects:

```text
TerritoryName

TerritoryType

AdministrativeCode

GeometryReference

TerritoryMetadata
```

Todos los Value Objects son inmutables.

---

# Relaciones

El Aggregate mantiene relaciones exclusivamente mediante
identificadores.

Ejemplos:

```text
OrganizationId

ParentTerritoryId

AssemblyId

DocumentId

AuditId
```

Nunca mantiene referencias directas a otros Aggregates.

---

# Invariantes

Siempre deben cumplirse las siguientes reglas:

- existe exactamente un TerritoryId;
- todo Territory posee un nombre válido;
- todo Territory posee un tipo;
- todo Territory posee un estado;
- un territorio no puede ser padre de sí mismo;
- no pueden existir ciclos en la jerarquía territorial;
- el código administrativo debe ser único dentro de su ámbito;
- un Territory archivado no admite modificaciones.

---

# Estados

```text
Draft

PendingValidation

Active

Inactive

Archived
```

Toda transición de estado es controlada por el Aggregate Root.

---

# Transiciones Permitidas

```text
Draft
    ↓
PendingValidation
    ↓
Active
   ↕
Inactive
    ↓
Archived
```

No existen transiciones directas que omitan estados
intermedios.

---

# Operaciones Públicas

El Aggregate expone únicamente comportamientos.

Ejemplos:

```text
create()

activate()

deactivate()

archive()

rename()

changeType()

changeAdministrativeCode()

changeGeometry()

changeParent()

updateMetadata()
```

Nunca expone setters públicos.

---

# Eventos del Dominio

El Aggregate puede publicar eventos como:

```text
TerritoryCreated

TerritoryActivated

TerritoryDeactivated

TerritoryArchived

TerritoryRenamed

TerritoryTypeChanged

TerritoryParentChanged

TerritoryGeometryChanged

TerritoryMetadataUpdated
```

Todos representan hechos consumados.

---

# Límites del Aggregate

Territory no administra directamente:

- Organization;
- Citizen;
- Membership;
- Role;
- Assembly;
- Proposal;
- Voting;
- Document;
- Notification;
- Audit.

La colaboración ocurre mediante identificadores y Domain
Events.

---

# Consistencia

Toda modificación ocurre dentro de una única transacción del
Aggregate.

La coordinación con otros Aggregates utiliza consistencia
eventual mediante eventos del dominio.

---

# Reglas de Diseño

- una única Aggregate Root;
- ninguna referencia directa a otros Aggregates;
- invariantes protegidas por el Aggregate;
- colaboración mediante identificadores;
- comportamiento orientado a métodos;
- alta cohesión;
- bajo acoplamiento.

---

# Beneficios

Este diseño proporciona:

- consistencia territorial;
- independencia respecto de la organización administrativa
  de cada país;
- escalabilidad para distintos niveles territoriales;
- compatibilidad con sistemas GIS;
- integración con plataformas Smart City;
- soporte para modelos jerárquicos;
- compatibilidad con CQRS y Event-Driven Architecture.

---

# Definición de Éxito

El Aggregate **Territory** representa de forma consistente la
estructura territorial utilizada por AURA. Centraliza la
identidad, clasificación y vigencia de los territorios,
protege sus invariantes, administra su jerarquía y publica los
eventos necesarios para que el resto de los Aggregates puedan
referenciar un contexto geográfico común sin generar
acoplamiento entre dominios.