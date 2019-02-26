from pkg_resources import resource_filename
from freezegun import freeze_time
from datetime import datetime

test_file = resource_filename(
    'smart_fact_crawler', 'resources/20160703_233149/observations.data'
)


def test_re():
    from smart_fact_crawler import run_re

    with open(test_file) as f:
        m = run_re.findall(f.read())

    assert len(m) == 67

    timestamp, run_type, source, run_id = m[0]

    assert timestamp == '23:31:27'
    assert run_type == 'data'
    assert source == 'Mrk 501'
    assert run_id == '67'


def test_source_names():
    from smart_fact_crawler import run_re

    all_fact_source_names = [
        'Moon',
        'Mrk 421',
        'Mrk 501',
        '1ES 2344+51.4',
        'PKS 2155-304',
        'Crab',
        'H 1426+428',
        '1ES 1959+650',
        '1ES 1218+304',
        'IC 310',
        '1H0323+342',
        'RGB J0521.8+2112',
        'PKS 0736+01',
        'V404 Cyg',
    ]

    template = '06:06:38 <#darkgreen>data [{name}] (Run 186)</#>'

    for name in all_fact_source_names:
        data = template.format(name=name)

        m = run_re.match(data)
        assert m is not None
        assert m.groups()[2] == name



@freeze_time('2016-07-03 23:32')
def test_build_run():
    from smart_fact_crawler import run_re, build_run

    with open(test_file) as f:
        m = run_re.findall(f.read())

    run = build_run(m[0])

    assert run.id == 67
    assert run.start == datetime(2016, 7, 3, 23, 31, 27)


@freeze_time('2016-07-04 00:32')
def test_build_run_after_midnight():
    from smart_fact_crawler import run_re, build_run

    with open(test_file) as f:
        m = run_re.findall(f.read())

    run = build_run(m[0])

    assert run.id == 67
    assert run.start == datetime(2016, 7, 3, 23, 31, 27)


@freeze_time('2016-07-03 23:32')
def test_observations():
    from smart_fact_crawler import observations

    obs = observations(url='file:' + test_file)

    assert obs.runs[-1].id == len(obs.runs)
