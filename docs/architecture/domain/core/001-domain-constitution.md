# ============================================================
# ARADA
# ============================================================
#
# Proyecto:
# AURA Core
#
# Unidad:
# CORE-001
#
# Documento:
# Domain Constitution
#
# Ruta:
# docs/architecture/CORE-001-domain-constitution.md
#
# Estado:
# Ratificado
#
# Versión:
# 1.0
#
# ADR:
# ADR-000
#
# ============================================================

# CORE-001 — Domain Constitution

## 1. Propósito

AURA Core es el núcleo de dominio de la plataforma ARADA.

Su responsabilidad consiste en modelar el comportamiento de las organizaciones,
sus procesos, actores, eventos y relaciones, de forma completamente desacoplada
de cualquier tecnología específica.

El dominio constituye el activo principal del proyecto.

Toda decisión arquitectónica deberá preservar su independencia.

---

# 2. Principios Fundamentales

## 2.1 El dominio es el centro

Toda dependencia apunta hacia el dominio.

Nunca al revés.

El dominio jamás conoce:

- React
- Next.js
- FastAPI
- Django
- PostgreSQL
- MongoDB
- REST
- GraphQL
- Docker
- Kubernetes
- Redis

El dominio únicamente conoce conceptos del negocio.

---

## 2.2 Lenguaje Ubicuo

Todos los nombres utilizados deberán pertenecer al lenguaje del dominio.

Ejemplos:

✔ Organization

✔ Member

✔ Assembly

✔ Vote

✔ Proposal

✔ Neighborhood

✔ Process

Nunca utilizar nombres tecnológicos como:

Controller

DTO

Model

Schema

DatabaseEntity

APIResponse

---

## 2.3 El dominio no posee Frameworks

Frameworks son detalles.

El dominio no depende de detalles.

Los detalles dependen del dominio.

---

## 2.4 El dominio es puro

No existen efectos secundarios.

No existen accesos a red.

No existen accesos a disco.

No existen consultas SQL.

No existen llamadas HTTP.

---

## 2.5 Inmutabilidad

Siempre que sea posible:

Los objetos del dominio serán inmutables.

El estado cambiará únicamente mediante nuevas instancias.

---

## 2.6 Reglas explícitas

Toda regla de negocio deberá existir como código.

Nunca como comentario.

Nunca como documentación.

Nunca como validación de interfaz.

---

# 3. Arquitectura

El dominio utilizará Clean Architecture.

```
Presentation

↓

Application

↓

Domain

↓

Infrastructure
```

Las dependencias únicamente apuntan hacia abajo.

Infrastructure jamás gobierna al dominio.

---

# 4. Bounded Contexts

AURA Core se dividirá en múltiples contextos delimitados.

Inicialmente:

```
Organization

Citizen

Assembly

Proposal

Voting

Process

Workflow

Notification

Identity

Permissions

Geo

Assets

Documents

Audit

Integration
```

Cada contexto será independiente.

---

# 5. Entidades

Una Entidad posee identidad.

Ejemplo:

Organization

Member

Assembly

Proposal

Document

Neighborhood

---

# 6. Value Objects

Un Value Object no posee identidad.

Ejemplo:

Email

Phone

Address

Coordinates

Period

Money

Role

VoteWeight

---

# 7. Domain Events

Toda modificación importante del dominio genera un evento.

Ejemplos:

OrganizationCreated

MemberAdded

AssemblyScheduled

ProposalApproved

VoteCast

DocumentSigned

Estos eventos representan hechos.

No comandos.

---

# 8. Casos de Uso

Los casos de uso viven fuera del dominio.

Responsabilidades:

Coordinar entidades.

Invocar repositorios.

Emitir eventos.

Nunca contienen reglas de negocio propias.

---

# 9. Repositorios

Los repositorios son interfaces.

Nunca implementaciones.

Ejemplo:

OrganizationRepository

MemberRepository

ProposalRepository

Infrastructure implementará estas interfaces.

---

# 10. Adaptadores

Todo acceso externo se realiza mediante adaptadores.

Ejemplos:

REST Adapter

GraphQL Adapter

NGSI-LD Adapter

Municipality Adapter

FIWARE Adapter

Keycloak Adapter

Email Adapter

SMS Adapter

---

# 11. Integraciones

Las integraciones nunca forman parte del dominio.

Las integraciones traducen.

Nunca gobiernan.

---

# 12. Testing

El dominio debe ser completamente testeable.

Sin mocks de frameworks.

Sin bases de datos.

Sin servidores.

Cada regla deberá poseer pruebas unitarias.

---

# 13. Convenciones

Idioma:

Código:

Inglés.

Documentación:

Español.

Comentarios:

Español.

Commit:

Conventional Commits.

PEP8 para Python.

ESLint + Prettier para TypeScript.

---

# 14. Principios SOLID

Toda implementación deberá respetar:

Single Responsibility

Open/Closed

Liskov

Interface Segregation

Dependency Inversion

---

# 15. Principios DDD

El dominio seguirá Domain Driven Design.

Componentes oficiales:

Entities

Value Objects

Aggregates

Repositories

Factories

Domain Services

Specifications

Policies

Domain Events

---

# 16. Reglas de Dependencia

Permitido:

Presentation

↓

Application

↓

Domain

↓

Infrastructure

Prohibido:

Domain → Infrastructure

Domain → React

Domain → SQL

Domain → HTTP

Domain → Frameworks

---

# 17. Objetivo Final

Construir una plataforma capaz de modelar organizaciones,
procesos comunitarios e interoperabilidad institucional
sin depender de ninguna tecnología específica.

El dominio deberá poder sobrevivir al reemplazo total de:

React

Next.js

FastAPI

Django

MongoDB

PostgreSQL

Docker

Kubernetes

FIWARE

sin modificar una sola regla de negocio.

---

# 18. Constitución

Esta constitución prevalece sobre cualquier decisión de implementación.

Toda nueva funcionalidad deberá respetar este documento.

Si una decisión contradice esta constitución:

la implementación deberá cambiar,

no la constitución.