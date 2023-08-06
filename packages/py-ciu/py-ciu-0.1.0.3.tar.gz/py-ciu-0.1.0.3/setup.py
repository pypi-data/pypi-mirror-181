import pathlib
import sys

from setuptools import setup, find_packages

long_desc = pathlib.Path('README.md').read_text()

if sys.version_info < (3, 6):
    print('CIU requires at least Python 3.6 due to the use of f-strings.')

setup(
    name='py-ciu',
    version='0.1.0.3',
    install_requires=[
        "matplotlib",
        "numpy",
        "pandas",
        "sklearn",
        "xgboost",
        "scikit_learn"
    ],
    url='https://github.com/KaryFramling/py-ciu',
    license='MIT',
    author='Vlad Apopei & Kary Främling',
    author_email='ioan-vlad.apopei@aalto.fi, kary.framling@umu.se',
    description='Python documentation generator',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    project_urls={
        "Code": "https://github.com/KaryFramling/py-ciu",
    },
    platforms='any',
    packages=find_packages(include=['ciu', 'ciu_tests', 'ciu_tests', 'ciu_tests.data']),
    package_data={
        '': ['*.csv'],
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Documentation",
    ],
)
