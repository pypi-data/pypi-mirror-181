from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'Pretty print for Python'
LONG_DESCRIPTION = 'Python package for having a prettier console output/input.'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="consoleplus",
    version=VERSION,
    license="General Public License v3.0",
    author="Evie",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'console', 'output', 'input', 'pretty', 'print']
)