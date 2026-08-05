# DOMAIN-001 — Organization Aggregate

Versión: 1.0

Estado: Oficial

Proyecto: AURA Core

Bounded Context:
Organization Management

Aggregate Root:
Organization

Autor:
ARADA

---

# Objetivo

Definir la arquitectura oficial del Aggregate
Organization.

Organization constituye el Aggregate raíz sobre el cual se
estructura la plataforma AURA.

Toda organización que participa en el ecosistema posee una
representación única, consistente e independiente.

Este Aggregate protege la identidad de la organización,
sus políticas y su estructura organizacional.

---

# Propósito

Representar una organización como una unidad de negocio
capaz de administrar personas, procesos, recursos y
participación ciudadana.

---

# Definición

Una Organization representa una entidad colectiva
autónoma con existencia administrativa dentro del
ecosistema AURA.

Puede representar tanto organizaciones públicas como
privadas.

Ejemplos:

- Junta de Vecinos
- Municipalidad
- Comité APR
- Comunidad Indígena
- Fundación
- Corporación
- ONG
- Cooperativa
- Asociación Gremial
- Universidad
- Servicio Público

---

# Aggregate Root

```text
Organization
```

Todas las operaciones del Aggregate deben ejecutarse
únicamente mediante Organization.

Ninguna entidad interna puede modificarse directamente.

---

# Responsabilidades

Organization es responsable de:

- identidad institucional;
- ciclo de vida;
- estado organizacional;
- configuración;
- políticas internas;
- estructura organizacional;
- pertenencia territorial;
- representación legal;
- emisión de Domain Events.

No administra procesos de negocio pertenecientes a otros
Aggregates.

---

# Principios

Organization cumple los siguientes principios:

- única fuente de verdad;
- consistencia transaccional;
- encapsulamiento;
- invariantes protegidas;
- independencia tecnológica;
- comunicación mediante eventos.

---

# Identidad

Toda organización posee un identificador global único.

```text
OrganizationId
```

El identificador:

- nunca cambia;
- nunca se reutiliza;
- identifica de manera absoluta al Aggregate.

---

# Atributos

Organization mantiene el siguiente estado mínimo.

```text
OrganizationId

OrganizationName

OrganizationType

OrganizationStatus

OrganizationCreationDate

OrganizationPolicies

OrganizationSettings

TerritoryId
```

El conjunto puede evolucionar sin alterar el contrato del
Aggregate.

---

# Entidades Internas

Las siguientes entidades pueden existir únicamente dentro
del Aggregate.

```text
Membership

Department

Committee

Representative

OrganizationalUnit

RoleAssignment
```

No poseen identidad fuera del Aggregate.

---

# Value Objects

Los siguientes Value Objects pertenecen al Aggregate.

```text
OrganizationName

OrganizationType

OrganizationStatus

OrganizationAddress

OrganizationContact

OrganizationPolicies

OrganizationSettings

OrganizationBrand

OrganizationSchedule
```

Todos son inmutables.

---

# Relaciones

Organization nunca mantiene referencias directas hacia
otros Aggregates.

Las relaciones siempre utilizan identificadores.

```text
CitizenId

AssemblyId

ProposalId

VoteId

NotificationId

DocumentId

AuditId

TerritoryId
```

---

# Límites

Organization no administra:

- votaciones;
- propuestas;
- asambleas;
- auditorías;
- documentos;
- notificaciones;
- autenticación.

Cada uno constituye un Aggregate independiente.

---

# Consistencia

Todas las modificaciones deben preservar el estado válido
del Aggregate.

Si una única regla falla, toda la operación se cancela.

---

# Invariantes

Siempre deben cumplirse las siguientes reglas.

Una organización posee exactamente un identificador.

Una organización siempre posee un nombre.

Una organización siempre posee un tipo.

Una organización siempre posee un estado.

Una organización nunca pierde sus políticas.

Una organización nunca puede existir parcialmente.

Toda membresía pertenece exactamente a una organización.

---

# Ciclo de Vida

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
retención normativa.

---

# Operaciones

El Aggregate únicamente expone comportamientos.

```text
create()

activate()

suspend()

archive()

rename()

changePolicies()

changeSettings()

changeAddress()

changeBrand()

registerMember()

removeMember()

assignRepresentative()

changeTerritory()
```

No existen setters públicos.

---

# Domain Events

Organization puede emitir eventos como:

```text
OrganizationCreated

OrganizationValidated

OrganizationActivated

OrganizationSuspended

OrganizationArchived

OrganizationRenamed

OrganizationPoliciesChanged

OrganizationSettingsChanged

OrganizationAddressChanged

OrganizationBrandChanged

RepresentativeAssigned

MemberRegistered

MemberRemoved

TerritoryChanged
```

Todos representan hechos consumados.

---

# Consistencia Transaccional

Todas las modificaciones internas pertenecen a una única
transacción del Aggregate.

La coordinación con otros Aggregates ocurre mediante
Domain Events.

---

# Reglas Arquitectónicas

## Regla 1

Organization es el único punto de entrada al Aggregate.

---

## Regla 2

Las entidades internas nunca son modificadas desde el
exterior.

---

## Regla 3

Toda modificación preserva las invariantes.

---

## Regla 4

Las relaciones externas utilizan únicamente
identificadores.

---

## Regla 5

No existen referencias directas entre Aggregates.

---

## Regla 6

Toda modificación produce un nuevo estado consistente.

---

## Regla 7

Toda colaboración con otros Bounded Contexts ocurre
mediante eventos del dominio o contratos públicos.

---

## Regla 8

Organization nunca contiene lógica perteneciente a otros
Aggregates.

---

## Regla 9

La infraestructura nunca modifica directamente el estado
del Aggregate.

---

## Regla 10

Organization constituye la autoridad máxima sobre su
propia consistencia.

---

# Dependencias

Organization únicamente depende de:

- Shared Kernel
- Value Objects propios
- Domain Events
- Repository Contracts

No depende de:

- Frameworks
- Base de datos
- HTTP
- Mensajería
- ORM
- Interfaces

---

# Beneficios

Esta arquitectura proporciona:

- alta cohesión;
- bajo acoplamiento;
- encapsulamiento fuerte;
- consistencia transaccional;
- evolución independiente;
- integración mediante eventos;
- independencia tecnológica;
- alineación con DDD y Clean Architecture.

---

# Definición de Éxito

El Aggregate Organization representa de manera única y
consistente a cualquier organización del ecosistema AURA,
protege sus invariantes, encapsula completamente su estado,
coordina sus entidades internas, publica eventos del
dominio y constituye el punto exclusivo de acceso para toda
modificación relacionada con la identidad y administración
organizacional.