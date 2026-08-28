"""
Pruebas de Domain del Bounded Context Proposal.

Este paquete contiene las pruebas automatizadas del modelo de dominio de
Proposal para el Vertical Slice VS-001.

Las pruebas de Domain deben validar exclusivamente comportamiento e invariantes
del Aggregate y sus Value Objects, sin depender de Application,
Infrastructure ni adapters externos.

Para VS-001 deben cubrir, entre otros, los siguientes comportamientos
normativos:

- creación válida de una Proposal;
- estado inicial Draft;
- Version inicial igual a 1;
- producción de ProposalCreated;
- presentación válida Draft -> Submitted;
- incremento de Version exactamente una vez;
- registro de SubmittedAt;
- producción de ProposalSubmitted;
- rechazo de una nueva presentación desde Submitted;
- ausencia de cambios de estado ante operaciones inválidas;
- ausencia de incremento de Version ante operaciones inválidas;
- ausencia de nuevos Domain Events ante operaciones inválidas;
- estabilidad de ProposalId;
- estabilidad de OrganizationId;
- conservación de referencias externas sin absorber otros Aggregates.

Las pruebas deben observar únicamente la API pública del Aggregate salvo que
sea estrictamente necesario verificar una propiedad interna protegida por una
invariante explícita.

No se deben utilizar:

- Repository implementations;
- bases de datos;
- HTTP;
- FIWARE;
- NGSI-LD;
- mocks de Infrastructure;
- lógica perteneciente a otros Bounded Contexts.

Los símbolos de test no se exportan desde este inicializador.
"""