# AURA Core — Plan de arquitectura y desarrollo

Versión: 2.0

Estado: Consolidación transversal del dominio

Baseline: `domain-model-v1.0.0`

## 1. Propósito

AURA Core es el núcleo conceptual de Smart Community Platform. El baseline
vigente define trece Bounded Contexts y trece Aggregates mediante Domain-Driven
Design y Hexagonal Architecture.

El repositorio no contiene todavía una aplicación funcional, API, persistencia,
mensajería ni infraestructura operativa. La prioridad actual es verificar la
coherencia horizontal del modelo antes de comenzar Application o seleccionar
tecnologías.

## 2. Principios ratificados

```text
Aggregate Boundary = Immediate Consistency Boundary
Cross-Aggregate Collaboration = Eventual Consistency
Domain Event != Integration Event != API Contract
```

- cada Aggregate conserva identidad, ownership, lifecycle y versión propios;
- las referencias cross-Aggregate utilizan identificadores;
- una operación de escritura confirma un único Aggregate;
- los Read Models no poseen autoridad de escritura;
- ningún Bounded Context consume directamente Domain Events ajenos;
- todo contrato público se selecciona y versiona explícitamente;
- Domain y Application permanecen independientes de frameworks y proveedores.

## 3. Estado comprobado

| Capacidad | Estado |
|---|---|
| Trece Aggregates, documento raíz y secuencia A–P | Cerrado |
| Baseline con hashes y tag anotado | Cerrado |
| Constitución y reglas CORE | Cerrado |
| Context Map normativo | Cerrado |
| Auditoría transversal | En consolidación |
| Mapa de relaciones | En consolidación |
| Catálogo transversal de eventos | En consolidación |
| Mapa de consistency boundaries | En consolidación |
| Contratos cross-domain | En consolidación |
| Application, APIs e infraestructura | No iniciado |

## 4. Fase actual — Consolidación transversal

La fase actual produce evidencia derivada del baseline sin redefinir los
Aggregates:

1. auditar cobertura, referencias y contradicciones;
2. registrar relaciones, dirección semántica y ownership;
3. catalogar Commands, Domain Events e Integration Events;
4. identificar límites de consistencia inmediata y eventual;
5. verificar el Context Map contra los trece modelos;
6. consolidar los contratos que pueden cruzar Boundaries;
7. representar los resultados mediante diagramas verificables.

Un hallazgo no autoriza modificar un documento normativo. Toda corrección de
dominio requiere revisión y aprobación explícita.

## 5. Criterio de salida

La consolidación termina cuando:

- los trece Aggregates aparecen en todos los inventarios transversales;
- cada Command y Domain Event oficial posee trazabilidad;
- cada Integration Event tiene contrato explícito o consta como inexistente;
- cada relación cross-Aggregate identifica al dueño de la referencia;
- ninguna relación implica ownership o transacción compartida;
- las contradicciones permanecen registradas y clasificadas;
- el validador y las pruebas documentales finalizan sin errores.

## 6. Fases futuras sujetas a aprobación

### Application

Definirá casos de uso, autorización, puertos de entrada y salida, coordinación
de commits y traducción explícita de contratos. No redefinirá reglas del
dominio.

### Arquitectura técnica

Seleccionará mediante ADR persistencia, API, identidad, publicación, operación
y observabilidad. Ninguna tecnología se considera adoptada antes de esa
decisión.

### Implementación

Se realizará mediante cortes verticales aprobados, comenzando por una capacidad
del baseline y verificando dominio, Application, adapters y aceptación antes de
abrir el siguiente corte.

## 7. Fuera del alcance actual

- implementación de Aggregates;
- endpoints o contratos HTTP;
- persistencia o migraciones;
- broker, outbox o inbox técnicos;
- selección de frameworks;
- FIWARE, IoT o proveedores externos;
- CQRS físico, Event Sourcing o microservicios.

## 8. Gobierno

`domain-model-v1.0.0` permanece como referencia inmutable. Los documentos de
consolidación describen el baseline; no lo sustituyen. Application e
Infrastructure sólo podrán comenzar después del cierre explícito de esta fase.
