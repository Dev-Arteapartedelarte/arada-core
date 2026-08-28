from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class ProposalCreatedForIntegration:
    """
    Contrato de integración derivado del hecho confirmado ProposalCreated.

    Fuente normativa:
        DOMAIN-007K-Integration-Events.md

    Payload conceptual:

        EventId
        EventType
        EventVersion
        OccurredAt
        PublishedAt
        ProposalId
        OrganizationId
        ProposerReference
        TerritoryId
        AssemblyId
        ProposalType
        ProposalStatus
        ProposalVersion
        CorrelationId
        CausationId

    Separaciones obligatorias:

        Domain Event
            !=
        Integration Event

        EventId
            !=
        ProposalId

        EventVersion
            !=
        ProposalVersion

        ActorId
            !=
        CorrelationId
            !=
        CausationId

    Responsabilidad de los metadatos:

    - EventId identifica exclusivamente este contrato publicado.
    - EventType identifica semánticamente el contrato.
    - EventVersion representa la versión del contrato de integración.
    - OccurredAt representa cuándo ocurrió el hecho de dominio.
    - PublishedAt representa cuándo el hecho confirmado fue preparado para
      publicación externa.
    - CorrelationId identifica, cuando exista, el flujo distribuido al que
      pertenece la operación.
    - CausationId identifica, cuando exista, la causa inmediata del hecho.

    Este objeto NO genera por sí mismo:

    - EventId;
    - CorrelationId;
    - CausationId;
    - PublishedAt.

    Dichos valores deben ser suministrados explícitamente por el contexto de
    Application que coordina la publicación.

    Esta decisión evita que el contrato:

    - invente causalidad;
    - confunda ActorId con metadata de trazabilidad;
    - dependa de una estrategia concreta de UUID;
    - dependa de un clock global oculto;
    - introduzca decisiones de Infrastructure en Application.

    TerritoryId y AssemblyId son referencias contextuales opcionales.

    CorrelationId y CausationId pueden no existir cuando el flujo confirmado
    todavía no dispone de metadata transversal correspondiente. Cuando
    existan, deben conservar su significado independiente.

    El contrato permanece independiente de:

    - Infrastructure;
    - mecanismos de transporte;
    - brokers;
    - persistencia;
    - FIWARE;
    - NGSI-LD;
    - representación serializada concreta.
    """

    event_id: str
    event_type: str
    event_version: int
    occurred_at: datetime
    published_at: datetime
    proposal_id: str
    organization_id: str
    proposer_reference: str
    territory_id: str | None
    assembly_id: str | None
    proposal_type: str
    proposal_status: str
    proposal_version: int
    correlation_id: str | None
    causation_id: str | None

    def __post_init__(self) -> None:
        """
        Valida únicamente coherencia estructural del contrato.

        Las reglas de negocio de Proposal permanecen exclusivamente en
        Domain. Este contrato no reproduce invariantes ni State Machine.
        """
        self._require_non_empty("event_id", self.event_id)
        self._require_non_empty("event_type", self.event_type)
        self._require_non_empty("proposal_id", self.proposal_id)
        self._require_non_empty("organization_id", self.organization_id)
        self._require_non_empty(
            "proposer_reference",
            self.proposer_reference,
        )
        self._require_non_empty("proposal_type", self.proposal_type)
        self._require_non_empty(
            "proposal_status",
            self.proposal_status,
        )

        self._require_positive_integer(
            "event_version",
            self.event_version,
        )
        self._require_positive_integer(
            "proposal_version",
            self.proposal_version,
        )

        self._require_datetime(
            "occurred_at",
            self.occurred_at,
        )
        self._require_datetime(
            "published_at",
            self.published_at,
        )

        if self.published_at < self.occurred_at:
            raise ValueError(
                "PublishedAt must not precede OccurredAt."
            )

        self._validate_optional_identifier(
            "territory_id",
            self.territory_id,
        )
        self._validate_optional_identifier(
            "assembly_id",
            self.assembly_id,
        )
        self._validate_optional_identifier(
            "correlation_id",
            self.correlation_id,
        )
        self._validate_optional_identifier(
            "causation_id",
            self.causation_id,
        )

    @staticmethod
    def _require_non_empty(
        field_name: str,
        value: str,
    ) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{field_name} must not be empty."
            )

    @staticmethod
    def _require_positive_integer(
        field_name: str,
        value: int,
    ) -> None:
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or value < 1
        ):
            raise ValueError(
                f"{field_name} must be a positive integer."
            )

    @staticmethod
    def _require_datetime(
        field_name: str,
        value: datetime,
    ) -> None:
        if not isinstance(value, datetime):
            raise TypeError(
                f"{field_name} must be a datetime."
            )

    @classmethod
    def _validate_optional_identifier(
        cls,
        field_name: str,
        value: str | None,
    ) -> None:
        if value is None:
            return

        cls._require_non_empty(
            field_name,
            value,
        )