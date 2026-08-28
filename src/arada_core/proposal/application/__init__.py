"""
Application Layer del Bounded Context Proposal.

Este paquete contiene la coordinación de casos de uso del Bounded Context
Proposal Management.

Conforme a CORE-013, CORE-015 y CORE-016, Application:

- recibe intenciones desde los adapters de entrada;
- coordina autorización mediante Output Ports;
- recupera y persiste Proposal mediante su Repository Contract;
- resuelve validaciones externas antes de invocar comportamiento de dominio;
- entrega al Aggregate la información necesaria para decidir;
- coordina efectos posteriores al Commit;
- puede transformar Domain Events en contratos destinados a integración;
- no implementa invariantes de negocio;
- no reproduce la State Machine;
- no modifica ProposalStatus directamente;
- no incrementa ProposalVersion directamente;
- no produce Domain Events en nombre del Aggregate;
- no depende de Infrastructure;
- no contiene SQL, ORM ni detalles de transporte;
- no utiliza Read Models como Write Model.

Para VS-001, Application coordinará exclusivamente los casos de uso:

    CreateProposalUseCase
        |
        v
    CreateProposalService
        |
        v
    Proposal.create(...)
        |
        v
    Draft

y:

    SubmitProposalUseCase
        |
        v
    SubmitProposalService
        |
        v
    Proposal.submit(...)
        |
        v
    Submitted

Los contratos externos requeridos por estos casos de uso se definirán mediante
Ports explícitos y tecnológicamente neutrales.

Los símbolos públicos se exportarán únicamente cuando sus implementaciones
correspondientes hayan sido creadas y verificadas.
"""