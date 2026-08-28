from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CitizenId:
    """
    Referencia estable a un Citizen relacionado con una Proposal.

    CitizenId representa, dentro del Bounded Context Proposal, la identidad
    externa del Citizen que puede actuar como origen ciudadano de la
    iniciativa.

    Conforme al modelo normativo consolidado:

    - referencia un Aggregate Citizen independiente;
    - no incorpora el Aggregate Citizen dentro de Proposal;
    - no transfiere estado ni comportamiento de Citizen;
    - no permite modificar Citizen desde Proposal;
    - preserva la separación entre Consistency Boundaries;
    - puede formar parte de la referencia conceptual al proponente;
    - no depende de Infrastructure;
    - no depende de mecanismos de persistencia.

    Proposal conserva únicamente la referencia necesaria para identificar
    al Citizen cuando corresponda.

    Las validaciones que requieran consultar el Bounded Context Citizen
    deben resolverse fuera del Aggregate Proposal antes de ejecutar el
    comportamiento correspondiente.

    Este Value Object protege exclusivamente la validez estructural de la
    referencia mantenida por Proposal.
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("CitizenId must not be empty.")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value