from __future__ import annotations

from enum import StrEnum


class ParticipationType(StrEnum):
    """Tipos oficiales reconocidos por el Aggregate Participation."""

    ATTENDANCE = "Attendance"
    INTERVENTION = "Intervention"
    DELIBERATION = "Deliberation"
    CONTRIBUTION = "Contribution"
    CONSULTATION = "Consultation"
    PROPOSAL_PARTICIPATION = "ProposalParticipation"
    ASSEMBLY_PARTICIPATION = "AssemblyParticipation"
    TERRITORIAL_PARTICIPATION = "TerritorialParticipation"