from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProposalPurpose:
    """
    Propósito formal de una Proposal dentro del dominio AURA.

    ProposalPurpose representa la finalidad que busca alcanzar la iniciativa.

    Conforme al modelo normativo consolidado:

    - pertenece al estado del Aggregate Proposal;
    - expresa la finalidad formal de la iniciativa;
    - debe encontrarse definido cuando las reglas del dominio lo exijan;
    - participa en las invariantes de creación y presentación;
    - no representa una Assembly;
    - no representa una Participation;
    - no representa una Voting;
    - no representa el resultado de una Voting;
    - puede permanecer estable aunque Proposal participe posteriormente
      en otros procesos del dominio.

    Este Value Object protege únicamente las reglas propias de su valor.

    Las reglas relativas a estados, transiciones, obligatoriedad contextual
    y condiciones de modificación pertenecen al Aggregate Proposal.
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("ProposalPurpose must not be empty.")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value