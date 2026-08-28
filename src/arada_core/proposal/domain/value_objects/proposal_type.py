from enum import StrEnum


class ProposalType(StrEnum):
    """
    Clasificación conceptual de una Proposal dentro del dominio AURA.

    ProposalType permite distinguir la naturaleza de la iniciativa sin
    alterar su identidad, autoridad ni Lifecycle.

    Conforme al modelo normativo consolidado:

    - pertenece al estado del Aggregate Proposal;
    - no constituye la identidad del Aggregate;
    - debe representar un valor reconocido por el dominio;
    - puede participar en invariantes específicas;
    - no ejecuta transiciones por sí mismo;
    - no modifica relaciones con otros Aggregates;
    - no depende de Infrastructure;
    - no depende de mecanismos de persistencia.

    La incorporación de nuevos valores requiere una evolución explícita del
    modelo de dominio conforme a los Extension Points de Proposal.
    """

    CITIZEN_INITIATIVE = "CitizenInitiative"
    ORGANIZATIONAL = "Organizational"
    COMMUNITY = "Community"
    TERRITORIAL = "Territorial"
    PROJECT = "Project"
    IMPROVEMENT = "Improvement"
    AGREEMENT = "Agreement"
    REGULATORY = "Regulatory"
    ACTION = "Action"
    SOLUTION = "Solution"
    CONSULTATIVE = "Consultative"