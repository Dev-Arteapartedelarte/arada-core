from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ParticipationVersion:
    """Versión lógica e inmutable del Aggregate Participation."""

    value: int

    def __post_init__(self) -> None:
        if self.value < 1:
            raise ValueError("ParticipationVersion must be greater than or equal to 1.")

    @classmethod
    def initial(cls) -> ParticipationVersion:
        return cls(1)

    def next(self) -> ParticipationVersion:
        return ParticipationVersion(self.value + 1)

    def __int__(self) -> int:
        return self.value