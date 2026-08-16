# DOMAIN-001O — Organization Security Model

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## Modelo

Application autentica al actor mediante un inbound port, valida contexto
organizacional y exige la Permission de DOMAIN-001F. Role, Membership y
Citizen no conceden acceso automáticamente.

El Aggregate protege estados e invariantes independientemente de la
autorización previa. Repository y adapters no deciden Permissions.

Los Integration Events aplican minimización de datos; secretos,
credenciales, tokens y modelos de Identity Provider nunca ingresan al
Aggregate ni al payload público.

Auditoría, cifrado, rate limiting y seguridad de transporte se implementan
fuera del dominio mediante puertos y adapters.
