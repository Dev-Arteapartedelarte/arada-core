# DOMAIN-004P — Role Extension Points

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Authorization Management

Aggregate:
Role

Documentos relacionados:

- DOMAIN-004-Aggregate.md
- DOMAIN-004D-Domain-Events.md
- DOMAIN-004F-Permissions.md
- DOMAIN-004K-Integration-Events.md
- DOMAIN-005-Aggregate.md
- CORE-018-Extension-Points.md

---

# Objetivo

Este documento define los puntos oficiales de extensión
(Extension Points) del Aggregate **Role**.

Los puntos de extensión permiten evolucionar el dominio sin
modificar el núcleo del Aggregate, facilitando la incorporación
de nuevas capacidades, integraciones y políticas específicas
para distintas organizaciones, municipios o despliegues de
AURA.

---

# Principios

Las extensiones del Aggregate deben cumplir los siguientes
principios:

- Open/Closed Principle;
- compatibilidad hacia atrás;
- desacoplamiento del dominio;
- preservación de invariantes;
- independencia tecnológica;
- extensibilidad mediante eventos.

---

# Filosofía

El Aggregate **Role** representa un cargo organizacional.

Su responsabilidad termina cuando:

- mantiene su identidad;
- administra su ciclo de vida;
- protege sus invariantes;
- publica los eventos correspondientes.

Toda funcionalidad adicional debe implementarse fuera del
Aggregate.

---

# Puntos Oficiales de Extensión

El Aggregate permite extensiones mediante:

```text
Commands

↓

Domain Events

↓

Integration Events

↓

Application Services

↓

Policies

↓

Read Models
```

Ninguna extensión modifica directamente la lógica interna del
Aggregate.

---

# Extensión mediante Application Services

Los Application Services pueden:

- validar reglas organizacionales;
- consultar otros Aggregates;
- coordinar transacciones;
- invocar múltiples Repositories;
- interactuar con servicios externos.

Ejemplo:

```text
CreateRole

↓

Application Service

↓

Validate Organization

↓

Validate Permissions

↓

Role Aggregate
```

---

# Extensión mediante Domain Policies

Las políticas del dominio permiten introducir reglas variables
sin alterar el Aggregate.

Ejemplos:

- máximo de Roles por Organization;
- nomenclatura obligatoria;
- restricciones por tipo de organización;
- Roles reservados;
- Roles temporales.

Las Policies deben ser evaluadas antes de ejecutar el Command.

---

# Extensión mediante Domain Events

Cada Domain Event puede originar nuevos comportamientos.

Ejemplo:

```text
RoleCreated

↓

Audit

↓

Notification

↓

Search Index

↓

Metrics
```

El Aggregate permanece desacoplado de los consumidores.

---

# Extensión mediante Integration Events

Los Integration Events permiten integrar AURA con plataformas
externas.

Ejemplos:

```text
RoleActivatedIntegrationEvent
```

Consumidores posibles:

- FIWARE;
- IAM corporativo;
- motores BPM;
- sistemas municipales;
- plataformas analíticas.

---

# Extensión mediante Read Models

Pueden construirse múltiples proyecciones especializadas.

Ejemplos:

```text
Roles por Organization

Roles Activos

System Roles

Roles por Tipo

Roles Archivados

Roles para Reportes
```

Cada Read Model mantiene su propio ciclo de actualización.

---

# Extensión mediante Metadata

Las implementaciones podrán incorporar atributos adicionales
mediante mecanismos de metadatos.

Ejemplos:

```text
Color

DisplayOrder

Category

Tags

Icon

Visibility
```

Estas propiedades:

- no modifican las invariantes;
- no alteran la identidad del Aggregate;
- no afectan el comportamiento esencial del dominio.

---

# Extensión mediante Catálogos

El dominio puede incorporar nuevos catálogos asociados al Role.

Ejemplos:

- clasificación organizacional;
- niveles jerárquicos;
- áreas funcionales;
- familias de Roles.

Estos catálogos permanecen fuera del Aggregate y son
referenciados mediante identificadores.

---

# Extensión mediante Permission

El Aggregate **Permission** amplía funcionalmente al Aggregate
Role.

Relación conceptual:

```text
Role

↓

Permission

↓

Authorization
```

El Role nunca almacena directamente las Permissions.

---

# Extensión mediante Membership

Un mismo Role puede asignarse a múltiples Memberships.

```text
Role

↓

Membership
```

La asignación pertenece al Aggregate **Membership**, preservando
la independencia entre Aggregates.

---

# Extensión mediante Integraciones Externas

El Aggregate puede integrarse con:

- FIWARE;
- Keyrock;
- Keycloak;
- Active Directory;
- LDAP;
- motores BPM;
- plataformas Smart City;
- sistemas ERP;
- sistemas GIS;
- plataformas de auditoría.

Siempre mediante eventos o servicios de aplicación.

---

# Extensiones No Permitidas

No está permitido:

- modificar invariantes del Aggregate;
- acceder directamente al Repository desde sistemas externos;
- alterar la máquina de estados;
- modificar la identidad del Role;
- omitir la validación de Version;
- publicar eventos antes del commit.

---

# Compatibilidad Evolutiva

Las nuevas versiones del Aggregate deben preservar:

- `RoleId`;
- `OrganizationId`;
- Commands existentes;
- Domain Events existentes;
- Integration Events versionados;
- compatibilidad con Read Models.

Las ampliaciones incompatibles deberán introducir nuevas
versiones de contrato.

---

# Gobernanza

Toda nueva extensión deberá:

1. documentarse en la arquitectura del dominio;
2. respetar las invariantes del Aggregate;
3. mantener compatibilidad con el modelo de autorización;
4. incorporar escenarios de prueba;
5. definir eventos cuando corresponda;
6. actualizar el versionado del contrato si modifica interfaces públicas.

---

# Compatibilidad Arquitectónica

Este modelo es compatible con:

- Domain-Driven Design (DDD);
- Open/Closed Principle;
- Clean Architecture;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing;
- Plugin Architecture;
- Hexagonal Architecture.

---

# Definición de Éxito

El Aggregate **Role** proporciona puntos de extensión claramente definidos que permiten evolucionar el ecosistema AURA sin comprometer la estabilidad del dominio. La separación entre el núcleo del Aggregate y sus mecanismos de extensión facilita la incorporación de nuevas capacidades, integraciones y políticas organizacionales, manteniendo un modelo desacoplado, versionable y preparado para el crecimiento de la plataforma.