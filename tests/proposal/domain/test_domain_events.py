from datetime import UTC, datetime

from arada_core.proposal.domain.events.proposal_created import ProposalCreated
from arada_core.proposal.domain.events.proposal_submitted import ProposalSubmitted
from arada_core.proposal.domain.value_objects.organization_id import OrganizationId
from arada_core.proposal.domain.value_objects.proposal_id import ProposalId
from arada_core.proposal.domain.value_objects.proposal_name import ProposalName
from arada_core.proposal.domain.value_objects.proposal_type import ProposalType
from arada_core.proposal.domain.value_objects.proposal_version import ProposalVersion


def test_proposal_created_preserves_domain_fact() -> None:
    """
    ProposalCreated debe representar inmutablemente el hecho de creación.

    El evento conserva únicamente información perteneciente al significado
    del hecho producido por el Aggregate y no incorpora responsabilidades de
    persistencia, autorización o integración.
    """
    occurred_at = datetime(
        2026,
        8,
        26,
        6,
        30,
        tzinfo=UTC,
    )

    event = ProposalCreated(
        proposal_id=ProposalId("proposal-001"),
        organization_id=OrganizationId("organization-001"),
        proposal_name=ProposalName("Mejoramiento del espacio comunitario"),
        proposal_type=ProposalType.COMMUNITY,
        occurred_at=occurred_at,
        version=ProposalVersion(1),
    )

    assert event.proposal_id == ProposalId("proposal-001")
    assert event.organization_id == OrganizationId("organization-001")
    assert event.proposal_name == ProposalName(
        "Mejoramiento del espacio comunitario"
    )
    assert event.proposal_type is ProposalType.COMMUNITY
    assert event.occurred_at == occurred_at
    assert event.version == ProposalVersion(1)


def test_proposal_submitted_preserves_domain_fact() -> None:
    """
    ProposalSubmitted debe representar inmutablemente una presentación válida.

    La Version contenida corresponde al estado resultante del Aggregate
    después de ejecutar correctamente Draft -> Submitted.
    """
    occurred_at = datetime(
        2026,
        8,
        26,
        6,
        31,
        tzinfo=UTC,
    )

    event = ProposalSubmitted(
        proposal_id=ProposalId("proposal-001"),
        organization_id=OrganizationId("organization-001"),
        occurred_at=occurred_at,
        version=ProposalVersion(2),
    )

    assert event.proposal_id == ProposalId("proposal-001")
    assert event.organization_id == OrganizationId("organization-001")
    assert event.occurred_at == occurred_at
    assert event.version == ProposalVersion(2)


def test_proposal_created_and_submitted_are_distinct_domain_facts() -> None:
    """
    ProposalCreated y ProposalSubmitted representan hechos diferentes del
    Lifecycle y no deben confundirse aunque pertenezcan al mismo Aggregate.
    """
    created_at = datetime(
        2026,
        8,
        26,
        6,
        30,
        tzinfo=UTC,
    )
    submitted_at = datetime(
        2026,
        8,
        26,
        6,
        31,
        tzinfo=UTC,
    )

    created = ProposalCreated(
        proposal_id=ProposalId("proposal-001"),
        organization_id=OrganizationId("organization-001"),
        proposal_name=ProposalName("Mejoramiento del espacio comunitario"),
        proposal_type=ProposalType.COMMUNITY,
        occurred_at=created_at,
        version=ProposalVersion(1),
    )

    submitted = ProposalSubmitted(
        proposal_id=ProposalId("proposal-001"),
        organization_id=OrganizationId("organization-001"),
        occurred_at=submitted_at,
        version=ProposalVersion(2),
    )

    assert type(created) is ProposalCreated
    assert type(submitted) is ProposalSubmitted
    assert type(created) is not type(submitted)
    assert created.version == ProposalVersion(1)
    assert submitted.version == ProposalVersion(2)