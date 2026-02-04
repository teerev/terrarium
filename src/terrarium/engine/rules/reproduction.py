from __future__ import annotations

from dataclasses import dataclass

from terrarium.core.protocols import RandomSource
from terrarium.entities.mutation import mutate_genome
from terrarium.entities.organism import Organism, create_organism
from terrarium.world.state import WorldState


@dataclass(slots=True)
class ReproductionRule:
    """Asexual reproduction rule.

    Design constraints
    ------------------
    - Deterministic: organisms are checked in sorted ID order.
    - Reproduction threshold comes from organism.phenotype.reproduction_threshold.
    - Single offspring per organism per tick.
    - Offspring spawns at parent's (wrapped) position.
    - Offspring inherits parent's genome, with optional mutation.
    - Parent energy is reduced by offspring starting energy.
    """

    # Fraction of parent's current energy given to the offspring.
    offspring_energy_fraction: float = 0.5

    # Mutation parameters (per-simulation configurable via rule configuration).
    mutation_rate: float = 0.1
    mutation_magnitude: float = 0.1

    def __post_init__(self) -> None:
        if self.offspring_energy_fraction <= 0.0 or self.offspring_energy_fraction >= 1.0:
            raise ValueError("offspring_energy_fraction must be in (0.0, 1.0)")
        if self.mutation_rate < 0.0 or self.mutation_rate > 1.0:
            raise ValueError("mutation_rate must be in [0.0, 1.0]")
        if self.mutation_magnitude < 0.0:
            raise ValueError("mutation_magnitude must be >= 0.0")

    def apply(self, world: WorldState, rng: RandomSource) -> list[Organism]:
        offspring: list[Organism] = []

        # Snapshot organisms first to avoid iterating a mutating collection.
        organisms = [e for e in world.iter_entities() if isinstance(e, Organism)]
        organisms_sorted = sorted(organisms, key=lambda o: str(o.id))

        for parent in organisms_sorted:
            threshold = parent.phenotype.reproduction_threshold
            if parent.energy <= threshold:
                continue

            # Give the offspring a portion of the parent's current energy.
            child_energy = int(parent.energy * self.offspring_energy_fraction)

            # Ensure reproduction has an actual cost and produces a viable offspring.
            if child_energy <= 0:
                continue
            if parent.energy - child_energy < 0:
                continue

            parent.energy -= child_energy

            child_genome = mutate_genome(
                parent.genome,
                rng,
                rate=self.mutation_rate,
                magnitude=self.mutation_magnitude,
            )

            child = create_organism(
                position=world.grid.wrap(parent.position),
                energy=child_energy,
                rng=rng,
                genome=child_genome,
                parent_id=parent.id,
                lineage_id=parent.lineage_id,
                generation=parent.generation + 1,
                birth_tick=world.tick,
            )

            world.add_entity(child)
            offspring.append(child)

        return offspring
