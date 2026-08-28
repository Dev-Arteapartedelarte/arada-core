"""
Ports de la Application Layer del Bounded Context Proposal.

Este paquete contiene los contratos mediante los cuales Application expone
casos de uso y solicita capacidades externas necesarias para coordinarlos.

Conforme a la arquitectura Hexagonal de AURA Core, los Ports se dividen
conceptualmente en:

Input Ports
    Capacidades que Application expone a los adapters de entrada.

Output Ports
    Capacidades externas que Application necesita para completar un caso de
    uso sin depender de implementaciones concretas de Infrastructure.

Para VS-001 se utilizarán los siguientes contratos aprobados:

Input Ports:

    CreateProposalUseCase
    SubmitProposalUseCase

Output Ports:

    AuthorizationPort
    ProposalReferenceValidationPort
    DomainEventPublisher
    IntegrationEventPublisher

Estos contratos deben preservar las siguientes reglas:

- Application depende de abstracciones, no de adapters concretos;
- ningún Port contiene lógica de dominio;
- ningún Port redefine invariantes;
- ningún Port modifica Proposal directamente;
- los Output Ports permanecen tecnológicamente neutrales;
- no deben aparecer nombres específicos de Keyrock, FIWARE, Orion,
  mensajería, bases de datos o frameworks;
- DomainEventPublisher e IntegrationEventPublisher representan
  responsabilidades diferentes;
- Domain Event e Integration Event no son equivalentes;
- los efectos externos deben respetar la coordinación post-Commit definida
  por AURA Core.

UnitOfWork permanece reservado y no forma parte de VS-001 mientras no exista
una necesidad concreta de persistencia que justifique introducir dicho
contrato.

Los símbolos públicos se exportarán únicamente cuando sus implementaciones
correspondientes hayan sido creadas y verificadas.
"""