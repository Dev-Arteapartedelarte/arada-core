# DOMAIN-010I — Document Versioning

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Document Management

Aggregate:
Document

Documentos Relacionados:

- DOMAIN-010-Aggregate.md
- DOMAIN-010C-Commands.md
- DOMAIN-010D-Domain-Events.md
- DOMAIN-010E-Invariants.md
- DOMAIN-010G-Repository-Contract.md
- DOMAIN-010J-Consistency-Boundary.md
- DOMAIN-010K-Integration-Events.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Definir las reglas oficiales de **Versioning** del Aggregate
**Document**.

Version representa la evolución lógica del Aggregate y permite
detectar modificaciones concurrentes incompatibles.

Toda modificación válida de Document produce una nueva Version.

El Versioning protege la consistencia del Aggregate sin introducir
dependencias con mecanismos concretos de persistencia.

---

# Principios

El Versioning de Document cumple los siguientes principios:

- Version pertenece al Aggregate;
- Version representa evolución lógica;
- toda modificación válida incrementa Version;
- una operación rechazada no incrementa Version;
- una operación de lectura no incrementa Version;
- una modificación concurrente incompatible debe ser detectada;
- una escritura nunca debe sobrescribir silenciosamente otra
  modificación confirmada;
- AggregateVersion debe permanecer coherente con los Domain Events;
- el mecanismo concreto de control de concurrencia pertenece a la
  implementación del Repository Contract;
- el dominio permanece independiente de la tecnología utilizada
  para persistir Version.

Debe mantenerse:

```text
Valid Modification

↓

Version N + 1
```

y:

```text
Rejected Operation

↓

Version N
```

---

# Concepto

Cada instancia de Document mantiene:

```text
Version
```

Version identifica la posición evolutiva actual del Aggregate.

Conceptualmente:

```text
Document

DocumentId = D1

Version = N
```

significa que el Aggregate identificado por:

```text
D1
```

se encuentra en su posición lógica:

```text
N
```

Version no constituye la identidad de Document.

Debe mantenerse:

```text
DocumentId

≠

Version
```

DocumentId permanece inmutable.

Version evoluciona cuando cambia válidamente el Aggregate.

---

# Ciclo de Vida

Version acompaña toda la evolución de Document.

Conceptualmente:

```text
CreateDocument
      │
      ▼
DocumentCreated
      │
      ▼
  Version 1
      │
      ▼
PublishDocument
      │
      ▼
DocumentPublished
      │
      ▼
  Version 2
      │
      ▼
ArchiveDocument
      │
      ▼
DocumentArchived
      │
      ▼
  Version 3
```

La numeración concreta debe preservar el principio fundamental:

```text
One Valid Aggregate Modification

=

One Version Increment
```

conforme al modelo consolidado de Versioning de AURA.

---

# Operaciones que Incrementan la Versión

Toda operación que produzca una modificación válida del Aggregate
incrementa Version.

Dentro del modelo Document versión 1.0, los Commands consolidados
que producen modificaciones son:

```text
CreateDocument

PublishDocument

ArchiveDocument
```

Conceptualmente:

```text
Version N

↓

Valid Command

↓

Valid Aggregate Modification

↓

Version N + 1
```

El incremento ocurre como consecuencia de una modificación válida
del Aggregate.

No como consecuencia de:

- lectura;
- consulta;
- autorización;
- proyección;
- serialización;
- entrega de mensajes;
- persistencia técnica aislada.

Si en el futuro Document incorpora otros Commands que produzcan
modificaciones válidas, dichos Commands deberán respetar la misma
regla.

---

# Operaciones que No Incrementan la Versión

No incrementan Version:

- lecturas del Aggregate;
- consultas;
- reconstrucción de Read Models;
- autorización de una intención;
- Commands rechazados;
- transiciones rechazadas;
- operaciones que no produzcan una modificación válida;
- consumo externo de Domain Events;
- generación de vistas derivadas.

Por ejemplo:

```text
DocumentStatus = Published

PublishDocument

↓

Rejected
```

debe mantener:

```text
Version = PreviousVersion
```

Del mismo modo:

```text
DocumentStatus = Draft

ArchiveDocument

↓

Rejected
```

