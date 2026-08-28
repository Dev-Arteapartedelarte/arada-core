from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrganizationId:
    """
    Referencia estable a la Organization propietaria de una Proposal.

    OrganizationId representa, dentro del Bounded Context Proposal,
    la identidad externa de la Organization a la que pertenece la
    iniciativa.

    Conforme al modelo normativo consolidado:

    - es obligatoria para una Proposal;
    - identifica una única Organization;
    - permanece estable durante todo el Lifecycle del Aggregate;
    - no puede modificarse mediante comportamiento de Proposal;
    - no incorpora el Aggregate Organization;
    - no permite modificar Organization desde Proposal;
    - preserva la separación entre Consistency Boundaries;
    - no depende de Infrastructure;
    - no depende de mecanismos de persistencia.

    Proposal conserva únicamente la referencia OrganizationId.

    Las validaciones que requieran consultar el Bounded Context Organization
    deben resolverse fuera del Aggregate Proposal antes de ejecutar el
    comportamiento correspondiente.

    Este Value Object protege exclusivamente la validez estructural de la
    referencia mantenida por Proposal.
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("OrganizationId must not be empty.")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value