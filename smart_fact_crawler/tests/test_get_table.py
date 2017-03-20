import pytest

from smart_fact_crawler.tools import get_table_entry


def test_get_entry():

    table = [['hello', 'world']]

    assert get_table_entry(table, 0, 0) == 'hello'
    assert get_table_entry(table, 0, 1) == 'world'


def test_get_entry_raise():

    table = [['hello', 'world']]

    with pytest.raises(IndexError):
        get_table_entry(table, 1, 0)


def test_get_entry_fallback():

    table = [['hello', 'world']]

    assert get_table_entry(table, 1, 0, fallback=True) is None
    assert get_table_entry(table, 1, 0, fallback=True, default=1.0) == 1.0
