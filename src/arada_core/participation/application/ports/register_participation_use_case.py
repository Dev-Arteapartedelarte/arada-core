from __future__ import annotations

from abc import ABC, abstractmethod

from arada_core.participation.application.commands.register_participation import (
    RegisterParticipation,
)
from arada_core.participation.application.dto.participation_result import (
    ParticipationResult,
)


class RegisterParticipationUseCase(ABC):
    """
    Puerto de entrada para el caso de uso RegisterParticipation.

    Este contrato representa la operación pública de Application encargada de
    coordinar el registro de una nueva Participation.

    El Use Case Port:

    - recibe un RegisterParticipation;
    - recibe el contexto del actor solicitante;
    - no contiene reglas de dominio;
    - no implementa autorización;
    - no accede directamente a Infrastructure;
    - no modifica otros Aggregates;
    - no expone la Aggregate Root al consumidor;
    - devuelve un ParticipationResult estable para la capa llamadora.

    La implementación concreta corresponde a
    RegisterParticipationService.
    """

    @abstractmethod
    def execute(
        self,
        command: RegisterParticipation,
        *,
        actor_id: str,
    ) -> ParticipationResult:
        """
        Ejecuta la intención de registrar una Participation.

        La implementación debe coordinar:

        - autorización;
        - validación de referencias externas;
        - verificación de identidad duplicada;
        - creación mediante Participation.register(...);
        - persistencia;
        - publicación de Domain Events confirmados;
        - mapping y publicación de Integration Events elegibles.
        """

        raise NotImplementedError