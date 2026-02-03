from __future__ import annotations


def test_package_importable() -> None:
    import terrarium

    assert terrarium.__name__ == "terrarium"
