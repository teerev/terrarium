import re


def test_package_importable():
    import terrarium  # noqa: F401


def test_version_defined():
    import terrarium

    assert isinstance(terrarium.__version__, str)
    assert re.fullmatch(r"\d+\.\d+\.\d+", terrarium.__version__) is not None
