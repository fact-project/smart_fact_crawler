from os import path
import smart_fact_crawler as sfc
from datetime import datetime
from pytest import raises


def test_is_install_folder_a_directory():
    dir_ = path.dirname(sfc.__file__)
    assert path.isdir(dir_)


def test_can_find_resource_folder():
    dir_ = path.join(
        path.dirname(sfc.__file__),
        'resources')
    assert path.isdir(dir_)


def test_can_find_a_testfilefolder():
    dir_ = path.join(
        path.dirname(sfc.__file__),
        'resources',
        '20160703_233149',
        )
    assert path.isdir(dir_)


def test_smartfact():
    sfc.smartfacturl = 'file:' + path.join(
        path.dirname(sfc.__file__),
        'resources',
        '20160703_233149',
        )

    sfc.smartfact()


def test_timestamp_dates():
    sfc.smartfacturl = 'file:' + path.join(
        path.dirname(sfc.__file__),
        'resources',
        '20160703_233149',
        )
    test_date = datetime(2016, 7, 3).date()

    complete = sfc.smartfact()

    for page_name in complete._asdict():
        page = complete._asdict()[page_name]
        for row_name in page._asdict():
            row = page._asdict()[row_name]
            if 'timestamp' in row_name:
                assert row.date() == test_date


def test_broken_page():
    test_file_dir = path.join(
        path.dirname(sfc.__file__),
        'resources',
        '20160703_233149_broken_fsc',
        )
    sfc.smartfacturl = 'file:' + test_file_dir

    with raises(IndexError):
        sfc.camera_climate()


def test_text_in_exception():
    test_file_dir = path.join(
        path.dirname(sfc.__file__),
        'resources',
        '20160703_233149_broken_fsc',
        )
    test_file_content = open(
        path.join(test_file_dir, 'fsc.data')
        ).read()
    sfc.smartfacturl = 'file:' + test_file_dir

    with raises(IndexError) as excinfo:
        sfc.camera_climate()

    message = excinfo.value.args[0]
    print(message)
    assert "text:" in message
    assert test_file_content in message


def test_broken_page_fallback():
    sfc.smartfacturl = 'file:' + path.join(
        path.dirname(sfc.__file__),
        'resources',
        '20160703_233149_broken_fsc',
        )

    sfc.camera_climate(fallback=True)


def test_source_name():
    sfc.smartfacturl = 'file:' + path.join(
        path.dirname(sfc.__file__),
        'resources',
        '20160703_233149',
        )

    assert sfc.current_source().name == 'Mrk 501'
    assert sfc.drive_tracking().source_name == 'Mrk 501'
