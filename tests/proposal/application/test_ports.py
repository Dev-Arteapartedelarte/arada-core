from collections.abc import Sequence

from arada_core.proposal.application.commands.create_proposal import CreateProposal
from arada_core.proposal.application.commands.submit_proposal import SubmitProposal
from arada_core.proposal.application.dto.proposal_result import ProposalResult
from arada_core.proposal.application.ports.authorization_port import AuthorizationPort
from arada_core.proposal.application.ports.create_proposal_use_case import (
    CreateProposalUseCase,
)
from arada_core.proposal.application.ports.domain_event_publisher import (
    DomainEventPublisher,
)
from arada_core.proposal.application.ports.integration_event_publisher import (
    IntegrationEventPublisher,
)
from arada_core.proposal.application.ports.proposal_reference_validation_port import (
    ProposalReferenceValidationPort,
)
from arada_core.proposal.application.ports.submit_proposal_use_case import (
    SubmitProposalUseCase,
)
from arada_core.proposal.domain.value_objects.submitted_at import SubmittedAt


def test_input_ports_are_abstract_contracts() -> None:
    """
    Los Input Ports deben permanecer como contratos de Application y no como
    implementaciones concretas de casos de uso.
    """
    assert CreateProposalUseCase.__abstractmethods__ == {"execute"}
    assert SubmitProposalUseCase.__abstractmethods__ == {"execute"}


def test_authorization_port_is_abstract_contract() -> None:
    """
    AuthorizationPort debe exigir una implementación externa para resolver
    autorización sin incorporar mecanismos técnicos a Application.
    """
    assert AuthorizationPort.__abstractmethods__ == {"is_authorized"}


def test_reference_validation_port_exposes_expected_capabilities() -> None:
    """
    ProposalReferenceValidationPort debe mantener separadas las capacidades
    externas requeridas por las referencias utilizadas en VS-001.
    """
    assert ProposalReferenceValidationPort.__abstractmethods__ == {
        "validate_organization",
        "validate_proposer",
        "validate_territory",
        "validate_assembly",
    }


def test_domain_event_publisher_is_abstract_contract() -> None:
    """
    La publicación de Domain Events debe permanecer detrás de un Output Port.
    """
    assert DomainEventPublisher.__abstractmethods__ == {"publish"}


def test_integration_event_publisher_is_abstract_contract() -> None:
    """
    La publicación de Integration Events debe permanecer detrás de un Output
    Port diferente del utilizado para Domain Events.
    """
    assert IntegrationEventPublisher.__abstractmethods__ == {"publish"}


def test_domain_and_integration_publishers_are_distinct_contracts() -> None:
    """
    DomainEventPublisher e IntegrationEventPublisher no deben colapsarse en
    una única abstracción porque representan responsabilidades diferentes.
    """
    assert DomainEventPublisher is not IntegrationEventPublisher
    assert not issubclass(DomainEventPublisher, IntegrationEventPublisher)
    assert not issubclass(IntegrationEventPublisher, DomainEventPublisher)


class DomainPublisherProbe(DomainEventPublisher):
    """Implementación mínima utilizada exclusivamente para verificar el Port."""

    def __init__(self) -> None:
        self.events: tuple[object, ...] = ()

    def publish(self, events: Sequence[object]) -> None:
        self.events = tuple(events)


class IntegrationPublisherProbe(IntegrationEventPublisher):
    """Implementación mínima utilizada exclusivamente para verificar el Port."""

    def __init__(self) -> None:
        self.events: tuple[object, ...] = ()

    def publish(self, events: Sequence[object]) -> None:
        self.events = tuple(events)


def test_publishers_accept_independent_event_sequences() -> None:
    """
    Cada publisher debe poder recibir su propio conjunto de contratos sin
    reinterpretar el tipo de eventos perteneciente al otro boundary.
    """
    domain_publisher = DomainPublisherProbe()
    integration_publisher = IntegrationPublisherProbe()

    domain_events = (object(), object())
    integration_events = (object(),)

    domain_publisher.publish(domain_events)
    integration_publisher.publish(integration_events)

    assert domain_publisher.events == domain_events
    assert integration_publisher.events == integration_events


def test_ports_do_not_expose_infrastructure_specific_names() -> None:
    """
    Los contratos públicos de Application deben permanecer tecnológicamente
    neutrales.

    Esta prueba protege explícitamente VS-001 contra el acoplamiento accidental
    de sus Ports con tecnologías concretas de seguridad, interoperabilidad,
    persistencia o mensajería.
    """
    port_names = {
        AuthorizationPort.__name__,
        CreateProposalUseCase.__name__,
        DomainEventPublisher.__name__,
        IntegrationEventPublisher.__name__,
        ProposalReferenceValidationPort.__name__,
        SubmitProposalUseCase.__name__,
    }

    forbidden_terms = {
        "Keyrock",
        "FIWARE",
        "Orion",
        "Kafka",
        "Postgres",
        "Mongo",
        "Redis",
        "HTTP",
    }

    for port_name in port_names:
        assert all(term not in port_name for term in forbidden_terms)


def test_create_input_port_exposes_complete_application_contract() -> None:
    """
    CreateProposalUseCase debe declarar la misma frontera pública que su
    Application Service:

        CreateProposal
        + actor_id
        -> ProposalResult

    actor_id pertenece al contexto de ejecución y no al Command funcional.
    """
    annotations = CreateProposalUseCase.execute.__annotations__

    assert annotations["command"] is CreateProposal
    assert annotations["actor_id"] is str
    assert annotations["return"] is ProposalResult


def test_submit_input_port_exposes_complete_application_contract() -> None:
    """
    SubmitProposalUseCase debe declarar la frontera pública completa:

        SubmitProposal
        + actor_id
        + SubmittedAt
        -> ProposalResult

    ExpectedVersion permanece dentro del Command, mientras actor_id y
    SubmittedAt pertenecen al contexto requerido para coordinar el caso de
    uso.
    """
    annotations = SubmitProposalUseCase.execute.__annotations__

    assert annotations["command"] is SubmitProposal
    assert annotations["actor_id"] is str
    assert annotations["submitted_at"] is SubmittedAt
    assert annotations["return"] is ProposalResult