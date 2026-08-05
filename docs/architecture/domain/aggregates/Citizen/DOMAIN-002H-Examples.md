# DOMAIN-002H — Citizen Examples

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Citizen Management

Aggregate:
Citizen

Documentos relacionados:

- DOMAIN-002-Aggregate.md
- DOMAIN-002A-Lifecycle.md
- DOMAIN-002B-State-Machine.md
- DOMAIN-002C-Commands.md
- DOMAIN-002D-Domain-Events.md
- DOMAIN-002E-Invariants.md
- DOMAIN-002F-Permissions.md
- DOMAIN-002G-Repository-Contract.md

---

# Objetivo

Este documento presenta escenarios completos de negocio para
el Aggregate **Citizen**.

Los ejemplos muestran cómo interactúan Commands, reglas de
negocio, transiciones de estado y Domain Events durante el
ciclo de vida de una identidad cívica dentro de AURA.

Los ejemplos son conceptuales y no representan una
implementación tecnológica.

---

# Ejemplo 1 — Registro de un nuevo ciudadano

## Escenario

María crea una identidad digital para participar en su Junta de
Vecinos.

### Estado inicial

```text
No existe Aggregate.
```

### Command

```text
RegisterCitizen
```

### Resultado

```text
Citizen

↓

State = Draft
```

### Domain Event

```text
CitizenRegistered
```

---

# Ejemplo 2 — Solicitud de verificación

## Escenario

María inicia el proceso de validación de identidad.

### Estado inicial

```text
Draft
```

### Command

```text
RequestCitizenVerification
```

### Estado final

```text
PendingVerification
```

### Domain Event

```text
CitizenVerificationRequested
```

---

# Ejemplo 3 — Verificación exitosa

## Escenario

La organización confirma la identidad de María utilizando el
mecanismo de verificación definido por la plataforma.

### Estado inicial

```text
PendingVerification
```

### Command

```text
VerifyCitizen
```

### Estado final

```text
Verified
```

### Domain Event

```text
CitizenVerified
```

---

# Ejemplo 4 — Activación

## Escenario

Una vez verificada la identidad, el ciudadano queda habilitado
para participar en la plataforma.

### Estado inicial

```text
Verified
```

### Command

```text
ActivateCitizen
```

### Estado final

```text
Active
```

### Domain Event

```text
CitizenActivated
```

---

# Ejemplo 5 — Actualización del perfil

## Escenario

El ciudadano modifica su fotografía pública y su biografía.

### Estado inicial

```text
Active
```

### Command

```text
UpdateCitizenProfile
```

### Estado final

```text
Active
```

(No existe transición de estado.)

### Domain Event

```text
CitizenProfileUpdated
```

---

# Ejemplo 6 — Cambio de domicilio

## Escenario

El ciudadano cambia su residencia dentro de la comuna.

### Estado inicial

```text
Active
```

### Command

```text
UpdateCitizenAddress
```

### Estado final

```text
Active
```

### Domain Event

```text
CitizenAddressUpdated
```

Este evento puede ser consumido posteriormente por los
Bounded Contexts de:

- Territory;
- Organization;
- Analytics.

---

# Ejemplo 7 — Suspensión temporal

## Escenario

La organización suspende temporalmente al ciudadano debido a un
procedimiento administrativo.

### Estado inicial

```text
Active
```

### Command

```text
SuspendCitizen
```

### Estado final

```text
Suspended
```

### Domain Event

```text
CitizenSuspended
```

---

# Ejemplo 8 — Reactivación

## Escenario

Finalizado el procedimiento administrativo, el ciudadano
recupera su participación.

### Estado inicial

```text
Suspended
```

### Command

```text
ReactivateCitizen
```

### Estado final

```text
Active
```

### Domain Event

```text
CitizenReactivated
```

---

# Ejemplo 9 — Retiro voluntario

## Escenario

El ciudadano decide abandonar temporalmente la plataforma.

### Estado inicial

```text
Active
```

### Command

```text
DeactivateCitizen
```

### Estado final

```text
Inactive
```

### Domain Event

```text
CitizenDeactivated
```

---

# Ejemplo 10 — Archivado

## Escenario

Después de completar el proceso de cierre establecido por la
organización, el Aggregate finaliza su ciclo de vida.

### Estado inicial

```text
Inactive
```

### Command

```text
ArchiveCitizen
```

### Estado final

```text
Archived
```

### Domain Event

```text
CitizenArchived
```

---

# Ejemplo 11 — Intento inválido

## Escenario

Se intenta activar un ciudadano cuya identidad aún no ha sido
verificada.

### Estado inicial

```text
Draft
```

### Command

```text
ActivateCitizen
```

### Resultado

```text
Rejected
```

### Motivo

La transición no está definida en la State Machine y viola las
invariantes del Aggregate.

### Domain Event

```text
Ninguno
```

---

# Ejemplo 12 — Modificación sobre un Citizen archivado

## Escenario

Se intenta actualizar la dirección de un ciudadano archivado.

### Estado inicial

```text
Archived
```

### Command

```text
UpdateCitizenAddress
```

### Resultado

```text
Rejected
```

### Motivo

Los Aggregates archivados son de solo lectura.

### Domain Event

```text
Ninguno
```

---

# Ejemplo 13 — Flujo completo del ciclo de vida

```text
RegisterCitizen
        │
        ▼
CitizenRegistered
        │
        ▼
Draft
        │
        ▼
RequestCitizenVerification
        │
        ▼
CitizenVerificationRequested
        │
        ▼
PendingVerification
        │
        ▼
VerifyCitizen
        │
        ▼
CitizenVerified
        │
        ▼
Verified
        │
        ▼
ActivateCitizen
        │
        ▼
CitizenActivated
        │
        ▼
Active
        │
        ├───────────────┐
        │               │
        ▼               ▼
UpdateProfile     UpdateAddress
        │               │
        ▼               ▼
CitizenProfileUpdated
CitizenAddressUpdated
        │
        ▼
SuspendCitizen
        │
        ▼
CitizenSuspended
        │
        ▼
Suspended
        │
        ▼
ReactivateCitizen
        │
        ▼
CitizenReactivated
        │
        ▼
Active
        │
        ▼
DeactivateCitizen
        │
        ▼
CitizenDeactivated
        │
        ▼
Inactive
        │
        ▼
ArchiveCitizen
        │
        ▼
CitizenArchived
        │
        ▼
Archived
```

---

# Relación con CQRS

Los Commands de estos ejemplos pertenecen al lado de escritura.

Los Domain Events generados alimentan posteriormente los Read
Models utilizados para consultas, estadísticas y paneles de
control.

---

# Relación con Event Sourcing

Cada escenario puede reconstruirse reproduciendo la secuencia
cronológica de Domain Events emitidos por el Aggregate.

La historia del Citizen constituye la fuente oficial de verdad
del dominio.

---

# Definición de Éxito

Los ejemplos presentados demuestran el comportamiento esperado
del Aggregate **Citizen** frente a situaciones habituales y
excepcionales del negocio. Sirven como referencia para el
diseño, implementación y validación del dominio, asegurando que
las reglas de negocio, la máquina de estados y los eventos de
dominio permanezcan coherentes en todo el ecosistema AURA.