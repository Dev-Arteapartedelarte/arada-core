from abc import ABC, abstractmethod
from collections.abc import Sequence


class IntegrationEventPublisher(ABC):
    """
    Output Port para publicar Integration Events derivados de hechos de Proposal.

    IntegrationEventPublisher define la capacidad que Application utiliza para
    entregar contratos de integración destinados a otros Bounded Contexts o
    sistemas externos.

    Conforme a la arquitectura aprobada de AURA Core:

    - Integration Event no es equivalente a Domain Event;
    - Integration Event no es equivalente a una notificación NGSI-LD;
    - el Aggregate Proposal no publica Integration Events directamente;
    - Domain permanece independiente de FIWARE y de cualquier infraestructura
      de integración;
    - Application puede coordinar la publicación únicamente después de que la
      modificación autoritativa haya sido persistida correctamente;
    - DOMAIN-013 Integration constituye la frontera responsable de adaptar los
      contratos de integración hacia representaciones externas cuando
      corresponda;
    - este Port no conoce Orion, Orion-LD, NGSI-LD, brokers, colas, topics,
      protocolos ni frameworks concretos;
    - este Port no contiene lógica de dominio;
    - este Port no modifica Proposal;
    - este Port no sustituye al Repository.

    Para VS-001 los hechos relevantes pueden originar conceptualmente:

        ProposalCreated
            |
            v
        ProposalCreatedForIntegration

        ProposalSubmitted
            |
            v
        ProposalSubmittedForIntegration

    La construcción concreta de dichos contratos debe respetar
    DOMAIN-007K-Integration-Events.md y mantener únicamente la información
    necesaria para cada propósito de integración.

    Este Port utiliza una secuencia de objetos porque AURA Core todavía no ha
    establecido un tipo base común obligatorio para todos los Integration
    Events. La introducción de una jerarquía física común debe realizarse
    únicamente cuando exista una decisión arquitectónica consolidada.
    """

    @abstractmethod
    def publish(self, events: Sequence[object]) -> None:
        """
        Publica Integration Events previamente construidos por la coordinación
        correspondiente de Application.

        La implementación concreta debe tratar los eventos recibidos como
        contratos ya definidos y no reconstruir reglas pertenecientes al
        Aggregate Proposal.

        La invocación debe producirse respetando la coordinación post-Commit
        establecida por AURA Core.
        """