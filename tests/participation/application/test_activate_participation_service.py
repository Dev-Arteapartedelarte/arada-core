from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime

import pytest

from arada_core.participation.application.commands.activate_participation import (
    ActivateParticipation,
)
from arada_core.participation.application.integration_events.participation_activated_integration_event import (
    ParticipationActivatedIntegrationEvent,
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
from arada_core.participation.application.services.activate_participation_service import (
    ActivateParticipationService,
)
from arada_core.participation.domain.aggregates.participation import Participation
from arada_core.participation.domain.events.participation_activated import (
    ParticipationActivated,
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
    """
    Test double con semántica de persistencia desacoplada del objeto cargado.

    Se utilizan copias para evitar que una mutación realizada sobre el
    Aggregate cargado modifique implícitamente el estado persistido antes de
    ejecutar save(...).

    Esto permite probar correctamente la concurrencia optimista.
    """

    def __init__(self) -> None:
        self._participations: dict[ParticipationId, Participation] = {}
        self._persisted_versions: dict[
            ParticipationId,
            ParticipationVersion,
        ] = {}
        self.saved_expected_versions: list[
            ParticipationVersion | None
        ] = []

    def get_by_id(
        self,
        participation_id: ParticipationId,
    ) -> Participation | None:
        participation = self._participations.get(participation_id)

        if participation is None:
            return None

        return deepcopy(participation)

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

            self._participations[participation_id] = deepcopy(
                participation
            )
            self._persisted_versions[participation_id] = (
                participation.version
            )
            self.saved_expected_versions.append(None)
            return

        persisted_version = self._persisted_versions.get(
            participation_id
        )

        if persisted_version is None:
            raise LookupError(
                f"Participation not found: {participation_id}"
            )

        if persisted_version != expected_version:
            raise ValueError("Participation version conflict.")

        self._participations[participation_id] = deepcopy(
            participation
        )
        self._persisted_versions[participation_id] = (
            participation.version
        )
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


class RecordingIntegrationEventPublisher(
    IntegrationEventPublisher
):
    def __init__(self) -> None:
        self.published_events: list[object] = []

    def publish(
        self,
        events: tuple[object, ...],
    ) -> None:
        self.published_events.extend(events)


def _registered_participation(
    *,
    participation_id: str = "PAR-001",
    organization_id: str = "ORG-001",
) -> Participation:
    participation = Participation.register(
        participation_id=ParticipationId(participation_id),
        organization_id=OrganizationId(organization_id),
        participation_type=ParticipationType.ATTENDANCE,
        created_at=datetime(
            2026,
            8,
            29,
            12,
            0,
            tzinfo=UTC,
        ),
        event_id="EVT-REGISTER",
        actor_id="ACTOR-REGISTER",
    )

    participation.pull_domain_events()

    return participation


def _repository_with_registered_participation(
) -> InMemoryParticipationRepository:
    repository = InMemoryParticipationRepository()

    repository.save(
        _registered_participation(),
        expected_version=None,
    )

    return repository


def _command(
    *,
    participation_id: str = "PAR-001",
    organization_id: str = "ORG-001",
    expected_version: int = 1,
) -> ActivateParticipation:
    return ActivateParticipation(
        participation_id=ParticipationId(participation_id),
        organization_id=OrganizationId(organization_id),
        expected_version=ParticipationVersion(
            expected_version
        ),
    )


def _build_service(
    *,
    repository: InMemoryParticipationRepository | None = None,
    authorization: StubAuthorizationPort | None = None,
    reference_validation: (
        StubParticipationReferenceValidationPort | None
    ) = None,
    domain_event_publisher: (
        RecordingDomainEventPublisher | None
    ) = None,
    integration_event_publisher: (
        RecordingIntegrationEventPublisher | None
    ) = None,
) -> tuple[
    ActivateParticipationService,
    InMemoryParticipationRepository,
    StubAuthorizationPort,
    StubParticipationReferenceValidationPort,
    RecordingDomainEventPublisher,
    RecordingIntegrationEventPublisher,
]:
    repository = (
        repository
        or _repository_with_registered_participation()
    )
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

    service = ActivateParticipationService(
        repository=repository,
        authorization=authorization,
        reference_validation=reference_validation,
        domain_event_publisher=domain_event_publisher,
        integration_event_publisher=(
            integration_event_publisher
        ),
    )

    return (
        service,
        repository,
        authorization,
        reference_validation,
        domain_event_publisher,
        integration_event_publisher,
    )


def test_activate_service_transitions_registered_to_active() -> None:
    (
        service,
        repository,
        _,
        _,
        _,
        _,
    ) = _build_service()

    started_at = datetime(
        2026,
        8,
        29,
        12,
        30,
        tzinfo=UTC,
    )

    result = service.execute(
        _command(),
        actor_id="ACTOR-001",
        started_at=started_at,
        event_id="EVT-002",
    )

    persisted = repository.get_by_id(
        ParticipationId("PAR-001")
    )

    assert persisted is not None
    assert persisted.status is ParticipationStatus.ACTIVE
    assert persisted.started_at == started_at
    assert persisted.version == ParticipationVersion(2)

    assert result.participation_id == ParticipationId(
        "PAR-001"
    )
    assert result.organization_id == OrganizationId(
        "ORG-001"
    )
    assert result.participation_type is (
        ParticipationType.ATTENDANCE
    )
    assert result.status is ParticipationStatus.ACTIVE
    assert result.version == ParticipationVersion(2)
    assert result.started_at == started_at


def test_activate_service_uses_expected_version_from_command() -> None:
    (
        service,
        repository,
        _,
        _,
        _,
        _,
    ) = _build_service()

    service.execute(
        _command(expected_version=1),
        actor_id="ACTOR-001",
        started_at=datetime(
            2026,
            8,
            29,
            12,
            30,
            tzinfo=UTC,
        ),
        event_id="EVT-002",
    )

    assert repository.saved_expected_versions == [
        None,
        ParticipationVersion(1),
    ]


def test_activate_service_checks_required_permission() -> None:
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
        started_at=datetime(
            2026,
            8,
            29,
            12,
            30,
            tzinfo=UTC,
        ),
        event_id="EVT-002",
    )

    assert authorization.calls == [
        ("ACTOR-001", "Participation.Activate"),
    ]


def test_activate_service_validates_organization_reference() -> None:
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
        started_at=datetime(
            2026,
            8,
            29,
            12,
            30,
            tzinfo=UTC,
        ),
        event_id="EVT-002",
    )

    assert reference_validation.validated_organizations == [
        OrganizationId("ORG-001"),
    ]


