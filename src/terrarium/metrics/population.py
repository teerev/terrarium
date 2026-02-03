from __future__ import annotations

import statistics
from typing import Any, Iterable


def compute_population_stats(organisms: Iterable[Any]) -> dict[str, float | None]:
    """Compute basic population statistics.

    Expects each organism to expose numeric ``age`` and ``energy`` attributes.

    For empty input, returns a dict with all values set to None.
    """

    org_list = list(organisms)
    if not org_list:
        return {
            "age_min": None,
            "age_max": None,
            "age_mean": None,
            "energy_min": None,
            "energy_max": None,
            "energy_mean": None,
        }

    ages = [float(getattr(o, "age")) for o in org_list]
    energies = [float(getattr(o, "energy")) for o in org_list]

    return {
        "age_min": float(min(ages)),
        "age_max": float(max(ages)),
        "age_mean": float(statistics.mean(ages)),
        "energy_min": float(min(energies)),
        "energy_max": float(max(energies)),
        "energy_mean": float(statistics.mean(energies)),
    }
