# AURA Core — Estado actual y plan para retomar el desarrollo

Audiencia: persona trainee o integrante que se incorpora al proyecto

Estado de referencia: primer corte vertical de Application completado y publicado

Baseline normativo: `domain-model-v1.0.0`

Baseline operativo actual: `6bb9a90 feat(proposal): implement Proposal VS-001`

## 1. Qué es AURA Core

AURA Core es el núcleo conceptual y ejecutable progresivo de Smart Community Platform.

Modela procesos de:

* organizaciones comunitarias;
* ciudadanía;
* membresías;
* roles;
* territorio;
* asambleas;
* propuestas;
* participación;
* votaciones;
* documentos;
* notificaciones;
* auditoría;
* integración.

El Domain Model se encuentra consolidado y constituye la autoridad conceptual del sistema.

El repositorio ha iniciado además la materialización de la capa Application mediante cortes verticales controlados.

El primer corte vertical implementado corresponde a:

```text
DOMAIN-007 Proposal
VS-001
CreateProposal + SubmitProposal
```

AURA Core todavía no constituye una aplicación productiva completa.

Actualmente no se presupone:

* API HTTP productiva;
* persistencia concreta;
* ORM;
* base de datos definitiva;
* broker de mensajería;
* Transactional Outbox;
* despliegue productivo;
* integración concreta con FIWARE;
* runtime distribuido completo.

La estrategia sigue siendo avanzar desde el dominio consolidado hacia capacidades ejecutables pequeñas, verificables y arquitectónicamente controladas.

---

## 2. Estado actual comprobado

| Área                              | Estado                              | Evidencia                                   |
| --------------------------------- | ----------------------------------- | ------------------------------------------- |
| Visión de producto                | Definida como hipótesis estratégica | `Smart-Community-Platform.md`               |
| Domain Model v1                   | Cerrado y etiquetado                | `DOMAIN-MODEL-CLOSURE.md`                   |
| Baseline normativo                | Preservado                          | `domain-model-v1.0.0`                       |
| Bounded Contexts                  | 13 definidos                        | documentos CORE y DOMAIN                    |
| Aggregates                        | 13 definidos y documentados         | documentación normativa                     |
| Commands y Domain Events          | Trazados                            | catálogo y documentos de Aggregate          |
| Integration Events                | Inventariados                       | contratos públicos existentes               |
| Relaciones y consistencia         | Consolidadas                        | documentos CROSS-001 a CROSS-004            |
| Hallazgos TA-001, TA-002 y TA-008 | Resueltos                           | documentos TA y artefactos normalizados     |
| Diagramas transversales           | Completados                         | archivos `.drawio` correspondientes         |
| Validación automatizada           | Operativa                           | Pytest, Ruff y MyPy                         |
| Application                       | Iniciada                            | Proposal VS-001 implementado                |
| Primer corte vertical             | Completado                          | DOMAIN-007 Proposal VS-001                  |
| API concreta                      | No iniciada                         | fuera del alcance actual                    |
| Persistencia concreta             | No iniciada                         | puertos definidos, adapters pendientes      |
| Infraestructura productiva        | No iniciada                         | pendiente de ADR y necesidad de caso de uso |
| DOMAIN-008 Participation          | Siguiente Aggregate oficial         | descubrimiento pendiente                    |

La rama `main` contiene el núcleo activo de AURA Core.

El experimento Security IoT se mantiene separado del desarrollo activo de AURA Core y no altera su modelo normativo.

La consolidación transversal resolvió TA-001, TA-002 y TA-008 mediante decisiones explícitas de dominio.

Las normalizaciones resultantes se aplicaron sobre los artefactos afectados sin reescribir el baseline normativo:

```text
domain-model-v1.0.0
```

El primer corte vertical ejecutable fue posteriormente materializado sobre DOMAIN-007 Proposal y publicado mediante:

```text
6bb9a90 feat(proposal): implement Proposal VS-001
```

---

## 3. Orden canónico de Aggregates

