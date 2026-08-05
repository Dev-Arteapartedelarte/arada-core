# DOMAIN-001O — Security Model

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
- DOMAIN-001F-Permissions.md
- DOMAIN-001G-Repository-Contract.md
- DOMAIN-001J-Consistency-Boundary.md
- DOMAIN-001K-Integration-Events.md
- CORE-006-Domain-Invariants.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Definir el modelo oficial de seguridad del Aggregate
**Organization**.

Este documento establece los principios, responsabilidades
y restricciones que garantizan la protección de la lógica
de negocio, la integridad del estado y la trazabilidad de
las operaciones, independientemente de la tecnología de
autenticación o autorización utilizada por la plataforma.

El dominio protege las reglas de negocio; la identidad y
la infraestructura de seguridad pertenecen a otras capas.

---

# Principios

El modelo de seguridad del dominio se basa en los
siguientes principios.

- Defensa en profundidad.
- Menor privilegio (Least Privilege).
- Seguridad por diseño (Secure by Design).
- Inmutabilidad de los eventos.
- Trazabilidad completa.
- Separación de responsabilidades.
- Independencia tecnológica.

---

# Filosofía

La autenticación identifica quién ejecuta una acción.

La autorización determina si puede ejecutarla.

El Aggregate únicamente valida si la operación solicitada
es coherente con las reglas del dominio.

```text
Usuario

↓

Identity Provider

↓

Application Service

↓

Authorization Policy

↓

Organization Aggregate

↓

Repository
```

El Aggregate nunca autentica usuarios.

---

# SM-001

## Responsabilidades del Aggregate

El Aggregate debe garantizar:

- cumplimiento de invariantes;
- validez de transiciones de estado;
- protección contra modificaciones inválidas;
- emisión consistente de Domain Events;
- consistencia interna del estado.

---

# SM-002

## Responsabilidades Externas

Las siguientes responsabilidades no pertenecen al dominio.

- autenticación;
- gestión de contraseñas;
- OAuth2;
- OpenID Connect;
- JWT;
- MFA;
- sesiones;
- certificados;
- criptografía de transporte.

Estas funciones pertenecen a Infrastructure.

---

# SM-003

## Modelo de Autorización

La autorización se evalúa antes de invocar el Aggregate.

Ejemplo.

```text
ApproveOrganization

↓

Authorization Policy

↓

Permitido

↓

Organization.approve()
```

Si la autorización falla, el Aggregate no es invocado.

---

# SM-004

## Protección de Invariantes

Ninguna operación puede vulnerar las invariantes del
Aggregate.

Ejemplos.

- aprobar sin representante;
- cambiar a un estado inválido;
- eliminar una organización activa;
- utilizar un identificador inconsistente.

Toda violación produce un error de dominio.

---

# SM-005

## Integridad del Estado

Cada cambio debe cumplir simultáneamente:

- estado válido;
- versión correcta;
- transición permitida;
- reglas de negocio satisfechas.

No existen estados intermedios visibles.

---

# SM-006

## Versionado Optimista

Toda modificación utiliza control optimista mediante el
campo Version.

```text
Version 8

↓

Modificar

↓

Version 9
```

Si la versión almacenada no coincide, se genera un
conflicto de concurrencia.

---

# SM-007

## Protección contra Repetición

Los Commands deben ser idempotentes cuando la operación
así lo requiera.

Ejemplo.

```text
ApproveOrganization
```

Ejecutarlo dos veces no puede producir dos aprobaciones.

---

# SM-008

## Domain Events

Los Domain Events representan evidencia del cambio.

Una vez emitidos:

- no se modifican;
- no se eliminan;
- no se reutilizan.

Son inmutables.

---

# SM-009

## Integration Events

Los Integration Events únicamente se publican después de
una persistencia exitosa.

```text
Aggregate

↓

Commit

↓

Integration Event
```

Nunca antes.

---

# SM-010

## Auditoría

Cada operación relevante debe poder reconstruirse a
partir de:

- Command ejecutado;
- Domain Event generado;
- versión del Aggregate;
- instante de ocurrencia.

La auditoría se implementa fuera del Aggregate.

---

# SM-011

## Protección de Identificadores

Los identificadores del dominio son inmutables.

Ejemplos.

