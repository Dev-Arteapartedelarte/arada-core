from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProposalId:
    """
    Identidad estable del Aggregate Proposal.

    ProposalId representa el identificador único de una Proposal dentro del
    Bounded Context Proposal Management.

    Conforme al modelo normativo de AURA Core:

    - identifica de forma única al Aggregate;
    - es inmutable;
    - permanece estable durante todo el Lifecycle;
    - no depende de Infrastructure;
    - no depende del mecanismo de persistencia;
    - no depende de ProposalStatus;
    - no depende de atributos descriptivos;
    - no puede reutilizarse como consecuencia de una transición de estado.

    La generación y garantía global de unicidad pertenecen a la coordinación
    correspondiente y no forman parte de este Value Object.
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("ProposalId must not be empty.")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value