El orden oficial de Aggregates de AURA Core es:

```text
DOMAIN-001 Organization
DOMAIN-002 Citizen
DOMAIN-003 Membership
DOMAIN-004 Role
DOMAIN-005 Territory
DOMAIN-006 Assembly
DOMAIN-007 Proposal
DOMAIN-008 Participation
DOMAIN-009 Voting
DOMAIN-010 Document
DOMAIN-011 Notification
DOMAIN-012 Audit
DOMAIN-013 Integration
```

No existe `Committee` como Aggregate dentro de esta secuencia.

Este orden debe respetarse en documentación, planificación y evolución del modelo.

---

## 4. Conceptos mínimos para comenzar

* **Bounded Context:** límite dentro del cual los términos mantienen un significado estable.

* **Aggregate:** conjunto de objetos de dominio que se modifica como una unidad de consistencia.

* **Aggregate Root:** único punto autorizado para modificar el Aggregate desde el exterior.

* **Command:** intención explícita de ejecutar una acción.

* **Domain Event:** hecho interno que ya ocurrió dentro del contexto productor.

* **Integration Event:** contrato público y versionado destinado a comunicar un hecho fuera del contexto productor.

* **Application Service:** coordinador de un caso de uso. Orquesta autorización, Aggregate, repositorios, puertos, eventos y DTOs sin duplicar reglas del dominio.

* **Input Port:** contrato mediante el cual Application expone un caso de uso.

* **Output Port:** contrato mediante el cual Application expresa una dependencia externa.

* **DTO de Application:** representación de salida que evita exponer directamente el Aggregate.

* **Consistencia inmediata:** reglas garantizadas dentro de un único límite transaccional.

* **Consistencia eventual:** coordinación posterior entre Aggregates, contextos o sistemas externos.

Regla esencial:

```text
Aggregate
    !=
NGSI-LD Entity
```

También:

```text
Domain Event
    !=
Integration Event
    !=
API Contract
```

Y:

```text
ActorId
    !=
CorrelationId
    !=
CausationId
```

Nunca se debe convertir automáticamente cualquier Domain Event en Integration Event.

Tampoco debe consumirse directamente un evento interno de otro contexto como sustituto de un contrato público.

---

## 5. Relación canónica AURA Core / FIWARE

AURA Core constituye la autoridad del dominio cívico.

FIWARE constituye infraestructura de interoperabilidad contextual.

La relación aprobada es:

```text
AURA Core
    |
    | Domain Event
    v
Commit
    |
    | Integration Event
    v
DOMAIN-013 Integration
    |
    | Anti-Corruption Layer / Adapter
    v
NGSI-LD
    |
    v
FIWARE Context Broker
```

Reglas:

```text
Aggregate != NGSI-LD Entity
```

```text
Domain Event != Integration Event != NGSI-LD Notification
```

AURA Core no debe depender directamente de:

* Orion;
* Orion-LD;
* FIWARE;
* protocolos concretos de Context Broker;
* serialización NGSI-LD.

DOMAIN-013 Integration constituye la frontera arquitectónica prevista para estos contratos.

---

## 6. Qué se puede cambiar y qué requiere aprobación

### Trabajo permitido para una persona trainee

* mejorar documentación no normativa;
* ampliar pruebas sin alterar semántica normativa;
* ampliar validadores sin modificar reglas de dominio;
* preparar ejemplos de uso para revisión;
* implementar tareas de Application ya especificadas y aprobadas;
* implementar Infrastructure sólo cuando exista contrato y decisión arquitectónica previa;
* registrar contradicciones encontradas con evidencia concreta;
* trabajar dentro de un Vertical Slice ya aprobado;
* corregir divergencias detectadas por Quality Gates cuando la autoridad canónica esté clara.

### Trabajo que requiere revisión previa

