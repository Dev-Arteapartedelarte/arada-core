# DOMAIN-001N — Performance Rules

Versión: 1.0

Estado:
Oficial

Proyecto:
AURA Core

Bounded Context:
Organization Management

Aggregate:
Organization

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-001-Aggregate.md
- DOMAIN-001G-Repository-Contract.md
- DOMAIN-001J-Consistency-Boundary.md
- DOMAIN-001L-Read-Model.md
- DOMAIN-001M-Test-Scenarios.md
- CORE-015-Package-Architecture.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Definir las reglas oficiales de rendimiento para el
Aggregate **Organization**.

Estas reglas establecen restricciones arquitectónicas
destinadas a garantizar un dominio predecible,
escalable y desacoplado de preocupaciones de
infraestructura.

El objetivo principal es preservar la rapidez del
modelo de dominio independientemente del crecimiento
de la plataforma.

---

# Principios

El Aggregate debe cumplir los siguientes principios.

- ejecución determinística;
- complejidad acotada;
- ausencia de operaciones bloqueantes;
- independencia del almacenamiento;
- consumo constante de memoria.

---

# Filosofía

El dominio representa conocimiento de negocio.

No representa consultas, persistencia,
comunicaciones ni procesos pesados.

Toda operación costosa pertenece a otras capas.

```text
Presentation

↓

Application

↓

Domain

↓

Infrastructure
```

El dominio siempre permanece pequeño.

---

# Regla PR-001

## Sin acceso a infraestructura

El Aggregate nunca puede realizar llamadas a:

- base de datos;
- sistema de archivos;
- HTTP;
- correo electrónico;
- mensajería;
- blockchain;
- servicios municipales;
- FIWARE;
- APIs externas.

---

# Regla PR-002

## Operaciones O(1)

Las operaciones principales del Aggregate deben tener
complejidad constante.

Ejemplos.

```text
ApproveOrganization()

SuspendOrganization()

RenameOrganization()

AssignRepresentative()
```

Todas deben ejecutarse en tiempo constante.

---

# Regla PR-003

## Colecciones Acotadas

El Aggregate no debe contener colecciones cuyo tamaño
pueda crecer indefinidamente.

Ejemplos permitidos.

```text
Representative

OrganizationType

Status
```

Ejemplos prohibidos.

```text
Todos los ciudadanos

Todos los proyectos

Todas las votaciones

Todo el historial
```

Estos elementos pertenecen a otros Aggregates.

---

# Regla PR-004

## Sin consultas complejas

El Aggregate nunca ejecuta búsquedas.

Ejemplos prohibidos.

```text
Buscar organización por nombre

Buscar por territorio

Buscar por representante

Filtrar organizaciones
```

Estas operaciones pertenecen al Read Model.

---

# Regla PR-005

## Sin iteraciones masivas

No deben existir algoritmos cuya complejidad dependa
del número total de organizaciones.

Ejemplo prohibido.

```text
for each Organization
```

Cada Aggregate trabaja únicamente sobre su propio
estado.

---

# Regla PR-006

## Sin agregaciones globales

No calcular:

- estadísticas;
- rankings;
- indicadores;
- reportes;
- dashboards.

Estas funciones pertenecen a Analytics o Read Models.

---

# Regla PR-007

## Eventos Livianos

Los Domain Events deben contener únicamente la
información necesaria para describir el cambio.

Ejemplo.

```text
OrganizationApproved

OrganizationId

OccurredAt

Version
```

No deben transportar objetos completos.

---

# Regla PR-008

## Lazy Integration

Toda integración externa ocurre después del Commit.

```text
Aggregate

↓

Commit

↓

Integration Event

↓

Infrastructure
```

El Aggregate nunca espera respuestas externas.

---

# Regla PR-009

## Consumo de Memoria

El tamaño del Aggregate debe permanecer pequeño.

Debe contener únicamente:

- Entity Root;
- Value Objects;
- referencias;
- estado actual.

Nunca información histórica completa.

---

# Regla PR-010

## Historial Externo

El historial pertenece al Event Store o a las
proyecciones.

El Aggregate mantiene solamente el estado vigente.

---

# Regla PR-011

## Read Model Especializado

Las consultas complejas utilizan modelos
desnormalizados.

