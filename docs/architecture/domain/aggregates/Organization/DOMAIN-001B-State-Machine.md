# DOMAIN-001B — Organization State Machine

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

ADR Relacionados:

- ADR-001 Adaptive Domain Architecture

Documentos Relacionados:

- DOMAIN-001-Aggregate.md
- DOMAIN-001A-Lifecycle.md
- CORE-005-Domain-Events.md
- CORE-006-Domain-Invariants.md

---

# Objetivo

Definir formalmente la máquina de estados del Aggregate
Organization.

Mientras DOMAIN-001A describe el ciclo de vida desde una
perspectiva funcional, este documento especifica las
transiciones válidas, sus precondiciones, postcondiciones,
comandos habilitadores y eventos generados.

Este documento constituye la referencia oficial para la
implementación del Aggregate Root.

---

# Principios

La máquina de estados debe cumplir las siguientes reglas.

- determinista;
- completamente auditable;
- sin estados ambiguos;
- sin transiciones implícitas;
- sin transiciones automáticas;
- todas las transiciones generan eventos;
- todas las transiciones preservan las invariantes.

---

# Estados Oficiales

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

# Diagrama Oficial

```text
                         create()

                            │

                            ▼

                    ┌───────────────┐
                    │     Draft     │
                    └───────────────┘
                            │
        submitForValidation()
                            │
                            ▼
             ┌────────────────────────┐
             │ PendingValidation      │
             └────────────────────────┘
                 │              │
        approve()│              │reject()
                 │              │
                 ▼              ▼
        ┌───────────────┐   ┌───────────────┐
        │    Active     │◄──┘     Draft     │
        └───────────────┘
            │          │
 suspend()  │          │ archive()
            ▼          ▼
   ┌────────────────┐ ┌────────────────┐
   │   Suspended    │ │   Archived     │
   └────────────────┘ └────────────────┘
            │                  │
 reactivate()                  │
            │                  │
            ▼                  ▼
       ┌───────────────┐   ┌───────────────┐
       │    Active     │   │    Deleted    │
       └───────────────┘   └───────────────┘
```

---

# Tabla Oficial de Transiciones

| Estado Actual | Comando | Estado Resultante |
|---------------|----------|-------------------|
| Draft | submitForValidation | PendingValidation |
| Draft | delete | Deleted |
| PendingValidation | approve | Active |
| PendingValidation | reject | Draft |
| Active | suspend | Suspended |
| Active | archive | Archived |
| Suspended | reactivate | Active |
| Suspended | archive | Archived |
| Archived | delete | Deleted |

Toda transición no listada se considera inválida.

---

# Definición de Transiciones

## Draft → PendingValidation

### Comando

```text
submitForValidation()
```

### Precondiciones

- OrganizationId válido.
- Nombre válido.
- Tipo definido.
- Políticas configuradas.
- Configuración inicial completa.
- Representante principal asignado.
- Territorio definido cuando aplique.

### Postcondiciones

- Estado = PendingValidation.

### Evento

```text
OrganizationSubmittedForValidation
```

---

## PendingValidation → Active

### Comando

```text
approve()
```

### Precondiciones

- Validación administrativa aprobada.
- Toda documentación aceptada.
- Sin observaciones pendientes.

### Postcondiciones

- Estado = Active.

### Evento

```text
OrganizationActivated
```

---

## PendingValidation → Draft

### Comando

```text
reject()
```

### Precondiciones

- Existen observaciones.
- La validación no fue aprobada.

### Postcondiciones

- Estado = Draft.

### Evento

```text
OrganizationValidationRejected
```

---

## Active → Suspended

### Comando

```text
suspend()
```

### Precondiciones

- Estado actual Active.

### Postcondiciones

- Estado = Suspended.

### Evento

```text
OrganizationSuspended
```

---

## Suspended → Active

### Comando

```text
reactivate()
```

### Precondiciones

- Causa de suspensión resuelta.
- Estado actual Suspended.

### Postcondiciones

- Estado = Active.

### Evento

```text
OrganizationReactivated
```

---

## Active → Archived

### Comando

```text
archive()
```

### Precondiciones

- Organización cerrada oficialmente.
- No existen procesos críticos abiertos.

### Postcondiciones

- Estado = Archived.

### Evento

```text
OrganizationArchived
```

---

## Suspended → Archived

### Comando

```text
archive()
```

### Precondiciones

- Estado Suspended.

### Postcondiciones

- Estado Archived.

### Evento

```text
OrganizationArchived
```

---

## Draft → Deleted

### Comando

```text
delete()
```

### Precondiciones

- Organización nunca activada.

### Postcondiciones

- Estado Deleted.

### Evento

```text
OrganizationDeleted
```

---

## Archived → Deleted

### Comando

```text
delete()
```

### Precondiciones

- Política de retención cumplida.
- Eliminación autorizada.

### Postcondiciones

- Estado Deleted.

### Evento

```text
OrganizationDeleted
```

---

# Transiciones Prohibidas

Las siguientes transiciones nunca podrán ocurrir.

```text
Draft
        → Active

Draft
        → Archived

Draft
        → Suspended

PendingValidation
        → Archived

PendingValidation
        → Suspended

Archived
        → Active

Archived
        → Draft

Deleted
        → cualquier estado

Suspended
        → Draft
```

---

# Reglas de Consistencia

## Regla 1

Toda transición modifica exactamente un estado.

---

## Regla 2

Toda transición ocurre dentro de una única transacción.

---

## Regla 3

Toda transición genera exactamente un Domain Event.

---

## Regla 4

Ninguna transición puede omitir validaciones.

---

## Regla 5

El estado nunca cambia mediante setters.

---

## Regla 6

Las transiciones únicamente pueden ejecutarse desde
Organization.

---

## Regla 7

Una transición fallida no modifica el Aggregate.

---

## Regla 8

Toda transición preserva las invariantes del dominio.

---

# Integración con Command Handlers

Cada transición será iniciada mediante un Command.

Ejemplo.

```text
CreateOrganizationCommand

↓

Organization.create()

↓

OrganizationCreated
```

```text
ApproveOrganizationCommand

↓

Organization.approve()

↓

OrganizationActivated
```

La lógica de transición pertenece exclusivamente al
Aggregate.

---

# Integración con Event Bus

Una vez confirmada la transacción:

```text
Organization

↓

Domain Event

↓

Outbox

↓

Event Bus

↓

Otros Bounded Contexts
```

El Aggregate nunca publica eventos directamente.

---

# Consideraciones de Implementación

La máquina de estados deberá implementarse mediante
comportamientos explícitos del Aggregate Root.

No se permitirán:

- flags booleanos para representar estados;
- cadenas de `if` dispersas por la aplicación;
- modificaciones directas del atributo `status`;
- validaciones fuera del Aggregate.

La representación del estado deberá realizarse mediante un
Value Object (`OrganizationStatus`) o un tipo enumerado del
dominio, manteniendo una única fuente de verdad.

---

# Definición de Éxito

La máquina de estados del Aggregate Organization garantiza
que todas las transiciones del ciclo de vida sean
explícitas, deterministas, auditables y consistentes,
preservando las invariantes del dominio y constituyendo la
única autoridad para la evolución del estado organizacional
dentro del ecosistema AURA.