* modificar documentación normativa de Aggregates;
* cambiar Commands;
* cambiar Domain Events;
* cambiar Integration Events;
* cambiar invariantes;
* cambiar permisos;
* cambiar ownership;
* cambiar límites de consistencia;
* cambiar State Machines;
* modificar resoluciones aprobadas de TA-001, TA-002 o TA-008;
* declarar nuevos consumidores;
* crear nuevos contratos públicos;
* introducir nuevos Aggregates;
* adoptar frameworks;
* adoptar bases de datos;
* adoptar brokers;
* adoptar proveedores;
* cambiar arquitectura de integración;
* iniciar un nuevo corte vertical sin alcance y aceptación aprobados.

Regla de normalización:

```text
Si existe una divergencia:

1. determinar la autoridad canónica;
2. detener la creación de artefactos nuevos;
3. normalizar exclusivamente los artefactos divergentes;
4. volver a ejecutar Quality Gates;
5. continuar sólo cuando todos estén en verde.
```

---

## 7. Preparación del entorno

Requisitos actuales:

* Python 3.12;
* entorno virtual;
* dependencias del proyecto instaladas;
* Git;
* Ruff;
* MyPy;
* Pytest.

Activación habitual:

```bash
source .venv/bin/activate
```

Validación mínima:

```bash
ruff check src tests
mypy src
python3 -m pytest -q
```

Baseline comprobado después de Proposal VS-001:

```text
Ruff:
All checks passed!

MyPy:
Success: no issues found in 54 source files

Pytest:
202 passed
```

El tiempo de ejecución de Pytest puede variar entre entornos y no forma parte del contrato.

Si el resultado difiere:

1. registrar el comando ejecutado;
2. conservar la salida completa;
3. identificar exactamente el artefacto divergente;
4. no alterar el Domain Model para hacer pasar una prueba;
5. corregir únicamente la divergencia demostrada.

---

## 8. Quality Gates obligatorios

Todo Vertical Slice debe superar, como mínimo:

```bash
ruff check src tests
mypy src
python3 -m pytest -q
```

Orden obligatorio:

```text
Ruff
  ↓
MyPy
  ↓
Pytest
```

No se debe avanzar al gate siguiente mientras el anterior esté en rojo.

No se debe crear un commit de cierre hasta que los tres estén en verde.

No se debe publicar un commit cuyo Vertical Slice conocido mantenga divergencias abiertas.

Estado de Proposal VS-001 al cierre:

```text
Ruff   PASS
MyPy   PASS
Pytest PASS — 202 tests
```

---

## 9. Ruta de lectura recomendada

1. `README.md`
   Alcance real del repositorio.

2. `Smart-Community-Platform.md`
   Visión e hipótesis de producto.

3. `DOMAIN-MODEL-CLOSURE.md`
   Decisiones cerradas del baseline.

4. `docs/architecture/domain/core/001-domain-constitution.md`
   Reglas constitucionales del dominio.

5. `docs/architecture/domain/core/CORE-002-Bounded-Context-Map.md`
   Mapa normativo de contextos.

6. `docs/architecture/domain/cross-context/CROSS-001-Transversal-Audit.md`
   Auditoría, hallazgos y estado de resolución.

7. `docs/architecture/domain/cross-context/CROSS-002-Aggregate-Relationship-Map.md`
   Relaciones y ownership.

8. `docs/architecture/domain/cross-context/CROSS-003-Consistency-Boundary-Map.md`
   Fronteras de consistencia.

9. `docs/architecture/domain/cross-context/CROSS-004-Cross-Domain-Contracts.md`
   Contratos públicos.

10. `docs/architecture/domain/events/event-catalog.md`
    Trazabilidad de eventos.

11. `docs/architecture/domain/cross-context/TA-001-AssemblyPublished-Origin.md`
    Resolución del origen semántico de `AssemblyPublished`.

12. `docs/architecture/domain/cross-context/TA-002-ProposalUpdatedForIntegration-Origin.md`
    Resolución del origen de `ProposalUpdatedForIntegration`.

13. `docs/architecture/domain/cross-context/TA-008-AssemblyModalityChanged-Naming.md`
    Normalización canónica de `AssemblyModalityChanged`.

