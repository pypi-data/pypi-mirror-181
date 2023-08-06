from pathlib import Path
from dbt.adapters.sas.whereis import whereis


def test_whereis():
    assert whereis("env") == Path("/usr/bin/env")


def test_whereis_not_found():
    assert whereis("--not-found--") is None


def test_whereis_none():
    assert whereis(None) is None
