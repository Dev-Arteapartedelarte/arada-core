# CORE-011 — Repository Contracts

Versión: 1.0

Estado: Oficial

Proyecto: AURA Core

Autor: ARADA

---

# Objetivo

Definir las reglas oficiales para el diseño de los
Repositories dentro de AURA Core.

Los Repositories constituyen la frontera entre el dominio y
los mecanismos de persistencia.

Su responsabilidad consiste exclusivamente en proporcionar
la ilusión de una colección de Aggregates pertenecientes al
dominio, ocultando completamente la infraestructura.

---

# Definición

Un Repository es un contrato del dominio encargado de
recuperar y persistir Aggregates.

Un Repository no implementa reglas de negocio.

No contiene lógica de infraestructura visible para el
dominio.

Representa únicamente una abstracción.

---

# Responsabilidad

Todo Repository debe ser responsable únicamente de:

- recuperar Aggregates;
- persistir Aggregates;
- eliminar Aggregates cuando el dominio lo permita.

Nada más.

---

# Ubicación

Los contratos de Repository pertenecen al Dominio.

Las implementaciones pertenecen a Infrastructure.

Ejemplo:

src/

domain/

repositories/

OrganizationRepository.ts

infrastructure/

persistence/

postgres/

PostgresOrganizationRepository.ts

---

# Un Repository por Aggregate

Existe exactamente un Repository por Aggregate Root.

Correcto:

OrganizationRepository

CitizenRepository

AssemblyRepository

ProposalRepository

Incorrecto:

MemberRepository

AddressRepository

VoteRepository

cuando éstos pertenecen internamente a otro Aggregate.

---

# Unidad de Persistencia

El Repository siempre trabaja con el Aggregate completo.

Nunca persiste entidades internas por separado.

El Aggregate constituye la unidad mínima de persistencia.

---

# Interfaces

Los contratos se expresan mediante interfaces.

Ejemplo conceptual:

Repository<T>

OrganizationRepository

CitizenRepository

ProposalRepository

---

# Dependencias

Los contratos de Repository pueden depender únicamente de:

- Aggregates;
- Value Objects;
- Identificadores;
- Shared Kernel.

Nunca dependen de:

- SQL;
- PostgreSQL;
- MongoDB;
- Redis;
- HTTP;
- ORM;
- FastAPI;
- Django.

---

# Implementaciones

Las implementaciones pertenecen exclusivamente a
Infrastructure.

El dominio nunca conoce cuál implementación se utiliza.

Ejemplos:

PostgreSQL

MongoDB

SQLite

REST

GraphQL

Event Store

Todas implementan exactamente el mismo contrato.

---

# Operaciones

Todo Repository puede ofrecer únicamente operaciones que
tengan significado para el dominio.

Ejemplos:

save()

findById()

exists()

remove()

Nunca operaciones orientadas al almacenamiento.

Incorrecto:

executeSQL()

insertRow()

updateRecord()

runQuery()

---

# Consultas

Las consultas complejas pertenecen al modelo de lectura.

No deben sobrecargar el Repository del dominio.

Para consultas especializadas se utilizarán:

- Read Models;
- Query Services;
- CQRS (cuando corresponda).

---

# Identificadores

Toda búsqueda utiliza Value Objects como identificadores.

Correcto:

findById(
OrganizationId,
)

Incorrecto:

findById(
string,
)

---

# Nullabilidad

Los métodos de búsqueda deben expresar claramente la
posibilidad de ausencia.

Ejemplos:

Option<Aggregate>

Result<Aggregate>

Aggregate | null

La convención oficial será definida en el Shared Kernel.

---

# Persistencia Transparente

El dominio nunca conoce:

- transacciones;
- conexiones;
- pools;
- sesiones;
- cursores;
- drivers.

Toda esa responsabilidad pertenece a Infrastructure.

---

# Consistencia

Los Repositories respetan los límites definidos por los
Aggregates.

Nunca permiten persistir estados inconsistentes.

---

# Domain Events

La publicación de Domain Events no pertenece al Repository.

El Repository únicamente persiste el Aggregate.

La coordinación de eventos pertenece a la capa de
Application o a un mecanismo de Unit of Work.

---

# Unit of Work

Cuando exista Unit of Work, el Repository colaborará con él.

El dominio continúa sin conocer su existencia.

---

# Testing

Los contratos permiten sustituir implementaciones reales
por:

- Fakes;
- Stubs;
- Mocks;
- Repositories en memoria.

Las pruebas del dominio nunca requieren una base de datos
real.

---

# Convenciones

Todo contrato deberá nombrarse utilizando el Aggregate Root.

Ejemplos:

OrganizationRepository

CitizenRepository

AssemblyRepository

ProposalRepository

Nunca:

Organizations

OrganizationDAO

OrganizationStorage

OrganizationPersistence

---

# Reglas Arquitectónicas

## Regla 1

Todo Repository pertenece al Dominio.

---

## Regla 2

Toda implementación pertenece a Infrastructure.

---

## Regla 3

Existe un único Repository por Aggregate Root.

---

## Regla 4

Los Repositories trabajan exclusivamente con Aggregates.

---

## Regla 5

Nunca contienen reglas del negocio.

---

## Regla 6

Nunca exponen detalles de persistencia.

---

## Regla 7

Toda búsqueda utiliza Value Objects como identificadores.

---

## Regla 8

Las consultas complejas pertenecen a Query Services o Read
Models.

---

## Regla 9

Los contratos permanecen independientes de cualquier motor
de almacenamiento.

---

## Regla 10

El dominio nunca conoce la implementación concreta de un
Repository.

---

# Beneficios

La aplicación de estas reglas proporciona:

- independencia tecnológica;
- facilidad para cambiar motores de persistencia;
- bajo acoplamiento;
- alta cohesión;
- mayor testabilidad;
- protección del dominio;
- evolución independiente de la infraestructura;
- claridad arquitectónica.

---

# Definición de Éxito

Todos los Repositories de AURA Core representan contratos
puros del dominio, trabajan exclusivamente con Aggregates,
ocultan completamente la infraestructura de persistencia y
permiten sustituir cualquier implementación sin modificar
el modelo de dominio.