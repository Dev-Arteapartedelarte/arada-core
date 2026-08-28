from abc import ABC, abstractmethod
from collections.abc import Sequence


class DomainEventPublisher(ABC):
    """
    Output Port para publicar Domain Events producidos por Proposal.

    DomainEventPublisher define la capacidad que Application utiliza para
    entregar a mecanismos externos los Domain Events que ya fueron producidos
    por comportamiento válido del Aggregate Proposal.

    Conforme a la arquitectura de AURA Core:

    - los Domain Events son producidos por el Aggregate;
    - Application no crea Domain Events en nombre del Aggregate;
    - Application coordina su publicación;
    - la publicación debe respetar la frontera transaccional definida por el
      caso de uso;
    - un Domain Event representa un hecho ocurrido dentro del dominio;
    - Domain Event no es equivalente a Integration Event;
    - Domain Event no es equivalente a una notificación NGSI-LD;
    - este contrato no depende de un broker, bus, protocolo o framework
      concreto;
    - este contrato no contiene lógica de dominio;
    - este contrato no modifica Proposal;
    - este contrato no ejecuta persistencia del Aggregate.

    Para VS-001 pueden publicarse, como consecuencia de comportamiento válido:

        ProposalCreated
        ProposalSubmitted

    El tipo concreto de cada evento permanece definido por Domain.

    Este Port utiliza una secuencia de objetos porque AURA Core todavía no ha
    establecido un tipo base común obligatorio para todos los Domain Events.
    Introducir una jerarquía artificial desde Application violaría la
    dependencia hacia Domain y añadiría una abstracción no consolidada.

    Cuando el Shared Kernel establezca formalmente un contrato común para
    Domain Events, esta firma podrá especializarse sin alterar la
    responsabilidad arquitectónica del Port.
    """

    @abstractmethod
    def publish(self, events: Sequence[object]) -> None:
        """
        Publica Domain Events previamente producidos por el Aggregate.

        La implementación concreta debe preservar el orden recibido cuando
        dicho orden sea relevante para la secuencia de hechos del Aggregate.

        Este método no debe reinterpretar, reconstruir ni reemplazar los
        eventos producidos por Domain.
        """