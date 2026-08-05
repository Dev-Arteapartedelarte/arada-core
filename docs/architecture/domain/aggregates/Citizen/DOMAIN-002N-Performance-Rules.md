# DOMAIN-002N — Citizen Performance Rules

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Citizen Management

Aggregate:
Citizen

Documentos relacionados:

- DOMAIN-002-Aggregate.md
- DOMAIN-002G-Repository-Contract.md
- DOMAIN-002J-Consistency-Boundary.md
- DOMAIN-002K-Integration-Events.md
- DOMAIN-002L-Read-Model.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Este documento establece las reglas oficiales de rendimiento
(Performance Rules) para el Aggregate **Citizen**.

Su propósito es garantizar que el Aggregate mantenga un
comportamiento predecible, escalable y consistente,
independientemente del crecimiento de la plataforma AURA.

Las reglas aquí descritas forman parte de la arquitectura del
dominio y deberán respetarse en todas las implementaciones.

---

# Principios

El Aggregate Citizen debe cumplir los siguientes principios:

- baja latencia;
- alta cohesión;
- tamaño reducido;
- consistencia inmediata;
- independencia tecnológica;
- escalabilidad horizontal.

---

# Responsabilidad del Aggregate

El Aggregate debe ejecutar únicamente lógica de negocio.

Nunca debe realizar:

- consultas complejas;
- agregaciones;
- búsquedas;
- cálculos estadísticos;
- operaciones analíticas;
- procesamiento masivo;
- llamadas de red;
- acceso a servicios externos.

Estas responsabilidades pertenecen a otros componentes de la
arquitectura.

---

# Tamaño del Aggregate

El Aggregate debe mantenerse pequeño.

Debe contener únicamente:

- identidad;
- estado;
- reglas de negocio;
- Value Objects;
- entidades internas indispensables.

Nunca debe incorporar colecciones ilimitadas de objetos.

---

# Tiempo de Ejecución

La ejecución de un Command debe ser constante y predecible.

Objetivos conceptuales:

- complejidad O(1) para operaciones internas;
- evitar recorridos completos de colecciones;
- evitar algoritmos de crecimiento cuadrático o exponencial.

---

# Persistencia

Cada Command debe producir como máximo:

- una carga del Aggregate;
- una persistencia del Aggregate.

No deben existir múltiples escrituras parciales durante una
misma operación.

---

# Transacciones

Las transacciones deben ser:

- cortas;
- atómicas;
- consistentes;
- aisladas;
- duraderas.

El Aggregate nunca debe mantener transacciones abiertas
mientras espera respuestas externas.

---

# Consultas

El Aggregate nunca responde consultas complejas.

Ejemplos de consultas prohibidas:

- ciudadanos por comuna;
- ciudadanos activos;
- ciudadanos por organización;
- ciudadanos con mayor participación;
- estadísticas territoriales.

Todas ellas pertenecen a los Read Models.

---

# Eventos

Los Domain Events deben generarse durante la ejecución del
Aggregate.

Su publicación debe realizarse después del commit mediante el
Outbox Pattern o un mecanismo equivalente.

El Aggregate nunca espera la confirmación de los consumidores.

---

# Consistencia

La consistencia inmediata se limita al Aggregate Citizen.

Las operaciones que involucren múltiples Aggregates utilizarán
consistencia eventual mediante eventos.

Esto evita bloqueos y mejora la escalabilidad.

---

# Concurrencia

El Aggregate utiliza:

```text
Optimistic Concurrency Control
```

No se permiten bloqueos pesimistas como estrategia principal.

Los conflictos deben resolverse mediante control de versión.

---

# Read Models

Las consultas de alta frecuencia deben dirigirse siempre a los
Read Models.

Nunca deben reconstruirse Aggregates para responder búsquedas o
listados.

---

# Índices

Los índices pertenecen exclusivamente a la infraestructura.

El dominio nunca define:

- índices SQL;
- índices NoSQL;
- motores de búsqueda;
- estructuras de almacenamiento.

---

# Caché

El Aggregate no depende de mecanismos de caché.

Si se implementan estrategias de caché, deberán ubicarse en la
capa de infraestructura o en los servicios de aplicación.

La consistencia del dominio no puede depender del caché.

---

# Escalabilidad

El diseño debe permitir:

- múltiples instancias de aplicación;
- procesamiento distribuido;
- particionamiento por Aggregate;
- procesamiento paralelo de eventos;
- escalado horizontal.

No debe existir estado compartido en memoria entre instancias.

---

# Consumo de Memoria

Durante la ejecución de un Command, el Aggregate debe mantener
únicamente el estado necesario para completar la operación.

No debe cargar información perteneciente a otros Aggregates.

---

# Integración

Las integraciones con:

- FIWARE;
- plataformas municipales;
- servicios de identidad;
- motores de mensajería;
- sistemas analíticos;

deben realizarse fuera del Aggregate mediante Application
Services o Infrastructure Services.

---

# Métricas Recomendadas

Las implementaciones deberán monitorear, entre otras, las
siguientes métricas:

- tiempo promedio de ejecución por Command;
- tiempo de persistencia;
- tasa de conflictos de concurrencia;
- tiempo de publicación de eventos;
- throughput de Commands;
- latencia de reconstrucción de Read Models;
- utilización de memoria.

Estas métricas no forman parte del dominio, pero permiten
verificar el cumplimiento de las reglas arquitectónicas.

---

# Antipatrones

Las siguientes prácticas están prohibidas dentro del Aggregate:

- consultas SQL;
- acceso directo a MongoDB;
- llamadas HTTP;
- llamadas gRPC;
- acceso a Redis;
- publicación directa en Kafka, RabbitMQ o MQTT;
- lectura de archivos;
- operaciones de entrada/salida;
- lógica de presentación;
- lógica de autenticación.

---

# Compatibilidad con CQRS

El lado de escritura permanece optimizado para operaciones
transaccionales.

El lado de lectura absorbe toda la carga de consultas,
estadísticas y búsquedas masivas.

---

# Compatibilidad con Event Sourcing

En implementaciones Event Sourcing:

- la reconstrucción del Aggregate debe depender únicamente de
  los eventos asociados a su **CitizenId**;
- el historial de otros Aggregates nunca debe cargarse durante
  la ejecución.

---

# Principios Arquitectónicos

Estas reglas siguen los principios de:

- Domain-Driven Design (DDD);
- CQRS;
- Event Sourcing;
- Clean Architecture;
- SOLID;
- Hexagonal Architecture;
- High Cohesion;
- Low Coupling.

---

# Definición de Éxito

El Aggregate **Citizen** mantiene un rendimiento constante,
escalable y desacoplado al limitar su responsabilidad a la
ejecución de reglas de negocio. Las consultas, integraciones,
proyecciones y operaciones distribuidas se delegan a los
componentes especializados de la arquitectura, permitiendo que
AURA evolucione hacia una plataforma de alta disponibilidad y
capaz de operar a escala municipal, regional y nacional.