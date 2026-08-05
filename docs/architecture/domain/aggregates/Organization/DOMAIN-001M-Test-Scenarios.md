# DOMAIN-001M — Test Scenarios

Versión: 1.0

Estado:
Oficial

Proyecto:
AURA Core

Bounded Context:
Organization Management

Aggregate:
Organization

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-001-Aggregate.md
- DOMAIN-001A-Lifecycle.md
- DOMAIN-001B-State-Machine.md
- DOMAIN-001C-Commands.md
- DOMAIN-001D-Domain-Events.md
- DOMAIN-001E-Invariants.md
- DOMAIN-001F-Permissions.md
- DOMAIN-001G-Repository-Contract.md
- DOMAIN-001I-Versioning.md
- DOMAIN-001J-Consistency-Boundary.md
- DOMAIN-001K-Integration-Events.md
- DOMAIN-001L-Read-Model.md

---

# Objetivo

Definir los escenarios oficiales de prueba del Aggregate
**Organization**.

Este documento especifica los comportamientos esperados del
Aggregate desde la perspectiva del dominio, sin depender de
frameworks, bases de datos o infraestructura.

Cada escenario representa una regla de negocio que deberá
estar respaldada por pruebas automatizadas.

---

# Estrategia de Pruebas

Las pruebas del Aggregate siguen los principios de Domain-
Driven Design.

Cada prueba valida:

- un Command;
- un estado inicial;
- una transición;
- las invariantes;
- los Domain Events emitidos;
- el estado final del Aggregate.

No se prueban detalles de implementación.

---

# Formato

Cada escenario utiliza la estructura:

```text
Given
When
Then
```

---

# Escenario 1

## Crear una Organización válida

### Given

No existe una organización con el mismo identificador.

### When

```text
CreateOrganization
```

### Then

- Organization creada.
- Estado = Draft.
- Version = 1.
- Domain Event:

```text
OrganizationCreated
```

---

# Escenario 2

## Rechazar nombre vacío

### Given

No existe organización.

### When

```text
CreateOrganization

Name = ""
```

### Then

Debe producirse:

```text
InvalidOrganizationNameError
```

No se crea el Aggregate.

---

# Escenario 3

## Aprobar organización

### Given

Organization

```text
Status = PendingValidation
```

### When

```text
ApproveOrganization
```

### Then

Estado:

```text
Approved
```

Evento:

```text
OrganizationApproved
```

Version:

```text
+1
```

---

# Escenario 4

## Aprobar una organización ya aprobada

### Given

```text
Status = Approved
```

### When

```text
ApproveOrganization
```

### Then

Debe producirse:

```text
InvalidStateTransitionError
```

---

# Escenario 5

## Suspender organización

### Given

```text
Status = Approved
```

### When

```text
SuspendOrganization
```

### Then

Estado:

```text
Suspended
```

Evento:

```text
OrganizationSuspended
```

---

# Escenario 6

## Reactivar organización

### Given

```text
Status = Suspended
```

### When

```text
ReactivateOrganization
```

### Then

Estado:

```text
Approved
```

Evento:

```text
OrganizationReactivated
```

---

# Escenario 7

## Archivar organización

### Given

```text
Status = Approved
```

### When

```text
ArchiveOrganization
```

### Then

Estado:

```text
Archived
```

Evento:

```text
OrganizationArchived
```

---

# Escenario 8

## Modificar nombre

### Given

Organization existente.

### When

```text
RenameOrganization
```

### Then

Nuevo nombre válido.

Evento:

```text
OrganizationRenamed
```

Version incrementada.

---

# Escenario 9

## Asignar representante

### Given

Organization válida.

### When

```text
AssignRepresentative
```

### Then

RepresentativeId actualizado.

Evento:

```text
RepresentativeAssigned
```

---

# Escenario 10

## Reemplazar representante

### Given

Existe representante activo.

### When

```text
AssignRepresentative
```

### Then

El representante anterior deja de ser el activo.

Nunca existen dos representantes activos
simultáneamente.

---

# Escenario 11

## Versionado

### Given

Version:

```text
5
```

### When

```text
RenameOrganization
```

### Then

Version:

```text
6
```

---

# Escenario 12

## Concurrencia Optimista

### Given

Proceso A

```text
Version 12
```

Proceso B

```text
Version 12
```

### When

A guarda correctamente.

Después B intenta guardar.

### Then

```text
ConcurrencyConflictError
```

---

# Escenario 13

## Invariante

### Given

Representative obligatorio.

### When

Intentar aprobar sin representante.

### Then

```text
BusinessRuleViolation
```

---

# Escenario 14

## Domain Event

### Given

Organization creada.

### When

Persistencia exitosa.

### Then

Debe existir exactamente un evento.

```text
OrganizationCreated
```

---

# Escenario 15

## Integration Event

### Given

Organization aprobada.

### When

Commit exitoso.

### Then

Debe generarse:

```text
OrganizationApprovedIntegrationEvent
```

---

# Escenario 16

## Read Model

### Given

Organization aprobada.

### When

Projection ejecutada.

### Then

Read Model actualizado.

---

# Escenario 17

## Consistencia

### Given

Aggregate válido.

### When

Commit.

### Then

Todas las invariantes permanecen satisfechas.

---

# Escenario 18

## Estado Final

### Given

```text
Archived
```

### When

Intentar modificar.

### Then

```text
InvalidStateTransitionError
```

---

# Escenario 19

## Eliminación

### Given

Organization archivada.

### When

```text
DeleteOrganization
```

### Then

Evento:

```text
OrganizationDeleted
```

---

# Escenario 20

## Reconstrucción

### Given

Secuencia completa de Domain Events.

### When

Rehidratar Aggregate.

### Then

El estado reconstruido coincide exactamente con el
último estado persistido.

---

# Cobertura Esperada

El conjunto mínimo de pruebas debe cubrir:

- creación;
- modificación;
- eliminación;
- transiciones de estado;
- invariantes;
- permisos;
- eventos;
- versionado;
- concurrencia;
- consistencia;
- reconstrucción;
- integración.

---

# Matriz de Cobertura

| Área | Cobertura |
|-------|-----------|
| Commands | 100% |
| State Machine | 100% |
| Invariants | 100% |
| Domain Events | 100% |
| Integration Events | 100% |
| Versioning | 100% |
| Repository Contract | 100% |
| Read Model | 100% |
| Concurrency | 100% |
| Permissions | 100% |

---

# Principios

Las pruebas del Aggregate deben ser:

- determinísticas;
- independientes;
- repetibles;
- rápidas;
- aisladas;
- expresivas;
- orientadas al comportamiento del dominio.

Ninguna prueba dependerá de:

- bases de datos;
- red;
- APIs;
- UI;
- infraestructura;
- reloj del sistema;
- framework específico.

---

# Definición de Éxito

El Aggregate **Organization** se considera validado cuando todos los escenarios definidos en este documento se ejecutan satisfactoriamente mediante pruebas automatizadas. La suite de pruebas constituye la especificación ejecutable del comportamiento del dominio y garantiza que futuras modificaciones preserven las invariantes, reglas de negocio, transiciones de estado, eventos, versionado y límites de consistencia establecidos para AURA Core.