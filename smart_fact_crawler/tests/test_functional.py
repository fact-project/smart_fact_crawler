from os import path
import smart_fact_crawler as sfc
from datetime import datetime
from pytest import raises, approx

test_dir = '2019_10_03_1531/data'


def test_is_install_folder_a_directory():
    dir_ = path.dirname(sfc.__file__)
    assert path.isdir(dir_)


def test_can_find_resource_folder():
    dir_ = path.join(
        path.dirname(sfc.__file__),
        'resources'
    )
    assert path.isdir(dir_)


def test_can_find_a_testfilefolder():
    dir_ = path.join(
        path.dirname(sfc.__file__),
        'resources',
        test_dir,
    )
    assert path.isdir(dir_)


def test_smartfact():
    sfc.smartfacturl = 'file:' + path.join(
        path.dirname(sfc.__file__),
        'resources',
        test_dir,
    )

    sfc.smartfact()


def test_timestamp_dates():
    sfc.smartfacturl = 'file:' + path.join(
        path.dirname(sfc.__file__),
        'resources',
        test_dir,
    )
    test_date = datetime(2019, 10, 3).date()

    complete = sfc.smartfact()

    for page_name in complete._asdict():
        page = complete._asdict()[page_name]

        # the sqm was broken and hence not up to date
        # the test data is not from during data taking
        # so errorhist is from the day before
        # tng_weather is also broken
        if page_name in ('sqm', 'errorhist', 'tng_weather'):
            continue

        for row_name in page._asdict():
            row = page._asdict()[row_name]
            if 'timestamp' in row_name:
                assert row.date() == test_date


def test_broken_page():
    sfc.smartfacturl = 'file:' + path.join(
        path.dirname(sfc.__file__),
        'resources',
        '20160703_233149_broken_fsc',
    )

    with raises(IndexError):
        sfc.camera_climate()


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
        test_dir,
    )

    assert sfc.current_source().name == 'Park'
    assert sfc.drive_tracking().source_name == ''


def test_weather_gtc_dust():
    sfc.smartfacturl = 'file:' + path.join(
        path.dirname(sfc.__file__),
        'resources',
        test_dir,
    )

    weather = sfc.weather()
    assert weather.dust_gtc.value == approx(19.2, abs=1e-1)
