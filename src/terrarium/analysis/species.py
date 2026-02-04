from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, NewType, Sequence, Tuple

from terrarium.entities.genome import Genome
from terrarium.entities.organism import Organism


SpeciesId = NewType("SpeciesId", int)


def genome_distance(g1: Genome, g2: Genome) -> float:
    """Compute Euclidean distance between two genomes in gene-value space."""

    # Keep deterministic and explicit ordering over known Genome fields.
    v1 = (
        float(g1.speed),
        float(g1.sense_range),
        float(g1.metabolism),
        float(g1.reproduction_threshold),
    )
    v2 = (
        float(g2.speed),
        float(g2.sense_range),
        float(g2.metabolism),
        float(g2.reproduction_threshold),
    )
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


@dataclass(slots=True)
class _Species:
    species_id: SpeciesId
    representative: Genome
    population: int = 0


class SpeciesClassifier:
    """Deterministic, threshold-based genome clustering.

    Clustering rule:
    - organisms within distance <= threshold of an existing species representative
      are assigned that species.
    - otherwise a new species is created.

    Determinism:
    - species IDs are assigned incrementally in first-seen order.
    - for ties (equal distance), the smallest species_id wins.
    """

    def __init__(self, *, threshold: float = 0.3):
        self.threshold = float(threshold)
        self._species: List[_Species] = []
        self._by_organism: Dict[object, SpeciesId] = {}
        self._next_id: int = 0

    @property
    def species_count(self) -> int:
        return len(self._species)

    def classify(self, organism: Organism) -> SpeciesId:
        """Assign and return a stable species id for *organism*.

        The same organism instance/id will always return the same SpeciesId
        for this classifier instance.
        """

        # Organism.id should always be set, but keep it robust.
        key: object = organism.id if organism.id is not None else id(organism)
        existing = self._by_organism.get(key)
        if existing is not None:
            return existing

        if not self._species:
            sid = SpeciesId(self._next_id)
            self._next_id += 1
            sp = _Species(species_id=sid, representative=organism.genome, population=1)
            self._species.append(sp)
            self._by_organism[key] = sid
            return sid

        # Find best matching species within threshold.
        best: Tuple[float, int] | None = None  # (distance, index)
        for idx, sp in enumerate(self._species):
            d = genome_distance(organism.genome, sp.representative)
            if d <= self.threshold:
                cand = (d, idx)
                if best is None:
                    best = cand
                else:
                    # Prefer smaller distance; for equal distance prefer smaller species id
                    if cand[0] < best[0]:
                        best = cand
                    elif cand[0] == best[0]:
                        if self._species[cand[1]].species_id < self._species[best[1]].species_id:
                            best = cand

        if best is None:
            sid = SpeciesId(self._next_id)
            self._next_id += 1
            sp = _Species(species_id=sid, representative=organism.genome, population=1)
            self._species.append(sp)
            self._by_organism[key] = sid
            return sid

        _, best_idx = best
        self._species[best_idx].population += 1
        sid = self._species[best_idx].species_id
        self._by_organism[key] = sid
        return sid

    def get_population(self, species_id: SpeciesId) -> int:
        for sp in self._species:
            if sp.species_id == species_id:
                return int(sp.population)
        return 0


def cluster_by_genome(
    organisms: Iterable[Organism], *, threshold: float = 0.3
) -> Dict[SpeciesId, List[Organism]]:
    """Convenience helper to cluster a batch of organisms by genome."""

    classifier = SpeciesClassifier(threshold=threshold)
    clusters: Dict[SpeciesId, List[Organism]] = {}
    for o in organisms:
        sid = classifier.classify(o)
        clusters.setdefault(sid, []).append(o)
    return clusters
