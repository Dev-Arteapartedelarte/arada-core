from __future__ import annotations

from datetime import datetime

from arada_core.participation.application.commands.activate_participation import (
    ActivateParticipation,
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
from arada_core.participation.domain.events.participation_activated import (
    ParticipationActivated,
)
from arada_core.participation.domain.repositories.participation_repository import (
    ParticipationRepository,
)


class ActivateParticipationService:
    """
    Application Service para el caso de uso ActivateParticipation.

    Responsabilidades:

    - comprobar autorización para ``Participation.Activate``;
    - cargar la Participation objetivo;
    - verificar que OrganizationId corresponda al Aggregate cargado;
    - validar la referencia organizacional mediante el puerto correspondiente;
    - delegar la transición Registered -> Active al Aggregate;
    - persistir utilizando expected_version;
    - publicar Domain Events únicamente después de persistencia exitosa;
    - traducir hechos explícitamente publicables a Integration Events;
    - publicar Integration Events únicamente después de persistencia exitosa;
    - devolver ParticipationResult y nunca la Aggregate Root.

    El Service no:

    - decide la State Machine;
    - modifica ParticipationStatus directamente;
    - establece StartedAt directamente;
    - incrementa ParticipationVersion directamente;
    - contiene invariantes del Aggregate;
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

        ActivateParticipation
            |
            v
        Authorization
            |
            v
        Repository.get_by_id(...)
            |
            v
        Organization Validation
            |
            v
        External Reference Validation
            |
            v
        Participation.activate(...)
            |
            v
        Repository.save(... expected_version)
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

    ACTIVATE_PERMISSION = "Participation.Activate"

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
        command: ActivateParticipation,
        *,
        actor_id: str,
        started_at: datetime,
        event_id: str,
        correlation_id: str | None = None,
        causation_id: str | None = None,
    ) -> ParticipationResult:
        """
        Ejecuta ActivateParticipation dentro de Application.

        ``actor_id`` identifica al actor que intenta ejecutar el caso de uso
        y se utiliza para autorización y trazabilidad del hecho.

        ``started_at`` representa el instante de dominio en que la
        Participation comienza formalmente.

        ``event_id`` identifica el hecho producido por el Aggregate.

        ``correlation_id`` y ``causation_id`` preservan metadata transversal
        únicamente cuando dicha metadata exista.

        Ninguno de estos valores es generado o inferido por este Service.
        """
        self._ensure_authorized(actor_id)

        participation = self._get_participation(command)

        self._ensure_organization_matches(
            participation=participation,
            command=command,
        )

        self._reference_validation.validate_organization(
            command.organization_id,
        )

        participation.activate(
            started_at=started_at,
            event_id=event_id,
            actor_id=actor_id,
            correlation_id=correlation_id,
            causation_id=causation_id,
        )

        self._repository.save(
            participation,
            expected_version=command.expected_version,
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
            self.ACTIVATE_PERMISSION,
        ):
            raise PermissionError(
                "Actor is not authorized to activate a Participation."
            )

    def _get_participation(
        self,
        command: ActivateParticipation,
    ) -> Participation:
        participation = self._repository.get_by_id(
            command.participation_id,
        )

        if participation is None:
            raise LookupError(
                f"Participation not found: {command.participation_id}"
            )

        return participation

    @staticmethod
    def _ensure_organization_matches(
        *,
        participation: Participation,
        command: ActivateParticipation,
    ) -> None:
        if participation.organization_id != command.organization_id:
            raise ValueError(
                "OrganizationId does not match the Participation aggregate."
            )

    @staticmethod
    def _map_integration_events(
        *,
        domain_events: tuple[object, ...],
    ) -> tuple[object, ...]:
        """
        Traduce únicamente hechos con contrato externo explícito en VS-001.

        ParticipationActivated posee mapping normativo hacia:

            ParticipationActivatedIntegrationEvent

        Eventos distintos de ParticipationActivated no son publicados desde
        este caso de uso.
        """
        mapper = ParticipationIntegrationEventMapper()
        integration_events: list[object] = []

        for domain_event in domain_events:
            if not isinstance(domain_event, ParticipationActivated):
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