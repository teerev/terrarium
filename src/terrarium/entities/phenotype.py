"""Phenotype (genome -> traits) mapping.

A Phenotype is a deterministic, computed view of an organism's Genome.

Design constraints:
- Derived deterministically from the Genome.
- Values are scaled/normalized into operational ranges.
- Recomputed on demand (callers may cache externally if desired).

Gene-to-trait mapping
---------------------
The Genome stores numeric genes which may be any reasonable int/float.
Phenotype scales these genes into stable ranges used by simulation rules.

Mapping formulas (linear scaling with clamping):

- speed:
    speed_gene = genome.speed
    speed = clamp(0.1, 3.0, base=0.5 + speed_gene * 1.0)

- sense_range:
    sense_gene = genome.sense_range
    sense_range = int(round(clamp(1.0, 10.0, base=2.0 + sense_gene * 1.0)))

- metabolism_rate:
    metab_gene = genome.metabolism
    metabolism_rate = int(round(clamp(1.0, 10.0, base=1.0 + metab_gene * 20.0)))

- reproduction_threshold:
    repro_gene = genome.reproduction_threshold
    reproduction_threshold = int(round(clamp(5.0, 200.0, base=10.0 + repro_gene * 10.0)))

Notes:
- The clamping ranges are chosen to keep values usable for simple rules.
- The default Genome values produce reasonable defaults.
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.entities.genome import Genome


def _clamp(x: float, lo: float, hi: float) -> float:
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


@dataclass(frozen=True, slots=True)
class Phenotype:
    """Computed traits derived from a :class:`~terrarium.entities.genome.Genome`."""

    speed: float
    sense_range: int
    metabolism_rate: int
    reproduction_threshold: int

    @classmethod
    def from_genome(cls, genome: Genome) -> "Phenotype":
        """Compute a phenotype deterministically from *genome*."""

        # speed: continuous float used for movement decisions
        speed = _clamp(0.5 + float(genome.speed) * 1.0, 0.1, 3.0)

        # sense_range: grid radius in tiles
        sense_range = int(round(_clamp(2.0 + float(genome.sense_range) * 1.0, 1.0, 10.0)))

        # metabolism_rate: energy cost per tick (integer)
        metabolism_rate = int(round(_clamp(1.0 + float(genome.metabolism) * 20.0, 1.0, 10.0)))

        # reproduction_threshold: energy required to reproduce (integer)
        reproduction_threshold = int(
            round(_clamp(10.0 + float(genome.reproduction_threshold) * 10.0, 5.0, 200.0))
        )

        return cls(
            speed=float(speed),
            sense_range=int(sense_range),
            metabolism_rate=int(metabolism_rate),
            reproduction_threshold=int(reproduction_threshold),
        )
