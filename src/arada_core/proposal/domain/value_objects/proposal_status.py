from enum import StrEnum


class ProposalStatus(StrEnum):
    """
    Estado conceptual del Aggregate Proposal.

    Los valores definidos corresponden exclusivamente a los estados
    oficiales establecidos por el modelo de dominio de AURA Core.

    ProposalStatus:

    - pertenece al estado del Aggregate Proposal;
    - no ejecuta transiciones por sí mismo;
    - no contiene reglas de Lifecycle;
    - no contiene reglas de autorización;
    - no depende de Infrastructure;
    - no depende de mecanismos de persistencia.

    Las transiciones válidas pertenecen al Aggregate Proposal y deben
    respetar DOMAIN-007A-Lifecycle.md, DOMAIN-007B-State-Machine.md y
    DOMAIN-007E-Invariants.md.

    VS-001 utiliza exclusivamente:

        Draft
        Submitted

    Los restantes estados se mantienen porque pertenecen al modelo oficial
    consolidado de Proposal y permiten preservar la semántica completa del
    Value Object.
    """

    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "UnderReview"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"
    ARCHIVED = "Archived"