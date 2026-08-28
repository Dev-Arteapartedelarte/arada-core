"""
Test suite del Bounded Context Proposal.

Este paquete contiene las pruebas automatizadas correspondientes al Vertical
Slice VS-001 y a las reglas de dominio y aplicación del Bounded Context
Proposal Management.

La estructura de tests refleja la arquitectura física aprobada:

    tests/proposal/
    ├── domain/
    └── application/

Las pruebas deben preservar las mismas fronteras arquitectónicas del código
productivo:

- Domain se prueba sin Infrastructure;
- Application se prueba mediante doubles de sus Ports y Repository Contracts;
- las pruebas no introducen reglas de negocio nuevas;
- las expectativas derivan de los artefactos normativos de DOMAIN-007;
- las operaciones inválidas no deben modificar estado, Version ni producir
  Domain Events;
- las operaciones válidas deben respetar Lifecycle, State Machine,
  invariantes y concurrencia optimista.

Para VS-001 se verificará principalmente:

    Nonexistent
        |
        | CreateProposal
        v
    Draft
        |
        | SubmitProposal
        v
    Submitted

Los símbolos de test permanecen organizados en sus respectivos paquetes y no
se exportan desde este inicializador.
"""