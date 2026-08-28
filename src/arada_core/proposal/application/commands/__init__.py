"""
Commands de la Application Layer del Bounded Context Proposal.

Este paquete contiene estructuras de intención utilizadas por los casos de uso
de Proposal.

Conforme a la arquitectura aprobada para AURA Core:

- un Command expresa intención;
- no representa un hecho consumado;
- no sustituye un Domain Event;
- no contiene lógica de persistencia;
- no contiene lógica de autorización;
- no implementa invariantes;
- no ejecuta directamente transiciones de estado;
- no conoce Infrastructure;
- no conoce mecanismos de transporte;
- no contiene ORM, SQL ni detalles de framework.

Para VS-001 se incorporarán exclusivamente:

    CreateProposal
    SubmitProposal

Los Commands serán entregados a los Application Services, que coordinarán las
dependencias necesarias y delegarán las decisiones de dominio al Aggregate
Proposal.

Los símbolos públicos se exportarán únicamente cuando sus implementaciones
correspondientes hayan sido creadas y verificadas.
"""