no incrementa Version.

---

# Concurrencia Optimista

Document utiliza **Optimistic Concurrency Control**.

Una operación de modificación parte conceptualmente de una Version
conocida del Aggregate.

Ejemplo:

```text
PersistedVersion = 5

ExpectedVersion = 5
```

La modificación puede continuar si las demás reglas del dominio se
encuentran satisfechas.

Si otra operación modifica primero el mismo Document:

```text
PersistedVersion = 6

ExpectedVersion = 5
```

la segunda escritura no debe sobrescribir silenciosamente el cambio
ya confirmado.

Debe producirse conceptualmente:

```text
ConcurrencyConflict
```

Debe mantenerse:

```text
PersistedVersion

=

ExpectedVersion
```

como condición necesaria para aceptar una escritura basada en esa
versión.

---

# Persistencia

El Repository debe preservar Version como parte del estado del
Aggregate.

Conceptualmente:

```text
Load Document

↓

Version N

↓

Execute Valid Domain Operation

↓

Version N + 1

↓

Save
```

Antes de aceptar la escritura, el Repository debe verificar que la
versión utilizada para realizar la modificación continúa siendo
compatible con la versión persistida.

El Repository:

- no inventa Version;
- no evita el control de concurrencia;
- no modifica arbitrariamente Version;
- no sobrescribe silenciosamente una versión más reciente;
- persiste Document como una unidad de consistencia.

La definición formal del contrato pertenece a:

```text
DOMAIN-010G-Repository-Contract.md
```

---

# Relación con Domain Events

Todo Domain Event producido por una modificación válida debe
mantener coherencia con la Version resultante del Aggregate.

Los Domain Events oficiales de Document son:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Cada evento mantiene conceptualmente:

```text
AggregateVersion
```

Debe mantenerse:

```text
AggregateVersion

=

Resulting Document Version
```

Conceptualmente:

```text
Version 1
DocumentCreated

Version 2
DocumentPublished

Version 3
DocumentArchived
```

cuando dicha secuencia represente las modificaciones válidas del
mismo Document.

Para un mismo DocumentId, el orden lógico de evolución debe ser
coherente con AggregateVersion.

Una operación rechazada:

- no incrementa Version;
- no produce el Domain Event de éxito.

---

# Relación con Integration Events

Integration Events no controlan Version del Aggregate.

Un Integration Event puede derivar de un hecho confirmado del
dominio, pero no constituye por sí mismo una nueva modificación de
Document.

Debe mantenerse:

```text
Domain Modification

↓

Domain Event

↓

Integration Event
```

sin interpretar:

```text
Integration Event Publication

=

New Document Version
```

La publicación, reintento o consumo de un Integration Event no
incrementa Version.

La definición formal pertenece a:

```text
DOMAIN-010K-Integration-Events.md
```

---

# Relación con Outbox

Cuando la arquitectura de persistencia utilice Transactional
Outbox, Version debe continuar representando exclusivamente la
evolución del Aggregate.

Conceptualmente:

```text
Document Modification

+

Domain Events

+

Outbox Record
```

pueden formar parte de una operación persistente coordinada por las
capas externas.

El registro en Outbox no constituye una modificación adicional de
Document.

Por lo tanto:

```text
Outbox Insert

≠

Document Version Increment
```

La infraestructura responsable de Outbox no puede alterar las
reglas de Versioning del dominio.

---

# Recuperación

Al recuperar un Document desde persistencia debe restaurarse su
Version correspondiente.

Conceptualmente:

```text
Repository

↓

Rehydrate Document

↓

DocumentId = D1

Version = N
```

La recuperación:

- no constituye una modificación;
- no incrementa Version;
- no produce nuevos Domain Events;
- no altera el Lifecycle;
- no modifica DocumentStatus.

Debe mantenerse:

```text
Rehydration

≠

Domain Modification
```

---

# Integración con Event Store

Cuando la persistencia adopte un Event Store, la evolución de
Document puede reconstruirse mediante sus Domain Events.

Conceptualmente:

```text
DocumentCreated
      │
      ▼
DocumentPublished
      │
      ▼
DocumentArchived
      │
      ▼
Current Document
```

