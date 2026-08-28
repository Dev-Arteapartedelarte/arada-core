from dataclasses import dataclass

from arada_core.proposal.domain.value_objects.citizen_id import CitizenId
from arada_core.proposal.domain.value_objects.membership_id import MembershipId


@dataclass(frozen=True, slots=True)
class ProposerReference:
    """
    Referencia de dominio al proponente de una Proposal.

    ProposerReference encapsula la referencia mediante la cual Proposal
    identifica al actor de dominio que origina o presenta formalmente una
    iniciativa.

    Conforme al modelo normativo consolidado:

    - puede representar un CitizenId;
    - puede representar un MembershipId;
    - mantiene únicamente una referencia hacia un Aggregate externo;
    - no incorpora Citizen ni Membership dentro de Proposal;
    - no transfiere comportamiento desde otros Bounded Contexts;
    - no ejecuta autorización;
    - no valida permisos técnicos;
    - no depende de Infrastructure;
    - no depende de mecanismos de persistencia.

    La interpretación concreta de la referencia depende del contexto
    organizacional aplicable.

    Las validaciones que requieran consultar Citizen o Membership deben
    resolverse fuera del Aggregate Proposal antes de ejecutar el
    comportamiento correspondiente.
    """

    value: CitizenId | MembershipId

    def __post_init__(self) -> None:
        if not isinstance(self.value, (CitizenId, MembershipId)):
            raise TypeError(
                "ProposerReference must contain a CitizenId or MembershipId."
            )

    @property
    def is_citizen(self) -> bool:
        """Indica si la referencia corresponde a un Citizen."""
        return isinstance(self.value, CitizenId)

    @property
    def is_membership(self) -> bool:
        """Indica si la referencia corresponde a una Membership."""
        return isinstance(self.value, MembershipId)

    def __str__(self) -> str:
        return str(self.value)