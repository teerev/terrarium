from __future__ import annotations

"""terrarium.entities.phenotype

Genome (genotype) -> Phenotype mapping.

Design
------
- Deterministic: the same Genome always produces the same Phenotype.
- Operational ranges: raw gene values are normalized/scaled into simulation-
  friendly ranges.
- Derived (not stored): Phenotype is computed from a Genome; organisms may
  cache it immutably.

Mapping formulas (simple linear scaling)
--------------------------------------
Let clamp(x, lo, hi) bound values.

Speed (float)
  gene: genome.speed (float)
  normalized: g = clamp(speed, 0.0, 1.0)
  trait: speed = 0.5 + g * 2.0
  range: [0.5, 2.5]

Sense range (int)
  gene: genome.sense_range (int)
  normalized: g = clamp(sense_range, 0, 10)
  trait: sense_range = 1 + g * 2
  range: [1, 21]

Metabolism rate (int)
  gene: genome.metabolism (float)
  normalized: g = clamp(metabolism, 0.0, 1.0)
  trait: metabolism_rate = 1 + round(g * 4)
  range: [1, 5]

Reproduction threshold (int)
  gene: genome.reproduction_threshold (int)
  normalized: g = clamp(reproduction_threshold, 0, 50)
  trait: reproduction_threshold = 10 + g * 2
  range: [10, 110]

Notes
-----
These are intentionally conservative defaults to keep behavior stable while
providing distinct phenotypic variation.
"""

from dataclasses import dataclass

from terrarium.entities.genome import Genome


def _clamp_float(value: float, lo: float, hi: float) -> float:
    v = float(value)
    if v < lo:
        return float(lo)
    if v > hi:
        return float(hi)
    return v


def _clamp_int(value: int, lo: int, hi: int) -> int:
    v = int(value)
    if v < lo:
        return int(lo)
    if v > hi:
        return int(hi)
    return v


@dataclass(frozen=True, slots=True)
class Phenotype:
    """Computed traits that affect organism behavior."""

    speed: float
    sense_range: int
    metabolism_rate: int
    reproduction_threshold: int

    @classmethod
    def from_genome(cls, genome: Genome) -> "Phenotype":
        """Create a phenotype deterministically from a genome."""

        g_speed = _clamp_float(genome.speed, 0.0, 1.0)
        speed = 0.5 + g_speed * 2.0

        g_sense = _clamp_int(genome.sense_range, 0, 10)
        sense_range = 1 + g_sense * 2

        g_met = _clamp_float(genome.metabolism, 0.0, 1.0)
        metabolism_rate = 1 + int(round(g_met * 4.0))

        g_rep = _clamp_int(genome.reproduction_threshold, 0, 50)
        reproduction_threshold = 10 + g_rep * 2

        return cls(
            speed=float(speed),
            sense_range=int(sense_range),
            metabolism_rate=int(metabolism_rate),
            reproduction_threshold=int(reproduction_threshold),
        )
