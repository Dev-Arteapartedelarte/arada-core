from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProposalContent:
    """
    Contenido propio de una Proposal dentro del dominio AURA.

    ProposalContent representa la información que desarrolla la iniciativa
    y permanece dentro del límite conceptual del Aggregate Proposal.

    Conforme al modelo normativo consolidado:

    - pertenece al Aggregate Proposal;
    - representa contenido propio de la iniciativa;
    - puede complementar ProposalName, ProposalPurpose y
      ProposalDescription;
    - no constituye la identidad del Aggregate;
    - no sustituye ProposalPurpose;
    - no incorpora otros Aggregates;
    - no ejecuta transiciones por sí mismo;
    - no modifica ProposalStatus directamente;
    - no depende de Infrastructure;
    - no depende de mecanismos de persistencia.

    Este Value Object protege exclusivamente las reglas propias de su valor.

    Las condiciones bajo las cuales ProposalContent puede crearse o
    modificarse pertenecen al Aggregate Proposal y deben respetar Lifecycle,
    State Machine e invariantes.
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("ProposalContent must not be empty.")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value