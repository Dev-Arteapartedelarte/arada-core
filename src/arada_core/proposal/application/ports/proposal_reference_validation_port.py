from abc import ABC, abstractmethod

from arada_core.proposal.domain.value_objects.assembly_id import AssemblyId
from arada_core.proposal.domain.value_objects.organization_id import OrganizationId
from arada_core.proposal.domain.value_objects.proposer_reference import (
    ProposerReference,
)
from arada_core.proposal.domain.value_objects.territory_id import TerritoryId


class ProposalReferenceValidationPort(ABC):
    """
    Output Port para validar referencias externas utilizadas por Proposal.

    ProposalReferenceValidationPort define la capacidad externa que
    Application necesita para comprobar referencias pertenecientes a otros
    Bounded Contexts antes de ejecutar comportamiento sobre el Aggregate
    Proposal.

    Conforme a los límites de consistencia de AURA Core:

    - Proposal no carga Aggregates externos;
    - Proposal conserva únicamente identificadores o referencias estables;
    - las validaciones que requieren consultar otros Bounded Contexts se
      resuelven fuera del Aggregate;
    - Application coordina dichas validaciones mediante este Port;
    - el contrato no incorpora Organization, Citizen, Membership, Territory
      ni Assembly dentro de Proposal;
    - el contrato no transfiere reglas pertenecientes a esos Aggregates;
    - el contrato no ejecuta autorización;
    - el contrato no depende de Infrastructure;
    - el contrato no conoce APIs, bases de datos, FIWARE, NGSI-LD ni
      mecanismos concretos de integración.

    Para VS-001, las referencias externas relevantes son:

        OrganizationId
        ProposerReference
        TerritoryId, cuando corresponda
        AssemblyId, cuando corresponda

    La implementación concreta debe resolver la verificación contra las
    fuentes autoritativas correspondientes sin convertir este Port en una
    frontera de consistencia distribuida.
    """

    @abstractmethod
    def validate_organization(
        self,
        organization_id: OrganizationId,
    ) -> bool:
        """
        Determina si la referencia OrganizationId es válida para continuar
        con el caso de uso.
        """

    @abstractmethod
    def validate_proposer(
        self,
        proposer_reference: ProposerReference,
        organization_id: OrganizationId,
    ) -> bool:
        """
        Determina si la referencia del proponente es válida dentro del
        contexto organizacional requerido por el caso de uso.
        """

    @abstractmethod
    def validate_territory(
        self,
        territory_id: TerritoryId,
    ) -> bool:
        """
        Determina si una referencia TerritoryId existente es válida.
        """

    @abstractmethod
    def validate_assembly(
        self,
        assembly_id: AssemblyId,
        organization_id: OrganizationId,
    ) -> bool:
        """
        Determina si una referencia AssemblyId existente es válida dentro del
        contexto requerido por el caso de uso.
        """