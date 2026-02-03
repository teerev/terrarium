import terrarium


def test_version_is_defined() -> None:
    assert isinstance(terrarium.__version__, str)
    assert terrarium.__version__
    assert terrarium.__version__ == "0.1.0"
