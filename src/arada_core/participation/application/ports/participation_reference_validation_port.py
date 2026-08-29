from __future__ import annotations

from abc import ABC, abstractmethod

from arada_core.participation.domain.value_objects.organization_id import OrganizationId


class ParticipationReferenceValidationPort(ABC):
    """
    Puerto de validación de referencias externas utilizadas por Participation.

    Este contrato permite que Application valide referencias pertenecientes a
    otros Aggregates sin incorporarlos dentro del Consistency Boundary de
    Participation.

    El puerto:

    - valida referencias externas necesarias para los casos de uso;
    - no modifica Aggregates externos;
    - no devuelve Aggregates mutables;
    - no contiene reglas internas de Participation;
    - no ejecuta Commands;
    - no persiste Participation;
    - no publica Domain Events;
    - no publica Integration Events;
    - no introduce dependencias de Infrastructure en Domain.

    VS-001 requiere únicamente la validación explícita de OrganizationId.

    Las referencias adicionales como CitizenId, MembershipId, TerritoryId,
    AssemblyId, ProposalId o VotingId no se incorporan a este contrato hasta
    que un caso de uso del slice las requiera de forma efectiva.
    """

    @abstractmethod
    def validate_organization(
        self,
        organization_id: OrganizationId,
    ) -> None:
        """
        Valida que OrganizationId corresponda a una Organization válida para
        ejecutar el caso de uso de Participation.

        La implementación debe rechazar la referencia cuando no pueda
        considerarse válida según el contrato de integración correspondiente.

        Esta operación no modifica Organization.
        """

        raise NotImplementedError