import dbt.flags as flags
from dbt.adapters.sas.impl import SasAdapter
from dbt.adapters.sas.credentials import SasCredentials
from dbt.adapters.sas.connections import SasConnectionManager
from dbt.adapters.sas.relation import SasRelation
from dbt.contracts.connection import Connection
from dbt.config.profile import read_profile
from dbt.config import RuntimeConfig
from dbt.adapters.factory import FACTORY

# FACTORY.load_plugin('sas')
profile_name = "dbt_sas"
profiles = read_profile(flags.PROFILES_DIR)
profile = profiles[profile_name]
target = profile["target"]
config = profile["outputs"][target]

credentials = SasCredentials(
    # handler="ws",
    host=config["host"],
    port=config["port"],
    username=config["user"],
    password=config["password"],
    autoexec=config.get("autoexec"),
    lib_base_path=config.get("lib_base_path"),
    schema="WORK",
)


class TestArgs:
    def __init__(self):
        self.which = "run"
        self.single_threaded = False
        self.profiles_dir = flags.PROFILES_DIR
        self.project_dir = "example"
        self.profile = None
        self.target = target


config = RuntimeConfig.from_args(TestArgs())
a = SasAdapter(config)
FACTORY.adapters["sas"] = a

connection = Connection(type="sas", name=None, credentials=credentials)
cm = SasConnectionManager(profile="sas")
cm.open(connection)
a.connections.set_thread_connection(connection)


def r(table):
    schema, identifier = table.split(".")
    return SasRelation.create(schema=schema, identifier=identifier)


# from dbt.adapters.sas.data import SASdata
# print("SASdata(con.handle, "movies", "video")")

print('a.list_schemas("")')
print('a.list_relations(database="", schema="TEST123")')
print('a.get_columns_in_relation(r("TEST123.TEST1"))')
