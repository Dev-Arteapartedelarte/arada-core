from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class SubmittedAt:
    """
    Momento en que una Proposal fue presentada formalmente.

    SubmittedAt representa, dentro del Bounded Context Proposal, el instante
    asociado al hecho de presentación de una iniciativa.

    Conforme al modelo normativo consolidado:

    - forma parte de la información conceptual de presentación;
    - se establece como consecuencia de una presentación válida;
    - no constituye la identidad del Aggregate;
    - no controla ProposalStatus;
    - no ejecuta transiciones por sí mismo;
    - no sustituye al Domain Event ProposalSubmitted;
    - no depende de Infrastructure;
    - no depende del mecanismo de persistencia.

    La decisión de cuándo establecer SubmittedAt pertenece al comportamiento
    del Aggregate Proposal durante una transición válida hacia Submitted.

    Este Value Object protege exclusivamente la validez estructural del
    instante registrado y no introduce reglas temporales adicionales no
    definidas por el dominio.
    """

    value: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.value, datetime):
            raise TypeError("SubmittedAt must contain a datetime.")

    def __str__(self) -> str:
        return self.value.isoformat()