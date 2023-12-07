import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0'
DESCRIPTION = 'AutoGenius is an agent framework.'
LONG_DESCRIPTION = "AutoGenius is an agent framework that is designed for large-scale agent groups and ultra-long workflows."

setup(
    name="pyautogan",
    version="0.1",
    author="boweniac",
    author_email="boweniac@yeah.net",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['python','chatgpt', 'agent'],
    install_requires=[
        'tiktoken',
        'python-docx',
        'wolframalpha',
        'openpyxl',
        'pandas',
        'PyPDF2',
        'matplotlib',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
    ]
)
