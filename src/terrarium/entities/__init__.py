"""Entity definitions.

This subpackage contains entity interfaces and (optionally) concrete entity
types such as organisms and resources.
"""

from __future__ import annotations

from .base import BaseEntity, Entity, EntityId, EntityType, generate_id
from .genome import DEFAULT_GENOME, Genome
from .mutation import MutationConfig, mutate_genome
from .organism import Organism, create_organism
from .phenotype import Phenotype
from .resource import Resource, create_resource

__all__ = [
    "BaseEntity",
    "Entity",
    "EntityId",
    "EntityType",
    "generate_id",
    "Genome",
    "DEFAULT_GENOME",
    "MutationConfig",
    "mutate_genome",
    "Phenotype",
    "Organism",
    "create_organism",
    "Resource",
    "create_resource",
]
