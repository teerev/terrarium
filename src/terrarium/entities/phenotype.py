"""Phenotype mapping.

Phenotype is the observable set of operational traits derived deterministically
from an organism's genome (genotype).

Design goals
------------
- Deterministic: same genome -> same phenotype
- Usable ranges: raw gene values are scaled into simulation-friendly values
- Recalculated on demand: phenotype is computed, not evolved over lifetime

Gene-to-trait mapping (simple linear scaling)
--------------------------------------------
All mappings are:
    trait = base + gene_value * scale

The genome currently stores numeric genes without strict bounds. To keep
phenotype values operational and avoid negative traits, genes are clamped to
>= 0.0 before scaling.

Traits
------
- speed (float): movement capability per tick-ish unit
- sense_range (int): how far the organism can sense
- metabolism_rate (int): energy consumed per tick / baseline cost factor
- reproduction_threshold (int): energy required to reproduce

These mappings are intentionally simple (P2.02 scope) and can be adjusted later
as the engine rules become more concrete.
"""

from __future__ import annotations

from dataclasses import dataclass

from .genome import Genome


def _clamp_non_negative(x: float) -> float:
    return x if x >= 0.0 else 0.0


def _scale_float(*, base: float, scale: float, gene: float) -> float:
    return base + _clamp_non_negative(float(gene)) * scale


def _scale_int(*, base: int, scale: float, gene: float) -> int:
    # Round to nearest int to avoid systematic downward bias from truncation.
    return int(round(base + _clamp_non_negative(float(gene)) * scale))


@dataclass(frozen=True, slots=True)
class Phenotype:
    """Computed traits derived from a Genome."""

    speed: float
    sense_range: int
    metabolism_rate: int
    reproduction_threshold: int

    @classmethod
    def from_genome(cls, genome: Genome) -> "Phenotype":
        """Create a phenotype deterministically derived from *genome*."""

        # Operational ranges (with default genome of 0.5 values):
        # - speed: base 0.5 + gene*1.5 => default 1.25
        # - sense_range: base 1 + gene*10 => default 6
        # - metabolism_rate: base 1 + gene*4 => default 3
        # - reproduction_threshold: base 5 + gene*5 => default 55 (since default gene is 10.0)
        speed = _scale_float(base=0.5, scale=1.5, gene=genome.speed)
        sense_range = _scale_int(base=1, scale=10.0, gene=genome.sense_range)
        metabolism_rate = _scale_int(base=1, scale=4.0, gene=genome.metabolism)
        reproduction_threshold = _scale_int(
            base=5, scale=5.0, gene=genome.reproduction_threshold
        )

        # Hard floors to ensure always-usable values.
        if sense_range < 1:
            sense_range = 1
        if metabolism_rate < 1:
            metabolism_rate = 1
        if reproduction_threshold < 1:
            reproduction_threshold = 1

        return cls(
            speed=float(speed),
            sense_range=int(sense_range),
            metabolism_rate=int(metabolism_rate),
            reproduction_threshold=int(reproduction_threshold),
        )
