from __future__ import annotations

from dataclasses import dataclass

from terrarium.engine.rng import SeededRNG
from terrarium.entities.mutation import MutationConfig, mutate_genome
from terrarium.entities.organism import Organism, create_organism
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class ReproductionRule:
    """Rule implementing asexual reproduction.

    Design constraints:
    - Deterministic: organisms are checked in sorted ID order.
    - Threshold comes from organism.phenotype.reproduction_threshold.
    - Cost comes from organism.phenotype.reproduction_cost (or rule default).
    - Parent must have energy > threshold + cost to reproduce.
    - Offspring spawned at the parent's position.
    - Offspring inherits parent's genome (with mutation).
    - Parent energy reduced by reproduction cost.
    - Offspring starts with energy derived from cost (ratio).
    - Parent retains a minimum viable energy after reproduction.

    Public API:
    - ReproductionRule.apply(world, rng) -> list[Organism]
    - ReproductionRule.reproduction_cost -> int
    - ReproductionRule.offspring_energy_ratio -> float
    """

    mutation: MutationConfig = MutationConfig()
    reproduction_cost: int = 4
    offspring_energy_ratio: float = 1.0
    min_parent_energy_after: int = 1

    def apply(self, world: WorldState, rng: SeededRNG) -> list[Organism]:
        # WorldState doesn't expose an organism iterator; access the internal index
        # (consistent with other rules) and keep deterministic order.
        entities = getattr(world, "_entities", {})
        organisms: list[Organism] = [e for e in entities.values() if isinstance(e, Organism)]
        organisms.sort(key=lambda o: str(o.id))

        offspring: list[Organism] = []

        for parent in organisms:
            threshold = int(parent.phenotype.reproduction_threshold)
            cost = int(getattr(parent.phenotype, "reproduction_cost", self.reproduction_cost))
            if cost <= 0:
                continue

            # Must have energy strictly greater than threshold + cost.
            if parent.energy <= threshold + cost:
                continue

            # Ensure parent retains minimum viable energy after paying the cost.
            if parent.energy - cost < int(self.min_parent_energy_after):
                continue

            child_energy = int(cost * float(self.offspring_energy_ratio))
            if child_energy <= 0:
                continue

            # Pay reproduction cost.
            parent.energy -= cost

            # Energy conservation (approx): parent_loss == offspring_gain.
            # If ratio != 1.0, bring offspring energy back to at most the cost.
            if child_energy > cost:
                child_energy = cost

            if parent.energy < int(self.min_parent_energy_after):
                # Safety net; should be unreachable due to checks.
                parent.energy += cost
                continue

            child_genome = mutate_genome(
                parent.genome,
                rng,
                rate=self.mutation.rate,
                magnitude=self.mutation.magnitude,
            )

            child = create_organism(
                position=parent.position,
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
