from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrganizationId:
    """Referencia inmutable a una Organization dentro de Participation."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("OrganizationId must not be empty.")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value