"""Organism entity.

An Organism represents a living agent in the world.

Scope notes:
- Organisms have mutable state (position, energy, age).
- Movement/reproduction/AI are out of scope for this work order.

Public APIs:
- :class:`Organism`
- :func:`create_organism`
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.engine.rng import SeededRNG
from terrarium.entities.base import EntityId, EntityType, generate_id, generate_id_from_rng
from terrarium.entities.genome import DEFAULT_GENOME, Genome
from terrarium.entities.phenotype import Phenotype
from terrarium.world.grid import Position


@dataclass(slots=True)
class Organism:
    """Living agent entity.

    Attributes:
        position: Current position (mutable).
        energy: Current energy (non-negative integer).
        age: Ticks since creation (starts at 0).
        id: Unique immutable entity id.
    """

    position: Position
    energy: int
    genome: Genome = DEFAULT_GENOME
    age: int = 0
    id: EntityId | None = None

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = generate_id()

        if not isinstance(self.energy, int) or self.energy < 0:
            raise ValueError("energy must be a non-negative integer")

        if not isinstance(self.age, int) or self.age < 0:
            raise ValueError("age must be a non-negative integer")

    @property
    def entity_type(self) -> EntityType:
        return EntityType.ORGANISM

    @property
    def phenotype(self) -> Phenotype:
        """Computed phenotype derived from the organism's genome."""

        return Phenotype.from_genome(self.genome)

    @property
    def is_alive(self) -> bool:
        return self.energy > 0

    def tick(self) -> int:
        """Advance organism internal time by one tick.

        Returns:
            The new age.
        """

        self.age += 1
        return self.age


def create_organism(
    position: Position,
    energy: int,
    *,
    entity_id: EntityId | None = None,
    rng: SeededRNG | None = None,
    genome: Genome | None = None,
) -> Organism:
    """Factory for creating Organism instances with a valid id.

    Determinism:
    - If entity_id is provided, it is used as-is.
    - Else if rng is provided, a deterministic id is generated from it.
    - Else a non-deterministic uuid4 id is generated.
    """

    if entity_id is None and rng is not None:
        entity_id = generate_id_from_rng(rng)

    if genome is None:
        genome = DEFAULT_GENOME

    return Organism(position=position, energy=energy, genome=genome, id=entity_id)