AggregateVersion permite mantener el orden lógico de evolución del
Aggregate.

Para un mismo DocumentId no deben existir dos modificaciones
confirmadas que ocupen de manera incompatible la misma posición
evolutiva.

La elección e implementación concreta de Event Store pertenece a
Infrastructure.

Document no depende de una tecnología de Event Store.

---

# Integración con CQRS

En CQRS, Version pertenece al lado de escritura.

Conceptualmente:

```text
Command

↓

Document Aggregate

↓

Version

↓

Domain Event
```

Los Read Models pueden proyectar Version cuando sea útil para
consulta, trazabilidad o sincronización.

Sin embargo:

```text
Read Model Version

≠

Authority to Modify Document
```

El Read Side no incrementa Version del Aggregate.

Solamente comportamiento válido ejecutado sobre Document puede
producir una nueva Version.

---

# Versionado del Contrato

La Version del Aggregate no debe confundirse con la versión
estructural de contratos.

Debe distinguirse:

```text
Aggregate Version

≠

Contract Version
```

Aggregate Version representa:

```text
evolución de una instancia concreta de Document
```

mientras una versión de contrato representa:

```text
evolución de la estructura de un contrato
```

El incremento de AggregateVersion no significa que haya cambiado
el esquema del Aggregate, del Domain Event o del Integration Event.

Del mismo modo, una evolución de contrato no incrementa
automáticamente Version de todos los Documents existentes.

---

# Restricciones

No está permitido:

- modificar Version directamente desde fuera del Aggregate;
- utilizar setters públicos para Version;
- omitir el incremento después de una modificación válida;
- incrementar Version después de una operación rechazada;
- incrementar Version por una lectura;
- incrementar Version por una consulta;
- incrementar Version por publicación o consumo de un Integration
  Event;
- sobrescribir silenciosamente una modificación concurrente;
- utilizar timestamps como sustituto obligatorio de Version;
- utilizar Version para reemplazar DocumentId;
- modificar versiones históricas para representar el estado actual;
- permitir que Infrastructure altere las reglas conceptuales de
  Versioning.

---

# Reglas

**REG-001**

Todo Document mantiene una Version asociada a su estado lógico.

**REG-002**

DocumentId y Version representan conceptos diferentes.

**REG-003**

Toda modificación válida incrementa Version.

**REG-004**

Una operación rechazada no incrementa Version.

**REG-005**

Una operación de lectura no incrementa Version.

**REG-006**

El Repository debe detectar escrituras incompatibles mediante
control de concurrencia optimista.

**REG-007**

Una modificación concurrente incompatible no puede sobrescribirse
silenciosamente.

**REG-008**

AggregateVersion de un Domain Event debe ser coherente con la
Version resultante del Aggregate.

**REG-009**

Integration Events, Read Models y mecanismos de Infrastructure no
incrementan Version por sí mismos.

**REG-010**

La recuperación o rehidratación restaura Version sin producir una
nueva modificación del Aggregate.

---

# Definición de Éxito

El Versioning del Aggregate **Document** garantiza una evolución
lógica consistente y permite detectar modificaciones concurrentes
incompatibles sin acoplar el dominio a tecnologías concretas.

El modelo garantiza que:

- Version pertenece al Aggregate;
- DocumentId permanece independiente de Version;
- toda modificación válida incrementa Version;
- una operación rechazada conserva Version;
- una lectura conserva Version;
- cada Domain Event mantiene AggregateVersion coherente;
- el Repository protege Optimistic Concurrency;
- una escritura obsoleta no sobrescribe silenciosamente una
  modificación posterior;
- Integration Events no incrementan Version;
- Outbox no incrementa Version;
- Read Models no controlan Version;
- la rehidratación restaura Version sin modificar el Aggregate;
- Event Store puede utilizar AggregateVersion para preservar el
  orden lógico cuando corresponda;
- Aggregate Version permanece separada del versionado estructural
  de contratos;
- Infrastructure no determina las reglas conceptuales de
  Versioning.

De esta forma, `DOMAIN-010I-Versioning.md` establece el modelo
oficial de Versioning del Aggregate **Document** conforme al patrón
consolidado de AURA Core.