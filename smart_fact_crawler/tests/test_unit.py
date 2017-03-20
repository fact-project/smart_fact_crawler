import pytest
import smart_fact_crawler.tools as tools_to_test


def test_extract_run_id_from_system_status_with_existing_run_id():

    contains_run_id = 'data(47) [1169/279s]'
    result = tools_to_test.extract_run_id_from_system_status(contains_run_id)
    assert result == 47


def test_extract_run_id_from_system_status_without_run_id():

    no_run_id = 'Idle [pedestal]'
    result = tools_to_test.extract_run_id_from_system_status(no_run_id)
    assert result is None


def test_extract_run_id_from_system_status_with_list():
    with pytest.raises(TypeError):
        a_list_by_accident = list('data(47) [1169/279s]')
        result = tools_to_test.extract_run_id_from_system_status(
            a_list_by_accident)


def test_extract_run_id_from_system_status_with_None():
    with pytest.raises(TypeError):
        result = tools_to_test.extract_run_id_from_system_status(None)
