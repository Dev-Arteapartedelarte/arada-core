from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TerritoryId:
    """
    Referencia estable a un Territory relacionado con una Proposal.

    TerritoryId representa, dentro del Bounded Context Proposal, la identidad
    externa del Territory que puede proporcionar contexto territorial a la
    iniciativa.

    Conforme al modelo normativo consolidado:

    - referencia un Aggregate Territory independiente;
    - no incorpora el Aggregate Territory dentro de Proposal;
    - no transfiere estado ni comportamiento de Territory;
    - no permite modificar Territory desde Proposal;
    - preserva la separación entre Consistency Boundaries;
    - puede formar parte del contexto de una Proposal cuando corresponda;
    - no constituye la identidad del Aggregate Proposal;
    - no depende de Infrastructure;
    - no depende de mecanismos de persistencia.

    Proposal conserva únicamente la referencia TerritoryId cuando el contexto
    territorial forma parte de la iniciativa.

    Las validaciones que requieran consultar el Bounded Context Territory
    deben resolverse fuera del Aggregate Proposal antes de ejecutar el
    comportamiento correspondiente.

    Este Value Object protege exclusivamente la validez estructural de la
    referencia mantenida por Proposal.
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("TerritoryId must not be empty.")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value