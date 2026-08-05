# CORE-012 — Domain Services

Versión: 1.0

Estado: Oficial

Proyecto: AURA Core

Autor: ARADA

---

# Objetivo

Definir las reglas oficiales para el diseño de los Domain
Services dentro de AURA Core.

Los Domain Services encapsulan reglas de negocio que no
pertenecen naturalmente a una Entity ni a un Aggregate, pero
que forman parte del núcleo del dominio.

Este documento establece cuándo un comportamiento debe
modelarse como Domain Service y cuáles son las restricciones
arquitectónicas para mantener un modelo cohesionado.

---

# Definición

Un Domain Service representa una operación del negocio que:

- posee significado para el dominio;
- involucra uno o más Aggregates;
- no pertenece naturalmente a una única Entity;
- no depende de infraestructura.

Su responsabilidad es expresar comportamiento del negocio,
no coordinar casos de uso.

---

# Propósito

Un Domain Service existe únicamente cuando el comportamiento
no puede ubicarse correctamente dentro de:

- una Entity;
- un Value Object;
- un Aggregate Root.

Antes de crear un Domain Service siempre debe evaluarse si
el comportamiento pertenece realmente a alguno de esos
elementos.

---

# Responsabilidad

Todo Domain Service debe:

- implementar reglas del negocio;
- mantener el modelo expresivo;
- preservar las invariantes del dominio.

Nunca debe:

- coordinar flujos de aplicación;
- acceder directamente a infraestructura;
- contener lógica de presentación.

---

# Características

Un Domain Service debe ser:

- explícito;
- cohesionado;
- determinista;
- independiente;
- fácilmente testeable.

---

# Stateless

Los Domain Services son completamente stateless.

No mantienen estado interno entre invocaciones.

Toda la información necesaria se recibe mediante
parámetros.

---

# Dependencias

Un Domain Service puede depender únicamente de:

- Entities;
- Aggregates;
- Value Objects;
- Repository Contracts;
- otros Domain Services (cuando sea estrictamente
  necesario);
- Shared Kernel.

Nunca depende de:

- Frameworks;
- HTTP;
- Base de datos;
- ORM;
- Redis;
- Mensajería;
- APIs externas.

---

# Colaboración

Los Domain Services colaboran con los Aggregates sin romper
sus límites.

Nunca modifican directamente el estado interno de una
Entity.

Toda modificación ocurre utilizando la API pública del
Aggregate correspondiente.

---

# Persistencia

Los Domain Services nunca implementan persistencia.

Cuando requieren recuperar información utilizan contratos
de Repository definidos por el dominio.

---

# Domain Events

Un Domain Service puede provocar cambios que generen Domain
Events.

Los eventos son publicados por el Aggregate Root o por la
capa de Application, nunca directamente por el Domain
Service.

---

# Ejemplos

## Correctos

- Resolver quórum de una asamblea.
- Validar compatibilidad entre organizaciones.
- Calcular elegibilidad de una propuesta.
- Determinar permisos territoriales.
- Resolver conflictos de calendario.
- Calcular prioridad de atención ciudadana.

---

## Incorrectos

- Enviar correos electrónicos.
- Guardar registros en PostgreSQL.
- Consumir APIs REST.
- Publicar mensajes en Kafka.
- Generar respuestas HTTP.
- Renderizar interfaces.

---

# Granularidad

Cada Domain Service representa un único concepto del
negocio.

No debe convertirse en un contenedor de reglas
heterogéneas.

Cuando un servicio crece excesivamente, debe dividirse
según las capacidades del dominio.

---

# Nomenclatura

Los nombres deben expresar una capacidad del negocio.

Correcto:

AssemblyQuorumService

CitizenEligibilityService

ProposalEvaluationService

TerritoryAssignmentService

OrganizationMergeService

Incorrecto:

Utils

Helper

Manager

Processor

BusinessLogic

CommonService

---

# Entrada y Salida

Los parámetros deben utilizar exclusivamente tipos del
dominio.

Ejemplos:

- Aggregate Roots;
- Value Objects;
- Identificadores;
- Objetos del Shared Kernel.

Nunca tipos específicos de infraestructura.

---

# Excepciones

Los Domain Services expresan errores mediante los
mecanismos oficiales definidos por el dominio.

No deben propagar excepciones propias de tecnologías
externas.

---

# Testing

Todo Domain Service debe poder probarse mediante pruebas
unitarias puras.

No requiere:

- base de datos;
- servidor web;
- contenedores;
- infraestructura externa.

---

# Ubicación

Los Domain Services pertenecen al Dominio.

Ejemplo:

src/

domain/

services/

AssemblyQuorumService.ts

ProposalEvaluationService.ts

CitizenEligibilityService.ts

---

# Reglas Arquitectónicas

## Regla 1

Un Domain Service representa comportamiento del negocio.

---

## Regla 2

No posee estado interno.

---

## Regla 3

No depende de infraestructura.

---

## Regla 4

Opera utilizando exclusivamente objetos del dominio.

---

## Regla 5

Nunca reemplaza el comportamiento que pertenece a una
Entity o Aggregate.

---

## Regla 6

Toda modificación del estado ocurre mediante la API pública
de los Aggregates.

---

## Regla 7

No coordina casos de uso.

---

## Regla 8

Debe poder probarse sin infraestructura.

---

## Regla 9

Sus nombres expresan capacidades del negocio.

---

## Regla 10

Debe preservar las invariantes del dominio.

---

# Beneficios

La aplicación de estas reglas proporciona:

- separación clara de responsabilidades;
- mayor cohesión del modelo;
- menor acoplamiento;
- reglas de negocio reutilizables;
- independencia tecnológica;
- facilidad de pruebas;
- evolución controlada del dominio;
- mayor expresividad del lenguaje ubicuo.

---

# Definición de Éxito

Todos los Domain Services de AURA Core encapsulan
capacidades reales del negocio que no pertenecen
naturalmente a una Entity o Aggregate, permanecen
completamente independientes de la infraestructura y
preservan la integridad del modelo de dominio mediante
reglas explícitas, cohesivas y fácilmente testeables.