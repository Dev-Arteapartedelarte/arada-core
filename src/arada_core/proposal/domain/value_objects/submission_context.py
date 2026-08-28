from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SubmissionContext:
    """
    Contexto asociado a la presentación formal de una Proposal.

    SubmissionContext representa información contextual propia del acto de
    presentación cuando dicha información debe quedar registrada como parte
    del estado del Aggregate Proposal.

    Conforme al modelo normativo consolidado:

    - pertenece conceptualmente a la información de presentación;
    - puede registrarse cuando una Proposal es presentada;
    - no constituye la identidad del Aggregate;
    - no sustituye SubmittedAt;
    - no sustituye la referencia al proponente;
    - no sustituye TerritoryId ni AssemblyId;
    - no representa autorización;
    - no ejecuta transiciones de Lifecycle;
    - no modifica ProposalStatus por sí mismo;
    - no produce Domain Events;
    - no incorpora Aggregates externos;
    - no depende de Infrastructure;
    - no depende de mecanismos de persistencia.

    El modelo normativo establece SubmissionContext como concepto de dominio,
    pero no define todavía una estructura interna especializada para VS-001.

    Por esta razón, esta implementación mantiene deliberadamente una
    representación textual mínima y opaca, evitando introducir categorías,
    atributos o relaciones que no hayan sido consolidados documentalmente.

    Si posteriormente el dominio formaliza una estructura específica para el
    contexto de presentación, este Value Object deberá evolucionar mediante
    una decisión explícita del modelo y no por necesidades particulares de
    Infrastructure.

    Este Value Object protege exclusivamente la validez estructural del valor
    cuando SubmissionContext existe.
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("SubmissionContext must not be empty.")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value