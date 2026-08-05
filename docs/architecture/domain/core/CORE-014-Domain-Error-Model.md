# CORE-014 — Domain Error Model

Versión: 1.0

Estado: Oficial

Proyecto: AURA Core

Autor: ARADA

---

# Objetivo

Definir el modelo oficial de errores del dominio para
AURA Core.

El propósito de este documento es establecer un mecanismo
uniforme para representar fallos del negocio sin depender
de excepciones técnicas, frameworks o tecnologías de
infraestructura.

Los errores del dominio representan conocimiento del
negocio y forman parte del Lenguaje Ubicuo.

---

# Principios

El modelo de errores debe cumplir los siguientes
principios:

- representar únicamente errores del negocio;
- ser independiente de la infraestructura;
- ser explícito;
- ser determinista;
- ser tipado;
- ser fácilmente testeable;
- formar parte del modelo de dominio.

---

# Qué es un Domain Error

Un Domain Error representa una condición del negocio que
impide completar correctamente una operación del dominio.

No representa errores técnicos.

Ejemplos:

- organización inactiva;
- ciudadano ya registrado;
- propuesta cerrada;
- quórum insuficiente;
- período de votación expirado.

---

# Qué NO es un Domain Error

Los siguientes casos no pertenecen al dominio:

- timeout de red;
- error SQL;
- conexión perdida;
- archivo inexistente;
- fallo HTTP;
- excepción del framework;
- error del sistema operativo.

Todos ellos pertenecen a Infrastructure.

---

# Clasificación

Los Domain Errors se clasifican en categorías.

## Validation Errors

Representan datos válidos sintácticamente, pero inválidos
para el negocio.

Ejemplos:

- nombre duplicado;
- RUT ya registrado;
- correo ya utilizado.

---

## State Errors

Representan estados incompatibles con la operación.

Ejemplos:

- organización archivada;
- propuesta cerrada;
- asamblea finalizada.

---

## Business Rule Errors

Representan la violación de una regla del dominio.

Ejemplos:

- quórum insuficiente;
- votación duplicada;
- presupuesto excedido.

---

## Authorization Errors

Representan permisos definidos por el negocio, no por la
seguridad técnica.

Ejemplos:

- ciudadano no pertenece a la organización;
- directiva sin atribuciones para convocar;
- vecino no habilitado para votar.

---

## Consistency Errors

Representan violaciones de invariantes.

Ejemplos:

- Aggregate inconsistente;
- estado imposible;
- referencia inválida.

---

# Representación

Todo Domain Error debe representarse mediante un tipo del
dominio.

Nunca mediante cadenas de texto arbitrarias.

Ejemplo conceptual:

OrganizationAlreadyExists

CitizenAlreadyRegistered

ProposalClosed

InsufficientQuorum

VoteAlreadyRegistered

---

# Inmutabilidad

Todo Domain Error es inmutable.

Una vez creado, su información nunca cambia.

---

# Información Mínima

Todo Domain Error debe contener:

- identificador;
- nombre;
- descripción;
- categoría.

Opcionalmente puede incluir:

- Aggregate involucrado;
- identificador del recurso;
- metadatos del dominio.

---

# Lenguaje

Los nombres de los errores deben utilizar el Lenguaje
Ubicuo.

Correcto:

ProposalClosed

AssemblyAlreadyOpen

CitizenNotEligible

OrganizationInactive

Incorrecto:

Error101

BusinessException

InvalidState

Failure

UnknownError

---

# Excepciones

Las excepciones del lenguaje de programación no forman
parte del modelo de dominio.

Las excepciones técnicas deben convertirse en errores del
dominio o manejarse en Infrastructure, según corresponda.

---

# Propagación

Los Domain Errors pueden propagarse mediante mecanismos
tipados como:

- Result;
- Either;
- Option;
- Error Objects.

La estrategia concreta será definida por el Shared Kernel.

---

# Domain Services

Los Domain Services pueden producir Domain Errors cuando
una regla del negocio no puede satisfacerse.

Nunca generan errores técnicos.

---

# Aggregates

Los Aggregates son responsables de detectar y producir
errores relacionados con sus propias invariantes.

---

# Application Services

Los Application Services reciben Domain Errors y deciden
cómo transformarlos para las capas externas.

Por ejemplo:

Domain Error

↓

HTTP 409

↓

GraphQL Error

↓

gRPC Status

↓

Evento de rechazo

El dominio nunca conoce estas transformaciones.

---

# Infraestructura

Infrastructure nunca define Domain Errors.

Puede capturar errores técnicos y traducirlos cuando sea
necesario.

---

# Persistencia

Los errores de persistencia nunca llegan al dominio como
errores SQL.

Siempre deben convertirse en una abstracción apropiada o
ser tratados en la infraestructura.

---

# Testing

Todo Domain Error debe poder verificarse mediante pruebas
unitarias.

No requiere infraestructura para su validación.

---

# Ubicación

Los tipos de error pertenecen al Dominio.

Ejemplo:

src/

domain/

errors/

OrganizationAlreadyExists.ts

ProposalClosed.ts

InsufficientQuorum.ts

CitizenNotEligible.ts

---

# Reglas Arquitectónicas

## Regla 1

Todo Domain Error representa una condición del negocio.

---

## Regla 2

Nunca representa un fallo técnico.

---

## Regla 3

Todo Domain Error es inmutable.

---

## Regla 4

Utiliza el Lenguaje Ubicuo.

---

## Regla 5

Los Aggregates producen errores relacionados con sus
invariantes.

---

## Regla 6

Los Domain Services producen errores asociados a reglas
compartidas del negocio.

---

## Regla 7

Los Application Services traducen los errores hacia las
capas externas.

---

## Regla 8

Infrastructure nunca define errores del dominio.

---

## Regla 9

Los errores poseen identidad y categoría explícitas.

---

## Regla 10

El dominio nunca depende de excepciones del lenguaje o del
framework.

---

# Beneficios

La aplicación de este modelo proporciona:

- lenguaje uniforme para los fallos del negocio;
- independencia tecnológica;
- mayor expresividad del dominio;
- mejor testabilidad;
- desacoplamiento respecto a frameworks;
- trazabilidad de reglas de negocio;
- integración sencilla con distintas interfaces
  (REST, GraphQL, gRPC, eventos);
- evolución consistente del modelo.

---

# Definición de Éxito

Todos los errores de AURA Core representan únicamente
condiciones del negocio, forman parte del Lenguaje Ubicuo,
son independientes de la infraestructura, se expresan
mediante tipos explícitos e inmutables y permiten que el
dominio permanezca completamente desacoplado de cualquier
mecanismo técnico de manejo de errores.