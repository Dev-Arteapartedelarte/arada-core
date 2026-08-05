# ============================================================
# ARADA
# ============================================================

# Proyecto

AURA Core

---

# Unidad

CORE-004

---

# Documento

Ubiquitous Language

---

# ADR relacionados

ADR-001

ADR-002

ADR-003

---

# Objetivo

Definir el Lenguaje Ubicuo oficial de AURA.

Todo concepto utilizado por el dominio debe poseer un
único significado.

El mismo término deberá utilizarse en:

• documentación

• código

• APIs

• eventos

• interfaces

• base de datos

• conversaciones técnicas

• conversaciones con expertos del dominio

No existen sinónimos dentro del dominio.

Una palabra representa exactamente un concepto.

---

# Principios

El Lenguaje Ubicuo constituye el contrato lingüístico
del dominio.

Todo cambio en el vocabulario debe realizarse mediante
un ADR.

El lenguaje pertenece al negocio.

No pertenece al software.

---

# Reglas

## 1.

Un concepto posee un único nombre.

Ejemplo

Correcto

Request

Incorrecto

Request

Ticket

Issue

Case

Todos representan el mismo concepto.

Sólo uno puede existir.

---

## 2.

Un nombre nunca cambia dependiendo
del contexto técnico.

Ejemplo

Request

No cambia a:

DTO

Model

Entity

Table

JSON

El concepto continúa siendo Request.

---

## 3.

Las clases utilizan exactamente el mismo
nombre definido por el dominio.

Ejemplo

Community

Organization

Citizen

Request

Workflow

Notification

Sensor

DigitalTwin

---

## 4.

Los eventos utilizan lenguaje del dominio.

Ejemplos

CitizenRegistered

OrganizationCreated

RequestCreated

RequestAssigned

WorkflowStarted

WorkflowCompleted

NotificationSent

SensorUpdated

---

## 5.

Los comandos utilizan verbos.

Ejemplos

CreateOrganization

ApproveRequest

RegisterCitizen

AssignRequest

CloseWorkflow

PublishNotification

---

## 6.

Las consultas utilizan lenguaje del negocio.

Ejemplos

FindCitizen

SearchOrganizations

ListRequests

GetWorkflowHistory

---

# Diccionario Oficial

---

## Citizen

Representa una persona que participa
en la comunidad.

Nunca utilizar:

User

Client

Person

Member

Actor

El dominio utiliza:

Citizen

---

## Community

Conjunto de ciudadanos que comparten
un territorio o interés.

Nunca:

Group

Collection

People

---

## Organization

Entidad formal reconocida.

Ejemplos

Junta de Vecinos

Comité

Corporación

Fundación

Asociación

---

## Membership

Relación entre un Citizen
y una Organization.

No representa al ciudadano.

Representa el vínculo.

---

## Request

Necesidad registrada por la comunidad.

Ejemplos

Solicitud

Incidente

Reclamo

Propuesta

Observación

Todos pertenecen al mismo concepto.

Request.

---

## Workflow

Proceso que mueve un Request
entre estados.

No representa reglas.

Representa el flujo.

---

## State

Situación actual
de un Aggregate.

Ejemplo

Pending

Assigned

Resolved

Closed

---

## Transition

Cambio entre dos estados.

Ejemplo

Pending

↓

Assigned

---

## Notification

Mensaje generado por un evento.

No representa correo.

No representa WhatsApp.

Representa una intención
de comunicación.

---

## Event

Hecho ocurrido
en el dominio.

Nunca representa:

mensaje

API

callback

---

## Domain Event

Evento publicado por un Aggregate.

Ejemplo

CitizenRegistered

---

## Aggregate

Límite de consistencia
del dominio.

Nunca corresponde
a una tabla.

Nunca corresponde
a un microservicio.

---

## Aggregate Root

Único punto de entrada
al Aggregate.

Toda modificación ocurre
a través de él.

---

## Entity

Objeto con identidad.

Ejemplo

Citizen

Organization

Request

---

## Value Object

Objeto sin identidad.

Ejemplo

Email

Address

Coordinates

PhoneNumber

GeoLocation

---

## Repository

Contrato para obtener
Aggregates.

Nunca contiene
lógica de negocio.

---

## Specification

Regla reutilizable.

Puede combinarse.

Puede componerse.

No modifica estado.

---

## Domain Service

Servicio del dominio.

Existe cuando una regla
no pertenece naturalmente
a una Entity
ni a un Value Object.

---

## Integration

Comunicación con sistemas externos.

Ejemplos

Municipalidad

FIWARE

Open311

Blockchain

Correo

SMS

Keycloak

Nunca contiene
reglas del dominio.

---

## Smart City

Modelo urbano digital.

Incluye

IoT

NGSI-LD

Gemelos Digitales

Sensores

Datos abiertos

---

## Digital Twin

Representación digital
de un activo físico.

Ejemplos

Barrio

Semáforo

Sensor

Espacio público

---

## Sensor

Fuente de datos.

No representa dispositivos.

Representa una entidad
del dominio Smart City.

---

## Capability

Capacidad observable
de un sistema.

Ejemplo

Puede autenticar.

Puede sincronizar.

Puede votar.

---

## Policy

Conjunto de reglas
que gobiernan un proceso.

No representa código.

Representa negocio.

---

## Permission

Acción autorizada.

Ejemplo

ReadRequest

CreateRequest

ApproveWorkflow

---

## Role

Conjunto de permisos.

Nunca representa
una persona.

---

## Identity

Representa la identidad
digital.

No representa
la persona.

---

# Verbos Oficiales

Create

Register

Assign

Approve

Reject

Close

Archive

Publish

Synchronize

Validate

Update

Remove

Deactivate

Activate

Search

Find

List

Resolve

Notify

---

# Sustantivos Oficiales

Citizen

Community

Organization

Membership

Request

Workflow

Notification

Event

Sensor

DigitalTwin

Integration

Identity

Permission

Role

Policy

Specification

Repository

Aggregate

Entity

ValueObject

---

# Prefijos Permitidos

Create

Update

Delete

Register

Assign

Publish

Notify

Resolve

Search

Find

List

Sync

Validate

---

# Prefijos Prohibidos

Do

Process

Execute

Handle

Manager

Helper

Utils

Misc

Common

Data

Generic

BaseManager

---

# Convenciones de Código

Clases

PascalCase

Ejemplo

Request

Citizen

Workflow

---

Interfaces

PascalCase

Sin prefijo "I".

Correcto

Repository

Incorrecto

IRepository

---

Métodos

camelCase

Ejemplo

createRequest()

assignCitizen()

publishEvent()

---

Constantes

UPPER_SNAKE_CASE

Ejemplo

DEFAULT_PRIORITY

MAX_REQUESTS

---

Archivos

snake_case

Ejemplo

request_repository.py

workflow_service.py

notification_policy.py

---

# Beneficios

El Lenguaje Ubicuo permite:

• reducir ambigüedad

• mejorar comunicación

• disminuir deuda técnica

• facilitar el onboarding

• mantener coherencia

• desacoplar el dominio
  de la tecnología

• preservar el conocimiento
  del negocio

---

# Estado

Versión

1.0

Estado

Aprobado

Proyecto

AURA Core

Autor

ARADA