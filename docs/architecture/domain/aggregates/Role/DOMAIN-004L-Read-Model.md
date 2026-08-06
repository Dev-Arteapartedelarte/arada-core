# DOMAIN-004L — Role Read Model

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
- DOMAIN-004C-Commands.md
- DOMAIN-004D-Domain-Events.md
- DOMAIN-004G-Repository-Contract.md
- DOMAIN-004K-Integration-Events.md
- CORE-014-Read-Model.md

---

# Objetivo

Este documento define el **Read Model** oficial del Aggregate
**Role**.

El Read Model proporciona una representación optimizada para
consultas, independiente del modelo transaccional del Aggregate.
Su propósito es facilitar búsquedas, listados y visualizaciones
sin comprometer la consistencia del modelo de escritura.

---

# Principios

El Read Model sigue los siguientes principios:

- optimizado para lectura;
- desacoplado del Aggregate;
- construido a partir de Domain Events o Integration Events;
- eventual consistente;
- libre de lógica de negocio;
- especializado para consultas.

---

# Responsabilidades

El Read Model permite responder consultas como:

- ¿Qué Roles existen en una Organization?
- ¿Cuáles están activos?
- ¿Qué Roles pertenecen al sistema?
- ¿Qué Roles pueden asignarse actualmente?
- ¿Cuál es la información descriptiva de un Role?
- ¿Cuál es el historial de cambios de un Role?

No ejecuta Commands ni modifica Aggregates.

---

# Modelo Conceptual

```text
RoleReadModel
```

Campos sugeridos:

```text
RoleId

OrganizationId

Name

Code

Description

RoleType

Status

IsSystemRole

Version

CreatedAt

UpdatedAt
```

Los campos pueden ampliarse según las necesidades de consulta,
manteniendo la independencia respecto del Aggregate.

---

# Fuentes de Datos

El Read Model se construye a partir de los siguientes eventos:

```text
RoleCreated

RoleRenamed

RoleDescriptionChanged

RoleActivated

RoleDeactivated

RoleArchived
```

Opcionalmente puede utilizar los correspondientes
Integration Events cuando el modelo de lectura reside en otro
Bounded Context.

---

# Actualización

Cada evento modifica únicamente la proyección de lectura.

Ejemplo:

```text
RoleRenamed

↓

Actualizar Name

↓

Persistir Read Model
```

No se modifica el Aggregate.

---

# Consultas Habituales

## Obtener un Role

```text
RoleId

↓

RoleReadModel
```

---

## Listar Roles por Organization

```text
OrganizationId

↓

Roles[]
```

---

## Listar Roles Activos

Filtro:

```text
Status = Active
```

---

## Buscar por Código

```text
OrganizationId

+

Code

↓

RoleReadModel
```

---

## Buscar por Nombre

```text
OrganizationId

+

Name

↓

RoleReadModel
```

---

## Listar System Roles

Filtro:

```text
IsSystemRole = true
```

---

## Historial Conceptual

El historial puede reconstruirse utilizando:

```text
RoleCreated

↓

RoleActivated

↓

RoleRenamed

↓

RoleArchived
```

o bien almacenando una proyección específica de auditoría.

---

# Ejemplo de Registro

```text
RoleId:
ROLE-001

OrganizationId:
ORG-001

Name:
Presidente

Code:
PRESIDENT

Description:
Máxima autoridad de la organización.

RoleType:
Executive

Status:
Active

IsSystemRole:
false

Version:
4
```

---

# Consistencia

El Read Model es:

```text
Eventually Consistent
```

Entre la ejecución de un Command y la actualización del modelo
de lectura puede existir un breve desfase.

Este comportamiento es esperado en una arquitectura CQRS.

---

# Sincronización

Flujo conceptual:

```text
Command

↓

Aggregate

↓

Domain Event

↓

Projector

↓

Role Read Model
```

En escenarios distribuidos:

```text
Integration Event

↓

Projector

↓

Read Database
```

---

# Índices Recomendados

Para optimizar consultas se recomienda indexar:

```text
RoleId

OrganizationId

Code

Name

Status

IsSystemRole
```

La selección de índices dependerá de la tecnología utilizada.

---

# Eliminación

Los Roles no se eliminan físicamente.

Cuando ocurre:

```text
RoleArchived
```

el Read Model debe reflejar:

```text
Status = Archived
```

La información histórica permanece disponible.

---

# Seguridad

El Read Model:

- no contiene credenciales;
- no almacena secretos;
- no reemplaza la autorización;
- puede exponer únicamente la información necesaria para las consultas.

El acceso continúa sujeto a las políticas de autorización de la
plataforma.

---

# Compatibilidad Arquitectónica

Este modelo es compatible con:

- Domain-Driven Design (DDD);
- CQRS;
- Event Sourcing;
- Event-Driven Architecture;
- Clean Architecture.

---

# Definición de Éxito

El **Read Model** del Aggregate **Role** proporciona una vista
eficiente, desacoplada y especializada para consultas sobre los
cargos organizacionales. Al derivarse exclusivamente de los
eventos del dominio, garantiza una representación consistente,
escalable y preparada para soportar búsquedas, auditorías y
procesos analíticos dentro del ecosistema AURA, sin afectar el
modelo transaccional del Aggregate.