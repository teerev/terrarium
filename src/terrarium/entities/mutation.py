from __future__ import annotations

from dataclasses import dataclass

from terrarium.engine.rng import SeededRNG
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
class MutationConfig:
    """Configuration for genome mutation.

    rate:
        Per-gene mutation probability.
    magnitude:
        Standard deviation for Gaussian noise applied to mutating genes.

    Notes
    -----
    - Deterministic when used with an injected RNG.
    - Magnitude is applied in gene units.
    """

    rate: float = 0.1
    magnitude: float = 0.1


def mutate_genome(
    genome: Genome,
    rng: SeededRNG,
    rate: float = 0.1,
    magnitude: float = 0.1,
) -> Genome:
    """Return a (possibly) mutated copy of *genome*.

    Mutation model
    --------------
    - Each gene mutates independently with probability *rate*.
    - If a gene mutates: new_value = old_value + rng.gauss(0, magnitude)
    - Values are clamped to valid operational gene ranges.

    Gene ranges (aligned with phenotype normalization)
    -------------------------------------------------
    - speed: [0.0, 1.0]
    - sense_range: [0, 10]
    - metabolism: [0.0, 1.0]
    - reproduction_threshold: [0, 50]
    """

    r = float(rate)
    if r < 0.0:
        r = 0.0
    if r > 1.0:
        r = 1.0

    mag = float(magnitude)
    if mag < 0.0:
        mag = 0.0

    speed = float(genome.speed)
    sense_range = int(genome.sense_range)
    metabolism = float(genome.metabolism)
    reproduction_threshold = int(genome.reproduction_threshold)

    if rng.random() < r:
        speed = speed + float(rng.gauss(0.0, mag))
    if rng.random() < r:
        sense_range = int(round(float(sense_range) + float(rng.gauss(0.0, mag))))
    if rng.random() < r:
        metabolism = metabolism + float(rng.gauss(0.0, mag))
    if rng.random() < r:
        reproduction_threshold = int(
            round(float(reproduction_threshold) + float(rng.gauss(0.0, mag)))
        )

    # Clamp to valid gene ranges.
    speed = _clamp_float(speed, 0.0, 1.0)
    sense_range = _clamp_int(sense_range, 0, 10)
    metabolism = _clamp_float(metabolism, 0.0, 1.0)
    reproduction_threshold = _clamp_int(reproduction_threshold, 0, 50)

    return Genome(
        speed=float(speed),
        sense_range=int(sense_range),
        metabolism=float(metabolism),
        reproduction_threshold=int(reproduction_threshold),
    )
