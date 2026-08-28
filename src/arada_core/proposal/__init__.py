"""
Bounded Context Proposal Management de AURA Core.

Este paquete constituye el módulo autónomo del Bounded Context Proposal,
conforme al patrón físico aprobado de CORE-015.

Su estructura evoluciona mediante Vertical Slices y mantiene las capas:

    proposal/
    ├── domain/
    ├── application/
    ├── infrastructure/
    └── interfaces/

VS-001 implementará exclusivamente el corte:

    Nonexistent
        |
        | CreateProposal
        v
    Draft
        |
        | SubmitProposal
        v
    Submitted

Las dependencias deben preservar las reglas arquitectónicas de AURA Core:

- Domain no depende de Application;
- Domain no depende de Infrastructure;
- Domain no depende de Interfaces;
- Application puede depender de Domain;
- Infrastructure implementa contratos definidos hacia el interior;
- Interfaces actúa como capa de entrada hacia Application;
- ningún detalle tecnológico debe convertirse en regla de dominio.

Los símbolos públicos se incorporarán progresivamente cuando existan
implementaciones completas y verificadas dentro del Vertical Slice.
"""