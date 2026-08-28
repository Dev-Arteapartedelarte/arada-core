from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssemblyId:
    """
    Referencia estable a una Assembly relacionada con una Proposal.

    AssemblyId representa, dentro del Bounded Context Proposal, la identidad
    externa de la Assembly con la que una iniciativa puede relacionarse
    cuando el contexto del dominio así lo requiera.

    Conforme al modelo normativo consolidado:

    - referencia un Aggregate Assembly independiente;
    - no incorpora el Aggregate Assembly dentro de Proposal;
    - no transfiere estado ni comportamiento de Assembly;
    - no permite modificar Assembly desde Proposal;
    - preserva la separación entre Consistency Boundaries;
    - puede formar parte del contexto de una Proposal cuando corresponda;
    - no constituye la identidad del Aggregate Proposal;
    - no depende de Infrastructure;
    - no depende de mecanismos de persistencia.

    Proposal conserva únicamente la referencia AssemblyId cuando exista una
    relación válida con una Assembly.

    Las validaciones que requieran consultar el Bounded Context Assembly
    deben resolverse fuera del Aggregate Proposal antes de ejecutar el
    comportamiento correspondiente.

    Este Value Object protege exclusivamente la validez estructural de la
    referencia mantenida por Proposal.
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("AssemblyId must not be empty.")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value