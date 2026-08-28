from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProposalDescription:
    """
    Descripción formal de una Proposal dentro del dominio AURA.

    ProposalDescription representa información contextual que complementa
    la definición de la iniciativa.

    Conforme al modelo normativo consolidado:

    - pertenece al Aggregate Proposal;
    - complementa ProposalName, ProposalPurpose y ProposalType;
    - no constituye la identidad del Aggregate;
    - no sustituye ProposalPurpose;
    - no ejecuta transiciones por sí misma;
    - no modifica ProposalStatus;
    - no depende de Infrastructure;
    - no depende de mecanismos de persistencia;
    - puede ser requerida únicamente cuando las reglas del dominio
      correspondientes así lo establezcan.

    Este Value Object protege exclusivamente la validez de una descripción
    cuando ésta existe.

    La obligatoriedad de ProposalDescription y las condiciones bajo las
    cuales puede modificarse pertenecen al Aggregate Proposal.
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("ProposalDescription must not be empty.")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value