14. Documentación completa de DOMAIN-007 Proposal.

15. Implementación de:

```text
src/arada_core/proposal/
tests/proposal/
```

16. Documentación completa de DOMAIN-008 Participation antes de iniciar su implementación.

Después de esta lectura se estudia exclusivamente el Aggregate relacionado con el siguiente caso de uso aprobado.

---

## 10. Arquitectura física vigente del primer slice

Proposal materializa la siguiente separación:

```text
src/arada_core/proposal/
├── __init__.py
├── domain/
│   ├── __init__.py
│   ├── aggregates/
│   ├── events/
│   ├── repositories/
│   └── value_objects/
├── application/
│   ├── __init__.py
│   ├── commands/
│   ├── dto/
│   ├── integration_events/
│   ├── mappers/
│   ├── ports/
│   └── services/
├── infrastructure/
│   └── __init__.py
└── interfaces/
    └── __init__.py
```

Tests:

```text
tests/proposal/
├── __init__.py
├── domain/
│   └── __init__.py
└── application/
    └── __init__.py
```

Esta estructura no debe generalizarse mecánicamente a otros Aggregates sin comprobar primero si el siguiente Vertical Slice requiere exactamente las mismas piezas.

---

## 11. DOMAIN-007 Proposal — cierre del primer Vertical Slice

Estado:

```text
Completed
```

Vertical Slice:

```text
DOMAIN-007 Proposal
VS-001
```

Capacidades incluidas:

```text
CreateProposal
SubmitProposal
```

State Machine cubierta:

```text
Nonexistent
    |
    | CreateProposal
    v
Draft
    |
    | SubmitProposal
    v
Submitted
```

Commands:

```text
CreateProposal
SubmitProposal
```

Domain Events:

```text
ProposalCreated
ProposalSubmitted
```

Integration Events:

```text
ProposalCreatedForIntegration
ProposalSubmittedForIntegration
```

Permisos:

```text
proposal:create
proposal:submit
```

Reglas relevantes:

* `OrganizationId` es obligatorio;
* el proposer puede referenciar Citizen o Membership;
* `TerritoryId` es contextual y opcional;
* `AssemblyId` es contextual y opcional;
* `ProposalName` es el término canónico;
* `ProposalVersion` inicia en 1;
* una mutación exitosa incrementa la versión exactamente una vez;
* Submit sólo permite `Draft -> Submitted`;
* el Aggregate controla la transición;
* Application no modifica `ProposalStatus` directamente;
* Application no modifica `ProposalVersion` directamente;
* persistencia utiliza control optimista de versión;
* los eventos se publican sólo después de persistencia exitosa dentro del orden lógico disponible en VS-001.

Contrato temporal:

```text
PublishedAt >= OccurredAt
```

Contrato de identidad de integración:

```text
EventId != AggregateId
```

Contrato de trazabilidad:

```text
ActorId
    !=
CorrelationId
    !=
CausationId
```

Commit de cierre:

```text
6bb9a90 feat(proposal): implement Proposal VS-001
```

Publicación:

```text
main -> origin/main
```

Quality Gates de cierre:

```text
Ruff   PASS
MyPy   PASS
Pytest PASS — 202 passed
```

---

## 12. Lecciones de ingeniería obtenidas en Proposal VS-001

### 12.1 El modelo normativo sigue siendo la autoridad

Los tests y el código de Application deben adaptarse al contrato canónico.

No debe modificarse una firma normativa sólo porque un stub de tests haya quedado desactualizado.

### 12.2 Las referencias pueden requerir contexto organizacional

La validación de proposer y assembly requiere contexto de `OrganizationId`.

Por ello:

```text
validate_proposer(
    ProposerReference,
    OrganizationId,
)
```

y:

```text
validate_assembly(
    AssemblyId,
    OrganizationId,
)
```

son contratos contextuales.

### 12.3 Los tests no deben depender de fechas históricas incompatibles con el reloj del dominio

