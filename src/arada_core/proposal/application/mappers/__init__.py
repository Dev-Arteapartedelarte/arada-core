"""
Mappers de Application para el Bounded Context Proposal.

Este paquete contiene transformaciones explícitas entre representaciones
pertenecientes a diferentes fronteras arquitectónicas.

Para VS-001, su responsabilidad principal es traducir:

    ProposalCreated
        ->
    ProposalCreatedForIntegration

y:

    ProposalSubmitted
        ->
    ProposalSubmittedForIntegration

La existencia de este paquete preserva la separación:

    Domain Event
        !=
    Integration Event

Los mappers de Application:

- no ejecutan reglas de negocio;
- no modifican el Aggregate Proposal;
- no reproducen la State Machine;
- no autorizan operaciones;
- no persisten estado;
- no publican eventos;
- no conocen Infrastructure;
- no conocen brokers de mensajería;
- no conocen FIWARE;
- no conocen NGSI-LD;
- no convierten automáticamente cualquier Domain Event en Integration Event;
- construyen únicamente contratos de integración explícitamente aprobados.

La decisión acerca de qué Domain Events poseen relevancia externa pertenece
al diseño de Application y a los contratos normativos correspondientes.

En VS-001 se reconocen explícitamente:

    ProposalCreated
        -> ProposalCreatedForIntegration

    ProposalSubmitted
        -> ProposalSubmittedForIntegration

La serialización posterior de estos contratos y su adaptación hacia sistemas
externos pertenecen a las capas de integración e infraestructura
correspondientes.

No se exportan símbolos desde este initializer para mantener imports
explícitos y evitar acoplamientos accidentales entre mappers.
"""