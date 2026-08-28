from datetime import datetime

from arada_core.proposal.application.commands.create_proposal import CreateProposal
from arada_core.proposal.application.dto.proposal_result import ProposalResult
from arada_core.proposal.application.mappers.proposal_integration_event_mapper import (
    ProposalIntegrationEventMapper,
)
from arada_core.proposal.application.ports.authorization_port import AuthorizationPort
from arada_core.proposal.application.ports.domain_event_publisher import (
    DomainEventPublisher,
)
from arada_core.proposal.application.ports.integration_event_publisher import (
    IntegrationEventPublisher,
)
from arada_core.proposal.application.ports.proposal_reference_validation_port import (
    ProposalReferenceValidationPort,
)
from arada_core.proposal.domain.aggregates.proposal import Proposal
from arada_core.proposal.domain.events.proposal_created import ProposalCreated
from arada_core.proposal.domain.repositories.proposal_repository import (
    ProposalRepository,
)


class CreateProposalService:
    """
    Application Service para el caso de uso CreateProposal.

    Responsabilidades:

    - comprobar autorización para ``proposal:create``;
    - validar referencias externas mediante puertos;
    - impedir creación de una Proposal con identidad ya existente;
    - delegar la creación del estado válido al Aggregate Proposal;
    - persistir una única Proposal;
    - publicar Domain Events únicamente después de persistencia exitosa;
    - traducir hechos relevantes a Integration Events;
    - publicar Integration Events únicamente después de persistencia exitosa;
    - devolver un DTO de Application y nunca el Aggregate.

    El Service no:

    - contiene reglas de negocio propias de Proposal;
    - modifica ProposalStatus directamente;
    - modifica ProposalVersion directamente;
    - reproduce invariantes;
    - reproduce la State Machine;
    - ejecuta SQL;
    - conoce ORM;
    - conoce FIWARE;
    - conoce NGSI-LD;
    - conoce mecanismos concretos de mensajería;
    - implementa Transactional Outbox;
    - genera EventId;
    - inventa CorrelationId;
    - inventa CausationId;
    - utiliza ActorId como sustituto de metadata de trazabilidad.

    La metadata de integración se recibe explícitamente desde la frontera
    de invocación de Application.

    Debe mantenerse:

        ActorId
            !=
        CorrelationId
            !=
        CausationId

    y:

        Domain Event
            !=
        Integration Event

    Flujo conceptual:

        CreateProposal
            |
            v
        Authorization
            |
            v
        External Reference Validation
            |
            v
        Proposal.create(...)
            |
            v
        Repository.save(...)
            |
            v
        Domain Event Publication
            |
            v
        Integration Mapping
            |
            v
        Integration Event Publication

    La implementación expresa únicamente el orden lógico disponible en
    VS-001.

    La garantía técnica de atomicidad entre persistencia y publicación no
    se presupone aquí y deberá resolverse posteriormente en Infrastructure
    mediante una decisión arquitectónica explícita cuando corresponda.
    """

    CREATE_PERMISSION = "proposal:create"

    def __init__(
        self,
        *,
        repository: ProposalRepository,
        authorization: AuthorizationPort,
        reference_validation: ProposalReferenceValidationPort,
        domain_event_publisher: DomainEventPublisher,
        integration_event_publisher: IntegrationEventPublisher,
    ) -> None:
        self._repository = repository
        self._authorization = authorization
        self._reference_validation = reference_validation
        self._domain_event_publisher = domain_event_publisher
        self._integration_event_publisher = integration_event_publisher

    def execute(
        self,
        command: CreateProposal,
        *,
        actor_id: str,
        integration_event_id: str,
        published_at: datetime,
        correlation_id: str | None = None,
        causation_id: str | None = None,
    ) -> ProposalResult:
        """
        Ejecuta CreateProposal dentro de Application.

        ``actor_id`` se utiliza exclusivamente para autorización.

        ``integration_event_id`` identifica el contrato público que será
        construido si ProposalCreated se confirma correctamente.

        ``published_at`` representa el instante de preparación/publicación
        contractual.

        ``correlation_id`` y ``causation_id`` preservan metadata transversal
        únicamente cuando dicha metadata exista.

        Ninguno de estos conceptos se deriva automáticamente de ActorId.
        """
        self._ensure_authorized(actor_id)
        self._validate_external_references(command)
        self._ensure_proposal_does_not_exist(command)

        proposal = Proposal.create(
            proposal_id=command.proposal_id,
            organization_id=command.organization_id,
            proposer_reference=command.proposer_reference,
            proposal_name=command.proposal_name,
            proposal_type=command.proposal_type,
            proposal_purpose=command.proposal_purpose,
            proposal_description=command.proposal_description,
            proposal_content=command.proposal_content,
            territory_id=command.territory_id,
            assembly_id=command.assembly_id,
        )

        self._repository.save(
            proposal,
            expected_version=None,
        )

        domain_events = proposal.pull_domain_events()

        self._domain_event_publisher.publish(domain_events)

        integration_events = self._map_integration_events(
            domain_events=domain_events,
            proposal=proposal,
            integration_event_id=integration_event_id,
            published_at=published_at,
            correlation_id=correlation_id,
            causation_id=causation_id,
        )

        if integration_events:
            self._integration_event_publisher.publish(integration_events)

        return self._to_result(proposal)

    def _ensure_authorized(
        self,
        actor_id: str,
    ) -> None:
        if not self._authorization.is_authorized(
            actor_id,
            self.CREATE_PERMISSION,
        ):
            raise PermissionError(
                "Actor is not authorized to create a Proposal."
            )

    def _validate_external_references(
        self,
        command: CreateProposal,
    ) -> None:
        self._reference_validation.validate_organization(
            command.organization_id
        )

        self._reference_validation.validate_proposer(
            command.proposer_reference,
            command.organization_id,
        )

        if command.territory_id is not None:
            self._reference_validation.validate_territory(
                command.territory_id
            )

        if command.assembly_id is not None:
            self._reference_validation.validate_assembly(
                command.assembly_id,
                command.organization_id,
            )

    def _ensure_proposal_does_not_exist(
        self,
        command: CreateProposal,
    ) -> None:
        if self._repository.exists(command.proposal_id):
            raise ValueError(
                f"Proposal already exists: {command.proposal_id}"
            )

    @staticmethod
    def _map_integration_events(
        *,
        domain_events: tuple[object, ...],
        proposal: Proposal,
        integration_event_id: str,
        published_at: datetime,
        correlation_id: str | None,
        causation_id: str | None,
    ) -> tuple[object, ...]:
        """
        Traduce únicamente hechos con contrato externo explícito en VS-001.

        ProposalCreated posee mapping normativo hacia:

            ProposalCreatedForIntegration

        El Mapper recibe:

        - EventId explícito;
        - PublishedAt explícito;
        - CorrelationId cuando exista;
        - CausationId cuando exista;
        - contexto confirmado de Proposal.

        No se genera ni infiere metadata dentro del Service.
        """
        integration_events: list[object] = []

        for domain_event in domain_events:
            if not isinstance(domain_event, ProposalCreated):
                continue

            integration_events.append(
                ProposalIntegrationEventMapper.from_proposal_created(
                    domain_event,
                    event_id=integration_event_id,
                    published_at=published_at,
                    proposer_reference=str(
                        proposal.proposer_reference
                    ),
                    territory_id=(
                        str(proposal.territory_id)
                        if proposal.territory_id is not None
                        else None
                    ),
                    assembly_id=(
                        str(proposal.assembly_id)
                        if proposal.assembly_id is not None
                        else None
                    ),
                    proposal_type=proposal.proposal_type.value,
                    proposal_status=proposal.status.value,
                    correlation_id=correlation_id,
                    causation_id=causation_id,
                )
            )

        return tuple(integration_events)

    @staticmethod
    def _to_result(
        proposal: Proposal,
    ) -> ProposalResult:
        return ProposalResult(
            proposal_id=proposal.proposal_id,
            organization_id=proposal.organization_id,
            proposer_reference=proposal.proposer_reference,
            proposal_name=proposal.proposal_name,
            proposal_type=proposal.proposal_type,
            proposal_status=proposal.status,
            version=proposal.version,
            territory_id=proposal.territory_id,
            assembly_id=proposal.assembly_id,
            submitted_at=(
                proposal.submitted_at.value
                if proposal.submitted_at is not None
                else None
            ),
        )