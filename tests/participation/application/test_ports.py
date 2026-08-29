from __future__ import annotations

from typing import cast

import pytest

from arada_core.participation.application.commands.activate_participation import (
    ActivateParticipation,
)
from arada_core.participation.application.commands.register_participation import (
    RegisterParticipation,
)
from arada_core.participation.application.dto.participation_result import (
    ParticipationResult,
)
from arada_core.participation.application.ports.activate_participation_use_case import (
    ActivateParticipationUseCase,
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
from arada_core.participation.application.ports.register_participation_use_case import (
    RegisterParticipationUseCase,
)
from arada_core.participation.domain.value_objects.organization_id import OrganizationId


class StubAuthorizationPort(AuthorizationPort):
    def is_authorized(
        self,
        actor_id: str,
        permission: str,
    ) -> bool:
        raise NotImplementedError


class StubDomainEventPublisher(DomainEventPublisher):
    def publish(
        self,
        events: tuple[object, ...],
    ) -> None:
        raise NotImplementedError


class StubIntegrationEventPublisher(IntegrationEventPublisher):
    def publish(
        self,
        events: tuple[object, ...],
    ) -> None:
        raise NotImplementedError


class StubParticipationReferenceValidationPort(
    ParticipationReferenceValidationPort
):
    def validate_organization(
        self,
        organization_id: OrganizationId,
    ) -> None:
        raise NotImplementedError


class StubRegisterParticipationUseCase(RegisterParticipationUseCase):
    def execute(
        self,
        command: RegisterParticipation,
        *,
        actor_id: str,
    ) -> ParticipationResult:
        raise NotImplementedError


class StubActivateParticipationUseCase(ActivateParticipationUseCase):
    def execute(
        self,
        command: ActivateParticipation,
        *,
        actor_id: str,
    ) -> ParticipationResult:
        raise NotImplementedError


@pytest.mark.parametrize(
    "port_type",
    [
        AuthorizationPort,
        DomainEventPublisher,
        IntegrationEventPublisher,
        ParticipationReferenceValidationPort,
        RegisterParticipationUseCase,
        ActivateParticipationUseCase,
    ],
)
def test_application_ports_cannot_be_instantiated_directly(
    port_type: type[object],
) -> None:
    with pytest.raises(TypeError):
        port_type()


def test_authorization_port_exposes_is_authorized_contract() -> None:
    port = StubAuthorizationPort()

    with pytest.raises(NotImplementedError):
        port.is_authorized(
            actor_id="ACTOR-001",
            permission="Participation.Register",
        )


def test_domain_event_publisher_exposes_publish_contract() -> None:
    port = StubDomainEventPublisher()

    with pytest.raises(NotImplementedError):
        port.publish(())


def test_integration_event_publisher_exposes_publish_contract() -> None:
    port = StubIntegrationEventPublisher()

    with pytest.raises(NotImplementedError):
        port.publish(())


def test_reference_validation_port_exposes_validate_organization_contract() -> None:
    port = StubParticipationReferenceValidationPort()

    with pytest.raises(NotImplementedError):
        port.validate_organization(
            OrganizationId("ORG-001"),
        )


def test_register_participation_use_case_exposes_execute_contract() -> None:
    port = StubRegisterParticipationUseCase()
    command = cast(RegisterParticipation, object())

    with pytest.raises(NotImplementedError):
        port.execute(
            command,
            actor_id="ACTOR-001",
        )


def test_activate_participation_use_case_exposes_execute_contract() -> None:
    port = StubActivateParticipationUseCase()
    command = cast(ActivateParticipation, object())

    with pytest.raises(NotImplementedError):
        port.execute(
            command,
            actor_id="ACTOR-001",
        )