from setuptools import setup, find_packages

VERSION = '1.1.2'
DESCRIPTION = 'Pretty print for Python'
LONG_DESCRIPTION = 'Python package for having a prettier console output/input. You can view the docs here: https://github.com/timof121/ConsolePlus/wiki'

# Setting up
setup(
    name="consoleplus",
    url="https://github.com/timof121/ConsolePlus",
    version=VERSION,
    license="General Public License v3.0",
    author="Evie",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'console', 'output', 'input', 'pretty', 'print']
)