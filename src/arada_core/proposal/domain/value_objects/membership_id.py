from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MembershipId:
    """
    Referencia estable a una Membership relacionada con una Proposal.

    MembershipId representa, dentro del Bounded Context Proposal, la
    identidad externa de una Membership que puede participar en la
    identificación contextual del proponente.

    Conforme al modelo normativo consolidado:

    - referencia un Aggregate Membership independiente;
    - no incorpora el Aggregate Membership dentro de Proposal;
    - no transfiere estado ni comportamiento de Membership;
    - no permite modificar Membership desde Proposal;
    - preserva la separación entre Consistency Boundaries;
    - puede formar parte de la referencia conceptual al proponente;
    - no depende de Infrastructure;
    - no depende de mecanismos de persistencia.

    Proposal conserva únicamente la referencia necesaria para identificar
    la Membership cuando corresponda.

    Las validaciones que requieran consultar el Bounded Context Membership
    deben resolverse fuera del Aggregate Proposal antes de ejecutar el
    comportamiento correspondiente.

    Este Value Object protege exclusivamente la validez estructural de la
    referencia mantenida por Proposal.
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("MembershipId must not be empty.")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value