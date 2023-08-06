import pytest
import dbt.flags as flags
from dbt.config.profile import read_profile

# Import the standard functional fixtures as a plugin
# Note: fixtures with session scope need to be local
pytest_plugins = ["dbt.tests.fixtures.project"]

PROFILE_NANE = "dbt_sas"
profile = read_profile(flags.PROFILES_DIR)[PROFILE_NANE]
target = profile["target"]
config = profile["outputs"][target]


@pytest.fixture(scope="class")
def dbt_profile_target():
    return {
        "host": config["host"],
        "port": config["port"],
        "username": config["user"],
        "password": config["password"],
        "autoexec": config.get("autoexec"),
        "lib_base_path": config.get("lib_base_path"),
        "schema": "WORK",
        "type": "sas",
        "handler": "ws",
        "fail_on_warnings": True,
        "threads": 1,
    }


@pytest.fixture(scope="class")
def unique_schema(request, prefix) -> str:
    return "dbt_test"