def test_activate_service_publishes_confirmed_domain_event() -> None:
    (
        service,
        _,
        _,
        _,
        domain_event_publisher,
        _,
    ) = _build_service()

    started_at = datetime(
        2026,
        8,
        29,
        12,
        30,
        tzinfo=UTC,
    )

    service.execute(
        _command(),
        actor_id="ACTOR-001",
        started_at=started_at,
        event_id="EVT-002",
        correlation_id="CORR-001",
        causation_id="CMD-002",
    )

    assert len(
        domain_event_publisher.published_events
    ) == 1

    event = domain_event_publisher.published_events[0]

    assert isinstance(event, ParticipationActivated)
    assert event.event_id == "EVT-002"
    assert event.participation_id == ParticipationId(
        "PAR-001"
    )
    assert event.organization_id == OrganizationId(
        "ORG-001"
    )
    assert event.started_at == started_at
    assert event.occurred_at == started_at
    assert event.aggregate_version == ParticipationVersion(2)
    assert event.actor_id == "ACTOR-001"
    assert event.correlation_id == "CORR-001"
    assert event.causation_id == "CMD-002"


def test_activate_service_publishes_activated_integration_event(
) -> None:
    (
        service,
        _,
        _,
        _,
        _,
        integration_event_publisher,
    ) = _build_service()

    started_at = datetime(
        2026,
        8,
        29,
        12,
        30,
        tzinfo=UTC,
    )

    service.execute(
        _command(),
        actor_id="ACTOR-001",
        started_at=started_at,
        event_id="EVT-002",
        correlation_id="CORR-001",
        causation_id="CMD-002",
    )

    assert len(
        integration_event_publisher.published_events
    ) == 1

    event = (
        integration_event_publisher.published_events[0]
    )

    assert isinstance(
        event,
        ParticipationActivatedIntegrationEvent,
    )
    assert event.event_id == "EVT-002"
    assert (
        event.event_type
        == "ParticipationActivatedIntegrationEvent"
    )
    assert event.event_version == 1
    assert event.aggregate_id == ParticipationId(
        "PAR-001"
    )
    assert event.aggregate_type == "Participation"
    assert event.aggregate_version == ParticipationVersion(2)
    assert event.occurred_at == started_at
    assert event.correlation_id == "CORR-001"
    assert event.causation_id == "CMD-002"
    assert event.organization_id == OrganizationId(
        "ORG-001"
    )
    assert not hasattr(event, "published_at")


