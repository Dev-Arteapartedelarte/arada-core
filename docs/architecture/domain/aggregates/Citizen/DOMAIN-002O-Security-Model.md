# DOMAIN-002O — Citizen Security Model

Versión: 1.1

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
- DOMAIN-002F-Permissions.md
- DOMAIN-002G-Repository-Contract.md
- DOMAIN-002J-Consistency-Boundary.md
- DOMAIN-002K-Integration-Events.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Este documento define el modelo de seguridad del Aggregate
**Citizen**.

Su propósito es proteger la identidad digital de los ciudadanos
sin introducir dependencias de infraestructura dentro del
dominio.

El Aggregate únicamente protege las reglas de negocio.

La autenticación, autorización y mecanismos criptográficos
pertenecen a otras capas de la arquitectura.

---

# Principios

El modelo de seguridad sigue los siguientes principios:

- Security by Design.
- Privacy by Design.
- Least Privilege.
- Defense in Depth.
- Zero Trust.
- Fail Secure.
- Auditability.
- Separation of Concerns.

---

# Responsabilidades del Aggregate

El Aggregate Citizen es responsable de:

- proteger sus invariantes;
- impedir transiciones inválidas;
- impedir modificaciones ilegales;
- preservar la integridad del estado;
- garantizar consistencia.

No es responsable de:

- autenticar usuarios;
- validar JWT;
- validar OAuth2;
- gestionar sesiones;
- cifrar comunicaciones;
- administrar certificados;
- controlar firewalls;
- enviar notificaciones.

---

# Modelo Conceptual

```text
Identity Provider

        │

Authentication

        │

Authorization

        │

Application Service

        │

Citizen Aggregate

        │

Repository
```

El Aggregate solamente recibe Commands previamente autorizados.

---

# Identidad

Cada Citizen posee una identidad única.

```text
CitizenId
```

La identidad:

- es inmutable;
- nunca se reutiliza;
- nunca cambia durante el ciclo de vida.

---

# Integridad

Toda modificación debe preservar:

- identidad;
- versión;
- estado;
- invariantes;
- consistencia.

No pueden existir estados parcialmente válidos.

---

# Autenticación

La autenticación pertenece a un Identity Provider adapter externo al
dominio.

Puede implementarse mediante tecnologías como:

- OpenID Connect;
- OAuth2;
- Passkeys;
- ClavesÚnica u otros proveedores de identidad;
- autenticación multifactor (MFA).

El Aggregate permanece completamente independiente de estas
tecnologías.

---

# Autorización

La autorización ocurre antes de ejecutar cualquier Command.

La capa de aplicación verifica:

- identidad del actor;
- roles;
- permisos;
- políticas;
- restricciones territoriales;
- reglas organizacionales.

Si la autorización falla, el Aggregate nunca es invocado.

---

# Protección de Datos Personales

El Aggregate gestiona información personal que debe tratarse de
acuerdo con los principios de minimización y finalidad.

Ejemplos:

- nombre;
- correo electrónico;
- teléfono;
- dirección;
- preferencias de idioma;
- consentimientos.

Los datos sensibles sólo deben exponerse cuando exista una
justificación de negocio y autorización explícita.

---

# Consentimiento

El Citizen controla sus consentimientos mediante Commands del
dominio.

Ejemplos:

```text
AcceptPrivacyPolicy

WithdrawConsent
```

Toda modificación genera Domain Events para mantener
trazabilidad.

---

# Auditoría

Toda operación relevante debe registrar:

- ActorId;
- CitizenId;
- Command;
- fecha y hora;
- resultado;
- dirección de origen (si aplica);
- CorrelationId;
- CausationId.

La auditoría pertenece a un Bounded Context independiente.

El Aggregate no almacena registros de auditoría.

---

# Integración Segura

Los Integration Events nunca deben incluir:

- contraseñas;
- tokens;
- claves privadas;
- secretos;
- información biométrica;
- datos personales innecesarios.

