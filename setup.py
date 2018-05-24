from setuptools import setup


setup(
    name='smart_fact_crawler',
    version='0.6.0',
    description='acquire data published on the smartfact web page',
    url='https://github.com/fact-project/smart_fact_crawler.git',
    author='Dominik Neise, Sebastian Mueller, Maximilian Nöthe',
    author_email='sebmuell@phys.ethz.ch',
    license='MIT',
    packages=[
        'smart_fact_crawler',
    ],
    package_data={
        'smart_fact_crawler': [
            'resources/20160703_233149/*.data',
            'resources/20160703_233149_broken_fsc/fsc.data',
        ]
    },
    install_requires=[
        'requests',
    ],
    tests_require=['pytest>=3.0', 'freezegun'],
    setup_requires=['pytest-runner'],
    zip_safe=True,
)
