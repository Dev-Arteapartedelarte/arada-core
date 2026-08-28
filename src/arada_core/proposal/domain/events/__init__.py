"""
Domain Events del Bounded Context Proposal.

Este paquete contiene los hechos de dominio producidos por el Aggregate
Proposal como consecuencia de comportamiento válido.

Los Domain Events:

- expresan hechos que ya ocurrieron dentro del dominio;
- son producidos por el Aggregate Proposal;
- utilizan lenguaje ubicuo del Bounded Context;
- no representan comandos;
- no ejecutan casos de uso;
- no contienen lógica de persistencia;
- no conocen mecanismos de transporte;
- no dependen de Infrastructure;
- no son equivalentes a Integration Events;
- no son equivalentes a notificaciones NGSI-LD.

Para VS-001, el flujo normativo contempla:

    CreateProposal
        |
        v
    ProposalCreated

    SubmitProposal
        |
        v
    ProposalSubmitted

La transformación posterior de Domain Events en Integration Events pertenece
a la coordinación correspondiente fuera del dominio y debe preservar la
separación:

    Domain Event != Integration Event != NGSI-LD Notification

Los símbolos públicos se exportarán únicamente cuando sus implementaciones
correspondientes hayan sido creadas y verificadas.
"""