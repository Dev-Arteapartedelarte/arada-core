"""
Integration Events de Application para el Bounded Context Proposal.

Este paquete contiene los contratos públicos de integración derivados de
hechos confirmados del Aggregate Proposal.

Conforme a DOMAIN-007K y a la decisión arquitectónica aprobada para VS-001:

    Domain Event
        !=
    Integration Event
        !=
    API Contract

Los Integration Events:

- pertenecen a la frontera de Application del Bounded Context productor;
- representan contratos de interoperabilidad;
- se derivan únicamente de hechos de dominio confirmados;
- se construyen después del Commit exitoso;
- poseen versionado explícito;
- exponen únicamente la información contractual necesaria;
- no contienen el Aggregate Proposal completo;
- no permiten modificar directamente Proposal;
- permanecen independientes de Infrastructure;
- permanecen independientes de FIWARE y NGSI-LD;
- pueden ser consumidos posteriormente por DOMAIN-013 Integration;
- pueden ser adaptados a representaciones externas sin modificar su
  semántica.

VS-001 incorpora exclusivamente los contratos derivados de los hechos que
forman parte de su alcance:

    ProposalCreated
        -> ProposalCreatedForIntegration

    ProposalSubmitted
        -> ProposalSubmittedForIntegration

La existencia de un Domain Event no implica automáticamente publicación
externa. La selección de hechos relevantes pertenece a Application y debe
respetar DOMAIN-007K.

No se exportan símbolos desde este initializer para evitar acoplar el paquete
a módulos que puedan evolucionar de forma independiente y para mantener
imports explícitos en los consumidores.
"""