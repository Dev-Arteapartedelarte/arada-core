# DOMAIN-001M — Organization Test Scenarios

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## Escenarios obligatorios

1. Cada Command oficial tiene caso exitoso y rechazo por estado inválido.
2. Creation inicia en Draft con versión e identidad válidas.
3. Todas las transiciones coinciden con DOMAIN-001B.
4. Los Commands descriptivos conservan OrganizationStatus.
5. Cada cambio válido incrementa AggregateVersion una vez y genera el
   Domain Event esperado.
6. Un rechazo conserva estado, versión y eventos.
7. ExpectedAggregateVersion obsoleta impide persistencia.
8. El Repository opera sobre una Organization completa.
9. Ningún Command modifica Membership, Role o Representative.
10. Un Integration Event sólo puede prepararse después del commit.
11. Las proyecciones no escriben en el Aggregate.
12. Event Sourcing no es requisito para ejecutar la suite.
