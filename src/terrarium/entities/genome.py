from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, TypeAlias


Gene: TypeAlias = float | int


class GeneName(str, Enum):
    """Fixed set of gene names.

    Using an Enum prevents typos and provides a stable, enumerable gene set.
    """

    SPEED = "speed"
    SENSE_RANGE = "sense_range"
    METABOLISM = "metabolism"
    REPRODUCTION_THRESHOLD = "reproduction_threshold"


@dataclass(frozen=True, slots=True)
class Genome:
    """Immutable container of heritable trait values."""

    speed: float = 0.5
    sense_range: int = 3
    metabolism: float = 0.1
    reproduction_threshold: int = 10

    def to_dict(self) -> dict[str, Gene]:
        """Return a JSON-serializable dict representation."""

        return {
            GeneName.SPEED.value: float(self.speed),
            GeneName.SENSE_RANGE.value: int(self.sense_range),
            GeneName.METABOLISM.value: float(self.metabolism),
            GeneName.REPRODUCTION_THRESHOLD.value: int(self.reproduction_threshold),
        }

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "Genome":
        """Construct a genome from a dict.

        Missing keys fall back to defaults.
        Extra keys are ignored.
        """

        return cls(
            speed=float(d.get(GeneName.SPEED.value, cls().speed)),
            sense_range=int(d.get(GeneName.SENSE_RANGE.value, cls().sense_range)),
            metabolism=float(d.get(GeneName.METABOLISM.value, cls().metabolism)),
            reproduction_threshold=int(
                d.get(GeneName.REPRODUCTION_THRESHOLD.value, cls().reproduction_threshold)
            ),
        )

    def distance(self, other: "Genome") -> float:
        """Simple normalized distance between two genomes.

        Intended as a lightweight similarity metric; not used for mutation.
        """

        # Keep this intentionally simple and deterministic.
        return (
            abs(float(self.speed) - float(other.speed))
            + abs(float(self.sense_range) - float(other.sense_range))
            + abs(float(self.metabolism) - float(other.metabolism))
            + abs(float(self.reproduction_threshold) - float(other.reproduction_threshold))
        )


DEFAULT_GENOME = Genome()
