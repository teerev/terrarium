"""Genome data structure.

This module defines an immutable, hashable container for heritable trait values.
Mutation and phenotype mapping are intentionally out of scope.

Public APIs:
- Gene (numeric type alias)
- GeneName (fixed set of gene names)
- Genome (immutable genome container)
- DEFAULT_GENOME (default genome instance)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, TypeAlias, overload


Gene: TypeAlias = float | int


class GeneName(str, Enum):
    """Fixed set of supported genes."""

    SPEED = "speed"
    SENSE_RANGE = "sense_range"
    METABOLISM = "metabolism"
    REPRODUCTION_THRESHOLD = "reproduction_threshold"


@dataclass(frozen=True, slots=True)
class Genome:
    """Immutable genome container.

    Genes are stored as named numeric values.

    Notes
    -----
    - This is a small, fixed-schema container (explicit fields) to keep it
      trivially hashable, fast, and easy to serialize.
    """

    speed: Gene = 0.5
    sense_range: Gene = 3
    metabolism: Gene = 0.5
    reproduction_threshold: Gene = 10

    def __post_init__(self) -> None:
        # Enforce numeric gene values.
        for name in ("speed", "sense_range", "metabolism", "reproduction_threshold"):
            value = getattr(self, name)
            if not isinstance(value, (int, float)):
                raise TypeError(f"{name} must be a numeric gene value (int|float)")

    def to_dict(self) -> dict[str, Gene]:
        """Serialize genome to a plain dict."""

        return {
            GeneName.SPEED.value: self.speed,
            GeneName.SENSE_RANGE.value: self.sense_range,
            GeneName.METABOLISM.value: self.metabolism,
            GeneName.REPRODUCTION_THRESHOLD.value: self.reproduction_threshold,
        }

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "Genome":
        """Reconstruct a Genome from a dict.

        Extra keys are ignored. Missing keys fall back to defaults.
        """

        def _get(key: GeneName, default: Gene) -> Gene:
            if key.value not in d:
                return default
            value = d[key.value]
            if not isinstance(value, (int, float)):
                raise TypeError(f"{key.value} must be a numeric gene value (int|float)")
            return value

        return cls(
            speed=_get(GeneName.SPEED, cls().speed),
            sense_range=_get(GeneName.SENSE_RANGE, cls().sense_range),
            metabolism=_get(GeneName.METABOLISM, cls().metabolism),
            reproduction_threshold=_get(
                GeneName.REPRODUCTION_THRESHOLD, cls().reproduction_threshold
            ),
        )

    def distance(self, other: "Genome") -> float:
        """Simple distance metric between two genomes.

        Uses sum of absolute differences across genes.
        """

        return float(
            abs(float(self.speed) - float(other.speed))
            + abs(float(self.sense_range) - float(other.sense_range))
            + abs(float(self.metabolism) - float(other.metabolism))
            + abs(float(self.reproduction_threshold) - float(other.reproduction_threshold))
        )


DEFAULT_GENOME = Genome()
