#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='currency',
    version='0.1.0.dev',
    description='A time aware tool to convert currencies.',
    maintainer='Tim Tröndle',
    maintainer_email='tim.troendle@usys.ethz.ch',
    url='https://www.github.com/timtroendle/currency',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        "click >= 6.0"
    ],
    entry_points={
        'console_scripts': [
            'currency=currency.cli:currency',
        ],
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering'
    ]
)
