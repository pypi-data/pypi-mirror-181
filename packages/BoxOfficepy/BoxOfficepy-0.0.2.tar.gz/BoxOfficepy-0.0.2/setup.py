from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'A Package to get Box Office Revenue'
# Setting up
setup(
    name="BoxOfficepy",
    version=VERSION,
    author="rahul192 (Rahul Raj Singh)",
    author_email="<rahul.raj.singh220899@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['datetime', 'requests', 'pandas', 'requests_html'],
    keywords=['python', 'revenue', 'box office'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)