
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name='nonholonomics',
    version='0.0.12',
    author='Jamal Ardister',
    author_email='ardiste3@msu.edu',
    description='A collection of tools to used to evaluate dynamical systems with nonholonomic constraints',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ardiste3/nonholonomics',
    project_urls={
        "Bug Tracker": "https://github.com/ardiste3/nonholonomics/issues"
    },
    license='GNU AGPLv3',
    packages=['nonholonomics', 'nonholonomics.NHL',
              'nonholonomics.Simulation'],
    install_requires=['numpy', 'sympy', 'scipy', 'matplotlib'],
)
