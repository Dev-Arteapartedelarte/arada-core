from __future__ import annotations

from arada_core.participation.application.integration_events.participation_activated_integration_event import (
    ParticipationActivatedIntegrationEvent,
)
from arada_core.participation.application.integration_events.participation_registered_integration_event import (
    ParticipationRegisteredIntegrationEvent,
)
from arada_core.participation.domain.events.participation_activated import (
    ParticipationActivated,
)
from arada_core.participation.domain.events.participation_registered import (
    ParticipationRegistered,
)


class ParticipationIntegrationEventMapper:
    """
    Mapper explícito entre Domain Events e Integration Events de Participation.

    VS-001 soporta únicamente:

        ParticipationRegistered
            ->
        ParticipationRegisteredIntegrationEvent

        ParticipationActivated
            ->
        ParticipationActivatedIntegrationEvent

    El mapper:

    - no genera EventId;
    - no genera CorrelationId;
    - no genera CausationId;
    - no genera timestamps;
    - no modifica AggregateVersion;
    - no inventa PublishedAt;
    - no transforma eventos no soportados;
    - mantiene EventVersion separado de AggregateVersion;
    - mantiene explícito el contrato público de integración.
    """

    REGISTERED_EVENT_TYPE = "ParticipationRegisteredIntegrationEvent"
    ACTIVATED_EVENT_TYPE = "ParticipationActivatedIntegrationEvent"
    EVENT_VERSION = 1
    AGGREGATE_TYPE = "Participation"

    def map(
        self,
        event: object,
    ) -> object:
        """
        Transforma un Domain Event soportado en su Integration Event oficial.

        Los eventos desconocidos son rechazados explícitamente para evitar
        publicación automática de hechos no declarados por DOMAIN-008K.
        """

        if isinstance(event, ParticipationRegistered):
            return self._map_registered(event)

        if isinstance(event, ParticipationActivated):
            return self._map_activated(event)

        raise TypeError(
            "Unsupported Participation domain event for integration mapping: "
            f"{type(event).__name__}."
        )

    def _map_registered(
        self,
        event: ParticipationRegistered,
    ) -> ParticipationRegisteredIntegrationEvent:
        return ParticipationRegisteredIntegrationEvent(
            event_id=event.event_id,
            event_type=self.REGISTERED_EVENT_TYPE,
            event_version=self.EVENT_VERSION,
            aggregate_id=event.participation_id,
            aggregate_type=self.AGGREGATE_TYPE,
            aggregate_version=event.aggregate_version,
            occurred_at=event.occurred_at,
            correlation_id=event.correlation_id,
            causation_id=event.causation_id,
            organization_id=event.organization_id,
            participation_type=event.participation_type,
        )

    def _map_activated(
        self,
        event: ParticipationActivated,
    ) -> ParticipationActivatedIntegrationEvent:
        return ParticipationActivatedIntegrationEvent(
            event_id=event.event_id,
            event_type=self.ACTIVATED_EVENT_TYPE,
            event_version=self.EVENT_VERSION,
            aggregate_id=event.participation_id,
            aggregate_type=self.AGGREGATE_TYPE,
            aggregate_version=event.aggregate_version,
            occurred_at=event.occurred_at,
            correlation_id=event.correlation_id,
            causation_id=event.causation_id,
            organization_id=event.organization_id,
        )