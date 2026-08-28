from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from arada_core.proposal.domain.value_objects.proposal_id import ProposalId
from arada_core.proposal.domain.value_objects.proposal_version import ProposalVersion

if TYPE_CHECKING:
    from arada_core.proposal.domain.aggregates.proposal import Proposal


class ProposalRepository(ABC):
    """
    Contrato de persistencia del Aggregate Proposal.

    ProposalRepository define exclusivamente las operaciones necesarias para
    recuperar, verificar existencia y persistir la unidad completa de
    consistencia Proposal.

    Conforme a DOMAIN-007G-Repository-Contract.md y CORE-011:

    - el contrato pertenece a Domain;
    - la implementación pertenece a Infrastructure;
    - opera sobre el Aggregate Root completo;
    - no expone ORM, SQL, tablas, documentos ni detalles de almacenamiento;
    - no sustituye Read Models;
    - no permite persistencia parcial del Aggregate;
    - utiliza Version para soportar concurrencia optimista;
    - una escritura condicionada debe comparar la versión persistida con la
      ExpectedVersion recibida.

    La implementación concreta debe rechazar una escritura cuando la versión
    persistida no coincida con ExpectedVersion.

    El Repository no decide transiciones, no incrementa Version y no produce
    Domain Events en nombre del Aggregate.
    """

    @abstractmethod
    def get_by_id(self, proposal_id: ProposalId) -> "Proposal | None":
        """
        Recupera una Proposal completa por su identidad.

        Retorna None cuando no existe una Proposal asociada al ProposalId
        solicitado.
        """

    @abstractmethod
    def exists(self, proposal_id: ProposalId) -> bool:
        """
        Determina si existe una Proposal identificada por ProposalId.

        Esta operación no reemplaza la recuperación del Aggregate cuando el
        caso de uso requiere ejecutar comportamiento de dominio.
        """

    @abstractmethod
    def save(
        self,
        proposal: "Proposal",
        expected_version: ProposalVersion | None,
    ) -> None:
        """
        Persiste la unidad completa de consistencia Proposal.

        expected_version representa la versión que el consumidor espera
        encontrar actualmente persistida.

        Para una nueva Proposal puede no existir una versión persistida previa,
        por lo que expected_version puede ser None.

        Para una Proposal existente, la implementación debe aplicar control de
        concurrencia optimista y rechazar la escritura si la versión almacenada
        difiere de expected_version.

        El Repository no modifica el estado del Aggregate ni incrementa su
        Version.
        """