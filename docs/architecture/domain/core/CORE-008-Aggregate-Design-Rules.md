# CORE-008 — Aggregate Design Rules

Versión: 2.0

Estado: Oficial

Proyecto: AURA Core

Autor: ARADA

---

# Objetivo

Definir las reglas oficiales para el diseño de Aggregates
dentro de AURA Core.

Este documento establece los principios que garantizan la
consistencia del dominio, la protección de las invariantes y
la independencia entre Bounded Contexts.

Todo Aggregate implementado en la plataforma deberá cumplir
estas reglas.

---

# Definición

Un Aggregate es un conjunto de objetos del dominio que se
comportan como una única unidad de consistencia.

Un Aggregate protege las reglas del negocio que no pueden
violarse.

Todo acceso al Aggregate ocurre exclusivamente a través de
su Aggregate Root.

---

# Aggregate Root

Todo Aggregate posee exactamente un Aggregate Root.

El Aggregate Root:

- representa la identidad del Aggregate;
- protege las invariantes;
- controla todas las modificaciones internas;
- genera y registra Domain Events;
- mantiene la consistencia del Aggregate.

Ningún objeto externo puede modificar directamente los
objetos internos del Aggregate.

---

# Responsabilidades

Un Aggregate debe ser responsable únicamente de:

- proteger sus invariantes;
- modificar su propio estado;
- coordinar sus entidades internas;
- generar Domain Events;
- mantener consistencia transaccional.

Nunca debe asumir responsabilidades de infraestructura.

---

# Invariantes

Toda regla que no pueda romperse pertenece al Aggregate.

Ejemplos:

- un miembro no puede pertenecer dos veces a la misma organización;
- una votación cerrada no admite nuevos votos;
- una organización debe poseer un identificador válido.

Las invariantes siempre deben cumplirse antes y después de
cada operación.

---

# Consistencia

La consistencia fuerte únicamente existe dentro del
Aggregate.

Toda operación pública debe dejar el Aggregate en un estado
válido.

Nunca puede existir un Aggregate parcialmente consistente.

---

# Tamaño

Los Aggregates deben ser pequeños.

Un Aggregate grande:

- reduce el rendimiento;
- incrementa el acoplamiento;
- dificulta la concurrencia;
- aumenta conflictos transaccionales.

La regla general es:

Diseñar el Aggregate más pequeño capaz de proteger sus
invariantes.

---

# Identidad

Todo Aggregate posee una identidad única.

La identidad nunca cambia durante su ciclo de vida.

La identidad no depende de atributos descriptivos.

Ejemplos:

- OrganizationId
- CitizenId
- AssemblyId
- ProposalId

---

# Referencias

Un Aggregate nunca mantiene referencias directas a otro
Aggregate.

Siempre utiliza identificadores.

Correcto:

OrganizationId

Incorrecto:

Organization

---

# Navegación

Los Aggregates no forman grafos de objetos.

Toda navegación entre Aggregates ocurre mediante:

- Repositories;
- Application Services;
- Domain Services.

Nunca mediante referencias internas.

---

# Persistencia

El Repository siempre persiste el Aggregate completo.

Nunca persiste entidades internas de forma aislada.

El Aggregate constituye la unidad mínima de persistencia.

---

# Repositories

Existe un único Repository por Aggregate Root.

Ejemplo:

OrganizationRepository

Nunca:

MemberRepository

Si Member pertenece al Aggregate Organization.

---

# Construcción

Los Aggregates deben construirse únicamente mediante:

- constructor;
- métodos estáticos;
- factories.

Nunca deben quedar parcialmente inicializados.

---

# Mutabilidad

Los cambios de estado únicamente ocurren mediante métodos
del Aggregate Root.

No existen propiedades públicas modificables.

Todo cambio representa una decisión del negocio.

---

# Entidades Internas

Las entidades internas:

- no poseen repositorios;
- no son accesibles desde otros contextos;
- existen únicamente dentro del Aggregate.

Su ciclo de vida depende completamente del Aggregate Root.

---

# Value Objects

Los Value Objects son preferibles a las entidades siempre
que exista ausencia de identidad.

Los Value Objects deben ser:

- inmutables;
- comparables por valor;
- libres de efectos secundarios.

---

# Domain Events

Cuando un Aggregate cambia significativamente su estado debe generar y
registrar un Domain Event. Application coordina cualquier publicación
interna después de persistir exitosamente el Aggregate.

Ejemplos:

- OrganizationCreated
- MemberJoined
- ProposalApproved
- AssemblyCompleted

Los eventos representan hechos consumados.

Nunca representan intenciones.

---

# Transacciones

Una transacción nunca debe modificar múltiples Aggregates.

Si varios Aggregates necesitan colaborar, se utiliza:

- Application Services para orquestación;
- Integration Events para cruzar Bounded Contexts;
- sagas o process managers cuando una decisión explícita los adopte.

---

# Servicios de Dominio

Si una regla requiere múltiples Aggregates, la lógica debe
ubicarse en un Domain Service.

Nunca dentro de un Aggregate.

---

# Dependencias

Un Aggregate únicamente puede depender de:

- Entities propias;
- Value Objects propios;
- Domain Services;
- Shared Kernel.

Nunca depende de:

- Infrastructure;
- Frameworks;
- HTTP;
- ORM;
- Base de datos.

---

# Encapsulamiento

El estado interno nunca se expone para modificación.

Los consumidores interactúan exclusivamente mediante
comportamientos del dominio.

Las operaciones expresan intención del negocio.

Ejemplos:

approveProposal()

completeAssembly()

registerCitizen()

Nunca:

setStatus()

setVotes()

setName()

---

# Reglas Arquitectónicas

## Regla 1

Todo Aggregate posee exactamente un Aggregate Root.

---

## Regla 2

Toda modificación ocurre mediante el Aggregate Root.

---

## Regla 3

Las invariantes nunca pueden violarse.

---

## Regla 4

No existen referencias directas entre Aggregates.

---

## Regla 5

Los Aggregates son pequeños.

---

## Regla 6

Cada Aggregate posee un único Repository.

---

## Regla 7

Las entidades internas no tienen repositorios propios.

---

## Regla 8

Los cambios relevantes generan Domain Events.

---

## Regla 9

Las transacciones nunca abarcan múltiples Aggregates.

---

## Regla 10

Los Aggregates representan conceptos del negocio, nunca
estructuras de almacenamiento.

---

# Beneficios

La aplicación de estas reglas permite:

- consistencia fuerte;
- bajo acoplamiento;
- alta cohesión;
- mejor concurrencia;
- evolución independiente;
- facilidad de pruebas;
- mayor claridad del modelo;
- escalabilidad del dominio.

---

# Definición de Éxito

Todo Aggregate de AURA Core protege completamente sus
invariantes, encapsula el comportamiento del negocio,
mantiene consistencia interna y colabora con otros
Aggregates exclusivamente mediante contratos explícitos,
identificadores e Integration Events cuando cruza contextos.