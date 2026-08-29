from dataclasses import dataclass

from arada_core.participation.domain.value_objects.organization_id import OrganizationId
from arada_core.participation.domain.value_objects.participation_id import (
    ParticipationId,
)
from arada_core.participation.domain.value_objects.participation_version import (
    ParticipationVersion,
)


@dataclass(frozen=True, slots=True)
class ActivateParticipation:
    """
    Intención de activar una Participation previamente registrada.

    ActivateParticipation:

    - identifica la Participation objetivo;
    - identifica su contexto organizacional;
    - transporta ExpectedVersion para concurrencia optimista;
    - no decide si la transición Registered -> Active es válida;
    - no modifica ParticipationStatus;
    - no incrementa ParticipationVersion;
    - no establece StartedAt;
    - no produce ParticipationActivated;
    - no persiste el Aggregate;
    - no contiene lógica de autorización;
    - no depende de Infrastructure.

    La validez de la transición pertenece exclusivamente al Aggregate
    Participation.

    Application debe coordinar autorización, carga del Aggregate,
    validaciones externas necesarias y persistencia utilizando
    expected_version.
    """

    participation_id: ParticipationId
    organization_id: OrganizationId
    expected_version: ParticipationVersion