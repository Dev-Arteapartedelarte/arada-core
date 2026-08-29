from __future__ import annotations

from datetime import UTC, datetime

import pytest

from arada_core.participation.application.commands.register_participation import (
    RegisterParticipation,
)
from arada_core.participation.application.integration_events.participation_registered_integration_event import (
    ParticipationRegisteredIntegrationEvent,
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
from arada_core.participation.application.services.register_participation_service import (
    RegisterParticipationService,
)
from arada_core.participation.domain.aggregates.participation import Participation
from arada_core.participation.domain.events.participation_registered import (
    ParticipationRegistered,
)
from arada_core.participation.domain.repositories.participation_repository import (
    ParticipationRepository,
)
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


class InMemoryParticipationRepository(ParticipationRepository):
    def __init__(self) -> None:
        self._participations: dict[ParticipationId, Participation] = {}
        self.saved_expected_versions: list[ParticipationVersion | None] = []

    def get_by_id(
        self,
        participation_id: ParticipationId,
    ) -> Participation | None:
        return self._participations.get(participation_id)

    def exists(
        self,
        participation_id: ParticipationId,
    ) -> bool:
        return participation_id in self._participations

    def save(
        self,
        participation: Participation,
        expected_version: ParticipationVersion | None,
    ) -> None:
        participation_id = participation.participation_id

        if expected_version is None:
            if participation_id in self._participations:
                raise ValueError(
                    f"Participation already exists: {participation_id}"
                )

            self._participations[participation_id] = participation
            self.saved_expected_versions.append(expected_version)
            return

        persisted = self._participations.get(participation_id)

        if persisted is None:
            raise LookupError(
                f"Participation not found: {participation_id}"
            )

        if persisted.version != expected_version:
            raise ValueError(
                "Participation version conflict."
            )

        self._participations[participation_id] = participation
        self.saved_expected_versions.append(expected_version)


class StubAuthorizationPort(AuthorizationPort):
    def __init__(self, *, authorized: bool = True) -> None:
        self.authorized = authorized
        self.calls: list[tuple[str, str]] = []

    def is_authorized(
        self,
        actor_id: str,
        permission: str,
    ) -> bool:
        self.calls.append((actor_id, permission))
        return self.authorized


class StubParticipationReferenceValidationPort(
    ParticipationReferenceValidationPort
):
    def __init__(self, *, should_fail: bool = False) -> None:
        self.should_fail = should_fail
        self.validated_organizations: list[OrganizationId] = []

    def validate_organization(
        self,
        organization_id: OrganizationId,
    ) -> None:
        self.validated_organizations.append(organization_id)

        if self.should_fail:
            raise ValueError(
                "Organization reference is invalid."
            )


class RecordingDomainEventPublisher(DomainEventPublisher):
    def __init__(self) -> None:
        self.published_events: list[object] = []

    def publish(
        self,
        events: tuple[object, ...],
    ) -> None:
        self.published_events.extend(events)


class RecordingIntegrationEventPublisher(IntegrationEventPublisher):
    def __init__(self) -> None:
        self.published_events: list[object] = []

    def publish(
        self,
        events: tuple[object, ...],
    ) -> None:
        self.published_events.extend(events)


def _command() -> RegisterParticipation:
    return RegisterParticipation(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.ATTENDANCE,
    )


def _build_service(
    *,
    repository: InMemoryParticipationRepository | None = None,
    authorization: StubAuthorizationPort | None = None,
    reference_validation: StubParticipationReferenceValidationPort | None = None,
    domain_event_publisher: RecordingDomainEventPublisher | None = None,
    integration_event_publisher: RecordingIntegrationEventPublisher | None = None,
) -> tuple[
    RegisterParticipationService,
    InMemoryParticipationRepository,
    StubAuthorizationPort,
    StubParticipationReferenceValidationPort,
    RecordingDomainEventPublisher,
    RecordingIntegrationEventPublisher,
]:
    repository = repository or InMemoryParticipationRepository()
    authorization = authorization or StubAuthorizationPort()
    reference_validation = (
        reference_validation
        or StubParticipationReferenceValidationPort()
    )
    domain_event_publisher = (
        domain_event_publisher
        or RecordingDomainEventPublisher()
    )
    integration_event_publisher = (
        integration_event_publisher
        or RecordingIntegrationEventPublisher()
    )

    service = RegisterParticipationService(
        repository=repository,
        authorization=authorization,
        reference_validation=reference_validation,
        domain_event_publisher=domain_event_publisher,
        integration_event_publisher=integration_event_publisher,
    )

    return (
        service,
        repository,
        authorization,
        reference_validation,
        domain_event_publisher,
        integration_event_publisher,
    )


def test_register_service_creates_and_persists_registered_participation() -> None:
    (
        service,
        repository,
        _,
        _,
        _,
        _,
    ) = _build_service()

    created_at = datetime(2026, 8, 29, 12, 0, tzinfo=UTC)

    result = service.execute(
        _command(),
        actor_id="ACTOR-001",
        created_at=created_at,
        event_id="EVT-001",
    )

    persisted = repository.get_by_id(
        ParticipationId("PAR-001"),
    )

    assert persisted is not None
    assert persisted.status is ParticipationStatus.REGISTERED
    assert persisted.version == ParticipationVersion(1)
    assert persisted.created_at == created_at
    assert persisted.started_at is None

    assert result.participation_id == ParticipationId("PAR-001")
    assert result.organization_id == OrganizationId("ORG-001")
    assert result.participation_type is ParticipationType.ATTENDANCE
    assert result.status is ParticipationStatus.REGISTERED
    assert result.version == ParticipationVersion(1)
    assert result.created_at == created_at
    assert result.started_at is None


def test_register_service_uses_none_expected_version_for_creation() -> None:
    (
        service,
        repository,
        _,
        _,
        _,
        _,
    ) = _build_service()

    service.execute(
        _command(),
        actor_id="ACTOR-001",
        created_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
        event_id="EVT-001",
    )

    assert repository.saved_expected_versions == [None]


def test_register_service_checks_required_permission() -> None:
    (
        service,
        _,
        authorization,
        _,
        _,
        _,
    ) = _build_service()

    service.execute(
        _command(),
        actor_id="ACTOR-001",
        created_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
        event_id="EVT-001",
    )

    assert authorization.calls == [
        ("ACTOR-001", "Participation.Register"),
    ]


def test_register_service_validates_organization_reference() -> None:
    (
        service,
        _,
        _,
        reference_validation,
        _,
        _,
    ) = _build_service()

    service.execute(
        _command(),
        actor_id="ACTOR-001",
        created_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
        event_id="EVT-001",
    )

    assert reference_validation.validated_organizations == [
        OrganizationId("ORG-001"),
    ]


def test_register_service_publishes_confirmed_domain_event() -> None:
    (
        service,
        _,
        _,
        _,
        domain_event_publisher,
        _,
    ) = _build_service()

    created_at = datetime(2026, 8, 29, 12, 0, tzinfo=UTC)

    service.execute(
        _command(),
        actor_id="ACTOR-001",
        created_at=created_at,
        event_id="EVT-001",
        correlation_id="CORR-001",
        causation_id="CMD-001",
    )

    assert len(domain_event_publisher.published_events) == 1

    event = domain_event_publisher.published_events[0]

    assert isinstance(event, ParticipationRegistered)
    assert event.event_id == "EVT-001"
    assert event.participation_id == ParticipationId("PAR-001")
    assert event.organization_id == OrganizationId("ORG-001")
    assert event.participation_type is ParticipationType.ATTENDANCE
    assert event.occurred_at == created_at
    assert event.aggregate_version == ParticipationVersion(1)
    assert event.actor_id == "ACTOR-001"
    assert event.correlation_id == "CORR-001"
    assert event.causation_id == "CMD-001"


def test_register_service_publishes_registered_integration_event() -> None:
    (
        service,
        _,
        _,
        _,
        _,
        integration_event_publisher,
    ) = _build_service()

    created_at = datetime(2026, 8, 29, 12, 0, tzinfo=UTC)

    service.execute(
        _command(),
        actor_id="ACTOR-001",
        created_at=created_at,
        event_id="EVT-001",
        correlation_id="CORR-001",
        causation_id="CMD-001",
    )

    assert len(integration_event_publisher.published_events) == 1

    event = integration_event_publisher.published_events[0]

    assert isinstance(
        event,
        ParticipationRegisteredIntegrationEvent,
    )
    assert event.event_id == "EVT-001"
    assert (
        event.event_type
        == "ParticipationRegisteredIntegrationEvent"
    )
    assert event.event_version == 1
    assert event.aggregate_id == ParticipationId("PAR-001")
    assert event.aggregate_type == "Participation"
    assert event.aggregate_version == ParticipationVersion(1)
    assert event.occurred_at == created_at
    assert event.correlation_id == "CORR-001"
    assert event.causation_id == "CMD-001"
    assert event.organization_id == OrganizationId("ORG-001")
    assert event.participation_type is ParticipationType.ATTENDANCE
    assert not hasattr(event, "published_at")


def test_register_service_rejects_unauthorized_actor_without_side_effects() -> None:
    authorization = StubAuthorizationPort(
        authorized=False,
    )

    (
        service,
        repository,
        _,
        reference_validation,
        domain_event_publisher,
        integration_event_publisher,
    ) = _build_service(
        authorization=authorization,
    )

    with pytest.raises(
        PermissionError,
        match="Actor is not authorized to register a Participation.",
    ):
        service.execute(
            _command(),
            actor_id="ACTOR-001",
            created_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
            event_id="EVT-001",
        )

    assert not repository.exists(ParticipationId("PAR-001"))
    assert reference_validation.validated_organizations == []
    assert domain_event_publisher.published_events == []
    assert integration_event_publisher.published_events == []


def test_register_service_rejects_invalid_organization_without_persisting() -> None:
    reference_validation = StubParticipationReferenceValidationPort(
        should_fail=True,
    )

    (
        service,
        repository,
        _,
        _,
        domain_event_publisher,
        integration_event_publisher,
    ) = _build_service(
        reference_validation=reference_validation,
    )

    with pytest.raises(
        ValueError,
        match="Organization reference is invalid.",
    ):
        service.execute(
            _command(),
            actor_id="ACTOR-001",
            created_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
            event_id="EVT-001",
        )

    assert not repository.exists(ParticipationId("PAR-001"))
    assert domain_event_publisher.published_events == []
    assert integration_event_publisher.published_events == []


def test_register_service_rejects_duplicate_identity_without_new_events() -> None:
    repository = InMemoryParticipationRepository()

    existing = Participation.register(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.ATTENDANCE,
        created_at=datetime(2026, 8, 29, 11, 0, tzinfo=UTC),
        event_id="EVT-EXISTING",
        actor_id="ACTOR-EXISTING",
    )
    existing.pull_domain_events()

    repository.save(
        existing,
        expected_version=None,
    )

    (
        service,
        _,
        _,
        _,
        domain_event_publisher,
        integration_event_publisher,
    ) = _build_service(
        repository=repository,
    )

    with pytest.raises(
        ValueError,
        match="Participation already exists: PAR-001",
    ):
        service.execute(
            _command(),
            actor_id="ACTOR-001",
            created_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
            event_id="EVT-001",
        )

    persisted = repository.get_by_id(
        ParticipationId("PAR-001"),
    )

    assert persisted is existing
    assert persisted.version == ParticipationVersion(1)
    assert domain_event_publisher.published_events == []
    assert integration_event_publisher.published_events == []


def test_register_service_does_not_publish_when_repository_save_fails() -> None:
    class FailingRepository(InMemoryParticipationRepository):
        def save(
            self,
            participation: Participation,
            expected_version: ParticipationVersion | None,
        ) -> None:
            raise RuntimeError("Persistence failure.")

    repository = FailingRepository()

    (
        service,
        _,
        _,
        _,
        domain_event_publisher,
        integration_event_publisher,
    ) = _build_service(
        repository=repository,
    )

    with pytest.raises(
        RuntimeError,
        match="Persistence failure.",
    ):
        service.execute(
            _command(),
            actor_id="ACTOR-001",
            created_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
            event_id="EVT-001",
        )

    assert domain_event_publisher.published_events == []
    assert integration_event_publisher.published_events == []


def test_register_service_returns_dto_not_aggregate() -> None:
    (
        service,
        _,
        _,
        _,
        _,
        _,
    ) = _build_service()

    result = service.execute(
        _command(),
        actor_id="ACTOR-001",
        created_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
        event_id="EVT-001",
    )

    assert not isinstance(result, Participation)