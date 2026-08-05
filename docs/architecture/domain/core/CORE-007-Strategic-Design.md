# CORE-007 — Strategic Design

Versión: 1.0

Estado: Oficial

Proyecto: AURA Core

Autor: ARADA

---

# Objetivo

Definir el diseño estratégico del dominio de AURA Core.

Este documento establece cómo se divide el dominio, cómo
colaboran sus distintos Bounded Contexts y cuáles son las
reglas que permiten que el sistema evolucione sin perder
cohesión.

El diseño estratégico constituye la base arquitectónica
sobre la cual se construirá todo el núcleo de la plataforma.

---

# Principios

El dominio se organiza siguiendo los principios de
Domain-Driven Design (DDD).

Las decisiones de diseño privilegian:

- Bajo acoplamiento
- Alta cohesión
- Independencia tecnológica
- Evolución incremental
- Escalabilidad funcional
- Lenguaje ubicuo
- Aislamiento de responsabilidades

---

# Clasificación del Dominio

AURA Core distingue tres categorías de dominio.

## Core Domain

Representa el conocimiento que diferencia a la plataforma.

Aquí reside el verdadero valor del producto.

Ejemplos:

- Gestión territorial
- Participación ciudadana
- Gobernanza digital
- Organización comunitaria
- Modelo de colaboración
- Inteligencia territorial

Todo el esfuerzo principal de diseño debe concentrarse en
este dominio.

---

## Supporting Domains

Son dominios necesarios para operar el sistema, pero no
constituyen la ventaja competitiva.

Ejemplos:

- Gestión documental
- Catálogo
- Notificaciones
- Configuración
- Reportes

Estos dominios pueden evolucionar de forma independiente.

---

## Generic Domains

Son capacidades comunes presentes en casi cualquier
plataforma.

Ejemplos:

- Autenticación
- Autorización
- Usuarios
- Auditoría
- Archivos
- Logging
- Observabilidad

Siempre que sea posible se reutilizan componentes
existentes.

---

# Bounded Contexts

Cada Bounded Context representa un modelo consistente del
dominio.

Dentro de un contexto no existen ambigüedades de lenguaje.

Cada contexto:

- posee su propio modelo
- posee sus propias reglas
- posee sus propios agregados
- publica sus propios eventos
- controla su consistencia

Nunca comparte entidades internas con otros contextos.

---

# Relaciones entre Contextos

Los contextos colaboran exclusivamente mediante contratos.

Nunca mediante acceso directo a objetos internos.

Los mecanismos oficiales son:

- Domain Events
- Application Services
- Interfaces
- ACL (Anti-Corruption Layer)

Nunca mediante dependencias implícitas.

---

# Shared Kernel

El Shared Kernel contiene únicamente conceptos que poseen
el mismo significado en todos los contextos.

Ejemplos:

- Identifier
- Timestamp
- Coordinates
- Email
- Result
- DomainEvent
- Entity
- AggregateRoot

El Shared Kernel debe permanecer pequeño y estable.

---

# Anti-Corruption Layer

Toda integración con sistemas externos debe realizarse a
través de un Anti-Corruption Layer.

Su responsabilidad es:

- traducir modelos
- adaptar contratos
- proteger el dominio

El dominio nunca conoce modelos externos.

---

# Context Mapping

Las relaciones entre contextos pueden clasificarse como:

## Partnership

Dos contextos evolucionan coordinadamente.

---

## Customer / Supplier

Un contexto consume servicios publicados por otro.

---

## Conformist

El consumidor acepta completamente el modelo del proveedor.

Debe evitarse cuando sea posible.

---

## Anti-Corruption Layer

La traducción protege el modelo interno.

Es la estrategia preferida para integraciones externas.

---

## Open Host Service

Un contexto publica contratos estables para otros
consumidores.

---

## Published Language

Los mensajes públicos utilizan un lenguaje independiente
del modelo interno.

Generalmente mediante DTOs o Domain Events.

---

# Ownership

Cada contexto posee completamente:

- su modelo
- sus entidades
- sus agregados
- sus repositorios
- sus eventos
- sus servicios de dominio

Ningún otro contexto puede modificarlos directamente.

---

# Consistencia

La consistencia fuerte sólo existe dentro de un Aggregate.

Entre contextos se utiliza:

Eventual Consistency.

La sincronización ocurre mediante Domain Events.

---

# Dependencias

Las dependencias permitidas son únicamente hacia adentro.

Infrastructure

↓

Application

↓

Domain

El dominio nunca depende de capas superiores.

---

# Independencia Tecnológica

El dominio nunca conoce:

- HTTP
- REST
- GraphQL
- PostgreSQL
- MongoDB
- Redis
- RabbitMQ
- Kafka
- Docker
- Kubernetes
- FastAPI
- Django

Toda tecnología pertenece a Infrastructure.

---

# Evolución

Cada contexto puede evolucionar de forma independiente.

Cambios internos no deben afectar a otros contextos si los
contratos públicos permanecen estables.

Esto permite desplegar nuevas capacidades sin modificar el
resto del sistema.

---

# Estrategia de Integración

La comunicación entre contextos sigue el siguiente flujo:

Aggregate

↓

Domain Event

↓

Application Service

↓

Event Bus

↓

Consumer

↓

Application Service

↓

Aggregate

El dominio permanece completamente desacoplado del
transporte utilizado.

---

# Reglas Arquitectónicas

## Regla 1

Un Aggregate nunca accede a otro Aggregate mediante
referencias directas.

Siempre utiliza identificadores.

---

## Regla 2

Los Bounded Contexts nunca comparten entidades.

---

## Regla 3

Todo intercambio entre contextos utiliza contratos
explícitos.

---

## Regla 4

Las reglas del negocio pertenecen exclusivamente al dominio.

---

## Regla 5

Infrastructure nunca contiene reglas del negocio.

---

## Regla 6

Application coordina casos de uso.

Nunca implementa lógica del dominio.

---

## Regla 7

Cada contexto mantiene su propio Lenguaje Ubicuo.

---

## Regla 8

Todo cambio relevante genera Domain Events.

---

## Regla 9

Los contratos públicos son estables.

Los cambios incompatibles requieren versionado.

---

## Regla 10

El Core Domain tiene prioridad sobre cualquier otro
dominio.

Las decisiones arquitectónicas siempre favorecen la
evolución del Core Domain.

---

# Beneficios

Esta estrategia proporciona:

- Evolución independiente
- Escalabilidad organizacional
- Bajo acoplamiento
- Alta cohesión
- Integración segura
- Protección del dominio
- Mantenibilidad
- Claridad conceptual
- Facilidad de pruebas
- Adaptabilidad tecnológica

---

# Definición de Éxito

AURA Core está compuesto por Bounded Contexts autónomos,
con un lenguaje consistente, reglas claramente delimitadas
y comunicación basada en contratos explícitos.

El dominio permanece protegido frente a cambios
tecnológicos y puede evolucionar de forma sostenible
durante toda la vida de la plataforma.