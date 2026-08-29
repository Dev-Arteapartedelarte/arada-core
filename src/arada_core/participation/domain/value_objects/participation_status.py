from __future__ import annotations

from enum import StrEnum


class ParticipationStatus(StrEnum):
    """Estados oficiales del Aggregate Participation."""

    REGISTERED = "Registered"
    ACTIVE = "Active"
    COMPLETED = "Completed"
    WITHDRAWN = "Withdrawn"
    INVALIDATED = "Invalidated"
    ARCHIVED = "Archived"