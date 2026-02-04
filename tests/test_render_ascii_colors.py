from __future__ import annotations

from terrarium.render.ascii import ColorScheme, render_world_ascii


def _world_snapshot(*, energy: int = 1, age: int = 0, species: str = "spA") -> dict:
    return {
        "tick": 1,
        "grid": {"width": 3, "height": 2},
        "entities": [
            {"id": "o1", "type": "organism", "position": [1, 0], "energy": energy, "age": age, "species_id": species},
            {"id": "r1", "type": "resource", "position": [0, 1], "energy_value": 1, "consumed": False},
        ],
    }


def test_render_world_ascii_no_color_contains_no_ansi() -> None:
    world = _world_snapshot(energy=1)
    out = render_world_ascii(world, color=False)
    assert "\033[" not in out
    assert "O" in out


def test_render_world_ascii_color_energy_thresholds() -> None:
    scheme = ColorScheme(energy_low="LOW", energy_mid="MID", energy_high="HIGH", reset="R")

    # low (< 25%)
    out_low = render_world_ascii(_world_snapshot(energy=1), color=True, color_by="energy", color_scheme=scheme, max_energy=10)
    assert "LOWOR" in out_low

    # mid (< 50%)
    out_mid = render_world_ascii(_world_snapshot(energy=3), color=True, color_by="energy", color_scheme=scheme, max_energy=10)
    assert "MIDOR" in out_mid

    # high (>= 50%)
    out_high = render_world_ascii(_world_snapshot(energy=7), color=True, color_by="energy", color_scheme=scheme, max_energy=10)
    assert "HIGHOR" in out_high


def test_render_world_ascii_color_by_species_is_stable_for_key() -> None:
    scheme = ColorScheme(species_cycle=("C0", "C1", "C2"), reset="R")

    w1 = _world_snapshot(energy=5, species="same")
    w2 = _world_snapshot(energy=9, species="same")

    out1 = render_world_ascii(w1, color=True, color_by="species", color_scheme=scheme)
    out2 = render_world_ascii(w2, color=True, color_by="species", color_scheme=scheme)

    # Same species key should map to same color prefix.
    assert any(prefix + "O" + scheme.reset in out1 for prefix in scheme.species_cycle)
    for prefix in scheme.species_cycle:
        token = prefix + "O" + scheme.reset
        if token in out1:
            assert token in out2
            break


def test_render_world_ascii_color_by_age() -> None:
    scheme = ColorScheme(age_young="Y", age_old="O", reset="R")

    out_young = render_world_ascii(_world_snapshot(age=0), color=True, color_by="age", color_scheme=scheme, max_age=10)
    assert "YOR" in out_young

    out_old = render_world_ascii(_world_snapshot(age=9), color=True, color_by="age", color_scheme=scheme, max_age=10)
    assert "OOR" in out_old
