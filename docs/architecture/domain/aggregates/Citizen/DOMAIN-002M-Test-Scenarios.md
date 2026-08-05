# DOMAIN-002M — Citizen Test Scenarios

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
- DOMAIN-002I-Versioning.md

---

# Objetivo

Este documento define los escenarios oficiales de prueba del
Aggregate **Citizen**.

Los escenarios verifican el comportamiento esperado del
Aggregate desde la perspectiva del dominio, asegurando que las
reglas de negocio, las invariantes y la máquina de estados se
cumplan correctamente.

No describen pruebas de infraestructura, interfaces de usuario
ni APIs.

---

# Principios

Las pruebas del dominio deben validar:

- comportamiento observable;
- invariantes;
- transiciones de estado;
- generación de Domain Events;
- control de versiones;
- consistencia del Aggregate.

Las pruebas nunca dependen de una base de datos, un framework
o una tecnología específica.

---

# Escenario 1 — Registrar un Citizen

## Dado

No existe un Aggregate con el CitizenId solicitado.

## Cuando

```text
RegisterCitizen
```

## Entonces

- se crea un nuevo Aggregate;
- el estado inicial es **Draft**;
- la versión es **1**;
- se publica:

```text
CitizenRegistered
```

---

# Escenario 2 — Solicitar verificación

## Dado

Un Citizen en estado:

```text
Draft
```

## Cuando

```text
RequestCitizenVerification
```

## Entonces

- el estado cambia a:

```text
PendingVerification
```

- se publica:

```text
CitizenVerificationRequested
```

---

# Escenario 3 — Verificar identidad

## Dado

```text
PendingVerification
```

## Cuando

```text
VerifyCitizen
```

## Entonces

- el estado cambia a:

```text
Verified
```

- la versión aumenta;
- se genera:

```text
CitizenVerified
```

---

# Escenario 4 — Activar Citizen

## Dado

```text
Verified
```

## Cuando

```text
ActivateCitizen
```

## Entonces

```text
State = Active
```

y se publica:

```text
CitizenActivated
```

---

# Escenario 5 — Actualizar perfil

## Dado

Un Citizen activo.

## Cuando

```text
UpdateCitizenProfile
```

## Entonces

- el estado permanece:

```text
Active
```

- aumenta la versión;
- se publica:

```text
CitizenProfileUpdated
```

---

# Escenario 6 — Cambiar dirección

## Dado

Un Citizen activo.

## Cuando

```text
UpdateCitizenAddress
```

## Entonces

- el Value Object Address cambia;
- las invariantes permanecen válidas;
- se publica:

```text
CitizenAddressUpdated
```

---

# Escenario 7 — Suspender Citizen

## Dado

```text
Active
```

## Cuando

```text
SuspendCitizen
```

## Entonces

```text
Suspended
```

y se publica:

```text
CitizenSuspended
```

---

# Escenario 8 — Reactivar Citizen

## Dado

```text
Suspended
```

## Cuando

```text
ReactivateCitizen
```

## Entonces

```text
Active
```

y se genera:

```text
CitizenReactivated
```

---

# Escenario 9 — Desactivar Citizen

## Dado

```text
Active
```

## Cuando

```text
DeactivateCitizen
```

## Entonces

```text
Inactive
```

y se publica:

```text
CitizenDeactivated
```

---

# Escenario 10 — Archivar Citizen

## Dado

```text
Inactive
```

## Cuando

```text
ArchiveCitizen
```

## Entonces

```text
Archived
```

y se publica:

```text
CitizenArchived
```

---

# Escenario 11 — Activación inválida

## Dado

```text
Draft
```

## Cuando

```text
ActivateCitizen
```

## Entonces

La operación es rechazada.

No cambia el estado.

No aumenta la versión.

No existe Domain Event.

---

# Escenario 12 — Modificación sobre Citizen archivado

## Dado

```text
Archived
```

## Cuando

```text
UpdateCitizenProfile
```

## Entonces

La operación es rechazada.

El Aggregate permanece inmutable.

---

# Escenario 13 — Conflicto de concurrencia

## Dado

```text
Version = 7
```

## Cuando

Otro proceso persiste:

```text
Version = 8
```

y posteriormente se intenta guardar la versión 7.

## Entonces

El Repository devuelve:

```text
ConcurrencyConflict
```

No se modifica el Aggregate.

---

# Escenario 14 — Violación de invariante

## Dado

Un Command intenta dejar al Citizen sin identidad válida.

## Cuando

Se ejecuta el comportamiento correspondiente.

## Entonces

La operación es rechazada.

No se persiste ningún cambio.

No se generan eventos.

---

# Escenario 15 — Verificación de permisos

## Dado

Un actor sin autorización.

## Cuando

Intenta ejecutar:

```text
SuspendCitizen
```

## Entonces

La capa de aplicación rechaza el Command.

El Aggregate nunca es invocado.

---

# Escenario 16 — Reconstrucción mediante Event Sourcing

## Dado

La secuencia:

```text
CitizenRegistered

CitizenVerificationRequested

CitizenVerified

CitizenActivated

CitizenAddressUpdated
```

## Cuando

Se reproducen todos los eventos.

## Entonces

El Aggregate reconstruido posee:

```text
State = Active
```

La dirección corresponde a la última actualización.

La versión coincide con el número de eventos aplicados.

---

# Escenario 17 — Reconstrucción de Read Models

## Dado

Una proyección eliminada.

## Cuando

Se ejecuta un replay completo de los Domain Events.

## Entonces

El Read Model se reconstruye íntegramente sin pérdida de
información.

---

# Escenario 18 — Publicación de Integration Events

## Dado

El Aggregate ejecuta correctamente:

```text
ActivateCitizen
```

## Cuando

La transacción es confirmada.

## Entonces

Se publica:

```text
CitizenActivatedIntegrationEvent
```

Nunca antes del commit.

---

# Cobertura Esperada

El conjunto mínimo de pruebas debe cubrir:

- Commands;
- transiciones de estado;
- invariantes;
- permisos;
- versiones;
- Domain Events;
- Integration Events;
- reconstrucción;
- concurrencia;
- consistencia.

---

# Automatización

Estos escenarios deben implementarse como pruebas
automatizadas del dominio.

Cada escenario debe ser:

- independiente;
- repetible;
- determinístico;
- aislado;
- rápido de ejecutar.

---

# Criterios de Aceptación

El Aggregate **Citizen** será considerado conforme cuando:

- todos los escenarios sean exitosos;
- ninguna invariante pueda violarse;
- todas las transiciones respeten la State Machine;
- todos los Commands generen los Domain Events esperados;
- los conflictos de concurrencia sean detectados correctamente;
- los Read Models puedan reconstruirse completamente.

---

# Principios Arquitectónicos

Este conjunto de pruebas sigue:

- Domain-Driven Design (DDD);
- Behavior-Driven Development (BDD);
- CQRS;
- Event Sourcing;
- Clean Architecture;
- Specification by Example.

---

# Definición de Éxito

Los escenarios definidos en este documento constituyen la
especificación ejecutable del Aggregate **Citizen**. Su objetivo
es garantizar que la implementación futura preserve
íntegramente el comportamiento esperado del dominio,
permitiendo evolucionar AURA con seguridad, trazabilidad y alta
confianza en las reglas de negocio.