Cuando `OccurredAt` es generado en tiempo de ejecución, un `PublishedAt` fijo anterior puede invalidar artificialmente el escenario.

Debe respetarse siempre:

```text
PublishedAt >= OccurredAt
```

### 12.4 `__init__.py` es el artefacto canónico de paquete Python

No debe utilizarse:

```text
init.py
```

como sustituto.

Debe utilizarse:

```text
__init__.py
```

### 12.5 Los Quality Gates son parte del diseño

Ruff, MyPy y Pytest no son pasos administrativos finales.

Actúan como mecanismos de descubrimiento de divergencias entre:

* contratos;
* tipos;
* tests;
* implementación;
* estructura física del repositorio.

---

## 13. Estado del plan por fases

### Fase 0 — Onboarding y baseline reproducible

Estado:

```text
Completed
```

Objetivo:

comprender los límites del proyecto y reproducir localmente un baseline válido.

Resultado actual:

* entorno reproducible;
* Quality Gates definidos;
* Domain Model validado;
* reglas de trabajo consolidadas.

---

### Fase 1 — Consolidación semántica transversal

Estado:

```text
Completed
```

Trabajo completado:

* resolución explícita de TA-001;
* resolución explícita de TA-002;
* resolución explícita de TA-008;
* normalización de artefactos normativos afectados;
* actualización de catálogos;
* actualización de contratos transversales;
* verificación física de coherencia;
* preservación del baseline `domain-model-v1.0.0`.

Resultado:

```text
TA-001 = Resolved
TA-002 = Resolved
TA-008 = Resolved
Transversal Closure = Approved
```

El baseline normativo permanece inmutable.

Las resoluciones posteriores no reescriben el tag:

```text
domain-model-v1.0.0
```

---

### Fase 2 — Descubrimiento del primer corte vertical

Estado:

```text
Completed for DOMAIN-007 Proposal
```

Resultado:

```text
Proposal VS-001
CreateProposal + SubmitProposal
```

El alcance fue suficientemente pequeño para preservar:

* un Aggregate por commit lógico;
* reglas dentro del Aggregate;
* Application independiente de Infrastructure;
* contratos públicos explícitos;
* ausencia de dependencia FIWARE dentro de Domain.

---

### Fase 3 — Diseño de Application

Estado:

```text
Started
```

Materializado actualmente para Proposal VS-001.

Se implementaron:

* Commands;
* Application Services;
* DTO;
* input/output contracts;
* Repository contract;
* autorización;
* validación externa mediante port;
* Domain Event Publishers;
* Integration Event Publishers;
* Integration Event Mapper;
* Integration Events;
* pruebas unitarias.

Criterio arquitectónico alcanzado:

```text
El caso de uso puede probarse mediante puertos
sin API, framework ni infraestructura concreta.
```

Esta fase continúa incrementalmente para cada Vertical Slice futuro.

---

### Fase 4 — Decisiones de arquitectura técnica

Estado:

```text
Pending
```

No se debe iniciar globalmente por anticipación.

Las decisiones deben aparecer cuando un caso de uso concreto las necesite.

Cada decisión relevante debe registrarse mediante ADR e incluir:

* contexto;
* alternativas;
* decisión;
* consecuencias;
* seguridad;
* operación;
* observabilidad;
* reversibilidad.

Áreas futuras:

* transporte de entrada;
* identidad;
* autenticación;
* persistencia;
* transacciones;
* publicación confiable;
* configuración;
* observabilidad;
* despliegue.

No se adopta una tecnología por haber aparecido en experimentos anteriores.

---

### Fase 5 — Implementación de cortes end-to-end

Estado:

```text
Pending
```

Orden recomendado cuando exista un Vertical Slice aprobado que requiera infraestructura:

1. modelo ejecutable del Aggregate;
2. caso de uso;
3. puertos;
4. adapter de persistencia;
5. adapter de entrada;
6. publicación de contratos cuando corresponda;
7. pruebas unitarias;
8. pruebas de integración;
9. pruebas de aceptación;
10. documentación operativa.

