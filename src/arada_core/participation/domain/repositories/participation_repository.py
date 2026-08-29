from __future__ import annotations

from abc import ABC, abstractmethod

from arada_core.participation.domain.aggregates.participation import Participation
from arada_core.participation.domain.value_objects.participation_id import (
    ParticipationId,
)
from arada_core.participation.domain.value_objects.participation_version import (
    ParticipationVersion,
)


class ParticipationRepository(ABC):
    """
    Puerto de persistencia para el Aggregate Participation.

    El Repository:

    - recupera Participation por identidad;
    - verifica existencia;
    - persiste el Aggregate completo;
    - soporta concurrencia optimista mediante expected_version;
    - no ejecuta Commands;
    - no aplica reglas de negocio;
    - no modifica ParticipationVersion;
    - no modifica atributos del Aggregate directamente;
    - no incorpora otros Aggregates dentro del límite de consistencia.

    Para una nueva Participation:

        expected_version = None

    Para una Participation existente:

        expected_version = ParticipationVersion(...)

    La implementación concreta pertenece a Infrastructure.
    """

    @abstractmethod
    def get_by_id(
        self,
        participation_id: ParticipationId,
    ) -> Participation | None:
        """Recupera una Participation por su identidad."""

        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        participation_id: ParticipationId,
    ) -> bool:
        """Indica si existe una Participation con la identidad indicada."""

        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        participation: Participation,
        expected_version: ParticipationVersion | None,
    ) -> None:
        """
        Persiste una Participation respetando concurrencia optimista.

        expected_version = None representa la creación de un nuevo Aggregate.

        Cuando expected_version contiene una ParticipationVersion, la
        implementación debe verificar que coincida con la versión persistida
        antes de confirmar la modificación.
        """

        raise NotImplementedError