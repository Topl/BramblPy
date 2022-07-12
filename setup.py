#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import (
    setup,
    find_packages,
)



with open('./README.md') as readme:
    long_description = readme.read()

setup(
    name='brambl',
    # *IMPORTANT*: Don't manually change the version here. Use the 'bumpversion' utility.
    version='0.0.1',
    description=(
        "A library for handling most things affiliated with the Topl Blockchain"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Sterling Wells',
    author_email='info@topl.me',
    url='https://github.com/Topl/BramblPy',
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    keywords='topl',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: MPL2 License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
