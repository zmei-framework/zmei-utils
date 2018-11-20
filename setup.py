#!/usr/bin/env python
from setuptools import find_packages, setup

project = "zmei-utils"
version = "0.1.12"

setup(
    name=project,
    version=version,
    description="Intuitive web-framework, based on rock-solid opensource components.",
    author="Alex Rudakov",
    author_email="ribozz@gmail.com",
    url="https://github.com/Negative Space OU/zmei",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
	    'djangorestframework',
        'django',
        # 'py_mini_racer',
        # 'termcolor',
    ],
    dependency_links=[
    ],
    entry_points={
    },
    tests_require=[
        "djangorestframework",
        "coverage>=3.7.1",
        "mock>=1.0.1",
        "pytest",
    ],
)
