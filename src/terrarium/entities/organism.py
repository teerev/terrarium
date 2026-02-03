"""Organism entity.

Organisms represent living agents in the simulation.

Scope (P1.08)
------------
- Mutable state: position, energy, age
- Energy is non-negative
- Age increments each tick (via `tick()`)
- Satisfies the `Entity` protocol

Out of scope: movement logic, reproduction, genetics, behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from terrarium.core.protocols import RandomSource
from terrarium.world.grid import Position

from .base import Entity, EntityId, EntityType, generate_id
from .genome import DEFAULT_GENOME, Genome
from .phenotype import Phenotype


@dataclass(slots=True)
class Organism(Entity):
    """A living entity with mutable state."""

    # Keep `id` first and make other required fields keyword-only to avoid
    # dataclass ordering issues across Python versions.
    id: EntityId = field(default_factory=generate_id, kw_only=True)

    # Lineage tracking (P2.03)
    # These fields are intended to be immutable after creation.
    parent_id: EntityId | None = field(default=None, kw_only=True)
    # Default to own id when not provided (computed in __post_init__).
    lineage_id: EntityId | None = field(default=None, kw_only=True)
    generation: int = field(default=0, kw_only=True)
    birth_tick: int = field(default=0, kw_only=True)

    position: Position = field(kw_only=True)
    genome: Genome = field(default=DEFAULT_GENOME)
    energy: int = 0
    age: int = 0

    def __post_init__(self) -> None:
        # Ensure lineage_id is always set; for initial organisms it typically
        # equals the organism's own id.
        if self.lineage_id is None:
            self.lineage_id = self.id

        if self.energy < 0:
            raise ValueError("energy must be >= 0")
        if self.age < 0:
            raise ValueError("age must be >= 0")
        if self.generation < 0:
            raise ValueError("generation must be >= 0")
        if self.birth_tick < 0:
            raise ValueError("birth_tick must be >= 0")

    @property
    def entity_type(self) -> EntityType:
        return EntityType.ORGANISM

    @property
    def is_alive(self) -> bool:
        """Return True if this organism has positive energy."""

        return self.energy > 0

    @property
    def phenotype(self) -> Phenotype:
        """Computed phenotype derived from this organism's genome."""

        return Phenotype.from_genome(self.genome)

    def tick(self) -> int:
        """Advance organism internal age by one tick and return new age."""

        self.age += 1
        return self.age


def create_organism(
    position: Position,
    energy: int,
    *,
    id: EntityId | None = None,
    rng: RandomSource | None = None,
    # Lineage tracking (P2.03)
    parent_id: EntityId | None = None,
    lineage_id: EntityId | None = None,
    generation: int | None = None,
    birth_tick: int = 0,
) -> Organism:
    """Factory for creating an Organism with a valid ID.

    If *id* is provided, it is used directly.
    Else if *rng* is provided, the ID is generated deterministically from it.
    Else a non-deterministic ID is generated.

    Lineage rules:
    - If *parent_id* is None, organism is considered an initial organism:
      generation defaults to 0 and lineage_id defaults to its own id.
    - If *parent_id* is provided, lineage_id defaults to *lineage_id* argument
      (typically parent's lineage_id) and generation defaults to parent+1 (must
      be provided via *generation*).

    Note: this factory does not look up the parent organism; callers must pass
    the appropriate lineage_id/generation when creating offspring.
    """

    resolved_id = generate_id(rng) if id is None else id

    if parent_id is None:
        resolved_generation = 0 if generation is None else generation
        resolved_lineage_id = resolved_id if lineage_id is None else lineage_id
    else:
        resolved_generation = 0 if generation is None else generation
        if lineage_id is None:
            raise ValueError("lineage_id must be provided when parent_id is set")
        resolved_lineage_id = lineage_id

    return Organism(
        position=position,
        energy=energy,
        age=0,
        id=resolved_id,
        parent_id=parent_id,
        lineage_id=resolved_lineage_id,
        generation=resolved_generation,
        birth_tick=birth_tick,
    )
