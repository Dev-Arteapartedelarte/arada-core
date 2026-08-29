from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from arada_core.participation.domain.value_objects.organization_id import OrganizationId
from arada_core.participation.domain.value_objects.participation_id import (
    ParticipationId,
)
from arada_core.participation.domain.value_objects.participation_status import (
    ParticipationStatus,
)
from arada_core.participation.domain.value_objects.participation_type import (
    ParticipationType,
)
from arada_core.participation.domain.value_objects.participation_version import (
    ParticipationVersion,
)


@dataclass(frozen=True, slots=True)
class ParticipationResult:
    """
    Resultado estable expuesto por los casos de uso de Participation.

    Este DTO pertenece a Application y evita exponer la Aggregate Root
    directamente hacia consumidores externos.

    ParticipationResult:

    - representa el estado confirmado después de ejecutar un caso de uso;
    - no contiene comportamiento de dominio;
    - no permite modificar Participation;
    - no sustituye al Aggregate;
    - no contiene Domain Events;
    - no contiene Integration Events;
    - no contiene dependencias de Infrastructure.
    """

    participation_id: ParticipationId
    organization_id: OrganizationId
    participation_type: ParticipationType
    status: ParticipationStatus
    version: ParticipationVersion
    created_at: datetime
    started_at: datetime | None