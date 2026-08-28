from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProposalVersion:
    """
    Versión de concurrencia optimista del Aggregate Proposal.

    ProposalVersion representa la versión lógica utilizada para detectar
    modificaciones concurrentes sobre una Proposal.

    Conforme al modelo normativo de DOMAIN-007I-Versioning.md y
    DOMAIN-007G-Repository-Contract.md:

    - una Proposal persistida comienza en versión 1;
    - la versión es un entero positivo;
    - cada cambio válido del Aggregate produce una nueva versión;
    - la versión no constituye identidad de dominio;
    - la versión no representa ProposalStatus;
    - Application no debe modificarla directamente;
    - Infrastructure no debe inventar transiciones de versión;
    - el Repository utiliza ExpectedVersion para aplicar control de
      concurrencia optimista.

    Este Value Object protege exclusivamente la validez estructural de una
    versión.

    La decisión de cuándo incrementar la versión pertenece al comportamiento
    válido del Aggregate Proposal.
    """

    value: int

    def __post_init__(self) -> None:
        if isinstance(self.value, bool) or not isinstance(self.value, int):
            raise TypeError("ProposalVersion must be an integer.")

        if self.value < 1:
            raise ValueError("ProposalVersion must be greater than or equal to 1.")

    def next(self) -> "ProposalVersion":
        """
        Construye la versión inmediatamente posterior.

        El método no muta la instancia actual y preserva la semántica de
        Value Object inmutable.
        """
        return ProposalVersion(self.value + 1)

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)