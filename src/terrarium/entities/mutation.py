from __future__ import annotations

from dataclasses import dataclass

from terrarium.core.protocols import RandomSource
from terrarium.entities.genome import GeneName, Genome


def _clamp_float(x: float, lo: float, hi: float) -> float:
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


def _clamp_gene(name: GeneName, value: float) -> float:
    # Ranges match phenotype normalization assumptions.
    if name in (GeneName.SPEED, GeneName.SENSE_RANGE, GeneName.METABOLISM):
        return _clamp_float(value, 0.0, 1.0)
    if name is GeneName.REPRODUCTION_THRESHOLD:
        return _clamp_float(value, 0.0, 100.0)
    # Fallback (should not happen with fixed GeneName set).
    return value


@dataclass(frozen=True, slots=True)
class MutationConfig:
    """Configuration for mutation behavior.

    - rate: probability per gene to mutate
    - magnitude: stddev used for gaussian mutation delta
    """

    rate: float = 0.1
    magnitude: float = 0.1

    def __post_init__(self) -> None:
        if self.rate < 0.0 or self.rate > 1.0:
            raise ValueError("rate must be in [0.0, 1.0]")
        if self.magnitude < 0.0:
            raise ValueError("magnitude must be >= 0.0")


def mutate_genome(
    genome: Genome,
    rng: RandomSource,
    rate: float = 0.1,
    magnitude: float = 0.1,
) -> Genome:
    """Return a (possibly) mutated copy of genome.

    Determinism
    -----------
    - Uses only the injected RNG.
    - Each gene mutates independently with probability `rate`.

    Mutation
    --------
    new_value = old_value + N(0, magnitude)

    Clamping
    --------
    - speed/sense_range/metabolism clamped to [0.0, 1.0]
    - reproduction_threshold clamped to [0.0, 100.0]

    Notes
    -----
    This function always returns a new Genome instance (even if unchanged).
    """

    cfg = MutationConfig(rate=rate, magnitude=magnitude)

    # Avoid requiring RandomSource.gauss(); Box-Muller from RandomSource.random().
    import math

    def gauss0(stddev: float) -> float:
        if stddev <= 0.0:
            return 0.0
        # Box-Muller transform. Ensure u1 is in (0,1] to avoid log(0).
        u1 = rng.random()
        while u1 <= 0.0:
            u1 = rng.random()
        u2 = rng.random()
        z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        return z0 * stddev

    data = genome.to_dict()
    mutated: dict[str, float] = {}

    for name in GeneName:
        old_v = float(data[name.value])
        if rng.random() < cfg.rate:
            new_v = old_v + gauss0(cfg.magnitude)
        else:
            new_v = old_v
        new_v = _clamp_gene(name, new_v)
        mutated[name.value] = new_v

    # Preserve the original gene types where it matters.
    # reproduction_threshold is used as numeric; keep it as int for compatibility.
    return Genome(
        speed=float(mutated[GeneName.SPEED.value]),
        sense_range=float(mutated[GeneName.SENSE_RANGE.value]),
        metabolism=float(mutated[GeneName.METABOLISM.value]),
        reproduction_threshold=int(round(mutated[GeneName.REPRODUCTION_THRESHOLD.value])),
    )
