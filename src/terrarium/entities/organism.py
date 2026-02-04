"""Organism entity.

An Organism represents a living agent in the world.

Scope notes:
- Organisms have mutable state (position, energy, age).
- Movement/reproduction/AI are out of scope for this work order.

Public APIs:
- :class:`Organism`
- :func:`create_organism`

Lineage tracking (P2.03):
- parent_id: immediate parent id (None for initial organisms)
- lineage_id: stable id identifying the original ancestor line
- generation: 0 for initial organisms; parent+1 for offspring
- birth_tick: simulation tick when created

Lineage fields are immutable after creation.
"""

from __future__ import annotations

from dataclasses import dataclass, field

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

        parent_id: Immediate parent id (None for initial organisms).
        lineage_id: Stable id for the lineage (typically original ancestor id).
        generation: Generation number (0 for initial organisms).
        birth_tick: Simulation tick when organism was created.
    """

    position: Position
    energy: int
    genome: Genome = DEFAULT_GENOME
    age: int = 0
    id: EntityId | None = None

    # Lineage tracking
    parent_id: EntityId | None = None
    lineage_id: EntityId | None = None
    generation: int = 0
    birth_tick: int = 0

    # Internal flag used to enforce immutability only after initialization.
    _lineage_frozen: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = generate_id()

        if not isinstance(self.energy, int) or self.energy < 0:
            raise ValueError("energy must be a non-negative integer")

        if not isinstance(self.age, int) or self.age < 0:
            raise ValueError("age must be a non-negative integer")

        if not isinstance(self.generation, int) or self.generation < 0:
            raise ValueError("generation must be a non-negative integer")

        if not isinstance(self.birth_tick, int) or self.birth_tick < 0:
            raise ValueError("birth_tick must be a non-negative integer")

        # Default lineage behavior:
        # - Initial organisms: parent_id=None, generation=0, lineage_id defaults to self.id
        # - Offspring: lineage_id must be provided (typically parent's lineage_id)
        if self.lineage_id is None:
            self.lineage_id = self.id

        # Freeze lineage fields after initialization completes.
        object.__setattr__(self, "_lineage_frozen", True)

    def __setattr__(self, name: str, value: object) -> None:
        # Enforce immutability for lineage fields after creation.
        if (
            name in {"parent_id", "lineage_id", "generation", "birth_tick"}
            and getattr(self, "_lineage_frozen", False)
        ):
            raise AttributeError(f"'{name}' is immutable after creation")
        object.__setattr__(self, name, value)

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
    # Lineage tracking inputs
    parent_id: EntityId | None = None,
    lineage_id: EntityId | None = None,
    generation: int | None = None,
    birth_tick: int = 0,
) -> Organism:
    """Factory for creating Organism instances with a valid id.

    Determinism:
    - If entity_id is provided, it is used as-is.
    - Else if rng is provided, a deterministic id is generated from it.
    - Else a non-deterministic uuid4 id is generated.

    Lineage:
    - If parent_id is None, defaults are parent_id=None, generation=0.
      lineage_id defaults to the organism's own id.
    - If parent_id is provided, generation defaults to 1 and lineage_id must be
      provided by the caller (typically parent's lineage_id).
    """

    if entity_id is None and rng is not None:
        entity_id = generate_id_from_rng(rng)

    if genome is None:
        genome = DEFAULT_GENOME

    if generation is None:
        generation = 0 if parent_id is None else 1

    return Organism(
        position=position,
        energy=energy,
        genome=genome,
        id=entity_id,
        parent_id=parent_id,
        lineage_id=lineage_id,
        generation=generation,
        birth_tick=birth_tick,
    )
