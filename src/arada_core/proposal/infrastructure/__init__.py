"""
Infrastructure Layer del Bounded Context Proposal.

Este paquete contiene las implementaciones técnicas de los contratos definidos
por Domain y Application para Proposal Management.

Conforme a CORE-015 y CORE-016:

- Infrastructure depende de Domain y Application;
- Domain nunca depende de Infrastructure;
- Application nunca depende de implementaciones concretas de Infrastructure;
- los Repository Contracts definidos por Domain se implementan aquí;
- los Output Ports definidos por Application se implementan aquí cuando exista
  una tecnología concreta que satisfaga la capacidad requerida;
- los detalles de persistencia, mensajería, identidad e integración permanecen
  fuera del Aggregate Proposal;
- las decisiones técnicas no deben modificar Lifecycle, State Machine,
  invariantes, Version ni Consistency Boundary.

Para VS-001 no se introduce todavía una implementación concreta de:

    ProposalRepository
    AuthorizationPort
    ProposalReferenceValidationPort
    DomainEventPublisher
    IntegrationEventPublisher

porque no existe en este Vertical Slice una decisión tecnológica consolidada
que justifique seleccionar anticipadamente:

- motor de persistencia;
- ORM;
- proveedor de identidad;
- mecanismo de mensajería;
- broker de eventos;
- protocolo de integración;
- adapter FIWARE o NGSI-LD.

Introducir cualquiera de esas implementaciones requerirá una decisión
arquitectónica explícita y deberá respetar la dependencia:

    Inbound Adapter
        |
        v
    Application
        |
        v
    Domain

y para capacidades de salida:

    Application / Domain Contract
        ^
        |
    Infrastructure Adapter

FIWARE permanece fuera del núcleo transaccional de Proposal. Cualquier
adaptación futura hacia NGSI-LD deberá respetar DOMAIN-013 Integration y la
separación:

    Domain Event
        !=
    Integration Event
        !=
    NGSI-LD Notification

Los símbolos públicos se exportarán únicamente cuando existan implementaciones
concretas aprobadas y verificadas.
"""