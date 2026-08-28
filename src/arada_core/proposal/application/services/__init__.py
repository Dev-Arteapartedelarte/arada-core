"""
Application Services del Bounded Context Proposal.

Este paquete contiene las implementaciones concretas de los casos de uso
expuestos por los Input Ports de Application.

Conforme a CORE-013, CORE-015 y CORE-016, un Application Service:

- implementa un caso de uso concreto;
- coordina dependencias y flujo de ejecución;
- recibe Commands;
- utiliza Repository Contracts;
- utiliza Output Ports;
- coordina autorización;
- coordina validaciones externas;
- invoca comportamiento del Aggregate Proposal;
- persiste la unidad de consistencia completa;
- coordina efectos posteriores al Commit;
- devuelve DTOs o resultados de Application;
- no implementa invariantes de dominio;
- no reproduce la State Machine;
- no modifica ProposalStatus directamente;
- no incrementa ProposalVersion directamente;
- no crea Domain Events en nombre del Aggregate;
- no contiene SQL, ORM ni detalles de Infrastructure;
- no expone directamente el Aggregate Proposal.

Para VS-001 se incorporarán exclusivamente:

    CreateProposalService
    SubmitProposalService

La relación física aprobada es:

    CreateProposalUseCase
        |
        v
    CreateProposalService

    SubmitProposalUseCase
        |
        v
    SubmitProposalService

Cada Service debe mantener la regla de una única frontera de consistencia por
Commit.

Las coordinaciones con Domain Events e Integration Events deberán respetar la
separación:

    Domain Event
        !=
    Integration Event
        !=
    NGSI-LD Notification

Los símbolos públicos se exportarán únicamente cuando sus implementaciones
correspondientes hayan sido creadas y verificadas.
"""