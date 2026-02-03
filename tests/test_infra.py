def test_sanity_check():
    assert True


def test_fixture_available(workdir):
    # Ensures our shared conftest fixture is discoverable/injectable.
    assert workdir.exists()
    assert workdir.is_dir()
