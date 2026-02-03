from __future__ import annotations

import terrarium


def test_package_version_present() -> None:
    assert isinstance(terrarium.__version__, str)
    assert terrarium.__version__
