"""
Pruebas de Application del Bounded Context Proposal.

Este paquete contiene las pruebas automatizadas de los casos de uso de
Proposal correspondientes al Vertical Slice VS-001.

Las pruebas de Application deben verificar coordinación y fronteras
arquitectónicas sin introducir reglas pertenecientes al Aggregate.

Para VS-001 deben cubrir principalmente:

CreateProposalService
---------------------

- autorización mediante proposal:create;
- rechazo de actores no autorizados;
- validación de OrganizationId;
- validación de ProposerReference;
- validación opcional de TerritoryId;
- validación opcional de AssemblyId;
- rechazo cuando ProposalId ya existe;
- delegación de creación al Aggregate Proposal;
- persistencia del Aggregate completo;
- persistencia inicial con expected_version=None;
- publicación de Domain Events únicamente después de una persistencia válida;
- ausencia de publicación cuando la persistencia falla;
- devolución de ProposalResult sin exponer el Aggregate.

SubmitProposalService
---------------------

- autorización mediante proposal:submit;
- rechazo de actores no autorizados;
- recuperación del Aggregate mediante ProposalRepository;
- rechazo cuando Proposal no existe;
- validación de referencias externas necesarias;
- delegación de Draft -> Submitted al Aggregate;
- persistencia utilizando ExpectedVersion;
- ausencia de sustitución o modificación de ExpectedVersion por Application;
- publicación de ProposalSubmitted únicamente después de persistir;
- ausencia de publicación cuando la persistencia falla;
- devolución de ProposalResult con estado y versión resultantes.

Las pruebas deben utilizar doubles explícitos de:

    ProposalRepository
    AuthorizationPort
    ProposalReferenceValidationPort
    DomainEventPublisher

y no implementaciones reales de Infrastructure.

No deben utilizar:

- bases de datos;
- ORM;
- SQL;
- HTTP;
- FIWARE;
- NGSI-LD;
- adapters de producción;
- IntegrationEventPublisher mientras VS-001 no coordine todavía un contrato
  concreto de Integration Event.

Las pruebas de Application no deben reproducir Lifecycle, State Machine ni
invariantes. Estas decisiones permanecen bajo autoridad del Aggregate
Proposal.
"""