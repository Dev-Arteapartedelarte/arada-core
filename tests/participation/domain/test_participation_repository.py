from __future__ import annotations

from typing import cast

import pytest

from arada_core.participation.domain.aggregates.participation import Participation
from arada_core.participation.domain.repositories.participation_repository import (
    ParticipationRepository,
)
from arada_core.participation.domain.value_objects.participation_id import (
    ParticipationId,
)
from arada_core.participation.domain.value_objects.participation_version import (
    ParticipationVersion,
)


class StubParticipationRepository(ParticipationRepository):
    def get_by_id(
        self,
        participation_id: ParticipationId,
    ) -> Participation | None:
        raise NotImplementedError

    def exists(
        self,
        participation_id: ParticipationId,
    ) -> bool:
        raise NotImplementedError

    def save(
        self,
        participation: Participation,
        expected_version: ParticipationVersion | None,
    ) -> None:
        raise NotImplementedError


def test_participation_repository_is_abstract_contract() -> None:
    assert issubclass(ParticipationRepository, object)


def test_participation_repository_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        ParticipationRepository()


def test_repository_contract_exposes_get_by_id() -> None:
    repository = StubParticipationRepository()

    assert callable(repository.get_by_id)


def test_repository_contract_exposes_exists() -> None:
    repository = StubParticipationRepository()

    assert callable(repository.exists)


def test_repository_contract_exposes_save() -> None:
    repository = StubParticipationRepository()

    assert callable(repository.save)


def test_get_by_id_contract_accepts_participation_id() -> None:
    repository = StubParticipationRepository()
    participation_id = ParticipationId("PAR-001")

    with pytest.raises(NotImplementedError):
        repository.get_by_id(participation_id)


def test_exists_contract_accepts_participation_id() -> None:
    repository = StubParticipationRepository()
    participation_id = ParticipationId("PAR-001")

    with pytest.raises(NotImplementedError):
        repository.exists(participation_id)


def test_save_contract_accepts_none_expected_version_for_creation() -> None:
    repository = StubParticipationRepository()

    participation = cast(Participation, object())

    with pytest.raises(NotImplementedError):
        repository.save(
            participation,
            expected_version=None,
        )


def test_save_contract_accepts_expected_version_for_existing_aggregate() -> None:
    repository = StubParticipationRepository()

    participation = cast(Participation, object())
    expected_version = ParticipationVersion(1)

    with pytest.raises(NotImplementedError):
        repository.save(
            participation,
            expected_version=expected_version,
        )