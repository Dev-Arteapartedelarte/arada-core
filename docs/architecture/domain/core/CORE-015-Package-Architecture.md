# CORE-015 — Package Architecture

Versión: 2.0

Estado: Oficial

Proyecto: AURA Core

Autor: ARADA

---

# Objetivo

Definir la arquitectura oficial de paquetes de AURA Core.

Este documento establece cómo debe organizarse físicamente
el código fuente para reflejar fielmente el modelo del
dominio definido mediante Domain-Driven Design (DDD),
Clean Architecture y principios SOLID.

La estructura de paquetes constituye una decisión
arquitectónica y no una preferencia de estilo.

---

# Principios

Toda la organización del código debe cumplir los siguientes
principios:

- reflejar el dominio;
- minimizar el acoplamiento;
- maximizar la cohesión;
- facilitar la evolución independiente;
- evitar dependencias circulares;
- preservar la independencia tecnológica.

---

# Organización General

La organización del proyecto sigue Hexagonal Architecture. Los nombres
de paquete expresan el núcleo y sus adapters, no una dependencia vertical
hacia Infrastructure.

```text
src/

    domain/

    application/

    infrastructure/

        adapters/

            inbound/

            outbound/

    shared/
```

Cada zona representa una responsabilidad dentro de la arquitectura
hexagonal; no constituye una cadena de dependencias descendente.

---

# Dominio

El paquete Domain contiene exclusivamente conocimiento del
negocio.

Nunca depende de Application, Infrastructure o Interfaces.

```text
domain/

    aggregates/

    entities/

    value_objects/

    services/

    events/

    repositories/

    errors/

    specifications/

    policies/

    factories/
```

---

# Application

La capa Application implementa los casos de uso.

Coordina el dominio sin incorporar reglas del negocio.

```text
application/

    services/

    commands/

    queries/

    handlers/

    dto/

    mappers/

    ports/
```

---

# Infrastructure

Infrastructure contiene outbound adapters que implementan puertos del
núcleo y composición técnica.

Ejemplos:

```text
infrastructure/

    persistence/

    messaging/

    email/

    storage/

    security/

    monitoring/

    configuration/
```

El dominio nunca depende de Infrastructure.

---

# Interfaces

Interfaces contiene inbound adapters que traducen mecanismos externos a
input ports de Application.

Ejemplos:

```text
interfaces/

    rest/

    graphql/

    grpc/

    cli/

    websocket/

    jobs/
```

Los inbound adapters nunca contienen reglas del negocio.

---

# Shared

Shared contiene componentes reutilizables entre múltiples
Bounded Contexts.

Debe mantenerse pequeño y estable.

Ejemplo:

```text
shared/

    kernel/

    primitives/

    result/

    identifiers/

    clock/

    pagination/
```

---

# Organización por Bounded Context

Cada Bounded Context replica internamente la misma
estructura arquitectónica.

Ejemplo:

```text
src/

    community/

        domain/

        application/

        infrastructure/

        interfaces/

    governance/

        domain/

        application/

        infrastructure/

        interfaces/

    identity/

        domain/

        application/

        infrastructure/

        interfaces/
```

Cada contexto constituye un módulo autónomo.

---

# Dependencias Permitidas

La dirección de las dependencias es única.

```text
Interfaces
      ↓

Application
      ↓

Domain

Infrastructure
      ↑
```

Infrastructure implementa contratos definidos por Domain o
Application.

Nunca ocurre el sentido inverso.

---

# Reglas de Visibilidad

Cada paquete expone únicamente su API pública.

Los detalles internos permanecen encapsulados.

Los consumidores nunca deben acceder a clases internas de
otro paquete.

---

# Cohesión

Los elementos relacionados deben permanecer juntos.

Ejemplo:

```text
Organization/

    Organization.ts

    OrganizationId.ts

    OrganizationName.ts

    OrganizationRepository.ts

    OrganizationEvents.ts
```

Debe evitarse la dispersión de conceptos relacionados.

---

# Acoplamiento

Los paquetes deben comunicarse mediante contratos.

Nunca mediante implementaciones concretas.

---

# Dependencias Circulares

Las dependencias circulares están estrictamente prohibidas.

Toda relación debe formar un grafo acíclico.

---

# Frameworks

Los frameworks pertenecen exclusivamente a Infrastructure
o Interfaces.

Nunca aparecen dentro del dominio.

---

# Nomenclatura

Los nombres de paquetes deben representar conceptos del
negocio.

Correcto:

Organization

Citizen

Assembly

Proposal

Vote

Territory

Incorrecto:

Utils

Common

Misc

General

Manager

Helper

---

# Tamaño

Los paquetes deben mantenerse pequeños y cohesivos.

Cuando un paquete crece excesivamente, debe dividirse
según conceptos del dominio.

Nunca por criterios técnicos.

---

# Importaciones

Las importaciones siempre deben respetar la arquitectura.

Ejemplo correcto:

Application

↓

Domain

Ejemplo incorrecto:

Domain

↓

REST Controller

---

# Testing

La estructura de pruebas replica la organización del
código.

Ejemplo:

```text
tests/

    domain/

    application/

    infrastructure/
```

Esto facilita la trazabilidad entre implementación y
validación.

---

# Escalabilidad

La arquitectura de paquetes debe permitir:

- nuevos Bounded Contexts;
- nuevos adaptadores;
- nuevas interfaces;
- nuevos mecanismos de persistencia;
- nuevas tecnologías.

Sin modificar el dominio existente.

---

# Reglas Arquitectónicas

## Regla 1

La estructura física refleja la estructura del dominio.

---

## Regla 2

El dominio nunca depende de otras capas.

---

## Regla 3

Application coordina el dominio.

---

## Regla 4

Infrastructure implementa contratos.

---

## Regla 5

Interfaces contienen únicamente mecanismos de entrada y
salida.

---

## Regla 6

Los paquetes deben ser altamente cohesivos.

---

## Regla 7

Las dependencias siempre apuntan hacia el dominio.

---

## Regla 8

No se permiten dependencias circulares.

---

## Regla 9

Cada Bounded Context mantiene autonomía estructural.

---

## Regla 10

La arquitectura física debe permanecer alineada con la
arquitectura conceptual definida por AURA Core.

---

# Beneficios

La aplicación de esta arquitectura proporciona:

- correspondencia directa entre modelo y código;
- independencia tecnológica;
- evolución modular;
- mantenimiento simplificado;
- reducción del acoplamiento;
- mayor cohesión;
- facilidad de pruebas;
- incorporación sencilla de nuevos Bounded Contexts;
- escalabilidad a largo plazo;
- comprensión inmediata de la organización del sistema.

---

# Definición de Éxito

La arquitectura de paquetes de AURA Core refleja fielmente
el modelo del dominio, mantiene una dirección única de
dependencias, garantiza la autonomía de los Bounded
Contexts, elimina el acoplamiento innecesario y permite
que la plataforma evolucione de forma modular, mantenible
e independiente de cualquier tecnología específica.