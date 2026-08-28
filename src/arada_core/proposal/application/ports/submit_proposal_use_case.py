from abc import ABC, abstractmethod

from arada_core.proposal.application.commands.submit_proposal import SubmitProposal
from arada_core.proposal.application.dto.proposal_result import ProposalResult
from arada_core.proposal.domain.value_objects.submitted_at import SubmittedAt


class SubmitProposalUseCase(ABC):
    """
    Input Port del caso de uso SubmitProposal.

    SubmitProposalUseCase define la capacidad que Application expone a los
    adapters de entrada para solicitar la presentación formal de una Proposal
    existente.

    Conforme al patrón físico aprobado para los Vertical Slices de AURA Core:

        <Verb><Aggregate>UseCase

    este contrato:

    - pertenece a Application;
    - representa una capacidad de entrada;
    - recibe una intención mediante SubmitProposal;
    - recibe la identidad del actor que intenta ejecutar el caso de uso;
    - recibe el instante de presentación necesario para registrar el hecho;
    - devuelve un resultado de Application mediante ProposalResult;
    - no expone directamente el Aggregate Proposal;
    - no implementa autorización;
    - no implementa invariantes;
    - no reproduce la State Machine;
    - no modifica ProposalStatus directamente;
    - no incrementa ProposalVersion directamente;
    - no produce ProposalSubmitted;
    - no ejecuta persistencia;
    - no conoce Infrastructure;
    - no conoce HTTP, CLI, mensajería ni otros mecanismos de entrada;
    - es implementado por SubmitProposalService.

    La identidad del actor pertenece al contexto de ejecución del caso de uso
    y permanece separada de la intención funcional expresada por
    SubmitProposal.

    SubmittedAt representa el instante utilizado por el comportamiento de
    dominio para registrar una presentación válida. El Input Port no decide
    por sí mismo si la transición puede ocurrir.

    Debe mantenerse:

        intención funcional
            !=
        contexto de seguridad
            !=
        decisión de dominio

    La ExpectedVersion permanece dentro de SubmitProposal porque forma parte
    de la intención de escritura sometida a control de concurrencia optimista.

    Los adapters de entrada deben depender de este contrato y no de una
    implementación concreta del caso de uso.

    La firma pública del Input Port debe permanecer compatible con la firma de
    SubmitProposalService para que la abstracción represente exactamente la
    capacidad implementada.
    """

    @abstractmethod
    def execute(
        self,
        command: SubmitProposal,
        *,
        actor_id: str,
        submitted_at: SubmittedAt,
    ) -> ProposalResult:
        """
        Ejecuta la capacidad de presentación formal de Proposal.

        Parameters
        ----------
        command:
            Intención funcional de presentar una Proposal existente,
            incluyendo ProposalId y ExpectedVersion.

        actor_id:
            Identidad opaca del actor que intenta ejecutar el caso de uso.
            Application utiliza este valor para coordinar autorización mediante
            AuthorizationPort.

        submitted_at:
            Instante de presentación entregado al comportamiento del Aggregate
            cuando la operación resulta válida.

        Returns
        -------
        ProposalResult
            Representación de Application del estado resultante sin exponer
            directamente el Aggregate Proposal.

        La implementación concreta debe coordinar autorización, recuperación,
        validaciones externas, comportamiento de dominio, persistencia con
        ExpectedVersion y efectos post-Commit sin trasladar reglas del
        Aggregate hacia Application.
        """