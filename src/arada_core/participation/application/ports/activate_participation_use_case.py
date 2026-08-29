from __future__ import annotations

from abc import ABC, abstractmethod

from arada_core.participation.application.commands.activate_participation import (
    ActivateParticipation,
)
from arada_core.participation.application.dto.participation_result import (
    ParticipationResult,
)


class ActivateParticipationUseCase(ABC):
    """
    Puerto de entrada para el caso de uso ActivateParticipation.

    Este contrato representa la operación pública de Application encargada de
    coordinar la activación de una Participation previamente registrada.

    El Use Case Port:

    - recibe un ActivateParticipation;
    - recibe el contexto del actor solicitante;
    - no contiene reglas de dominio;
    - no decide la transición Registered -> Active;
    - no implementa autorización;
    - no incrementa ParticipationVersion;
    - no establece StartedAt;
    - no accede directamente a Infrastructure;
    - no expone la Aggregate Root al consumidor;
    - devuelve un ParticipationResult estable para la capa llamadora.

    La implementación concreta corresponde a
    ActivateParticipationService.
    """

    @abstractmethod
    def execute(
        self,
        command: ActivateParticipation,
        *,
        actor_id: str,
    ) -> ParticipationResult:
        """
        Ejecuta la intención de activar una Participation.

        La implementación debe coordinar:

        - autorización;
        - carga de Participation;
        - validación del contexto organizacional;
        - validaciones externas requeridas;
        - ejecución de Participation.activate(...);
        - persistencia con expected_version;
        - publicación de Domain Events confirmados;
        - mapping y publicación de Integration Events elegibles.
        """

        raise NotImplementedError