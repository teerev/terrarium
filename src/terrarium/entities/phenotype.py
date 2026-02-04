from __future__ import annotations

"""Genome -> phenotype mapping.

This module defines :class:`Phenotype`, a computed, deterministic view of a
:class:`~terrarium.entities.genome.Genome`.

Design constraints
------------------
- Deterministic: the same genome always yields the same phenotype.
- Usable ranges: traits are normalized/scaled into operational ranges.
- Recomputed: phenotype is derived from a genome, not mutated over time.

Mapping
-------
Gene values are assumed to be numeric. We normalize each gene with a clamp to a
fixed input range, then linearly scale into a trait range.

Let clamp(x, lo, hi) = min(max(x, lo), hi)
Let lerp(a, b, t) = a + (b-a) * t

Normalization:
- speed_gene, sense_gene, metabolism_gene are normalized from [0.0, 1.0]
- reproduction_threshold_gene is normalized from [0, 100]

Trait formulas:
- speed = lerp(0.5, 2.0, norm(speed_gene))
- sense_range = round(lerp(1, 10, norm(sense_gene)))
- metabolism_rate = round(lerp(1, 5, norm(metabolism_gene)))
- reproduction_threshold = round(lerp(10, 50, norm(reproduction_threshold_gene)))

These ranges are intentionally conservative to keep downstream rules stable.
"""

from dataclasses import dataclass

from terrarium.entities.genome import Genome


def _clamp(x: float, lo: float, hi: float) -> float:
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def _norm(x: float, in_min: float, in_max: float) -> float:
    """Normalize x from [in_min, in_max] into [0.0, 1.0], clamped."""

    if in_max <= in_min:
        raise ValueError("invalid normalization range")
    x_c = _clamp(x, in_min, in_max)
    return (x_c - in_min) / (in_max - in_min)


@dataclass(frozen=True, slots=True)
class Phenotype:
    """Computed trait container derived from a Genome."""

    speed: float
    sense_range: int
    metabolism_rate: int
    reproduction_threshold: int

    @classmethod
    def from_genome(cls, genome: Genome) -> "Phenotype":
        """Create a phenotype deterministically from a genome."""

        speed_t = _norm(float(genome.speed), 0.0, 1.0)
        sense_t = _norm(float(genome.sense_range), 0.0, 1.0)
        metab_t = _norm(float(genome.metabolism), 0.0, 1.0)
        repro_t = _norm(float(genome.reproduction_threshold), 0.0, 100.0)

        speed = float(_lerp(0.5, 2.0, speed_t))
        sense_range = int(round(_lerp(1.0, 10.0, sense_t)))
        metabolism_rate = int(round(_lerp(1.0, 5.0, metab_t)))
        reproduction_threshold = int(round(_lerp(10.0, 50.0, repro_t)))

        # Safety clamps after rounding to ensure invariants.
        if sense_range < 1:
            sense_range = 1
        if metabolism_rate < 1:
            metabolism_rate = 1
        if reproduction_threshold < 1:
            reproduction_threshold = 1

        return cls(
            speed=speed,
            sense_range=sense_range,
            metabolism_rate=metabolism_rate,
            reproduction_threshold=reproduction_threshold,
        )