def test_activate_service_rejects_unauthorized_actor_without_side_effects(
) -> None:
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
        match=(
            "Actor is not authorized to activate a "
            "Participation."
        ),
    ):
        service.execute(
            _command(),
            actor_id="ACTOR-001",
            started_at=datetime(
                2026,
                8,
                29,
                12,
                30,
                tzinfo=UTC,
            ),
            event_id="EVT-002",
        )

    persisted = repository.get_by_id(
        ParticipationId("PAR-001")
    )

    assert persisted is not None
    assert persisted.status is ParticipationStatus.REGISTERED
    assert persisted.version == ParticipationVersion(1)
    assert persisted.started_at is None
    assert reference_validation.validated_organizations == []
    assert domain_event_publisher.published_events == []
    assert integration_event_publisher.published_events == []


def test_activate_service_rejects_missing_participation() -> None:
    repository = InMemoryParticipationRepository()

    (
        service,
        _,
        _,
        reference_validation,
        domain_event_publisher,
        integration_event_publisher,
    ) = _build_service(
        repository=repository,
    )

    with pytest.raises(
        LookupError,
        match="Participation not found: PAR-001",
    ):
        service.execute(
            _command(),
            actor_id="ACTOR-001",
            started_at=datetime(
                2026,
                8,
                29,
                12,
                30,
                tzinfo=UTC,
            ),
            event_id="EVT-002",
        )

    assert reference_validation.validated_organizations == []
    assert domain_event_publisher.published_events == []
    assert integration_event_publisher.published_events == []


def test_activate_service_rejects_organization_mismatch() -> None:
    (
        service,
        repository,
        _,
        reference_validation,
        domain_event_publisher,
        integration_event_publisher,
    ) = _build_service()

    with pytest.raises(
        ValueError,
        match=(
            "OrganizationId does not match the "
            "Participation aggregate."
        ),
    ):
        service.execute(
            _command(
                organization_id="ORG-999",
            ),
            actor_id="ACTOR-001",
            started_at=datetime(
                2026,
                8,
                29,
                12,
                30,
                tzinfo=UTC,
            ),
            event_id="EVT-002",
        )

    persisted = repository.get_by_id(
        ParticipationId("PAR-001")
    )

    assert persisted is not None
    assert persisted.status is ParticipationStatus.REGISTERED
    assert persisted.version == ParticipationVersion(1)
    assert persisted.started_at is None

    assert reference_validation.validated_organizations == []
    assert domain_event_publisher.published_events == []
    assert integration_event_publisher.published_events == []


def test_activate_service_rejects_invalid_organization_reference(
) -> None:
    reference_validation = (
        StubParticipationReferenceValidationPort(
            should_fail=True,
        )
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
            started_at=datetime(
                2026,
                8,
                29,
                12,
                30,
                tzinfo=UTC,
            ),
            event_id="EVT-002",
        )

    persisted = repository.get_by_id(
        ParticipationId("PAR-001")
    )

    assert persisted is not None
    assert persisted.status is ParticipationStatus.REGISTERED
    assert persisted.version == ParticipationVersion(1)
    assert persisted.started_at is None
    assert domain_event_publisher.published_events == []
    assert integration_event_publisher.published_events == []


