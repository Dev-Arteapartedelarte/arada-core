# DOMAIN-002 — Citizen Aggregate

Versión: 1.1

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Citizen Management

Aggregate:
Citizen

Autor:
ARADA

Documentos Relacionados:

- CORE-002-Bounded-Context-Map.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-006-Domain-Invariants.md
- CORE-007-Strategic-Design.md
- DOMAIN-001-Aggregate.md

---

# Objetivo

El Aggregate **Citizen** representa a una persona que participa
en el ecosistema AURA.

Constituye la identidad cívica utilizada por la plataforma
para relacionar organizaciones, membresías, territorios,
participación ciudadana, documentos, votaciones e
integraciones con sistemas externos.

Citizen es uno de los Aggregates fundamentales del dominio,
junto con Organization.

---

# Propósito

El Aggregate es responsable de:

- representar una identidad cívica;
- administrar su ciclo de vida;
- mantener su estado de participación;
- garantizar la unicidad de la identidad;
- publicar eventos relevantes;
- proteger la consistencia de la información.

No administra autenticación ni credenciales.

---

# Responsabilidades

Citizen es responsable de:

- identidad del ciudadano;
- información personal permitida por el dominio;
- estado de actividad;
- pertenencia al ecosistema;
- historial de cambios relevantes;
- emisión de Domain Events.

No es responsable de:

- autenticación;
- autorización;
- sesiones;
- tokens;
- organizaciones;
- votaciones;
- membresías;
- documentos;
- notificaciones.

---

# Identidad

La identidad del Aggregate está determinada por:

```text
CitizenId
```

Este identificador:

- es global;
- es inmutable;
- nunca cambia;
- nunca se reutiliza.

No depende del almacenamiento.

---

# Entidades Internas

El Aggregate puede contener entidades como:

```text
Citizen

PrimaryAddress

EmergencyContact

CitizenPreferences
```

Estas entidades no existen fuera del Aggregate.

---

# Value Objects

Entre los Value Objects del dominio se consideran:

```text
FullName

Email

PhoneNumber

NationalIdentifier

BirthDate

Address

Locale

Language

ProfilePhoto

CitizenStatus
```

Todos son inmutables.

---

# Estado

El ciclo de vida del ciudadano se representa mediante
CitizenStatus.

Estados iniciales propuestos:

```text
Draft

PendingVerification

Active

Inactive

Suspended

Archived
```

Las transiciones válidas serán definidas en:

```text
DOMAIN-002B-State-Machine.md
```

---

# Invariantes

El Aggregate mantiene, entre otras, las siguientes
invariantes:

- CitizenId nunca cambia.
- NationalIdentifier es único.
- Email es único dentro del dominio.
- Un ciudadano archivado no puede reactivarse sin un
  proceso explícito.
- No existen dos ciudadanos activos con la misma identidad.
- Todo cambio incrementa la versión del Aggregate.

Las reglas completas se documentarán en:

```text
DOMAIN-002E-Invariants.md
```

---

# Relaciones

Citizen mantiene referencias a otros Aggregates.

```text
Citizen
    │
    ├──────── Organization
    │
    ├──────── Membership
    │
    ├──────── Territory
    │
    ├──────── Participation
    │
    ├──────── Proposal
    │
    ├──────── Assembly
    │
    ├──────── Voting
    │
    ├──────── Notification
    │
    └──────── Document
```

Nunca almacena Aggregates completos.

---

# Consistencia

Citizen constituye un límite de consistencia.

Todas sus modificaciones deben ocurrir dentro de una única
transacción lógica.

No existen actualizaciones parciales.

---

# Eventos

Citizen genera y registra Domain Events cuando cambia su estado.

Ejemplos:

```text
CitizenRegistered

CitizenVerified

CitizenActivated

CitizenSuspended

CitizenArchived

CitizenProfileUpdated
```

Los eventos completos se especificarán en:

```text
DOMAIN-002D-Domain-Events.md
```

---

# Commands

El Aggregate responde a Commands como:

```text
RegisterCitizen

VerifyCitizen

ActivateCitizen

SuspendCitizen

ArchiveCitizen

UpdateCitizenProfile
```

La especificación formal se desarrollará en:

```text
DOMAIN-002C-Commands.md
```

---

# Integración

Citizen puede sincronizarse con:

- Registro Civil;
- plataformas municipales;
- proveedores de identidad;
- sistemas Smart City;
- plataformas de participación ciudadana.

Estas integraciones se realizan mediante Integration Events,
nunca mediante acceso directo al Aggregate.

---

# Versionado

Citizen utiliza Versionado Optimista.

Cada modificación incrementa:

```text
Version
```

El repositorio valida la concurrencia antes de persistir.

---

# Seguridad

Citizen nunca almacena:

- contraseñas;
- tokens;
- certificados;
- claves privadas;
- secretos criptográficos.

La autenticación pertenece a un Identity Provider externo accedido por
un puerto de Application.

---

# Principios Arquitectónicos

Citizen cumple:

- Domain Driven Design.
- Clean Architecture.
- Hexagonal Architecture.
- SOLID.
- Event Driven Architecture.
- CQRS Ready.
- Event Sourcing Compatible.

---

# Dependencias

Citizen depende únicamente de:

- Shared Kernel;
- Value Objects;
- Domain Events;
- Repository Contracts.

Nunca depende de:

- Infrastructure;
- Frameworks;
- Bases de datos;
- HTTP;
- OAuth;
- JWT;
- React;
- FastAPI;
- Django.

---

# Relaciones Estratégicas

Citizen es consumido por:

- Organization Management
- Membership Management
- Participation
- Governance
- Voting
- Documents
- Notifications
- Analytics
- Smart City Integration

Es uno de los Aggregates con mayor número de relaciones del
dominio.

---

# Objetivos de Diseño

El Aggregate busca garantizar:

- identidad única;
- consistencia del estado;
- independencia tecnológica;
- trazabilidad;
- evolución controlada;
- interoperabilidad.

---

# Definición de Éxito

El Aggregate **Citizen** representa la identidad cívica oficial
del ecosistema AURA. Actúa como el punto de referencia para la
participación de las personas en organizaciones, procesos
democráticos, servicios municipales e integraciones Smart City,
manteniendo un modelo consistente, desacoplado y preparado para
una arquitectura distribuida.