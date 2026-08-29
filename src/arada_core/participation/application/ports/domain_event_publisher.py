from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence


class DomainEventPublisher(ABC):
    """
    Puerto de publicación de Domain Events para Participation.

    AURA Core no establece todavía un tipo base común obligatorio para todos
    los Domain Events. Por ello, el contrato trabaja con Sequence[object],
    siguiendo el patrón consolidado en Proposal.

    El publisher:

    - recibe Domain Events ya producidos por el Aggregate;
    - no crea Domain Events;
    - no ejecuta comportamiento de dominio;
    - no modifica Participation;
    - no decide si un evento debe convertirse en Integration Event;
    - no conoce consumidores concretos;
    - no introduce dependencias de Infrastructure en Domain o Application.
    """

    @abstractmethod
    def publish(
        self,
        events: Sequence[object],
    ) -> None:
        """Publica los Domain Events confirmados recibidos."""

        raise NotImplementedError