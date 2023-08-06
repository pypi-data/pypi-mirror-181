def test_import_connections():
    from dbt.adapters.sas import connections

    assert connections


def test_import_credentials():
    from dbt.adapters.sas import credentials

    assert credentials


def test_import_impl():
    from dbt.adapters.sas import impl

    assert impl


def test_import_relation():
    from dbt.adapters.sas import relation

    assert relation


def test_import_whereis():
    from dbt.adapters.sas import whereis

    assert whereis


def test_import_utils():
    from dbt.adapters.sas import utils

    assert utils


def test_import_column():
    from dbt.adapters.sas import column

    assert column
    assert isinstance(column.TEXT, str)
    assert "varchar" in column.STRING_DATATYPES
    assert "int" in column.INTEGER_DATATYPES
    assert "varchar(10)" == column.SasColumn.string_type(10)


def test_import_sas_macros():
    from dbt.adapters.sas import sas_macros

    for key in sas_macros.__all__:
        if key.isupper():
            value = getattr(sas_macros, key)
            assert value
            assert isinstance(value, str)
