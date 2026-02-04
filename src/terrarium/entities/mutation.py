from __future__ import annotations

from dataclasses import dataclass

from terrarium.engine.rng import SeededRNG
from terrarium.entities.genome import Genome


@dataclass(frozen=True, slots=True)
class MutationConfig:
    """Configuration for genome mutation.

    Attributes:
        rate: Probability (per gene) that a mutation is applied.
        magnitude: Standard deviation for Gaussian mutation noise.

    Note:
        The default rate is 0.0 to preserve prior behavior (no mutation) unless
        a simulation explicitly enables mutation.
    """

    rate: float = 0.0
    magnitude: float = 0.1


def _clamp(value: float, lo: float, hi: float) -> float:
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value


# Gene-specific valid ranges.
# Keep defaults simple/stable; these are gene (genome) ranges, not phenotype ranges.
_GENE_RANGES: dict[str, tuple[float, float]] = {
    "speed": (0.0, 1.0),
    "sense_range": (0.0, 10.0),
    "metabolism": (0.0, 1.0),
    "reproduction_threshold": (0.0, 20.0),
}


def mutate_genome(
    genome: Genome,
    rng: SeededRNG,
    rate: float = 0.0,
    magnitude: float = 0.1,
) -> Genome:
    """Return a (possibly) mutated copy of *genome*.

    Determinism:
        All randomness comes from the injected *rng*.

    Mutation model:
        Each gene independently mutates with probability *rate* by adding
        rng.gauss(0, magnitude), then clamping to a valid range.
    """

    r = float(rate)
    if r <= 0.0:
        return genome

    m = float(magnitude)

    changed = False

    # Mutate per field; keep Genome immutable by creating a new instance only
    # when at least one gene changes.
    speed = float(genome.speed)
    if rng.random() < r:
        speed = _clamp(speed + float(rng.gauss(0.0, m)), *_GENE_RANGES["speed"])
        changed = True

    sense_range = float(genome.sense_range)
    if rng.random() < r:
        sense_range = _clamp(
            sense_range + float(rng.gauss(0.0, m)), *_GENE_RANGES["sense_range"]
        )
        changed = True

    metabolism = float(genome.metabolism)
    if rng.random() < r:
        metabolism = _clamp(
            metabolism + float(rng.gauss(0.0, m)), *_GENE_RANGES["metabolism"]
        )
        changed = True

    reproduction_threshold = float(genome.reproduction_threshold)
    if rng.random() < r:
        reproduction_threshold = _clamp(
            reproduction_threshold + float(rng.gauss(0.0, m)),
            *_GENE_RANGES["reproduction_threshold"],
        )
        changed = True

    if not changed:
        return genome

    return Genome(
        speed=speed,
        sense_range=sense_range,
        metabolism=metabolism,
        reproduction_threshold=reproduction_threshold,
    )
