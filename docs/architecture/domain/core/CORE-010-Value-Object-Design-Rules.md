# CORE-010 — Value Object Design Rules

Versión: 1.0

Estado: Oficial

Proyecto: AURA Core

Autor: ARADA

---

# Objetivo

Definir las reglas oficiales para el diseño de Value
Objects dentro de AURA Core.

Los Value Objects representan conceptos del dominio cuyo
significado está determinado exclusivamente por su valor y
no por una identidad propia.

Este documento establece los principios para garantizar un
modelo de dominio expresivo, seguro e inmutable.

---

# Definición

Un Value Object representa una característica, atributo o
concepto del dominio que no posee identidad.

Dos Value Objects son iguales cuando todos sus valores son
iguales.

No existe noción de ciclo de vida independiente.

---

# Características Fundamentales

Todo Value Object debe cumplir las siguientes propiedades:

- No posee identidad.
- Es completamente inmutable.
- Se compara por valor.
- Es autoconsistente.
- Representa un concepto del negocio.
- No posee efectos secundarios.

---

# Igualdad

La igualdad depende exclusivamente de sus atributos.

Correcto:

Email("ana@arada.cl") ==
Email("ana@arada.cl")

Incorrecto:

Comparar referencias de memoria.

---

# Inmutabilidad

Todo Value Object es completamente inmutable.

Después de su construcción no puede modificarse ningún
atributo.

Toda operación genera una nueva instancia.

Correcto:

newAddress =
oldAddress.changeCity("Temuco")

Incorrecto:

address.city = "Temuco"

---

# Construcción

Un Value Object siempre debe construirse en un estado
válido.

Nunca puede existir una instancia inválida.

Las validaciones ocurren durante la creación.

---

# Validación

Las reglas del negocio forman parte del propio Value
Object.

Ejemplo:

Email

- formato válido
- longitud máxima
- dominio permitido (si aplica)

Coordinates

- latitud válida
- longitud válida

Money

- moneda válida
- monto permitido

---

# Encapsulamiento

Los atributos permanecen protegidos.

Los consumidores únicamente utilizan la interfaz pública
del Value Object.

Nunca modifican directamente su estado.

---

# Comportamiento

Los Value Objects contienen comportamiento relacionado con
su propio significado.

Ejemplos:

Money.add()

Money.subtract()

Coordinates.distanceTo()

Email.domain()

DateRange.contains()

---

# Ausencia de Identidad

Nunca se asignan identificadores a un Value Object.

Incorrecto:

AddressId

MoneyId

CoordinatesId

Correcto:

Address

Money

Coordinates

---

# Persistencia

Los Value Objects no conocen mecanismos de persistencia.

Nunca contienen:

- SQL
- ORM
- HTTP
- Frameworks
- MongoDB

Su persistencia es responsabilidad del Repository del
Aggregate.

---

# Reutilización

Los Value Objects pueden reutilizarse en múltiples
Aggregates siempre que conserven exactamente el mismo
significado.

Si un mismo concepto cambia de significado según el
contexto, deben definirse Value Objects diferentes.

---

# Composición

Un Value Object puede componerse de otros Value Objects.

Ejemplo:

Address

compuesto por:

- Street
- City
- PostalCode
- Country

Cada componente mantiene sus propias invariantes.

---

# Dependencias

Los Value Objects únicamente pueden depender de:

- otros Value Objects;
- Shared Kernel;
- tipos primitivos cuando corresponda.

Nunca dependen de:

- Infrastructure;
- Frameworks;
- Repositories;
- Services.

---

# Efectos Secundarios

Los Value Objects nunca producen efectos secundarios.

Nunca:

- escriben en bases de datos;
- envían eventos;
- realizan llamadas HTTP;
- modifican objetos externos.

Toda operación es determinista.

---

# Conversión

Cuando sea necesario convertir un Value Object a un tipo
primitivo, la conversión debe ser explícita.

Ejemplo:

Email.value()

Money.amount()

Coordinates.latitude()

Nunca exponer internamente su representación para permitir
modificaciones externas.

---

# Serialización

Los Value Objects pueden serializarse para comunicación
externa.

La serialización no modifica su comportamiento ni rompe su
inmutabilidad.

---

# Ejemplos

## Identificadores

- OrganizationId
- CitizenId
- ProposalId

---

## Localización

- Coordinates
- Address
- Region
- Commune

---

## Comunicación

- Email
- PhoneNumber
- Url

---

## Tiempo

- DateRange
- TimeWindow
- Timestamp

---

## Economía

- Money
- Currency

---

## Geometría

- Distance
- Area
- Radius

---

# Reglas Arquitectónicas

## Regla 1

Todo Value Object es inmutable.

---

## Regla 2

No posee identidad.

---

## Regla 3

La igualdad depende únicamente del valor.

---

## Regla 4

Siempre se construye en un estado válido.

---

## Regla 5

Toda validación pertenece al propio Value Object.

---

## Regla 6

Nunca produce efectos secundarios.

---

## Regla 7

Puede contener comportamiento relacionado con su
significado.

---

## Regla 8

No depende de Infrastructure.

---

## Regla 9

Puede componerse de otros Value Objects.

---

## Regla 10

Representa un concepto del negocio, nunca un mecanismo de
persistencia.

---

# Beneficios

La aplicación de estas reglas proporciona:

- mayor expresividad del dominio;
- reducción de errores;
- eliminación de estados inválidos;
- facilidad de pruebas;
- reutilización segura;
- menor acoplamiento;
- mayor legibilidad del modelo;
- consistencia semántica.

---

# Definición de Éxito

Todos los Value Objects de AURA Core representan conceptos
claros del negocio, son completamente inmutables, se
comparan exclusivamente por valor y encapsulan las
validaciones necesarias para garantizar que nunca existan
instancias inválidas dentro del dominio.