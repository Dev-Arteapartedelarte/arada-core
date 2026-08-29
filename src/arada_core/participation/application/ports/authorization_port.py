from __future__ import annotations

from abc import ABC, abstractmethod


class AuthorizationPort(ABC):
    """
    Puerto de autorización utilizado por los casos de uso de Participation.

    La autorización pertenece a Application y permanece separada de las
    invariantes y reglas internas del Aggregate.

    Debe mantenerse:

        Authorization
        !=
        Domain Validation

    Un actor autorizado todavía puede recibir rechazo por:

    - estado inválido;
    - violación de invariantes;
    - conflicto de Version;
    - Organization incorrecta;
    - referencias externas inválidas.

    El puerto no conoce Infrastructure ni mecanismos concretos de identidad.
    """

    @abstractmethod
    def is_authorized(
        self,
        actor_id: str,
        permission: str,
    ) -> bool:
        """
        Determina si el actor posee la Permission indicada.

        El valor de permission debe corresponder al lenguaje autorizado por
        Participation para el caso de uso que realiza la evaluación.
        """

        raise NotImplementedError