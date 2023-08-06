from setuptools import setup, find_packages
import codecs
import os

VERSION = '2.0.4'
DESCRIPTION = 'PythonTutorial'
LONG_DESCRIPTION = 'A package to find area of different figures'

# Setting up
setup(
    name="shahgame",
    version=VERSION,
    author="Shahmir Khan",
    author_email="ShahKhan@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['Guesture', 'Game', 'Controller of figs', 'area', 'developergautam'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)