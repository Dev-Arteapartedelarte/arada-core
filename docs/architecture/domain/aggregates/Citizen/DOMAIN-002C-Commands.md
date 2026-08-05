# DOMAIN-002C — Citizen Commands

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
- DOMAIN-002D-Domain-Events.md
- DOMAIN-002E-Invariants.md
- CORE-005-Domain-Events.md

---

# Objetivo

Este documento define los Commands oficiales que pueden
modificar el estado del Aggregate Citizen.

Los Commands representan solicitudes explícitas de cambio
de estado. No contienen lógica de negocio ni describen el
resultado esperado; únicamente expresan una intención.

Toda modificación del Aggregate debe originarse mediante un
Command válido.

---

# Principios

Los Commands cumplen los siguientes principios:

- representan intención;
- son inmutables;
- poseen un único propósito;
- son validados antes de ejecutarse;
- pueden rechazarse;
- nunca representan consultas.

---

# Flujo General

```text
Actor

      │

      ▼

Application Service

      │

      ▼

Command

      │

      ▼

Citizen Aggregate

      │

      ▼

Domain Validation

      │

      ▼

Domain Events
```

---

# Commands Oficiales

El Aggregate Citizen reconoce los siguientes Commands.

```text
RegisterCitizen

RequestCitizenVerification

VerifyCitizen

ActivateCitizen

SuspendCitizen

ReactivateCitizen

DeactivateCitizen

ArchiveCitizen

UpdateCitizenProfile

UpdateCitizenContactInformation

UpdateCitizenAddress

ChangePreferredLanguage

AcceptPrivacyPolicy

WithdrawConsent
```

---

# RegisterCitizen

## Propósito

Crear una nueva identidad cívica.

## Estado requerido

No existe Aggregate previo.

## Estado resultante

```text
Draft
```

## Eventos esperados

```text
CitizenRegistered
```

---

# RequestCitizenVerification

## Propósito

Solicitar el proceso de validación de identidad.

## Estado requerido

```text
Draft
```

## Estado resultante

```text
PendingVerification
```

## Eventos

```text
CitizenVerificationRequested
```

---

# VerifyCitizen

## Propósito

Confirmar la identidad del ciudadano.

## Estado requerido

```text
PendingVerification
```

## Estado resultante

```text
Verified
```

## Eventos

```text
CitizenVerified
```

---

# ActivateCitizen

## Propósito

Habilitar la participación del ciudadano.

## Estado requerido

```text
Verified
```

## Estado resultante

```text
Active
```

## Eventos

```text
CitizenActivated
```

---

# SuspendCitizen

## Propósito

Suspender temporalmente al ciudadano.

## Estado requerido

```text
Active
```

## Estado resultante

```text
Suspended
```

## Eventos

```text
CitizenSuspended
```

---

# ReactivateCitizen

## Propósito

Restablecer la participación de un ciudadano suspendido.

## Estado requerido

```text
Suspended
```

## Estado resultante

```text
Active
```

## Eventos

```text
CitizenReactivated
```

---

# DeactivateCitizen

## Propósito

Retirar temporalmente al ciudadano del ecosistema.

## Estado requerido

```text
Active
```

## Estado resultante

```text
Inactive
```

## Eventos

```text
CitizenDeactivated
```

---

# ArchiveCitizen

## Propósito

Finalizar el ciclo de vida del Aggregate.

## Estados permitidos

```text
Verified

Active

Suspended

Inactive
```

## Estado resultante

```text
Archived
```

## Eventos

```text
CitizenArchived
```

---

# UpdateCitizenProfile

## Propósito

Actualizar la información general del ciudadano.

## Estado requerido

```text
Verified

Active

Suspended
```

## Estado

No cambia.

## Eventos

```text
CitizenProfileUpdated
```

---

# UpdateCitizenContactInformation

## Propósito

Modificar medios oficiales de contacto.

Ejemplos:

- correo electrónico;
- teléfono;
- canales de comunicación.

## Estado

No cambia.

## Eventos

```text
CitizenContactInformationUpdated
```

---

# UpdateCitizenAddress

## Propósito

Actualizar el domicilio del ciudadano.

## Estado

No cambia.

## Eventos

```text
CitizenAddressUpdated
```

---

# ChangePreferredLanguage

## Propósito

Modificar el idioma preferido del ciudadano.

## Estado

No cambia.

## Eventos

```text
CitizenLanguageChanged
```

---

# AcceptPrivacyPolicy

## Propósito

Registrar la aceptación de una política de privacidad o de
tratamiento de datos.

## Estado

No cambia.

## Eventos

```text
CitizenPrivacyPolicyAccepted
```

---

# WithdrawConsent

## Propósito

Registrar el retiro del consentimiento previamente otorgado
por el ciudadano cuando la normativa lo permita.

## Estado

No cambia necesariamente.

Puede activar procesos adicionales definidos por políticas
del dominio.

## Eventos

```text
CitizenConsentWithdrawn
```

---

# Reglas Generales

Todo Command debe cumplir:

- AggregateId válido;
- Version válida;
- autorización previa;
- invariantes satisfechas;
- Value Objects válidos;
- consistencia del Aggregate.

---

# Commands Rechazados

El Aggregate debe rechazar Commands cuando:

- el estado actual no permite la transición;
- el Aggregate está archivado;
- existe conflicto de versión;
- faltan permisos;
- existen datos inválidos;
- se incumplen invariantes.

---

# Idempotencia

Los Application Services deben garantizar que un mismo
Command no produzca efectos duplicados cuando sea recibido
más de una vez.

La estrategia concreta depende de la infraestructura y no
forma parte del Aggregate.

---

# Relación con Domain Events

Todo Command exitoso genera uno o más Domain Events.

```text
Command

        │

        ▼

Aggregate

        │

        ▼

Domain Event(s)
```

Un Command nunca publica eventos directamente.

---

# Relación con CQRS

Los Commands pertenecen exclusivamente al lado de escritura
(Command Side).

No pueden utilizarse para consultas ni para construir
proyecciones.

---

# Compatibilidad con Event Sourcing

Cada Command representa el origen de una nueva secuencia de
Domain Events que permitirá reconstruir posteriormente el
estado del Aggregate.

---

# Evolución

Nuevos Commands podrán incorporarse sin modificar los ya
existentes, siempre que:

- respeten el Ubiquitous Language;
- no violen las invariantes;
- mantengan la consistencia del Aggregate;
- preserven la compatibilidad con versiones anteriores.

---

# Definición de Éxito

Los Commands del Aggregate Citizen constituyen la única
interfaz válida para modificar una identidad cívica dentro
del ecosistema AURA. Expresan intenciones de negocio de forma
explícita, desacoplada y consistente, permitiendo que toda
evolución del Aggregate sea validable, auditable y compatible
con arquitecturas basadas en eventos.