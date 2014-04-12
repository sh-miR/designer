from setuptools import setup, find_packages

setup(
    name='shmir_api',
    version='2.0',
    author=('Sylwester Brzeczkowski, Mateusz Flieger, Piotr Rogulski, '
            'Michal Rostecki, Martyna Urbanek'),
    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points=('[console_scripts]\n'
                  'shmir = shmir_api.app:run'),
    install_requires=[
        'Flask==0.10.1',
        'psycopg2==2.5.2',
        'sqlalchemy==0.9.2',
        'sqlsoup==0.9.0',
        'Twisted==13.2.0'
    ],
    test_suite='shmir_api.tests',
)
