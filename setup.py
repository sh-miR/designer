from pip.req import parse_requirements
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
        str(package.req) for package in parse_requirements('requirements.txt')
    ],
    test_suite='shmir.tests',
)
