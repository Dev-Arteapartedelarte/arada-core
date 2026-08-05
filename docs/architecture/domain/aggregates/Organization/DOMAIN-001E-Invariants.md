# DOMAIN-001E — Organization Invariants

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
- DOMAIN-001A-Lifecycle.md
- DOMAIN-001B-State-Machine.md
- DOMAIN-001C-Commands.md
- DOMAIN-001D-Domain-Events.md
- CORE-006-Domain-Invariants.md

---

# Objetivo

Definir las invariantes del Aggregate Organization.

Las invariantes representan las reglas fundamentales que
deben cumplirse siempre. Ningún comando, transición,
servicio de dominio o repositorio puede dejar el Aggregate
en un estado que viole alguna de estas reglas.

Las invariantes constituyen la principal responsabilidad
del Aggregate Root.

---

# Definición

Una invariante es una condición que permanece verdadera
durante toda la existencia del Aggregate.

No depende del flujo de ejecución.

No depende de la interfaz.

No depende de la persistencia.

Forma parte del dominio.

---

# Principios

Las invariantes deben ser:

- permanentes;
- explícitas;
- verificables;
- deterministas;
- independientes de la infraestructura;
- protegidas únicamente por el Aggregate.

---

# Invariantes de Identidad

## INV-001

Toda Organization posee un único OrganizationId.

Nunca cambia.

---

## INV-002

No pueden existir dos organizaciones con el mismo
OrganizationId.

---

## INV-003

La identidad de la organización es independiente de su
nombre, estado o configuración.

---

# Invariantes de Estado

## INV-004

La organización siempre posee un estado válido.

Estados permitidos.

```text
Draft

PendingValidation

Active

Suspended

Archived

Deleted
```

---

## INV-005

No existen estados intermedios.

---

## INV-006

Toda transición debe cumplir la máquina de estados
definida en DOMAIN-001B.

---

## INV-007

Una organización eliminada (Deleted) no puede volver a
cambiar de estado.

---

# Invariantes de Nombre

## INV-008

Toda organización posee un nombre oficial.

---

## INV-009

El nombre no puede estar vacío.

---

## INV-010

El nombre debe cumplir las reglas del Value Object
OrganizationName.

---

# Invariantes de Representación

## INV-011

Toda organización posee exactamente un representante
principal.

---

## INV-012

El representante principal debe pertenecer a la propia
organización.

---

## INV-013

No pueden existir dos representantes principales activos
simultáneamente.

---

# Invariantes de Membresía

## INV-014

Todo miembro pertenece a una única organización.

---

## INV-015

Un miembro no puede registrarse dos veces dentro de la
misma organización.

---

## INV-016

Una organización Active debe poseer al menos un miembro.

---

# Invariantes de Configuración

## INV-017

La configuración institucional siempre existe.

Nunca es nula.

---

## INV-018

Las políticas institucionales siempre existen.

---

## INV-019

La configuración debe ser consistente con el estado de la
organización.

---

# Invariantes Territoriales

## INV-020

Toda organización pertenece a un territorio válido cuando
el tipo organizacional así lo requiera.

---

## INV-021

El territorio debe existir antes de ser asociado.

---

# Invariantes de Auditoría

## INV-022

Toda modificación del Aggregate debe registrar la fecha de
ocurrencia.

---

## INV-023

Toda modificación debe registrar el actor responsable.

---

## INV-024

Toda modificación debe producir trazabilidad completa.

---

# Invariantes de Eventos

## INV-025

Todo cambio exitoso del Aggregate genera uno o más Domain
Events.

---

## INV-026

Los Domain Events deben representar únicamente hechos ya
ocurridos.

---

## INV-027

Los eventos deben emitirse respetando el orden de la
transacción.

---

# Invariantes de Persistencia

## INV-028

El Aggregate se guarda siempre como una unidad
transaccional.

---

## INV-029

No puede persistirse parcialmente.

---

## INV-030

La versión del Aggregate debe incrementarse en cada cambio
exitoso.

---

# Invariantes de Consistencia

## INV-031

El Aggregate nunca puede quedar en un estado inválido tras
ejecutar un Command.

---

## INV-032

Si una regla falla, toda la operación debe revertirse.

---

## INV-033

No existen modificaciones parciales del Aggregate.

---

# Invariantes Arquitectónicas

## INV-034

Ninguna regla del dominio puede depender de:

- HTTP;
- Base de Datos;
- Frameworks;
- UI;
- APIs externas.

---

## INV-035

Todas las reglas de negocio pertenecen al Aggregate o a un
Domain Service.

---

## INV-036

Las invariantes nunca son validadas por los repositorios.

---

# Responsabilidades

El Aggregate Root es responsable de garantizar todas las
invariantes antes y después de ejecutar cualquier comando.

Los Application Services coordinan casos de uso.

Los Repository únicamente persisten.

Los Domain Services encapsulan reglas que involucran más
de un Aggregate.

---

# Validación

Las invariantes deben comprobarse:

- al crear el Aggregate;
- antes de ejecutar una transición;
- antes de emitir eventos;
- antes de persistir cambios.

Nunca deben confiar únicamente en validaciones de entrada
(UI o API).

---

# Violaciones

Cuando una invariante no pueda cumplirse:

- el Aggregate rechaza la operación;
- no cambia su estado;
- no genera Domain Events;
- no se persiste ninguna modificación.

La violación debe expresarse mediante un Domain Error
específico.

---

# Definición de Éxito

El Aggregate Organization mantiene su consistencia durante
todo su ciclo de vida garantizando que ninguna operación,
sin importar su origen, pueda romper las reglas esenciales
del dominio. Las invariantes constituyen la máxima
autoridad sobre la integridad del Aggregate y aseguran un
modelo de negocio robusto, predecible y alineado con los
principios de Domain-Driven Design.