from __future__ import annotations

from datetime import datetime
from typing import Self

from arada_core.participation.domain.events.participation_activated import (
    ParticipationActivated,
)
from arada_core.participation.domain.events.participation_registered import (
    ParticipationRegistered,
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


class Participation:
    """Aggregate Root del Bounded Context Participation Management."""

    def __init__(
        self,
        *,
        participation_id: ParticipationId,
        organization_id: OrganizationId,
        participation_type: ParticipationType,
        status: ParticipationStatus,
        version: ParticipationVersion,
        created_at: datetime,
        started_at: datetime | None = None,
    ) -> None:
        self._participation_id = participation_id
        self._organization_id = organization_id
        self._participation_type = participation_type
        self._status = status
        self._version = version
        self._created_at = created_at
        self._started_at = started_at
        self._domain_events: list[object] = []

    @classmethod
    def register(
        cls,
        *,
        participation_id: ParticipationId,
        organization_id: OrganizationId,
        participation_type: ParticipationType,
        created_at: datetime,
        event_id: str,
        actor_id: str,
        correlation_id: str | None = None,
        causation_id: str | None = None,
    ) -> Self:
        """Registra una nueva Participation en estado Registered."""

        cls._ensure_non_empty_metadata(event_id, "event_id")
        cls._ensure_non_empty_metadata(actor_id, "actor_id")
        cls._ensure_optional_metadata(correlation_id, "correlation_id")
        cls._ensure_optional_metadata(causation_id, "causation_id")

        version = ParticipationVersion.initial()

        participation = cls(
            participation_id=participation_id,
            organization_id=organization_id,
            participation_type=participation_type,
            status=ParticipationStatus.REGISTERED,
            version=version,
            created_at=created_at,
        )

        participation._record_domain_event(
            ParticipationRegistered(
                event_id=event_id,
                participation_id=participation_id,
                organization_id=organization_id,
                participation_type=participation_type,
                occurred_at=created_at,
                aggregate_version=version,
                actor_id=actor_id,
                correlation_id=correlation_id,
                causation_id=causation_id,
            )
        )

        return participation

    def activate(
        self,
        *,
        started_at: datetime,
        event_id: str,
        actor_id: str,
        correlation_id: str | None = None,
        causation_id: str | None = None,
    ) -> None:
        """Activa una Participation previamente registrada."""

        self._ensure_can_activate()
        self._ensure_started_at_is_valid(started_at)
        self._ensure_non_empty_metadata(event_id, "event_id")
        self._ensure_non_empty_metadata(actor_id, "actor_id")
        self._ensure_optional_metadata(correlation_id, "correlation_id")
        self._ensure_optional_metadata(causation_id, "causation_id")

        next_version = self._version.next()

        self._status = ParticipationStatus.ACTIVE
        self._started_at = started_at
        self._version = next_version

        self._record_domain_event(
            ParticipationActivated(
                event_id=event_id,
                participation_id=self._participation_id,
                organization_id=self._organization_id,
                started_at=started_at,
                occurred_at=started_at,
                aggregate_version=next_version,
                actor_id=actor_id,
                correlation_id=correlation_id,
                causation_id=causation_id,
            )
        )

    def _ensure_can_activate(self) -> None:
        if self._status is not ParticipationStatus.REGISTERED:
            raise ValueError(
                "Participation can only be activated from Registered status."
            )

    def _ensure_started_at_is_valid(self, started_at: datetime) -> None:
        if started_at < self._created_at:
            raise ValueError(
                "Participation started_at must not be earlier than created_at."
            )

    @staticmethod
    def _ensure_non_empty_metadata(value: str, field_name: str) -> None:
        if not value.strip():
            raise ValueError(f"{field_name} must not be empty.")

    @staticmethod
    def _ensure_optional_metadata(value: str | None, field_name: str) -> None:
        if value is not None and not value.strip():
            raise ValueError(f"{field_name} must not be empty when provided.")

    def _record_domain_event(self, event: object) -> None:
        self._domain_events.append(event)

    def pull_domain_events(self) -> tuple[object, ...]:
        events = tuple(self._domain_events)
        self._domain_events.clear()
        return events

    @property
    def participation_id(self) -> ParticipationId:
        return self._participation_id

    @property
    def organization_id(self) -> OrganizationId:
        return self._organization_id

    @property
    def participation_type(self) -> ParticipationType:
        return self._participation_type

    @property
    def status(self) -> ParticipationStatus:
        return self._status

    @property
    def version(self) -> ParticipationVersion:
        return self._version

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def started_at(self) -> datetime | None:
        return self._started_at