def test_activate_service_rejects_stale_expected_version_without_persisting(
) -> None:
    (
        service,
        repository,
        _,
        _,
        domain_event_publisher,
        integration_event_publisher,
    ) = _build_service()

    with pytest.raises(
        ValueError,
        match="Participation version conflict.",
    ):
        service.execute(
            _command(
                expected_version=2,
            ),
            actor_id="ACTOR-001",
            started_at=datetime(
                2026,
                8,
                29,
                12,
                30,
                tzinfo=UTC,
            ),
            event_id="EVT-002",
        )

    persisted = repository.get_by_id(
        ParticipationId("PAR-001")
    )

    assert persisted is not None
    assert persisted.status is ParticipationStatus.REGISTERED
    assert persisted.version == ParticipationVersion(1)
    assert persisted.started_at is None
    assert domain_event_publisher.published_events == []
    assert integration_event_publisher.published_events == []


def test_activate_service_rejects_second_activation() -> None:
    (
        service,
        repository,
        _,
        _,
        domain_event_publisher,
        integration_event_publisher,
    ) = _build_service()

    service.execute(
        _command(),
        actor_id="ACTOR-001",
        started_at=datetime(
            2026,
            8,
            29,
            12,
            30,
            tzinfo=UTC,
        ),
        event_id="EVT-002",
    )

    domain_event_publisher.published_events.clear()
    integration_event_publisher.published_events.clear()

    with pytest.raises(
        ValueError,
        match=(
            "Participation can only be activated from "
            "Registered status."
        ),
    ):
        service.execute(
            _command(
                expected_version=2,
            ),
            actor_id="ACTOR-002",
            started_at=datetime(
                2026,
                8,
                29,
                13,
                0,
                tzinfo=UTC,
            ),
            event_id="EVT-003",
        )

    persisted = repository.get_by_id(
        ParticipationId("PAR-001")
    )

    assert persisted is not None
    assert persisted.status is ParticipationStatus.ACTIVE
    assert persisted.version == ParticipationVersion(2)
    assert persisted.started_at == datetime(
        2026,
        8,
        29,
        12,
        30,
        tzinfo=UTC,
    )
    assert domain_event_publisher.published_events == []
    assert integration_event_publisher.published_events == []


def test_activate_service_rejects_started_at_before_created_at(
) -> None:
    (
        service,
        repository,
        _,
        _,
        domain_event_publisher,
        integration_event_publisher,
    ) = _build_service()

    with pytest.raises(
        ValueError,
        match=(
            "Participation started_at must not be "
            "earlier than created_at."
        ),
    ):
        service.execute(
            _command(),
            actor_id="ACTOR-001",
            started_at=datetime(
                2026,
                8,
                29,
                11,
                59,
                tzinfo=UTC,
            ),
            event_id="EVT-002",
        )

    persisted = repository.get_by_id(
        ParticipationId("PAR-001")
    )

    assert persisted is not None
    assert persisted.status is ParticipationStatus.REGISTERED
    assert persisted.version == ParticipationVersion(1)
    assert persisted.started_at is None
    assert domain_event_publisher.published_events == []
    assert integration_event_publisher.published_events == []


def test_activate_service_does_not_publish_when_repository_save_fails(
) -> None:
    class FailingRepository(
        InMemoryParticipationRepository
    ):
        def save(
            self,
            participation: Participation,
            expected_version: ParticipationVersion | None,
        ) -> None:
            if expected_version is None:
                super().save(
                    participation,
                    expected_version,
                )
                return

            raise RuntimeError("Persistence failure.")

    repository = FailingRepository()

    repository.save(
        _registered_participation(),
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
        RuntimeError,
        match="Persistence failure.",
    ):
        service.execute(
            _command(),
            actor_id="ACTOR-001",
            started_at=datetime(
                2026,
                8,
                29,
                12,
                30,
                tzinfo=UTC,
            ),
            event_id="EVT-002",
        )

    persisted = repository.get_by_id(
        ParticipationId("PAR-001")
    )

    assert persisted is not None
    assert persisted.status is ParticipationStatus.REGISTERED
    assert persisted.version == ParticipationVersion(1)
    assert persisted.started_at is None
    assert domain_event_publisher.published_events == []
    assert integration_event_publisher.published_events == []


def test_activate_service_returns_dto_not_aggregate() -> None:
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
        started_at=datetime(
            2026,
            8,
            29,
            12,
            30,
            tzinfo=UTC,
        ),
        event_id="EVT-002",
    )

    assert not isinstance(result, Participation)