from abc import ABC, abstractmethod


class AuthorizationPort(ABC):
    """
    Output Port para autorización de operaciones sobre Proposal.

    AuthorizationPort define la capacidad externa que Application necesita
    para determinar si un actor puede intentar ejecutar una operación
    determinada dentro del Bounded Context Proposal.

    Conforme al modelo de seguridad de AURA Core:

    - autenticación y autorización no pertenecen al Aggregate Proposal;
    - Application coordina la verificación de permisos;
    - Proposal conserva la autoridad sobre sus invariantes y State Machine;
    - una autorización válida no obliga al Aggregate a aceptar una operación;
    - una operación autorizada puede seguir siendo inválida para el dominio;
    - un rechazo de autorización impide continuar el caso de uso;
    - el contrato no depende de una tecnología concreta de identidad;
    - el contrato no conoce Keyrock, OAuth2, JWT, FIWARE ni frameworks.

    Para VS-001 las capacidades relevantes son conceptualmente:

        proposal:create
        proposal:submit

    El identificador del actor se mantiene deliberadamente como un valor
    opaco para Application. La resolución concreta de identidad pertenece
    al adapter o mecanismo de seguridad correspondiente.
    """

    @abstractmethod
    def is_authorized(
        self,
        actor_id: str,
        permission: str,
    ) -> bool:
        """
        Determina si un actor posee la permission requerida.

        Retorna True únicamente cuando el actor puede intentar ejecutar la
        operación solicitada.

        Este resultado no reemplaza las decisiones posteriores del Aggregate
        Proposal sobre validez de estado, invariantes o transición.
        """