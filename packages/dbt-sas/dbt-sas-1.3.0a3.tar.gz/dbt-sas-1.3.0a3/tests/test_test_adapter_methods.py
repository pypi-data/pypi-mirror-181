import pytest
from dbt.tests.adapter.basic.test_base import BaseSimpleMaterializations
from dbt.tests.adapter.basic.test_singular_tests import BaseSingularTests
from dbt.tests.adapter.basic.test_empty import BaseEmpty
from dbt.tests.adapter.basic.test_incremental import BaseIncremental
from dbt.tests.adapter.basic.test_generic_tests import BaseGenericTests
from dbt.tests.adapter.basic.test_snapshot_check_cols import BaseSnapshotCheckCols
from dbt.tests.adapter.basic.test_snapshot_timestamp import BaseSnapshotTimestamp
from dbt.tests.adapter.basic.test_adapter_methods import BaseAdapterMethod


test_passing_sql = """
select * from (
    select 1 as id
    from dictionary.dictionaries
    where memname='DICTIONARIES' and name='NAME'
) as my_subquery
where id = 2
"""

test_failing_sql = """
select * from (
    select 1 as id
    from dictionary.dictionaries
    where memname='DICTIONARIES' and name='NAME'
) as my_subquery
where id = 1
"""


class TestSimpleMaterializationsMyAdapter(BaseSimpleMaterializations):  # [test passed]
    pass


class TestSingularTestsMyAdapter(BaseSingularTests):  # [test passed]
    @pytest.fixture(scope="class")
    def tests(self):
        return {
            "passing.sql": test_passing_sql,
            "failing.sql": test_failing_sql,
        }

    pass


class TestEmptyMyAdapter(BaseEmpty):  # [test passed]
    pass


class TestGenericTestsMyAdapter(BaseGenericTests):  # [test passed]
    pass


# class TestIncrementalMyAdapter(BaseIncremental):
#     pass
#
#
# class TestSnapshotCheckColsMyAdapter(BaseSnapshotCheckCols):  # several errors.
#     pass
#
#
# class TestSnapshotTimestampMyAdapter(BaseSnapshotTimestamp):
#     pass
#

models__upstream_sql = """
select 1 as id
from dictionary.dictionaries
where memname='DICTIONARIES' and name='NAME'
"""

models__expected_sql = """
-- make sure this runs after 'model'
-- {{ ref('model') }}
select 2 as id
from dictionary.dictionaries
where memname='DICTIONARIES' and name='NAME'
"""

models__model_sql = """

{% set upstream = ref('upstream') %}

{% if execute %}
    {# don't ever do any of this #}
    {%- do adapter.drop_schema(upstream) -%}
    {% set existing = adapter.get_relation(upstream.database, upstream.schema, upstream.identifier) %}
    {% if existing is not none %}
        {% do exceptions.raise_compiler_error('expected ' ~ ' to not exist, but it did') %}
    {% endif %}

    {%- do adapter.create_schema(upstream) -%}

    {% set sql = create_view_as(upstream, "select 2 as id from dictionary.dictionaries where memname='DICTIONARIES' and name='NAME'") %}
    {% do run_query(sql) %}
{% endif %}


select * from {{ upstream }}

"""

# class TestBaseAdapterMethod(BaseAdapterMethod):
#     @pytest.fixture(scope="class")
#     def models(self):
#         return {
#             "upstream.sql": models__upstream_sql,
#             "expected.sql": models__expected_sql,
#             "model.sql": models__model_sql,
#         }
