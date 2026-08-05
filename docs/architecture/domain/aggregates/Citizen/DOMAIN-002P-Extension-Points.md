# DOMAIN-002P — Citizen Extension Points

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
- DOMAIN-002C-Commands.md
- DOMAIN-002D-Domain-Events.md
- DOMAIN-002K-Integration-Events.md
- DOMAIN-002L-Read-Model.md
- CORE-007-Strategic-Design.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Este documento identifica los puntos oficiales de extensión
(Extension Points) del Aggregate **Citizen**.

Los Extension Points permiten incorporar nuevas capacidades al
dominio sin modificar el núcleo del Aggregate, respetando los
principios de Domain-Driven Design (DDD), Open/Closed Principle
y Clean Architecture.

El Aggregate debe permanecer estable mientras el ecosistema
AURA evoluciona mediante nuevos módulos, Bounded Contexts e
integraciones.

---

# Principios

Toda extensión debe cumplir los siguientes principios:

- no romper las invariantes del Aggregate;
- no modificar el comportamiento histórico;
- preservar el lenguaje ubicuo;
- mantener bajo acoplamiento;
- ser compatible con CQRS y Event Sourcing;
- evolucionar mediante composición y eventos.

---

# Filosofía

El Aggregate **Citizen** representa la identidad cívica de una
persona.

Las capacidades relacionadas con participación, identidad,
beneficios, territorios o integraciones no deben agregarse al
Aggregate si pertenecen a otro dominio.

La evolución ocurre alrededor del Aggregate, no dentro de él.

---

# Punto de Extensión 1 — Nuevos Commands

Es posible incorporar nuevos Commands cuando representen un
nuevo comportamiento del dominio.

Ejemplos:

```text
UpdateCitizenAvatar

ChangePreferredLanguage

RegisterEmergencyContact

RequestDataExport

DeletePersonalData

AcceptUpdatedPrivacyPolicy
```

Todo nuevo Command deberá:

- respetar las invariantes;
- actualizar la versión cuando corresponda;
- generar Domain Events;
- mantener la consistencia del Aggregate.

---

# Punto de Extensión 2 — Nuevos Domain Events

La evolución funcional puede introducir nuevos Domain Events.

Ejemplos:

```text
CitizenAvatarUpdated

CitizenLanguageChanged

EmergencyContactRegistered

CitizenDataExportRequested

CitizenPrivacyPolicyAccepted
```

Los eventos existentes nunca se modifican.

---

# Punto de Extensión 3 — Nuevos Integration Events

El ecosistema puede requerir nuevos contratos de integración.

Ejemplos:

```text
CitizenSyncedToMunicipality

CitizenImportedFromRegistry

CitizenLinkedToIdentityProvider

CitizenParticipationScoreUpdated
```

Cada contrato debe:

- estar versionado;
- ser estable;
- permanecer desacoplado del modelo interno.

---

# Punto de Extensión 4 — Nuevos Read Models

Pueden crearse nuevas proyecciones sin modificar el Aggregate.

Ejemplos:

```text
CitizenPublicProfile

CitizenParticipationHistory

CitizenEngagementDashboard

CitizenAccessibilityProfile

CitizenMunicipalStatistics
```

Todas las proyecciones deben alimentarse exclusivamente de
Domain Events o Integration Events.

---

# Punto de Extensión 5 — Nuevos Value Objects

El Aggregate puede enriquecerse mediante nuevos Value Objects
cuando aporten significado al dominio.

Ejemplos:

```text
EmergencyContact

AccessibilityPreferences

NotificationPreferences

DigitalIdentity

PreferredCommunicationChannel
```

Cada Value Object debe ser:

- inmutable;
- autoconsistente;
- libre de identidad propia.

---

# Punto de Extensión 6 — Nuevas Políticas

Las políticas del dominio pueden crecer sin alterar el núcleo.

Ejemplos:

