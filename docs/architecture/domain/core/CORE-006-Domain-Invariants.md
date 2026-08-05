# CORE-006 — Domain Invariants

Version: 1.0

Estado: Oficial

Proyecto: AURA Core

Autor: ARADA

ADR relacionados:

- ADR-001 Domain Driven Design
- ADR-002 Hexagonal Architecture
- ADR-003 Event Driven Core

---

# Objetivo

Definir las reglas que **siempre deben cumplirse**
dentro del dominio.

Una Invariante representa una verdad permanente.

No depende de:

- UI
- API
- Base de datos
- Framework
- Infraestructura

Si una invariante se rompe,
el dominio deja de ser consistente.

---

# Principios

Toda regla del negocio debe existir
únicamente dentro del Dominio.

Nunca en:

- React
- FastAPI
- Django
- PostgreSQL
- MongoDB

---

# Invariantes Globales

## 1.

Todo Aggregate Root posee identidad única.

Nunca puede existir un Aggregate sin Id.

---

## 2.

Un Aggregate sólo puede modificarse
mediante sus propios métodos.

Nunca desde afuera.

Ejemplo incorrecto

Persona.nombre = "Juan"

Ejemplo correcto

Persona.cambiar_nombre(...)

---

## 3.

Todo cambio importante genera un Domain Event.

Ejemplos

PersonaRegistrada

SolicitudCreada

ProyectoPublicado

OrganizacionCreada

---

## 4.

Los Value Objects son inmutables.

Nunca cambian su estado.

Si cambia un valor,
se crea un nuevo objeto.

---

## 5.

Las Entidades nunca exponen setters públicos.

Toda modificación pasa por reglas del dominio.

---

## 6.

Toda operación debe preservar consistencia.

Nunca se aceptan estados intermedios inválidos.

---

## 7.

Ninguna regla depende del almacenamiento.

El dominio desconoce:

- PostgreSQL

- MongoDB

- Redis

- S3

- Kafka

---

## 8.

Ninguna regla depende del transporte.

El dominio desconoce:

- HTTP

- REST

- GraphQL

- WebSocket

- gRPC

---

## 9.

Las decisiones del negocio son determinísticas.

Misma entrada.

Misma salida.

---

## 10.

Las reglas del dominio son testeables
sin infraestructura.

Todos los tests deben poder ejecutarse únicamente con Python.

---

# Entidades

Una Entidad:

- posee identidad

- cambia de estado

- protege invariantes

Ejemplo

Persona

Proyecto

Organizacion

Solicitud

---

# Value Objects

Un Value Object:

- no posee identidad

- es inmutable

- representa un concepto

Ejemplos

Email

Direccion

Telefono

Coordenada

Rut

Money

---

# Aggregate Root

Sólo el Aggregate Root puede modificar
el estado interno del Aggregate.

Ejemplo

Proyecto

↓

Tareas

↓

Miembros

↓

Recursos

Todo acceso ocurre mediante Proyecto.

---

# Repositories

Los Repository únicamente:

guardan

obtienen

eliminan

Nunca contienen reglas del negocio.

---

# Domain Services

Sólo existen cuando la lógica
no pertenece naturalmente
a una Entidad.

Ejemplos

MatchingService

ScoringService

RecommendationService

IdentityValidationService

---

# Factories

Construyen Aggregates válidos.

Nunca crean objetos inconsistentes.

---

# Domain Events

Todo cambio significativo genera
un evento inmutable.

Los eventos representan hechos.

Nunca comandos.

---

# Commands

Representan intención.

Ejemplos

CrearProyecto

RegistrarPersona

ActualizarPerfil

---

# Events

Representan hechos ocurridos.

Ejemplos

ProyectoCreado

PersonaRegistrada

PerfilActualizado

---

# Queries

Nunca modifican estado.

Sólo consultan.

---

# Casos de Uso

Un Caso de Uso:

coordina

orquesta

ejecuta

Pero nunca contiene reglas fundamentales.

---

# Anti-Invariantes

Nunca estará permitido:

❌ lógica de negocio en Controllers

❌ lógica de negocio en API

❌ lógica de negocio en React

❌ lógica de negocio en SQL

❌ lógica de negocio en ORM

❌ lógica de negocio en Repository

❌ entidades anémicas

❌ setters públicos

❌ dependencias circulares

❌ acceso directo entre Aggregates

---

# Regla Fundamental

Toda regla importante vive
en el Dominio.

Todo lo demás
es únicamente infraestructura.

---

# Definición de Éxito

Si mañana cambiamos:

- FastAPI por Django

- PostgreSQL por MongoDB

- React por Flutter

- REST por GraphQL

- Docker por Kubernetes

El Dominio permanece idéntico.

Esa es la medida de éxito de AURA Core.