# CORE-013 — Application Services

Versión: 1.0

Estado: Oficial

Proyecto: AURA Core

Autor: ARADA

---

# Objetivo

Definir las reglas oficiales para el diseño de los
Application Services dentro de AURA Core.

Los Application Services representan la capa de
orquestación del sistema.

Su responsabilidad consiste en coordinar la ejecución de
casos de uso utilizando el modelo de dominio, sin contener
reglas de negocio.

---

# Definición

Un Application Service implementa un caso de uso de la
plataforma.

Coordina la interacción entre:

- Aggregates;
- Domain Services;
- Repositories;
- Event Bus;
- Unit of Work;
- servicios de infraestructura.

No implementa reglas del negocio.

---

# Responsabilidad

Todo Application Service debe:

- iniciar un caso de uso;
- recuperar Aggregates;
- invocar Domain Services;
- modificar Aggregates;
- persistir cambios;
- coordinar transacciones;
- publicar Domain Events;
- devolver un resultado.

Nada más.

---

# Ubicación

Los Application Services pertenecen a la capa
Application.

Ejemplo:

src/

application/

services/

CreateOrganizationService.ts

RegisterCitizenService.ts

CreateProposalService.ts

VoteProposalService.ts

---

# Flujo General

Todo Application Service sigue el mismo patrón.

1. Recibe una solicitud.

2. Valida datos estructurales.

3. Recupera Aggregates.

4. Invoca el dominio.

5. Persiste cambios.

6. Publica Domain Events.

7. Devuelve un resultado.

---

# Responsabilidades Permitidas

Un Application Service puede:

- abrir transacciones;
- utilizar Repositories;
- utilizar Domain Services;
- invocar Aggregates;
- construir DTOs;
- coordinar Event Bus;
- coordinar Unit of Work.

---

# Responsabilidades Prohibidas

Nunca puede:

- implementar reglas del negocio;
- modificar directamente Entities;
- acceder directamente a SQL;
- generar respuestas HTTP;
- renderizar vistas;
- contener lógica de UI;
- conocer detalles del framework.

---

# Dependencias

Los Application Services pueden depender de:

- Domain;
- Repository Contracts;
- Domain Services;
- Shared Kernel;
- Event Bus;
- Unit of Work.

Nunca dependen de componentes de presentación.

---

# Validaciones

Las validaciones se dividen en dos categorías.

## Validaciones estructurales

Pertenecen al Application Service.

Ejemplos:

- DTO válido;
- campos obligatorios;
- formato JSON;
- autenticación;
- autorización.

---

## Validaciones del negocio

Pertenecen exclusivamente al Dominio.

Ejemplos:

- quórum;
- elegibilidad;
- estado permitido;
- invariantes;
- permisos del negocio.

---

# DTO

Los Application Services reciben DTOs.

Nunca reciben entidades HTTP.

Ejemplo conceptual:

CreateProposalCommand

RegisterCitizenCommand

CreateAssemblyCommand

---

# Resultado

Los Application Services devuelven:

- DTOs;
- Result;
- Response Models;
- Read Models.

Nunca exponen directamente Aggregates hacia el exterior.

---

# Transacciones

El Application Service constituye el límite transaccional.

Cuando un caso de uso modifica múltiples Aggregates, la
transacción se controla aquí.

---

# Unit of Work

Cuando exista Unit of Work, será coordinado desde esta
capa.

El Dominio permanece completamente ajeno.

---

# Domain Events

Una vez completada la transacción, el Application Service
coordina la publicación de los Domain Events generados por
los Aggregates.

---

# Infraestructura

Los servicios de infraestructura únicamente se utilizan
desde esta capa.

Ejemplos:

- Email Service;
- Storage;
- Notification Service;
- Identity Provider;
- Message Broker.

El dominio nunca conoce estos servicios.

---

# CQRS

Cuando la arquitectura utilice CQRS:

Los Application Services implementan únicamente comandos.

Las consultas pertenecen a Query Services.

---

# Nomenclatura

Los nombres deben expresar claramente un caso de uso.

Correcto:

CreateOrganizationService

RegisterCitizenService

OpenAssemblyService

CloseAssemblyService

ApproveProposalService

VoteProposalService

---

Incorrecto:

OrganizationManager

ApplicationHelper

Utils

BusinessManager

CommonService

---

# Testing

Los Application Services pueden probarse utilizando:

- Repositories Fake;
- Domain Services Fake;
- Event Bus Fake;
- Unit of Work Fake.

No requieren infraestructura real.

---

# Reglas Arquitectónicas

## Regla 1

Cada Application Service implementa un único caso de uso.

---

## Regla 2

No contiene reglas del negocio.

---

## Regla 3

Toda regla del negocio pertenece al Dominio.

---

## Regla 4

Coordina Repositories y Domain Services.

---

## Regla 5

Controla el límite transaccional.

---

## Regla 6

Coordina la publicación de Domain Events.

---

## Regla 7

No conoce detalles de presentación.

---

## Regla 8

Puede utilizar servicios de infraestructura mediante
abstracciones.

---

## Regla 9

Devuelve DTOs o modelos de respuesta.

Nunca expone Aggregates.

---

## Regla 10

Cada servicio representa exactamente un caso de uso.

---

# Relación con el Dominio

Application Services utilizan el dominio.

El dominio nunca conoce la existencia de los Application
Services.

La dependencia siempre apunta hacia el dominio.

---

# Beneficios

La aplicación de estas reglas proporciona:

- separación clara entre coordinación y negocio;
- casos de uso explícitos;
- independencia del framework;
- facilidad de pruebas;
- transacciones bien definidas;
- integración controlada con infraestructura;
- mayor mantenibilidad;
- evolución independiente del dominio.

---

# Definición de Éxito

Todos los Application Services de AURA Core representan un
único caso de uso, coordinan exclusivamente la interacción
entre los componentes del dominio y la infraestructura,
mantienen el dominio libre de responsabilidades técnicas y
garantizan una arquitectura limpia, desacoplada y
fácilmente evolutiva.