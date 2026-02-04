import re


def test_package_importable() -> None:
    import terrarium  # noqa: F401


def test_version_defined() -> None:
    import terrarium

    assert hasattr(terrarium, "__version__")
    assert isinstance(terrarium.__version__, str)
    assert re.fullmatch(r"\d+\.\d+\.\d+", terrarium.__version__)