```text
CitizenEligibilityPolicy

CitizenVerificationPolicy

CitizenConsentPolicy

CitizenParticipationPolicy
```

Las políticas encapsulan reglas complejas reutilizables por
Application Services y Domain Services.

---

# Punto de Extensión 7 — Nuevas Integraciones

El Aggregate puede integrarse con nuevos ecosistemas mediante
Integration Events.

Ejemplos:

- FIWARE;
- plataformas municipales;
- sistemas regionales;
- plataformas nacionales;
- sistemas de identidad;
- motores de analítica;
- servicios GIS;
- plataformas de participación ciudadana.

La integración nunca debe realizarse desde el Aggregate.

---

# Punto de Extensión 8 — Nuevos Bounded Contexts

El crecimiento de AURA permitirá incorporar nuevos contextos
que colaboren con Citizen.

Ejemplos:

```text
Identity

Membership

Territory

Assembly

Voting

Proposal

Notification

Document

Credential

Audit

Analytics

Volunteer

Benefit

Emergency
```

La colaboración se realiza mediante eventos y referencias por
identidad.

---

# Punto de Extensión 9 — Automatización

Los eventos del Aggregate pueden activar procesos automáticos.

Ejemplos:

```text
CitizenVerified

↓

Create Membership

↓

Assign Default Role

↓

Send Welcome Notification

↓

Update Analytics
```

Estas automatizaciones pertenecen a la capa de aplicación o a
procesos de orquestación.

---

# Punto de Extensión 10 — IA y Automatización Inteligente

El dominio podrá incorporar capacidades de inteligencia
artificial sin modificar el Aggregate.

Ejemplos:

- asistentes ciudadanos;
- clasificación automática de solicitudes;
- recomendación de organizaciones;
- análisis de participación;
- detección de abandono;
- predicción de necesidades territoriales.

La IA consumirá Read Models e Integration Events.

Nunca accederá directamente al Aggregate.

---

# Restricciones

No constituyen puntos de extensión:

- modificar CitizenId;
- alterar la máquina de estados existente;
- romper invariantes;
- eliminar Domain Events históricos;
- cambiar el significado de Commands ya publicados;
- introducir dependencias de infraestructura en el dominio.

---

# Compatibilidad con CQRS

Las extensiones del lado de lectura pueden evolucionar
independientemente del lado de escritura.

Nuevas consultas no requieren modificar el Aggregate.

---

# Compatibilidad con Event Sourcing

Toda nueva funcionalidad debe expresarse mediante nuevos
Domain Events.

Los eventos históricos permanecen inmutables y continúan siendo
la fuente oficial de verdad.

---

# Estrategia de Evolución

La evolución del Aggregate seguirá el siguiente principio:

```text
Nuevos requisitos

        │

        ▼

Nuevos Commands

        │

        ▼

Nuevos Domain Events

        │

        ▼

Nuevos Read Models

        │

        ▼

Nuevas Integraciones

        │

        ▼

Nuevo Valor para el Ecosistema
```

El núcleo del Aggregate permanece estable durante todo el
proceso.

---

# Principios Arquitectónicos

Los Extension Points siguen:

- Domain-Driven Design (DDD);
- Open/Closed Principle;
- Clean Architecture;
- Hexagonal Architecture;
- CQRS;
- Event Sourcing;
- Event-Driven Architecture;
- Low Coupling;
- High Cohesion.

---

# Definición de Éxito

El Aggregate **Citizen** dispone de una estrategia explícita de
extensión que permite incorporar nuevas capacidades funcionales
sin alterar su núcleo conceptual. Gracias a estos puntos de
extensión, AURA puede evolucionar desde una plataforma para
organizaciones comunitarias hacia un ecosistema interoperable
de participación ciudadana, ciudades inteligentes e integración
con servicios municipales, regionales y nacionales, preservando
la estabilidad del dominio y la coherencia arquitectónica.