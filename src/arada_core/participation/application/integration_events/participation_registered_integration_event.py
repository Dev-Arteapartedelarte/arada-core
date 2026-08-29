from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from arada_core.participation.domain.value_objects.organization_id import OrganizationId
from arada_core.participation.domain.value_objects.participation_id import (
    ParticipationId,
)
from arada_core.participation.domain.value_objects.participation_type import (
    ParticipationType,
)
from arada_core.participation.domain.value_objects.participation_version import (
    ParticipationVersion,
)


@dataclass(frozen=True, slots=True)
class ParticipationRegisteredIntegrationEvent:
    """
    Contrato público de integración para una Participation registrada.

    Este Integration Event:

    - representa un hecho de dominio ya confirmado;
    - deriva explícitamente de ParticipationRegistered;
    - es inmutable;
    - no expone la Aggregate Root;
    - no contiene lógica de negocio;
    - no modifica otros Aggregates;
    - mantiene EventVersion separado de AggregateVersion;
    - conserva identidad, correlación y causalidad;
    - no incorpora PublishedAt porque no forma parte del contrato
      propietario de DOMAIN-008.
    """

    event_id: str
    event_type: str
    event_version: int
    aggregate_id: ParticipationId
    aggregate_type: str
    aggregate_version: ParticipationVersion
    occurred_at: datetime
    correlation_id: str | None
    causation_id: str | None
    organization_id: OrganizationId
    participation_type: ParticipationType