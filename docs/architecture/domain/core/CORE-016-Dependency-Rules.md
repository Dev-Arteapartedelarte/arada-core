# CORE-016 — Dependency Rules

Versión: 1.0

Estado: Oficial

Proyecto: AURA Core

Autor: ARADA

---

# Objetivo

Definir las reglas oficiales de dependencia de AURA Core.

Este documento establece la dirección permitida de las
dependencias entre los distintos componentes de la
arquitectura para preservar la independencia del dominio,
evitar el acoplamiento accidental y garantizar la
evolución sostenible de la plataforma.

Las reglas aquí descritas son obligatorias para todo el
código fuente del proyecto.

---

# Principio Fundamental

Las dependencias siempre apuntan hacia el centro del
modelo.

Mientras más interno sea un componente, mayor será su
estabilidad y menor su conocimiento del exterior.

Ningún componente interno puede depender de uno externo.

---

# Dirección de Dependencias

La dirección oficial es:

```text
Interfaces
      │
      ▼
Application
      │
      ▼
Domain
```

Infrastructure implementa contratos definidos por Domain o
Application.

Nunca ocurre la dirección inversa.

---

# Modelo de Capas

```text
┌───────────────────────────────┐
│ Interfaces                    │
├───────────────────────────────┤
│ Application                   │
├───────────────────────────────┤
│ Domain                        │
└───────────────────────────────┘

Infrastructure
implementa contratos definidos
por las capas superiores.
```

---

# Dominio

El dominio constituye el núcleo del sistema.

No puede depender de:

- Application;
- Infrastructure;
- Interfaces;
- Frameworks;
- Librerías de persistencia;
- HTTP;
- Bases de datos;
- Mensajería.

Únicamente puede depender de:

- sí mismo;
- Shared Kernel.

---

# Application

Application puede depender de:

- Domain;
- Shared Kernel.

Puede utilizar contratos definidos por el dominio.

Nunca depende de Interfaces.

---

# Infrastructure

Infrastructure puede depender de:

- Domain;
- Application;
- Shared Kernel.

Su función consiste en implementar contratos.

Nunca define reglas del negocio.

---

# Interfaces

Las Interfaces representan el punto de entrada al sistema.

Pueden depender de:

- Application;
- Shared Kernel.

Nunca implementan reglas del dominio.

---

# Shared Kernel

El Shared Kernel representa el nivel más estable de toda
la arquitectura.

Puede ser utilizado por:

- Domain;
- Application;
- Infrastructure;
- Interfaces.

El Shared Kernel nunca depende de ningún Bounded Context.

---

# Bounded Contexts

Cada Bounded Context mantiene independencia respecto a los
demás.

La comunicación entre contextos ocurre mediante:

- Domain Events;
- Interfaces públicas;
- Anti-Corruption Layer;
- Published Language.

Nunca mediante acceso directo a clases internas.

---

# Contratos

Toda dependencia entre capas debe realizarse mediante
abstracciones.

Ejemplos:

- Repository Contracts;
- Domain Services;
- Ports;
- Interfaces.

Nunca mediante implementaciones concretas.

---

# Frameworks

Los frameworks pertenecen exclusivamente a Infrastructure
o Interfaces.

Ejemplos:

- FastAPI;
- Django;
- SQLAlchemy;
- MongoDB Driver;
- Redis;
- Kafka;
- RabbitMQ.

El dominio permanece completamente ajeno a ellos.

---

# Persistencia

El dominio no conoce:

- tablas;
- colecciones;
- consultas SQL;
- índices;
- ORMs.

La persistencia se implementa exclusivamente en
Infrastructure.

---

# Transporte

El dominio nunca conoce:

- HTTP;
- REST;
- GraphQL;
- gRPC;
- WebSocket;
- CLI.

Estos mecanismos pertenecen a Interfaces.

---

# Dependencias entre Aggregates

Un Aggregate nunca mantiene referencias directas a otro
Aggregate.

La comunicación se realiza mediante:

- identificadores;
- Domain Events;
- Domain Services.

---

# Dependencias entre Entities

Las Entities pertenecientes a distintos Aggregates no deben
referenciarse directamente.

Toda colaboración ocurre a través del Aggregate Root.

---

# Dependencias Circulares

Las dependencias circulares están estrictamente
prohibidas.

El grafo completo de dependencias debe ser acíclico.

---

# Dependencias Implícitas

También se consideran dependencias:

- imports;
- herencia;
- composición;
- referencias estáticas;
- tipos genéricos;
- anotaciones;
- atributos.

Todas deben respetar estas reglas.

---

# Inversión de Dependencias

Toda dependencia técnica debe invertirse mediante
abstracciones.

Ejemplo:

Domain

↓

Repository Interface

↓

Infrastructure Repository

Nunca:

Domain

↓

PostgreSQL Repository

---

# Inyección de Dependencias

La composición de objetos ocurre en el Composition Root.

Normalmente:

- Bootstrap;
- Dependency Container;
- Main;
- Startup.

El dominio nunca construye infraestructura.

---

# Testing

Las pruebas respetan las mismas reglas de dependencia que
el código productivo.

Los dobles de prueba implementan contratos del dominio.

---

# Verificación

Las reglas de dependencia deben poder validarse mediante:

- revisión arquitectónica;
- análisis estático;
- herramientas de arquitectura;
- pruebas automatizadas.

---

# Reglas Arquitectónicas

## Regla 1

Todas las dependencias apuntan hacia el dominio.

---

## Regla 2

El dominio nunca depende de infraestructura.

---

## Regla 3

Application depende únicamente del dominio y del Shared
Kernel.

---

## Regla 4

Infrastructure implementa contratos definidos por capas
internas.

---

## Regla 5

Interfaces únicamente coordinan la entrada y salida del
sistema.

---

## Regla 6

Los Bounded Contexts permanecen desacoplados entre sí.

---

## Regla 7

Las dependencias siempre utilizan abstracciones.

---

## Regla 8

No se permiten dependencias circulares.

---

## Regla 9

La composición de dependencias ocurre únicamente en el
Composition Root.

---

## Regla 10

Toda nueva dependencia debe preservar la independencia del
modelo de dominio.

---

# Beneficios

La aplicación de estas reglas proporciona:

- independencia tecnológica;
- arquitectura estable;
- reducción del acoplamiento;
- mayor cohesión;
- facilidad de pruebas;
- sustitución sencilla de infraestructura;
- evolución modular;
- incorporación de nuevos adaptadores sin modificar el
  dominio;
- mantenimiento a largo plazo;
- alineación con Clean Architecture y DDD.

---

# Definición de Éxito

Todas las dependencias de AURA Core respetan una dirección
única hacia el dominio, utilizan abstracciones como punto
de integración, mantienen desacopladas las distintas capas
y Bounded Contexts, eliminan dependencias circulares y
garantizan que el núcleo del negocio permanezca estable,
independiente y ajeno a cualquier tecnología o framework.