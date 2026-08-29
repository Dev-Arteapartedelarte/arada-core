from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from arada_core.participation.domain.value_objects.organization_id import OrganizationId
from arada_core.participation.domain.value_objects.participation_id import (
    ParticipationId,
)
from arada_core.participation.domain.value_objects.participation_version import (
    ParticipationVersion,
)


@dataclass(frozen=True, slots=True)
class ParticipationActivated:
    """Hecho de dominio que representa la activación válida de una Participation."""

    event_id: str
    participation_id: ParticipationId
    organization_id: OrganizationId
    started_at: datetime
    occurred_at: datetime
    aggregate_version: ParticipationVersion
    actor_id: str
    correlation_id: str | None = None
    causation_id: str | None = None