Criterio de salida:

* comportamiento aceptado;
* Quality Gates verdes;
* decisiones documentadas;
* ninguna dependencia de Infrastructure dentro de Domain.

---

### Fase 6 — Operación y siguiente incremento

Estado:

```text
Pending
```

Objetivo futuro:

observar el comportamiento real de capacidades end-to-end antes de ampliar la plataforma.

Trabajo previsto:

* métricas funcionales;
* métricas técnicas;
* recuperación;
* idempotencia;
* fallos esperados;
* seguridad;
* privacidad;
* feedback;
* decisión de iterar, mantener, retirar o ampliar.

---

## 14. Próximo Aggregate oficial — DOMAIN-008 Participation

El siguiente Aggregate en el orden canónico es:

```text
DOMAIN-008 Participation
```

Estado:

```text
Discovery
```

No se debe comenzar creando código.

Primero debe estudiarse la documentación normativa completa de Participation.

El objetivo inicial es establecer qué significa `Participation` dentro de AURA y delimitarlo respecto de:

```text
DOMAIN-003 Membership
DOMAIN-006 Assembly
DOMAIN-007 Proposal
DOMAIN-009 Voting
```

Especial atención debe prestarse a evitar solapamientos semánticos.

Antes de implementar Participation deberán quedar explícitos:

* Aggregate Root;
* identidad;
* Value Objects;
* invariantes;
* estados;
* transiciones;
* Commands;
* Domain Events;
* permisos;
* Repository contract;
* referencias externas;
* Integration Events;
* límites de consistencia;
* alcance del VS-001;
* exclusiones;
* escenarios de aceptación.

No debe asumirse que la arquitectura física de Proposal se replica sin cambios.

---

## 15. Backlog inmediato recomendado

### Prioridad 1 — Cierre operativo de Proposal

* preservar evidencia del cierre;
* mantener commit `6bb9a90` como referencia;
* no reabrir Proposal VS-001 salvo divergencia demostrada;
* registrar futuras mejoras como trabajo posterior y no como correcciones retroactivas sin necesidad.

### Prioridad 2 — Resolver artefactos operacionales del repositorio

Revisar individualmente:

```text
STATUS-AND-RESTART-PLAN.md
verify-domain-closure.sh
commit-domain-closure.sh
```

Cada uno debe clasificarse como:

```text
Keep
Normalize
Remove
```

No deben agregarse automáticamente al repositorio sin revisión.

### Prioridad 3 — Descubrimiento de DOMAIN-008 Participation

* leer documentación raíz y A–P;
* construir mapa semántico;
* identificar términos canónicos;
* revisar Commands existentes;
* revisar Domain Events existentes;
* revisar Integration Events existentes;
* verificar relaciones CROSS;
* verificar consistency boundaries;
* identificar divergencias antes de diseñar Application.

### Prioridad 4 — Definir Participation VS-001

Sólo después del análisis normativo:

* actor;
* problema;
* resultado;
* Command inicial;
* comportamiento esperado;
* Aggregate involucrado;
* eventos;
* permisos;
* referencias;
* contratos;
* exclusiones;
* escenarios de aceptación.

---

## 16. Definition of Done general

Una tarea se considera terminada cuando:

* su alcance está explícito;
* sus criterios de aceptación están explícitos;
* no altera semántica normativa sin aprobación;
* respeta las resoluciones transversales vigentes;
* mantiene el término canónico;
* mantiene un Aggregate como unidad de consistencia;
* evita transacciones distribuidas implícitas;
* incluye pruebas proporcionales al riesgo;
* Ruff está en verde;
* MyPy está en verde;
* Pytest está en verde;
* cualquier validador adicional requerido está en verde;
* la documentación afectada está actualizada;
* Domain no depende de Application;
* Domain no depende de Infrastructure;
* AURA Core no depende directamente de FIWARE;
* los contratos públicos se mantienen explícitos;
* el commit es pequeño, temático y revisable;
* el staging fue inspeccionado antes del commit;
* el árbol de trabajo queda bajo control.

