from datetime import UTC, datetime

from arada_core.proposal.domain.events.proposal_created import ProposalCreated
from arada_core.proposal.domain.events.proposal_submitted import ProposalSubmitted
from arada_core.proposal.domain.value_objects.assembly_id import AssemblyId
from arada_core.proposal.domain.value_objects.organization_id import OrganizationId
from arada_core.proposal.domain.value_objects.proposal_content import ProposalContent
from arada_core.proposal.domain.value_objects.proposal_description import (
    ProposalDescription,
)
from arada_core.proposal.domain.value_objects.proposal_id import ProposalId
from arada_core.proposal.domain.value_objects.proposal_name import ProposalName
from arada_core.proposal.domain.value_objects.proposal_purpose import ProposalPurpose
from arada_core.proposal.domain.value_objects.proposal_status import ProposalStatus
from arada_core.proposal.domain.value_objects.proposal_type import ProposalType
from arada_core.proposal.domain.value_objects.proposal_version import ProposalVersion
from arada_core.proposal.domain.value_objects.proposer_reference import (
    ProposerReference,
)
from arada_core.proposal.domain.value_objects.submitted_at import SubmittedAt
from arada_core.proposal.domain.value_objects.territory_id import TerritoryId


class Proposal:
    """
    Aggregate Root del Bounded Context Proposal.

    Proposal constituye la frontera autoritativa de consistencia para las
    reglas, estado y transiciones de una iniciativa dentro de AURA Core.

    Para VS-001 protege exclusivamente el flujo:

        Nonexistent
            |
            | create(...)
            v
        Draft
            |
            | submit(...)
            v
        Submitted

    Responsabilidades del Aggregate:

    - preservar ProposalId durante todo el Lifecycle;
    - preservar OrganizationId durante todo el Lifecycle;
    - mantener referencias externas sin absorber otros Aggregates;
    - controlar ProposalStatus;
    - ejecutar únicamente transiciones válidas;
    - incrementar Version como consecuencia de modificaciones válidas;
    - producir Domain Events después de comportamiento válido;
    - impedir que operaciones inválidas alteren estado, Version o eventos.

    Proposal no:

    - ejecuta autorización;
    - consulta otros Bounded Contexts;
    - persiste su propio estado;
    - conoce Repository implementations;
    - publica Integration Events;
    - depende de Infrastructure;
    - depende de FIWARE, NGSI-LD o mecanismos de transporte.

    La creación se realiza mediante el factory method ``create`` para impedir
    la construcción pública de estados que no hayan atravesado las reglas del
    Aggregate.

    La reconstitución desde persistencia podrá incorporarse cuando exista una
    necesidad concreta de Infrastructure. VS-001 no introduce anticipadamente
    una API de rehidratación no requerida.
    """

    def __init__(
        self,
        *,
        proposal_id: ProposalId,
        organization_id: OrganizationId,
        proposer_reference: ProposerReference,
        proposal_name: ProposalName,
        proposal_type: ProposalType,
        proposal_purpose: ProposalPurpose | None,
        proposal_description: ProposalDescription | None,
        proposal_content: ProposalContent | None,
        territory_id: TerritoryId | None,
        assembly_id: AssemblyId | None,
        status: ProposalStatus,
        version: ProposalVersion,
        submitted_at: SubmittedAt | None,
    ) -> None:
        self._proposal_id = proposal_id
        self._organization_id = organization_id
        self._proposer_reference = proposer_reference
        self._proposal_name = proposal_name
        self._proposal_type = proposal_type
        self._proposal_purpose = proposal_purpose
        self._proposal_description = proposal_description
        self._proposal_content = proposal_content
        self._territory_id = territory_id
        self._assembly_id = assembly_id
        self._status = status
        self._version = version
        self._submitted_at = submitted_at
        self._domain_events: list[object] = []

    @classmethod
    def create(
        cls,
        *,
        proposal_id: ProposalId,
        organization_id: OrganizationId,
        proposer_reference: ProposerReference,
        proposal_name: ProposalName,
        proposal_type: ProposalType,
        proposal_purpose: ProposalPurpose | None = None,
        proposal_description: ProposalDescription | None = None,
        proposal_content: ProposalContent | None = None,
        territory_id: TerritoryId | None = None,
        assembly_id: AssemblyId | None = None,
    ) -> "Proposal":
        """
        Crea una Proposal válida en estado Draft.

        Una creación válida:

        - establece Draft como estado inicial;
        - establece Version en 1;
        - preserva las referencias recibidas;
        - produce exactamente un ProposalCreated;
        - no modifica otros Aggregates.

        Las verificaciones que requieren consultar fuentes autoritativas
        externas deben haber sido coordinadas por Application antes de
        invocar este comportamiento.
        """
        proposal = cls(
            proposal_id=proposal_id,
            organization_id=organization_id,
            proposer_reference=proposer_reference,
            proposal_name=proposal_name,
            proposal_type=proposal_type,
            proposal_purpose=proposal_purpose,
            proposal_description=proposal_description,
            proposal_content=proposal_content,
            territory_id=territory_id,
            assembly_id=assembly_id,
            status=ProposalStatus.DRAFT,
            version=ProposalVersion(1),
            submitted_at=None,
        )

        proposal._record_domain_event(
            ProposalCreated(
                proposal_id=proposal.proposal_id,
                organization_id=proposal.organization_id,
                proposal_name=proposal.proposal_name,
                proposal_type=proposal.proposal_type,
                occurred_at=datetime.now(UTC),
                version=proposal.version,
            )
        )

        return proposal

    def submit(self, *, submitted_at: SubmittedAt) -> None:
        """
        Presenta formalmente la Proposal.

        VS-001 permite exclusivamente:

            Draft -> Submitted

        Una presentación válida:

        - cambia ProposalStatus a Submitted;
        - registra SubmittedAt;
        - incrementa Version exactamente una vez;
        - produce exactamente un ProposalSubmitted.

        Una operación inválida debe fallar antes de modificar el estado,
        Version, SubmittedAt o la colección de Domain Events.
        """
        self._ensure_can_submit()

        next_version = self._version.next()

        self._status = ProposalStatus.SUBMITTED
        self._submitted_at = submitted_at
        self._version = next_version

        self._record_domain_event(
            ProposalSubmitted(
                proposal_id=self.proposal_id,
                organization_id=self.organization_id,
                occurred_at=submitted_at.value,
                version=self.version,
            )
        )

    def _ensure_can_submit(self) -> None:
        """
        Protege la transición Draft -> Submitted.

        La State Machine pertenece al Aggregate. Application no debe repetir
        esta decisión.
        """
        if self._status is not ProposalStatus.DRAFT:
            raise ValueError(
                "Proposal can only be submitted from Draft status."
            )

    def _record_domain_event(self, event: object) -> None:
        """
        Registra internamente un hecho producido por comportamiento válido.

        El registro no publica el evento ni ejecuta efectos externos.
        """
        self._domain_events.append(event)

    def pull_domain_events(self) -> tuple[object, ...]:
        """
        Extrae los Domain Events pendientes respetando su orden de producción.

        La extracción vacía la colección interna para evitar que el mismo
        Aggregate entregue repetidamente los mismos eventos dentro de una
        misma instancia en memoria.

        La publicación efectiva pertenece a Application mediante el Port
        correspondiente.
        """
        events = tuple(self._domain_events)
        self._domain_events.clear()
        return events

    @property
    def proposal_id(self) -> ProposalId:
        """Identidad inmutable del Aggregate."""
        return self._proposal_id

    @property
    def organization_id(self) -> OrganizationId:
        """Organization propietaria de la Proposal."""
        return self._organization_id

    @property
    def proposer_reference(self) -> ProposerReference:
        """Referencia de dominio al proponente."""
        return self._proposer_reference

    @property
    def proposal_name(self) -> ProposalName:
        """Nombre canónico de la Proposal."""
        return self._proposal_name

    @property
    def proposal_type(self) -> ProposalType:
        """Tipo de la Proposal."""
        return self._proposal_type

    @property
    def proposal_purpose(self) -> ProposalPurpose | None:
        """Propósito formal cuando forma parte de la Proposal."""
        return self._proposal_purpose

    @property
    def proposal_description(self) -> ProposalDescription | None:
        """Descripción formal cuando forma parte de la Proposal."""
        return self._proposal_description

    @property
    def proposal_content(self) -> ProposalContent | None:
        """Contenido propio cuando forma parte de la Proposal."""
        return self._proposal_content

    @property
    def territory_id(self) -> TerritoryId | None:
        """Referencia territorial contextual cuando existe."""
        return self._territory_id

    @property
    def assembly_id(self) -> AssemblyId | None:
        """Referencia contextual a Assembly cuando existe."""
        return self._assembly_id

    @property
    def status(self) -> ProposalStatus:
        """Estado actual controlado por el Aggregate."""
        return self._status

    @property
    def version(self) -> ProposalVersion:
        """Versión lógica actual del Aggregate."""
        return self._version

    @property
    def submitted_at(self) -> SubmittedAt | None:
        """Momento de presentación cuando la transición ya ocurrió."""
        return self._submitted_at