from pathlib import Path
import agate
from dbt.clients.agate_helper import DEFAULT_TYPE_TESTER
from decimal import Decimal
from dbt.adapters.sas.utils import (
    get_temp_filename,
    get_temp_local_filename,
    get_temp_data_set_name,
    path_join,
    agate_table_get_column_values,
)


def test_get_temp_filename():
    t1 = get_temp_filename()
    assert t1
    assert isinstance(t1, str)
    assert t1.startswith("/tmp/")
    t2 = get_temp_filename()
    assert t2
    assert t1 != t2


def test_get_temp_filename_ext():
    t1 = get_temp_filename(ext=".csv")
    assert t1
    assert isinstance(t1, str)
    assert t1.startswith("/tmp/")
    assert t1.endswith(".csv")


def test_get_temp_local_filename():
    t1 = get_temp_local_filename()
    assert t1
    assert isinstance(t1, Path)
    t2 = get_temp_filename()
    assert t2
    assert t1 != t2
    t3 = get_temp_filename(ext=".csv")
    assert t3
    assert isinstance(t3, str)


def test_get_temp_data_set_name():
    for _ in range(0, 10):
        table_name = get_temp_data_set_name()
        assert table_name
        assert isinstance(table_name, str)
        assert len(table_name) <= 32
        assert table_name.upper().startswith("WORK.TMP_")


def test_path_join():
    assert path_join() == ""
    assert path_join(None) == ""
    assert path_join("") == ""
    assert path_join("", "") == ""
    assert path_join("aaa", "bbb") == "aaa/bbb"
    assert path_join("aaa/", "bbb") == "aaa/bbb"
    assert path_join("C:\\some_folder", r"some_file.txt") == "C:\\some_folder\\some_file.txt"
    assert path_join("C:\\some_folder\\", r"some_file.txt") == "C:\\some_folder\\some_file.txt"


def test_agate_table_get_column_values():
    data = [{"a": 1, "b": 2}]
    table = agate.Table.from_object(data, column_types=DEFAULT_TYPE_TESTER)
    assert isinstance(agate_table_get_column_values(table, "a")[0], Decimal)
    assert isinstance(agate_table_get_column_values(table, "b")[0], Decimal)

    data = []
    table = agate.Table.from_object(data, column_types=DEFAULT_TYPE_TESTER)
    assert agate_table_get_column_values(table, "a") == []
