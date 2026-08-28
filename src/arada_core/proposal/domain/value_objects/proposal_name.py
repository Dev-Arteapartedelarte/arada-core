from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProposalName:
    """
    Nombre canónico de una Proposal dentro del dominio AURA.

    ProposalName representa el término oficial utilizado para identificar
    descriptivamente una Proposal.

    Conforme al modelo normativo consolidado:

    - pertenece al Aggregate Proposal;
    - no constituye la identidad del Aggregate;
    - debe poseer un valor válido;
    - puede participar en las invariantes de creación y presentación;
    - puede modificarse únicamente mediante comportamiento válido del
      Aggregate y cuando el Lifecycle lo permita;
    - no debe representarse mediante términos divergentes como Title o
      ProposalTitle.

    Este Value Object protege únicamente las reglas propias de su valor.

    Las reglas relativas a estados, transiciones y condiciones bajo las cuales
    ProposalName puede modificarse pertenecen al Aggregate Proposal.
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("ProposalName must not be empty.")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value