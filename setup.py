from setuptools import setup, find_packages

setup(
    name='shmir',
    version='2.0',
    author=('Sylwester Brzeczkowski, Mateusz Flieger, Piotr Rogulski, '
            'Michal Rostecki, Martyna Urbanek'),
    package_dir={'': 'src'},
    package_data={'': ['structures/*']},
    packages=find_packages('src'),
    entry_points=('[console_scripts]\n'
                  'shmir = shmir:run'),
    install_requires=[
        'Flask==0.10.1',
        'psycopg2==2.5.2',
        'sqlalchemy==0.9.2',
        'Twisted==13.2.0',
        'celery==3.1.11'
    ],
    test_suite='shmir.tests',
)