Ejemplos.

```text
OrganizationDashboard

OrganizationStatistics

OrganizationSearch

OrganizationMap
```

Nunca el Aggregate.

---

# Regla PR-012

## Caché Transparente

El dominio no conoce mecanismos de caché.

Si existen, pertenecen a Infrastructure.

---

# Regla PR-013

## Sin Sincronización Distribuida

El Aggregate nunca coordina transacciones entre
múltiples servicios.

La coordinación pertenece a:

- Sagas;
- Process Managers;
- Application Services.

---

# Regla PR-014

## Versionado Optimista

La concurrencia utiliza control optimista mediante el
campo Version.

No existen bloqueos pesimistas.

---

# Regla PR-015

## Rehidratación Rápida

La reconstrucción del Aggregate debe depender
únicamente de su estado persistido o de su secuencia de
eventos.

No debe requerir consultas adicionales.

---

# Regla PR-016

## Tiempo de Ejecución

Las operaciones del Aggregate deben ejecutarse en
milisegundos.

Cualquier proceso de larga duración debe ejecutarse de
forma asíncrona mediante Integration Events.

---

# Regla PR-017

## Escalabilidad Horizontal

El Aggregate debe poder ejecutarse en múltiples nodos
sin compartir memoria.

Toda coordinación se realiza mediante persistencia y
versionado.

---

# Regla PR-018

## Independencia Tecnológica

El rendimiento del Aggregate no depende del motor de
base de datos, del broker de mensajes ni del proveedor
cloud.

El comportamiento del dominio permanece idéntico.

---

# Tabla de Complejidad Esperada

| Operación | Complejidad |
|-----------|-------------|
| Crear Organization | O(1) |
| Aprobar | O(1) |
| Suspender | O(1) |
| Reactivar | O(1) |
| Archivar | O(1) |
| Renombrar | O(1) |
| Cambiar representante | O(1) |
| Emitir Domain Event | O(1) |
| Validar invariantes | O(1) |
| Incrementar versión | O(1) |

---

# Métricas Objetivo

| Métrica | Objetivo |
|----------|----------|
| Tiempo de ejecución de un Command | < 5 ms (sin infraestructura) |
| Complejidad temporal | O(1) |
| Complejidad espacial | O(1) |
| Accesos a infraestructura | 0 |
| Dependencias externas | 0 |
| Operaciones bloqueantes | 0 |

---

# Reglas

## REG-001

El Aggregate nunca realiza consultas complejas.

---

## REG-002

Las operaciones del dominio deben ejecutarse en tiempo
constante.

---

## REG-003

Toda comunicación externa ocurre mediante eventos.

---

## REG-004

El historial completo nunca forma parte del Aggregate.

---

## REG-005

Los Read Models absorben toda carga de consulta.

---

## REG-006

La infraestructura nunca condiciona el rendimiento del
dominio.

---

## REG-007

El Aggregate debe permanecer pequeño durante toda la
vida del proyecto.

---

## REG-008

Las optimizaciones nunca deben comprometer las
invariantes del dominio.

---

## REG-009

La concurrencia utiliza exclusivamente control
optimista.

---

## REG-010

El dominio debe ser capaz de escalar horizontalmente sin
modificaciones.

---

# Diagrama Conceptual

```text
                  COMMAND

                    │
                    ▼

        Organization Aggregate
        ──────────────────────
        O(1)
        Sin I/O
        Sin Red
        Sin SQL
        Sin HTTP
        Sin Cache
        Sin Mensajería
        ──────────────────────

                    │

            Domain Events

                    │

                    ▼

        Infrastructure Layer
        ──────────────────────
        Repository
        Read Models
        Message Broker
        Analytics
        FIWARE
        Blockchain
        Municipality
        Cache
        APIs
```

---

# Definición de Éxito

El Aggregate **Organization** mantiene un rendimiento constante, independiente de la infraestructura y del volumen global de datos. Todas las operaciones críticas se ejecutan en tiempo y espacio **O(1)**, sin acceso a recursos externos, preservando un dominio altamente escalable, predecible y preparado para soportar la evolución de AURA Core hacia una plataforma distribuida de participación ciudadana e interoperabilidad con ecosistemas Smart City.