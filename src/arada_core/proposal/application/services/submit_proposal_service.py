from datetime import datetime

from arada_core.proposal.application.commands.submit_proposal import SubmitProposal
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
from arada_core.proposal.domain.events.proposal_submitted import ProposalSubmitted
from arada_core.proposal.domain.repositories.proposal_repository import (
    ProposalRepository,
)
from arada_core.proposal.domain.value_objects.submitted_at import SubmittedAt


class SubmitProposalService:
    """
    Application Service para el caso de uso SubmitProposal.

    Responsabilidades:

    - comprobar autorización para ``proposal:submit``;
    - recuperar la Proposal existente;
    - validar referencias externas mediante puertos;
    - delegar la transición Draft -> Submitted al Aggregate Proposal;
    - persistir una única Proposal mediante control de versión;
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

        SubmitProposal
            |
            v
        Authorization
            |
            v
        ProposalRepository.get_by_id(...)
            |
            v
        External Reference Validation
            |
            v
        Proposal.submit(...)
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

    SUBMIT_PERMISSION = "proposal:submit"

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
        command: SubmitProposal,
        *,
        actor_id: str,
        submitted_at: SubmittedAt,
        integration_event_id: str,
        published_at: datetime,
        correlation_id: str | None = None,
        causation_id: str | None = None,
    ) -> ProposalResult:
        """
        Ejecuta SubmitProposal dentro de Application.

        ``actor_id`` se utiliza exclusivamente para autorización.

        ``submitted_at`` representa el instante de dominio en que la Proposal
        alcanza correctamente el estado Submitted.

        ``integration_event_id`` identifica el contrato público que será
        construido si ProposalSubmitted se confirma correctamente.

        ``published_at`` representa el instante de preparación/publicación
        contractual.

        ``correlation_id`` y ``causation_id`` preservan metadata transversal
        únicamente cuando dicha metadata exista.

        Ninguno de estos conceptos se deriva automáticamente de ActorId.
        """
        self._ensure_authorized(actor_id)

        proposal = self._get_proposal(command)
        self._validate_external_references(proposal)

        proposal.submit(
            submitted_at=submitted_at,
        )

        self._repository.save(
            proposal,
            expected_version=command.expected_version,
        )

        domain_events = proposal.pull_domain_events()

        self._domain_event_publisher.publish(domain_events)

        integration_events = self._map_integration_events(
            domain_events=domain_events,
            proposal=proposal,
            submitted_at=submitted_at,
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
            self.SUBMIT_PERMISSION,
        ):
            raise PermissionError(
                "Actor is not authorized to submit a Proposal."
            )

    def _get_proposal(
        self,
        command: SubmitProposal,
    ) -> Proposal:
        proposal = self._repository.get_by_id(command.proposal_id)

        if proposal is None:
            raise LookupError(
                f"Proposal not found: {command.proposal_id}"
            )

        return proposal

    def _validate_external_references(
        self,
        proposal: Proposal,
    ) -> None:
        self._reference_validation.validate_organization(
            proposal.organization_id
        )

        self._reference_validation.validate_proposer(
            proposal.proposer_reference,
            proposal.organization_id,
        )

        if proposal.territory_id is not None:
            self._reference_validation.validate_territory(
                proposal.territory_id
            )

        if proposal.assembly_id is not None:
            self._reference_validation.validate_assembly(
                proposal.assembly_id,
                proposal.organization_id,
            )

    @staticmethod
    def _map_integration_events(
        *,
        domain_events: tuple[object, ...],
        proposal: Proposal,
        submitted_at: SubmittedAt,
        integration_event_id: str,
        published_at: datetime,
        correlation_id: str | None,
        causation_id: str | None,
    ) -> tuple[object, ...]:
        """
        Traduce únicamente hechos con contrato externo explícito en VS-001.

        ProposalSubmitted posee mapping normativo hacia:

            ProposalSubmittedForIntegration

        El Mapper recibe:

        - EventId explícito;
        - PublishedAt explícito;
        - SubmittedAt confirmado por el dominio;
        - CorrelationId cuando exista;
        - CausationId cuando exista;
        - contexto confirmado de Proposal.

        No se genera ni infiere metadata dentro del Service.
        """
        integration_events: list[object] = []

        for domain_event in domain_events:
            if not isinstance(domain_event, ProposalSubmitted):
                continue

            integration_events.append(
                ProposalIntegrationEventMapper.from_proposal_submitted(
                    domain_event,
                    event_id=integration_event_id,
                    published_at=published_at,
                    submitted_at=submitted_at.value,
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