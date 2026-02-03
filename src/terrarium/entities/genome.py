"""Genome data structure.

Genomes encode heritable numeric traits for organisms.

Scope (P2.01)
------------
- Immutable (frozen dataclass)
- Hashable and comparable
- Fixed set of named genes
- Serializable to/from dict

Out of scope: mutation, phenotype mapping, gene interactions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, TypeAlias


Gene: TypeAlias = float


class GeneName(str, Enum):
    SPEED = "speed"
    SENSE_RANGE = "sense_range"
    METABOLISM = "metabolism"
    REPRODUCTION_THRESHOLD = "reproduction_threshold"


@dataclass(frozen=True, slots=True)
class Genome:
    """Immutable container of gene values."""

    speed: Gene
    sense_range: Gene
    metabolism: Gene
    reproduction_threshold: Gene

    def __post_init__(self) -> None:
        # Keep validation minimal and numeric-focused.
        for name in (
            "speed",
            "sense_range",
            "metabolism",
            "reproduction_threshold",
        ):
            value = getattr(self, name)
            if not isinstance(value, (int, float)):
                raise TypeError(f"{name} must be numeric")

    def to_dict(self) -> dict[str, Gene]:
        return {
            GeneName.SPEED.value: float(self.speed),
            GeneName.SENSE_RANGE.value: float(self.sense_range),
            GeneName.METABOLISM.value: float(self.metabolism),
            GeneName.REPRODUCTION_THRESHOLD.value: float(self.reproduction_threshold),
        }

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "Genome":
        return cls(
            speed=float(d[GeneName.SPEED.value]),
            sense_range=float(d[GeneName.SENSE_RANGE.value]),
            metabolism=float(d[GeneName.METABOLISM.value]),
            reproduction_threshold=float(d[GeneName.REPRODUCTION_THRESHOLD.value]),
        )

    def distance(self, other: "Genome") -> float:
        """Simple L1 distance across gene values."""

        return (
            abs(self.speed - other.speed)
            + abs(self.sense_range - other.sense_range)
            + abs(self.metabolism - other.metabolism)
            + abs(self.reproduction_threshold - other.reproduction_threshold)
        )


DEFAULT_GENOME = Genome(
    speed=0.5,
    sense_range=0.5,
    metabolism=0.5,
    reproduction_threshold=10.0,
)
