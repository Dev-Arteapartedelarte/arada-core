"""
Aggregates del Bounded Context Proposal.

Este paquete contiene los Aggregate Roots responsables de proteger la
consistencia transaccional y las invariantes propias del dominio Proposal.

Para VS-001, Proposal constituye el Aggregate Root y la única frontera de
consistencia del flujo:

    Nonexistent
        |
        | CreateProposal
        v
    Draft
        |
        | SubmitProposal
        v
    Submitted

El Aggregate Proposal es responsable de:

- proteger sus invariantes;
- controlar sus transiciones de estado;
- decidir cuándo un comportamiento es válido;
- producir Domain Events como consecuencia de hechos válidos;
- mantener coherencia de su versión lógica;
- impedir mutaciones directas de ProposalStatus;
- preservar una única frontera de consistencia por Commit.

El Aggregate no debe:

- autorizar actores;
- consultar otros Bounded Contexts;
- acceder a Infrastructure;
- ejecutar persistencia;
- publicar Integration Events directamente;
- depender de FIWARE, NGSI-LD o mecanismos de transporte;
- utilizar Read Models como fuente autoritativa.

Los símbolos públicos se exportarán únicamente cuando sus implementaciones
correspondientes hayan sido creadas y verificadas.
"""