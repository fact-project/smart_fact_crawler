from os import path
from datetime import datetime

from pytest import raises
import pytest

@pytest.fixture
def sfc():
    import smart_fact_crawler as sfc
    dir_ = path.join(
        path.dirname(sfc.__file__),
        'resources',
        '20160703_233149',
        )
    assert path.isdir(dir_)
    sfc.smartfacturl = 'file:' + dir_
    return sfc

@pytest.fixture
def broken_fsc():
    import smart_fact_crawler as sfc
    dir_ = path.join(
        path.dirname(sfc.__file__),
        'resources',
        '20160703_233149_broken_fsc',
        )
    assert path.isdir(dir_)
    sfc.smartfacturl = 'file:' + dir_
    return sfc

def test_is_install_folder_a_directory():
    import smart_fact_crawler as sfc
    dir_ = path.dirname(sfc.__file__)
    assert path.isdir(dir_)

def test_can_find_resource_folder():
    import smart_fact_crawler as sfc
    dir_ = path.join(
        path.dirname(sfc.__file__),
        'resources')
    assert path.isdir(dir_)

def test_can_find_a_testfilefolder():
    import smart_fact_crawler as sfc
    dir_ = path.join(
        path.dirname(sfc.__file__),
        'resources',
        '20160703_233149',
        )
    assert path.isdir(dir_)

def test_smartfact(sfc):
    
    sfc.smartfact()

def test_timestamp_dates(sfc):
    test_date = datetime(2016, 7, 3).date()
    
    complete = sfc.smartfact()

    for page_name in complete._asdict():
        page = complete._asdict()[page_name]
        for row_name in page._asdict():
            row = page._asdict()[row_name]            
            if 'timestamp' in row_name:
                assert row.date() == test_date


def test_broken_page(broken_fsc):
    with raises(IndexError):
        broken_fsc.camera_climate()

def test_source_name(sfc):

    assert sfc.current_source().name == 'Mrk 501'
    assert sfc.drive_tracking().source_name == 'Mrk 501'