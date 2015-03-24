import pip
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
                  'shmir = shmir:run\n'
                  'shmir-db-manage = shmir.data.migration.cli:main\n'
                  'shmir-db-seed = shmir.data.cli:main'),
    install_requires=[
        str(package.req)
        for package in pip.req.parse_requirements(
            'requirements.txt', session=pip.download.PipSession())
    ],
    test_suite='shmir.tests',
)
