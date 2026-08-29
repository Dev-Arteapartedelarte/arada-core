from dataclasses import dataclass

from arada_core.participation.domain.value_objects.organization_id import OrganizationId
from arada_core.participation.domain.value_objects.participation_id import (
    ParticipationId,
)
from arada_core.participation.domain.value_objects.participation_type import (
    ParticipationType,
)


@dataclass(frozen=True, slots=True)
class RegisterParticipation:
    """
    Intención de registrar una nueva Participation.

    RegisterParticipation transporta exclusivamente los datos requeridos por
    el caso de uso de registro dentro de VS-001.

    El Command:

    - expresa intención y no un hecho consumado;
    - identifica la nueva Participation mediante ParticipationId;
    - establece su contexto organizacional mediante OrganizationId;
    - declara el ParticipationType correspondiente;
    - no decide si el registro está autorizado;
    - no verifica existencia de Aggregates externos;
    - no persiste información;
    - no establece ParticipationStatus;
    - no establece ParticipationVersion;
    - no establece CreatedAt;
    - no produce ParticipationRegistered;
    - no contiene lógica de dominio;
    - no depende de Infrastructure.

    Application debe resolver previamente la autorización y las validaciones
    externas necesarias y posteriormente delegar el registro válido al
    Aggregate Participation.

    Las referencias adicionales de actor participante o contexto no se
    incorporan en VS-001 mientras el modelo documental no establezca una
    cardinalidad concreta que deba ser representada por este Command.
    """

    participation_id: ParticipationId
    organization_id: OrganizationId
    participation_type: ParticipationType