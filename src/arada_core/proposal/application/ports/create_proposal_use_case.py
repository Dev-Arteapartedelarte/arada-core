from abc import ABC, abstractmethod

from arada_core.proposal.application.commands.create_proposal import CreateProposal
from arada_core.proposal.application.dto.proposal_result import ProposalResult


class CreateProposalUseCase(ABC):
    """
    Input Port del caso de uso CreateProposal.

    CreateProposalUseCase define la capacidad que Application expone a los
    adapters de entrada para solicitar la creación de una nueva Proposal.

    Conforme al patrón físico aprobado para los Vertical Slices de AURA Core:

        <Verb><Aggregate>UseCase

    este contrato:

    - pertenece a Application;
    - representa una capacidad de entrada;
    - recibe una intención mediante CreateProposal;
    - recibe la identidad del actor que intenta ejecutar el caso de uso;
    - devuelve un resultado de Application mediante ProposalResult;
    - no expone el Aggregate Proposal;
    - no implementa autorización;
    - no implementa invariantes;
    - no ejecuta directamente comportamiento de dominio;
    - no ejecuta persistencia;
    - no conoce Infrastructure;
    - no conoce HTTP, CLI, mensajería ni otros mecanismos de entrada;
    - es implementado por CreateProposalService.

    La identidad del actor forma parte del contexto de ejecución del caso de
    uso y no del Command de dominio funcional.

    Mantener actor_id fuera de CreateProposal evita mezclar:

        intención funcional
            !=
        contexto de seguridad

    Los adapters de entrada deben depender de este contrato y no de una
    implementación concreta del caso de uso.

    La firma pública del Input Port debe permanecer compatible con la firma de
    su Application Service. Esto evita que la abstracción declare una
    capacidad diferente de la que realmente implementa CreateProposalService.
    """

    @abstractmethod
    def execute(
        self,
        command: CreateProposal,
        *,
        actor_id: str,
    ) -> ProposalResult:
        """
        Ejecuta la capacidad de creación de Proposal.

        Parameters
        ----------
        command:
            Intención funcional de crear la Proposal.

        actor_id:
            Identidad opaca del actor que intenta ejecutar el caso de uso.
            Application utiliza este valor únicamente para coordinar la
            autorización mediante AuthorizationPort.

        Returns
        -------
        ProposalResult
            Representación de Application del resultado exitoso sin exponer
            directamente el Aggregate Proposal.

        La implementación concreta debe coordinar el caso de uso sin trasladar
        reglas de negocio desde el Aggregate Proposal hacia Application.
        """