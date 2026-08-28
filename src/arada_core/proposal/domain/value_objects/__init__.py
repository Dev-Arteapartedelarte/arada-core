"""
Value Objects del Bounded Context Proposal.

Este paquete contiene conceptos inmutables del lenguaje ubicuo utilizados
por el Aggregate Proposal.

Los Value Objects:

- representan conceptos explícitos del dominio;
- encapsulan reglas propias de validez;
- no poseen identidad independiente;
- no ejecutan casos de uso;
- no coordinan autorización;
- no acceden a Infrastructure;
- no conocen mecanismos de persistencia;
- no modifican otros Aggregates;
- permanecen independientes de frameworks.

Las reglas que involucren Lifecycle, State Machine, consistencia entre varios
valores o transiciones de Proposal permanecen bajo la autoridad del
Aggregate Root.

VS-001 incorporará únicamente los Value Objects necesarios para implementar
y verificar el flujo:

    Nonexistent
        |
        | CreateProposal
        v
    Draft
        |
        | SubmitProposal
        v
    Submitted

Los símbolos públicos se exportarán progresivamente cuando sus
implementaciones correspondientes hayan sido creadas y verificadas.
"""