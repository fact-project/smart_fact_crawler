from distutils.core import setup


setup(
    name='smart_fact_crawler',
    version='0.1.2',
    description='acquieres data published on the smartfact web page',
    url='https://github.com/fact-project/smart_fact_crawler.git',
    author='Dominik Neise, Sebastian Mueller',
    author_email='sebmuell@phys.ethz.ch',
    license='MIT',
    packages=[
        'smart_fact_crawler',
    ],
    install_requires=[
        'requests',
        'python-dateutil',
    ],
    zip_safe=True,
)