Los eventos deben contener únicamente la información mínima
requerida para la integración.

---

# Comunicación entre Contextos

La comunicación entre Bounded Contexts debe realizarse mediante:

- Domain Events;
- Integration Events;
- APIs protegidas;
- mensajería autenticada.

Nunca mediante acceso directo a las bases de datos de otro
contexto.

---

# Concurrencia

El modelo utiliza:

```text
Optimistic Concurrency Control
```

Esto evita:

- sobrescrituras accidentales;
- pérdida de información;
- inconsistencias por escritura concurrente.

---

# Protección frente a Errores

Ante cualquier condición inesperada:

- la operación se cancela;
- no se modifica el Aggregate;
- no se generan Domain Events;
- la transacción se revierte.

---

# Gestión de Secretos

El Aggregate nunca conoce:

- contraseñas;
- claves API;
- certificados;
- secretos criptográficos;
- credenciales de infraestructura.

Toda gestión de secretos pertenece a la infraestructura.

---

# Cifrado

El dominio es independiente del mecanismo de cifrado.

La infraestructura podrá utilizar:

- TLS;
- cifrado en reposo;
- cifrado de bases de datos;
- cifrado de discos;
- HSM;
- KMS.

Nada de esto modifica el comportamiento del Aggregate.

---

# Trazabilidad

Toda operación debe poder reconstruirse mediante:

```text
Commands

↓

Domain Events

↓

Integration Events

↓

Audit Logs
```

La combinación de estos elementos permite reconstruir la
historia completa del Citizen.

---

# Cumplimiento Normativo

El modelo está diseñado para facilitar el cumplimiento de:

- Ley N.º 19.628 sobre Protección de la Vida Privada (Chile);
- futuras leyes chilenas de protección de datos personales;
- principios del Reglamento General de Protección de Datos
  (GDPR) como referencia arquitectónica;
- normativas municipales aplicables;
- políticas internas de AURA.

La adaptación normativa específica corresponde a la capa de
aplicación y a la infraestructura.

---

# Compatibilidad con FIWARE

La integración con FIWARE deberá realizarse mediante APIs o
Integration Events.

El Aggregate nunca interactúa directamente con:

- Orion Context Broker;
- Keyrock;
- Wilma PEP Proxy;
- IoT Agents.

Estas integraciones pertenecen a la infraestructura del
ecosistema AURA.

---

# Compatibilidad con Event Sourcing

El historial de eventos constituye un registro inmutable.

Los eventos publicados nunca deben alterarse ni eliminarse.

Las correcciones se realizan mediante nuevos eventos del
dominio.

---

# Compatibilidad con CQRS

Las políticas de acceso al lado de lectura pueden diferir del
lado de escritura.

Los Read Models podrán aplicar:

- anonimización;
- filtrado por rol;
- ocultamiento de atributos;
- vistas parciales.

Sin modificar el Aggregate.

---

# Amenazas Mitigadas

Este modelo reduce el riesgo de:

- modificaciones no autorizadas;
- escalamiento de privilegios;
- corrupción del estado del Aggregate;
- pérdida de trazabilidad;
- exposición innecesaria de datos personales;
- acoplamiento entre seguridad e infraestructura.

---

# Principios Arquitectónicos

El modelo sigue:

- Domain-Driven Design (DDD);
- Clean Architecture;
- Hexagonal Architecture;
- Zero Trust Architecture;
- Privacy by Design;
- Security by Design;
- SOLID;
- Dependency Inversion Principle.

---

# Definición de Éxito

El modelo de seguridad del Aggregate **Citizen** garantiza que
las identidades digitales del ecosistema AURA se gestionen de
forma consistente, trazable y desacoplada de la infraestructura.
El Aggregate protege exclusivamente las reglas del dominio,
mientras que la autenticación, autorización, cifrado y
comunicaciones seguras permanecen en capas especializadas,
permitiendo que la plataforma evolucione de forma segura desde
escenarios comunitarios hasta despliegues municipales,
regionales y nacionales.