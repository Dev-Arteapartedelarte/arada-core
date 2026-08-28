from dataclasses import dataclass

from arada_core.proposal.domain.value_objects.proposal_id import ProposalId
from arada_core.proposal.domain.value_objects.proposal_version import ProposalVersion


@dataclass(frozen=True, slots=True)
class SubmitProposal:
    """
    Intención de presentar formalmente una Proposal existente.

    SubmitProposal transporta exclusivamente la información necesaria para
    identificar el Aggregate y aplicar control de concurrencia optimista
    durante el caso de uso de presentación de VS-001.

    El Command:

    - expresa intención y no un hecho consumado;
    - identifica la Proposal mediante ProposalId;
    - declara la ExpectedVersion observada por el consumidor;
    - no decide si el actor está autorizado;
    - no modifica ProposalStatus;
    - no incrementa ProposalVersion;
    - no establece SubmittedAt;
    - no produce ProposalSubmitted;
    - no ejecuta persistencia;
    - no contiene lógica de dominio;
    - no depende de Infrastructure.

    Application debe:

    - resolver autorización mediante la capacidad correspondiente;
    - recuperar el Aggregate completo mediante ProposalRepository;
    - resolver las validaciones externas necesarias;
    - delegar la transición al Aggregate Proposal;
    - persistir utilizando ExpectedVersion;
    - coordinar únicamente después del Commit los efectos externos
      correspondientes.

    La ExpectedVersion forma parte de la intención de escritura y permite
    impedir actualizaciones silenciosas basadas en una versión obsoleta.
    """

    proposal_id: ProposalId
    expected_version: ProposalVersion