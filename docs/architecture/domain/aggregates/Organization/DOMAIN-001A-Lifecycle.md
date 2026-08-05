# DOMAIN-001A — Organization Lifecycle

Versión: 1.0

Estado: Oficial

Proyecto: AURA Core

Bounded Context:
Organization Management

Aggregate:
Organization

Autor:
ARADA

---

# Objetivo

Definir el ciclo de vida completo del Aggregate
Organization.

Este documento especifica los estados por los cuales puede
transitar una organización desde su creación hasta su
retiro definitivo del ecosistema AURA.

El ciclo de vida constituye parte de las reglas del dominio
y debe ser respetado por todas las implementaciones.

---

# Principios

El ciclo de vida de una organización debe cumplir las
siguientes propiedades.

- determinista;
- consistente;
- auditable;
- reversible únicamente cuando el dominio lo permita;
- gobernado exclusivamente por el Aggregate Root.

---

# Estados Oficiales

El Aggregate Organization puede encontrarse únicamente en
uno de los siguientes estados.

```text
Draft

PendingValidation

Active

Suspended

Archived

Deleted
```

No existen estados adicionales.

---

# Estado: Draft

## Descripción

Representa una organización recién creada.

Todavía no forma parte del ecosistema operativo.

Puede encontrarse incompleta.

---

## Objetivo

Permitir la creación progresiva de la organización antes
de solicitar su incorporación formal.

---

## Operaciones Permitidas

```text
rename()

changeAddress()

changePolicies()

changeSettings()

changeBrand()

assignRepresentative()

changeTerritory()

submitForValidation()

delete()
```

---

## Operaciones Prohibidas

```text
activate()

createAssembly()

registerCitizen()

issueOfficialDocuments()

vote()

publish()
```

---

# Estado: PendingValidation

## Descripción

La organización ha solicitado validación y espera revisión.

Durante este estado no puede iniciar procesos
institucionales.

---

## Objetivo

Garantizar que la organización cumple los requisitos del
dominio antes de quedar activa.

---

## Operaciones Permitidas

```text
approve()

reject()

suspendValidation()

updateDocumentation()
```

---

## Operaciones Prohibidas

Toda operación operacional.

---

# Estado: Active

## Descripción

La organización forma parte oficialmente del ecosistema
AURA.

Puede operar normalmente.

---

## Capacidades

Puede:

- administrar miembros;
- convocar asambleas;
- emitir propuestas;
- iniciar votaciones;
- administrar documentos;
- publicar información;
- integrarse con otros servicios.

---

## Operaciones Permitidas

```text
rename()

changeSettings()

changePolicies()

changeBrand()

registerMember()

removeMember()

createAssembly()

createProposal()

createDocument()

suspend()

archive()
```

---

# Estado: Suspended

## Descripción

La organización permanece registrada pero sus operaciones
quedan temporalmente restringidas.

---

## Motivos

Ejemplos:

- incumplimiento normativo;
- suspensión administrativa;
- solicitud voluntaria;
- investigación.

---

## Operaciones Permitidas

```text
reactivate()

archive()

updateContactInformation()
```

---

## Operaciones Bloqueadas

```text
createAssembly()

createProposal()

vote()

publish()

registerMember()
```

---

# Estado: Archived

## Descripción

La organización deja de operar pero conserva toda su
historia.

Es un estado permanente.

---

## Objetivo

Garantizar trazabilidad y preservación histórica.

---

## Operaciones Permitidas

```text
query()

export()

audit()
```

---

## Operaciones Prohibidas

Todas las operaciones de modificación.

---

# Estado: Deleted

## Descripción

Representa una eliminación lógica.

No implica eliminación física de datos.

---

## Objetivo

Cumplir requisitos regulatorios, retención documental y
auditoría.

---

# Máquina de Estados

```text
                +------------------+
                |      Draft       |
                +------------------+
                          |
                          |
                          v
          +-------------------------------+
          | PendingValidation             |
          +-------------------------------+
               |                   |
        approve()             reject()
               |                   |
               v                   |
        +------------------+       |
        |     Active       |<------+
        +------------------+
           |           |
 suspend() |           | archive()
           |           |
           v           v
 +----------------+  +----------------+
 |  Suspended     |  |   Archived     |
 +----------------+  +----------------+
          |
 reactivate()
          |
          +--------------------+
                               |
                               v
                        +---------------+
                        |    Active     |
                        +---------------+
```

---

# Transiciones Permitidas

| Estado origen | Estado destino |
|---------------|----------------|
| Draft | PendingValidation |
| Draft | Deleted |
| PendingValidation | Active |
| PendingValidation | Draft |
| Active | Suspended |
| Active | Archived |
| Suspended | Active |
| Suspended | Archived |
| Archived | Deleted |

Cualquier otra transición está prohibida.

---

# Reglas del Dominio

## Regla 1

Una organización siempre comienza en Draft.

---

## Regla 2

Nunca puede activarse directamente.

Debe pasar por PendingValidation.

---

## Regla 3

Una organización suspendida conserva toda su información.

---

## Regla 4

Archive nunca elimina información.

---

## Regla 5

Deleted representa una eliminación lógica.

---

## Regla 6

Una organización archivada nunca vuelve al estado Active.

---

## Regla 7

Cada transición debe generar exactamente un Domain Event.

---

# Domain Events Asociados

```text
OrganizationCreated

OrganizationSubmittedForValidation

OrganizationValidated

OrganizationRejected

OrganizationActivated

OrganizationSuspended

OrganizationReactivated

OrganizationArchived

OrganizationDeleted
```

---

# Responsabilidades del Aggregate

El Aggregate Organization es el único responsable de:

- validar transiciones;
- impedir cambios ilegales;
- preservar invariantes;
- publicar eventos;
- mantener consistencia transaccional.

Ningún servicio externo puede modificar directamente el
estado del ciclo de vida.

---

# Integración con Otros Aggregates

Los demás Aggregates deben considerar el estado del ciclo
de vida antes de ejecutar operaciones.

Ejemplos:

- Assembly requiere Organization Active.
- Proposal requiere Organization Active.
- Voting requiere Organization Active.
- Membership requiere Organization Active.

---

# Definición de Éxito

El ciclo de vida del Aggregate Organization garantiza que
toda organización del ecosistema AURA evoluciona mediante
transiciones explícitas, auditables y consistentes,
preservando las invariantes del dominio y evitando estados
inválidos o ambiguos durante toda su existencia.