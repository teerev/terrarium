from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from terrarium.core.protocols import RandomSource
from terrarium.entities.base import EntityId, EntityType, generate_id
from terrarium.entities.genome import DEFAULT_GENOME, Genome
from terrarium.entities.phenotype import Phenotype
from terrarium.world.grid import Position


@dataclass(slots=True)
class Organism:
    """Living entity with mutable state.

    Notes:
    - position is mutable so the engine/world can move organisms.
    - energy is mutable and must be non-negative.
    - age starts at 0 and can be incremented externally each tick.

    Lineage
    -------
    - parent_id: immediate parent only (None for initial organisms)
    - lineage_id: ID of the original ancestor for this lineage
    - generation: 0 for initial organisms, parent.generation + 1 for offspring
    - birth_tick: simulation tick when created

    Lineage fields are intended to be immutable after creation.
    """

    position: Position
    energy: int
    id: EntityId

    # Mutable simulation state
    age: int = 0

    # Immutable-ish configuration/state
    genome: Genome = DEFAULT_GENOME

    # Lineage tracking (immutable after creation by convention)
    parent_id: Optional[EntityId] = None
    lineage_id: Optional[EntityId] = None
    generation: int = 0
    birth_tick: int = 0

    def __post_init__(self) -> None:
        if self.energy < 0:
            raise ValueError("energy must be non-negative")
        if self.age < 0:
            raise ValueError("age must be non-negative")
        if self.generation < 0:
            raise ValueError("generation must be non-negative")
        if self.birth_tick < 0:
            raise ValueError("birth_tick must be non-negative")

        # Default lineage_id to self.id when not provided (initial organisms).
        if self.lineage_id is None:
            self.lineage_id = self.id

    @property
    def entity_type(self) -> EntityType:
        return EntityType.ORGANISM

    @property
    def is_alive(self) -> bool:
        return self.energy > 0

    @property
    def phenotype(self) -> Phenotype:
        """Computed phenotype derived from the current genome."""

        return Phenotype.from_genome(self.genome)


def create_organism(
    position: Position,
    energy: int,
    *,
    id: Optional[EntityId] = None,
    rng: Optional[RandomSource] = None,
    genome: Genome = DEFAULT_GENOME,
    parent_id: Optional[EntityId] = None,
    lineage_id: Optional[EntityId] = None,
    generation: int = 0,
    birth_tick: int = 0,
) -> Organism:
    """Factory for Organism with a valid ID.

    If `rng` is provided and `id` is not, the id will be derived from the RNG for
    deterministic replay.

    Lineage behavior
    ----------------
    - If lineage_id is not provided, it defaults to the organism's own id.
    - Offspring should pass parent_id, lineage_id=parent.lineage_id, and
      generation=parent.generation+1.
    """

    oid = id or generate_id(rng)
    return Organism(
        position=position,
        energy=energy,
        id=oid,
        genome=genome,
        parent_id=parent_id,
        lineage_id=lineage_id,
        generation=generation,
        birth_tick=birth_tick,
    )
