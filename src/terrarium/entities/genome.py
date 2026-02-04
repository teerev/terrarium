from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Union


Gene = Union[int, float]


class GeneName(str, Enum):
    """Fixed set of supported gene names."""

    SPEED = "speed"
    SENSE_RANGE = "sense_range"
    METABOLISM = "metabolism"
    REPRODUCTION_THRESHOLD = "reproduction_threshold"


@dataclass(frozen=True, slots=True)
class Genome:
    """Immutable container for heritable numeric traits.

    Notes:
    - This is intentionally minimal: it stores a fixed set of named values.
    - Mutation and phenotype mapping are handled in separate work orders.
    """

    speed: Gene
    sense_range: Gene
    metabolism: Gene
    reproduction_threshold: Gene

    def __post_init__(self) -> None:
        # Ensure values are numeric and finite-ish.
        for name in GeneName:
            value = getattr(self, name.value)
            if not isinstance(value, (int, float)):
                raise TypeError(f"{name.value} must be int or float")

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
        """Construct a Genome from a mapping.

        Unknown keys are ignored. Missing keys fall back to DEFAULT_GENOME.
        """

        defaults = DEFAULT_GENOME.to_dict()
        data: dict[str, Any] = dict(defaults)
        for k, v in d.items():
            if k in defaults:
                data[k] = v

        return cls(
            speed=data[GeneName.SPEED.value],
            sense_range=data[GeneName.SENSE_RANGE.value],
            metabolism=data[GeneName.METABOLISM.value],
            reproduction_threshold=data[GeneName.REPRODUCTION_THRESHOLD.value],
        )


DEFAULT_GENOME = Genome(
    speed=0.5,
    sense_range=3.0,
    metabolism=1.0,
    reproduction_threshold=20,
)
