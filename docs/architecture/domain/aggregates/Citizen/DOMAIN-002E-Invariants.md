# DOMAIN-002E — Citizen Invariants

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
- DOMAIN-002A-Lifecycle.md
- DOMAIN-002B-State-Machine.md
- DOMAIN-002C-Commands.md
- DOMAIN-002D-Domain-Events.md
- CORE-006-Domain-Invariants.md

---

# Objetivo

Este documento define las invariantes oficiales del Aggregate
Citizen.

Las invariantes representan reglas de negocio que siempre deben
cumplirse durante toda la vida del Aggregate. Ningún Command,
Application Service, Repository o mecanismo de persistencia
puede violarlas.

Su objetivo es preservar la consistencia del dominio,
independientemente de la tecnología utilizada.

---

# Principios

Las invariantes del Aggregate cumplen los siguientes principios:

- son permanentes;
- son independientes de la infraestructura;
- representan reglas del negocio;
- son verificables;
- protegen la consistencia del Aggregate;
- no pueden deshabilitarse.

---

# Invariantes Fundamentales

## INV-001

Todo Citizen posee un único CitizenId.

Nunca puede existir más de una identidad con el mismo
identificador.

---

## INV-002

CitizenId nunca cambia.

Una vez asignado permanece inmutable durante todo el ciclo de
vida del Aggregate.

---

## INV-003

Todo Citizen posee exactamente un estado válido definido por la
State Machine.

No pueden coexistir múltiples estados simultáneamente.

---

## INV-004

Toda transición de estado debe estar definida por la máquina de
estados oficial.

Las transiciones implícitas o manuales están prohibidas.

---

## INV-005

Todo cambio del Aggregate incrementa su versión.

La versión nunca disminuye.

---

## INV-006

Todo cambio exitoso genera al menos un Domain Event.

No existen modificaciones silenciosas.

---

## INV-007

Los Domain Events nunca se modifican ni eliminan.

Representan hechos históricos permanentes.

---

## INV-008

Un Citizen archivado no puede volver a estados operativos.

```text
Archived

×

Active
```

La transición está prohibida.

---

## INV-009

Un Citizen suspendido conserva completamente su identidad.

La suspensión restringe operaciones, pero nunca elimina datos.

---

## INV-010

Un Citizen inactivo conserva todas sus relaciones históricas.

La desactivación no rompe la integridad referencial.

---

## INV-011

Todo Citizen debe poseer información mínima de identidad antes
de alcanzar el estado **Verified**.

Como mínimo:

- nombre legal;
- identificador oficial definido por la organización
  (cuando corresponda);
- información de contacto requerida por las políticas del
  dominio.

---

## INV-012

Ningún Citizen puede participar en procesos del dominio mientras
no alcance el estado **Active**.

Esto incluye, entre otros:

- membresías;
- votaciones;
- asambleas;
- propuestas;
- procesos participativos.

---

## INV-013

Toda modificación de datos personales debe preservar la
consistencia de los Value Objects asociados.

No pueden existir direcciones, correos electrónicos, números
telefónicos u otros datos parcialmente válidos.

---

## INV-014

Todo Citizen pertenece exactamente a un Aggregate Root.

Las entidades internas nunca pueden compartirse entre
Aggregates.

---

## INV-015

Los cambios de información personal deben mantener la identidad
histórica del Aggregate.

Actualizar datos nunca implica crear un nuevo Citizen.

---

## INV-016

La aceptación de políticas o consentimientos debe quedar
registrada mediante Domain Events.

Nunca puede almacenarse únicamente como un estado mutable.

---

## INV-017

Las referencias desde otros Aggregates siempre utilizan
CitizenId.

Nunca deben depender de información mutable como nombre,
correo electrónico o dirección.

---

## INV-018

Todo Command debe ejecutarse sobre la versión vigente del
Aggregate.

Las versiones obsoletas deben rechazarse para evitar conflictos
de concurrencia.

---

## INV-019

Las operaciones sobre un Citizen archivado son únicamente de
lectura.

No se permiten modificaciones posteriores al archivado.

---

## INV-020

La historia completa del Aggregate debe poder reconstruirse
mediante la secuencia de Domain Events.

No puede existir información indispensable fuera del historial
de eventos.

---

# Reglas de Validación

Las invariantes deben verificarse:

- antes de ejecutar un Command;
- antes de confirmar cambios del Aggregate;
- antes de publicar Domain Events;
- antes de persistir el Aggregate.

Si alguna invariante falla, la operación debe cancelarse.

---

# Relación con la State Machine

Las invariantes complementan la máquina de estados.

La State Machine determina:

- qué transiciones son posibles.

Las invariantes determinan:

- bajo qué condiciones dichas transiciones son válidas.

Ambos mecanismos son obligatorios y complementarios.

---

# Compatibilidad con Event Sourcing

Todas las invariantes deben mantenerse tanto durante la
ejecución normal como durante la reconstrucción del Aggregate
mediante la reproducción de eventos.

Un historial de eventos nunca puede producir un estado inválido.

---

# Compatibilidad con CQRS

Las proyecciones de lectura no aplican invariantes de negocio.

Las invariantes se verifican exclusivamente en el lado de
escritura (Command Side), garantizando que toda información
publicada ya sea consistente.

---

# Evolución

Nuevas invariantes podrán incorporarse cuando evolucionen las
reglas del negocio, siempre que:

- no contradigan invariantes existentes;
- respeten el Ubiquitous Language;
- mantengan la compatibilidad con los Aggregates
  relacionados;
- preserven la consistencia del dominio.

---

# Definición de Éxito

Las invariantes del Aggregate Citizen garantizan que toda
identidad cívica administrada por AURA conserve un estado
válido, consistente y trazable durante todo su ciclo de vida.
Constituyen el mecanismo principal para proteger la integridad
del dominio frente a errores de implementación, concurrencia o
integración, asegurando que las reglas de negocio permanezcan
inalterables independientemente de la infraestructura o la
tecnología utilizada.