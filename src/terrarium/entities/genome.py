"""Genome data structure.

A Genome is an immutable, hashable container of named genes.

Public API:
- Gene: numeric alias for gene values
- GeneName: fixed set of supported gene identifiers
- Genome: immutable genome container
- DEFAULT_GENOME: default genome instance
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, TypeAlias


Gene: TypeAlias = int | float


class GeneName(str, Enum):
    """Fixed set of genes supported by the simulation."""

    SPEED = "speed"
    SENSE_RANGE = "sense_range"
    METABOLISM = "metabolism"
    REPRODUCTION_THRESHOLD = "reproduction_threshold"


_DEFAULT_VALUES: dict[GeneName, Gene] = {
    GeneName.SPEED: 0.5,
    GeneName.SENSE_RANGE: 2.0,
    GeneName.METABOLISM: 0.1,
    GeneName.REPRODUCTION_THRESHOLD: 10,
}


@dataclass(frozen=True, slots=True)
class Genome:
    """Immutable genome.

    The genes are stored as individual fields to keep the structure fixed and
    hashable by default.
    """

    speed: Gene = _DEFAULT_VALUES[GeneName.SPEED]
    sense_range: Gene = _DEFAULT_VALUES[GeneName.SENSE_RANGE]
    metabolism: Gene = _DEFAULT_VALUES[GeneName.METABOLISM]
    reproduction_threshold: Gene = _DEFAULT_VALUES[GeneName.REPRODUCTION_THRESHOLD]

    def __post_init__(self) -> None:
        for name in ("speed", "sense_range", "metabolism", "reproduction_threshold"):
            value = getattr(self, name)
            if not isinstance(value, (int, float)):
                raise TypeError(f"Gene '{name}' must be numeric (int|float)")

    def to_dict(self) -> dict[str, Gene]:
        """Return a JSON-serializable dict representation."""

        return {
            GeneName.SPEED.value: self.speed,
            GeneName.SENSE_RANGE.value: self.sense_range,
            GeneName.METABOLISM.value: self.metabolism,
            GeneName.REPRODUCTION_THRESHOLD.value: self.reproduction_threshold,
        }

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "Genome":
        """Construct a Genome from a dict.

        Unknown keys are ignored to allow forward compatibility.
        Missing keys fall back to defaults.
        """

        def _get(name: GeneName) -> Gene:
            if name.value not in d:
                return _DEFAULT_VALUES[name]
            v = d[name.value]
            if not isinstance(v, (int, float)):
                raise TypeError(f"Gene '{name.value}' must be numeric (int|float)")
            return v

        return cls(
            speed=_get(GeneName.SPEED),
            sense_range=_get(GeneName.SENSE_RANGE),
            metabolism=_get(GeneName.METABOLISM),
            reproduction_threshold=_get(GeneName.REPRODUCTION_THRESHOLD),
        )

    def distance(self, other: "Genome") -> float:
        """Simple similarity metric: L1 distance over the known genes."""

        return float(
            abs(float(self.speed) - float(other.speed))
            + abs(float(self.sense_range) - float(other.sense_range))
            + abs(float(self.metabolism) - float(other.metabolism))
            + abs(float(self.reproduction_threshold) - float(other.reproduction_threshold))
        )


DEFAULT_GENOME = Genome()