```text
OrganizationId

RepresentativeId

TerritoryId
```

Nunca cambian durante el ciclo de vida del Aggregate.

---

# SM-012

## Protección de Referencias

El Aggregate almacena únicamente referencias a otros
Aggregates.

Nunca mantiene copias completas de entidades externas.

---

# SM-013

## Consistencia Transaccional

Todas las modificaciones del Aggregate ocurren dentro de
una única transacción lógica.

No existen cambios parciales.

---

# SM-014

## Separación de Secretos

El Aggregate nunca almacena:

- contraseñas;
- claves privadas;
- tokens de acceso;
- secretos criptográficos;
- credenciales de servicios.

Estos datos pertenecen a componentes especializados.

---

# SM-015

## Integridad de Integraciones

Los sistemas externos nunca modifican directamente el
Aggregate.

Toda modificación ocurre mediante:

- Commands;
- Application Services;
- Repositories.

---

# SM-016

## Seguridad de Extensiones

Las extensiones del dominio deben respetar todas las
invariantes existentes.

No pueden modificar:

- State Machine;
- reglas de negocio;
- contratos públicos;
- consistencia del Aggregate.

---

# SM-017

## Aislamiento

El Aggregate nunca comparte estado mutable con otros
Aggregates.

Cada Aggregate constituye un límite de consistencia.

---

# SM-018

## Observabilidad

Los mecanismos de observabilidad deben implementarse sin
alterar el comportamiento del dominio.

Ejemplos.

- métricas;
- tracing;
- logging;
- auditoría;
- monitoreo.

---

# Tabla de Responsabilidades

| Componente | Responsabilidad |
|------------|-----------------|
| Identity Provider | Autenticación |
| Authorization Policy | Permisos |
| Application Service | Orquestación |
| Organization Aggregate | Reglas de negocio |
| Repository | Persistencia |
| Event Bus | Distribución de eventos |
| Audit Service | Evidencia histórica |

---

# Amenazas Mitigadas

| Riesgo | Mitigación |
|--------|------------|
| Cambio de estado inválido | State Machine |
| Corrupción del Aggregate | Invariantes |
| Actualización concurrente | Versionado optimista |
| Modificación parcial | Consistencia transaccional |
| Repetición de Commands | Idempotencia |
| Dependencia de infraestructura | Arquitectura por capas |
| Integraciones inseguras | Integration Events |
| Acceso directo al dominio | Application Services |

---

# Reglas

## REG-001

El Aggregate nunca autentica usuarios.

---

## REG-002

Toda autorización ocurre antes del dominio.

---

## REG-003

Las invariantes son la primera línea de defensa del
modelo.

---

## REG-004

Los Domain Events son inmutables.

---

## REG-005

Toda modificación incrementa la versión del Aggregate.

---

## REG-006

Las integraciones nunca modifican directamente el estado
interno.

---

## REG-007

Los secretos nunca forman parte del Aggregate.

---

## REG-008

Cada operación debe ser completamente trazable.

---

## REG-009

El dominio permanece independiente de proveedores de
identidad y tecnologías de seguridad.

---

## REG-010

La seguridad del dominio debe mantenerse incluso cuando
la infraestructura evolucione.

---

# Diagrama Conceptual

```text
                 Usuario
                    │
                    ▼
         Identity Provider
                    │
                    ▼
       Authorization Policy
                    │
                    ▼
        Application Service
                    │
                    ▼
       Organization Aggregate
     ┌─────────────────────────┐
     │ Invariantes             │
     │ State Machine           │
     │ Versionado              │
     │ Domain Events           │
     └─────────────────────────┘
                    │
                    ▼
             Repository
                    │
                    ▼
          Integration Events
                    │
     ┌──────────────┼──────────────┐
     ▼              ▼              ▼
 Municipality    FIWARE      Analytics
```

---

# Definición de Éxito

El Aggregate **Organization** implementa un modelo de seguridad centrado en el dominio, donde la integridad del estado, las invariantes, las transiciones válidas y la trazabilidad de los eventos constituyen la principal barrera de protección. La autenticación, la autorización, la criptografía y los mecanismos de infraestructura permanecen desacoplados, permitiendo que AURA Core evolucione hacia una plataforma distribuida y segura sin comprometer la estabilidad del modelo de negocio.