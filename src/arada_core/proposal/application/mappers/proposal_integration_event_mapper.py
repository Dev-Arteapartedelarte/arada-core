from datetime import datetime

from arada_core.proposal.application.integration_events.proposal_created_for_integration import (
    ProposalCreatedForIntegration,
)
from arada_core.proposal.application.integration_events.proposal_submitted_for_integration import (
    ProposalSubmittedForIntegration,
)
from arada_core.proposal.domain.events.proposal_created import ProposalCreated
from arada_core.proposal.domain.events.proposal_submitted import ProposalSubmitted


class ProposalIntegrationEventMapper:
    """
    Traduce Domain Events confirmados de Proposal a Integration Events.

    Este Mapper pertenece a Application porque transforma explícitamente:

        Domain Event
            +
        Confirmed Proposal Context
            +
        Integration Metadata
            ->
        Integration Event

    Para VS-001 soporta exclusivamente:

        ProposalCreated
            ->
        ProposalCreatedForIntegration

        ProposalSubmitted
            ->
        ProposalSubmittedForIntegration

    La transformación preserva:

        Domain Event
            !=
        Integration Event

    y:

        ActorId
            !=
        CorrelationId
            !=
        CausationId

    El Mapper:

    - no modifica Proposal;
    - no ejecuta comportamiento de dominio;
    - no reproduce invariantes;
    - no reproduce la State Machine;
    - no autoriza operaciones;
    - no persiste información;
    - no publica eventos;
    - no genera EventId;
    - no genera CorrelationId;
    - no genera CausationId;
    - no obtiene el tiempo actual;
    - no conoce Infrastructure;
    - no conoce brokers;
    - no conoce FIWARE;
    - no conoce NGSI-LD;
    - no implementa Transactional Outbox.

    EventId, PublishedAt, CorrelationId y CausationId son proporcionados
    explícitamente por el contexto de Application responsable de coordinar
    la publicación.

    Esto evita introducir en el Mapper decisiones físicas no consolidadas
    sobre:

    - generación de identificadores;
    - UUID;
    - clocks;
    - propagación de correlación;
    - propagación de causalidad.

    EventVersion pertenece al contrato de integración y permanece separado
    de ProposalVersion.
    """

    CREATED_EVENT_TYPE = "ProposalCreatedForIntegration"
    SUBMITTED_EVENT_TYPE = "ProposalSubmittedForIntegration"

    CREATED_EVENT_VERSION = 1
    SUBMITTED_EVENT_VERSION = 1

    @classmethod
    def from_proposal_created(
        cls,
        event: ProposalCreated,
        *,
        event_id: str,
        published_at: datetime,
        proposer_reference: str,
        territory_id: str | None,
        assembly_id: str | None,
        proposal_type: str,
        proposal_status: str,
        correlation_id: str | None,
        causation_id: str | None,
    ) -> ProposalCreatedForIntegration:
        """
        Construye ProposalCreatedForIntegration desde un ProposalCreated
        confirmado y el contexto necesario de Application.

        DOMAIN-007K exige para este contrato:

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

        Los datos que no pertenecen al Domain Event se reciben
        explícitamente. El Mapper no los inventa ni los consulta.
        """
        cls._validate_event_id(event_id)
        cls._validate_publication_time(
            occurred_at=event.occurred_at,
            published_at=published_at,
        )
        cls._validate_optional_identifier(
            "correlation_id",
            correlation_id,
        )
        cls._validate_optional_identifier(
            "causation_id",
            causation_id,
        )

        return ProposalCreatedForIntegration(
            event_id=event_id,
            event_type=cls.CREATED_EVENT_TYPE,
            event_version=cls.CREATED_EVENT_VERSION,
            occurred_at=event.occurred_at,
            published_at=published_at,
            proposal_id=str(event.proposal_id),
            organization_id=str(event.organization_id),
            proposer_reference=proposer_reference,
            territory_id=territory_id,
            assembly_id=assembly_id,
            proposal_type=proposal_type,
            proposal_status=proposal_status,
            proposal_version=event.version.value,
            correlation_id=correlation_id,
            causation_id=causation_id,
        )

    @classmethod
    def from_proposal_submitted(
        cls,
        event: ProposalSubmitted,
        *,
        event_id: str,
        published_at: datetime,
        proposer_reference: str,
        territory_id: str | None,
        assembly_id: str | None,
        proposal_type: str,
        proposal_status: str,
        submitted_at: datetime,
        correlation_id: str | None,
        causation_id: str | None,
    ) -> ProposalSubmittedForIntegration:
        """
        Construye ProposalSubmittedForIntegration desde un
        ProposalSubmitted confirmado y el contexto necesario de Application.

        DOMAIN-007K exige para este contrato:

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
            SubmittedAt
            ProposalVersion
            CorrelationId
            CausationId

        En particular, el contrato Submitted debe conservar:

        - ProposerReference;
        - TerritoryId cuando corresponda;
        - AssemblyId cuando corresponda;
        - ProposalType.

        Estos campos no pueden omitirse del mapping por no existir
        directamente dentro de ProposalSubmitted. Se obtienen del estado
        confirmado de Proposal coordinado por Application.
        """
        cls._validate_event_id(event_id)
        cls._validate_publication_time(
            occurred_at=event.occurred_at,
            published_at=published_at,
        )
        cls._validate_datetime(
            "submitted_at",
            submitted_at,
        )
        cls._validate_optional_identifier(
            "correlation_id",
            correlation_id,
        )
        cls._validate_optional_identifier(
            "causation_id",
            causation_id,
        )

        return ProposalSubmittedForIntegration(
            event_id=event_id,
            event_type=cls.SUBMITTED_EVENT_TYPE,
            event_version=cls.SUBMITTED_EVENT_VERSION,
            occurred_at=event.occurred_at,
            published_at=published_at,
            proposal_id=str(event.proposal_id),
            organization_id=str(event.organization_id),
            proposer_reference=proposer_reference,
            territory_id=territory_id,
            assembly_id=assembly_id,
            proposal_type=proposal_type,
            proposal_status=proposal_status,
            submitted_at=submitted_at,
            proposal_version=event.version.value,
            correlation_id=correlation_id,
            causation_id=causation_id,
        )

    @staticmethod
    def _validate_event_id(
        event_id: str,
    ) -> None:
        """
        Exige una identidad explícita para el Integration Event.

        La estrategia concreta de generación de EventId no pertenece al
        Mapper.
        """
        if not isinstance(event_id, str) or not event_id.strip():
            raise ValueError(
                "event_id must not be empty."
            )

    @staticmethod
    def _validate_publication_time(
        *,
        occurred_at: datetime,
        published_at: datetime,
    ) -> None:
        """
        Protege la relación temporal entre el hecho y su publicación.

        OccurredAt representa el hecho de dominio.
        PublishedAt representa la preparación/publicación contractual
        posterior del hecho confirmado.
        """
        ProposalIntegrationEventMapper._validate_datetime(
            "published_at",
            published_at,
        )

        if published_at < occurred_at:
            raise ValueError(
                "PublishedAt must not precede OccurredAt."
            )

    @staticmethod
    def _validate_datetime(
        field_name: str,
        value: datetime,
    ) -> None:
        if not isinstance(value, datetime):
            raise TypeError(
                f"{field_name} must be a datetime."
            )

    @staticmethod
    def _validate_optional_identifier(
        field_name: str,
        value: str | None,
    ) -> None:
        """
        Permite ausencia de metadata transversal cuando todavía no exista,
        pero rechaza una representación presente y vacía.
        """
        if value is None:
            return

        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{field_name} must not be empty when provided."
            )