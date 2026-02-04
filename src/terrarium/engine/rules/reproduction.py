from __future__ import annotations

from dataclasses import dataclass

from terrarium.engine.rng import SeededRNG
from terrarium.entities.organism import Organism, create_organism
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class ReproductionRule:
    """Rule implementing asexual reproduction.

    Design constraints:
    - Deterministic: organisms are checked in sorted ID order.
    - Threshold comes from organism.phenotype.reproduction_threshold.
    - Offspring spawned at the parent's position.
    - Offspring inherits parent's genome (no mutation in this work order).
    - Parent energy reduced by offspring starting energy (energy split).

    Public API:
    - ReproductionRule.apply(world, rng) -> list[Organism]
    """

    def apply(self, world: WorldState, rng: SeededRNG) -> list[Organism]:
        # WorldState doesn't expose an organism iterator; access the internal index
        # (consistent with other rules) and keep deterministic order.
        entities = getattr(world, "_entities", {})
        organisms: list[Organism] = [e for e in entities.values() if isinstance(e, Organism)]
        organisms.sort(key=lambda o: str(o.id))

        offspring: list[Organism] = []

        for parent in organisms:
            threshold = int(parent.phenotype.reproduction_threshold)
            if parent.energy <= threshold:
                continue

            # Single-offspring reproduction with an even split of current energy.
            # Parent energy decreases by offspring starting energy.
            child_energy = parent.energy // 2
            if child_energy <= 0:
                continue

            parent.energy -= child_energy

            child = create_organism(
                position=parent.position,
                energy=child_energy,
                rng=rng,
                genome=parent.genome,
                parent_id=parent.id,
                lineage_id=parent.lineage_id,
                generation=parent.generation + 1,
                birth_tick=world.tick,
            )

            world.add_entity(child)
            offspring.append(child)

        return offspring
