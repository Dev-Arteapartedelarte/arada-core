"""
Domain del Bounded Context Proposal.

Este paquete contiene exclusivamente conceptos y contratos pertenecientes
al modelo de dominio de Proposal.

Conforme a las reglas arquitectónicas de AURA Core:

- Domain no depende de Application;
- Domain no depende de Infrastructure;
- Domain no depende de Interfaces;
- Domain conserva autoridad sobre invariantes;
- Domain conserva autoridad sobre Lifecycle;
- Domain conserva autoridad sobre State Machine;
- Domain produce Domain Events como consecuencia de comportamiento válido;
- Repository Contracts pertenecen a Domain;
- detalles de persistencia permanecen fuera de Domain.

VS-001 incorporará progresivamente los elementos necesarios para demostrar:

    Nonexistent
        |
        | CreateProposal
        v
    Draft
        |
        | SubmitProposal
        v
    Submitted

Los símbolos públicos se exportarán únicamente cuando sus implementaciones
correspondientes hayan sido creadas y verificadas.
"""