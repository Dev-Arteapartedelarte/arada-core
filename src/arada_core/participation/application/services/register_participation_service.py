from __future__ import annotations

from datetime import datetime

from arada_core.participation.application.commands.register_participation import (
    RegisterParticipation,
)
from arada_core.participation.application.dto.participation_result import (
    ParticipationResult,
)
from arada_core.participation.application.mappers.participation_integration_event_mapper import (
    ParticipationIntegrationEventMapper,
)
from arada_core.participation.application.ports.authorization_port import (
    AuthorizationPort,
)
from arada_core.participation.application.ports.domain_event_publisher import (
    DomainEventPublisher,
)
from arada_core.participation.application.ports.integration_event_publisher import (
    IntegrationEventPublisher,
)
from arada_core.participation.application.ports.participation_reference_validation_port import (
    ParticipationReferenceValidationPort,
)
from arada_core.participation.domain.aggregates.participation import Participation
from arada_core.participation.domain.events.participation_registered import (
    ParticipationRegistered,
)
from arada_core.participation.domain.repositories.participation_repository import (
    ParticipationRepository,
)


class RegisterParticipationService:
    """
    Application Service para el caso de uso RegisterParticipation.

    Responsabilidades:

    - comprobar autorización para ``Participation.Register``;
    - validar OrganizationId mediante el puerto correspondiente;
    - impedir el registro de una Participation con identidad ya existente;
    - delegar la creación del estado válido al Aggregate Participation;
    - persistir una única Participation;
    - publicar Domain Events únicamente después de persistencia exitosa;
    - traducir hechos explícitamente publicables a Integration Events;
    - publicar Integration Events únicamente después de persistencia exitosa;
    - devolver ParticipationResult y nunca el Aggregate.

    El Service no:

    - contiene reglas internas de Participation;
    - establece ParticipationStatus directamente;
    - incrementa ParticipationVersion directamente;
    - reproduce la State Machine;
    - modifica otros Aggregates;
    - ejecuta SQL;
    - conoce ORM;
    - conoce FIWARE;
    - conoce NGSI-LD;
    - conoce mecanismos concretos de mensajería;
    - implementa Transactional Outbox;
    - genera EventId;
    - inventa CorrelationId;
    - inventa CausationId.

    La metadata necesaria para producir el hecho se recibe explícitamente
    desde la frontera de invocación de Application.

    Flujo conceptual:

        RegisterParticipation
            |
            v
        Authorization
            |
            v
        Reference Validation
            |
            v
        Duplicate Identity Check
            |
            v
        Participation.register(...)
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

    VS-001 expresa únicamente el orden lógico disponible actualmente.

    La garantía técnica de atomicidad entre persistencia y publicación no se
    presupone en este Service y deberá resolverse posteriormente en
    Infrastructure mediante una decisión arquitectónica explícita.
    """

    REGISTER_PERMISSION = "Participation.Register"

    def __init__(
        self,
        *,
        repository: ParticipationRepository,
        authorization: AuthorizationPort,
        reference_validation: ParticipationReferenceValidationPort,
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
        command: RegisterParticipation,
        *,
        actor_id: str,
        created_at: datetime,
        event_id: str,
        correlation_id: str | None = None,
        causation_id: str | None = None,
    ) -> ParticipationResult:
        """
        Ejecuta RegisterParticipation dentro de Application.

        ``actor_id`` identifica al actor que intenta ejecutar el caso de uso
        y se utiliza para autorización y trazabilidad del hecho.

        ``created_at`` representa el instante de dominio en que la
        Participation es registrada.

        ``event_id`` identifica el hecho producido por el Aggregate.

        ``correlation_id`` y ``causation_id`` preservan metadata transversal
        únicamente cuando dicha metadata exista.

        Ninguno de estos valores es generado o inferido por este Service.
        """
        self._ensure_authorized(actor_id)
        self._validate_external_references(command)
        self._ensure_participation_does_not_exist(command)

        participation = Participation.register(
            participation_id=command.participation_id,
            organization_id=command.organization_id,
            participation_type=command.participation_type,
            created_at=created_at,
            event_id=event_id,
            actor_id=actor_id,
            correlation_id=correlation_id,
            causation_id=causation_id,
        )

        self._repository.save(
            participation,
            expected_version=None,
        )

        domain_events = participation.pull_domain_events()

        self._domain_event_publisher.publish(domain_events)

        integration_events = self._map_integration_events(
            domain_events=domain_events,
        )

        if integration_events:
            self._integration_event_publisher.publish(integration_events)

        return self._to_result(participation)

    def _ensure_authorized(
        self,
        actor_id: str,
    ) -> None:
        if not self._authorization.is_authorized(
            actor_id,
            self.REGISTER_PERMISSION,
        ):
            raise PermissionError(
                "Actor is not authorized to register a Participation."
            )

    def _validate_external_references(
        self,
        command: RegisterParticipation,
    ) -> None:
        self._reference_validation.validate_organization(
            command.organization_id,
        )

    def _ensure_participation_does_not_exist(
        self,
        command: RegisterParticipation,
    ) -> None:
        if self._repository.exists(command.participation_id):
            raise ValueError(
                f"Participation already exists: {command.participation_id}"
            )

    @staticmethod
    def _map_integration_events(
        *,
        domain_events: tuple[object, ...],
    ) -> tuple[object, ...]:
        """
        Traduce únicamente hechos con contrato externo explícito en VS-001.

        ParticipationRegistered posee mapping normativo hacia:

            ParticipationRegisteredIntegrationEvent

        Eventos distintos de ParticipationRegistered no son publicados desde
        este caso de uso.
        """
        mapper = ParticipationIntegrationEventMapper()
        integration_events: list[object] = []

        for domain_event in domain_events:
            if not isinstance(domain_event, ParticipationRegistered):
                continue

            integration_events.append(
                mapper.map(domain_event)
            )

        return tuple(integration_events)

    @staticmethod
    def _to_result(
        participation: Participation,
    ) -> ParticipationResult:
        return ParticipationResult(
            participation_id=participation.participation_id,
            organization_id=participation.organization_id,
            participation_type=participation.participation_type,
            status=participation.status,
            version=participation.version,
            created_at=participation.created_at,
            started_at=participation.started_at,
        )