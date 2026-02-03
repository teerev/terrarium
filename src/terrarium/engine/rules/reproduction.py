from __future__ import annotations

from dataclasses import dataclass

from terrarium.engine.rng import SeededRNG
from terrarium.entities.mutation import MutationConfig, mutate_genome
from terrarium.entities.organism import Organism
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class ReproductionRule:
    """Asexual reproduction rule.

    Deterministic behavior:
    - Organisms are checked in sorted id order.
    - Backwards compatible default behavior when no explicit reproduction cost is configured:
        - If organism.energy > organism.phenotype.reproduction_threshold, it reproduces.
        - Energy is split evenly between parent and child.
    - Configured cost behavior:
        - Parent must have energy > threshold + cost.
        - Parent pays explicit reproduction cost.
        - Offspring starts with energy derived from that cost.

    Public API
    ----------
    reproduction_cost -> int
    offspring_energy_ratio -> float
    apply(world, rng) -> list[Organism]
        Returns created offspring (also added to world).
    """

    mutation: MutationConfig = MutationConfig(rate=0.0, magnitude=0.1)

    # If provided, forces cost-based reproduction.
    reproduction_cost_override: int | None = None

    # Offspring starting energy formula when using a cost: floor(cost * ratio)
    offspring_energy_ratio: float = 1.0

    # Parent must retain at least this much energy after paying cost.
    min_parent_energy_after: int = 1

    @property
    def reproduction_cost(self) -> int:
        """Configured reproduction cost override (0 when not set)."""

        if self.reproduction_cost_override is None:
            return 0
        return max(0, int(self.reproduction_cost_override))

    def _effective_cost(self, parent: Organism) -> int:
        if self.reproduction_cost_override is not None:
            return max(0, int(self.reproduction_cost_override))
        # Allow phenotype influence when no override is set.
        return max(0, int(getattr(parent.phenotype, "reproduction_cost", 0)))

    def apply(self, world: WorldState, rng: SeededRNG) -> list[Organism]:
        organisms: list[Organism] = []
        for ent in list(world._entities.values()):  # type: ignore[attr-defined]
            if isinstance(ent, Organism):
                organisms.append(ent)

        organisms = sorted(organisms, key=lambda o: str(o.id))

        offspring: list[Organism] = []

        for parent in organisms:
            threshold = int(parent.phenotype.reproduction_threshold)
            current = int(parent.energy)

            # Backwards compatible mode: when no explicit cost override is configured,
            # reproduction gating is based only on threshold and energy is split.
            if self.reproduction_cost_override is None:
                if current <= threshold:
                    continue

                child_energy = current // 2
                parent_final = current - child_energy

                if parent_final < int(self.min_parent_energy_after):
                    continue
                if child_energy <= 0:
                    continue

            else:
                cost = int(self._effective_cost(parent))
                # Parent must have energy > threshold + cost.
                if current <= (threshold + cost):
                    continue

                parent_final = current - cost
                child_energy = int(cost * float(self.offspring_energy_ratio))

                if parent_final < int(self.min_parent_energy_after):
                    continue
                if child_energy <= 0:
                    continue

            parent.energy = parent_final

            if float(self.mutation.rate) > 0.0 and float(self.mutation.magnitude) > 0.0:
                child_genome = mutate_genome(
                    parent.genome,
                    rng,
                    rate=float(self.mutation.rate),
                    magnitude=float(self.mutation.magnitude),
                )
            else:
                child_genome = parent.genome

            child = Organism(
                position=parent.position,
                energy=child_energy,
                rng=rng,
                genome=child_genome,
                parent_id=parent.id,
                lineage_id=parent.lineage_id,
                generation=int(parent.generation) + 1,
                birth_tick=int(world.tick),
            )
            world.add_entity(child)
            offspring.append(child)

        return offspring
