# CORE-009 — Entity Design Rules

Versión: 1.0

Estado: Oficial

Proyecto: AURA Core

Autor: ARADA

---

# Objetivo

Definir las reglas oficiales para el diseño de Entities
dentro de AURA Core.

Este documento establece los principios que permiten
modelar correctamente los conceptos del dominio que poseen
identidad propia y cuyo ciclo de vida evoluciona a través
del tiempo.

Todas las entidades implementadas en la plataforma deberán
cumplir estas reglas.

---

# Definición

Una Entity representa un objeto del dominio cuya identidad
permanece constante independientemente de los cambios en su
estado.

Una Entity no se reconoce por sus atributos.

Se reconoce por su identidad.

---

# Identidad

Toda Entity posee exactamente una identidad.

La identidad:

- es única;
- es estable;
- nunca cambia;
- no depende de atributos descriptivos.

Ejemplos:

- OrganizationId
- CitizenId
- ProposalId
- AssemblyId

---

# Igualdad

Dos Entities son iguales únicamente cuando poseen la misma
identidad.

Nunca se comparan utilizando sus atributos internos.

Correcto:

OrganizationId == OrganizationId

Incorrecto:

name == name

---

# Ciclo de Vida

Las Entities evolucionan.

Su estado puede modificarse mientras su identidad permanece
constante.

Ejemplo:

Una Organización puede cambiar:

- nombre;
- dirección;
- representantes;
- configuración.

Pero continúa siendo la misma Organización.

---

# Responsabilidad

Una Entity representa comportamiento del negocio.

No representa únicamente datos.

Toda modificación del estado expresa una decisión del
dominio.

---

# Encapsulamiento

Las propiedades internas permanecen protegidas.

La modificación del estado ocurre exclusivamente mediante
métodos del dominio.

Nunca mediante asignaciones públicas.

Correcto:

rename()

activate()

suspend()

changeRepresentative()

Incorrecto:

setName()

setStatus()

setOwner()

---

# Estado Válido

Toda Entity debe permanecer siempre en un estado válido.

Las validaciones pertenecen al dominio.

Nunca deben depender de interfaces de usuario ni de la
infraestructura.

---

# Constructores

Una Entity nunca puede quedar parcialmente inicializada.

Toda Entity debe construirse mediante:

- constructor;
- Factory;
- método estático.

La creación siempre produce una Entity válida.

---

# Inmutabilidad Parcial

La identidad es completamente inmutable.

Los atributos del dominio pueden cambiar únicamente cuando
el negocio lo permite.

---

# Colaboración

Las Entities colaboran únicamente mediante métodos del
dominio.

Nunca modifican directamente el estado interno de otras
Entities.

---

# Aggregate Root

Las Entities internas pertenecen a un Aggregate.

Nunca son modificadas directamente desde el exterior.

Toda modificación ocurre mediante el Aggregate Root.

---

# Persistencia

Las Entities no conocen mecanismos de persistencia.

Nunca contienen:

- SQL;
- MongoDB;
- ORM;
- HTTP;
- Frameworks.

La persistencia pertenece exclusivamente al Repository.

---

# Domain Events

Cuando una Entity provoca un cambio significativo del
negocio, el Aggregate Root correspondiente publica un
Domain Event.

Las Entities internas no publican eventos directamente.

---

# Dependencias

Las Entities únicamente pueden depender de:

- Value Objects;
- otras Entities del mismo Aggregate;
- Shared Kernel;
- Domain Services (cuando corresponda).

Nunca dependen de Infrastructure.

---

# Identificadores

Los identificadores deben representarse mediante Value
Objects específicos.

Correcto:

OrganizationId

CitizenId

ProposalId

Incorrecto:

string

UUID

number

---

# Mutaciones

Cada mutación debe expresar intención del negocio.

Ejemplos:

approve()

reject()

archive()

registerMember()

closeAssembly()

Nunca:

setApproved()

setArchived()

setClosed()

---

# Cohesión

Cada Entity representa un único concepto del dominio.

No debe acumular responsabilidades ajenas.

Cuando una Entity comienza a representar múltiples
conceptos, el modelo debe refactorizarse.

---

# Tamaño

Las Entities deben permanecer pequeñas.

El comportamiento complejo que involucra múltiples
Entities pertenece a:

- Domain Services;
- Application Services;
- Aggregates.

---

# Integridad

Las Entities nunca permiten estados imposibles.

Las reglas del negocio deben verificarse antes de aceptar
cualquier modificación.

---

# Serialización

Las Entities no existen para transportar datos.

Cuando sea necesario comunicar información al exterior se
utilizarán:

- DTOs;
- Read Models;
- Published Language.

---

# Reglas Arquitectónicas

## Regla 1

Toda Entity posee una identidad única.

---

## Regla 2

La identidad nunca cambia.

---

## Regla 3

La igualdad depende exclusivamente de la identidad.

---

## Regla 4

Toda modificación expresa una regla del negocio.

---

## Regla 5

Las propiedades internas permanecen encapsuladas.

---

## Regla 6

Las Entities nunca contienen lógica de infraestructura.

---

## Regla 7

Las Entities pertenecen a un Aggregate.

---

## Regla 8

Las Entities no poseen repositorios propios salvo que sean
Aggregate Roots.

---

## Regla 9

Los identificadores son Value Objects.

---

## Regla 10

Toda Entity representa comportamiento, no estructuras de
datos.

---

# Beneficios

La aplicación de estas reglas proporciona:

- identidad consistente;
- encapsulamiento;
- alta cohesión;
- bajo acoplamiento;
- facilidad de evolución;
- mayor expresividad del dominio;
- independencia tecnológica;
- facilidad de pruebas.

---

# Definición de Éxito

Todas las Entities de AURA Core representan conceptos
reales del dominio, mantienen una identidad inmutable,
protegen su estado mediante comportamiento explícito y
colaboran únicamente a través de las reglas establecidas
por sus Aggregates y el modelo de dominio.