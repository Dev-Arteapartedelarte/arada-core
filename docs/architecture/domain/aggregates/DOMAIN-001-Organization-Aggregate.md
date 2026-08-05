# DOMAIN-001 — Organization Aggregate

Versión: 1.0

Estado: Oficial

Proyecto: AURA Core

Autor: ARADA

---

# Objetivo

Definir el Aggregate **Organization**, considerado la raíz
organizacional del dominio de AURA.

Toda interacción dentro de la plataforma ocurre en el
contexto de una organización. Ningún ciudadano, asamblea,
votación, documento o proceso existe de forma aislada.

Organization constituye el principal límite de consistencia
del sistema.

---

# Definición

Una Organization representa una entidad colectiva con
existencia jurídica o administrativa que participa en la
plataforma AURA.

Ejemplos:

- Junta de Vecinos
- Municipalidad
- Comunidad Indígena
- Comité de Agua Potable Rural
- Cooperativa
- Fundación
- Corporación
- Asociación Gremial
- Organización Funcional
- Organización Comunitaria

---

# Responsabilidades

El Aggregate Organization es responsable de:

- mantener su identidad;
- administrar su ciclo de vida;
- controlar su estado;
- definir políticas internas;
- administrar membresías;
- definir permisos organizacionales;
- establecer límites territoriales;
- emitir eventos del dominio.

Nunca administra directamente votaciones,
asambleas o documentos.

---

# Aggregate Root

La raíz del Aggregate es:

Organization

Toda modificación debe realizarse exclusivamente a través
de esta entidad.

No existen modificaciones directas sobre entidades internas.

---

# Identidad

Cada Organization posee un identificador global e
inmutable.

```text
OrganizationId
```

Este identificador nunca cambia durante toda la vida de la
organización.

---

# Atributos Principales

La Aggregate Root mantiene como mínimo:

```text
OrganizationId

OrganizationName

OrganizationType

OrganizationStatus

OrganizationCreationDate

OrganizationSettings

OrganizationPolicies

TerritoryId
```

Estos atributos representan el estado consistente de la
organización.

---

# Entidades Internas

El Aggregate puede contener entidades como:

```text
Membership

Department

Committee

Representative

RoleAssignment
```

Estas entidades no existen fuera del Aggregate.

---

# Value Objects

Entre los Value Objects asociados se consideran:

```text
OrganizationName

OrganizationType

OrganizationAddress

OrganizationContact

OrganizationSettings

OrganizationPolicies

OrganizationSchedule

OrganizationBrand
```

Todos son inmutables.

---

# Relaciones

Organization mantiene relaciones mediante identificadores
con otros Aggregates.

```text
CitizenId

AssemblyId

ProposalId

VoteId

DocumentId

NotificationId

AuditId

TerritoryId
```

Nunca mantiene referencias directas.

---

# Invariantes

Siempre deben cumplirse las siguientes reglas:

Una organización posee exactamente un identificador.

Una organización siempre posee un nombre válido.

Una organización siempre posee un tipo.

Una organización siempre posee un estado.

Una organización nunca puede quedar sin políticas.

Una organización nunca puede existir sin territorio
asociado cuando su tipo lo requiera.

Toda membresía pertenece a una única organización.

---

# Estados

La organización puede encontrarse en uno de los siguientes
estados:

```text
Draft

PendingValidation

Active

Suspended

Archived

Deleted
```

Cada transición es controlada por el Aggregate Root.

---

# Transiciones Permitidas

```text
Draft
    ↓

PendingValidation
    ↓

Active
    ↓
Suspended
    ↓
Active
    ↓
Archived
```

Deleted representa un estado lógico reservado para
retención y cumplimiento normativo.

---

# Operaciones Públicas

El Aggregate expone únicamente comportamientos.

Ejemplos:

```text
create()

activate()

suspend()

archive()

rename()

changeSettings()

changePolicies()

registerMember()

removeMember()

assignRepresentative()

changeTerritory()
```

Nunca expone setters públicos.

---

# Consistencia

Toda operación debe preservar las invariantes antes de
confirmar la transacción.

Si alguna regla se incumple, la operación completa falla.

---

# Eventos del Dominio

El Aggregate puede emitir eventos como:

```text
OrganizationCreated

OrganizationActivated

OrganizationSuspended

OrganizationArchived

OrganizationRenamed

OrganizationPoliciesChanged

OrganizationSettingsChanged

MemberRegistered

MemberRemoved

RepresentativeAssigned

TerritoryChanged
```

Los eventos representan hechos consumados.

---

# Límites del Aggregate

Organization no administra directamente:

- votaciones;
- propuestas;
- documentos;
- auditorías;
- notificaciones.

Estos pertenecen a Aggregates independientes.

---

# Consistencia Transaccional

Todas las modificaciones internas ocurren dentro de una
única transacción del Aggregate.

La coordinación con otros Aggregates ocurre mediante
Domain Events.

---

# Reglas de Diseño

- Organization es el único punto de entrada al Aggregate.
- Ninguna entidad interna puede modificarse desde el
  exterior.
- Toda colaboración externa utiliza identificadores.
- Ninguna referencia directa cruza Aggregates.
- Toda modificación genera un nuevo estado consistente.

---

# Beneficios

Este diseño proporciona:

- aislamiento del dominio;
- alta cohesión;
- bajo acoplamiento;
- consistencia transaccional;
- escalabilidad organizacional;
- independencia entre procesos;
- facilidad para integrar nuevos tipos de organización;
- compatibilidad con arquitecturas orientadas a eventos.

---

# Definición de Éxito

El Aggregate **Organization** representa de forma
consistente a cualquier organización participante de AURA,
centraliza las reglas de negocio relacionadas con su
identidad y administración, protege sus invariantes,
coordina sus entidades internas y publica eventos del
dominio que permiten la colaboración con el resto de los
Bounded Contexts sin comprometer el desacoplamiento del
modelo.