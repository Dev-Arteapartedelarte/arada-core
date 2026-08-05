# ============================================================
# ARADA
# ============================================================

# Proyecto

AURA Core

---

# Unidad

CORE-002

---

# Documento

Bounded Context Map

---

# ADR relacionado

ADR-001
ADR-002 (pendiente)

---

# Objetivo

Definir oficialmente los Bounded Contexts que conforman
el dominio de la plataforma AURA.

Este documento constituye el mapa conceptual del sistema
y establece los límites de cada subdominio.

No define implementación.

Define lenguaje.

Define responsabilidades.

Define fronteras.

---

# Principios

Cada contexto posee:

• su propio modelo

• su propio lenguaje

• sus propias reglas

• sus propios eventos

• su propia evolución

Nunca se comparte el modelo interno entre contextos.

La comunicación siempre ocurre mediante contratos.

---

# Visión General

                    +--------------------+
                    |   Identity         |
                    +---------+----------+
                              |
                              |
                              v
                    +--------------------+
                    | Community          |
                    +---------+----------+
                              |
              +---------------+----------------+
              |                                |
              v                                v
      +---------------+               +----------------+
      | Participation |               | Organization   |
      +-------+-------+               +--------+-------+
              |                                |
              +---------------+----------------+
                              |
                              v
                    +--------------------+
                    | Requests           |
                    +---------+----------+
                              |
                              v
                    +--------------------+
                    | Workflow           |
                    +---------+----------+
                              |
                              v
                    +--------------------+
                    | Notification       |
                    +---------+----------+
                              |
                              v
                    +--------------------+
                    | Integration        |
                    +---------+----------+
                              |
                              v
                    +--------------------+
                    | Smart City         |
                    +--------------------+

---

# Contextos Oficiales

La plataforma se divide inicialmente en
nueve Bounded Contexts.

---

## 1.

Identity

Responsabilidad

Gestionar identidades.

Incluye:

- autenticación

- autorización

- roles

- permisos

No conoce organizaciones.

No conoce juntas de vecinos.

No conoce solicitudes.

---

## 2.

Community

Representa la comunidad.

Conceptos:

- vecinos

- dirigentes

- comunidades

- relaciones

Es el corazón social del sistema.

---

## 3.

Organization

Representa organizaciones.

Ejemplos:

- junta de vecinos

- comité

- asociación

- corporación

No administra usuarios.

Administra organizaciones.

---

## 4.

Participation

Representa toda interacción ciudadana.

Incluye:

- votaciones

- consultas

- encuestas

- cabildos

- participación digital

---

## 5.

Requests

Gestiona necesidades.

Ejemplos:

- reclamos

- solicitudes

- incidentes

- requerimientos

- propuestas

No ejecuta procesos.

Sólo administra solicitudes.

---

## 6.

Workflow

Motor de procesos.

Responsabilidad

Mover estados.

Ejemplo

Creado

↓

Validado

↓

Asignado

↓

En ejecución

↓

Finalizado

No conoce el significado del proceso.

Sólo administra estados.

---

## 7.

Notification

Eventos.

Correo.

Push.

WhatsApp.

SMS.

WebSocket.

Nunca contiene lógica de negocio.

---

## 8.

Integration

Adaptadores externos.

Ejemplos

Municipalidad

Keycloak

Correo

Open311

FIWARE

Blockchain

LoRaWAN

APIs externas

Nunca contiene reglas del dominio.

---

## 9.

Smart City

Modelo urbano.

Entidades:

sensores

IoT

NGSI-LD

FIWARE

Digital Twin

Open Data

No conoce usuarios.

No conoce autenticación.

Sólo ciudad.

---

# Relaciones

Identity
↓

Community

Community
↓

Organization

Organization
↓

Participation

Organization
↓

Requests

Requests
↓

Workflow

Workflow
↓

Notification

Integration conecta todos los contextos
mediante Anti-Corruption Layers.

Smart City consume eventos publicados
por los demás contextos.

---

# Dependencias Permitidas

Identity

↓

Community

↓

Organization

↓

Participation

↓

Requests

↓

Workflow

↓

Notification

↓

Integration

↓

Smart City

Las dependencias son únicamente hacia abajo.

Nunca hacia arriba.

Nunca circulares.

---

# Lenguaje Ubicuo

Cada contexto mantiene su propio
lenguaje.

Ejemplo

Community

Vecino

Dirigente

Comunidad

--------------------------------

Requests

Solicitud

Incidente

Caso

Estado

--------------------------------

Workflow

Proceso

Transición

Paso

Estado

--------------------------------

Smart City

Entidad NGSI-LD

Sensor

Gemelo Digital

Evento

---

# Reglas

Un contexto nunca modifica directamente
el estado interno de otro.

La comunicación ocurre mediante:

• Eventos

o

• APIs públicas

Nunca mediante acceso directo.

---

# Eventos del Dominio

Ejemplos

CitizenRegistered

OrganizationCreated

RequestCreated

RequestAssigned

WorkflowStarted

WorkflowFinished

NotificationSent

SensorUpdated

MunicipalitySynchronized

---

# Objetivo Arquitectónico

Mantener un dominio:

cohesionado

desacoplado

extensible

orientado al negocio

independiente de frameworks.

---

# Estado

Versión

1.0

Estado

Aprobado

Proyecto

Project Chrysalis

Autor

ARADA
