from setuptools import setup

extras_require = {
    "tests": ['pytest>=3.0', 'freezegun'],
}
extras_require['all'] = extras_require['tests']



setup(
    name='smart_fact_crawler',
    version='0.7.0',
    description='acquire data published on the smartfact web page',
    url='https://github.com/fact-project/smart_fact_crawler.git',
    author='Dominik Neise, Sebastian Mueller, Maximilian Nöthe',
    author_email='sebmuell@phys.ethz.ch',
    license='MIT',
    packages=[
        'smart_fact_crawler',
    ],
    install_requires=[
        'requests',
    ],
    include_package_data=True,
    package_data={
        'smart_fact_crawler': ['resources/*'],
    },
    extras_require=extras_require,
    zip_safe=False,
)
