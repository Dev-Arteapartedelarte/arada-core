from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence


class IntegrationEventPublisher(ABC):
    """
    Puerto de publicación de Integration Events para Participation.

    AURA Core no establece todavía un tipo base común obligatorio para todos
    los Integration Events. Por ello, el contrato trabaja con
    Sequence[object], siguiendo el patrón consolidado en Proposal.

    El publisher:

    - recibe Integration Events ya construidos por Application;
    - no crea Integration Events;
    - no ejecuta comportamiento de dominio;
    - no modifica Participation;
    - no transforma Domain Events;
    - no decide qué Domain Events son publicables;
    - no conoce consumidores concretos;
    - no introduce dependencias de Infrastructure en Domain o Application.

    La selección y transformación de Domain Events hacia Integration Events
    corresponde al mapper explícito del Bounded Context Participation.
    """

    @abstractmethod
    def publish(
        self,
        events: Sequence[object],
    ) -> None:
        """Publica los Integration Events confirmados recibidos."""

        raise NotImplementedError