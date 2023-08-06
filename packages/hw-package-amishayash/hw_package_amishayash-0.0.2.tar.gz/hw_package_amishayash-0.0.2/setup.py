from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'First Package made by Amisha and Yash'
LONG_DESCRIPTION = 'A package that runs tests to check whether all text files contains the substring sample'

# Setting up
setup(
    name="hw_package_amishayash",
    version=VERSION,
    author="yash19130 (Yash Tanwar)",
    author_email="<yash19130@iiitd.ac.in>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'tests', 'package', 'assertions', 'runner', 'os'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)