Para cierre de Vertical Slice:

```text
Ruff PASS
    +
MyPy PASS
    +
Pytest PASS
    +
Staging reviewed
    +
Commit created
    +
Push verified
```

---

## 17. Protocolo de trabajo ante divergencias

Cuando un gate detecta una discrepancia:

```text
STOP
```

No se continúa creando artefactos.

Procedimiento:

```text
1. observar el fallo real;
2. identificar el contrato implicado;
3. determinar la autoridad canónica;
4. aislar los artefactos divergentes;
5. normalizar sólo esos artefactos;
6. ejecutar nuevamente los gates;
7. continuar únicamente cuando estén en verde.
```

No se deben usar correcciones masivas sin comprender primero el alcance.

Una herramienta automática puede aplicarse cuando:

* el error es puramente mecánico;
* el alcance está claramente identificado;
* la herramienta no cambia semántica;
* posteriormente se vuelven a ejecutar todos los Quality Gates.

Ejemplo:

```bash
ruff check <archivos-específicos> --fix
```

para normalización de imports.

---

## 18. Protocolo Git para cierre de un Vertical Slice

Antes del staging:

```bash
git status
```

Agregar únicamente el Vertical Slice aprobado:

```bash
git add <src-del-slice> <tests-del-slice>
```

Revisar:

```bash
git status
```

No deben incluirse accidentalmente:

* archivos temporales;
* logs;
* resultados de pruebas;
* scripts no revisados;
* documentación operacional fuera de alcance;
* experimentos.

Ejecutar Quality Gates finales:

```bash
ruff check src tests
mypy src
python3 -m pytest -q
```

Sólo después:

```bash
git commit -m "<mensaje-temático>"
```

Verificar:

```bash
git status
git log -1 --oneline
```

Publicar:

```bash
git push origin main
```

Verificación esperada:

```text
HEAD -> main
origin/main
```

apuntando al mismo commit.

---

## 19. Estado comprobado de Git después de Proposal VS-001

Referencia publicada:

```text
6bb9a90 (HEAD -> main, origin/main, origin/HEAD)
feat(proposal): implement Proposal VS-001
```

Estado de Proposal:

```text
Committed
Pushed
Validated
Closed
```

Artefactos operacionales todavía sujetos a revisión:

```text
STATUS-AND-RESTART-PLAN.md
commit-domain-closure.sh
verify-domain-closure.sh
```

Estos artefactos no forman parte del commit de Proposal VS-001.

---

## 20. Resultado actual del plan

AURA Core ya no se encuentra únicamente en estado de modelo conceptual consolidado.

El proyecto alcanzó el siguiente nivel:

```text
Normative Domain Model
        |
        v
Transversal Consolidation
        |
        v
Approved Vertical Slice
        |
        v
Executable Domain
        |
        v
Application Services + Ports
        |
        v
Integration Contracts
        |
        v
Automated Quality Gates
```

DOMAIN-007 Proposal demostró que el modelo puede materializarse en código manteniendo:

* DDD;
* separación Domain/Application;
* Aggregate como consistency boundary;
* optimistic concurrency;
* contratos de integración explícitos;
* independencia de infraestructura;
* independencia directa respecto de FIWARE;
* pruebas automatizadas;
* tipado estático;
* linting;
* trazabilidad de cierre mediante Git.

El siguiente avance no consiste en añadir infraestructura global ni generalizar prematuramente la arquitectura.

Corresponde abrir:

```text
DOMAIN-008 Participation
```

mediante descubrimiento normativo controlado.

La secuencia recomendada es:

```text
Read
  ↓
Audit
  ↓
Determine canonical semantics
  ↓
Resolve divergences
  ↓
Define VS-001
  ↓
Approve
  ↓
Implement
  ↓
Quality Gates
  ↓
Commit
  ↓
Push
```

El Domain Model consolidado continúa siendo la autoridad conceptual durante toda la evolución de AURA Core.
