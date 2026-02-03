from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, NewType, Sequence

from terrarium.entities.genome import Genome
from terrarium.entities.organism import Organism


SpeciesId = NewType("SpeciesId", int)


def genome_distance(g1: Genome, g2: Genome) -> float:
    """Euclidean distance between two genomes in gene-value space."""

    dx_speed = float(g1.speed) - float(g2.speed)
    dx_sense = float(g1.sense_range) - float(g2.sense_range)
    dx_met = float(g1.metabolism) - float(g2.metabolism)
    dx_rep = float(g1.reproduction_threshold) - float(g2.reproduction_threshold)

    return float(
        math.sqrt(
            dx_speed * dx_speed
            + dx_sense * dx_sense
            + dx_met * dx_met
            + dx_rep * dx_rep
        )
    )


@dataclass(frozen=True, slots=True)
class _Species:
    id: SpeciesId
    representative: Genome


class SpeciesClassifier:
    """Deterministic threshold-based species classifier.

    Design
    ------
    - Each species has a representative genome (first organism assigned).
    - An organism is assigned to the first species (lowest id) whose
      representative is within the distance threshold.
    - Otherwise, a new species is created.
    - Population counts are tracked for assignments made via this classifier.

    Notes
    -----
    Species IDs are stable within a simulation run (this classifier instance).
    """

    def __init__(self, *, threshold: float = 0.3) -> None:
        self._threshold = float(threshold)
        if self._threshold < 0.0:
            raise ValueError("threshold must be non-negative")

        self._species: List[_Species] = []
        self._populations: Dict[SpeciesId, int] = {}

    @property
    def species_count(self) -> int:
        return len(self._species)

    def classify(self, organism: Organism) -> SpeciesId:
        """Assign *organism* to a species and increment population count."""

        g = organism.genome

        for sp in self._species:
            if genome_distance(g, sp.representative) <= self._threshold:
                self._populations[sp.id] = int(self._populations.get(sp.id, 0)) + 1
                return sp.id

        # Create new species deterministically at next integer id.
        new_id = SpeciesId(len(self._species))
        self._species.append(_Species(id=new_id, representative=g))
        self._populations[new_id] = int(self._populations.get(new_id, 0)) + 1
        return new_id

    def get_population(self, species_id: SpeciesId) -> int:
        return int(self._populations.get(species_id, 0))


def cluster_by_genome(
    organisms: Sequence[Organism] | Iterable[Organism], *, threshold: float = 0.3
) -> Dict[SpeciesId, List[Organism]]:
    """Cluster organisms into species based on genome similarity.

    Returns a mapping from species_id to the organisms assigned to that species.
    Deterministic for a given organism iteration order.
    """

    clf = SpeciesClassifier(threshold=float(threshold))
    out: Dict[SpeciesId, List[Organism]] = {}

    for org in organisms:
        sid = clf.classify(org)
        out.setdefault(sid, []).append(org)

    return out
