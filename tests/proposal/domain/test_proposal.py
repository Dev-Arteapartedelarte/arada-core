from datetime import UTC, datetime

import pytest

from arada_core.proposal.domain.aggregates.proposal import Proposal
from arada_core.proposal.domain.events.proposal_created import ProposalCreated
from arada_core.proposal.domain.events.proposal_submitted import ProposalSubmitted
from arada_core.proposal.domain.value_objects.citizen_id import CitizenId
from arada_core.proposal.domain.value_objects.organization_id import OrganizationId
from arada_core.proposal.domain.value_objects.proposal_id import ProposalId
from arada_core.proposal.domain.value_objects.proposal_name import ProposalName
from arada_core.proposal.domain.value_objects.proposal_status import ProposalStatus
from arada_core.proposal.domain.value_objects.proposal_type import ProposalType
from arada_core.proposal.domain.value_objects.proposal_version import ProposalVersion
from arada_core.proposal.domain.value_objects.proposer_reference import (
    ProposerReference,
)
from arada_core.proposal.domain.value_objects.submitted_at import SubmittedAt


def build_proposal() -> Proposal:
    """
    Construye una Proposal válida para pruebas de VS-001.

    El helper utiliza únicamente la API pública del Aggregate y Value Objects
    del Bounded Context Proposal.
    """
    return Proposal.create(
        proposal_id=ProposalId("proposal-001"),
        organization_id=OrganizationId("organization-001"),
        proposer_reference=ProposerReference(CitizenId("citizen-001")),
        proposal_name=ProposalName("Mejoramiento del espacio comunitario"),
        proposal_type=ProposalType.COMMUNITY,
    )


def test_create_proposal_initializes_draft_version_one_and_event() -> None:
    """
    Una creación válida debe producir Draft, Version 1 y ProposalCreated.
    """
    proposal = build_proposal()

    assert proposal.proposal_id == ProposalId("proposal-001")
    assert proposal.organization_id == OrganizationId("organization-001")
    assert proposal.status is ProposalStatus.DRAFT
    assert proposal.version == ProposalVersion(1)
    assert proposal.submitted_at is None

    events = proposal.pull_domain_events()

    assert len(events) == 1

    event = events[0]

    assert isinstance(event, ProposalCreated)
    assert event.proposal_id == proposal.proposal_id
    assert event.organization_id == proposal.organization_id
    assert event.proposal_name == proposal.proposal_name
    assert event.proposal_type == proposal.proposal_type
    assert event.version == ProposalVersion(1)
    assert event.occurred_at.tzinfo is not None


def test_pull_domain_events_removes_pending_events() -> None:
    """
    Los Domain Events entregados no deben permanecer pendientes en la misma
    instancia del Aggregate.
    """
    proposal = build_proposal()

    first_pull = proposal.pull_domain_events()
    second_pull = proposal.pull_domain_events()

    assert len(first_pull) == 1
    assert second_pull == ()


def test_submit_proposal_transitions_from_draft_to_submitted() -> None:
    """
    Una presentación válida debe ejecutar Draft -> Submitted.
    """
    proposal = build_proposal()
    proposal.pull_domain_events()

    submitted_at = SubmittedAt(
        datetime(2026, 8, 26, 6, 30, tzinfo=UTC)
    )

    proposal.submit(submitted_at=submitted_at)

    assert proposal.status is ProposalStatus.SUBMITTED
    assert proposal.version == ProposalVersion(2)
    assert proposal.submitted_at == submitted_at


def test_submit_proposal_produces_proposal_submitted_event() -> None:
    """
    La transición válida a Submitted debe producir ProposalSubmitted con la
    nueva Version.
    """
    proposal = build_proposal()
    proposal.pull_domain_events()

    submitted_at = SubmittedAt(
        datetime(2026, 8, 26, 6, 31, tzinfo=UTC)
    )

    proposal.submit(submitted_at=submitted_at)

    events = proposal.pull_domain_events()

    assert len(events) == 1

    event = events[0]

    assert isinstance(event, ProposalSubmitted)
    assert event.proposal_id == proposal.proposal_id
    assert event.organization_id == proposal.organization_id
    assert event.occurred_at == submitted_at.value
    assert event.version == ProposalVersion(2)


def test_submit_proposal_increments_version_exactly_once() -> None:
    """
    Una transición válida Draft -> Submitted debe incrementar Version
    exactamente una vez.
    """
    proposal = build_proposal()
    proposal.pull_domain_events()

    initial_version = proposal.version

    proposal.submit(
        submitted_at=SubmittedAt(
            datetime(2026, 8, 26, 6, 32, tzinfo=UTC)
        )
    )

    assert initial_version == ProposalVersion(1)
    assert proposal.version == ProposalVersion(2)


def test_submit_from_submitted_is_rejected_without_state_change() -> None:
    """
    Una Proposal ya Submitted no puede volver a ejecutar SubmitProposal.
    """
    proposal = build_proposal()
    proposal.pull_domain_events()

    first_submitted_at = SubmittedAt(
        datetime(2026, 8, 26, 6, 33, tzinfo=UTC)
    )

    proposal.submit(submitted_at=first_submitted_at)
    proposal.pull_domain_events()

    version_before_invalid_operation = proposal.version

    with pytest.raises(
        ValueError,
        match="Proposal can only be submitted from Draft status.",
    ):
        proposal.submit(
            submitted_at=SubmittedAt(
                datetime(2026, 8, 26, 6, 34, tzinfo=UTC)
            )
        )

    assert proposal.status is ProposalStatus.SUBMITTED
    assert proposal.version == version_before_invalid_operation
    assert proposal.submitted_at == first_submitted_at
    assert proposal.pull_domain_events() == ()


def test_proposal_id_remains_stable_after_submission() -> None:
    """
    ProposalId debe permanecer estable durante la transición de VS-001.
    """
    proposal = build_proposal()
    proposal.pull_domain_events()

    proposal_id_before_submission = proposal.proposal_id

    proposal.submit(
        submitted_at=SubmittedAt(
            datetime(2026, 8, 26, 6, 35, tzinfo=UTC)
        )
    )

    assert proposal.proposal_id == proposal_id_before_submission


def test_organization_id_remains_stable_after_submission() -> None:
    """
    OrganizationId debe permanecer estable durante el Lifecycle de Proposal.
    """
    proposal = build_proposal()
    proposal.pull_domain_events()

    organization_id_before_submission = proposal.organization_id

    proposal.submit(
        submitted_at=SubmittedAt(
            datetime(2026, 8, 26, 6, 36, tzinfo=UTC)
        )
    )

    assert proposal.organization_id == organization_id_before_submission