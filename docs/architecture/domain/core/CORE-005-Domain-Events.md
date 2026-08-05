# CORE-005 — Domain Events

Version: 1.0

Estado: Oficial

Proyecto: AURA Core

Autor: ARADA

ADR relacionados:

- ADR-001 Domain Driven Design
- ADR-002 Hexagonal Architecture
- ADR-003 Event Driven Core

---

# Objetivo

Definir el modelo oficial de Domain Events de AURA Core.

Los Domain Events representan hechos que ya ocurrieron
dentro del dominio.

No representan intenciones.

No representan solicitudes.

Representan cambios consumados del negocio.

---

# Definición

Un Domain Event es un objeto inmutable que describe un
hecho significativo ocurrido dentro de un Aggregate.

Ejemplos:

- PersonaRegistrada
- OrganizaciónCreada
- ProyectoPublicado
- SolicitudAceptada
- PermisoRevocado

---

# Propiedades

Todo Domain Event debe ser:

- Inmutable
- Identificable
- Serializable
- Versionable
- Independiente de infraestructura

---

# Responsabilidades

Un Domain Event permite:

- comunicar cambios entre Bounded Contexts
- desacoplar componentes
- iniciar procesos posteriores
- registrar auditoría
- reconstruir historial
- publicar integración externa

Nunca modifica el estado del dominio.

---

# Estructura Conceptual

Todo Domain Event contiene como mínimo:

- EventId
- EventName
- AggregateId
- AggregateType
- OccurredAt
- Version
- Payload

---

# Ciclo de Vida

1.

El Aggregate ejecuta una operación válida.

↓

2.

El Aggregate cambia su estado.

↓

3.

El Aggregate crea uno o más Domain Events.

↓

4.

Los eventos quedan registrados.

↓

5.

La capa de Aplicación los publica.

↓

6.

Los consumidores reaccionan.

---

# Publicación

Los Aggregates nunca publican eventos.

Únicamente los crean.

La publicación corresponde a la capa de Aplicación.

Esto mantiene al Dominio completamente desacoplado.

---

# Ejemplo Conceptual

Comando

RegistrarPersona

↓

Aggregate

Persona

↓

Cambio de estado

↓

Evento

PersonaRegistrada

↓

Application Layer

↓

Event Bus

↓

Consumidores

---

# Clasificación

## Eventos de Creación

- PersonaRegistrada
- OrganizaciónCreada
- ProyectoCreado

---

## Eventos de Actualización

- PerfilActualizado
- PermisoModificado
- ProyectoActualizado

---

## Eventos de Eliminación

- OrganizaciónEliminada
- ProyectoArchivado
- UsuarioDeshabilitado

---

## Eventos de Relación

- MiembroAgregado
- PermisoAsignado
- OrganizaciónAsociada

---

# Reglas

## Regla 1

Todo evento representa un hecho pasado.

Nunca una intención futura.

Correcto

ProyectoCreado

Incorrecto

CrearProyecto

---

## Regla 2

Todo evento es inmutable.

Nunca cambia después de ser emitido.

---

## Regla 3

Todo evento pertenece a un Aggregate Root.

Nunca nace fuera del dominio.

---

## Regla 4

Los eventos nunca contienen comportamiento.

Sólo información.

---

## Regla 5

Los eventos nunca conocen infraestructura.

No conocen:

- HTTP
- REST
- PostgreSQL
- MongoDB
- Kafka
- RabbitMQ
- Redis

---

## Regla 6

Los eventos pueden almacenarse para auditoría.

Nunca deben modificarse.

---

# Event Naming

Formato oficial

<Sustantivo><VerboEnParticipio>

Ejemplos

PersonaRegistrada

ProyectoPublicado

SolicitudAceptada

PermisoRevocado

OrganizaciónCreada

---

# Event Versioning

Todo evento posee versión.

Ejemplo

Version = 1

Si cambia su estructura:

Version = 2

Esto permite mantener compatibilidad hacia atrás.

---

# Event Payload

El Payload contiene únicamente la información necesaria
para describir el hecho ocurrido.

Debe ser lo más pequeño posible.

No debe contener objetos completos.

Debe contener identificadores y datos relevantes.

---

# Consumo

Los Domain Events pueden ser consumidos por:

- Application Services
- Event Handlers
- Integraciones
- Bounded Contexts
- Sistemas externos

Nunca por el propio Aggregate que los generó.

---

# Beneficios

El uso de Domain Events permite:

- Bajo acoplamiento
- Alta cohesión
- Escalabilidad
- Auditoría completa
- Integración entre dominios
- Eventual Consistency
- Evolución independiente de módulos

---

# Definición de Éxito

Todo cambio importante del dominio genera un Domain Event.

El dominio únicamente produce eventos.

La infraestructura decide cómo transportarlos.

De este modo, AURA Core permanece independiente de cualquier
tecnología de mensajería o mecanismo de integración.