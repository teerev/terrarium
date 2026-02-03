from __future__ import annotations

from terrarium.metrics.population import compute_population_stats


class _Org:
    def __init__(self, *, age: int, energy: int) -> None:
        self.age = age
        self.energy = energy


def test_compute_population_stats_empty() -> None:
    stats = compute_population_stats([])
    assert stats == {
        "age_min": None,
        "age_max": None,
        "age_mean": None,
        "energy_min": None,
        "energy_max": None,
        "energy_mean": None,
    }


def test_compute_population_stats_values() -> None:
    organisms = [_Org(age=1, energy=10), _Org(age=3, energy=5)]
    stats = compute_population_stats(organisms)

    assert stats["age_min"] == 1.0
    assert stats["age_max"] == 3.0
    assert stats["age_mean"] == 2.0

    assert stats["energy_min"] == 5.0
    assert stats["energy_max"] == 10.0
    assert stats["energy_mean"] == 7.5
