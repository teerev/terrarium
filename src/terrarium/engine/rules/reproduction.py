from __future__ import annotations

from dataclasses import dataclass

from terrarium.engine.rng import SeededRNG
from terrarium.entities.organism import Organism
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class ReproductionRule:
    """Asexual reproduction rule.

    Deterministic behavior:
    - Organisms are checked in sorted id order.
    - If organism.energy > organism.phenotype.reproduction_threshold, it reproduces.
    - Offspring spawns at the parent's current position.
    - Offspring inherits the parent's genome (no mutation in this work order).
    - Energy is split: offspring gets half of parent's current energy (floor);
      parent keeps the remainder.
    - Offspring lineage is set from parent:
        parent_id = parent.id
        lineage_id = parent.lineage_id
        generation = parent.generation + 1
        birth_tick = world.tick

    Public API
    ----------
    apply(world, rng) -> list[Organism]
        Returns created offspring (also added to world).
    """

    def apply(self, world: WorldState, rng: SeededRNG) -> list[Organism]:
        # Snapshot organisms first to avoid iterating a dict while mutating.
        organisms: list[Organism] = []
        for ent in list(world._entities.values()):  # type: ignore[attr-defined]
            if isinstance(ent, Organism):
                organisms.append(ent)

        # Deterministic processing order: stable sort by id.
        organisms = sorted(organisms, key=lambda o: str(o.id))

        offspring: list[Organism] = []

        for parent in organisms:
            threshold = int(parent.phenotype.reproduction_threshold)
            if int(parent.energy) <= threshold:
                continue

            # Energy split. Offspring gets half (floor), parent keeps remainder.
            current = int(parent.energy)
            child_energy = current // 2
            if child_energy <= 0:
                continue

            parent.energy = current - child_energy

            child = Organism(
                position=parent.position,
                energy=child_energy,
                rng=rng,
                genome=parent.genome,
                parent_id=parent.id,
                lineage_id=parent.lineage_id,
                generation=int(parent.generation) + 1,
                birth_tick=int(world.tick),
            )
            world.add_entity(child)
            offspring.append(child)

        return offspring
