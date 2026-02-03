from __future__ import annotations

from functools import cached_property

from terrarium.engine.rng import SeededRNG
from terrarium.entities.base import EntityId, EntityType, generate_id, generate_id_from_rng
from terrarium.entities.genome import DEFAULT_GENOME, Genome
from terrarium.entities.phenotype import Phenotype
from terrarium.world.grid import Position


class Organism:
    """A living, mutable agent.

    Organisms have mutable state: position, energy, and age.

    Lineage tracking fields are immutable once set:
    - parent_id: immediate parent (or None for initial organisms)
    - lineage_id: stable identifier for the lineage (typically the original ancestor's id)
    - generation: 0 for initial organisms, parent.generation + 1 for offspring
    - birth_tick: simulation tick when created (caller-provided)
    """

    def __init__(
        self,
        position: Position,
        energy: int,
        *,
        id: EntityId | None = None,
        rng: SeededRNG | None = None,
        genome: Genome | None = None,
        parent_id: EntityId | None = None,
        lineage_id: EntityId | None = None,
        generation: int | None = None,
        birth_tick: int = 0,
    ) -> None:
        if id is None:
            if rng is not None:
                self._id = generate_id_from_rng(rng)
            else:
                self._id = generate_id()
        else:
            self._id = id

        self._position: Position = position
        self._energy: int = int(energy)
        if self._energy < 0:
            raise ValueError("energy must be a non-negative integer")
        self._age: int = 0

        self._genome: Genome = genome if genome is not None else DEFAULT_GENOME

        # Lineage fields (immutable)
        self._parent_id: EntityId | None = parent_id
        self._lineage_id: EntityId = lineage_id if lineage_id is not None else self._id
        if generation is None:
            self._generation = 0 if parent_id is None else 1
        else:
            self._generation = int(generation)
        if self._generation < 0:
            raise ValueError("generation must be a non-negative integer")
        self._birth_tick: int = int(birth_tick)
        if self._birth_tick < 0:
            raise ValueError("birth_tick must be a non-negative integer")

    @property
    def id(self) -> EntityId:
        return self._id

    @property
    def parent_id(self) -> EntityId | None:
        return self._parent_id

    @property
    def lineage_id(self) -> EntityId:
        return self._lineage_id

    @property
    def generation(self) -> int:
        return self._generation

    @property
    def birth_tick(self) -> int:
        return self._birth_tick

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, value: Position) -> None:
        self._position = value

    @property
    def entity_type(self) -> EntityType:
        return EntityType.ORGANISM

    @property
    def energy(self) -> int:
        return self._energy

    @energy.setter
    def energy(self, value: int) -> None:
        v = int(value)
        if v < 0:
            raise ValueError("energy must be a non-negative integer")
        self._energy = v

    @property
    def age(self) -> int:
        return self._age

    @property
    def is_alive(self) -> bool:
        return self._energy > 0

    @property
    def genome(self) -> Genome:
        return self._genome

    @cached_property
    def phenotype(self) -> Phenotype:
        """Return this organism's derived phenotype.

        The phenotype is deterministic given the genome and is cached immutably.
        """

        return Phenotype.from_genome(self._genome)

    def tick(self) -> int:
        """Advance organism age by one tick and return new age."""

        self._age += 1
        return self._age


def create_organism(
    position: Position,
    energy: int,
    *,
    id: EntityId | None = None,
    parent_id: EntityId | None = None,
    lineage_id: EntityId | None = None,
    generation: int | None = None,
    birth_tick: int = 0,
) -> Organism:
    """Factory for Organism with generated id if not provided.

    Lineage fields are optional for backwards compatibility.

    Notes
    -----
    - If lineage_id is not provided, it defaults to the organism's id (initial organism).
    - If generation is not provided, it defaults to 0 if parent_id is None, else 1.
    """

    return Organism(
        position=position,
        energy=energy,
        id=id,
        parent_id=parent_id,
        lineage_id=lineage_id,
        generation=generation,
        birth_tick=birth_tick,
    )
